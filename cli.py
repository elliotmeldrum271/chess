#!/usr/bin/env python3
""" Main driver for a chess game."""

from chess import play
from players import HumanPlayer, RandomPlayer, MiniMax

players = {
    'h': HumanPlayer,
    'r': RandomPlayer,
    'm': MiniMax
}


def main():
    """ Run a game of chess."""

    print_visuals = True
    #  print_visuals = False

    try:
        p_0 = p_1 = None
        #  p_0, p_1 = MiniMax, MiniMax

        while not p_0:
            p_0_input = input("Select the white player. Enter 'h' to play as a " \
                              + "human, 'r' to have random moves be played, or 'm' to have the computer use a minimax strategy..\n")
            p_0 = players.get(p_0_input, None)
        while not p_1:
            p_1_input = input("Select the white player. Enter 'h' to play as a " \
                              + "human, 'r' to have random moves be played, or 'm' to have the computer use a minimax strategy..\n")
            p_1 = players.get(p_1_input, None)


        if HumanPlayer in [p_0, p_1]:
            print_visuals = True


        if p_0 is RandomPlayer:
            p_0 = p_0(print_visuals)
        elif p_0 is MiniMax:
            p_0 = p_0(0, print_visuals)
        else:
            p_0 = p_0()

        if p_1 is RandomPlayer:
            p_1 = p_1(print_visuals)
        elif p_1 is MiniMax:
            p_1 = p_1(0, print_visuals)
        else:
            p_1 = p_1()


        result = play(p_0, p_1, print_visuals=print_visuals)

        if not print_visuals:
            print('Winner: ', result)
    except KeyboardInterrupt:
        print('\nAborting Game')


if __name__ == "__main__":
    main()
