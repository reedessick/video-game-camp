"""a module that defines the characters to be used within BoxBreaker
"""
__author__ = "Reed Essick (reed.essick@gmail.com)"

#-------------------------------------------------

import pygame

### non-standard libraries
from vgc import utils
BoundingBox = utils.BoundingBox
intersects = utils.intersect

#-------------------------------------------------

DEFAULT_WIDTH = 32
DEFAULT_HEIGHT = 32

DEFAULT_COLOR = (0, 0, 255)

#-------------------------------------------------

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
