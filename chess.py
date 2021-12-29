#!/usr/bin/env python3
""" A standalone chess game.
TODO:
    -handle pawn promotion appropriately
"""

from os import system
from enum import Enum
from typing import List


class Color(Enum):
    """Colors."""
    WHITE = 0
    BLACK = 1

    @classmethod
    def other(cls, color):
        """ Return the other color."""
        if color is cls.WHITE:
            return cls.BLACK
        if color is cls.BLACK:
            return cls.WHITE
        raise Exception(f"unknown color: {color}")


class Location:
    """ Hold information about a particular location."""
    def __init__(self, algebraic: str = None, row_col: tuple = None):
        if algebraic is not None:
            self.algebraic = algebraic
            if self.algebraic == "-":
                self.row, self.col = -1, -1
            else:
                self.row, self.col = Location.row_col_from_algebraic(algebraic)
        elif row_col is not None:
            self.row, self.col = row_col
            self.algebraic = Location.algebraic_from_row_col(row_col)
        else:
            raise Exception("bad inputs")

    @classmethod
    def algebraic_from_row_col(cls, row_col: tuple) -> str:
        """ Return a string with the algebraic notation for the given row_col"""
        def idx_to_letter(idx: int) -> str:
            return chr(idx + 97)

        return idx_to_letter(row_col[1]) + str(8 - row_col[0])

    @classmethod
    def row_col_from_algebraic(cls, algebraic: str) -> tuple:
        """ Return a tuple containing the location of algebraic as indexes into an 8x8 matrix."""
        def letter_to_idx(ltr: str) -> int:
            return ord(ltr) - 97

        return (8 - int(algebraic[1:]), letter_to_idx(algebraic[0]))

    @property
    def in_bounds(self) -> bool:
        """ Check if self is in bounds."""
        return 0 <= self.row <= 7 and 0 <= self.col <= 7

    def __eq__(self, other: Color) -> bool:
        return self.algebraic == other.algebraic


class Board:
    """ Class to represent a chess board.

    board_rep:          An 8x8 matrix, where each element is either a piece or Board.empty.
    castling_rights:    A list describing each player's castling rights.
    half_move_clock:    The number of halfmoves, in terms of the 50 move draw rule.
    full_move_number:   The number of full moves in a game. incremented every black move.
    en_passant_target:  The location of the en passant target.
    who:                The color of the current player.
    """
    initial_setup = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    empty = ()

    def __init__(self, fen: str = None):
        if fen is None:
            fen = Board.initial_setup
        fen = fen.split()
        position_field = list(fen[0]) + ["/"]

        self.board_rep, row = [], []
        row_idx, col_idx = 0, 0
        for elem in position_field:
            if elem.lower() in PIECE_TYPES:
                color = Color(elem.islower())
                piece = PIECE_TYPES[elem.lower()](Location(row_col=(row_idx,
                                                                    col_idx)),
                                                  color, self)
                row.append(piece)
                col_idx += 1
            elif elem.isnumeric():
                for _ in range(int(elem)):
                    row.append(Board.empty)
                    col_idx += 1
            elif elem == "/":
                self.board_rep.append(row)
                row = []
                row_idx += 1
                col_idx = 0
            else:
                raise Exception(f"unknown value in fen string: {elem}")

        if fen[1] == "w":
            self.who = Color.WHITE
        else:
            self.who = Color.BLACK
        self.castling_rights = list(fen[2])
        self.en_passant_target = Location(algebraic=fen[3])
        self.half_move_clock = int(fen[4])
        self.full_move_number = int(fen[5])

    def make_move(self, origin: Location, target: Location) -> None:
        """ If given move is illegal, raise IllegalMoveError, otherwise make the move."""
        piece_to_move = self.board_rep[origin.row][origin.col]

        # if the move is not legal, an error will be thrown in the next two lines
        self.is_legal_move_general(origin, target)
        piece_to_move.is_legal(target)

        pawn_was_moved = isinstance(piece_to_move, Pawn)
        en_passant_capture = self.en_passant_target == target and pawn_was_moved
        self.update_en_passant_target(origin, target, pawn_was_moved)
        self.update_clocks(target, en_passant_capture, pawn_was_moved)
        self.update_castling_rights(origin)
        castling_occured = isinstance(
            piece_to_move, King) and abs(origin.col - target.col) > 1
        if castling_occured:
            king_moved_left = origin.col > target.col
            if king_moved_left:
                castle_to_move = self.board_rep[origin.row][0]
                castle_target_col = target.col + 1
            else:
                castle_to_move = self.board_rep[origin.row][7]
                castle_target_col = target.col - 1
            castle_orig_location = castle_to_move.location
            castle_to_move.location = Location(row_col=(origin.row,
                                                        castle_target_col))
            self.board_rep[castle_to_move.location.row][
                castle_to_move.location.col] = castle_to_move
            self.board_rep[castle_orig_location.row][
                castle_orig_location.col] = Board.empty

        self.who = Color.other(self.who)
        piece_to_move.location = target
        self.board_rep[target.row][target.col] = piece_to_move
        self.board_rep[origin.row][origin.col] = Board.empty
        if en_passant_capture:
            self.board_rep[origin.row][target.col] = Board.empty


    def update_en_passant_target(self, origin: Location, target: Location,
                                 pawn_was_moved: bool) -> None:
        """ Update the en passant target."""
        if pawn_was_moved and abs(origin.row - target.row) == 2:
            en_passant_row = (origin.row + target.row) // 2
            self.en_passant_target = Location(row_col=(en_passant_row,
                                                       target.col))
        else:
            self.en_passant_target = Location(algebraic="-")

    def update_clocks(
        self,
        target: Location,
        en_passant_capture: bool,
        pawn_was_moved: bool,
    ) -> None:
        """ Update the game clocks."""
        piece_was_captured = (self.board_rep[target.row][target.col]
                              is not Board.empty) or en_passant_capture
        if pawn_was_moved or piece_was_captured:
            self.half_move_clock = 0
        else:
            self.half_move_clock += 1
        if self.who is Color.BLACK:
            self.full_move_number += 1

    def update_castling_rights(self, origin: Location) -> None:
        """ Update the castling rights."""
        piece_to_move = self.board_rep[origin.row][origin.col]
        if len(self.castling_rights) > 0:
            castling_rights_to_remove = []
            if origin.row == 0 and origin.col == 0:
                castling_rights_to_remove.extend("q")
            elif origin.row == 0 and origin.col == 7:
                castling_rights_to_remove.extend("k")
            elif piece_to_move.color == Color.BLACK and isinstance(
                    piece_to_move, King):
                castling_rights_to_remove.extend("k")
                castling_rights_to_remove.extend("q")
            elif origin.row == 7 and origin.col == 0:
                castling_rights_to_remove.extend("Q")
            elif origin.row == 7 and origin.col == 7:
                castling_rights_to_remove.extend("K")
            elif piece_to_move.color == Color.WHITE and isinstance(
                    piece_to_move, King):
                castling_rights_to_remove.extend("K")
                castling_rights_to_remove.extend("Q")
            for elem in castling_rights_to_remove:
                if elem in self.castling_rights:
                    self.castling_rights.remove(elem)
        if not self.castling_rights:
            self.castling_rights = ['-']

    def check(self, color: Color) -> bool:
        """ Return True if color is in check, False otherwise."""
        king_location = self.player_king(color).location
        for piece in self.flat_board_rep:
            if piece is not Board.empty and piece.color is not color:
                for target in piece.move_generator():
                    if target == king_location:
                        return True
        return False

    def checkmate(self, color: Color) -> bool:
        """ Return True if color is in checkmate, False otherwise."""
        if self.check(color) is False:
            return False
        for piece in self.color_pieces_flat(color):
            if piece.all_legal_moves:  # if there's any legal moves, no check mate
                return False
        return True

    def get_piece_at(self, location: Location):
        """ Return the piece located at location."""
        return self.board_rep[location.row][location.col]

    def color_pieces(self, color: Color) -> List[List[int]]:
        """ Return an 8x8 bit array, with a 1 if there are color pieces there, and a 0 otherwise."""
        cur_player_bit_arr = []
        for row in self.board_rep:
            cur_player_bit_arr.append([
                int(elem is not Board.empty and elem.color is color)
                for elem in row
            ])
        return cur_player_bit_arr

    def color_pieces_flat(self, color: Color):
        """ Return a list of color pieces."""
        pieces = []
        for piece in self.flat_board_rep:
            if piece is not Board.empty and piece.color is color:
                pieces.append(piece)
        return pieces

    def player_king(self, color: Color):
        """ Return the king of the appropriate color."""
        for piece in self.color_pieces_flat(color):
            if isinstance(piece, King):
                return piece
        raise Exception("king not found")

    @property
    def fen_str(self) -> str:
        """ The fen string for self."""
        def letter_from_type(typ) -> str:
            for k, v in PIECE_TYPES.items():
                if v == typ:
                    return k
            raise Exception("unknown piece type")

        fen_str = ""
        for row in self.board_rep:
            empty_sqr_count = 0
            for piece in row:
                if piece is not Board.empty:
                    if empty_sqr_count > 0:
                        fen_str += str(empty_sqr_count)
                        empty_sqr_count = 0
                    letter = letter_from_type(type(piece))
                    if piece.color == Color.WHITE:
                        letter = letter.upper()
                    fen_str += letter
                else:
                    empty_sqr_count += 1
            if empty_sqr_count > 0:
                fen_str += str(empty_sqr_count)
            fen_str += "/"  # add a slash at the end of each row
        fen_str = fen_str[:-1]  # remove the final slash
        fen_str += " " + self.who.name[0].lower() + " "
        fen_str += "".join(self.castling_rights)
        fen_str += " " + self.en_passant_target.algebraic
        fen_str += " " + str(self.half_move_clock)
        fen_str += " " + str(self.full_move_number)
        return fen_str

    @property
    def flat_board_rep(self) -> list:
        """ A 64 element list representing the board."""
        flat_board = []
        for row in self.board_rep:
            flat_board.extend(row)
        return flat_board

    @property
    def has_winner(self) -> bool:
        """ True if there is a winner, False otherwise."""
        return self.checkmate(self.who) or self.checkmate(Color.other(
            self.who))

    def __str__(self) -> str:
        """ Return a human readable string displaying the board."""
        str_rep = "   a b c d e f g h\n"
        i = 8
        for row in self.board_rep:
            str_rep += str(i) + "  "
            for piece in row:
                if piece is Board.empty:
                    str_rep += "_"
                else:
                    str_rep += str(piece)
                str_rep += " "
            str_rep += " " + str(i) + "\n"
            i -= 1
        str_rep += "   a b c d e f g h"
        str_rep += '\n' + self.fen_str + '\n'
        return str_rep

    def is_legal_move_general(self, origin, target) -> None:
        """ Raise an error it the given move fails some general checks for move legality."""
        if not origin.in_bounds:
            raise IllegalMoveError(
                "Starting row and column must be be within 0-8 inclusive")
        if not target.in_bounds:
            raise IllegalMoveError(
                "Cannot move outside the boundaries of the board. Please select "
                + "a different destination.")
        if self.board_rep[origin.row][origin.col] is Board.empty:
            raise IllegalMoveError(
                "Cannot make a move from an empty square. Please select a valid piece to move."
            )
        if self.board_rep[origin.row][origin.col].color != self.who:
            raise IllegalMoveError(
                f"It is {self.who.name.lower()}'s turn and " +
                f"{self.who.name.lower()} does not " +
                "control the selected piece. Please select a valid piece to " +
                "move.")


class Piece:
    """ A class for chess pieces."""
    def __init__(self, location, color, board, symbol):
        if not location.in_bounds:
            raise Exception(
                "Invalid position for piece instantiation. Attempted to create"
                + f"piece at row={location.row}, col={location.col}")
        self.location = location
        self.color = color
        self.board = board
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    @property
    def row(self) -> int:
        """ Return the row where the piece is located."""
        return self.location.row

    @property
    def col(self) -> int:
        """ Return the column where the piece is located."""
        return self.location.col

    @property
    def algebraic(self) -> str:
        """ Return the loction of the piece in algebraic notation."""
        return self.location.algebraic

    @property
    def all_legal_moves(self) -> list:
        """ Return a list of all legal target locations for this piece."""
        targets = []
        for target in self.move_generator():
            if not self.moving_into_check(target):
                targets.append(target)
        return targets

    def is_legal(self, target: Location) -> None:
        """ Raise an error if self can not legally move to target."""
        if target not in self.all_legal_moves:
            raise IllegalMoveError("Move is not legal")

    def moving_into_check(self, target: Location) -> bool:
        """ Return True if self moving to target would result in self being in check."""
        brd = Board(self.board.fen_str)
        brd.board_rep[target.row][target.col] = brd.board_rep[self.row][
            self.col]
        brd.board_rep[self.row][self.col] = Board.empty
        brd.board_rep[target.row][target.col].location = target

        return brd.check(self.color)

    def move_generator(self):
        """ Return a generator which yields target locations not considering whether
        they would be 'moving into check'"""
        raise NotImplementedError


class King(Piece):
    """ King class."""
    def __init__(self, location, color, board):
        if color == Color.WHITE:
            symbol = "\N{white chess king}"
        else:
            symbol = "\N{black chess king}"
        super().__init__(location, color, board, symbol)

    def move_generator(self):
        """ Return a generator which yields target locations not considering whether
        they would be 'moving into check'"""
        directions = {
            "up": [-1, 0],
            "up_right": [-1, 1],
            "right": [0, 1],
            "down_right": [1, 1],
            "down": [1, 0],
            "down_left": [1, -1],
            "left": [0, -1],
            "up_left": [-1, -1]
        }
        own_squares = self.board.color_pieces(self.color)
        for direction in directions.values():
            target = Location(row_col=(self.row + direction[0],
                                       self.col + direction[1]))
            if target.in_bounds:
                if own_squares[target.row][target.col] == 0:
                    yield target
        yield from self.castle_move_generator()

    def castle_move_generator(self):
        """ Return a generator which yields castling moves, not considering
        whether they would be moving through or into check."""
        if self.color == Color.WHITE:
            relevant_castling_rights = filter(lambda elem: elem.isupper(),
                                              self.board.castling_rights)
        else:
            relevant_castling_rights = filter(lambda elem: elem.islower(),
                                              self.board.castling_rights)
        relevant_castling_rights = map(lambda elem: elem.lower(),
                                       relevant_castling_rights)
        if "k" in relevant_castling_rights:
            if all(
                    self.board.get_piece_at(Location(
                        algebraic=loc)) is Board.empty
                    for loc in [f"f{8 - self.row}", f"g{8 - self.row}"]):
                if not self.moving_into_check(
                        Location(algebraic=f"f{8 - self.row}")):
                    yield Location(algebraic=f"g{8 - self.row}")

        if "q" in relevant_castling_rights:
            if all(
                    self.board.get_piece_at(Location(
                        algebraic=loc)) is Board.empty for loc in
                [f"b{8 - self.row}", f"c{8 - self.row}", f"d{8 - self.row}"]):
                if not self.moving_into_check(
                        Location(algebraic=f"d{8 - self.row}")):
                    yield Location(algebraic=f"c{8 - self.row}")


class Queen(Piece):
    """ Queen class"""
    def __init__(self, location, color, board):
        if color == Color.WHITE:
            symbol = "\N{white chess queen}"
        else:
            symbol = "\N{black chess queen}"
        super().__init__(location, color, board, symbol)

    def move_generator(self):
        """ Return a generator which yields target locations not considering whether
        they would be 'moving into check'"""
        own_squares = self.board.color_pieces(self.color)
        opp_squares = self.board.color_pieces(Color.other(self.color))
        directions = {
            "up": [-1, 0],
            "up_right": [-1, 1],
            "right": [0, 1],
            "down_right": [1, 1],
            "down": [1, 0],
            "down_left": [1, -1],
            "left": [0, -1],
            "up_left": [-1, -1]
        }
        for direction in directions.values():
            target = Location(row_col=(self.row + direction[0],
                                       self.col + direction[1]))
            while target.in_bounds:
                if own_squares[target.row][target.col]:
                    break
                yield target
                if opp_squares[target.row][target.col]:
                    break
                target = Location(row_col=(target.row + direction[0],
                                           target.col + direction[1]))


class Rook(Piece):
    """ Rook class."""
    def __init__(self, location, color, board):
        if color == Color.WHITE:
            symbol = "\N{white chess rook}"
        else:
            symbol = "\N{black chess rook}"
        super().__init__(location, color, board, symbol)

    def move_generator(self):
        """ Return a generator which yields target locations not considering whether
        they would be 'moving into check'"""
        own_squares = self.board.color_pieces(self.color)
        opp_squares = self.board.color_pieces(Color.other(self.color))
        directions = {
            "up": [-1, 0],
            "down": [1, 0],
            "left": [0, -1],
            "right": [0, 1]
        }
        for direction in directions.values():
            target = Location(row_col=(self.row + direction[0],
                                       self.col + direction[1]))
            while target.in_bounds:
                if own_squares[target.row][target.col]:
                    break
                yield target
                if opp_squares[target.row][target.col]:
                    break
                target = Location(row_col=(target.row + direction[0],
                                           target.col + direction[1]))


class Bishop(Piece):
    """ Bishop class."""
    def __init__(self, location, color, board):
        if color == Color.WHITE:
            symbol = "\N{white chess bishop}"
        else:
            symbol = "\N{black chess bishop}"
        super().__init__(location, color, board, symbol)

    def move_generator(self):
        """ Return a generator which yields target locations not considering whether
        they would be 'moving into check'"""
        own_squares = self.board.color_pieces(self.color)
        opp_squares = self.board.color_pieces(Color.other(self.color))
        for vert_incr in [1, -1]:
            for horiz_incr in [1, -1]:
                target = Location(row_col=(self.row + vert_incr,
                                           self.col + horiz_incr))
                while target.in_bounds:
                    if own_squares[target.row][target.col]:
                        break
                    yield target
                    if opp_squares[target.row][target.col]:
                        break
                    target = Location(row_col=(target.row + vert_incr,
                                               target.col + horiz_incr))


class Knight(Piece):
    """ Knight class."""
    def __init__(self, location, color, board):
        if color == Color.WHITE:
            symbol = "\N{white chess knight}"
        else:
            symbol = "\N{black chess knight}"
        super().__init__(location, color, board, symbol)

    def move_generator(self):
        """ Return a generator which yields target locations not considering whether
        they would be 'moving into check'"""
        own_squares = self.board.color_pieces(self.color)
        for vert_distance in [1, 2]:
            horiz_distance = vert_distance % 2 + 1
            for vert_direction in [1, -1]:
                for horiz_direction in [1, -1]:
                    target = Location(
                        row_col=(self.row + vert_distance * vert_direction,
                                 self.col + horiz_direction * horiz_distance))
                    if target.in_bounds and not own_squares[target.row][
                            target.col]:
                        yield target


class Pawn(Piece):
    """ Pawn class."""
    def __init__(self, location: Location, color: Color, board):
        if color == Color.WHITE:
            symbol = "\N{white chess pawn}"
            self.starting_row = 6
            self.forward = -1
        else:
            symbol = "\N{black chess pawn}"
            self.starting_row = 1
            self.forward = 1
        super().__init__(location, color, board, symbol)

    def move_generator(self):
        """ Return a generator which yields target locations not considering whether
        they would be 'moving into check'"""
        opp_squares = self.board.color_pieces(Color.other(self.color))
        en_passant_target = self.board.en_passant_target
        if en_passant_target.in_bounds:
            opp_squares[en_passant_target.row][en_passant_target.col] = 1

        one_sqr_fwd = Location(row_col=(self.row + self.forward, self.col))
        if one_sqr_fwd.in_bounds \
                and self.board.board_rep[one_sqr_fwd.row][one_sqr_fwd.col] is Board.empty:
            yield one_sqr_fwd

        two_sqr_fwd = Location(row_col=(self.row + 2 * self.forward, self.col))
        if self.row == self.starting_row \
                and self.board.board_rep[one_sqr_fwd.row][one_sqr_fwd.col] is Board.empty \
                and self.board.board_rep[two_sqr_fwd.row][two_sqr_fwd.col] is Board.empty:
            yield Location(row_col=(self.row + 2 * self.forward, self.col))

        attack_right = Location(row_col=(self.row + self.forward,
                                         self.col + 1))
        if attack_right.in_bounds \
                and opp_squares[attack_right.row][attack_right.col]:
            yield attack_right

        attack_left = Location(row_col=(self.row + self.forward, self.col - 1))
        if attack_left.in_bounds and opp_squares[attack_left.row][
                attack_left.col]:
            yield attack_left


PIECE_TYPES = {
    "r": Rook,
    "n": Knight,
    "b": Bishop,
    "q": Queen,
    "k": King,
    "p": Pawn
}


class IllegalMoveError(Exception):
    """ An error that is raised when illegal moves are attempted."""


def clear_screen():
    """ Clear the screen and move the cursor down 10 lines."""
    #  system("clear")
    for _ in range(9):
        print()


def play(p_0, p_1, print_visuals=True):
    """ Play a game of chess."""
    def next_player(player):
        if player == p_0:
            return p_1
        return p_0

    cur_player = p_0
    board = Board()
    game_over = False
    while not game_over:
        if print_visuals:
            print(board)
            print(f"It is {board.who.name.lower()}'s turn.")
        origin, target = cur_player.move(board)
        try:
            board.make_move(origin, target)
            cur_player = next_player(cur_player)
            if board.has_winner or not any(
                    piece.all_legal_moves for piece in board.color_pieces_flat(
                        board.who)) or board.half_move_clock >= 100:
                game_over = True
            if print_visuals:
                clear_screen()
        except IllegalMoveError as exp:
            if print_visuals:
                clear_screen()
                print(str(exp) + "\n")
        except ValueError as exp:
            if print_visuals:
                clear_screen()
                print(str(exp) + "\n")

    if print_visuals:
        print(board)
    if board.checkmate(Color.WHITE):
        print("Black wins!")
    elif board.checkmate(Color.BLACK):
        print("White wins!")
    else:
        print("Draw.")
