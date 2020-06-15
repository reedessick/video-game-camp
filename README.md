# video-game-camp

Welcome to Video-Game Summer Camp (2020)!

During this camp, you will learn the basics of video game design, including how to come up with creative ideas for new games, how to design computer programs to represent those ideas, and how to make the computer run your game.
This should be accessible to anyone, even those with no prior programing experience.

This repository is meant to contain the basic infrastructure that can be used to make many different games.
You can either copy this repository many times to create more than one game, or you can create multiple games in this repository.
We will show you how to organize your code to make this easy and so that you can continue to develop your games as much or as little as you like at any point in the future (even after camp is over!).

## Playing Games

To begin playing games, make sure you have installed the code and then run
```
python -m vgc
```
This will provide you with an interactive menu of all games currently known to the video-game-camp source code (`vgc`).
Type in the name of the game you'd like to play, and `vgc` will launch that game for you automatically.

If you know the name of the game you want to play already (for example, `BoxBreaker`), you can launch that game directly with
```
python -m vgc.BoxBreaker
```

Throughout this week-long camp, campers will learn how to develop a new game within the `vgc`/`pygame` architecture.
When camp finishes, they can define more games and build the arcade of their dreams!

## Schedule

During the 5 day camp, you will design a video game and program a computer to let you play it.
This starts from the very basics of how to make your characters interact within the game on Day 1, to more advanced ideas like how to keep score, how to make your game unpredictable and exciting, and how to add new features later by the end of Day 4.
Day 5 will be a tournament with your friends and family in which you can show off your new game!

### [Day 1](day1/README.md)

*Design*: Brainstorm the basic aspects of your game!

*Code*: Learn how to play a `vgc` game and the basics of bounding boxes!

*Test*: Begin building your own game! Brainstorm more features while exploring bounding box behavior!

### Day 2

*Design*: Create images for your characters!

*Code*: Create your characters!

*Test*: Make your characters interact within your game!

### Day 3

*Design*: Create custom levels!

*Code*: ...

*Test*: ...

### Day 4

*Design*: Make a user-guide that explains how to play your game!

*Code*: ...

*Test*: ...

### Day 5

*TOURNAMENT*: Get your friends and family to try your game!

## Installation

This library relies upon pygame. On linux systems, this is simple to install with
```
sudo apt-get install python-pygame
```
This will discover and install the version of pygame consistent with your default Python interpreter. Mine happens to be Python2.7; yours is likely to be Python3.7 or higher.

Once that is installed, simply install this library from source via
```
python setup.py install --prefix /path/to/install
```
and then you can launch your arcade via
```
python -m vgc
```

## Contact

You can contact Reed with questions at `reed.essick@gmail.com`.
Please feel free to build upon this simple camp with your friends and family!

