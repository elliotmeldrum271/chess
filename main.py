#!/usr/bin/env python3
""" Main driver for a chess game."""

from chess import play
from players import HumanPlayer


def main():
    """ Run a game of chess."""
    p_0 = HumanPlayer()
    p_1 = HumanPlayer()
    play(p_0, p_1)


if __name__ == "__main__":
    main()
