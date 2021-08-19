import copy
import move_utils as mv_u
import enemies
from colour_manager import colours


class enemy_template():
    def __init__(self, *e_args, enemy_type):
        self.args = e_args
        self.type = enemy_type

        # self.enemy = enemy_type(*e_args)

    def copy(self, pos=(0, 0), **kwargs):
        return self.type(pos, *self.args, **kwargs)


class level():
    def __init__(self, list):
        self.enemies = list
        self.iter = 0

        self.pause = None

    def get(self, game):

        if self.iter >= len(self.enemies):
            self.iter = 0

        instruction, action = self.enemies[self.iter]

        if self.pause is not None:
            if self.pause.get() is True:
                self.pause = None
                self.iter += 1
                return None
            else:
                return None

        if instruction == "SPAWN":
            self.iter += 1
            return copy.deepcopy(action)

        if instruction == "PAUSE":
            if action is None:
                if len(game.sprites["ENEMY"]) == 0:
                    self.iter += 1
                    return None
            else:
                self.pause = mv_u.frametick(action, game)

        return None


E_pebble = enemy_template(15, 4, colours.white, enemy_type=enemies.pebble)
E_angel = enemy_template(30, 7, colours.white, enemy_type=enemies.angel)


level1 = (
    # ["SPAWN", E_pebble.copy((0, 500))],
    # ["PAUSE", 10],
    #
    # ["SPAWN", E_pebble.copy((0, 500))],
    # ["PAUSE", 10],
    #
    # ["SPAWN", E_pebble.copy((0, 500))],
    # ["PAUSE", 10],
    #
    # ["SPAWN", E_pebble.copy((0, 500))],
    # ["PAUSE", 10],
    #
    # ["SPAWN", E_pebble.copy((0, 500))],
    # ["PAUSE", 10],
    #
    # ["SPAWN", E_pebble.copy((0, 500))],
    # ["PAUSE", 10],
    #
    # ["SPAWN", E_pebble.copy((0, 500))],
    # ["PAUSE", 10],
    #
    # ["SPAWN", E_pebble.copy((0, 500))],
    # ["PAUSE", 10],
    #
    # ["SPAWN", E_pebble.copy((0, 500))],
    # ["PAUSE", None],
    # ["PAUSE", 100],

    # ["SPAWN", E_angel.copy((970, 0), jump_pos=[(970, 250), (1170, 250), (770, 250)])],
    ["SPAWN", E_angel.copy((970, 0), jump_pos=[(1170, 250), (770, 250), (970, 250)])],
    ["SPAWN", E_angel.copy((970, 0), jump_pos=[(770, 250), (970, 250), (1170, 250)])],
    ["PAUSE", None],
    #
    # ["SPAWN", E_pebble.copy((0, 500))],
    # ["PAUSE", 50]
)

def init():
    global LEVEL_ONE
    LEVEL_ONE = level(level1)
