"""Very basic module to house different games. Each game is specified as a submodule, and this top-level interface allows users to select games from a list of automatically discovered games based on the submodules present herein.

We expect users to call this module via `python -m vgc` to launch their arcades.
"""

__author__ = 'Reed Essick (reed.essick@gmail.com)'

#-------------------------------------------------

from . import BoxBreaker
