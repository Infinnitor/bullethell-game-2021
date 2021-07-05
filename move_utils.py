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
