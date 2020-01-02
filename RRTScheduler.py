import pygame
import random
import math
import sys

from Parser import Parser
from pygame.locals import *


# Helper functions
def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def collides_point(point, circles):
    for circle in circles:
        if dist(point, [circle['X'], circle['Y']]) <= circle['R']:
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

    if (disc <= 0):
        return False
    sqrtdisc = math.sqrt(disc)
    t1 = (-b + sqrtdisc) / (2 * a)
    t2 = (-b - sqrtdisc) / (2 * a)
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
        self.dim = 500
        self.max_nodes = max_nodes
        self.epsilon = epsilon

    def fit(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode([self.dim, self.dim])
        start_point = Node((0, 0), None)
        finish_point = Node((self.dim, self.dim), None)
        current_state = 'buildTree'
        count = 0
        nodes = [start_point]

        screen.fill([201, 211, 255])
        pygame.display.set_caption('Rapidly Exploring Random Tree')

        for circle in self.data.circles:
            circle.x *= self.dim
            circle.y *= self.dim
            circle.r *= self.dim
            pygame.draw.circle(screen, [68, 57, 47], (int(circle.x), int(circle.y)), int(circle.r))

        while True:
            if current_state == 'goalFound':
                current_node = finish_point.parent

                while current_node.parent is not None:
                    pygame.draw.line(screen, [255, 0, 0], current_node.point, current_node.parent.point)
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
                        pygame.draw.line(screen, [0, 0, 255], parent_node.point, new_node)
                    else:
                        count -= 1

                    if dist(new_node, finish_point.point) < self.epsilon:
                        current_state = 'goalFound'
                        finish_point = nodes[len(nodes) - 1]

            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                    sys.exit("Exiting")

            pygame.display.update()
            clock.tick(10000)


if __name__ == "__main__":
    trivial = Parser('Data/mess.json')
    scheduler = RRTScheduler(trivial, 5000, 10)
    scheduler.fit()
