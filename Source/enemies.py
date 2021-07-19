from sprite_class import sprite

import move_utils as mv_u
from move_utils import random, math

import draw_utils as draw_u
from draw_utils import draw

from colour_manager import colours


class enemy(sprite):
    layer = "ENEMY"

    def __init__(self, pos, radius):

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

    def collide(self, collider):
        pass

    def flash(self, game):
        o = (self.x, self.y)
        game.add_sprite(enemy_explosion(pos=o, radius=self.r, speed=2, colour=colours.switch(), game=game))


class angel(enemy):
    def __init__(self, pos, radius, colour):

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.c = colour

        r = self.r * 2
        q = r * 0.3

        star_shape = [
            (r, 0),
            (r + q, r - q),
            (r * 2, r),
            (r + q, r + q),
            (r, r * 2),
            (r - q, r + q),
            (0, r),
            (r - q, r - q)
        ]

        star = mv_u.polygon.anchor(star_shape, (r, r))

        self.polygons = [star, mv_u.polygon.rotate(star, (0, 0), -45)]
        self.morph = mv_u.offset_morphpolygon(*self.polygons, offset=(0, 0), parent=self, shift=3)
        self.iter = 0

    def update_move(self, game):
        if game.frames % 55 == 0:
            self.iter += 1
            if self.iter == len(self.morph):
                self.iter = 0
            self.morph.init_morph(self.iter, 30)

    def update_draw(self, game):
        polygon = self.morph.get()
        draw.polygon(game.win, self.c, polygon)

        draw.circle(game.win, colours.red, (self.x, self.y), self.r)

    def collide(self, collider):
        if mv_u.circle_collide(self, collider):
            return True


class enemy_explosion(sprite):
    def __init__(self, pos, radius, speed, colour, game):
        self.layer = "BACKGROUND"

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.speed = speed
        self.c = colour

        self.target_r = max((abs(0 - self.x), (game.win_w - self.x)))
        self.window_corners = [
            (0, 0),
            (game.win_w, 0),
            (0, game.win_h),
            (game.win_w, game.win_h)
        ]

    def update_move(self, game):
        self.r += self.speed
        self.speed += 0.01

    def update_draw(self, game):
        draw.circle(game.win, self.c, (self.x, self.y), self.r)

        if self.r > self.target_r and game.frames % 20 == 0:

            check = 0
            for pos in self.window_corners:
                if math.dist((self.x, self.y), pos) < self.r:
                    check += 1

            if check == 4:
                game.bg_kill(self)
