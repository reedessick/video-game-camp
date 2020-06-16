"""a module that defines the characters to be used within BoxBreaker
"""
__author__ = "Reed Essick (reed.essick@gmail.com)"

#-------------------------------------------------

import pygame

#-------------------------------------------------

DEFAULT_WIDTH = 32
DEFAULT_HEIGHT = 32

DEFAULT_COLOR = (0, 0, 255)

DEFAULT_MAX = 2048
DEFAULT_MIN = 0

#-------------------------------------------------

class BoundingBox(object):
    "a simple BoundingBox object that knows where it is and what color it should be colored"

    def __init__(self, x, y, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, color=DEFAULT_COLOR):
        self._x = int(x)
        self._y = int(y)
        self._width = width
        self._height = height
        self._color = color

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

    def move_left(self, dx, min_x=DEFAULT_MIN):
        self._x = int(max(self._x - dx, min_x))

    def move_right(self, dx, max_x=DEFAULT_MAX):
        self._x = int(min(self._x + dx, max_x))

    def move_down(self, dy, min_y=DEFAULT_MIN):
        self._y = int(max(self._y - dy, min_y))

    def move_up(self, dy, max_y=DEFAULT_MAX):
        self._y = int(min(self._y + dy, max_y))

class Character(BoundingBox):
    """a simple extension of BoundingBox that also tracks the character's name and other attributes.
NOTE, characters are represented with a BoundingBox but they are drawn as circles. This means that they may not appear to exactly overlap in the screen even though the code acts as if they do."""

    def __init__(self, name, x, y, radius=DEFAULT_WIDTH, color=DEFAULT_COLOR):
        self._name = name
        self._radius = radius
        self.invert_color = False
        BoundingBox.__init__(self, x, y, width=2*radius, height=2*radius, color=color)

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        r, g, b = self._color
        if self.invert_color:
            r = 255 - r
            g = 255 - g
            b = 255 - b
        return (r, g, b)

    @property
    def radius(self):
        return self._radius

    def draw(self, screen, level):
        pygame.draw.circle(screen, self.color, (self.x_center - level.left, self.y_center - level.bottom), self.radius, 2)

class Opponent(Character):
    """an opponent rather than a character"""

    def draw(self, screen, level):
        pygame.draw.rect(screen, self.color, (self.left - level.left, self.bottom - level.bottom, self.width, self.height))

#-------------------------------------------------

def D(X1, x, X2):
    """Determine whether x is between X1 and X2"""
    A = X1 <= x
    B = x <= X2
    return A and B

def overlap(x1, x2, y1, y2):
    AandB = D(x1, y1, x2)
    CandD = D(x1, y2, x2)
    return (AandB or CandD)

def intersects(B1, B2):
    """Determine whether two BoundingBox objects intersect! Use the properties of the 
    return either True or False"""
    overlap_in_x = overlap(B1.left, B1.right, B2.left, B2.right)
    overlap_in_y = overlap(B1.bottom, B1.top, B2.bottom, B2.top)

    return (overlap_in_x and overlap_in_y)
