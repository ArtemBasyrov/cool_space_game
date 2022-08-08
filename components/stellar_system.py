from __future__ import annotations

from typing import Iterable, Tuple
import numpy as np
from game_map import GameMap
import tile_types


class StellarSystem:
    def __init__(self, x: int, y: int, star: Star, planets: Iterable[Planet] = [], 
        game_map: GameMap = None):
        self.x = x
        self.y = y

        self.star = star
        self.star.parent = self

        self.planets = planets.copy()
        self.habitability_zone()

        self.game_map = game_map
        


    def habitability_zone(self) -> None:
        distance_ZH_star = np.power(self.star.luminosity, 0.5)
        self.hab_zone_min = int((0.95 * distance_ZH_star)*120)+ self.star.r*5
        self.hab_zone_max = int((1.37 * distance_ZH_star)*120)+ self.star.r*5


    def generate_planets(self, width: int =None, height: int =None) -> None:
        if width is None:
            width = self.game_map.width
        if height is None:
            height = self.game_map.height


        star_type = self.star.type

        if star_type == 'M-type':
            N = round(np.random.triangular(0, 3, 8))
            start_x = 10+self.star.r
            if N != 0:
                dx = (width-start_x-10)/N
            for i in range(N):
                x = np.random.randint(int(start_x+i*dx)+10, int(start_x+(i+1)*dx)-10)
                y = np.random.randint(20, height-20)
                r = np.random.randint(5, 9)
                new_planet = Planet(x=x,y=y,r=r)
                new_planet.parent = self

                if x < self.hab_zone_min:
                    new_planet.tile_dark = tile_types.molten_planet_dark
                    new_planet.tile_light = tile_types.molten_planet_light

                elif x > self.hab_zone_max:
                    new_planet.tile_dark = tile_types.frozen_planet_dark
                    new_planet.tile_light = tile_types.frozen_planet_light

                    if np.random.random() < 1/40:
                        new_planet.tile_dark = tile_types.gas_giant_planet_dark
                        new_planet.tile_light = tile_types.gas_giant_planet_light
                        new_planet.r *= 3

                else:
                    new_planet.habitable = True

                    if np.random.random() < 0.4: # super-Earth
                        new_planet.tile_dark_dark = tile_types.super_earth_planet_dark
                        new_planet.tile_dark_light = tile_types.super_earth_planet_light
                        new_planet.r *= 1.6
                
                self.planets += [new_planet]


        if star_type in ['K-type','G-type']:
            N = round(np.random.triangular(0, 4, 8))
            start_x = 10+self.star.r
            if N != 0:
                dx = (width-start_x-10)/N
            for i in range(N):
                x = np.random.randint(int(start_x+i*dx)+10, int(start_x+(i+1)*dx)-10)
                y = np.random.randint(20, height-20)
                r = np.random.randint(5, 9)
                new_planet = Planet(x=x,y=y,r=r)
                new_planet.parent = self

                if x < self.hab_zone_min:
                    new_planet.tile_dark = tile_types.molten_planet_dark
                    new_planet.tile_light = tile_types.molten_planet_light

                elif x > self.hab_zone_max:
                    new_planet.tile_dark = tile_types.frozen_planet_dark
                    new_planet.tile_light = tile_types.frozen_planet_light

                    if np.random.random() < 1/16:
                        new_planet.tile_dark = tile_types.gas_giant_planet_dark
                        new_planet.tile_light = tile_types.gas_giant_planet_light
                        new_planet.r *= 3

                else:
                    new_planet.habitable = True

                    if np.random.random() < 0.4: # super-Earth
                        new_planet.tile_dark_dark = tile_types.super_earth_planet_dark
                        new_planet.tile_dark_light = tile_types.super_earth_planet_light
                        new_planet.r *= 1.6
                
                self.planets += [new_planet]


        if star_type == 'F-type':
            N = round(np.random.triangular(0, 3, 5))
            start_x = 10+self.star.r
            if N != 0:
                dx = (width-start_x-10)/N
            for i in range(N):
                x = np.random.randint(int(start_x+i*dx)+10, int(start_x+(i+1)*dx)-10)
                y = np.random.randint(20, height-20)
                r = np.random.randint(5, 9)
                new_planet = Planet(x=x,y=y,r=r)
                new_planet.parent = self

                if x < self.hab_zone_min:
                    new_planet.tile_dark = tile_types.molten_planet_dark
                    new_planet.tile_light = tile_types.molten_planet_light

                elif x > self.hab_zone_max:
                    new_planet.tile_dark = tile_types.frozen_planet_dark
                    new_planet.tile_light = tile_types.frozen_planet_light

                    if np.random.random() < 1/6:
                        new_planet.tile_dark = tile_types.gas_giant_planet_dark
                        new_planet.tile_light = tile_types.gas_giant_planet_light
                        new_planet.r *= 3

                else:
                    new_planet.habitable = True

                    if np.random.random() < 0.4: # super-Earth
                        new_planet.tile_dark_dark = tile_types.super_earth_planet_dark
                        new_planet.tile_dark_light = tile_types.super_earth_planet_light
                        new_planet.r *= 1.6
                
                self.planets += [new_planet]


        if star_type == 'A-type':
            N = round(np.random.triangular(0, 1, 4))
            start_x = 10+self.star.r
            if N != 0:
                dx = (width-start_x-10)/N
            for i in range(N):
                x = np.random.randint(int(start_x+i*dx)+10, int(start_x+(i+1)*dx)-10)
                y = np.random.randint(20, height-20)
                r = np.random.randint(5, 9)
                new_planet = Planet(x=x,y=y,r=r)
                new_planet.parent = self

                if x < self.hab_zone_min:
                    new_planet.tile_dark = tile_types.molten_planet_dark
                    new_planet.tile_light = tile_types.molten_planet_light

                elif x > self.hab_zone_max:
                    new_planet.tile_dark = tile_types.frozen_planet_dark
                    new_planet.tile_light = tile_types.frozen_planet_light

                    if np.random.random() < 1/6:
                        new_planet.tile_dark = tile_types.gas_giant_planet_dark
                        new_planet.tile_light = tile_types.gas_giant_planet_light
                        new_planet.r *= 3

                else:
                    new_planet.habitable = True

                    if np.random.random() < 0.4: # super-Earth
                        new_planet.tile_dark_dark = tile_types.super_earth_planet_dark
                        new_planet.tile_dark_light = tile_types.super_earth_planet_light
                        new_planet.r *= 1.6
                
                self.planets += [new_planet]


        if star_type == 'B-type':
            N = round(np.random.triangular(0, 0.1, 1))
            start_x = 10+self.star.r
            if N != 0:
                dx = (width-start_x-10)/N
            for i in range(N):
                x = np.random.randint(int(start_x+i*dx)+10, int(start_x+(i+1)*dx)-10)
                y = np.random.randint(20, height-20)
                r = np.random.randint(5, 9)
                new_planet = Planet(x=x,y=y,r=r)
                new_planet.parent = self

                if x < self.hab_zone_min:
                    new_planet.tile_dark = tile_types.molten_planet_dark
                    new_planet.tile_light = tile_types.molten_planet_light

                elif x > self.hab_zone_max:
                    new_planet.tile_dark = tile_types.frozen_planet_dark
                    new_planet.tile_light = tile_types.frozen_planet_light

                    if np.random.random() < 0.9:
                        new_planet.tile_dark = tile_types.gas_giant_planet_dark
                        new_planet.tile_light = tile_types.gas_giant_planet_light
                        new_planet.r *= 3

                else:
                    new_planet.habitable = True

                    if np.random.random() < 0.4: # super-Earth
                        new_planet.tile_dark_dark = tile_types.super_earth_planet_dark
                        new_planet.tile_dark_light = tile_types.super_earth_planet_light
                        new_planet.r *= 1.6
                
                self.planets += [new_planet]





class Planet:
    parent: StellarSystem

    def __init__(self, x: int, y: int, r: int):
        self.x = x
        self.y = y
        self.r = r
        self.tile_dark = tile_types.base_planet_dark
        self.tile_light = tile_types.base_planet_light
        self.habitable = False

    @property
    def center(self) -> Tuple[int, int]:
        return self.x, self.y

    def inner(self, map_width, map_height) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        area = np.full((map_width, map_height), False, order='F')
        x = np.arange(map_width)
        y = np.arange(map_height)

        for i in x:
            for j in y:
                if (i-self.x)**2 + (j-self.y)**2 < self.r**2:
                    area[i,j] = True 
        
        return area


    def facing_star(self, map_width, map_height) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        star = self.parent.star
        dist2 = (star.x - self.x)**2 + (star.y - self.y)**2


        area = np.full((map_width, map_height), False, order='F')
        x = np.arange(map_width)
        y = np.arange(map_height)

        for i in x:
            for j in y:
                if (i-star.x)**2 + (j-star.y)**2 < dist2 \
                   and (i-self.x)**2 + (j-self.y)**2 < self.r**2:
                    area[i,j] = True 
        
        return area



class Star:
    parent: StellarSystem

    def __init__(self, x: int, y: int, r: int):
        self.x = x
        self.y = y
        self.mass = self.sampleFromSalpeter(N=1)[0]
        self.mass_radius()
        self.stellar_type()
        self.mass_luminosity()

    @property
    def center(self) -> Tuple[int, int]:
        return self.x, self.y

    def mass_radius(self) -> None:
        self.r = np.power(self.mass,0.8)

    def mass_luminosity(self) -> None:
        if self.mass < 0.43:
            self.luminosity = 0.23*np.power(self.mass, 2.3)
        elif 0.43 <= self.mass < 2.:
            self.luminosity = 1.0*np.power(self.mass, 4.)
        elif 2. <= self.mass < 55.:
            self.luminosity = 1.4*np.power(self.mass, 3.5)
        elif self.mass >= 55.:
            self.luminosity = 32000.0*self.mass

    def stellar_type(self) -> None:
        if self.mass > 16:
            self.tile = tile_types.O_type_star
            self.type = "O-type"
            self.r = round(self.r*1.5)
        elif 2 <= self.mass <= 16:
            self.tile = tile_types.B_type_star
            self.type = "B-type"
            self.r = round(self.r*3)
        elif 1.4 <= self.mass < 2:
            self.tile = tile_types.A_type_star
            self.type = "A-type"
            self.r = round(self.r*3.8)
        elif 1.0 <= self.mass < 1.4:
            self.tile = tile_types.F_type_star
            self.type = "F-type"
            self.r = round(self.r*4.3)
        elif 0.85 <= self.mass < 1.0:
            self.tile = tile_types.G_type_star
            self.type = "G-type"
            self.r = round(self.r*3.5)
        elif 0.5 <= self.mass < 0.85:
            self.tile = tile_types.K_type_star
            self.type = "K-type"
            self.r = round(self.r*3)
        elif self.mass < 0.5:
            self.tile = tile_types.M_type_star
            self.type = "M-type"
            self.r = 2

    def sampleFromSalpeter(self, N, alpha=2.35, M_min=0.1, M_max=100):
        # Convert limits from M to logM.
        log_M_Min = np.log(M_min)
        log_M_Max = np.log(M_max)
        # Since Salpeter SMF decays, maximum likelihood occurs at M_min
        maxlik = np.power(M_min, 1.0 - alpha)

        # Prepare array for output masses.
        Masses = []
        # Fill in array.
        while (len(Masses) < N):
            # Draw candidate from logM interval.
            logM = np.random.uniform(log_M_Min,log_M_Max)
            M    = np.exp(logM)
            # Compute likelihood of candidate from Salpeter SMF.
            likelihood = np.power(M, 1.0 - alpha)
            # Accept randomly.
            u = np.random.uniform(0.0,maxlik)
            if (u < likelihood):
                Masses.append(M)
        return Masses


    def inner(self, map_width, map_height, rad=None) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        if rad is None: rad = self.r

        area = np.full((map_width, map_height), False, order='F')
        x = np.arange(map_width)
        y = np.arange(map_height)

        for i in x:
            for j in y:
                if (i-self.x)**2 + (j-self.y)**2 < rad**2:
                    area[i,j] = True 
        
        return area


    def outter(self, map_width, map_height, rad=None) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        if rad is None: rad = self.r+2

        area = np.full((map_width, map_height), False, order='F')
        x = np.arange(map_width)
        y = np.arange(map_height)

        for i in x:
            for j in y:
                if (self.r-1)**2 < (i-self.x)**2 + (j-self.y)**2 < rad**2:
                    area[i,j] = True 
        
        return area


    def check_proximity(self, other_star):
        if (self.x - other_star.x)**2 + (self.y - other_star.y)**2 < (self.r + other_star.r+20)**2:
            return False
        else:
            return True