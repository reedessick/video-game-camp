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

### [Day 1](day1/)

*Design*: Brainstorm the basic aspects of your game!

*Code*: Learn how to play a `vgc` game and the basics of bounding boxes!

*Test*: Begin building your own game! Brainstorm more features while exploring bounding box behavior!

### [Day 2](day2/)

*Design*: Create images for your characters!

*Code*: Create your characters!

*Test*: Make your characters interact within your game!

### [Day 3](day3/)

*Design*: Create custom levels!

*Code*: Allow your characters to score points and advance to higher levels!

*Test*: See if you can get your characters to progress through all 3 levels!

### [Day 4](day4/)

*Design*: Make a user-guide that explains how to play your game!

*Code*: ...

*Test*: ...

### [Day 5](day5/)

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
Make sure you remember to update your environment to point to your new installation within your `$PYTHONPATH`.
You can then launch your arcade via
```
python -m vgc
```

## Architecture

The video-game-camp (`vgc`) library is structured as a collection of Python modules.
The basic `vgc` module registers which games are available and provides a simple menu for users to navigate to the games they want to play.
In order for new games to become available, users will have to import them within `~/vgc/__init__.py` (see the example for how to import `BoxBreaker`).

Users should define their new games as submodules within `~/vgc~`; remember to include `__init__.py` and `__main__.py` modules.
Importantly, users should define a `utils.py` within their game, and there must be a `main()` function defined within `utils.py`.
This `utils.main()` should be imported an called within `__main__.py` so that users can directly launch this game from the command line without navigating the `vgc` menu.
However, we also need the `main()` function to be defined within `utils` so that the menu within `vgc` can launch games in a standard way.

Beyond that, developers can add whatever material they like within their game's subdirectory, including defining other modules to support gameplay.
`BoxBreaker` provides a very basic example of how this can be done.

## Contact

You can contact Reed with questions at `reed.essick@gmail.com`.
Please feel free to build upon this simple camp with your friends and family!

