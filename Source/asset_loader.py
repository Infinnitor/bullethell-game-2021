from pygame import image


class player_assets():
    def __init__(self):
        self.default = image.load('data/sprites/player/PlayerSmall.png')
        self.default.set_colorkey((0, 0, 0))

player = player_assets()
