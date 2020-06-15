"""a module that defines the levels we will use in BoxBreaker
"""
__author__ = "Reed Essick (reed.essick@gmail.com)"

#-------------------------------------------------

DEFAULT_GAMEWIDTH = 800
DEFAULT_GAMEHEIGHT = 800

DEFAULT_COLOR = (255, 255, 255) ### white

#-------------------------------------------------

from . import characters

#-------------------------------------------------

class Level(characters.BoundingBox):
    "a simple Level object that knows how big the level is and what color it should be"

    def __init__(self, width=DEFAULT_GAMEWIDTH, height=DEFAULT_GAMEHEIGHT, color=DEFAULT_COLOR):
        characters.BoundingBox.__init__(self, 0., 0., width=width, height=height, color=color)

    def in_bounds(self, other):
        """determine whether other is within the board's scope or not"""
        return (self.left <= other.left) and (self.right >= other.right) and (self.top >= other.top) and (self.bottom <= other.bottom)
