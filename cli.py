#!/usr/bin/env python3
""" Main driver for a chess game."""

from chess import play
from players import HumanPlayer, RandomPlayer


players = {'h': HumanPlayer, 'r': RandomPlayer}
def main():
    """ Run a game of chess."""
    try:
        p_0 = p_1 = None
        p_0 = p_1 = RandomPlayer

        while not p_0:
            p_0_input = input("Select the white player. Enter 'h' to play as a human, 'r' to have random moves be played.\n")
            p_0 = players.get(p_0_input, None)
        while not p_1:
            p_1_input = input("Select the white player. Enter 'h' to play as a human, 'r' to have random moves be played.\n")
            p_1 = players.get(p_1_input, None)

        play(p_0, p_1)
    except KeyboardInterrupt:
        print('\nAborting Game')


if __name__ == "__main__":
    main()
