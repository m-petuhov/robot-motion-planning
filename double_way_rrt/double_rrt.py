from rrt.rrt_scheduler import *


def find_closest_node(vertices, point):
    shortest_dist = dist(vertices[0].point, point)
    closest_node = vertices[0]
    for vertex in vertices:
        current_dist = dist(vertex.point, point)
        if current_dist < shortest_dist:
            shortest_dist = current_dist
            closest_node = vertex

    return closest_node


class DoubleRRT:
    def __init__(self, data, epsilon):
        self.data = data
        self.dim = 500
        self.drawer = Drawer(self.dim, 'Two Rapidly Exploring Random Trees')
        self.epsilon = epsilon
        self.path = []

        self._configure_environment()

    def _configure_environment(self):
        for circle in self.data.circles:
            circle.x *= self.dim
            circle.y *= self.dim
            circle.r *= self.dim
            self.drawer.draw_circle(circle)

    def _add_and_draw(self, tree, node):
        tree.append(node)
        self.drawer.draw_line(node.point, node.parent.point)

    def _draw_path_to_root(self, node):
        while node.parent is not None:
            self.drawer.draw_line(node.point, node.parent.point, Colors.SHORTEST_PATH_COLOR)
            node = node.parent

    def _expand_tree(self, tree):
        while True:
            random_point = get_random_point(self.dim, self.dim)
            closest_node = find_closest_node(tree, random_point)
            new_point = step_from_to(closest_node.point, random_point, self.epsilon)
            if not collision_check(new_point, closest_node.point, self.data.circles):
                self._add_and_draw(tree, Node(new_point, closest_node))
                return

    def build_path(self):
        tree_1 = [Node((0, 0), None)]
        tree_2 = [Node((self.dim, self.dim), None)]

        did_bridge_trees = False

        while not did_bridge_trees:
            self._expand_tree(tree_1)
            added_node = tree_1[-1]
            closest_node = find_closest_node(tree_2, added_node.point)

            if not collision_check(added_node.point, closest_node.point, self.data.circles):
                self._add_and_draw(tree_1, Node(closest_node.point, added_node))
                self._draw_path_to_root(tree_1[-1])
                self._draw_path_to_root(closest_node)
                did_bridge_trees = True

                node = tree_1[-1]
                self.path.append(node.point)
                while node.parent is not None:
                    node = node.parent
                    self.path.append(node.point)

                node = closest_node
                self.path.reverse()
                self.path.append(node.point)
                while node.parent is not None:
                    node = node.parent
                    self.path.append(node.point)
            else:
                # swap trees for the next iteration
                tree_1, tree_2 = tree_2, tree_1

        while True:
            if self.drawer.check_exit():
                break
