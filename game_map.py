from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  
from tcod.console import Console

from entity import Actor, Item, Effect
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, 
        window_width: int, window_height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.window_width, self.window_height = window_width, window_height
        self.entities = set(entities)

        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")
        sel = np.random.random(size=self.tiles.shape)
        sel = (sel >= 0.95)
        self.tiles[sel] = np.full(len(self.tiles[sel]), fill_value=tile_types.floor_star)

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=True, order="F")  # Tiles the player can currently see

        self.system_exit_location = np.full((width, height), fill_value=False, order="F") 

    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def corpses(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and not entity.is_alive
        )

    @property
    def effects(self) -> Iterator[Effect]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Effect) and entity.lifetime_in_turns != 0
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height


    def get_window_coordinates(self, x: int, y: int):
        player = self.engine.player
        x_low = int(player.x-self.window_width/2)
        x_high = int(player.x+self.window_width/2)
        y_low = int(player.y-self.window_height/2)
        y_high = int(player.y+self.window_height/2)
        if x_low <= 0: x_low = 0; x_high = self.window_width
        if y_low <= 0: y_low = 0; y_high = self.window_height

        if x_high >= self.width: x_high = self.width; x_low = self.width - self.window_width
        if y_high >= self.height: y_high = self.height; y_low = self.height - self.window_height

        return x-x_low, y-y_low


    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        player = self.engine.player
        x_low = int(player.x-self.window_width/2)
        x_high = int(player.x+self.window_width/2)
        y_low = int(player.y-self.window_height/2)
        y_high = int(player.y+self.window_height/2)
        if x_low <= 0: x_low = 0; x_high = self.window_width
        if y_low <= 0: y_low = 0; y_high = self.window_height

        if x_high >= self.width: x_high = self.width; x_low = self.width - self.window_width
        if y_high >= self.height: y_high = self.height; y_low = self.height - self.window_height

        console.tiles_rgb[0:self.window_width, 0:self.window_height] = np.select(
            condlist=[self.visible[x_low:x_high,y_low:y_high], self.explored[x_low:x_high,y_low:y_high]],
            choicelist=[self.tiles[x_low:x_high,y_low:y_high]["light"], self.tiles[x_low:x_high,y_low:y_high]["dark"]],
            default=tile_types.SHROUD,
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            # Only print entities that are in the FOV and on screen
            if 0 <= entity.x - x_low <= self.window_width and 0 <= entity.y - y_low <= self.window_height:
                if self.visible[entity.x, entity.y]:
                    console.print(x=entity.x - x_low, y=entity.y - y_low, string=entity.char, fg=entity.color)


class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """

    def __init__(
        self,
        *,
        engine: Engine,
        map_window_width: int,
        map_window_height: int,
        map_width: int,
        map_height: int,
        max_monsters: int,
        min_monsters: int,
        max_items: int,

        current_map: GameMap = None,
        main_map: GameMap = None,
        stellar_systems: Iterable[StellarSystem]=[],

    ):
        self.engine = engine

        self.map_window_width = map_window_width
        self.map_window_height = map_window_height

        self.map_width = map_width
        self.map_height = map_height

        self.max_monsters = max_monsters
        self.min_monsters = min_monsters
        self.max_items = max_items

        self.current_map = current_map
        self.main_map = main_map
        self.stellar_systems = stellar_systems


    def generate_galaxy(self) -> None:
        from procgen import generate_space

        self.main_map, self.stellar_systems = generate_space(
            map_width=self.map_width, 
            map_height=self.map_height, 
            max_monsters=self.max_monsters,
            min_monsters=self.min_monsters,
            max_items=self.max_items,
            engine=self.engine,
            map_window_width=self.map_window_width,
            map_window_height=self.map_window_height,
        )

        self.engine.game_map = self.main_map
        self.current_map = self.main_map

