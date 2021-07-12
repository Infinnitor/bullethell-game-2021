from gameinfo import game_info, pygame, time, math, random
import move_utils as u
from sprite_class import sprite


# Player class
class player_class(sprite):
    def __init__(self, pos, radius, speed, sprites):
        self.name = "PLAYER"

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.speed = speed
        self.default_speed = speed
        self.focus_speed = self.default_speed // 2

        self.bullet_offset = u.offset_point(self, (0, self.r * -1))

        self.sprites = sprites

    def update_move(self, game):

        if game.check_key(pygame.K_LSHIFT, pygame.K_RSHIFT):
            if self.speed > self.focus_speed:
                self.speed -= 0.1
            else:
                self.speed = self.focus_speed
        else:
            if self.speed < self.default_speed:
                self.speed += 0.1
            else:
                self.speed = self.default_speed

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

        if game.check_key(pygame.K_q, buffer=True):
            print(random.choice(game.sprites))

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
                                    sprites=None))

    def update_draw(self, game):
        a_dest = self.center_image_pos(self.sprites, (self.x, self.y))

        game.win.blit(self.sprites, a_dest)

        if self.moving:
            game.init_particles(number=1,
                                origin=(self.x, self.y),
                                radius=15,
                                angle="RAND",
                                speed=0.5,
                                randspeed=True,
                                lifetime=10,
                                colour=game.colours.fullcyan,
                                layer="LOW")

        self.update_highlight(game)


class standard_bullet(sprite):
    def __init__(self, pos, radius, speed, angle, sprites, target=None):
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

        if self.target is not None:
            a = math.atan2(self.target.x - self.x, self.target.y - self.y)
            self.xmove = math.cos(a)
            self.ymove = math.sin(a)

            if u.circle_collide(self, self.target):
                self.destroy = True

    def update_draw(self, game):
        pygame.draw.circle(game.win, game.colours.red, (self.x, self.y), self.r)
        self.update_highlight(game)

    def draw_highlight(self, game):
        pygame.draw.circle(game.win, game.colours.green, (self.x, self.y), self.r)


class tracking_bullet(sprite):
    def __init__(self, pos, radius, speed, sprites, target=None, target_delay=0):
        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.speed = speed

        a = math.radians(self.angle)
        self.xmove = math.cos(a)
        self.ymove = math.sin(a)

        self.target = target
        self.target_delay = target_delay

        self.sprites = sprites

    def update_move(self, game):
        if self.onscreen(game):
            self.x += self.xmove * self.speed
            self.y += self.ymove * self.speed
        else:
            self.destroy = True

        a = -90
        if game.frames & self.target_delay == 0:
            if self.target is not None:
                a = math.atan2(self.target.x - self.x, self.target.y - self.y)

        self.xmove = math.cos(a)
        self.ymove = math.sin(a)

        if u.circle_collide(self, self.target):
            self.destroy = True

    def update_draw(self, game):
        pygame.draw.circle(game.win, game.colours.blue, (self.x, self.y), self.r)
        self.update_highlight(game)

    def draw_highlight(self, game):
        pygame.draw.circle(game.win, game.colours.green, (self.x, self.y), self.r)


def main_game(game):

    player_origin = game.orientate("Center", "Bottom-Center")
    player = player_class(
                        pos=player_origin,
                        radius=15,
                        speed=4,
                        sprites=pygame.image.load('data/sprites/player/PlayerSmall.png'))

    game.add_sprite(player)

    while game.run:

        game.update_keys()

        game.update_draw()

        game.update_scaled()

        game.update_state()


game = game_info(
                name="BULLETHELL",
                win_w=1280,
                win_h=720,
                user_w=1920,
                user_h=1080,
                bg=(0, 0, 0),
                framecap=60,
                show_framerate=True,
                quit_key=pygame.K_ESCAPE)

main_game(game)
