import random

from common.drawer import *
from common.common_functions import *


def get_random_point(x_dim, y_dim):
    return random.random() * x_dim, random.random() * y_dim


def step_from_to(p1, p2, eps):
    if dist(p1, p2) < eps:
        return p2
    else:
        theta = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        return p1[0] + eps * math.cos(theta), p1[1] + eps * math.sin(theta)


class RRTScheduler:
    def __init__(self, data, max_nodes, epsilon):
        self.data = data
        self.max_nodes = max_nodes
        self.epsilon = epsilon
        self.dim = 500
        self.drawer = Drawer(self.dim, 'Rapidly Exploring Random Tree')

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
                    rand = get_random_point(self.dim, self.dim)
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
