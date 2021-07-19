from gameinfo import game_info, pygame, time, math, random
from colour_manager import colours

import draw_utils as draw_u
import move_utils as mv_u

import enemies
import bullets

from sprite_class import sprite


# Player class
class player_class(sprite):

    class player_defaults():
        def __init__(p, parent):
            p.parent = parent

            p.speed = p.parent.speed
            p.focus_speed = p.parent.speed / 2

            p.focus_size = p.parent.r * 4
            p.focus_reduce = 4

    def __init__(self, pos, radius, speed):
        self.layer = "PLAYER"

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius
        self.side = self.r * 4

        self.mysurface = pygame.Surface((self.side, self.side))

        self.speed = speed

        self.c = colours.fullblack

        self.bullet_offset = mv_u.offset_point(self, (0, self.r * -1))

        # Defaults for player
        self.defaults = self.player_defaults(self)

        # self.morph = mv_u.offset_polygon()

    def update_move(self, game):

        self.focus = False

        if game.check_key(pygame.K_LSHIFT, pygame.K_RSHIFT):
            self.focus = True
            self.speed = self.defaults.focus_speed

            if self.side > self.r:
                self.side -= self.defaults.focus_reduce
            else:
                self.side = self.r
        else:
            self.speed = self.defaults.speed

            if self.side < self.defaults.focus_size:
                self.side += self.defaults.focus_reduce
            else:
                self.side = self.r * self.defaults.focus_reduce

        oldx = self.x
        oldy = self.y

        self.moving = False
        if game.check_key(pygame.K_LEFT, pygame.K_a):
            self.x -= self.speed
            self.moving = True
        if game.check_key(pygame.K_RIGHT, pygame.K_d):
            self.x += self.speed
            self.moving = True
        if not self.onscreen(game):
            self.x = oldx

        if game.check_key(pygame.K_UP, pygame.K_w):
            self.y -= self.speed
            self.moving = True
        if game.check_key(pygame.K_DOWN, pygame.K_s):
            self.y += self.speed
            self.moving = True
        if not self.onscreen(game):
            self.y = oldy
        onscreen_status = self.onscreen_info(game)
        if onscreen_status == "X":
            self.x = oldx
        elif onscreen_status == "Y":
            self.y = oldy

        if game.check_key(pygame.K_SPACE, pygame.K_z, buffer=True):
            game.add_sprite(bullets.standard(
                                    pos=self.bullet_offset.get_pos(),
                                    radius=self.r * 0.75,
                                    speed=10,
                                    angle=-90,
                                    collider="ENEMY"))

        if game.check_key(pygame.K_x, timebuffer=7):
            t = game.sprites["ENEMY"][0]
            game.add_sprite(bullets.prox(
                                        pos=self.bullet_offset.get_pos(),
                                        radius=self.r * 0.75,
                                        speed=10,
                                        target=t,
                                        target_prox=100,
                                        collider="ENEMY"))

        if game.check_key(pygame.K_c, timebuffer=7):
            t = game.sprites["ENEMY"][0]
            game.add_sprite(bullets.homing(
                                        pos=self.bullet_offset.get_pos(),
                                        radius=self.r * 0.75,
                                        speed=10,
                                        angle=-90,
                                        target=t,
                                        target_prox=0,
                                        homing=5,
                                        collider="ENEMY"))

    def update_draw(self, game):

        self.mysurface.fill(colours.colourkey)
        self.mysurface.set_colorkey(colours.colourkey)

        surf_rect = (
            self.r*2 - self.side//2,
            self.r*2 - self.side//2,
            self.side,
            self.side)

        if self.side < self.defaults.focus_size:
            if self.focus:
                if self.rounding_r < self.side//self.defaults.focus_reduce:
                    self.rounding_r += 1
            else:
                if self.rounding_r > self.side//self.defaults.focus_reduce:
                    self.rounding_r -= 1

            pygame.draw.rect(self.mysurface, self.c, surf_rect, 0, self.rounding_r)

        else:
            self.rounding_r = 0
            pygame.draw.rect(self.mysurface, self.c, surf_rect)

        game.win.blit(self.mysurface, (self.x - self.r * 2, self.y - self.r * 2))
        pygame.draw.circle(game.win, self.c, (self.x, self.y), self.r)

        self.update_highlight(game)


def main_game(game):

    player_origin = game.orientate("Center", "Bottom-Center")
    player = player_class(
                        pos=player_origin,
                        radius=12,
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
                user_w=1280,
                user_h=720,
                bg=colours.switch(),
                framecap=60,
                show_framerate=False,
                quit_key=pygame.K_ESCAPE)

main_game(game)
