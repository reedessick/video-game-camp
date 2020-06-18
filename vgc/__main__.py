"""a basic menu from which users can navigate to different games they have designed.
"""

__author__ = 'Reed Essick (reed.essick@gmail.com)'

#-------------------------------------------------

import sys
import inspect

### non-standard libraries
import vgc

#-------------------------------------------------

def print_available_games(games):
    for game in games.keys():
        print(' -- '+game)

def select_game(games):
    """interact with the command line to select a game"""

    Ngames = len(games)
    if Ngames == 0: ### no games available
        print('I\'m sorry, but there are no games currently available. Please design a game soon so we can get playing!')
        sys.exit(0)

    elif Ngames==1:
        print('There is only a single game available!')
        return games.items()[0]

    else:
        print('Please tell me which of the following games you would like to play!')
        print_available_games(games)
        selected = raw_input('')

        while selected not in games: ### make sure the specified game is available
            print('I\'m sorry, but I did not understand. Please specify one of the following, or specify "exit" to quit')
            print_available_games(games)
            selected = raw_input('')

            if selected == 'exit': ### quit
                sys.exit(0)

        return selected, games[selected]

#------------------------

def main():
    """the basic function that will be run when this module is called as an executable. This should discover the available games and prompt the user to select which game they would like to play. It should then launch that game.
Note, users should also be able to launch individual games directly by calling the associated modules that live within vgc."""

    name, game = select_game(vgc.KNOWN_GAMES)
    print('---- Launching: %s -----'%name)
    game.game.main()
    sys.exit(0)

#-------------------------------------------------

main()
