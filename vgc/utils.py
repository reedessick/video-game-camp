"""basic utilities that are helpful in many games"""
__author__ = "Reed Essick (reed.essick@gmail.com)"

#-------------------------------------------------

import random

#-------------------------------------------------

DEFAULT_WIDTH = 32
DEFAULT_HEIGHT = 32

DEFAULT_COLOR = (0, 0, 255)
RANDOM_COLOR = None

DEFAULT_MAX = 2048
DEFAULT_MIN = 0

#-------------------------------------------------

def random_character_placement(gamesize, charactersize):
    return (random.random() - 0.5)*(gamesize - charactersize)

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

#-------------------------------------------------

class BoundingBox(object):
    "a simple BoundingBox object that knows where it is and what color it should be colored"

    def __init__(self, x, y, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, color=RANDOM_COLOR):
        self._x = int(x)
        self._y = int(y)
        self._width = width
        self._height = height
        self._color = random_color() if color == RANDOM_COLOR else color

    @property
    def area(self):
        return self.width*self.height

    @property
    def color(self):
        return self._color

    @property
    def x_center(self):
        return self._x

    @property
    def y_center(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def left(self):
        return int(self._x - self._width/2)

    @property
    def right(self):
        return int(self._x + self._width/2)

    @property
    def top(self):
        return int(self._y + self._height/2)

    @property
    def bottom(self):
        return int(self._y - self._height/2)

    def intersects(self, other):
        return intersect(self, other)

    def move_left(self, dx, min_x=DEFAULT_MIN):
        self._x = int(max(self._x - dx, min_x))

    def move_right(self, dx, max_x=DEFAULT_MAX):
        self._x = int(min(self._x + dx, max_x))

    def move_down(self, dy, min_y=DEFAULT_MIN):
        self._y = int(max(self._y - dy, min_y))

    def move_up(self, dy, max_y=DEFAULT_MAX):
        self._y = int(min(self._y + dy, max_y))

#-------------------------------------------------

def is_between(low, x, high):
    """Determine whether x is between X1 and X2"""
    return (low <= x) and (x <= high)

def lines_overlap(x1, x2, y1, y2):
    return is_between(x1, y1, x2) or is_between(x1, y2, x2) or is_between(y1, x1, y2) or is_between(y1, x2, y2)

def intersect(B1, B2):
    """Determine whether two BoundingBox objects intersect! Use the properties of the 
    return either True or False"""
    return lines_overlap(B1.left, B1.right, B2.left, B2.right) and lines_overlap(B1.bottom, B1.top, B2.bottom, B2.top)
