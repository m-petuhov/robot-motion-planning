from common.common_functions import collision_check
from common.drawer import *


class Smooth:
    """Smooth implementing different algorithms.

    Parameters
    ----------
    data : object Parser, required
        Input data.

    path : list, required
        List of path points.
    """

    def __init__(self, data, path):
        self.data = data
        self.path = path

        self.dim = 500
        self.drawer = Drawer(self.dim, 'Smoothing')

    def reduction(self):
        for circle in self.data.circles:
            self.drawer.draw_circle(circle)

        begin_point = self.path[0]
        for end_point in self.path[1:]:
            self.drawer.draw_line(begin_point, end_point, Colors.SHORTEST_PATH_COLOR)
            begin_point = end_point

        start = 0
        current = len(self.path) - 1
        while self.path[start][0] != self.path[-1][0] and self.path[start][1] != self.path[-1][1]:
            if not collision_check(self.path[start], self.path[current], self.data.circles):
                self.drawer.draw_line(self.path[start], self.path[current], Colors.REDUCTION_PATH_COLOR)
                indent = len(self.path) - current
                self.path = self.path[:start + 1] + self.path[current:]
                start = len(self.path) - indent
                current = len(self.path) - 1
            else:
                current -= 1

        while True:
            if self.drawer.check_exit():
                break
