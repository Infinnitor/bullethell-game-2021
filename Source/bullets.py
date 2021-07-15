from sprite_class import sprite
from pygame import draw

import move_utils as mv_u
import draw_utils as draw_u

import math
from colour_manager import colours


class bullet(sprite):
    def update_move(self, game):
        self.update_bullet(game)
        self.update_tracking(game)

    def update_bullet(self, game):
        pass

    def update_tracking(self, game):
        pass

class standard(bullet):
    def __init__(self, pos, radius, speed, angle, target=""):
        self.name = "BULLET"

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.speed = speed
        self.angle = angle

        a = math.radians(self.angle)
        self.xmove = math.cos(a)
        self.ymove = math.sin(a)

        self.target = target

        self.c = colours.fullblack

    def update_bullet(self, game):
        if self.onscreen(game):
            self.x += self.xmove * self.speed
            self.y += self.ymove * self.speed
        else:
            self.destroy = True

        if self.target != "":

            for t in game.sprites[self.target]:

                if mv_u.circle_collide(self, t):
                    t.flash()
                    self.kill()

    def update_draw(self, game):
        # pygame.draw.circle(game.win, self.c, (self.x, self.y), self.r)

        triangle = (
            (self.x, self.y - self.r*2),
            (self.x - self.r, self.y),
            (self.x, self.y + self.r*2),
            (self.x + self.r, self.y),
        )

        draw.polygon(game.win, self.c, triangle)
        self.update_highlight(game)


class prox(bullet):
    def __init__(self, pos, radius, speed, target=None, target_prox=1):
        self.name = "BULLET"

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

    def update_bullet(self, game):

        if mv_u.circle_collide(self, self.target):
            self.target.flash()
            self.kill()

        if self.onscreen(game):
            self.x += self.xmove * self.speed
            self.y += self.ymove * self.speed
        else:
            self.destroy = True

    def update_tracking(self, game):
        if mv_u.circle_collide(self, self.target, add=[self.target_prox]):
            self.target_update = False

        if self.target_update:
            a = -90
            if self.target is not None:
                a = math.atan2(self.target.y - self.y, self.target.x - self.x)

            self.xmove = math.cos(a)
            self.ymove = math.sin(a)


    def update_draw(self, game):
        draw.circle(game.win, self.c, (self.x, self.y), self.r)
        self.update_highlight(game)


# Work in progress
class homing(bullet):
    def __init__(self, pos, radius, speed, angle, target=None, target_prox=1, homing=1):
        self.name = "BULLET"

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

    def update_bullet(self, game):

        if mv_u.circle_collide(self, self.target):
            self.target.flash()
            self.kill()

        if self.onscreen(game):
            self.x += self.xmove * self.speed
            self.y += self.ymove * self.speed
        else:
            self.destroy = True

    def update_tracking(self, game):
        if mv_u.circle_collide(self, self.target, add=[self.target_prox]):
            self.target_update = False

        if self.target_update:
            target_a = self.angle
            if self.target is not None:
                target_a = math.atan2(self.target.y - self.y, self.target.x - self.x)

            if self.angle > math.degrees(target_a):
                self.c = colours.fullcyan
                self.angle -= self.homing
            elif self.angle < math.degrees(target_a):
                self.c = colours.fullgreen
                self.angle += self.homing

            self.xmove = math.cos(math.radians(self.angle))
            self.ymove = math.sin(math.radians(self.angle))


    def update_draw(self, game):
        draw.circle(game.win, self.c, (self.x, self.y), self.r)
        self.update_highlight(game)
