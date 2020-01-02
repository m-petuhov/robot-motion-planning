import pygame
from enum import Enum


class Colors(Enum):
    FIELD_BACKGROUND_COLOR = [201, 211, 255]
    OBSTACLE_COLOR = [68, 57, 47]
    LINES_COLOR = [0, 0, 255]
    SHORTEST_PATH_COLOR = [255, 0, 0]


class Drawer(object):
    def __init__(self, size, title=''):
        self.size = size
        pygame.init()
        self.screen = pygame.display.set_mode([self.size, self.size])
        self._setup_field(title)

    @staticmethod
    def _update():
        pygame.event.get()
        pygame.display.update()

    def _setup_field(self, title):
        self.screen.fill(Colors.FIELD_BACKGROUND_COLOR.value)
        pygame.display.set_caption(title)
        self._update()

    def draw_circle(self, circle):
        pygame.draw.circle(self.screen, Colors.OBSTACLE_COLOR.value, (int(circle.x), int(circle.y)), int(circle.r))

    def draw_line(self, p1, p2, line_color=Colors.LINES_COLOR):
        pygame.draw.line(self.screen, line_color.value, p1, p2)
        self._update()
