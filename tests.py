#!/usr/bin/env python
"""
Test that Chess is behaving correctly.

TODO:
    - test end game conditions:
        - game should end in a tie if there is a stalemate
        - game should end if there is a checkmate
        - game should end properly with the 50 move draw rule
    - test that the halfmove clock and fullmove number are updated appropriately
    - test that fullmove and halmove counters are updated correctly
    - test that the game ends if either playter is in check mate
    - test that 'i' can not move into check
    - test that the game ends if the half move counter reaches 100
    - make sure to update castling rights after moving a king or a castle
    - test check more
    - test checkmate more
"""

from chess import *


def test():
    """
    Run some tests for Chess.py
    >>> b = Board()
    >>> print(b)
       a b c d e f g h
    1  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  _ _ _ _ _ _ _ _  4
    5  _ _ _ _ _ _ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  7
    8  ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.fen_str
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    >>> b.who.value
    0
    >>> b.en_passant_target.algebraic
    '-'
    >>> b.who.name
    'WHITE'
    >>> try:
    ...     b.make_move(Location(algebraic='b2'), Location(algebraic='b3'))
    ... except IllegalMoveError as e:
    ...     print(e)
    It is white\'s turn and white does not control the selected piece. Please select a valid piece to move.
    >>> try:
    ...     b.make_move(Location(algebraic='a4'), Location(algebraic='a5'))
    ... except IllegalMoveError as e:
    ...     print(e)
    Cannot make a move from an empty square. Please select a valid piece to move.
    >>> b.make_move(Location(algebraic='b8'), Location(algebraic='c6'))
    >>> print(b)
       a b c d e f g h
    1  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  _ _ _ _ _ _ _ _  4
    5  _ _ _ _ _ _ _ _  5
    6  _ _ ♘ _ _ _ _ _  6
    7  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  7
    8  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.make_move(Location(algebraic='a2'), Location(algebraic='a4'))
    >>> print(b)
       a b c d e f g h
    1  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ ♟ ♟ ♟ ♟ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  ♟ _ _ _ _ _ _ _  4
    5  _ _ _ _ _ _ _ _  5
    6  _ _ ♘ _ _ _ _ _  6
    7  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  7
    8  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.make_move(Location(algebraic='c6'), Location(algebraic='a5'))
    >>> print(b)
       a b c d e f g h
    1  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ ♟ ♟ ♟ ♟ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  ♟ _ _ _ _ _ _ _  4
    5  ♘ _ _ _ _ _ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  7
    8  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.make_move(Location(algebraic='b2'), Location(algebraic='b4'))
    >>> print(b)
       a b c d e f g h
    1  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ ♟ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  ♟ ♟ _ _ _ _ _ _  4
    5  ♘ _ _ _ _ _ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  7
    8  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> pawn = b.get_piece_at(Location(algebraic='b4'))
    >>> [move.algebraic for move in pawn.all_legal_moves]
    ['b5', 'a5']
    >>> kn = b.get_piece_at(Location(algebraic='a5'))
    >>> [move.algebraic for move in kn.all_legal_moves]
    ['c6', 'c4', 'b3']
    >>> try:
    ...     b.make_move(Location(algebraic='a5'), Location(algebraic='a6'))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal
    >>> try:
    ...     b.make_move(Location(algebraic='a5'), Location(algebraic='a42'))
    ... except IllegalMoveError as e:
    ...     print(e)
    Cannot move outside the boundaries of the board. Please select a different destination.
    >>> fen_str = b.fen_str
    >>> b2 = Board(fen_str)
    >>> print(b2)
       a b c d e f g h
    1  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ ♟ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  ♟ ♟ _ _ _ _ _ _  4
    5  ♘ _ _ _ _ _ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  7
    8  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> try:
    ...     b.make_move(Location(algebraic='b7'), Location(algebraic='b4'))
    ... except:
    ...     print('illegal move')
    illegal move
    >>> b.make_move(Location(algebraic='b7'), Location(algebraic='b5')); print(b)
       a b c d e f g h
    1  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ ♟ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  ♟ ♟ _ _ _ _ _ _  4
    5  ♘ ♙ _ _ _ _ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ _ ♙ ♙ ♙ ♙ ♙ ♙  7
    8  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> list(map(lambda t: t.algebraic, b.get_piece_at(Location(algebraic='c8')).all_legal_moves))
    ['b7', 'a6']
    >>> try:
    ...     b.make_move(Location(algebraic='b1'), Location(algebraic='b2'))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal
    >>> list(map(lambda t: t.algebraic, b.get_piece_at(Location(algebraic='c1')).all_legal_moves))
    ['b2', 'a3']
    >>> b.make_move(Location(algebraic='b1'), Location(algebraic='c3')); print(b)
       a b c d e f g h
    1  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ ♟ ♟ ♟ ♟  2
    3  _ _ ♞ _ _ _ _ _  3
    4  ♟ ♟ _ _ _ _ _ _  4
    5  ♘ ♙ _ _ _ _ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ _ ♙ ♙ ♙ ♙ ♙ ♙  7
    8  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.make_move(Location(algebraic='d7'), Location(algebraic='d5')); print(b)
       a b c d e f g h
    1  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ ♟ ♟ ♟ ♟  2
    3  _ _ ♞ _ _ _ _ _  3
    4  ♟ ♟ _ _ _ _ _ _  4
    5  ♘ ♙ _ ♙ _ _ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ _ ♙ _ ♙ ♙ ♙ ♙  7
    8  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.en_passant_target.algebraic
    'd6'
    >>> b.who = Color.WHITE
    >>> b.make_move(Location(algebraic='d5'), Location(algebraic='d4')); print(b)
       a b c d e f g h
    1  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ ♟ ♟ ♟ ♟  2
    3  _ _ ♞ _ _ _ _ _  3
    4  ♟ ♟ _ ♙ _ _ _ _  4
    5  ♘ ♙ _ _ _ _ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ _ ♙ _ ♙ ♙ ♙ ♙  7
    8  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.make_move(Location(algebraic='e2'), Location(algebraic='e4')); print(b)
       a b c d e f g h
    1  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ _ ♟ ♟ ♟  2
    3  _ _ ♞ _ _ _ _ _  3
    4  ♟ ♟ _ ♙ ♟ _ _ _  4
    5  ♘ ♙ _ _ _ _ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ _ ♙ _ ♙ ♙ ♙ ♙  7
    8  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.fen_str
    'r1bqkbnr/2pp1ppp/2n5/pp1Pp3/NP6/8/P1P1PPPP/R1BQKBNR w KQkq e3 0 5'
    >>> list(map(lambda t: t.algebraic, b.get_piece_at(Location(algebraic='d4')).all_legal_moves))
    ['d3', 'e3', 'c3']
    >>> try:
    ...     b.make_move(Location(algebraic='d4'), Location(algebraic='d4'))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal
    >>> try:
    ...     b.make_move(Location(algebraic='a5'), Location(algebraic='a5'))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal
    >>> try:
    ...     b.make_move(Location(algebraic='c8'), Location(algebraic='c8'))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal
    >>> list(map(lambda t: t.algebraic, b.get_piece_at(Location(algebraic='c8')).all_legal_moves))
    ['d7', 'e6', 'f5', 'g4', 'h3', 'b7', 'a6']
    >>> b.make_move(Location(algebraic='c8'), Location(algebraic='f5')); print(b)
       a b c d e f g h
    1  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ _ ♟ ♟ ♟  2
    3  _ _ ♞ _ _ _ _ _  3
    4  ♟ ♟ _ ♙ ♟ _ _ _  4
    5  ♘ ♙ _ _ _ ♗ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ _ ♙ _ ♙ ♙ ♙ ♙  7
    8  ♖ _ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> list(map(lambda t: t.algebraic, b.get_piece_at(Location(algebraic='f5')).all_legal_moves))
    ['g6', 'e6', 'd7', 'c8', 'g4', 'h3', 'e4']
    >>> b.who = Color.WHITE
    >>> b.make_move(Location(algebraic='f5'), Location(algebraic='e4')); print(b)
       a b c d e f g h
    1  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ _ ♟ ♟ ♟  2
    3  _ _ ♞ _ _ _ _ _  3
    4  ♟ ♟ _ ♙ ♗ _ _ _  4
    5  ♘ ♙ _ _ _ _ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ _ ♙ _ ♙ ♙ ♙ ♙  7
    8  ♖ _ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.castling_rights
    ['K', 'Q', 'k', 'q']
    >>> b.half_move_clock
    0
    >>> try:
    ...     b.make_move(Location(algebraic='b4'), Location(algebraic='b6'))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal
    >>> b.make_move(Location(algebraic='b4'), Location(algebraic='a5')); print(b)
       a b c d e f g h
    1  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ _ ♟ ♟ ♟  2
    3  _ _ ♞ _ _ _ _ _  3
    4  ♟ _ _ ♙ ♗ _ _ _  4
    5  ♟ ♙ _ _ _ _ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ _ ♙ _ ♙ ♙ ♙ ♙  7
    8  ♖ _ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> try:
    ...     b.make_move(Location(algebraic='b5'), Location(algebraic='b3'))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal
    >>> b.who = Color.WHITE
    >>> b.make_move(Location(algebraic='f7'), Location(algebraic='f5'))
    >>> b.en_passant_target.algebraic
    'f6'
    >>> try:
    ...     b.make_move(Location(algebraic='c3'), Location(algebraic='c4'))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal
    >>> b.make_move(Location(algebraic='c3'), Location(algebraic='e4')); print(b)
       a b c d e f g h
    1  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ _ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  ♟ _ _ ♙ ♞ _ _ _  4
    5  ♟ ♙ _ _ _ ♙ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ _ ♙ _ ♙ _ ♙ ♙  7
    8  ♖ _ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.en_passant_target.algebraic
    '-'
    >>> ##b.get_piece_at(Location(algebraic='a8')).all_legal_moves
    >>> list(map(lambda t: t.algebraic, b.get_piece_at(Location(algebraic='a8')).all_legal_moves))
    ['b8', 'c8']
    >>> b.make_move(Location(algebraic='a8'), Location(algebraic='b8'))
    >>> print(b)
       a b c d e f g h
    1  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ _ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  ♟ _ _ ♙ ♞ _ _ _  4
    5  ♟ ♙ _ _ _ ♙ _ _  5
    6  _ _ _ _ _ _ _ _  6
    7  ♙ _ ♙ _ ♙ _ ♙ ♙  7
    8  _ ♖ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> list(map(lambda t: t.algebraic, b.get_piece_at(Location(algebraic='b8')).all_legal_moves))
    ['b7', 'b6', 'a8', 'c8']
    >>> try:
    ...     b.make_move(Location(algebraic='b8'), Location(algebraic='b5'))
    ... except IllegalMoveError as e:
    ...     print('Illegal move was attempted')
    Illegal move was attempted
    >>> b.who = Color.WHITE
    >>> b.make_move(Location(algebraic='e7'), Location(algebraic='e6'))
    >>> print(b)
       a b c d e f g h
    1  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ _ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  ♟ _ _ ♙ ♞ _ _ _  4
    5  ♟ ♙ _ _ _ ♙ _ _  5
    6  _ _ _ _ ♙ _ _ _  6
    7  ♙ _ ♙ _ _ _ ♙ ♙  7
    8  _ ♖ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> ##b.get_piece_at(Location(algebraic='d8')).all_legal_moves
    >>> list(map(lambda t: t.algebraic, b.get_piece_at(Location(algebraic='d8')).all_legal_moves))
    ['d7', 'd6', 'd5', 'e7', 'f6', 'g5', 'h4', 'c8']
    >>> b.get_piece_at(Location(algebraic='d8')).color.value
    0
    >>> b.get_piece_at(Location(algebraic='d8')).color.name
    'WHITE'
    >>> b.castling_rights
    ['K', 'k', 'q']
    >>> b.check(Color.WHITE)
    False
    >>> b.make_move(Location(algebraic='d1'), Location(algebraic='h5'))
    >>> print(b)
       a b c d e f g h
    1  ♜ _ ♝ _ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ _ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  ♟ _ _ ♙ ♞ _ _ _  4
    5  ♟ ♙ _ _ _ ♙ _ ♛  5
    6  _ _ _ _ ♙ _ _ _  6
    7  ♙ _ ♙ _ _ _ ♙ ♙  7
    8  _ ♖ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.check(Color.WHITE)
    True
    >>> for piece in b.color_pieces_flat(Color.WHITE):
    ...     print(list(map(lambda t: t.algebraic, piece.all_legal_moves)))
    ...
    []
    []
    []
    []
    []
    []
    ['g6']
    []
    []
    []
    ['e7', 'd7']
    []
    []
    []
    >>> b.make_move(Location(algebraic='g7'), Location(algebraic='g6'))
    >>> print(b)
       a b c d e f g h
    1  ♜ _ ♝ _ ♚ ♝ ♞ ♜  1
    2  _ _ ♟ ♟ _ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  ♟ _ _ ♙ ♞ _ _ _  4
    5  ♟ ♙ _ _ _ ♙ _ ♛  5
    6  _ _ _ _ ♙ _ ♙ _  6
    7  ♙ _ ♙ _ _ _ _ ♙  7
    8  _ ♖ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.make_move(Location(algebraic='c2'), Location(algebraic='c4'))
    >>> print(b)
       a b c d e f g h
    1  ♜ _ ♝ _ ♚ ♝ ♞ ♜  1
    2  _ _ _ ♟ _ ♟ ♟ ♟  2
    3  _ _ _ _ _ _ _ _  3
    4  ♟ _ ♟ ♙ ♞ _ _ _  4
    5  ♟ ♙ _ _ _ ♙ _ ♛  5
    6  _ _ _ _ ♙ _ ♙ _  6
    7  ♙ _ ♙ _ _ _ _ ♙  7
    8  _ ♖ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b.make_move(Location(algebraic='d4'), Location(algebraic='c3'))
    >>> print(b)
       a b c d e f g h
    1  ♜ _ ♝ _ ♚ ♝ ♞ ♜  1
    2  _ _ _ ♟ _ ♟ ♟ ♟  2
    3  _ _ ♙ _ _ _ _ _  3
    4  ♟ _ _ _ ♞ _ _ _  4
    5  ♟ ♙ _ _ _ ♙ _ ♛  5
    6  _ _ _ _ ♙ _ ♙ _  6
    7  ♙ _ ♙ _ _ _ _ ♙  7
    8  _ ♖ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> list(map(lambda t: t.algebraic, b.get_piece_at(Location(algebraic='g6')).all_legal_moves))
    ['h5']
    >>> b.make_move(Location(algebraic='c1'), Location(algebraic='a3'))
    >>> print(b)
       a b c d e f g h
    1  ♜ _ _ _ ♚ ♝ ♞ ♜  1
    2  _ _ _ ♟ _ ♟ ♟ ♟  2
    3  ♝ _ ♙ _ _ _ _ _  3
    4  ♟ _ _ _ ♞ _ _ _  4
    5  ♟ ♙ _ _ _ ♙ _ ♛  5
    6  _ _ _ _ ♙ _ ♙ _  6
    7  ♙ _ ♙ _ _ _ _ ♙  7
    8  _ ♖ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> print(list(map(lambda t: t.algebraic, b.player_king(Color.BLACK).all_legal_moves)))
    ['e2', 'd1', 'c1']
    >>> b2 = Board(b.fen_str)
    >>> b.make_move(Location(algebraic='c3'), Location(algebraic='c2'))
    >>> print(b)
       a b c d e f g h
    1  ♜ _ _ _ ♚ ♝ ♞ ♜  1
    2  _ _ ♙ ♟ _ ♟ ♟ ♟  2
    3  ♝ _ _ _ _ _ _ _  3
    4  ♟ _ _ _ ♞ _ _ _  4
    5  ♟ ♙ _ _ _ ♙ _ ♛  5
    6  _ _ _ _ ♙ _ ♙ _  6
    7  ♙ _ ♙ _ _ _ _ ♙  7
    8  _ ♖ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> print(list(map(lambda t: t.algebraic, b.player_king(Color.BLACK).all_legal_moves)))
    ['e2']
    >>> print(b2)
       a b c d e f g h
    1  ♜ _ _ _ ♚ ♝ ♞ ♜  1
    2  _ _ _ ♟ _ ♟ ♟ ♟  2
    3  ♝ _ ♙ _ _ _ _ _  3
    4  ♟ _ _ _ ♞ _ _ _  4
    5  ♟ ♙ _ _ _ ♙ _ ♛  5
    6  _ _ _ _ ♙ _ ♙ _  6
    7  ♙ _ ♙ _ _ _ _ ♙  7
    8  _ ♖ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    >>> b2.who = Color.BLACK
    >>> b2.make_move(Location(algebraic='e1'), Location(algebraic='c1'))
    >>> print(b2)
       a b c d e f g h
    1  _ _ ♚ ♜ _ ♝ ♞ ♜  1
    2  _ _ _ ♟ _ ♟ ♟ ♟  2
    3  ♝ _ ♙ _ _ _ _ _  3
    4  ♟ _ _ _ ♞ _ _ _  4
    5  ♟ ♙ _ _ _ ♙ _ ♛  5
    6  _ _ _ _ ♙ _ ♙ _  6
    7  ♙ _ ♙ _ _ _ _ ♙  7
    8  _ ♖ _ ♕ ♔ ♗ ♘ ♖  8
       a b c d e f g h
    """
