from common.common_functions import *


class VisibilityGraph:
    def __init__(self, nodes, obstacles):
        self.nodes = nodes
        self.obstacles = obstacles
        self.edges = {}

        self._connect_all_neighbours()

    def _connect_nodes(self, n1, n2):
        weight = dist(self.nodes[n1], self.nodes[n2])
        self.edges[n1] = self.edges.get(n1, []) + [(n2, weight)]
        self.edges[n2] = self.edges.get(n2, []) + [(n1, weight)]

    def _connect_all_neighbours(self):
        for i in range(0, len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                print(i, "/", len(self.nodes), " ", j, "/", len(self.nodes))
                if not collision_check(self.nodes[i], self.nodes[j], self.obstacles):
                    self._connect_nodes(i, j)

    def neighbors(self, node):
        return self.edges[node]

    def get_closest_node(self, point):
        closest_node = 0
        shortest_dist = 1000
        for i, node in enumerate(self.nodes):
            current_dist = dist(node, point)
            if current_dist < shortest_dist and not collision_check(point, node, self.obstacles):
                shortest_dist = current_dist
                closest_node = i

        return closest_node


def get_tangents(circle_a, circle_b):
    (x1, y1, r1) = circle_a
    (x2, y2, r2) = circle_b

    d_sq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
    if d_sq <= (r1 - r2) * (r1 - r2):
        return []

    d = math.sqrt(d_sq)
    vx = (x2 - x1) / d
    vy = (y2 - y1) / d

    res = []

    # Let A, B be the centers, and C, D be points at which the tangent
    # touches first and second circle, and n be the normal vector to it.
    #
    # We have the system:
    #   n * n = 1          (n is a unit vector)
    #   C = A + r1 * n
    #   D = B +/- r2 * n
    #   n * CD = 0         (common orthogonality)
    #
    # n * CD = n * (AB +/- r2*n - r1*n) = AB*n - (r1 -/+ r2) = 0,  <=>
    # AB * n = (r1 -/+ r2), <=>
    # v * n = (r1 -/+ r2) / d,  where v = AB/|AB| = AB/d
    # This is a linear equation in unknown vector n.

    for sign1 in [-1, 1]:
        c = (r1 - sign1 * r2) / d
        c_squared = c*c

        # Now we're just intersecting a line with a circle: v*n=c, n*n=1

        if c_squared > 1.0:
            continue
        h = math.sqrt(max(0.0, 1.0 - c_squared))

        for sign2 in [-1, 1]:
            nx = vx * c - sign2 * h * vy
            ny = vy * c + sign2 * h * vx

            res.append([(x1 + r1 * nx, y1 + r1 * ny), (x2 + sign1 * r2 * nx, y2 + sign1 * r2 * ny)])

    return res
