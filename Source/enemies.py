from sprite_class import sprite
from pygame import draw
import random
import draw_utils as draw_u


class enemy_class(sprite):
    def __init__(self, pos, radius, sprites=None):
        self.layer = "ENEMY"

        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.colour = (50, 50, 50)
        self.sprites = sprites

        self.up = random.choice((True, False))

    def update_move(self, game):

        if self.y < self.r or self.y > 500:
            self.up = not self.up

        if self.up:
            self.y -= 4
        else:
            self.y += 4

    def update_draw(self, game):
        self.colour = draw_u.rgb.compliment(game.bg)

        if self.sprites is not None:
            a_dest = self.center_image_pos(self.sprites, (self.x, self.y))

            game.win.blit(self.sprites, a_dest)

        else:
            draw.circle(game.win, self.colour, (self.x, self.y), self.r)

        self.update_highlight(game)

    def flash(self):
        self.colour = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))


class enemy_explosion(sprite):
    def __init__(self, pos, speed):
        self.layer = "BACKGROUND"

        self.x = pos[0]
        self.y = pos[1]
