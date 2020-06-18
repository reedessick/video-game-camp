"""main library for the game. We define everything in here so that campers don't have to remember which file is which"""
__author__ = "Reed Essick (reed.essick@gmail.com)"

#-------------------------------------------------

import os
import random

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

    def __init__(self, speed=1, width=utils.DEFAULT_WIDTH, height=utils.DEFAULT_HEIGHT, color=utils.RANDOM_COLOR):
        utils.BoundingBox.__init__(self, 0, 0, width=width, height=height, color=color)
        self._speed = speed
        self._x_velocity = 0
        self._y_velocity = 0

    @property
    def speed(self):
        return self._speed

    def _randomize_velocity(self):
        self._x_velocity = random.randint(-1, +1)*self.speed
        self._y_velocity = random.randint(-1, +1)*self.speed

    def walk(self, min_x=-DEFAULT_GAMEWIDTH, max_x=+DEFAULT_GAMEWIDTH, min_y=-DEFAULT_GAMEHEIGHT, max_y=+DEFAULT_GAMEHEIGHT):
        r = random.random()
        if r < 0.01: ### change x_velocity
            self._randomize_velocity()
        else:
            pass
        self.move(min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)

    def move(self, min_x=-DEFAULT_GAMEWIDTH, max_x=+DEFAULT_GAMEWIDTH, min_y=-DEFAULT_GAMEHEIGHT, max_y=+DEFAULT_GAMEHEIGHT):
        if self._x_velocity == 0:
            pass
        elif self._x_velocity > 0:
            self.move_right(self._x_velocity, max_x=max_x)
        else:
            self.move_left(-self._x_velocity, min_x=min_x)

        if self._y_velocity == 0:
            pass
        elif self._y_velocity > 0:
            self.move_up(self._y_velocity, max_y=max_y)
        else:
            self.move_down(-self._y_velocity, min_y=min_y)

    def draw(self, screen, view):
        raise NotImplementedError

#------------------------

class Dinosaur(Player):
    name = 'Dinosaur'

    def __init__(self, *args, **kwargs):
        kwargs['color'] = (0, 0, 0)
        Player.__init__(self, *args, **kwargs)

    def draw(self, screen, view):
        
        pygame.draw.ellipse(screen, self.color, (self.left - view.left, self.bottom - view.bottom, self.width/3, self.height/4))
        pygame.draw.line(screen, self.color, (self.left + self.width/8 - view.left, self.bottom - view.bottom), (self.left + self.width/3 - view.left, self.y_center-view.bottom), 4)
        pygame.draw.ellipse(screen, self.color, (self.x_center - self.width/3 - view.left, self.y_center - self.height/8 - view.bottom, self.width*2/3, self.height/4))
        pygame.draw.rect(screen, self.color, (self.x_center - self.width/4 - view.left, self.y_center - view.bottom, self.width/8, self.height/2))
        pygame.draw.rect(screen, self.color, (self.x_center + self.width/8 - view.left, self.y_center - view.bottom, self.width/8, self.height/2))
        pygame.draw.line(screen, self.color, (self.right - self.width/3 - view.left, self.y_center - view.bottom), (self.right - view.left, self.top - self.height/8 - view.bottom), 4)

class Airplane(Player):
    name = 'Airplane'

    def __init__(self, *args, **kwargs):
        kwargs['color'] = (0, 0, 0)
        Player.__init__(self, *args, **kwargs)

    def draw(self, screen, view):      
        points = [
            (self.left - view.left, self.top - self.height/4 - view.bottom),
            (self.right - view.left, self.top - self.height/4 - view.bottom),
            (self.x_center - view.left, self.bottom + self.height/4 - view.bottom),
        ]
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.ellipse(screen, self.color, (self.x_center - self.width/8 - view.left, self.bottom - view.bottom, self.width/4, self.height))

class Enemy(Player):
    name = 'Enemy'

    def draw(self, screen, view):
        pygame.draw.ellipse(screen, self.color, (self.left - view.left, self.bottom +self.height/4 - view.bottom, self.width, self.height/2), 2)
        pygame.draw.ellipse(screen, self.color, (self.left + self.width/4 - view.left, self.bottom - view.bottom, self.width/2, self.height), 2)

#------------------------

KNOWN_CHARACTERS = {
    Dinosaur.name : Dinosaur,
    Airplane.name : Airplane,
#    Enemy.name : Enemy,
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
        self._target = utils.BoundingBox(0, 0, width=width/2, height=height/2, color=color)
        self.invert = False

    @property
    def target(self):
        return self._target

    def place(self, game):
        self._x = self._target._x = utils.random_character_placement(game.width, self.width)
        self._y = self._target._y = utils.random_character_placement(game.height, self.height)

    def draw(self, screen, view):
        if self.intersects(view):
            r, g, b = self.color
            if self.invert:
                r = 255 - r
                g = 255 - g
                b = 255 - b
            pygame.draw.rect(screen, (r, g, b), (self.left - view.left, self.bottom - view.bottom, self.width, self.height), 2)
            pygame.draw.rect(screen, (r, g, b), (self.target.left - view.left, self.target.bottom - view.bottom, self.target.width, self.target.height))

    def bounce(self, other):
        if abs(other.x_center - self.x_center) > abs(other.y_center - self.y_center): ### move to the side
            if other.x_center > self.x_center: ### move to the right
                other._x = self.right + other.width/2
            else:
                other._x = self.left - other.width/2
        else: ### move up and down
            if other.y_center > self.y_center:
                other._y = self.top + other.height/2
            else:
                other._y = self.bottom - other.height/2

class Portal(Obstacle):

    def __init__(self, width=utils.DEFAULT_WIDTH, height=utils.DEFAULT_HEIGHT):
        Obstacle.__init__(self, width=width, height=height, color=(150, 0, 150))

    @staticmethod
    def transport(box, level):
        box._x = utils.random_character_placement(level.game.width, box.width)
        box._y = utils.random_character_placement(level.game.height, box.height)

    def draw(self, screen, view):
        if self.intersects(view):
            pygame.draw.ellipse(screen, self.color, (self.left - self.width/2- view.left, self.bottom - self.height/2 - view.bottom, 2*self.width, 2*self.height), 2)
            pygame.draw.ellipse(screen, self.color, (self.left - self.width/4 - view.left, self.bottom - self.height/4 - view.bottom, self.width*3/2, self.height*3/2), 2)
            pygame.draw.ellipse(screen, self.color, (self.left - view.left, self.bottom - view.bottom, self.width, self.height), 2)
            pygame.draw.ellipse(screen, self.color, (self.target.left - view.left, self.target.bottom - view.bottom, self.target.width, self.target.height))

class FinishLine(Obstacle):

    def __init__(self, width=utils.DEFAULT_WIDTH, height=utils.DEFAULT_HEIGHT):
        Obstacle.__init__(self, width=width, height=height, color=(0, 0, 0))

    def draw(self, screen, view):
        if self.intersects(view):
            pygame.draw.rect(screen, self.color, (self.left - self.width/2- view.left, self.bottom - self.height/2 - view.bottom, 2*self.width, 2*self.height), 2)
            pygame.draw.rect(screen, self.color, (self.left - self.width/4 - view.left, self.bottom - self.height/4 - view.bottom, self.width*3/2, self.height*3/2), 2)
            pygame.draw.rect(screen, self.color, (self.left - view.left, self.bottom - view.bottom, self.width, self.height), 2)
            pygame.draw.rect(screen, self.color, (self.target.left - view.left, self.target.bottom - view.bottom, self.target.width, self.target.height))

#------------------------

class Level(object):

    background_characters = []

    def __init__(
            self,
            obstacles_per_view=10.,
            portals_per_view=1.,
            num_enemies=0,
            viewwidth=DEFAULT_VIEWWIDTH,
            viewheight=DEFAULT_VIEWHEIGHT,
            gamewidth=DEFAULT_GAMEWIDTH,
            gameheight=DEFAULT_GAMEHEIGHT,
            color=(255, 255, 255), ### white
        ):
        ### set up view and total game board
        self._view = utils.BoundingBox(0, 0, width=viewwidth, height=viewheight, color=color)
        self._game = utils.BoundingBox(0, 0, width=gamewidth, height=gameheight, color=None)

        ### add randomly placed obstacles
        num_obstacles = int(obstacles_per_view * self.game.area / self.view.area) + 1
        self._obstacles = [Obstacle() for i in range(num_obstacles)]
        for obstacle in self._obstacles:
            obstacle.place(self.game)

        ### add randomly placed portals
        num_portals = int(portals_per_view * self.game.area / self.view.area) + 1
        self._portals = [Portal() for i in range(num_portals)]
        for portal in self._portals:
            portal.place(self.game)

        ### add enemies
        self._enemies = [Enemy() for i in range(int(num_enemies))]

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
    def portals(self):
        return self._portals

    @property
    def enemies(self):
        return self._enemies

    @property
    def finishline(self):
        return self._finishline

    def animate(self):
        for enemy in self.enemies:
            enemy.walk(min_x=self.game.left, max_x=self.game.right, min_y=self.game.bottom, max_y=self.game.top)

        for background_character in self.background_characters:
            pass ### move these around the game

    def draw(self, screen):
        for background_character in self.background_characters:
            background_character.draw(screen, self.view)

        for obstacle in self.obstacles:
            obstacle.draw(screen, self.view)

        for portal in self.portals:
            portal.draw(screen, self.view)

        for enemy in self.enemies:
            enemy.draw(screen, self.view)

        self.finishline.draw(screen, self.view)

class Level0(Level):
    name = "Training"
    win_points = 0
    lose_points = 0

class Level1(Level):
    name = "Sacramento, CA"
    win_points = 10
    lose_points = 5

    def __init__(self):
        Level.__init__(
            self,
            obstacles_per_view=10.,
            portals_per_view=1.,
            num_enemies=1.,
            color=(0, 0, 200), ### blue
        )

class Level2(Level):
    name = "Under Water"
    win_points = 10
    lose_points = 15

    def __init__(self):
        Level.__init__(
            self,
            obstacles_per_view=20.,
            portals_per_view=2.,
            num_enemies=5.,
            color=(0, 0, 150), ### blue
        )
        
class Level3(Level):
    name = "Chicago, IL"
    win_points = 15
    lose_points = 10

    def __init__(self):
        Level.__init__(
            self,
            obstacles_per_view=30.,
            portals_per_view=3.,
            num_enemies=10.,
            color=(100, 100, 100), ### grey
        )

#------------------------

KNOWN_LEVELS = {
    Level0.name : Level0,
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

    ### figure out how many points you have
    if os.path.exists('.points'):
        with open('.points', 'r') as points_file:
            points = int(points_file.read())
    else:
        points = 200

    print('You are starting with %d points'%points)

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

        down = pressed.get(K_DOWN, False)
        up = pressed.get(K_UP, False)
        left = pressed.get(K_LEFT, False)
        right = pressed.get(K_RIGHT, False)

        if down and (not up):
            player._y_velocity = +player.speed
        elif up and (not down):
            player._y_velocity = -player.speed
        else:
            player._y_velocity = 0

        if left and (not right):
            player._x_velocity = -player.speed
        elif right and (not left):
            player._x_velocity = +player.speed
        else:
            player._x_velocity = 0

        # make background characters move
        level.animate()

        # move the player
        player.move(min_x=level.game.left, max_x=level.game.right, min_y=level.game.bottom, max_y=level.game.top)

        # condition for portals
        for enemy in level.enemies:
            for portal in level.portals:
                if portal.target.intersects(enemy):
                    portal.transport(enemy, level)
                    break

        for portal in level.portals:
            if portal.target.intersects(player): ### randomly scatter the player
                portal.transport(player, level)
                break

        # obstacles change color when you run over them
        for enemy in level.enemies:
            for obstacle in level.obstacles:
                if obstacle.target.intersects(enemy):
                    obstacle.bounce(enemy) 
                    break
        
        for obstacle in level.obstacles:
            obstacle.invert = obstacle.intersects(player)
            if obstacle.target.intersects(player):
                obstacle.bounce(player)
                break

        # condition to exit the game
        if level.finishline.target.intersects(player):
            print('You crossed the finish line! You gained %d points!'%level.win_points)
            running = False
            points += level.win_points

        for enemy in level.enemies:
            if level.finishline.target.intersects(enemy):
                print('An enemy crossed the finish line! You lost %d points!'%level.lose_points)
                running = False
                points -= level.lose_points

        ### fill in the background color for the screen
        screen.fill(level.view.color)

        level.view._x = player.x_center
        level.view._y = player.y_center

        level.draw(screen)
        player.draw(screen, level.view)

        ### update the screen
        pygame.display.flip()

    print('You finished with %d points'%points)
    with open('.points', 'w') as points_file:
        points_file.write('%d'%points)
