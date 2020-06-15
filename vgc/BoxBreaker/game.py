"""utility functions for BoxBreaker"""

__author__ = "Reed Essick (reed.essick@gmail.com)"

#-------------------------------------------------

import random
import pygame

from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, KEYUP, QUIT)

### non-standard libraries
from . import characters
from . import levels

#-------------------------------------------------

def random_character_placement(gamesize, charactersize):
    return (random.random() - 0.5)*(gamesize - charactersize)

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

#-------------------------------------------------

def main(**kwargs):
    """Launch the game and enter the main loop!"""

    print('Welcome to BoxBreaker!')
    pygame.init()

    for level_name, level in [('Level 1', level1)]:
        print('Entering '+level_name)
        if not level(**kwargs): ### we quit out of the level, so we should exit the game
            break

    print('Exiting BoxBreaker!')
    pygame.quit()

#------------------------

def loop(level, player, others, player_speed=5):
    """execute the main loop that drives the game"""
    screen = pygame.display.set_mode([level.width, level.height]) ### set the screen to match the level
    screen.fill(level.color) ### fill in the background color for the level

    pressed = dict()
    running = True
    while running:
        for event in pygame.event.get():
            print(event)
            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE): ### clicked the close button or pressed escape
                running = False

            elif event.type == KEYDOWN:
                pressed[event.key] = True

            elif event.type == KEYUP:
                pressed[event.key] = False

        for key in [key for key, is_pressed in pressed.items() if is_pressed]:
            if key == K_DOWN:
                player.move_up(player_speed, max_y=level.top)

            elif key == K_UP:
                player.move_down(player_speed, min_y=level.bottom)

            elif key == K_LEFT:
                player.move_left(player_speed, min_x=level.left)

            elif key == K_RIGHT:
                player.move_right(player_speed, max_x=level.right)

        ### make the background the level's color
        screen.fill(level.color)

        ### draw the others on the screen
        for other in others:
            if characters.intersects(player, other):
                other.invert_color = True
            else:
                other.invert_color = False
            other.draw(screen, level)

        ### draw the player on the screen. This makes sure that the player is always on top of the others
        player.draw(screen, level)

        ### update the screen
        pygame.display.flip()

    else: ### game ended without quitting
        return True

    return False ### game ended by quitting

#-------------------------------------------------

def level1(
        gamewidth=levels.DEFAULT_GAMEWIDTH,
        gameheight=levels.DEFAULT_GAMEHEIGHT,
        characterradius=characters.DEFAULT_WIDTH,
    ):
    """the first level of the game!"""

    ### create the level
    level = levels.Level(width=gamewidth, height=gameheight, color=levels.DEFAULT_COLOR)

    ### create the main character
    player = characters.Character(
        'Player',
        0, ### start off in the center of the game
        0,
        radius=characterradius,
        color=characters.DEFAULT_COLOR,
    )

    ### create other characters
    others = []

    opponent = characters.Character(
        'Other',
        random_character_placement(gamewidth, 2*characterradius),
        random_character_placement(gameheight, 2*characterradius),
        radius=characterradius,
        color=random_color(),
    )
    others.append(opponent)

    ### enter the game loop
    loop(level, player, others)
