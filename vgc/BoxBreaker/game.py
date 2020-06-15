"""utility functions for BoxBreaker"""

__author__ = "Reed Essick (reed.essick@gmail.com)"

#-------------------------------------------------

import random
import pygame

from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, KEYDOWN, KEYUP, K_ESCAPE, QUIT)

### non-standard libraries
from . import characters
from . import levels

#-------------------------------------------------

def random_character_placement(gamesize, charactersize):
    return (random.random() - 0.5)*(gamesize - charactersize)

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

#-------------------------------------------------

def main(fps=30, max_opponents=1000, **kwargs):
    """Launch the game and enter the main loop!"""

    print('Welcome to BoxBreaker!')
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick(fps)

    total_score = 0
    number_of_opponents = 1
    opponent_respawn_time = 5000
    level = 1
    speed = 1
    while number_of_opponents < max_opponents:
        print('Entering Level %d'%level)

        score, running = game(player_speed=speed, number_of_opponents=number_of_opponents, opponent_respawn_time=opponent_respawn_time, **kwargs)
        total_score += score

        if running:
            level += 1
#            speed = max(5, speed+1)
            number_of_opponents *= 2
            if (level % 3) == 0:
                opponent_respawn_time = max(3*fps, opponent_respawn_time/2)

        else:
            break

    print('---> total score: %d <---'%total_score)
    print('Exiting BoxBreaker!')
    pygame.quit()

#------------------------

def loop(level, player, others, player_speed=1, respawn_time=1000):
    """execute the main loop that drives the game"""
    screen = pygame.display.set_mode([level.width, level.height]) ### set the screen to match the level
    screen.fill(level.color) ### fill in the background color for the level

    pressed = dict()
    running = True
    removed = []

    respawn = 1
    while running and len(others):
        for event in pygame.event.get():
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

        ### add back opponents if the timed out
        if (respawn % respawn_time) == 0:
            if removed:
                others.append(removed.pop(0))
        respawn += 1

        ### draw the others on the screen
        for i in range(len(others)):
            other = others.pop(0)
            if characters.intersects(player, other):
                other.invert_color = True
                if pressed.get(K_SPACE, False):
                    removed.append(other)
                else:
                    others.append(other)
            else:
                other.invert_color = False
                others.append(other)

        ### make the background the level's color
        screen.fill(level.color)
        
        ### now draw the others to the screen
        for other in others:
            other.draw(screen, level)

        ### draw the player on the screen. This makes sure that the player is always on top of the others
        player.draw(screen, level)

        ### update the screen
        pygame.display.flip()

    return len(removed) - respawn//respawn_time, running ### if we are still running (have not quit), we need to convey that

#-------------------------------------------------

def game(
        player_speed=1,
        number_of_opponents=1,
        opponent_respawn_time=1000,
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
    return loop(level, player, others, respawn_time=opponent_respawn_time, player_speed=player_speed)
