import pygame
from pygame.locals import *
from enum import Enum


class Colors(Enum):
    FIELD_BACKGROUND_COLOR = [201, 211, 255]
    OBSTACLE_COLOR = [68, 57, 47]
    LINES_COLOR = [0, 0, 255]
    SHORTEST_PATH_COLOR = [255, 0, 0]


class Drawer(object):
    def __init__(self, size):
        self.size = size
        pygame.init()
        self.screen = pygame.display.set_mode([self.size, self.size])
        self._setup_field()

    def _setup_field(self):
        self.screen.fill(Colors.FIELD_BACKGROUND_COLOR.value)
        pygame.display.set_caption('Rapidly Exploring Random Tree')
        self._update()

    def draw_circle(self, circle):
        pygame.draw.circle(self.screen, Colors.OBSTACLE_COLOR.value, (int(circle.x), int(circle.y)), int(circle.r))

    def draw_line(self, p1, p2, line_color=Colors.LINES_COLOR):
        pygame.draw.line(self.screen, line_color.value, p1, p2)
        self._update()

    @staticmethod
    def _update():
        pygame.event.get()
        pygame.display.update()


if __name__ == "__main__":
    # drawer = Drawer(1000)
    # drawer.draw_line((0, 0), (100, 100))
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 500))
    screen.fill(Colors.FIELD_BACKGROUND_COLOR.value)
    pygame.display.set_caption('Rapidly Exploring Random Tree')

    while True:

        pygame.display.update()
        # clock.tick(10000)

