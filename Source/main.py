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

        self.speed = speed

        self.c = colours.fullblack

        self.bullet_offset = mv_u.offset_point(self, (0, self.r * -1))

        # Defaults for player
        self.defaults = self.player_defaults(self)

        square_shape = mv_u.polygon.anchor(
                        [(0, 0), (self.side, 0), (self.side, self.side), (self.side//2, self.side), (0, self.side)],
                        (self.side//2, self.side//2))

        hit_r = self.r * 1.25
        hitbox_shape = mv_u.polygon.anchor(
                        [(hit_r, 0), (hit_r, 0), (hit_r * 2, hit_r), (hit_r, hit_r * 2), (0, hit_r)],
                        (hit_r, hit_r))

        shooting_shape = mv_u.polygon.anchor(
                        [(self.side//2, 0), (self.side//2, 0), (self.side, self.side - self.r), (self.side//2, self.side), (0, self.side - self.r)],
                        (self.side//2, self.side//2))

        hitbox_shoot = mv_u.polygon.anchor(
                        [(hit_r, 0), (hit_r, 0), (hit_r * 2, hit_r * 1.75), (hit_r, hit_r * 2), (0, hit_r * 1.75)],
                        (hit_r, hit_r))

        self.polygons = [square_shape, hitbox_shape, shooting_shape, hitbox_shoot]
        self.morph = mv_u.offset_morphpolygon(
                                *self.polygons,
                                offset=(0, 0),
                                parent=self)

    def update_move(self, game):

        if game.check_key(pygame.K_LSHIFT, pygame.K_RSHIFT):
            self.focus = True
            self.speed = self.defaults.focus_speed

            if game.check_key(pygame.K_z, pygame.K_x):
                self.morph.init_morph(3, frames=10)

            else:
                self.morph.init_morph(1, frames=10)

        else:
            self.focus = False
            self.speed = self.defaults.speed

            if game.check_key(pygame.K_z, pygame.K_x):
                self.morph.init_morph(2, frames=5)

            else:
                self.morph.init_morph(0, frames=10)

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

        if game.check_key(pygame.K_SPACE, pygame.K_z, timebuffer=7):
            game.add_sprite(bullets.standard(
                                    pos=self.bullet_offset.get_pos(),
                                    radius=self.r * 0.75,
                                    speed=10,
                                    angle=-90,
                                    collider="ENEMY"))

        if game.check_key(pygame.K_x, timebuffer=7):
            t = None
            if game.sprites["ENEMY"]:
                t = game.sprites["ENEMY"][0]
            game.add_sprite(bullets.prox(
                                        pos=self.bullet_offset.get_pos(),
                                        radius=self.r * 0.75,
                                        speed=10,
                                        target=t,
                                        target_prox=100,
                                        collider="ENEMY"))

    def update_draw(self, game):
        pygame.draw.polygon(game.win, self.c, self.morph.get())
        # pygame.draw.circle(game.win, self.c, (self.x, self.y), self.r)


def main_game(game):

    player_origin = game.orientate("Center", "Bottom-Center")
    player = player_class(
                        pos=player_origin,
                        radius=12,
                        speed=7)

    game.add_sprite(player)
    # game.add_sprite(enemies.sprout(game.orientate("Left-Center", "Center"), 15, colours.white))

    while game.run:

        game.update_keys()

        if game.check_mouse(0, timebuffer=1):
            game.add_sprite(enemies.pebble(game.mouse_pos, 15, colours.white))

        game.update_draw()

        game.update_scaled()

        game.update_state()


game = game_info(
                name="BULLETHELL",
                win_w=1920,
                win_h=1080,
                user_w=1920,
                user_h=1080,
                bg=colours.switch(),
                framecap=60,
                show_framerate=True,
                quit_key=pygame.K_ESCAPE)

main_game(game)
