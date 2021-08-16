import copy
import move_utils as mv_u
import enemies
from colour_manager import colours


def pos_mod(enemy, pos):
    obj = copy.copy(enemy)
    obj.x = pos[0]
    obj.y = pos[1]

    return obj


class level():
    def __init__(self, list):
        self.enemies = list
        self.iter = 0

        self.pause = None

    def get(self, game):
        instruction, action = self.enemies[self.iter]

        if self.pause is not None:
            if self.pause.get() is True:
                self.pause = None
                self.iter += 1
            else:
                return None

        if instruction == "SPAWN":
            self.iter += 1
            return action

        if instruction == "PAUSE":
            if action is None:
                if len(game.sprites["ENEMY"]) == 0:
                    self.iter += 1
                    return None
            else:
                self.pause = mv_u.frametick(action, game)

        if self.iter >= len(self.enemies):
            self.iter = 0

        return None


E_pebble = enemies.pebble((1000, 1000), 15, 4, colours.white)
E_angel = enemies.angel((0, 0), 15, 4, colours.white)

p = pos_mod(E_pebble, (0, 500))
print(f"{p.x} {p.y}")


level1 = (
    ["SPAWN", enemies.pebble((0, 500), 15, 4, colours.white)],
    ["PAUSE", 10],

    ["SPAWN", enemies.pebble((0, 500), 15, 4, colours.white)],
    ["PAUSE", 10],

    ["SPAWN", enemies.pebble((0, 500), 15, 4, colours.white)],
    ["PAUSE", 10],

    ["SPAWN", enemies.pebble((0, 500), 15, 4, colours.white)],
    ["PAUSE", 10],

    ["SPAWN", enemies.pebble((0, 500), 15, 4, colours.white)],
    ["PAUSE", 10],

    ["SPAWN", enemies.pebble((0, 500), 15, 4, colours.white)],
    ["PAUSE", 10],

    ["SPAWN", enemies.pebble((0, 500), 15, 4, colours.white)],
    ["PAUSE", 10],

    ["SPAWN", enemies.pebble((0, 500), 15, 4, colours.white)],
    ["PAUSE", 10],

    ["SPAWN", enemies.pebble((0, 500), 15, 4, colours.white)],
    ["PAUSE", None],

    ["SPAWN", enemies.angel((250, 250), 15, 4, colours.white)],
    ["SPAWN", enemies.angel((500, 500), 15, 4, colours.white)],
    ["PAUSE", None],

    ["SPAWN", pos_mod(E_pebble, (0, 500))],
)

LEVEL_ONE = level(level1)
