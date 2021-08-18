from sprite_class import sprite

import move_utils as mv_u
from move_utils import random, math

import bullets

import draw_utils as draw_u
from pygame import draw, transform, Surface

from colour_manager import colours


class enemy(sprite):
    layer = "ENEMY"

    def collide(self, collider):
        for hit in self.hitbox:
            if mv_u.circle_collide(hit, collider):
                self.health -= 1
                return True

        return False

    def explode(self, game):
        o = (self.x, self.y)
        game.add_sprite(enemy_explosion_circle(pos=o, radius=self.r, speed=2, colour=colours.switch(), game=game))
        self.kill()


class angel(enemy):
    def __init__(self, pos, radius, speed, colour, jump_pos):

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.c = colour

        self.health = 50

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
            (r, 0),
            (r, 0),
            (0, self.r),
            (0, self.r),
            (r * -1, 0),
            (r * -1, 0)
        ]

        self.polygons = [star, mv_u.polygon.rotate(star, (0, 0), -90), jump_dm]
        self.morph = mv_u.offset_morphpolygon(*self.polygons, offset=(0, 0), parent=self, shift=3)
        self.morph_iter = False

        self.hitbox = [
            mv_u.offset_circle(self, (self.r//2 * -1, 0), self.r),
            mv_u.offset_circle(self, (self.r//2, 0), self.r)
        ]

        self.destroy_surf = None
        self.destroy_shrink = self.r * 4

    def find_slope(self):
        self.a = math.atan2(self.targetY - self.y, self.targetX - self.x)

        hyp = math.dist((self.x, self.y), (self.targetX, self.targetY))
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
            r = range(0, 360, 11)

        if t == "BLARGH2":
            r = range(11, 371, 23)

        if t in use_range:
            for angle in list(r):
                game.add_sprite(bullets.diamond((self.x, self.y), 8, speed, angle, colour=self.c, collider="PLAYER"))

        if t == "CUSTOM":
            for angle in a_list:
                game.add_sprite(bullets.diamond((self.x, self.y), 8, speed, angle, colour=self.c, collider="PLAYER"))

    def update_move(self, game):
        if self.health < 1:
            self.destroy_surf = Surface((self.r * 4, self.r * 4))
            self.destroy_surf.fill(colours.colourkey)
            self.destroy_surf.set_colorkey(colours.colourkey)

            freeze_polygon = mv_u.polygon.adjust(self.morph.get(), x=(self.x - self.r*2)*-1, y=(self.y - self.r*2)*-1)

            draw.polygon(self.destroy_surf, self.c, freeze_polygon)
            self.destroying = True

        if math.dist((self.x, self.y), (self.targetX, self.targetY)) < self.speed / 2:

            if self.shoot_tick is None:
                self.shoot_tick = mv_u.frametick(5, game)
                self.shoot_iter = 0

            elif self.shoot_tick.get():
                # game.add_sprite(bullets.diamond((self.x, self.y), 8, 5, 90, colour=self.c, collider="PLAYER"))
                if self.shoot_iter % 2 == 0:
                    self.pattern("BLARGH", game, speed=7)
                else:
                    self.pattern("BLARGH2", game, speed=7)

                if self.shoot_iter % 10 == 0:
                    p = game.sprites["PLAYER"][0]
                    game.add_sprite(bullets.prox_diamond((self.x, self.y), 15, 5, self.c, target=p, target_prox=300, collider="PLAYER"))

                # else:
                #     self.pattern("CUSTOM", game, a_list=range(17, 377, 23), speed=10)

                # self.pattern("BLARGH", game, speed=7)

                self.shoot_iter += 1
                if self.shoot_iter > 50:
                    self.shoot_tick = None
                    self.shoot_iter = 0

                self.morph_iter = not self.morph_iter
                self.morph.init_morph(int(self.morph_iter), 10)

            if self.shoot_tick is None:
                self.jump_iter += 1
                if self.jump_iter == len(self.jump_pos):
                    self.jump_iter = 0

                self.targetX = self.jump_pos[self.jump_iter][0]
                self.targetY = self.jump_pos[self.jump_iter][1]

                self.find_slope()

        if self.shoot_tick is None:
            self.x += self.xmove
            self.y += self.ymove

        for hit in self.hitbox:
            hit.update_pos()

    def update_draw(self, game):
        polygon = self.morph.get()
        draw.polygon(game.win, self.c, polygon)
        # draw.circle(game.win, self.c, (self.targetX, self.targetY), self.r)

    def update_destroy(self, game):
        self.destroy_shrink -= 2
        if self.destroy_shrink < 1:
            self.explode(game)
            self.kill()
            return

        shrunk = transform.scale(self.destroy_surf, (self.destroy_shrink, self.destroy_shrink))
        game.win.blit(shrunk, self.center_image_pos(shrunk))


class pebble(enemy):
    def __init__(self, pos, radius, speed, colour):
        self.x = pos[0]
        self.y = pos[1]
        self.start_y = pos[1]
        self.r = radius

        self.speed = speed

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
            self.frametick = mv_u.frametick(self.tick, game)

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
