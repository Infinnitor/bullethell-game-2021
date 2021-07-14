import random


def fix_rgb(colour, min=1, max=255):
    assert min > 0 and max < 256, "Min and Max must be between 1 and 255"

    fixed_colour = []
    for c in colour:
        if c > max:
            c = max
        elif c < min:
            c = min

        fixed_colour.append(c)

    return tuple(fixed_colour)


def randomize_rgb(colour, upper=-20, lower=20):
    final_colour = [c + random.randint(upper, lower) for c in colour]
    return fix_rgb(final_colour)


class particles():
    def explosion(number, pos, speed, colour, game, lifetime=30, randcol=False, layer="HIGH"):
        for p in range(number):

            final_colour = colour
            if randcol is True:
                final_colour = randomize_rgb(colour)

            new_part = game.particle(
                                    pos=pos,
                                    size=15,
                                    speed=speed,
                                    angle=random.randint(0, 359),
                                    lifetime=lifetime,
                                    colour=final_colour)

            new_part.name = layer + "PARTICLE"
            game.add_sprite(new_part)
