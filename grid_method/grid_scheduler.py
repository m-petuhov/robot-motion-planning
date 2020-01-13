from common.drawer import *
from grid_method.visibility_graph import *
from grid_method.a_star_search import *
from collections import namedtuple


Circle = namedtuple("Circle", "x y r")


class GridScheduler:
    def __init__(self, data, dim, start, end):
        self.data = data
        self.dim = dim
        self.start = start
        self.end = end
        self.drawer = Drawer(self.dim, 'Path based on visibility graph')

        self._configure_environment()

        self.visibility_graph = self._build_visibility_graph()
        # self._draw_graph()

    def _configure_environment(self):
        (x, y) = self.start
        self.start = (x * self.dim, y * self.dim)
        (x, y) = self.end
        self.end = (x * self.dim, y * self.dim)

        for circle in self.data.circles:
            circle.x *= self.dim
            circle.y *= self.dim
            circle.r *= self.dim
            self.drawer.draw_circle(circle)

    def _draw_graph(self):
        for (i, node) in enumerate(self.visibility_graph.nodes):
            for (neighbor, _) in self.visibility_graph.neighbors(i):
                if i < neighbor:
                    self.drawer.draw_line(node, self.visibility_graph.nodes[neighbor])

    def _build_visibility_graph(self, epsilon=0.00001):
        circles = self.data.circles
        nodes = []
        for i in range(0, len(circles)):
            for j in range(i+1, len(circles)):
                tangents = get_tangents(circles[i], circles[j])

                for tangent in tangents:

                    # add in-between points
                    (p1, p2) = tangent
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]

                    # move points from the surface of the circle
                    d_epsilon = dx * epsilon
                    tangent = [(p1[0] + d_epsilon, p1[1] + d_epsilon), (p2[0] - d_epsilon, p2[1] - d_epsilon)]

                    for delta in range(1, 3+1):
                        d = delta / 4
                        tangent.append((p1[0] + dx * d, p1[1] + dy * d))

                    for p in tangent:
                        size = (self.dim, self.dim)
                        if point_lies_within_bounds(p, size) and not point_lies_within_circle(p, self.data.circles):
                            nodes.append(p)
                            self.drawer.draw_circle(Circle(p[0], p[1], self.dim / 100), Colors.REDUCTION_PATH_COLOR)

        return VisibilityGraph(nodes, circles)

    def build_path(self):
        closest_to_start = self.visibility_graph.get_closest_node(self.start)
        closest_to_end = self.visibility_graph.get_closest_node(self.end)

        result, _ = a_star_search(self.visibility_graph, closest_to_start, closest_to_end)
        path = [self.end, self.visibility_graph.nodes[closest_to_end]]

        if closest_to_end in result.keys():
            current_node = result[closest_to_end]
            while current_node is not None:
                path.append(self.visibility_graph.nodes[current_node])
                current_node = result[current_node]
            path.append(self.start)

            for (index, point) in enumerate(path[:-1]):
                p1, p2 = point, path[index + 1]
                self.drawer.draw_line(p1, p2, Colors.SHORTEST_PATH_COLOR)
        else:
            print("Goal is unreachable")

        while True:
            if self.drawer.check_exit():
                break
