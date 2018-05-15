"""
Insipred by the Coding Challange #98 Quadtree, by Daniel Shiffman
https://www.youtube.com/watch?v=OJxEcs0w_kE&t=1s
"""


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:

    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def __str__(self):
        return "Start point: {}, {} \n" \
               "End point: {}, {}".format(self.x0, self.y0, self.x1, self.y1)


class QuadTree:

    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []

    def subdivide(self):
        x_half = (self.boundary.x1 - self.boundary.x0) / 2
        y_half = (self.boundary.y1 - self.boundary.y0) / 2

        northeast = Rectangle(x_half, y_half,
                              self.boundary.x1, self.boundary.y1)
        northwest = Rectangle(self.boundary.x0, y_half,
                              x_half, self.boundary.y1)
        southwest = Rectangle(self.boundary.x0, self.boundary.y0,
                              x_half, y_half)
        southeast = Rectangle(x_half, self.boundary.y0,
                              self.boundary.x1, y_half)

    def insert(self, point):
        if len(self.points) < self.capacity:
            pass
        else:
            self.subdivide()


#


root_bound = Rectangle(0., 0., 1., 1.)

new_tree = QuadTree(root_bound, 1)


print(new_tree.boundary)

