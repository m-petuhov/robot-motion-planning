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
        self.path_start = Node((0, 0), None)
        self.path_end = Node((self.dim, self.dim), None)
        self.path = []

    def build_path(self):
        finish_point = self.path_end
        finish_flag = False
        count = 0
        nodes = [self.path_start]

        for circle in self.data.circles:
            circle.x *= self.dim
            circle.y *= self.dim
            circle.r *= self.dim
            self.drawer.draw_circle(circle)

        while True:
            if finish_flag:
                current_node = finish_point
                self.path.append(current_node.point)

                while current_node.parent is not None:
                    self.drawer.draw_line(current_node.point, current_node.parent.point, Colors.SHORTEST_PATH_COLOR)
                    current_node = current_node.parent
                    self.path.append(current_node.point)

                self.path.reverse()
                break
            elif count < self.max_nodes:
                rand = get_random_point(self.dim, self.dim)
                parent_node = nodes[0]

                for p in nodes:
                    if dist(p.point, rand) <= dist(parent_node.point, rand):
                        new_point = step_from_to(p.point, rand, self.epsilon)
                        if not collision_check(p.point, new_point, self.data.circles):
                            parent_node = p

                new_node = step_from_to(parent_node.point, rand, self.epsilon)
                if not collision_check(parent_node.point, new_node, self.data.circles):
                    nodes.append(Node(new_node, parent_node))
                    self.drawer.draw_line(parent_node.point, new_node)
                    count = count + 1

                if not collision_check(new_node, finish_point.point, self.data.circles):
                    finish_point.parent = Node(new_node, parent_node)
                    self.drawer.draw_line(finish_point.point, new_node)
                    finish_flag = True

        while True:
            if self.drawer.check_exit():
                break
