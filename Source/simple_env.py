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

tr2 = [
    [200, 200],
    [400, 200],
    [300, 400],
    [300, 400]
]

dm1 = [
    [300, 200],
    [400, 300],
    [300, 400],
    [200, 300]
]

dm2 = [
    [500, 200],
    [600, 300],
    [500, 400],
    [400, 300]
]

morph = mv_u.polygon_morph(sq1, sq2, tr1, tr2, dm1, dm2)
morph.init_morph(1, frames=20)
ln = 2
iter = 0

while game.run:
    game.update_keys()
    game.update_draw()

    if game.check_key(pygame.K_LEFT, buffer=True):
        iter -= 1
        if iter < 0:
            iter = 0
    elif game.check_key(pygame.K_RIGHT, buffer=True):
        iter += 1
        if iter > len(morph.shapes) - 1:
            iter = len(morph.shapes) - 1

    if morph.morphing is False:
        morph.init_morph(iter, frames=10)

    # if game.check_key(pygame.K_LEFT):
    #     morph.init_morph(0, frames=10)
    # elif game.check_key(pygame.K_RIGHT):
    #     morph.init_morph(1, frames=10)
    # elif game.check_key(pygame.K_UP):
    #     morph.init_morph(2, frames=10)
    # elif game.check_key(pygame.K_DOWN):
    #     morph.init_morph(3, frames=10)

    pygame.draw.polygon(game.win, colours.blue, morph.shapes[iter - 1])
    pygame.draw.polygon(game.win, colours.red, morph.get())

    for l1, l2 in zip(morph.morph1, morph.sorted_points):
        pygame.draw.line(game.win, colours.green, l1, l2, ln)

    game.update_scaled()
    game.update_state()

pygame.quit()
