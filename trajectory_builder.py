from common.common_functions import collision_check
from common.drawer import *


class TrajectoryBuilder:
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

    def _step_from_to(self, start_point, end_point, forces, i=1):
        necessary_force = (((end_point[0] - start_point[0]) / self.data.dt**2) / self.dim / i**2,
                               ((end_point[1] - start_point[1]) / self.data.dt**2) / self.dim / i**2)

        if necessary_force[0] ** 2 + necessary_force[1] ** 2 <= self.data.fmax ** 2:
            for j in range(i):
                forces.append([necessary_force[0], necessary_force[1]])
            for j in range(i):
                forces.append([-necessary_force[0], -necessary_force[1]])
        else:
            self._step_from_to(start_point, end_point, forces, i*2)

    def reduction(self):
        for circle in self.data.circles:
            self.drawer.draw_circle(circle)

        start_point = self.path[0]
        for end_point in self.path[1:]:
            self.drawer.draw_line(start_point, end_point, Colors.SHORTEST_PATH_COLOR)
            start_point = end_point

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

    def simple_robot_motion(self):
        forces = []

        for i in range(1, len(self.path)):
            self._step_from_to(self.path[i - 1], self.path[i], forces)

        forces.append([0, 0])
        return forces
