# Sprite skeleton class
class sprite():

    def update_move(self, game):
        pass

    def update_draw(self, game):
        pass

    def update_destroy(self, game):
        pass

    def add_default_attr(self):
        self.destroy = False

    def kill(self):
        self.destroy = True

    def onscreen(self, game):
        if self.x < 0 or self.x > game.win_w:
            return False
        if self.y < 0 or self.y > game.win_h:
            return False

        return True
