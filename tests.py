#!/usr/bin/env python3
"""
Test that Chess is behaving correctly.

TODO:
    - test end game conditions:
        - game should end in a tie if there is a stalemate
        - game should end if there is a checkmate
        - game should end properly with the 50 move draw rule
    - test that the halfmove clock and fullmove number are updated appropriately
    - test that fullmove and halmove counters are updated correctly
    - test that the game ends if either player is in check mate
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
    8  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  _ _ _ _ _ _ _ _  5
    4  _ _ _ _ _ _ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  2
    1  ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    <BLANKLINE>
    >>> b.fen_str
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    >>> b.who.value
    0
    >>> b.en_passant_target.algebraic
    '-'
    >>> b.who.name
    'WHITE'
    >>> try:
    ...     b.make_move(Move(Location(algebraic='b7'), Location(algebraic='b6')))
    ... except IllegalMoveError as e:
    ...     print(e)
    It is white\'s turn and white does not control the selected piece. Please select a valid piece to move.
    >>> try:
    ...     b.make_move(Move(Location(algebraic='a5'), Location(algebraic='a4')))
    ... except IllegalMoveError as e:
    ...     print(e)
    Cannot make a move from an empty square. Please select a valid piece to move.
    >>> b.make_move(Move(Location(algebraic='b1'), Location(algebraic='c3')))
    >>> print(b)
       a b c d e f g h
    8  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  _ _ _ _ _ _ _ _  5
    4  _ _ _ _ _ _ _ _  4
    3  _ _ ♘ _ _ _ _ _  3
    2  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  2
    1  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR b KQkq - 1 1
    <BLANKLINE>
    >>> b.make_move(Move(Location(algebraic='a7'), Location(algebraic='a5')))
    >>> print(b)
       a b c d e f g h
    8  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ ♟ ♟ ♟ ♟ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  ♟ _ _ _ _ _ _ _  5
    4  _ _ _ _ _ _ _ _  4
    3  _ _ ♘ _ _ _ _ _  3
    2  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  2
    1  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    rnbqkbnr/1ppppppp/8/p7/8/2N5/PPPPPPPP/R1BQKBNR w KQkq a6 0 2
    <BLANKLINE>
    >>> b.make_move(Move(Location(algebraic='c3'), Location(algebraic='a4')))
    >>> print(b)
       a b c d e f g h
    8  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ ♟ ♟ ♟ ♟ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  ♟ _ _ _ _ _ _ _  5
    4  ♘ _ _ _ _ _ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  2
    1  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    rnbqkbnr/1ppppppp/8/p7/N7/8/PPPPPPPP/R1BQKBNR b KQkq - 1 2
    <BLANKLINE>
    >>> b.make_move(Move(Location(algebraic='b7'), Location(algebraic='b5')))
    >>> print(b)
       a b c d e f g h
    8  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ ♟ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  ♟ ♟ _ _ _ _ _ _  5
    4  ♘ _ _ _ _ _ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  2
    1  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    rnbqkbnr/2pppppp/8/pp6/N7/8/PPPPPPPP/R1BQKBNR w KQkq b6 0 3
    <BLANKLINE>
    >>> pawn = b.get_piece_at(Location(algebraic='b5'))
    >>> [move.target.algebraic for move in pawn.all_legal_moves]
    ['b4', 'a4']
    >>> kn = b.get_piece_at(Location(algebraic='a4'))
    >>> [move.target.algebraic for move in kn.all_legal_moves]
    ['c3', 'c5', 'b6']
    >>> try:
    ...     b.make_move(Move(Location(algebraic='a4'), Location(algebraic='a3')))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal.
    >>> try:
    ...     b.make_move(Move(Location(algebraic='a4'), Location(algebraic='a52')))
    ... except IllegalMoveError as e:
    ...     print(e)
    Cannot move outside the boundaries of the board. Please select a different destination.
    >>> fen_str = b.fen_str
    >>> b2 = Board(fen_str)
    >>> print(b2)
       a b c d e f g h
    8  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ ♟ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  ♟ ♟ _ _ _ _ _ _  5
    4  ♘ _ _ _ _ _ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  2
    1  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    rnbqkbnr/2pppppp/8/pp6/N7/8/PPPPPPPP/R1BQKBNR w KQkq b6 0 3
    <BLANKLINE>
    >>> try:
    ...     b.make_move(Move(Location(algebraic='b2'), Location(algebraic='b5')))
    ... except:
    ...     print('illegal move')
    illegal move
    >>> b.make_move(Move(Location(algebraic='b2'), Location(algebraic='b4'))); print(b)
       a b c d e f g h
    8  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ ♟ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  ♟ ♟ _ _ _ _ _ _  5
    4  ♘ ♙ _ _ _ _ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ _ ♙ ♙ ♙ ♙ ♙ ♙  2
    1  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    rnbqkbnr/2pppppp/8/pp6/NP6/8/P1PPPPPP/R1BQKBNR b KQkq b3 0 3
    <BLANKLINE>
    >>> list(map(lambda m: m.target.algebraic, b.get_piece_at(Location(algebraic='c1')).all_legal_moves))
    ['b2', 'a3']
    >>> try:
    ...     b.make_move(Move(Location(algebraic='b8'), Location(algebraic='b7')))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal.
    >>> list(map(lambda m: m.target.algebraic, b.get_piece_at(Location(algebraic='c8')).all_legal_moves))
    ['b7', 'a6']
    >>> b.make_move(Move(Location(algebraic='b8'), Location(algebraic='c6'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ ♟ ♟ ♟ ♟  7
    6  _ _ ♞ _ _ _ _ _  6
    5  ♟ ♟ _ _ _ _ _ _  5
    4  ♘ ♙ _ _ _ _ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ _ ♙ ♙ ♙ ♙ ♙ ♙  2
    1  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1bqkbnr/2pppppp/2n5/pp6/NP6/8/P1PPPPPP/R1BQKBNR w KQkq - 1 4
    <BLANKLINE>
    >>> b.make_move(Move(Location(algebraic='d2'), Location(algebraic='d4'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ ♟ ♟ ♟ ♟  7
    6  _ _ ♞ _ _ _ _ _  6
    5  ♟ ♟ _ _ _ _ _ _  5
    4  ♘ ♙ _ ♙ _ _ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ _ ♙ _ ♙ ♙ ♙ ♙  2
    1  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1bqkbnr/2pppppp/2n5/pp6/NP1P4/8/P1P1PPPP/R1BQKBNR b KQkq d3 0 4
    <BLANKLINE>
    >>> b.en_passant_target.algebraic
    'd3'
    >>> b.who = Color.WHITE
    >>> b.make_move(Move(Location(algebraic='d4'), Location(algebraic='d5'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ ♟ ♟ ♟ ♟  7
    6  _ _ ♞ _ _ _ _ _  6
    5  ♟ ♟ _ ♙ _ _ _ _  5
    4  ♘ ♙ _ _ _ _ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ _ ♙ _ ♙ ♙ ♙ ♙  2
    1  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1bqkbnr/2pppppp/2n5/pp1P4/NP6/8/P1P1PPPP/R1BQKBNR b KQkq - 0 4
    <BLANKLINE>
    >>> b.make_move(Move(Location(algebraic='e7'), Location(algebraic='e5'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ _ ♟ ♟ ♟  7
    6  _ _ ♞ _ _ _ _ _  6
    5  ♟ ♟ _ ♙ ♟ _ _ _  5
    4  ♘ ♙ _ _ _ _ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ _ ♙ _ ♙ ♙ ♙ ♙  2
    1  ♖ _ ♗ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1bqkbnr/2pp1ppp/2n5/pp1Pp3/NP6/8/P1P1PPPP/R1BQKBNR w KQkq e6 0 5
    <BLANKLINE>
    >>> b.fen_str
    'r1bqkbnr/2pp1ppp/2n5/pp1Pp3/NP6/8/P1P1PPPP/R1BQKBNR w KQkq e6 0 5'
    >>> list(map(lambda m: m.target.algebraic, b.get_piece_at(Location(algebraic='d5')).all_legal_moves))
    ['d6', 'e6', 'c6']
    >>> try:
    ...     b.make_move(Move(Location(algebraic='d5'), Location(algebraic='d5')))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal.
    >>> try:
    ...     b.make_move(Move(Location(algebraic='a4'), Location(algebraic='a4')))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal.
    >>> try:
    ...     b.make_move(Move(Location(algebraic='c1'), Location(algebraic='c1')))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal.
    >>> list(map(lambda m: m.target.algebraic, b.get_piece_at(Location(algebraic='c1')).all_legal_moves))
    ['d2', 'e3', 'f4', 'g5', 'h6', 'b2', 'a3']
    >>> b.make_move(Move(Location(algebraic='c1'), Location(algebraic='f4'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ _ ♟ ♟ ♟  7
    6  _ _ ♞ _ _ _ _ _  6
    5  ♟ ♟ _ ♙ ♟ _ _ _  5
    4  ♘ ♙ _ _ _ ♗ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ _ ♙ _ ♙ ♙ ♙ ♙  2
    1  ♖ _ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1bqkbnr/2pp1ppp/2n5/pp1Pp3/NP3B2/8/P1P1PPPP/R2QKBNR b KQkq - 1 5
    <BLANKLINE>
    >>> list(map(lambda m: m.target.algebraic, b.get_piece_at(Location(algebraic='f4')).all_legal_moves))
    ['g3', 'e3', 'd2', 'c1', 'g5', 'h6', 'e5']
    >>> b.who = Color.WHITE
    >>> b.make_move(Move(Location(algebraic='f4'), Location(algebraic='e5'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ _ ♟ ♟ ♟  7
    6  _ _ ♞ _ _ _ _ _  6
    5  ♟ ♟ _ ♙ ♗ _ _ _  5
    4  ♘ ♙ _ _ _ _ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ _ ♙ _ ♙ ♙ ♙ ♙  2
    1  ♖ _ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1bqkbnr/2pp1ppp/2n5/pp1PB3/NP6/8/P1P1PPPP/R2QKBNR b KQkq - 0 5
    <BLANKLINE>
    >>> b.castling_rights
    ['K', 'Q', 'k', 'q']
    >>> b.half_move_clock
    0
    >>> try:
    ...     b.make_move(Move(Location(algebraic='b5'), Location(algebraic='b3')))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal.
    >>> b.make_move(Move(Location(algebraic='b5'), Location(algebraic='a4'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ _ ♟ ♟ ♟  7
    6  _ _ ♞ _ _ _ _ _  6
    5  ♟ _ _ ♙ ♗ _ _ _  5
    4  ♟ ♙ _ _ _ _ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ _ ♙ _ ♙ ♙ ♙ ♙  2
    1  ♖ _ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1bqkbnr/2pp1ppp/2n5/p2PB3/pP6/8/P1P1PPPP/R2QKBNR w KQkq - 0 6
    <BLANKLINE>
    >>> try:
    ...     b.make_move(Move(Location(algebraic='b4'), Location(algebraic='b6')))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal.
    >>> b.who = Color.WHITE
    >>> b.make_move(Move(Location(algebraic='f2'), Location(algebraic='f4')))
    >>> b.en_passant_target.algebraic
    'f3'
    >>> try:
    ...     b.make_move(Move(Location(algebraic='c6'), Location(algebraic='c5')))
    ... except IllegalMoveError as e:
    ...     print(e)
    Move is not legal.
    >>> b.make_move(Move(Location(algebraic='c6'), Location(algebraic='e5'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ _ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  ♟ _ _ ♙ ♞ _ _ _  5
    4  ♟ ♙ _ _ _ ♙ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ _ ♙ _ ♙ _ ♙ ♙  2
    1  ♖ _ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1bqkbnr/2pp1ppp/8/p2Pn3/pP3P2/8/P1P1P1PP/R2QKBNR w KQkq - 0 7
    <BLANKLINE>
    >>> b.en_passant_target.algebraic
    '-'
    >>> ##b.get_piece_at(Location(algebraic='a1')).all_legal_moves
    >>> list(map(lambda m: m.target.algebraic, b.get_piece_at(Location(algebraic='a1')).all_legal_moves))
    ['b1', 'c1']
    >>> b.make_move(Move(Location(algebraic='a1'), Location(algebraic='b1')))
    >>> print(b)
       a b c d e f g h
    8  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ _ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  ♟ _ _ ♙ ♞ _ _ _  5
    4  ♟ ♙ _ _ _ ♙ _ _  4
    3  _ _ _ _ _ _ _ _  3
    2  ♙ _ ♙ _ ♙ _ ♙ ♙  2
    1  _ ♖ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1bqkbnr/2pp1ppp/8/p2Pn3/pP3P2/8/P1P1P1PP/1R1QKBNR b Kkq - 1 7
    <BLANKLINE>
    >>> list(map(lambda m: m.target.algebraic, b.get_piece_at(Location(algebraic='b1')).all_legal_moves))
    ['b2', 'b3', 'a1', 'c1']
    >>> try:
    ...     b.make_move(Move(Location(algebraic='b1'), Location(algebraic='b4')))
    ... except IllegalMoveError as e:
    ...     print('Illegal move was attempted')
    Illegal move was attempted
    >>> b.who = Color.WHITE
    >>> b.make_move(Move(Location(algebraic='e2'), Location(algebraic='e3'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ ♛ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ _ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  ♟ _ _ ♙ ♞ _ _ _  5
    4  ♟ ♙ _ _ _ ♙ _ _  4
    3  _ _ _ _ ♙ _ _ _  3
    2  ♙ _ ♙ _ _ _ ♙ ♙  2
    1  _ ♖ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1bqkbnr/2pp1ppp/8/p2Pn3/pP3P2/4P3/P1P3PP/1R1QKBNR b Kkq - 0 7
    <BLANKLINE>
    >>> ##b.get_piece_at(Location(algebraic='d1')).all_legal_moves
    >>> list(map(lambda m: m.target.algebraic, b.get_piece_at(Location(algebraic='d1')).all_legal_moves))
    ['d2', 'd3', 'd4', 'e2', 'f3', 'g4', 'h5', 'c1']
    >>> b.get_piece_at(Location(algebraic='d1')).color.value
    0
    >>> b.get_piece_at(Location(algebraic='d1')).color.name
    'WHITE'
    >>> b.castling_rights
    ['K', 'k', 'q']
    >>> b.check(Color.WHITE)
    False
    >>> b.make_move(Move(Location(algebraic='d8'), Location(algebraic='h4'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ _ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ _ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  ♟ _ _ ♙ ♞ _ _ _  5
    4  ♟ ♙ _ _ _ ♙ _ ♛  4
    3  _ _ _ _ ♙ _ _ _  3
    2  ♙ _ ♙ _ _ _ ♙ ♙  2
    1  _ ♖ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1b1kbnr/2pp1ppp/8/p2Pn3/pP3P1q/4P3/P1P3PP/1R1QKBNR w Kkq - 1 8
    <BLANKLINE>
    >>> b.check(Color.WHITE)
    True
    >>> for piece in b.color_pieces_flat(Color.WHITE):
    ...     print(list(map(lambda m: m.target.algebraic, piece.all_legal_moves)))
    ...
    []
    []
    []
    []
    []
    []
    ['g3']
    []
    []
    []
    ['e2', 'd2']
    []
    []
    []
    >>> b.make_move(Move(Location(algebraic='g2'), Location(algebraic='g3'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ _ ♚ ♝ ♞ ♜  8
    7  _ _ ♟ ♟ _ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  ♟ _ _ ♙ ♞ _ _ _  5
    4  ♟ ♙ _ _ _ ♙ _ ♛  4
    3  _ _ _ _ ♙ _ ♙ _  3
    2  ♙ _ ♙ _ _ _ _ ♙  2
    1  _ ♖ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1b1kbnr/2pp1ppp/8/p2Pn3/pP3P1q/4P1P1/P1P4P/1R1QKBNR b Kkq - 0 8
    <BLANKLINE>
    >>> b.make_move(Move(Location(algebraic='c7'), Location(algebraic='c5'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ _ ♚ ♝ ♞ ♜  8
    7  _ _ _ ♟ _ ♟ ♟ ♟  7
    6  _ _ _ _ _ _ _ _  6
    5  ♟ _ ♟ ♙ ♞ _ _ _  5
    4  ♟ ♙ _ _ _ ♙ _ ♛  4
    3  _ _ _ _ ♙ _ ♙ _  3
    2  ♙ _ ♙ _ _ _ _ ♙  2
    1  _ ♖ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1b1kbnr/3p1ppp/8/p1pPn3/pP3P1q/4P1P1/P1P4P/1R1QKBNR w Kkq c6 0 9
    <BLANKLINE>
    >>> b.make_move(Move(Location(algebraic='d5'), Location(algebraic='c6'))); print(b)
       a b c d e f g h
    8  ♜ _ ♝ _ ♚ ♝ ♞ ♜  8
    7  _ _ _ ♟ _ ♟ ♟ ♟  7
    6  _ _ ♙ _ _ _ _ _  6
    5  ♟ _ _ _ ♞ _ _ _  5
    4  ♟ ♙ _ _ _ ♙ _ ♛  4
    3  _ _ _ _ ♙ _ ♙ _  3
    2  ♙ _ ♙ _ _ _ _ ♙  2
    1  _ ♖ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r1b1kbnr/3p1ppp/2P5/p3n3/pP3P1q/4P1P1/P1P4P/1R1QKBNR b Kkq - 0 9
    <BLANKLINE>
    >>> list(map(lambda m: m.target.algebraic, b.get_piece_at(Location(algebraic='g3')).all_legal_moves))
    ['h4']
    >>> b.make_move(Move(Location(algebraic='c8'), Location(algebraic='a6'))); print(b)
       a b c d e f g h
    8  ♜ _ _ _ ♚ ♝ ♞ ♜  8
    7  _ _ _ ♟ _ ♟ ♟ ♟  7
    6  ♝ _ ♙ _ _ _ _ _  6
    5  ♟ _ _ _ ♞ _ _ _  5
    4  ♟ ♙ _ _ _ ♙ _ ♛  4
    3  _ _ _ _ ♙ _ ♙ _  3
    2  ♙ _ ♙ _ _ _ _ ♙  2
    1  _ ♖ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r3kbnr/3p1ppp/b1P5/p3n3/pP3P1q/4P1P1/P1P4P/1R1QKBNR w Kkq - 1 10
    <BLANKLINE>
    >>> print(list(map(lambda m: m.target.algebraic, b.player_king(Color.BLACK).all_legal_moves)))
    ['e7', 'd8', 'c8']
    >>> b2 = Board(b.fen_str)
    >>> b.make_move(Move(Location(algebraic='c6'), Location(algebraic='c7')))
    >>> print(b)
       a b c d e f g h
    8  ♜ _ _ _ ♚ ♝ ♞ ♜  8
    7  _ _ ♙ ♟ _ ♟ ♟ ♟  7
    6  ♝ _ _ _ _ _ _ _  6
    5  ♟ _ _ _ ♞ _ _ _  5
    4  ♟ ♙ _ _ _ ♙ _ ♛  4
    3  _ _ _ _ ♙ _ ♙ _  3
    2  ♙ _ ♙ _ _ _ _ ♙  2
    1  _ ♖ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r3kbnr/2Pp1ppp/b7/p3n3/pP3P1q/4P1P1/P1P4P/1R1QKBNR b Kkq - 0 10
    <BLANKLINE>
    >>> print(list(map(lambda m: m.target.algebraic, b.player_king(Color.BLACK).all_legal_moves)))
    ['e7']
    >>> print(b2)
       a b c d e f g h
    8  ♜ _ _ _ ♚ ♝ ♞ ♜  8
    7  _ _ _ ♟ _ ♟ ♟ ♟  7
    6  ♝ _ ♙ _ _ _ _ _  6
    5  ♟ _ _ _ ♞ _ _ _  5
    4  ♟ ♙ _ _ _ ♙ _ ♛  4
    3  _ _ _ _ ♙ _ ♙ _  3
    2  ♙ _ ♙ _ _ _ _ ♙  2
    1  _ ♖ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    r3kbnr/3p1ppp/b1P5/p3n3/pP3P1q/4P1P1/P1P4P/1R1QKBNR w Kkq - 1 10
    <BLANKLINE>
    >>> b2.who = Color.BLACK
    >>> b2.make_move(Move(Location(algebraic='e8'), Location(algebraic='c8')))
    >>> print(b2)
       a b c d e f g h
    8  _ _ ♚ ♜ _ ♝ ♞ ♜  8
    7  _ _ _ ♟ _ ♟ ♟ ♟  7
    6  ♝ _ ♙ _ _ _ _ _  6
    5  ♟ _ _ _ ♞ _ _ _  5
    4  ♟ ♙ _ _ _ ♙ _ ♛  4
    3  _ _ _ _ ♙ _ ♙ _  3
    2  ♙ _ ♙ _ _ _ _ ♙  2
    1  _ ♖ _ ♕ ♔ ♗ ♘ ♖  1
       a b c d e f g h
    2kr1bnr/3p1ppp/b1P5/p3n3/pP3P1q/4P1P1/P1P4P/1R1QKBNR w K - 2 11
    <BLANKLINE>
    """
