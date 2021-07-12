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


def circle_dist(p, q, attr=True):
    if attr:
        return math.dist((p.x, p.y), (q.x, q.y))
    else:
        return math.dist((p[0], p[1]), (q[0], q[1]))


def rect_collide(a, b, attr=True):

    if attr:
        a = (a.x, a.y, a.width, a.height)
        b = (b.x, b.y, b.width, b.height)

    def within_x(x, r):
        if x > r[0] and x < r[1]:
            return True
        return False

    def within_y(y, r):
        if y > r[0] and y < r[1]:
            return True
        return False

    b_x = (b[0], b[2])
    b_y = (b[1], b[3])

    if within_x(a[0], b_x) and within_y(a[1], b_y):
        return True

    if within_x(a[2], b_x) and within_x(a[3], b_y):
        return True

    return False


class offset():
    def update_pos(self):
        self.x = self.parent.x + self.offset_x
        self.y = self.parent.y + self.offset_y


class offset_point(offset):
    def __init__(self, parent, offset):

        self.parent = parent

        self.offset_x = offset[0]
        self.offset_y = offset[1]

        self.update_pos()

    def get_pos(self):
        self.update_pos()

        return [self.x, self.y]


class offset_circle(offset):
    def __init__(self, parent, offset, radius):

        self.parent = parent

        self.offset_x = offset[0]
        self.offset_y = offset[1]

        self.update_pos()
        self.r = radius

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
