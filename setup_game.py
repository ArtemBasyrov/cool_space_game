"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod

import color
from engine import Engine
import entity_factories
import input_handlers
from game_map import GameWorld

# Load the background image and remove the alpha channel.
background_image = tcod.image.load("menu_background_space.png")[:, :, :3]


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_window_width = 79
    map_window_height = 43


    map_width = 79*3
    map_height = 43*3

    max_monsters = 6
    min_monsters = 3

    max_items = 1

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        map_window_width=map_window_width, 
        map_window_height=map_window_height, 
        map_width=map_width,
        map_height=map_height,
        max_monsters=max_monsters,
        min_monsters=min_monsters,
        max_items = max_items,
        engine=engine,
    )
    
    engine.game_world.generate_galaxy()
    engine.update_fov()

    engine.message_log.add_message(
        "The galaxy is dark and full of danger...", color.welcome_text
    )

    dagger_laser = copy.deepcopy(entity_factories.dagger_laser)
    basic_armor = copy.deepcopy(entity_factories.basic_armor)

    dagger_laser.parent = player.inventory
    basic_armor.parent = player.inventory

    player.inventory.items.append(dagger_laser)
    player.equipment.toggle_equip(dagger_laser, add_message=False)

    player.inventory.items.append(basic_armor)
    player.equipment.toggle_equip(basic_armor, add_message=False)

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "COOL SPACE GAME",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Artem Basyrov",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())

        return None