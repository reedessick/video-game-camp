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

def main(fps=30, **kwargs):
    """Launch the game and enter the main loop!"""

    LEVELS = [
        ('Level 1', game, 2),
        ('Level 2', game, 5),
        ('Level 3', game, 10),
    ]

    print('Welcome to BoxBreaker!')
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick(fps)

    for level_name, level, number_of_opponents in LEVELS:
        print('Entering '+level_name)
        if not level(number_of_opponents=number_of_opponents, **kwargs): ### we quit out of the level, so we should exit the game
            break

    print('Exiting BoxBreaker!')
    pygame.quit()

#------------------------

def loop(level, player, others, player_speed=1):
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

def game(
        number_of_opponents=1,
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

    for i in range(number_of_opponents):
        opponent = characters.Character(
            'Opponent %d'%(i+1),
            random_character_placement(gamewidth, 2*characterradius),
            random_character_placement(gameheight, 2*characterradius),
            radius=characterradius,
            color=random_color(),
        )
        others.append(opponent)

    ### enter the game loop
    loop(level, player, others)
