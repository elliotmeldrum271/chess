#!/usr/bin/env python3
""" Some players.
TODO:
    -implement an Alpha-Beta algorithm to play chess
        -implement a simple position evaluation function
        -implement an RL based evaluation function
"""

import random
from chess import Location
from typing import Tuple


class HumanPlayer:
    """ A class that takes human input to make moves."""
    @classmethod
    def move(cls, _) -> Tuple[Location]:
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



class RandomPlayer:
    """ A class that makes a random legal move."""
    @classmethod
    def move(cls, board) -> Tuple[Location]:
        """ Return a random move."""
        pieces = board.color_pieces_flat(board.who)
        moves = []
        for piece in pieces:
            moves.extend([(piece.location, target) for target in
                          piece.all_legal_moves])
        move = random.choice(moves)
        print(move[0].algebraic, move[1].algebraic)
        #  input()
        return move
