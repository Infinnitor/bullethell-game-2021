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

        if game.check_key(pygame.K_LEFT, pygame.K_a):
            self.x -= self.speed
        if game.check_key(pygame.K_RIGHT, pygame.K_d):
            self.x += self.speed
        if game.check_key(pygame.K_UP, pygame.K_w):
            self.y -= self.speed
        if game.check_key(pygame.K_DOWN, pygame.K_s):
            self.y += self.speed

        if game.check_key(pygame.K_q, buffer=True):
            print(random.choice(game.sprites))

        onscreen_status = self.onscreen_info(game)
        if onscreen_status == "X":
            self.x = oldx
        elif onscreen_status == "Y":
            self.y = oldy

        if game.check_key(pygame.K_SPACE, timebuffer=7):
            game.add_sprite(bullet(
                                    pos=self.bullet_offset.get_pos(),
                                    radius=self.r//2,
                                    speed=10,
                                    angle=-90,
                                    sprites=None))

    def update_draw(self, game):
        pygame.draw.circle(game.win, game.colours.red, (self.x, self.y), self.r)
        self.update_highlight(game)

    def draw_highlight(self, game):
        pygame.draw.circle(game.win, game.colours.green, (self.x, self.y), self.r)

class bullet(sprite):
    def __init__(self, pos, radius, speed, angle, sprites, target=None):
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
        pygame.draw.circle(game.win, game.colours.blue, (self.x, self.y), self.r)
        self.update_highlight(game)

    def draw_highlight(self, game):
        pygame.draw.circle(game.win, game.colours.green, (self.x, self.y), self.r)

def main_game(game):

    player_origin = game.orientate("Center", "Bottom-Center")
    player = player_class(pos=player_origin, radius=15, speed=4, sprites=None)
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
                user_w=1280,
                user_h=720,
                bg=(0, 0, 0),
                framecap=60,
                show_framerate=False,
                quit_key=pygame.K_ESCAPE)

main_game(game)
