from pygame import transform, draw


# Sprite skeleton class
class sprite():

    def __repr__(self):
        self.highlight = 30
        return f"{self.name} at position {self.x}, {self.y}"

    def update_move(self, game):
        pass

    def update_draw(self, game):
        pass

    def update_destroy(self, game):
        pass

    def update_highlight(self, game):
        if self.highlight > 0:
            self.draw_highlight(game)
            self.highlight -= 1

    def draw_highlight(self, game):
        draw.rect(game.win, game.colours.green, (self.x, self.y, 20, 20))

    def add_default_attr(self):
        try:
            self.name
        except AttributeError:
            self.name = str(type(self))

        self.destroy = False
        self.highlight = 0

    def kill(self):
        self.destroy = True

    def onscreen(self, game):
        if self.x < 0 or self.x > game.win_w:
            return False
        if self.y < 0 or self.y > game.win_h:
            return False

        return True

    def onscreen_info(self, game):
        if self.x < 0 or self.x > game.win_w:
            return "X"
        if self.y < 0 or self.y > game.win_h:
            return "Y"

        return ""

    def center_image_pos(self, sprite, pos):
        i = sprite.get_size()

        x = pos[0] - (i[0] // 2)
        y = pos[1] - (i[0] // 2)

        return x, y

    def blit_rotate(self, image, angle, game):
        img = transform.rotate(image, angle)

        b_x = self.x - img.get_width()//2
        b_y = self.y - img.get_height()//2

        game.win.blit(img, (b_x, b_y))
