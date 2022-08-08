from __future__ import annotations

import lzma
import pickle
import numpy as np
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
from message_log import MessageLog
import render_functions
import color

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine(object):
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.index = 0


    def main_turns_cycle(self) -> None:
        actors = set(self.game_map.actors)-{self.player}
        actors = np.array(list(actors)+list(self.game_map.effects))

        if self.index > len(actors):
            self.index -= len(actors)

        # continue where we broke off
        actors = np.concatenate((actors[self.index:], actors[:self.index]))
        

        for i, entity in enumerate(actors):
            entity.action_points += entity.speed
            entity.decide_what_to_do()
            action = entity.stored_action

            while action is not None:

                # if entity ceased to exist before its turn -> skip its turn
                if entity not in list(self.game_map.actors)+list(self.game_map.effects):
                    break

                entity.decide_what_to_do()
                action = entity.get_action()

                if action is None:
                    break

                try:
                    spawned_actor = action.perform()
                    entity.action_points -= action.cost

                    if spawned_actor:
                        actors = np.insert(actors, i+1, spawned_actor)

                except exceptions.Impossible as exc:
                    if entity in set(self.game_map.effects):
                        entity.despawn()

                    entity.stored_action = None
                    break

           
            self.index += 1
    
    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.
    
    def handle_effects_turns(self) -> None:
        for entity in set(self.game_map.effects):
            if not entity.parent.in_bounds(entity.x, entity.y):
                entity.despawn()
            try:
                entity.act()
            except exceptions.Impossible as exc:
                entity.despawn()

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=50,
        )
        # If a tile is "visible" it should be added to "explored".
        #self.game_map.explored |= self.game_map.visible


    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_space_level(
            console=console,
            gameworld=self.game_world,
            location=(0, 47),
        )

        render_functions.render_names_at_mouse_location(console=console, x=21, y=44, engine=self)

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
        