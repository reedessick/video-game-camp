"""main library for the game. We define everything in here so that campers don't have to remember which file is which"""
__author__ = "Reed Essick (reed.essick@gmail.com)"

#-------------------------------------------------

import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, KEYDOWN, KEYUP, K_ESCAPE, QUIT)

### non-standard libraries
from vgc import utils

#-------------------------------------------------

DEFAULT_VIEWWIDTH = 800
DEFAULT_VIEWHEIGHT = 800

DEFAULT_GAMEWIDTH = 2*DEFAULT_VIEWWIDTH
DEFAULT_GAMEHEIGHT = 2*DEFAULT_VIEWHEIGHT

#-------------------------------------------------

### DEFINE CHARACTERS, which we alwasys draw to the screen
class Player(utils.BoundingBox):
    name = 'Player'

    def __init__(self, speed=1, width=utils.DEFAULT_WIDTH, height=utils.DEFAULT_HEIGHT, color=utils.DEFAULT_COLOR):
        self._speed = speed
        utils.BoundingBox.__init__(self, 0, 0, width=width, height=height, color=color)

    @property
    def speed(self):
        return self._speed

    def draw(self, screen, view):
        raise NotImplementedError

#------------------------

class Dinosaur(Player):
    name = 'Dinosaur'

    def draw(self, screen, view):
        pygame.draw.ellipse(screen, self.color, (self.left - view.left, self.bottom - view.bottom, self.width, self.height), 2)

class Airplane(Player):
    name = 'Airplane'

    def draw(self, screen, view):      
        points = [
            (self.left - view.left, self.top - view.bottom),
            (self.right - view.left, self.top - view.bottom),
            (self.x_center - view.left, self.bottom - view.bottom),
        ]
        pygame.draw.polygon(screen, self.color, points, 2)

#------------------------

KNOWN_CHARACTERS = {
    Dinosaur.name : Dinosaur,
    Airplane.name : Airplane,
}

#-------------------------------------------------

### DEFINE OBSTACLES, which we only draw to the screen if they are within the scrren's field of view

class Obstacle(utils.BoundingBox):

    def __init__(self, width=utils.DEFAULT_WIDTH, height=utils.DEFAULT_HEIGHT, color=utils.RANDOM_COLOR):
        utils.BoundingBox.__init__(
           self,
           0,
           0,
           width=width,
           height=height,
           color=color,
        )

    def place(self, game):
        self._x = utils.random_character_placement(game.width, self.width)
        self._y = utils.random_character_placement(game.height, self.height)

    def draw(self, screen, view):
        if self.intersects(view):
            pygame.draw.rect(screen, self.color, (self.left - view.left, self.bottom - view.bottom, self.width, self.height))

class FinishLine(Obstacle):

    def __init__(self, width=2*utils.DEFAULT_WIDTH, height=2*utils.DEFAULT_HEIGHT):
        Obstacle.__init__(self, width=width, height=height, color=(0, 0, 0))

    def is_found(self, player):
       return utils.is_between(player.left, self.x_center, player.right) and utils.is_between(player.bottom, self.y_center, player.top)

    def draw(self, screen, view):
#        if self.intersects(view):
            pygame.draw.rect(screen, self.color, (self.left - view.left, self.bottom - view.bottom, self.width, self.height), 2)
            pygame.draw.rect(screen, self.color, (self.left + self.width*1/8 - view.left, self.bottom + self.height*1/8 - view.bottom, self.width*3/4, self.height*3/4), 2)
            pygame.draw.rect(screen, self.color, (self.left + self.width*1/4 - view.left, self.bottom + self.height*1/4 - view.bottom, self.width/2, self.height/2), 2)
            pygame.draw.rect(screen, self.color, (self.left + self.width*3/8 - view.left, self.bottom + self.height*3/8 - view.bottom, self.width/4, self.height/4), 2)

#------------------------

class Level(object):

    background_characters = []

    def __init__(
            self,
            obstacles_per_view=10.,
            viewwidth=DEFAULT_VIEWWIDTH,
            viewheight=DEFAULT_VIEWHEIGHT,
            gamewidth=DEFAULT_GAMEWIDTH,
            gameheight=DEFAULT_GAMEHEIGHT,
            color=(255, 255, 255), ### white
        ):
        ### set up view and total game board
        self._view = utils.BoundingBox(0, 0, width=viewwidth, height=viewheight, color=color)
        self._game = utils.BoundingBox(0, 0, width=gamewidth, height=gameheight, color=None)

        ### add randomly places obstacles
        num_obstacles = int(obstacles_per_view * self.game.area / self.view.area)+1
        self._obstacles = [Obstacle() for i in range(num_obstacles)]
        for obstacle in self._obstacles:
            obstacle.place(self.game)

        ### add radomly placed finish line
        self._finishline = FinishLine()
        self._finishline.place(self.game)

    @property
    def view(self):
        return self._view

    @property
    def game(self):
        return self._game

    @property
    def obstacles(self):
        return self._obstacles

    @property
    def finishline(self):
        return self._finishline

    def animate(self):
        for background_character in self.background_characters:
            pass ### move these around the game

    def draw(self, screen):
        for background_character in self.background_characters:
            background_character.draw(screen, self.view)

        for obstacle in self.obstacles:
            obstacle.draw(screen, self.view)
        self.finishline.draw(screen, self.view)

class Level1(Level):
    name = "Sacramento, CA"

    def __init__(self):
        Level.__init__(
            self,
            obstacles_per_view=10.,
            color=(255, 255, 200), ### blue
        )

class Level2(Level):
    name = "Under Water"

    def __init__(self):
        Level.__init__(
            self,
            obstacles_per_view=10.,
            color=(0, 0, 50), ### blue
        )
        
class Level3(Level):
    name = "Chicago, IL"

    def __init__(self):
        Level.__init__(
            self,
            obstacles_per_view=10.,
            color=(100, 100, 100), ### grey
        )

#------------------------

KNOWN_LEVELS = {
    Level1.name : Level1,
    Level2.name : Level2,
    Level3.name : Level3,
}

#-------------------------------------------------

def main(fps=30):

    print('Welcome to Dinosaurs vs Airplanes!')

    # select the character
    if len(KNOWN_CHARACTERS) == 1:
        player = KNOWN_CHARACTERS.keys()[0]

    else:
        print('Choose your character:')
        print('\n'.join(' -- '+key for key in KNOWN_CHARACTERS.keys()))
        player = raw_input('')
        while player not in KNOWN_CHARACTERS:
            print('I did not understand. Please pick one of:')
            print('\n'.join(' -- '+key for key in KNOWN_CHARACTERS.keys()))
            player = raw_input('')

    player = KNOWN_CHARACTERS[player]()

    # select level
    if len(KNOWN_LEVELS) == 1:
        level = KNOWN_LEVELS.keys()[0]

    else:
        print('Choose your level:')
        print('\n'.join(' -- '+key for key in KNOWN_LEVELS.keys()))
        level = raw_input('')
        while level not in KNOWN_LEVELS:
            print('I did not understand. Please pick one of:')
            print('\n'.join(' -- '+key for key in KNOWN_LEVELS.keys()))
            level = raw_input('')

    # there is only a single level at the moment, so we just instantiate that
    level = KNOWN_LEVELS[level]()

    # init game
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick(fps)

    # enter main game loop
    screen = pygame.display.set_mode([level.view.width, level.view.height])
    loop(screen, level, player)

    # exit game
    print('Exiting Dinosaurs vs Airplanes!')
    pygame.quit()

#------------------------

def loop(screen, level, player):

    ### enter the main game loop
    running = True
    pressed = dict()
    while running:
        for event in pygame.event.get():
            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE): ### clicked the close button or pressed escape
                running = False

            elif event.type == KEYDOWN:
                pressed[event.key] = True

            elif event.type == KEYUP:
                pressed[event.key] = False

        for key in [key for key, is_pressed in pressed.items() if is_pressed]:
            if key == K_DOWN:
                player.move_up(player.speed, max_y=level.game.top)
                level.view.move_up(player.speed, max_y=level.game.top)

            elif key == K_UP:
                player.move_down(player.speed, min_y=level.game.bottom)
                level.view.move_down(player.speed, min_y=level.game.bottom)

            elif key == K_LEFT:
                player.move_left(player.speed, min_x=level.game.left)
                level.view.move_left(player.speed, min_x=level.game.left)

            elif key == K_RIGHT:
                player.move_right(player.speed, max_x=level.game.right)
                level.view.move_right(player.speed, max_x=level.game.right)

        ### FIXME: put in logic to make the game do things!

        # make background characters move
        level.animate()

        # condition to exit the game
        if level.finishline.is_found(player):
            running = False

        ### fill in the background color for the screen
        screen.fill(level.view.color)

        level.draw(screen)
        player.draw(screen, level.view)

        ### update the screen
        pygame.display.flip()

