from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING
import numpy as np

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item, Effect


class Action:
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


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up the {item.name}!")
                return
        '''
        
        '''
        raise exceptions.Impossible("There is nothing here to pick up.")


class LootAction(Action):
    """Loots an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor, item: item):
        super().__init__(entity)
        self.item=item

    def perform(self) -> None:
        inventory = self.entity.inventory

        if len(inventory.items) >= inventory.capacity:
            raise exceptions.Impossible("Your inventory is full.")
        
        self.item.parent = self.entity.inventory
        inventory.items.append(self.item)

        self.engine.message_log.add_message(f"You picked up the {self.item.name}!")
        return

class ItemAction(Action):
    def __init__(
        self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)


class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)
            
        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)


class WaitAction(Action):
    def __init__(self, entity: Actor, cost: int = 0) -> None:
        super().__init__(entity)
        self.cost: int = entity.speed

    def perform(self) -> None:
        pass


class EnterSystemAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if self.engine.game_map.system_exit_location[self.entity.x, self.entity.y]:

            if self.engine.game_map is self.engine.game_world.main_map:
                game_world = self.engine.game_world

                for system in game_world.stellar_systems:

                    if (self.entity.x-system.x)**2 + (self.entity.y-system.y)**2 < (system.star.r+5)**2:
                        self.engine.game_map = system.game_map

                        self.entity.gamemap.entities.remove(self.entity)
                        self.entity.parent = system.game_map
                        self.entity.gamemap.entities.add(self.entity)

                        self.entity.place(int(self.engine.game_map.width-10), int(self.engine.game_map.height/2), self.engine.game_map)
                        self.engine.message_log.add_message(
                            "You enter the system.", color.descend)
            else:
                self.engine.game_map = self.engine.game_world.main_map

                self.entity.gamemap.entities.remove(self.entity)
                self.entity.parent = self.engine.game_world.main_map
                self.entity.gamemap.entities.add(self.entity)
                
                self.entity.place(self.entity.global_map_x, self.entity.global_map_y, self.engine.game_map)
                #self.entity.place(int(self.engine.game_map.width-10), int(self.engine.game_map.height/2), space)
                self.engine.message_log.add_message(
                    "You exit the system.", color.descend)
        else:
            raise exceptions.Impossible("There is no system transit here.")


class ActionWithDirection(Action):
    def __init__(self, entity: Union[Actor, Effect], dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.mass - target.fighter.mass

        attack_desc = f"{self.entity.name.capitalize()} rams into {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(f"{attack_desc} dealing {damage} damage.")
            target.fighter.hp -= damage
        elif damage < 0:
            self.engine.message_log.add_message(f"{attack_desc} receiving {-damage} damage.")
            self.entity.fighter.hp += damage
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.")


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


class ProjectileFlyAction(ActionWithDirection):
    def __init__(self, entity: Union[Actor, Effect], dx: int, dy: int, cost: int = 20):
        super().__init__(entity, dx, dy)
        self.cost = cost
    
    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""

        #print(self.dx)
        target = self.engine.game_map.get_actor_at_location(self.entity.x + self.dx, self.entity.y + self.dy)
        if target:
            return target

        return 


    def perform(self) -> None:
        target = self.target_actor

        if target:
            damage = self.entity.origin.fighter.power - target.fighter.defense

            attack_desc = f"{self.entity.origin.name.capitalize()} hits {target.name} with laser"
            if damage > 0:
                self.engine.message_log.add_message(f"{attack_desc} dealing {damage} damage.")
                target.fighter.hp -= damage
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage.")
            self.entity.despawn()
        else:
            MovementAction(self.entity, self.dx, self.dy).perform()

