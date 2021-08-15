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
    def __init__(self, pos, radius, speed, colour):

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.c = colour

        self.health = 15

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

        self.polygons = [star, mv_u.polygon.rotate(star, (0, 0), -90)]
        self.morph = mv_u.offset_morphpolygon(*self.polygons, offset=(0, 0), parent=self, shift=3)
        self.iter = False

        self.hitbox = [
            mv_u.offset_circle(self, (self.r//2 * -1, 0), self.r),
            mv_u.offset_circle(self, (self.r//2, 0), self.r)
        ]

        self.destroy_surf = None
        self.destroy_shrink = self.r * 4

    def update_move(self, game):
        if self.health < 1:
            self.destroy_surf = Surface((self.r * 4, self.r * 4))
            self.destroy_surf.fill(colours.colourkey)
            self.destroy_surf.set_colorkey(colours.colourkey)

            freeze_polygon = mv_u.polygon.adjust(self.morph.get(), x=(self.x - self.r*2)*-1, y=(self.y - self.r*2)*-1)

            draw.polygon(self.destroy_surf, self.c, freeze_polygon)
            self.destroying = True

        if game.frames % 55 == 0:
            self.iter = not self.iter
            self.morph.init_morph(int(self.iter), 30)

        for hit in self.hitbox:
            hit.update_pos()

    def update_draw(self, game):
        polygon = self.morph.get()
        draw.polygon(game.win, self.c, polygon)

    def update_destroy(self, game):
        self.destroy_shrink -= 2
        if self.destroy_shrink < 1:
            self.flash(game)
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

    def add_class_attr(self, game):
        self.frametick = mv_u.frametick(self.tick, game)

    def update_move(self, game):

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

        if self.start_move:
            if not self.onscreen(game):
                self.kill()
        else:
            for hit in self.hitbox:
                hit.update_pos()

    def update_draw(self, game):
        polygon = self.morph.get()
        draw.polygon(game.win, self.c, polygon)

    def update_destroy(self, game):
        self.r -= 1
        if self.r < 3:
            self.explode(game)

        draw.circle(game.win, self.c, (self.x, self.y), self.r)


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
