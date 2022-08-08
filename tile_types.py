from typing import Tuple

import numpy as np 

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (255, 255, 255)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (0, 0, 0), (30, 30, 30)),
    light=(ord(" "), (0, 0, 0), (0, 0, 0)),
)

floor_star = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("."), (180, 180, 180), (30, 30, 30)),
    light=(ord("."), (200, 200, 200), (0, 0, 0)),
)

system_exit = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (0, 0, 0), (100, 100, 0)),
    light=(ord(" "), (0, 0, 0), (200, 200, 0)),
)

M_type_star = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (180, 40, 0)),
    light=(ord(" "), (255, 255, 255), (180, 40, 0)),
)

K_type_star = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (255, 150, 0)),
    light=(ord(" "), (255, 255, 255), (255, 150, 0)),
)

G_type_star = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (255, 255, 0)),
    light=(ord(" "), (255, 255, 255), (255, 255, 0)),
)

F_type_star = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (255, 255, 255)),
    light=(ord(" "), (255, 255, 255), (255, 255, 255)),
)

A_type_star = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (176,224,230)),
    light=(ord(" "), (255, 255, 255), (176,224,230)),
)

B_type_star = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (135,206,250)),
    light=(ord(" "), (255, 255, 255), (135,206,250)),
)

O_type_star = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0,191,255)),
    light=(ord(" "), (255, 255, 255), (0,191,255)),
)

base_planet_dark = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (34,139,34)),
    light=(ord(" "), (255, 255, 255), (34,139,34)),
)

base_planet_light = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (154,205,50)),
    light=(ord(" "), (255, 255, 255), (154,205,50)),
)

gas_giant_planet_dark = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (46,139,87)),
    light=(ord(" "), (255, 255, 255), (46,139,87)),
)

gas_giant_planet_light = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (60,179,113)),
    light=(ord(" "), (255, 255, 255), (60,179,113)),
)

super_earth_planet_dark = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (70,130,180)),
    light=(ord(" "), (255, 255, 255), (70,130,180)),
)

super_earth_planet_light = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (100,149,237)),
    light=(ord(" "), (255, 255, 255), (100,149,237)),
)

molten_planet_dark = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (128,0,0)),
    light=(ord(" "), (255, 255, 255), (128,0,0)),
)

molten_planet_light = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (205,92,92)),
    light=(ord(" "), (255, 255, 255), (205,92,92)),
)

frozen_planet_dark = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (25,25,112)),
    light=(ord(" "), (255, 255, 255), (25,25,112)),
)

frozen_planet_light = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (0,0,205)),
    light=(ord(" "), (255, 255, 255), (0,0,205)),
)

