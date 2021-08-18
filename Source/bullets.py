from sprite_class import sprite
from pygame import draw

import move_utils as mv_u
import draw_utils as draw_u

import math
from colour_manager import colours


class bullet(sprite):
    def update_move(self, game):
        if self.destroying:
            self.update_destroy(game)
            return

        self.update_bullet(game)
        self.update_collisions(game)

    def update_bullet(self, game):
        pass

    def update_collisions(self, game):
        if self.collider_type != "":
            for obj in game.sprites[self.collider_type]:
                if obj.collide(self):
                    self.hit_target()

    def update_destroy(self, game):
        self.r -= 0.7
        if self.r < 3:
            self.kill()

        self.update_draw(game)

    def hit_target(self):
        self.destroying = True


class tracking_bullet(bullet):
    def update_move(self, game):
        if self.destroying:
            self.update_destroy(game)
            return

        self.update_tracking(game)
        self.update_bullet(game)
        self.update_collisions(game)


class standard_bullet(bullet):
    layer = "BULLET"

    def __init__(self, pos, radius, speed, angle, colour, collider=""):

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.speed = speed
        self.angle = angle

        self.a = math.radians(self.angle)
        self.xmove = math.cos(self.a)
        self.ymove = math.sin(self.a)

        self.collider_type = collider

        self.c = colour

    def update_bullet(self, game):
        if self.onscreen(game):
            self.x += self.xmove * self.speed
            self.y += self.ymove * self.speed
        else:
            self.destroy = True

    def update_draw(self, game):
        draw.circle(game.win, self.c, (self.x, self.y), self.r)


class diamond(standard_bullet):
    def update_draw(self, game):
        diamond = (
            (self.x, self.y - self.r*1.5),
            (self.x - self.r*1.5, self.y),
            (self.x, self.y + self.r*1.5),
            (self.x + self.r*1.5, self.y),
        )

        draw.polygon(game.win, self.c, diamond)


class square(standard_bullet):
    def update_draw(self, game):
        draw.rect(game.win, self.c, (self.x - self.r, self.y - self.r, self.r*2, self.r*2))


class shard(standard_bullet):
    def update_draw(self, game):
        diamond = (
            (self.x, self.y - self.r*1.5),
            (self.x - self.r, self.y),
            (self.x, self.y + self.r*1.5),
            (self.x + self.r, self.y),
        )

        draw.polygon(game.win, self.c, diamond)


class rotate_shard(standard_bullet):
    def __init__(self, pos, radius, speed, angle, colour, shard_mod=2, collider=""):

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.speed = speed
        self.angle = angle

        self.a = math.radians(self.angle)
        self.xmove = math.cos(self.a)
        self.ymove = math.sin(self.a)

        self.shard_mod = shard_mod
        stretch_diamond = (
            (0, self.r * -1),
            (self.r * shard_mod * -1, 0),
            (0, self.r),
            (self.r * shard_mod, 0),
        )
        self.polygon = mv_u.polygon.rotate(stretch_diamond, (0, 0), angle)

        self.collider_type = collider

        self.c = colour

    def update_draw(self, game):
        draw.polygon(game.win, self.c, mv_u.polygon.adjust(self.polygon, x=self.x, y=self.y))

    def update_destroy(self, game):
        self.r -= 0.7
        if self.r < 3:
            self.kill()

        shard_diamond = (
            (0, self.r * -1),
            (self.r * self.shard_mod * -1, 0),
            (0, self.r),
            (self.r * self.shard_mod, 0),
        )
        shard_r = mv_u.polygon.rotate(shard_diamond, (0, 0), self.a)
        draw.polygon(game.win, self.c, mv_u.polygon.adjust(shard_r, x=self.x, y=self.y))


class prox(tracking_bullet):
    layer = "BULLET"

    def __init__(self, pos, radius, speed, colour, target=None, target_prox=1, collider=""):

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.speed = speed

        self.target = target
        self.target_prox = target_prox
        self.target_update = True

        self.a = -90
        if self.target is not None:
            self.a = math.atan2(self.target.y - self.y, self.target.x - self.x)

            self.xmove = math.cos(self.a)
            self.ymove = math.sin(self.a)

        self.c = colour

        h_r = self.r
        side_diamond = [
            (self.r*4, self.r*2),
            (self.r*3, self.r*4 - h_r),
            (0, self.r*2),
            (self.r*3, h_r)
        ]

        self.shape = mv_u.polygon.anchor(side_diamond, (self.r, self.r))

        self.collider_type = collider

    def update_bullet(self, game):

        if self.target is not None:
            if self.target.collide(self):
                # self.target.flash(game)
                self.hit_target()

        if self.onscreen(game):
            self.x += self.xmove * self.speed
            self.y += self.ymove * self.speed
        else:
            self.destroy = True

    def update_tracking(self, game):
        if self.target is not None:
            if mv_u.circle_collide(self, self.target, add=[self.target_prox]):
                self.target_update = False

        if self.target_update:
            self.a = -90
            if self.target is not None:
                self.a = math.atan2(self.target.y - self.y, self.target.x - self.x)

            self.xmove = math.cos(self.a)
            self.ymove = math.sin(self.a)

    def update_draw(self, game):
        draw.circle(game.win, self.c, (self.x, self.y), self.r)

class prox_diamond(prox):
    def update_draw(self, game):
        diamond = (
            (self.x, self.y - self.r*1.5),
            (self.x - self.r*1.5, self.y),
            (self.x, self.y + self.r*1.5),
            (self.x + self.r*1.5, self.y),
        )

        draw.polygon(game.win, self.c, diamond)


class prox_funi(prox):
    def update_draw(self, game):
        r_polygon = mv_u.polygon.rotate(self.shape, (self.r, self.r), math.degrees(self.a))
        draw.polygon(game.win, self.c, mv_u.polygon.adjust(r_polygon, x=self.x, y=self.y))
