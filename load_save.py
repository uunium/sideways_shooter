"""Module for managing save state of the game."""

import json


def save_game(gameinst: "Game") -> None:  # noqa: F821
    """Save game stats for the future.

    Create a dictionary and dump it to save.json file.
    """
    # Save ship stats
    ships_left = gameinst.settings.ships_left
    ship_speed = gameinst.settings.ship_speed
    # Save game stats
    level = gameinst.sb.level
    speedup = gameinst.sb.speedup
    score = gameinst.sb.score
    alien_price = gameinst.sb.alien_price
    # Save alien stats
    alien_hor_speed = gameinst.settings.alien_hor_speed
    alien_ver_speed = gameinst.settings.alien_ver_speed
    # Save bullet stats
    shot_delay = gameinst.settings.shot_delay

    save_dict = {
        "ships_left": ships_left,
        "ship_speed": ship_speed,
        "level": level,
        "speedup": speedup,
        "score": score,
        "alien_price": alien_price,
        "alien_hor_speed": alien_hor_speed,
        "alien_ver_speed": alien_ver_speed,
        "shot_delay": shot_delay,
    }
    _work_with_file("save", save_dict)


def load_game(gameinst: "Game") -> None:  # noqa: F821
    """Load game from save.json file."""
    settings_attributes = [
        "ships_left",
        "ship_speed",
        "alien_hor_speed",
        "alien_ver_speed",
        "shot_delay",
    ]
    scoreboard_attributes = [
        "level",
        "speedup",
        "score",
        "alien_price",
    ]

    save_dict = _work_with_file("load")
    _change_attributes("settings", settings_attributes, save_dict, gameinst)
    _change_attributes("sb", scoreboard_attributes, save_dict, gameinst)


def _change_attributes(
    module: str, attributes: list, save_dict: dict, gameinst: "Game"
) -> None:
    """Change gamestate bu loading saved attributes."""
    target_module = getattr(gameinst, module)
    for attribute in attributes:
        setattr(target_module, attribute, save_dict[attribute])
        if module == "settings":
            gameinst.menu._create_lives()
        elif module == "sb":
            gameinst.menu._create_level()
            gameinst.menu._create_score()


def _work_with_file(state: "str", save_dict: dict | None = None) -> None | dict:
    """Write or read from save.json."""
    if state == "save":
        with open("save.json", "w") as savefile:
            savefile.write(json.dumps(save_dict))
    elif state == "load":
        with open("save.json", "r") as savefile:
            return json.loads(savefile.read())
