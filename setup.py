#!/usr/bin/env python

__usage__ = "setup.py command [--options]"
__description__ = "standard install script"
__author__ = "Reed Essick (reed.essick@gmail.com)"

#-------------------------------------------------

from setuptools import (setup, find_packages)
import glob

setup(
    name = 'vgc',
    version = '0.0',
    url = 'https://github.com/reedessick/video-game-camp',
    author = __author__,
    author_email = 'reed.essick@gmail.com',
    description = __description__,
    license = 'MIT',
    scripts = glob.glob('bin/*'),
    packages = find_packages(),
    data_files = [],
    requires = [],
)

