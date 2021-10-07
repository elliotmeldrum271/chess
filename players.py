#!/usr/bin/env python3
""" Some players.
TODO:
    -implement an Alpha-Beta algorithm to play chess
        -implement a simple position evaluation function
        -implement an RL based evaluation function
"""

from chess import Location


class HumanPlayer:
    """ A class that takes human input to make moves."""
    @classmethod
    def move(cls, _):
        """ Get user input and return a move."""
        origin = Location("-")
        target = Location("-")
        while not origin.in_bounds:
            try:
                origin = Location(
                    input(
                        "Enter a location to move from in algebraic notation (e.g. e7)\n"
                    ))
            except ValueError:
                pass
        while not target.in_bounds:
            try:
                target = Location(
                    input(
                        "Enter a location to move to in algebraic notation (e.g. e5)\n"
                    ))
            except ValueError:
                pass
        return (origin, target)
