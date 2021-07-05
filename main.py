from gameinfo import game_info, pygame, time, math, random


# Sprite skeleton class
class sprite():

    def update_move(self):
        pass

    def update_draw(self):
        pass

    def kill(self):
        self.destroy = True


# Player class
class player_class(sprite):
    def __init__(self, pos, radius, speed, sprite):
        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.default_speed = speed
        self.speed = self.default_speed

        self.sprite = sprite

    def update_move(self, game):

        if game.check_key(pygame.K_LSHIFT, pygame.K_RSHIFT):
            self.speed = self.default_speed // 2
        else:
            self.speed = self.default_speed

        if game.check_key(pygame.K_LEFT, pygame.K_a):
            self.x -= self.speed
        if game.check_key(pygame.K_RIGHT, pygame.K_d):
            self.x += self.speed
        if game.check_key(pygame.K_UP, pygame.K_w):
            self.y -= self.speed
        if game.check_key(pygame.K_DOWN, pygame.K_s):
            self.y += self.speed

    def update_draw(self, game):
        pygame.draw.circle(game.win, game.colours.red, (self.x, self.y), self.r)


def main_game(game):

    player_origin = game.orientate("Center", "Bottom-Center")
    player = player_class(pos=player_origin, radius=15, speed=4, sprite=None)
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
                show_framerate=True,
                quit_key=pygame.K_ESCAPE)

main_game(game)
