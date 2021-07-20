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
                    # obj.flash(game)
                    self.hit_target()

    def update_destroy(self, game):
        self.r -= 0.7
        if self.r < 3:
            self.kill()

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


class standard(bullet):
    layer = "BULLET"

    def __init__(self, pos, radius, speed, angle, collider=""):

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.speed = speed
        self.angle = angle

        a = math.radians(self.angle)
        self.xmove = math.cos(a)
        self.ymove = math.sin(a)

        self.collider_type = collider

        self.c = colours.fullblack

    def update_bullet(self, game):
        if self.onscreen(game):
            self.x += self.xmove * self.speed
            self.y += self.ymove * self.speed
        else:
            self.destroy = True

    def update_draw(self, game):

        diamond = (
            (self.x, self.y - self.r*2),
            (self.x - self.r, self.y),
            (self.x, self.y + self.r*2),
            (self.x + self.r, self.y),
        )

        draw.polygon(game.win, self.c, diamond)
        # draw.circle(game.win, self.c, (self.x, self.y), self.r)


class prox(tracking_bullet):
    layer = "BULLET"

    def __init__(self, pos, radius, speed, target=None, target_prox=1, collider=""):

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.speed = speed

        self.target = target
        self.target_prox = target_prox
        self.target_update = True

        a = -90
        if self.target is not None:
            a = math.atan2(self.target.y - self.y, self.target.x - self.x)

            self.xmove = math.cos(a)
            self.ymove = math.sin(a)

        self.c = colours.fullblack

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
            if mv_u.circle_collide(self, self.target):
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
        r_polygon = mv_u.polygon.rotate(self.shape, (self.r, self.r), math.degrees(self.a))
        draw.polygon(game.win, self.c, mv_u.polygon.adjust(r_polygon, x=self.x, y=self.y))

        # draw.circle(game.win, self.c, (self.x, self.y), self.r)

# Work in progress
class homing(tracking_bullet):
    layer = "BULLET"

    def __init__(self, pos, radius, speed, angle, target=None, target_prox=1, homing=1, collider=""):

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.speed = speed
        self.angle = angle

        self.target = target
        self.target_prox = target_prox
        self.target_update = True

        self.homing = homing

        a = self.angle
        if self.target is not None:
            a = math.atan2(self.target.y - self.y, self.target.x - self.x)

            self.xmove = math.cos(a)
            self.ymove = math.sin(a)

        self.c = colours.fullblack

        self.collider_type = collider

    def update_bullet(self, game):

        if self.target is not None:
            if mv_u.circle_collide(self, self.target):
                # self.target.flash(game)
                self.kill()

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
            target_a = self.angle
            if self.target is not None:
                target_a = math.atan2(self.target.y - self.y, self.target.x - self.x)

            if self.angle > math.degrees(target_a):
                self.angle -= self.homing
            elif self.angle < math.degrees(target_a):
                self.angle += self.homing

            self.xmove = math.cos(math.radians(self.angle))
            self.ymove = math.sin(math.radians(self.angle))

    def update_draw(self, game):
        draw.circle(game.win, self.c, (self.x, self.y), self.r)
