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
    [0, 0],
    [200, 0],
    [200, 200],
    [0, 200],
]

sq2 = [
    [-50, -50],
    [50, -50],
    [50, 50],
    [-50, 50],
]

tr1 = [
    [0, 0],
    [0, 200],
    [100, 0],
    [100, 0],
]

tr2 = [
    [0, 0],
    [200, 0],
    [100, 200],
    [100, 200]
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

# morph = mv_u.polygon(sq1, sq2, tr1, tr2, dm1, dm2)
morph = mv_u.offset_polygon(sq1, sq2, tr1, tr2, dm1, dm2, offset=(0, 0))
iter = 0

while game.run:
    game.update_keys()
    game.update_draw()

    start_morph = False
    if game.check_key(pygame.K_LEFT, buffer=True):
        iter -= 1
        if iter < 0:
            iter = 0
        start_morph = True

    elif game.check_key(pygame.K_RIGHT, buffer=True):
        iter += 1
        if iter > len(morph.shapes) - 1:
            iter = len(morph.shapes) - 1

        start_morph = True

    if start_morph:
        if morph.morphing is False:
            morph.init_morph(iter, frames=20)
            start_morph = False

    # pygame.draw.polygon(game.win, colours.red, morph.get())
    m = morph.get(game.mouse_pos)
    pygame.draw.polygon(game.win, colours.fullcyan, m)

    for i, lines, in enumerate(zip(morph.morph1, morph.morph2)):
        pygame.draw.line(game.win, colours.green, lines[0], lines[1], 2)

    game.update_scaled()
    game.update_state()

pygame.quit()
