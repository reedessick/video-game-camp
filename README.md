# video-game-camp

A repository in which we store video games produced and camp materials from the summer of 2020.
During this camp, you will learn the basics of video game design, including how to come up with creative ideas for new games, how to design computer programs to represent those ideas, and how to make the computer run your game.
This should be accessible to anyone, even those with no prior programing experience.

## Schedule

During the 5 day camp, you will design a video game and program a computer to let you play it.
This starts from the very basics of how to make your characters interact within the game on Day 1, to more advanced ideas like how to keep score, how to make your game unpredictable and exciting, and how to add new features later by the end of Day 4.
Day 5 will be a tournament with your friends and family in which you can show off your new game!

### Day 1

*Design*

Write down the following in your notebook
  * Your game's title
  * What players will do within the game
    * What is the goal? How do you get points?
    * Is there a story to go along with your game?
    * What makes the game challenging?
  * At least 3 characters (including what they look like and any special powers they have)
  * At least 3 levels (what you have to do in each)

*Code*
  * Learn how to start the game
  * Learn how to edit the game's source code
  * Write function to determine whether bounding boxes overlap

*Test*

  * Play the game with and without the bounding-box overlap function defined.
  * Can you think how you would change the game to make actions occur when bounding boxes overlap?

### Day 2

*Design*

Find images online (or draw your own!) for the different characters and levels you described on Day 1.

*Code*

  * Create your characters!
    * Define objects to represent your characters and their special powers. These should extend the BoundingBox class.
    * See if you can make the characters look like you designed them by including the pictures you drew!

*Test*

  * Building on the basic game from Day 1, add multiple characters to your game and see if you can make them do things when their bounding-boxes overlap.
  * Can you change which character you control?
  * Can you make multiple characters move at the same time?

### Day 3

*Design*

Find images online (or draw your own!) for the levels. These could be backgrounds or specific items that you have to interact with in each level.

*Code*

*Test*

### Day 4

*Design*

Make a user-guide that explains how to play your game!

*Code*

*Test*

### Day 5

*TOURNAMENT*

Get your friends and family to try your game!
    * Show them your user-guide
    * Demonstrate how to play the game and what you have learned
    * See who can get the highest score

## Installation

This library relies upon pygame. On linux systems, this is simple to install with
```
sudo apt-get install python-pygame
```
This will discover and install the version of pygame consistent with your default Python interpreter. Mine happens to be Python2.7; yours is likely to be Python3.7 or higher.
