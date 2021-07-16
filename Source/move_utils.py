import math
import copy


def circle_collide(p, q, add=[], attr=True):
    if attr:
        if math.dist((p.x, p.y), (q.x, q.y)) < p.r + q.r + sum(add):
            return True
        return False

    else:
        if math.dist((p[0], p[1]), (q[0], q[1])) < p[2] + q[2] + sum(add):
            return True
        return False


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


class poly_morph():

    def init_morph_calc(self):

        self.sorted_points = []
        morph2 = copy.copy(self.morph2)

        for iter, p1 in enumerate(self.morph1):

            points_dist = []
            for p2 in morph2:
                points_dist.append(math.dist(p1, p2))

            print(points_dist)
            print(min(points_dist))
            for i, dist in enumerate(points_dist):
                if dist == min(points_dist):
                    print(True)
                    self.sorted_points.append(morph2.pop(i))
                    break

        self.sorted_points_mv = []
        for a, b in zip(self.morph1, self.sorted_points):
            x_d = b[0] - a[0]
            y_d = b[1] - a[1]

            self.sorted_points_mv.append([x_d, y_d])

    def morph(self):
        ret = []
        for c, d in zip(self.morph1, self.sorted_points_mv):
            mv_x = c[0] + (d[0] * (self.iter / 100))
            mv_y = c[1] + (d[1] * (self.iter / 100))
            ret.append([mv_x, mv_y])

        return ret


class polygon_morph(poly_morph):
    def __init__(self, *shapes):
        self.shapes = shapes
        self.polygon = self.shapes[0]

        self.step = 1
        self.iter = 0

        self.morphing = False
        self.target = 0

    def add(self, new_shape):
        self.shapes.append(new_shape)

    def init_morph(self, target, step):

        if target == self.target:
            return

        self.morphing = True
        self.target = target

        self.morph1 = self.polygon
        self.morph2 = self.shapes[target]

        self.iter = 0
        self.step = step

        self.init_morph_calc()

    def get(self):
        if self.iter < 100:
            self.iter += self.step
        else:
            self.iter = 100
            self.morphing = False

        if self.morphing is True:
            self.polygon = self.morph()

        return self.polygon
