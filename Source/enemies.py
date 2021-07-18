from sprite_class import sprite

import move_utils as mv_u
from move_utils import random, math

import draw_utils as draw_u
from draw_utils import draw

from colour_manager import colours


class enemy_class(sprite):
    def __init__(self, pos, radius):
        self.layer = "ENEMY"

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.c = (255, 255, 255)

        self.up = random.choice((True, False))

    def update_move(self, game):

        if self.y < self.r or self.y > 500:
            self.up = not self.up

        if self.up:
            self.y -= 4
        else:
            self.y += 4

    def update_draw(self, game):

        draw.circle(game.win, self.c, (self.x, self.y), self.r)

        self.update_highlight(game)

    def flash(self, game):
        self.colour = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        o = (random.randint(0, game.win_w), random.randint(0, game.win_h))
        # o = (self.x, self.y)
        game.add_sprite(enemy_explosion(pos=o, radius=self.r, speed=4, colour=colours.switch()))


class enemy_explosion(sprite):
    def __init__(self, pos, radius, speed, colour):
        self.layer = "BACKGROUND"

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.speed = speed
        self.c = colour

    def update_move(self, game):
        self.r += self.speed

    def update_draw(self, game):
        draw.circle(game.win, self.c, (self.x, self.y), self.r)

        window_corners = [
            (0, 0),
            (game.win_w, 0),
            (0, game.win_h),
            (game.win_w, game.win_h)
        ]

        check = 0
        for pos in window_corners:
            if math.dist((self.x, self.y), pos) < self.r:
                check += 1

        if check == 4:
            # self.kill()
            # game.bg = self.c

            game.bg_kill(self)
