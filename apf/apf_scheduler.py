from common.common_functions import *
from common.drawer import *


class APFScheduler:
    """Scheduler implementing the artificial potential field.

    Parameters
    ----------
    data : object Parser, required
        Input data of algorithm.

    k_attraction : float, required
        Coefficient of attraction.

    k_repulsion : float, required
        Repulsion coefficient.

    d_repulsion : float, required
        Repulsive force range.

    max_iters : int, required
        Limit the number of iterations.

    step : float, required
        Size of step.
    """

    def __init__(self, data, k_attraction, k_repulsion, d_repulsion, max_iters, step):
        self.data = data
        self.k_attraction = k_attraction
        self.k_repulsion = k_repulsion
        self.d_repulsion = d_repulsion
        self.max_iters = max_iters
        self.step = step

        self.dim = 500
        self.start = [0, 0]
        self.goal = [self.dim, self.dim]
        self.path = []
        self.drawer = Drawer(self.dim, 'Artificial potential field')

        for circle in self.data.circles:
            circle.x *= self.dim
            circle.y *= self.dim
            circle.r *= self.dim

    def _attractive_force_function(self, current_position):
        return [self.k_attraction * (self.goal[0] - current_position[0]),
                self.k_attraction * (self.goal[1] - current_position[1])]

    def _repulsion_force_function(self, current_position):
        total = [0, 0]
        for circle in self.data.circles:
            distance = dist(current_position, [circle.x, circle.y])

            if distance <= circle.r:
                distance = 0
            else:
                distance -= circle.r

            t_vec = [(current_position[0] - circle.x - circle.r) / distance,
                     (current_position[1] - circle.y - circle.r) / distance]

            if distance <= self.d_repulsion:
                total[0] += t_vec[0] * self.k_repulsion * (1.0 / distance - 1.0 / self.d_repulsion) / (distance ** 2)
                total[1] += t_vec[1] * self.k_repulsion * (1.0 / distance - 1.0 / self.d_repulsion) / (distance ** 2)

        return total

    def fit(self):
        for circle in self.data.circles:
            self.drawer.draw_circle(circle)

        iters = 0
        current_position = self.start
        while iters < self.max_iters and dist(current_position, self.goal) != 0:
            attractive = self._attractive_force_function(current_position)
            repulsion = self._repulsion_force_function(current_position)
            f_vec = [attractive[0] + repulsion[0], attractive[1] + repulsion[1]]
            new_position = [current_position[0] + f_vec[0] * self.step, current_position[1] + f_vec[1] * self.step]

            self.drawer.draw_line(current_position, new_position, Colors.SHORTEST_PATH_COLOR)
            self.path.append(new_position)
            current_position = new_position
            iters += 1

        while True:
            if self.drawer.check_exit():
                break
