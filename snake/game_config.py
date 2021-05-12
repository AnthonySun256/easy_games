from  dataclasses import dataclass
import curses

D_Left  = 0
D_Right = 1
D_Up    = 2
D_Down  = 3

@dataclass
class Position:
    x: int
    y: int


snake_config = {
    "length": 3,
    "lives": 3,
    "speed": 1,
}


keys = {
    'DOWN': 0x42,
    'LEFT': 0x44,
    'RIGHT': 0x43,
    'UP': 0x41,
    'Q': 0x71,
    'R': 0x72,
    'ENTER': 0x0a,
}

game_sizes = {
    'height': 10,
    'width': 10,
}

game_themes = {
    "colors": {
        "default": (curses.COLOR_WHITE, curses.COLOR_BLACK),
        "snake": (curses.COLOR_GREEN, curses.COLOR_BLACK),
        "food": (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        "lives": (curses.COLOR_RED, curses.COLOR_BLACK),
    },
    "tiles": {
        "snake_body": '@',
        "food": '#',
        "lives": '♥ '
    }

}
