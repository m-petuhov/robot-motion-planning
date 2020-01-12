import math


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def point_lies_within_circle(point, circles):
    for circle in circles:
        if dist(point, [circle.x, circle.y]) <= circle.r:
            return True
    return False


def line_intersects_circle(p1, p2, circle):
    ax = p1[0] - circle.x
    ay = p1[1] - circle.y
    bx = p2[0] - circle.x
    by = p2[1] - circle.y
    a = math.pow(bx - ax, 2) + math.pow(by - ay, 2)
    b = 2 * (ax * (bx - ax) + ay * (by - ay))
    c = math.pow(ax, 2) + math.pow(ay, 2) - math.pow(circle.r, 2)
    disc = math.pow(b, 2) - 4 * a * c

    if disc <= 0:
        return False
    sqrt_disc = math.sqrt(disc)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)
    if (0 < t1 < 1) or (0 < t2 < 1):
        return True
    return False


def collision_check(start_point, finish_point, circles):
    for circle in circles:
        if line_intersects_circle(start_point, finish_point, circle):
            return True

    return False


class Node:
    def __init__(self, point, parent):
        self.point = point
        self.parent = parent
