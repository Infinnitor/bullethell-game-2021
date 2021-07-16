import math
import random


def circle_collide(p, q, add=[], attr=True):
    if attr:
        if math.dist((p.x, p.y), (q.x, q.y)) < p.r + q.r + sum(add):
            return True
        return False

    else:
        if math.dist((p[0], p[1]), (q[0], q[1])) < p[2] + q[2] + sum(add):
            return True
        return False


def midpoint(p, q, attr=True, rounding=False):
    if attr:
        ret = [(p.x + q.x) / 2, (p.y + q.y) / 2]
    else:
        ret = [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2]

    if rounding:
        ret = [round(r) for r in ret]
    return ret


def polygon_adjust(polygon, x=0, y=0):
    new_polygon = []
    for point in polygon:
        new_polygon.append((point[0] + x, point[1] + y))

    return new_polygon


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
    def update_pos(self, anchor=(0, 0)):
        if self.parent is not None:
            anchor = (self.parent.x, self.parent.y)

        self.x = anchor[0] + self.offset_x
        self.y = anchor[1] + self.offset_y

    def get_pos(self, anchor=(0, 0)):
        self.update_pos(anchor)

        return [self.x, self.y]


class offset_point(offset):
    def __init__(self, parent, offset):

        self.parent = parent

        self.offset_x = offset[0]
        self.offset_y = offset[1]

        self.update_pos()


class offset_circle(offset):
    def __init__(self, parent, offset, radius):

        self.parent = parent

        self.offset_x = offset[0]
        self.offset_y = offset[1]

        self.update_pos()
        self.r = radius


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


class morph():

    def log_shapes(self, shapes):
        self.shapes = shapes
        assert sum([len(s) for s in self.shapes]) == max([len(s) for s in self.shapes]) * len(self.shapes), "All shapes must have an equal amount of points"

        self.polygon = self.shapes[0]

        self.step = 1
        self.iter = 0

        self.morphing = False
        self.target = 0

        self.init_morph(0, frames=1)

    def add(self, new_shape):
        assert len(new_shape) == max([len(s) for s in self.shapes]), "Number of points on added shape must be equal to that of existing shapes"
        self.shapes.append(new_shape)

    def init_morph(self, target, frames):

        self.morph1 = self.polygon
        self.morph2 = self.shapes[target]
        if target == self.target:
            return

        self.morphing = True
        self.target = target

        self.iter = 0
        self.step = 100 / frames

        self.init_morph_calc()

    def init_morph_calc(self):

        self.sorted_points_mv = []
        for a, b in zip(self.morph1, self.morph2):
            x_d = b[0] - a[0]
            y_d = b[1] - a[1]

            self.sorted_points_mv.append([x_d, y_d])

    def morph(self):
        morph_polygon = []
        for c, d in zip(self.morph1, self.sorted_points_mv):
            mv_x = c[0] + (d[0] * (self.iter / 100))
            mv_y = c[1] + (d[1] * (self.iter / 100))
            morph_polygon.append([mv_x, mv_y])

        self.polygon = morph_polygon


class polygon(morph):

    def __init__(self, *shapes):
        self.log_shapes(shapes)

    def get(self):
        if self.iter < 100:
            self.iter += self.step
        else:
            self.iter = 100
            self.morphing = False

        if self.morphing is True:
            self.morph()

        return self.polygon


class offset_polygon(offset, morph):
    def __init__(self, *shapes, offset, parent=None):

        self.offset_x = offset[0]
        self.offset_y = offset[1]

        self.parent = parent

        self.log_shapes(shapes)

    def get(self, anchor=(0, 0)):
        if self.iter < 100:
            self.iter += self.step
        else:
            self.iter = 100
            self.morphing = False

        self.update_pos(anchor)

        if self.morphing is True:
            self.morph()

        ret_polygon = []
        for x, y in self.polygon:
            ret_polygon.append([x + self.x, y + self.y])

        print(ret_polygon)

        return ret_polygon
