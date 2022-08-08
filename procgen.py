from __future__ import annotations

from typing import Tuple
import numpy as np
import copy

import entity_factories
from game_map import GameMap
import tile_types
from components.stellar_system import Star, StellarSystem, Planet

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)






def place_entities(
    stars: Star, 
    space: GameMap, 
    player,
    maximum_monsters: int,
    minimum_monsters: int,
    maximum_items: int
) -> None:
    number_of_monsters = np.random.randint(minimum_monsters, maximum_monsters)
    number_of_items = np.random.randint(0, maximum_items)

    for i in range(number_of_monsters):
        x = np.random.randint(0, space.width)
        y = np.random.randint(0, space.height)


        if not any(entity.x == x and entity.y == y for entity in space.entities) \
           and not any(s.inner(space.width, space.height)[x,y] for s in stars):
            if np.random.random() < 0.8:
                entity_factories.skirmisher.spawn(space, x, y)
            else:
                entity_factories.fighter.spawn(space, x, y)

    for i in range(number_of_items):
        x = np.random.randint(0, space.width)
        y = np.random.randint(0, space.height)

        if not any(entity.x == x and entity.y == y for entity in space.entities) \
           and not any(s.inner(space.width, space.height)[x,y] for s in stars):
            item_chance = np.random.random()

            if item_chance < 0.7:
                entity_factories.repair_kit.spawn(space, x, y)
            elif item_chance < 0.8:
                entity_factories.missile.spawn(space, x, y)
            elif item_chance < 0.9:
                entity_factories.targeted_EMP.spawn(space, x, y)
            else:
                entity_factories.lightning_scroll.spawn(space, x, y)

    for entity in set(space.actors)-{player}:
        entity.inventory.add(entity_factories.repair_kit)

    
def generate_space(map_width: int, 
                   map_height: int, 
                   engine: Engine,
                   max_monsters: int,
                   min_monsters: int,
                   max_items: int,
                   map_window_width: int, 
                   map_window_height: int,
                   ):

    player = engine.player

    space = GameMap(
        engine=engine, 
        width=map_width, 
        height=map_height, 
        entities=[player],
        window_width=map_window_width,
        window_height=map_window_height,
    )

    player.place(int(map_width/2), int(map_height/2), space)


    stars = []
    stellar_sys = []
    while len(stars) != 20:
        rand_x = np.random.randint(0,map_width)
        rand_y = np.random.randint(0,map_height)
        rand_r = np.random.randint(4,12)

        if (rand_x-player.x)**2 + (rand_y-player.y)**2 < rand_r**2:
            continue

        new_star = Star(x=rand_x,y=rand_y,r=rand_r)
        if len(stars) == 0:
            stars += [new_star]
            continue

        prox_check = []
        for s in stars:
            prox_check += [s.check_proximity(new_star)]


        if all(prox_check):
            new_StellarSystem = StellarSystem(
                x=new_star.x, 
                y=new_star.y,
                star=copy.deepcopy(new_star),
            )

            
            new_StellarSystem.generate_planets(
                width=map_window_width*4,
                height=map_window_height*2
            )            
            
            
            system_map = generate_star_system(
                engine=engine, 
                map_width=map_window_width*4, 
                map_height=map_window_height*2, 
                window_width=map_window_width,
                window_height=map_window_height,
                stellar_system=new_StellarSystem,
            )
            
            new_StellarSystem.game_map = system_map

            stellar_sys += [new_StellarSystem]
            stars += [new_star]
            space.tiles[stars[-1].inner(map_width, map_height)] = stars[-1].tile
            space.system_exit_location[stars[-1].outter(map_width, map_height)] = \
            ~ space.system_exit_location[stars[-1].outter(map_width, map_height)]

    #place_entities(stars, space, player, max_monsters, min_monsters, max_items)

    return space, set(stellar_sys)


def generate_star_system(
        engine: Engine, 
        map_width: int, 
        map_height: int, 
        window_width: int,
        window_height: int,
        stellar_system: StellarSystem,
    ):

    space = GameMap(
        engine=engine, 
        width=map_width, 
        height=map_height,
        window_width=window_width,
        window_height=window_height,
    )

    stellar_system.star.x = 0
    stellar_system.star.y = int(map_height/2)
    stellar_system.star.r *= 5

    space.tiles[stellar_system.star.inner(map_width, map_height)] = stellar_system.star.tile
    space.system_exit_location[int(map_width-10):int(map_width),0:int(map_height)] = \
        ~space.system_exit_location[int(map_width-10):int(map_width),0:int(map_height)]


    if len(stellar_system.planets) != 0:
        for planet in stellar_system.planets:
            space.tiles[planet.inner(map_width, map_height)] = planet.tile_dark
            space.tiles[planet.facing_star(map_width, map_height)] = planet.tile_light
    

    return space

