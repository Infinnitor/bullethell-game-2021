from sprite_class import sprite
from pygame import draw, transform, Surface

import move_utils as mv_u
import math

import bullets

from colour_manager import colours


def float_range(start, end, step):
    i = start
    items = []
    while i < end:
        items.append(i)
        i += step

    return items


class enemy(sprite):
    layer = "ENEMY"

    def collide(self, collider):
        for hit in self.hitbox:
            if mv_u.circle_collide(hit, collider):
                self.health -= 1
                return True

        return False

    def explode(self, game):
        game.add_sprite(enemy_explosion_circle(pos=(self.x, self.y), radius=self.r, speed=2, colour=colours.switch(), game=game))
        self.kill()


class angel(enemy):
    def __init__(self, pos, radius, speed, colour, jump_pos):

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.c = colour

        self.health = 25

        self.speed = speed

        self.jump_pos = jump_pos
        self.jump_iter = 0

        self.targetX = self.jump_pos[0][0]
        self.targetY = self.jump_pos[0][1]
        self.find_slope()

        self.shoot_iter = 0
        self.shoot_tick = None

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

        jump_dm = [
            (0, self.r * -1),
            (0, self.r * -1),
            (self.r, 0),
            (self.r, 0),
            (0, self.r),
            (0, self.r),
            (self.r * -1, 0),
            (self.r * -1, 0)
        ]

        death_dm = [
            (0, -2),
            (0, -2),
            (2, 0),
            (2, 0),
            (0, 2),
            (0, 2),
            (-2, 0),
            (-2, 0),
        ]

        # jump = mv_u.polygon.anchor(jump_dm, (0, 0))

        self.polygons = [star, mv_u.polygon.rotate(star, (0, 0), -90), jump_dm, death_dm]
        self.morph = mv_u.offset_morphpolygon(*self.polygons, offset=(0, 0), parent=self, shift=3)
        self.morph_iter = False

        self.moving = False

        self.hitbox = [
            mv_u.offset_circle(self, (self.r//2 * -1, 0), self.r),
            mv_u.offset_circle(self, (self.r//2, 0), self.r)
        ]

        self.destroy_surf = None
        self.destroy_shrink = self.r * 4

    def find_slope(self):
        self.a = math.atan2(self.targetY - self.y, self.targetX - self.x)

        self.xmove = math.cos(self.a) * self.speed
        self.ymove = math.sin(self.a) * self.speed

    def pattern(self, t, game, radius=8, speed=5, a_list=[]):
        use_range = ("4DIAGONAL", "4DIR", "BLARGH", "BLARGH2")
        r = None

        if t == "4DIAGONAL":
            r = range(-45, 315, 90)

        if t == "4DIR":
            r = range(0, 360, 90)

        if t == "BLARGH":
            r = range(0, 360, 15)

        if t == "BLARGH2":
            # r = range(11, 371, 23)
            r = float_range(7.5, 367.5, 15)

        if t in use_range:
            for angle in r:
                game.add_sprite(bullets.rotate_shard((self.x, self.y), 8, speed, angle, self.c, shard_mod=1.5, collider="PLAYER"))

        if t == "CUSTOM":
            for angle in a_list:
                game.add_sprite(bullets.rotate_shard((self.x, self.y), 8, speed, angle, self.c, shard_mod=1.5, collider="PLAYER"))

    def update_move(self, game):
        if self.health < 1:
            self.destroying = True

        if math.dist((self.x, self.y), (self.targetX, self.targetY)) < self.speed:
            self.moving = False
            self.x = self.targetX
            self.y = self.targetY
        else:
            self.moving = True

        if self.moving is False:

            if self.shoot_tick is None:
                self.shoot_tick = game.frametick(10)
                self.shoot_iter = 0
                self.morph.init_morph(0, 10)

            elif self.shoot_tick.get():
                if self.shoot_iter % 3 == 0:
                    p = game.sprites["PLAYER"][0]
                    game.add_sprite(bullets.init_diamond((self.x, self.y), 10, 5, self.c, target=p, target_prox=300, collider="PLAYER"))

                self.pattern("CUSTOM", game, a_list=range(-45, 315, 60), speed=7)

                self.shoot_iter += 1
                if self.shoot_iter > 9:
                    self.shoot_iter = 0
                    self.moving = True

                    # Find new target
                    self.jump_iter += 1
                    self.shoot_tick = None
                    if self.jump_iter == len(self.jump_pos):
                        self.jump_iter = 0

                    self.targetX = self.jump_pos[self.jump_iter][0]
                    self.targetY = self.jump_pos[self.jump_iter][1]
                    self.find_slope()

                self.morph_iter = not self.morph_iter
                self.morph.init_morph(int(self.morph_iter), 10)

        else:
            self.x += self.xmove
            self.y += self.ymove
            self.morph.init_morph(2, 15)

        for hit in self.hitbox:
            hit.update_pos()

    def update_draw(self, game):
        if self.moving is True:
            polygon = self.morph.get()
            draw.polygon(game.win, self.c, polygon)

        else:
            polygon = self.morph.get()
            draw.polygon(game.win, self.c, polygon)
            # draw.circle(game.win, self.c, (self.targetX, self.targetY), self.r)

    def update_destroy(self, game):
        self.morph.init_morph(3, 45)

        polygon = self.morph.get()
        if self.morph.morphing is False:
            self.explode(game)
            self.kill()

        draw.polygon(game.win, self.c, polygon)


class pebble(enemy):
    def __init__(self, pos, radius, speed, colour, ov_speed=None):
        self.x = pos[0]
        self.y = pos[1]
        self.start_y = pos[1]
        self.r = radius

        self.speed = speed
        if ov_speed is not None:
            self.speed = ov_speed

        self.c = colour

        self.health = 1

        dm1 = mv_u.polygon.anchor([(self.r, self.r*2), (0, self.r), (self.r, 0), (self.r*2, self.r)], (self.r, self.r))
        dm2 = mv_u.polygon.anchor([(self.r, 0), (self.r*2, self.r), (self.r, self.r*2), (0, self.r)], (self.r, self.r))
        self.morph = mv_u.offset_morphpolygon(dm1, dm2, offset=(0, 0), parent=self)

        self.wave = mv_u.sine_bob(wavelength=20, period=4)
        self.iter = 0

        self.hitbox = [mv_u.offset_circle(self, (0, 0), self.r)]
        self.start_move = False

        self.tick = 20
        self.frametick = None

    def update_move(self, game):
        if self.frametick is None:
            self.frametick = game.frametick(self.tick)

        if self.health < 1:
            self.destroying = True

        self.x += self.speed
        self.y = self.start_y + self.wave.get_pos()

        if self.frametick.get():
            self.iter += 1
            if self.iter == len(self.morph):
                self.iter = 0
            self.morph.init_morph(self.iter, 15)
            game.add_sprite(bullets.diamond((self.x, self.y), self.r//2, 5, 90, colour=self.c, collider="PLAYER"))

        if not self.start_move:
            self.start_move = True

        else:
            for hit in self.hitbox:
                hit.update_pos()
            if not self.onscreen(game):
                self.kill()

    def update_draw(self, game):
        polygon = self.morph.get()
        draw.polygon(game.win, self.c, polygon)

        self.update_highlight(game)

    def update_destroy(self, game):
        self.r -= 1
        if self.r < 3:
            self.explode(game)

        draw.circle(game.win, self.c, (self.x, self.y), self.r)

    def explode(self, game):
        o = (self.x, self.y)
        game.add_sprite(enemy_explosion_square(pos=o, radius=self.r, speed=2, colour=colours.switch(), game=game))
        self.kill()


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

            if self.x - (self.r * 0.7) < 0 and self.x + (self.r * 0.7) > game.win_w:
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
