from gameinfo import game_info, pygame, time, math, random
from colour_manager import colours

import draw_utils as draw_u
import move_utils as mv_u

import enemies

from sprite_class import sprite


# Player class
class player_class(sprite):
    def __init__(self, pos, radius, speed):
        self.name = "PLAYER"

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius
        self.side = self.r * 2

        self.mysurface = pygame.Surface((self.side, self.side))

        self.speed = speed
        self.default_speed = speed
        self.focus_speed = speed / 2

        self.c = colours.fullblack

        self.bullet_offset = mv_u.offset_point(self, (0, self.r * -1))

    def update_move(self, game):

        if game.check_key(pygame.K_LSHIFT, pygame.K_RSHIFT):
            self.speed = self.focus_speed

            if self.side > self.r * 1.5:
                self.side -= 1
            else:
                self.side = self.r * 1.5
        else:
            self.speed = self.default_speed

            if self.side < self.r * 2:
                self.side += 1
            else:
                self.side = self.r * 2

        oldx = self.x
        oldy = self.y

        self.moving = False
        if game.check_key(pygame.K_LEFT, pygame.K_a):
            self.x -= self.speed
            self.moving = True
        if game.check_key(pygame.K_RIGHT, pygame.K_d):
            self.x += self.speed
            self.moving = True
        if game.check_key(pygame.K_UP, pygame.K_w):
            self.y -= self.speed
            self.moving = True
        if game.check_key(pygame.K_DOWN, pygame.K_s):
            self.y += self.speed
            self.moving = True

        onscreen_status = self.onscreen_info(game)
        if onscreen_status == "X":
            self.x = oldx
        elif onscreen_status == "Y":
            self.y = oldy

        if game.check_key(pygame.K_SPACE, timebuffer=7):
            game.add_sprite(standard_bullet(
                                    pos=self.bullet_offset.get_pos(),
                                    radius=self.r//2,
                                    speed=10,
                                    angle=-90,
                                    sprites=None,
                                    target="ENEMY"))

        if game.check_key(pygame.K_z, timebuffer=7):
            t = game.sprites["ENEMY"][0]
            game.add_sprite(tracking_bullet(
                                            pos=self.bullet_offset.get_pos(),
                                            radius=self.r//2,
                                            speed=10,
                                            sprites=None,
                                            target=t,
                                            target_prox=100))

    def update_draw(self, game):

        self.mysurface.fill((0, 0, 0))

        surf_rect = (
            self.r - self.side//2,
            self.r - self.side//2,
            self.side,
            self.side)

        if self.side < self.r * 2:
            draw_u.rounded_rect(self.mysurface, self.c, surf_rect, self.side//4)
        else:
            pygame.draw.rect(self.mysurface, self.c, surf_rect)

        game.win.blit(self.mysurface, (self.x - self.r, self.y - self.r))
        pygame.draw.circle(game.win, self.c, (self.x, self.y), self.r)

        self.update_highlight(game)


class standard_bullet(sprite):
    def __init__(self, pos, radius, speed, angle, sprites, target=""):
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

        self.sprites = sprites

    def update_move(self, game):
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
        pygame.draw.circle(game.win, colours.red, (self.x, self.y), self.r)
        self.update_highlight(game)


class tracking_bullet(sprite):
    def __init__(self, pos, radius, speed, sprites, target=None, target_prox=1):
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

        self.sprites = sprites

    def update_move(self, game):

        if mv_u.circle_collide(self, self.target, add=[self.target_prox]):
            self.target_update = False

        if self.target_update:
            a = -90
            if self.target is not None:
                a = math.atan2(self.target.y - self.y, self.target.x - self.x)

            self.xmove = math.cos(a)
            self.ymove = math.sin(a)

        if mv_u.circle_collide(self, self.target):
            self.target.flash()
            self.kill()

        if self.onscreen(game):
            self.x += self.xmove * self.speed
            self.y += self.ymove * self.speed
        else:
            self.destroy = True

    def update_draw(self, game):
        pygame.draw.circle(game.win, colours.blue, (self.x, self.y), self.r)
        self.update_highlight(game)


def main_game(game):

    player_origin = game.orientate("Center", "Bottom-Center")
    player = player_class(
                        pos=player_origin,
                        radius=20,
                        speed=7)

    game.add_sprite(player)

    game.add_sprite(enemies.enemy_class(pos=(500, 500), radius=50))

    while game.run:

        game.update_keys()

        game.update_draw()

        game.update_scaled()

        game.update_state()


game = game_info(
                name="BULLETHELL",
                win_w=1920,
                win_h=1080,
                user_w=1920,
                user_h=1080,
                bg=(1, 1, 155),
                framecap=60,
                show_framerate=False,
                quit_key=pygame.K_ESCAPE)

main_game(game)
