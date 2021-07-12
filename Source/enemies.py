from sprite_class import sprite
import pygame
import random


class enemy_class(sprite):
    def __init__(self, pos, radius, sprites=None):
        self.name = "ENEMY"

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
        if self.sprites is not None:
            a_dest = self.center_image_pos(self.sprites, (self.x, self.y))

            game.win.blit(self.sprites, a_dest)

        else:
            pygame.draw.circle(game.win, self.colour, (self.x, self.y), self.r)

    def flash(self):
        self.colour = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
