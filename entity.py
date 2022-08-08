from __future__ import annotations

import copy
import math
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union
from actions import ProjectileFlyAction,WaitAction
import actions

from render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.consumable import Consumable
    from components.equipment import Equipment
    from components.equippable import Equippable
    from components.fighter import Fighter
    from components.inventory import Inventory
    from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity(object):
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory]

    def __init__(
        self,
        parent: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        global_map_x: int = 0,
        global_map_y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.global_map_x = global_map_x
        self.global_map_y = global_map_y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def despawn(self: T) -> None:
        """despawn this instance"""
        self.gamemap.entities.remove(self)

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"):  # Possibly uninitialized.
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        
    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

        engine = self.parent.engine
        if engine.game_map is engine.game_world.main_map:
            self.global_map_x = self.x
            self.global_map_y = self.y


class Effect(Entity):

    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        vx: int = 0,
        vy: int = 0,
        lifetime_in_turns: int = 100,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        origin: Entity = None,
        action_points: int = 0,
        speed: int,
        stored_action: Action = None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.EFFECT,
        )

        self.vx=vx
        self.vy=vy
        self.lifetime_in_turns=lifetime_in_turns+1
        self.origin = origin

        self.speed = speed
        self.action_points = action_points
        self.stored_action = stored_action


    def decide_what_to_do(self) -> None:

        if self.vx != 0 or self.vy != 0:
            self.stored_action = ProjectileFlyAction(self, self.vx[0], self.vy[0])
        else:
            self.stored_action = WaitAction(self)

    def get_action(self):
        action = self.stored_action
        if action is not None:
            if action.cost < self.action_points:
                self.stored_action = None

                self.lifetime_in_turns -= 1

                if self.lifetime_in_turns == 0:
                    self.despawn()
                    return None

                return action



class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        equipment: Equipment,
        fighter: Fighter,
        inventory: Inventory,
        action_points: int = 0,
        speed: int,
        stored_action: Action = None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        if ai_cls:
            self.ai: Optional[BaseAI] = ai_cls(self)
        else:
            self.ai = None

        self.equipment: Equipment = equipment
        self.equipment.parent = self

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

        self.speed = speed
        self.action_points = action_points
        self.stored_action = stored_action

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""

        return bool(self.ai)

    def decide_what_to_do(self) -> None:
        if self.stored_action is None and self.ai:
            self.stored_action = self.ai.choose_next_action()


    def get_action(self) -> Action:
        action = self.stored_action
        if action is not None:
            if action.cost < self.action_points:
                self.stored_action = None
                return action
                



class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        consumable: Optional[Consumable] = None,
        equippable: Optional[Equippable] = None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        self.consumable = consumable
        
        if self.consumable:
            self.consumable.parent = self

        self.equippable = equippable

        if self.equippable:
            self.equippable.parent = self


