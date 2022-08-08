from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING
import numpy as np

from effects_factory import laser_beam, explosion
import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item, Effect

class SpawnAction:
    def __init__(self, entity: Actor, cost: int = 100) -> None:
        super().__init__()
        self.entity = entity
        self.cost = cost


    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine


    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class ShootAction(SpawnAction):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    def perform(self) -> None:
        projectile = laser_beam.spawn(
            gamemap=self.entity.gamemap, 
            x=self.entity.x, 
            y=self.entity.y,
        )
        projectile.vx=1*self.dx,
        projectile.vy=1*self.dy,
        projectile.origin=self.entity

        if projectile.name == 'laser beam':
            if self.dy == 0:
                projectile.char = '-'

        return projectile


class ExplodeAction(SpawnAction):
    def __init__(self, entity: Actor, cost: int = 0) -> None:
        super().__init__(entity, cost)

    def perform(self) -> None:
        gamemap = self.entity.gamemap
        x_low = int(gamemap.engine.player.x-gamemap.window_width/2)
        y_low = int(gamemap.engine.player.y-gamemap.window_height/2)
        x = range(self.entity.x-1,self.entity.x+2)
        y = range(self.entity.y-1,self.entity.y+2)

        for xi in x:
            for yi in y:
                explosion.spawn(
                    gamemap=self.entity.gamemap,
                    x=xi, 
                    y=yi,
                )

                target = self.entity.gamemap.get_actor_at_location(x=xi,y=yi)
                if target == self.entity:
                    continue
                if target:
                    attack_desc = f"{target.name} gets caught into the explosion" 
                    damage = 5 - target.fighter.defense
                    if damage > 0:
                        self.engine.message_log.add_message(f"{attack_desc} receiving {damage} damage.")
                        target.fighter.hp -= damage
                    else:
                        self.engine.message_log.add_message(f"{attack_desc} but gets no damage.")

        self.entity.despawn()
        return explosion

