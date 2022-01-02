# Chess
A chess engine written in python. To play the game on the command line, run `python3 cli.py`.


##
TODO:
  - add memoization for piece.all legal moves
  - make Board.check(color) more efficient, search outwards from the king's location as opposed to checking if any pieces can reach the king's loction


###
Known Issues:
  - The 50 move draw rule is implemented so that after 50 moves with no pawn movement and no captures, the game automatically ends in a draw. The official rules of chess permit claiming of a draw by either player, but the draw is not automatic.
  - The three-fold and five-fold repetition rules are ignored in this implementation of chess.
