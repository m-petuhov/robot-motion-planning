import random
import math

from common.Parser import Parser
from common.Drawer import Drawer, Colors


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def collides_point(point, circles):
    for circle in circles:
        if dist(point, [circle.x, circle.y]) <= circle.r:
            return True
    return False


def line_intersects_circle(ax, ay, bx, by, cx, cy, r):
    ax -= cx
    ay -= cy
    bx -= cx
    by -= cy
    a = math.pow(bx - ax, 2) + math.pow(by - ay, 2)
    b = 2 * (ax * (bx - ax) + ay * (by - ay))
    c = math.pow(ax, 2) + math.pow(ay, 2) - math.pow(r, 2)
    disc = math.pow(b, 2) - 4 * a * c

    if disc <= 0:
        return False
    sqrt_disc = math.sqrt(disc)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)
    if (0 < t1 < 1) or (0 < t2 < 1):
        return True
    return False


def collides_line(start_point, finish_point, circles):
    for circle in circles:
        if line_intersects_circle(start_point[0], start_point[1], finish_point[0], finish_point[1], circle.x, circle.y, circle.r):
            return True

    return False


def step_from_to(p1, p2, eps):
    if dist(p1, p2) < eps:
        return p2
    else:
        theta = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        return p1[0] + eps * math.cos(theta), p1[1] + eps * math.sin(theta)


# Helper class
class Node:
    def __init__(self, point, parent):
        self.point = point
        self.parent = parent


# Our scheduler
class RRTScheduler:
    def __init__(self, data, max_nodes, epsilon):
        self.data = data
        self.max_nodes = max_nodes
        self.epsilon = epsilon
        self.dim = 500
        self.drawer = Drawer(self.dim)

    def fit(self):
        start_point = Node((0, 0), None)
        finish_point = Node((self.dim, self.dim), None)
        current_state = 'buildTree'
        count = 0
        nodes = [start_point]

        for circle in self.data.circles:
            circle.x *= self.dim
            circle.y *= self.dim
            circle.r *= self.dim
            self.drawer.draw_circle(circle)

        while True:
            if current_state == 'goalFound':
                current_node = finish_point.parent

                while current_node.parent is not None:
                    self.drawer.draw_line(current_node.point, current_node.parent.point, Colors.SHORTEST_PATH_COLOR)
                    current_node = current_node.parent
            else:
                count = count + 1
                if count < self.max_nodes:
                    rand = random.random() * self.dim, random.random() * self.dim
                    parent_node = nodes[0]
                    for p in nodes:
                        if dist(p.point, rand) <= dist(parent_node.point, rand):
                            new_point = step_from_to(p.point, rand, self.epsilon)
                            if not collides_line(p.point, new_point, self.data.circles):
                                parent_node = p

                    new_node = step_from_to(parent_node.point, rand, self.epsilon)
                    if not collides_line(parent_node.point, new_node, self.data.circles):
                        nodes.append(Node(new_node, parent_node))
                        self.drawer.draw_line(parent_node.point, new_node)
                    else:
                        count -= 1

                    if dist(new_node, finish_point.point) < self.epsilon:
                        current_state = 'goalFound'
                        finish_point = nodes[len(nodes) - 1]


if __name__ == "__main__":
    trivial = Parser('data/mess.json')
    scheduler = RRTScheduler(trivial, 5000, 10)
    scheduler.fit()
