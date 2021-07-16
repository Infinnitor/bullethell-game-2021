from gameinfo import game_info, pygame, time, math, random
from colour_manager import colours

import draw_utils as draw_u
import move_utils as mv_u

import enemies
import bullets

from sprite_class import sprite


game = game_info(
                name="Launched from module py file",
                win_w=1280,
                win_h=720,
                user_w=1280,
                user_h=720,
                bg=(0, 0, 0),
                framecap=60,
                show_framerate=False,
                quit_key=pygame.K_ESCAPE)

sq1 = [
    [200, 200],
    [400, 200],
    [400, 400],
    [200, 400],
]

sq2 = [
    [250, 250],
    [350, 250],
    [350, 350],
    [250, 350],
]

tr1 = [
    [400, 400],
    [200, 400],
    [300, 200],
    [300, 200],
]

morph = mv_u.polygon_morph(sq1, sq2, tr1)
morph.init_morph(1, frames=20)
ln = 2

while game.run:
    game.update_keys()
    game.update_draw()

    if game.check_key(pygame.K_LEFT):
        morph.init_morph(1, frames=20)
    elif game.check_key(pygame.K_RIGHT):
        morph.init_morph(0, frames=20)
    elif game.check_key(pygame.K_UP):
        morph.init_morph(2, frames=20)

    pygame.draw.polygon(game.win, colours.red, morph.get())

    pygame.draw.line(game.win, colours.blue, sq1[0], sq1[1], ln)
    pygame.draw.line(game.win, colours.blue, sq1[1], sq1[2], ln)
    pygame.draw.line(game.win, colours.blue, sq1[2], sq1[3], ln)
    pygame.draw.line(game.win, colours.blue, sq1[3], sq1[0], ln)

    pygame.draw.line(game.win, colours.green, sq2[0], sq2[1], ln)
    pygame.draw.line(game.win, colours.green, sq2[1], sq2[2], ln)
    pygame.draw.line(game.win, colours.green, sq2[2], sq2[3], ln)
    pygame.draw.line(game.win, colours.green, sq2[3], sq2[0], ln)

    for l1, l2 in zip(morph.morph1, morph.sorted_points):
        pygame.draw.line(game.win, colours.red, l1, l2, ln)

    game.update_scaled()
    game.update_state()

pygame.quit()
