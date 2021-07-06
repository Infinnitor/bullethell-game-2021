import math


def circle_collide(p, q, attr=True):
    if attr:
        if math.dist((p.x, p.y), (q.x, q.y)) < p.r + q.r:
            return True
        return False

    else:
        if math.dist((p[0], p[1]), (q[0], q[1])) < p[2] + q[2]:
            return True
        return False


class offset_point():
    def __init__(self, parent, offset):

        self.parent = parent

        self.offset_x = offset[0]
        self.offset_y = offset[1]

        self.update_pos()

    def update_pos(self):
        self.x = self.parent.x + self.offset_x
        self.y = self.parent.y + self.offset_y

    def get_pos(self):
        self.update_pos()

        return [self.x, self.y]


class sine_bob():
    def __init__(self, wavelength, period):
        self.w = wavelength
        self.p = period

        self.x = 0
        self.y_mod = 0

    def update_pos(self):
        self.x += 0.01
        self.y_mod = self.w * math.sin(self.x * self.p)

    def get_pos(self, update=True):
        if update:
            self.update_pos()
            return self.y_mod
        else:
            return 0
