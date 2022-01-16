#!/usr/bin/env python3
""" Some chess players.
TODO:
    -implement an Alpha-Beta algorithm to play chess
        -implement a simple position evaluation function
        -implement an RL based evaluation function
"""

import random
import numpy as np
from chess import Color, Location, Move, Board
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
                        "Enter a location to move from in algebraic notation (e.g. e2)\n"
                    ))
            except ValueError:
                pass
        while not target.in_bounds:
            try:
                target = Location(
                    input(
                        "Enter a location to move to in algebraic notation (e.g. e4)\n"
                    ))
            except ValueError:
                pass
        return Move(origin, target)


class RandomPlayer:
    """ A class that makes a random legal move."""
    def __init__(self, print_visuals=False):
        self.print_visuals = print_visuals

    def move(self, board: Board) -> Move:
        """ Return a random move."""
        pieces = board.color_pieces_flat(board.who)
        moves = []
        for piece in pieces:
            moves.extend(piece.all_legal_moves)
        move = random.choice(moves)
        if self.print_visuals:
            print(move.origin.algebraic, move.target.algebraic)
            #  input('Press return to continue.')
        return move


class MiniMax:
    """ A class that implements a mini-max search algorighm.
    Note, self.depth must be an even integer for the player to play correctly.
    """
    def __init__(self, depth=0, print_visuals=False):
        self.depth = depth
        self.color = None
        self.counter = 0
        self.print_visuals = print_visuals

    def move_helper(self, board, depth: int = None):
        """ Take in a board and a depth. Return the (board, score) tuple that
        contains the board with the most extreme score, either maximized or
        minimized depending on the depth paramater.
        """
        try:
            if board.has_winner:
                if board.checkmate(self.color):
                    return ('we lost', -10000)
                return ('we won', 10000)

            if depth is None:
                depth = self.depth
            fen = board.fen_str
            possible_boards = [(move, Board(fen))
                               for move in board.all_legal_moves]
            for move, board in possible_boards:
                board.make_move(move)

            if not possible_boards:
                return ('stalement', 0)

            if depth == 0:
                scored_boards = [(move, self.simple_evaluator(board))
                                 for move, board in possible_boards]
            else:
                scored_boards = [(move, self.move_helper(board, depth - 1)[1])
                                 for move, board in possible_boards]

            np.random.shuffle(scored_boards)
            #  if depth == self.depth:
            #      for b in scored_boards:
            #          print(b)

            if depth % 2 == self.depth % 2:
                return max(scored_boards, key=lambda ms: ms[1])
            else:
                return min(scored_boards, key=lambda ms: ms[1])
        except ValueError as e:
            print(scored_boards)
            print(board)
            raise e

    def move(self, board: Board) -> Move:
        self.color = board.who
        move, score = self.move_helper(board)
        if self.print_visuals:
            print(self.counter)
            print(move, score)
        self.counter = 0
        #  input(move)
        return move

    def simple_evaluator(self, board: Board):
        self.counter += 1
        piece_scores = {
            'r': 4,
            'n': 3,
            'b': 4,
            'q': 7,
            'k': 0,
            'p': 1,
        }
        #  if board.has_winner:
        #      if board.checkmate(self.color):
        #          return -10000
        #      return 10000

        fen = board.fen_str.split()[0]
        pieces = [e for e in list(fen) if e.lower().islower()]

        white_pieces = [piece for piece in pieces if piece.isupper()]
        black_pieces = [piece for piece in pieces if piece.islower()]

        white_score = sum(piece_scores[piece.lower()]
                          for piece in white_pieces)
        black_score = sum(piece_scores[piece] for piece in black_pieces)

        if self.color == Color.WHITE:
            return white_score - black_score
        else:
            return black_score - white_score
