from gameinfo import game_info, pygame, time, math, random
from colour_manager import colours
from sprite_class import sprite

import move_utils as mv_u
import draw_utils as draw_u

import bullets

import levels_manager


# Player class
class player_class(sprite):

    class player_defaults():
        def __init__(p, parent):
            p.parent = parent

            p.speed = p.parent.speed
            p.focus_speed = p.parent.speed / 2

            p.focus_size = p.parent.r * 4
            p.focus_reduce = 4

            p.deflect_frames = 5
            p.deflect_recharge = 30

            p.iframes = 100

            p.health = 6

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

        self.deflect = 0
        self.deflect_recharge = 0

        self.health = self.defaults.health

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
        self.morph = mv_u.offset_morphpolygon(offset=(0, 0), *self.polygons, parent=self)

        self.hitbox = [mv_u.offset_circle(parent=self, offset=(0, 0), radius=self.r)]
        self.collided_frame = False
        self.iframes = 0

    def update_move(self, game):
        self.collided_frame = False
        if self.iframes > 0:
            self.iframes -= 1

        if self.health < 1:
            self.kill()

        if game.check_key(pygame.K_LSHIFT, pygame.K_RSHIFT):
            self.focus = True
            self.speed = self.defaults.focus_speed

            if game.check_key(pygame.K_z, pygame.K_SPACE):
                self.morph.init_morph(3, frames=10)

            else:
                self.morph.init_morph(1, frames=10)

        else:
            self.focus = False
            self.speed = self.defaults.speed

            if game.check_key(pygame.K_z, pygame.K_SPACE):
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
            game.add_sprite(bullets.shard(
                                    pos=self.bullet_offset.get_pos(),
                                    radius=self.r * 0.75,
                                    speed=11,
                                    angle=-90,
                                    colour=self.c,
                                    collider="ENEMY"))

        if game.check_key(pygame.K_x):
            if self.deflect_recharge == 0:
                self.deflect = self.defaults.deflect_frames
                self.deflect_recharge = self.defaults.deflect_recharge

        if self.deflect > 0:
            self.deflect -= 1
        if self.deflect_recharge > 0:
            self.deflect_recharge -= 1

    def update_draw(self, game):
        # if self.collided_frame:
        #     game.init_screenshake(4, 10)

        if self.iframes // 10 % 2 == 1:
            return

        if self.deflect > 0:
            pygame.draw.circle(game.win, colours.purple, (self.x, self.y), self.r*3)
        pygame.draw.polygon(game.win, self.c, self.morph.get())

    def collide(self, collider):
        if self.iframes > 0:
            return False

        for hit in self.hitbox:
            hit.get_pos()
            if mv_u.circle_collide(hit, collider):
                self.health -= 1
                self.collided_frame = True
                self.iframes = self.defaults.iframes
                return True

        return False


def main_game(game):

    player_origin = game.orientate("Center", "Bottom-Center")
    player = player_class(
                        pos=player_origin,
                        radius=12,
                        speed=7)

    game.add_sprite(player)

    while game.run:

        game.update_keys()

        game.add_text(f"Enemies: {len(game.sprites['ENEMY'])}")
        game.update_draw()

        if player.destroy is True:
            return False

        game.update_scaled()

        game.update_state()

    return True


game = game_info(
                name="BULLETHELL",
                win_w=1920,
                win_h=1080,
                user_w=1280,
                user_h=720,
                bg=colours.switch(),
                framecap=60,
                show_framerate=True,
                quit_key=pygame.K_ESCAPE)

while not main_game(game):
    game.purge_sprites()
    game.load_levels()
