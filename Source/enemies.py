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
        for hit in self.hitbox:
            if mv_u.circle_collide(hit, collider):
                self.health -= 1
                return True

        return False

    def flash(self, game):
        o = (self.x, self.y)
        game.add_sprite(enemy_explosion_square(pos=o, radius=self.r, speed=2, colour=colours.switch(), game=game))
        self.kill()


class angel(enemy):
    def __init__(self, pos, radius, colour):

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.c = colour

        r = self.r * 2
        q = r * 0.3

        self.health = 100

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

        self.polygons = [star, mv_u.polygon.rotate(star, (0, 0), -90)]
        self.morph = mv_u.offset_morphpolygon(*self.polygons, offset=(0, 0), parent=self, shift=3)
        self.iter = 0

        self.hitbox = [
            mv_u.offset_circle(self, (self.r//2 * -1, 0), self.r),
            mv_u.offset_circle(self, (self.r//2, 0), self.r)
        ]

    def update_move(self, game):
        if self.health < 1:
            self.flash(game)

        if game.frames % 55 == 0:
            self.iter += 1
            if self.iter == len(self.morph):
                self.iter = 0
            self.morph.init_morph(self.iter, 30)

        for hit in self.hitbox:
            hit.update_pos()

    def update_draw(self, game):
        polygon = self.morph.get()
        draw.polygon(game.win, self.c, polygon)

        for hit in self.hitbox:
            draw.circle(game.win, colours.red, (hit.x, hit.y), hit.r)


class pebble(enemy):
    def __init__(self, pos, radius, colour):
        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.c = colour

        self.health = 1

        dm1 = [
            (self.r, self.r*2),
            (0, self.r),
            (self.r, 0),
            (self.r*2, self.r)
        ]
        diamond1 = mv_u.polygon.anchor(dm1, (self.r, self.r))

        dm2 = [
            (self.r, 0),
            (self.r*2, self.r),
            (self.r, self.r*2),
            (0, self.r),
        ]

        diamond2 = mv_u.polygon.anchor(dm2, (self.r, self.r))

        self.morph = mv_u.offset_morphpolygon(diamond1, diamond2, offset=(0, 0), parent=self)
        self.iter = 0

        self.hitbox = [mv_u.offset_circle(self, (0, 0), self.r)]

    def add_class_attr(self, game):
        self.frametick = mv_u.frametick(20, game)

    def update_move(self, game):
        if self.health < 1:
            self.flash(game)

        if self.frametick.get():
            self.iter += 1
            if self.iter == len(self.morph):
                self.iter = 0
            self.morph.init_morph(self.iter, 15)

        for hit in self.hitbox:
            hit.update_pos()

    def update_draw(self, game):
        polygon = self.morph.get()
        draw.polygon(game.win, self.c, polygon)

        # for hit in self.hitbox:
        #     draw.circle(game.win, colours.red, (hit.x, hit.y), hit.r)


class enemy_explosion_circle(sprite):
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


class enemy_explosion_square(sprite):
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
        draw.rect(game.win, self.c, (self.x - self.r, self.y - self.r, self.r*2, self.r*2))

        if game.frames % 20 == 0:
            if self.x - self.r < 0 and self.x + self.r > game.win_w:
                game.bg_kill(self)
