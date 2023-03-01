import numpy as np


X_AXIS = 8
Y_AXIS = 8
Z_AXIS = 1
NUM_SQUARES = X_AXIS * Y_AXIS * Z_AXIS
_X_MAP = [ "A", "B", "C", "D", "E", "F", "G", "H" ]
_Y_MAP = [ "1", "2", "3", "4", "5", "6", "7", "8" ]

########## PIECES
_PAWN = 1
_KNIGHT = 3
_BISHOP = 4
_ROOK = 5
_QUEEN = 9
_KING = 8
_PIECE_MAP = [
    None,
    "pawn",
    None,
    "knight",
    "bishop",
    "rook",
    None,
    None,
    "king",
    "queen",
]

_WHITE = 10
_BLACK = 20
_COLOR_MAP = [
    None,
    'white',
    'black',
]

_STARTING_BOARD = np.array([
_ROOK, _KNIGHT, _BISHOP, _QUEEN, _KING, _BISHOP, _KNIGHT, _ROOK,
_PAWN, _PAWN, _PAWN, _PAWN, _PAWN, _PAWN, _PAWN, _PAWN,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
_PAWN, _PAWN, _PAWN, _PAWN, _PAWN, _PAWN, _PAWN, _PAWN,
_ROOK, _KNIGHT, _BISHOP, _QUEEN, _KING, _BISHOP, _KNIGHT, _ROOK
]).reshape(X_AXIS, Y_AXIS)

# Polarize the starting board for white and black pieces
print(_STARTING_BOARD)
_STARTING_BOARD[0] += _WHITE
_STARTING_BOARD[1] += _WHITE
_STARTING_BOARD[-2] += _BLACK
_STARTING_BOARD[-1] += _BLACK

print(_STARTING_BOARD)

# A Chess game, retrieve current moves, current board status, etc.
class Chess():
    def __init__(self, board=None):
        self.board = np.zeros(NUM_SQUARES).reshape(X_AXIS, Y_AXIS)

        if board is None:
            self.setup_board()

    # Returns an array of all possible moves in strings
    def possible_moves(self):
        print("nothing to do yet")

    def setup_board(self):
        self.board = _STARTING_BOARD

    def show_board(self):
        print(self.board)

    # Return all possible moves
    def find_moves(self):
        possible_moves = []

        flattened_board = self.board.flatten()
        for i, x in enumerate(flattened_board):
            if x == 0:
                continue

            piece_type = _PIECE_MAP[x % 10]
            piece_color = _COLOR_MAP[int(x / 10)]

            self._find_moves_for_piece(i, piece_type, piece_color)

            print("{}\t{}\t{}\t{}\n".format(i, self._lookup_square(i), piece_color, piece_type))

    def _lookup_square(self, i):
        x = i % X_AXIS
        y = int(i / Y_AXIS)

        return("{}{}".format(_X_MAP[x], _Y_MAP[y]))

    def _rank(self, i):
        return _Y_MAP[int(i / Y_AXIS)]

    def _file(self, i):
        return _X_MAP[int(i / X_AXIS)]

    def _find_moves_for_piece(self, i, ptype, pcolor):

        match ptype:
            case "pawn":
                print("Current square: {}".format(i))
                match pcolor:
                    case "white":
                        if self._rank(i) == "2":
                            print("Pawn on second rank")
                        pass
                    case "black":
                        if self._rank(i) == "7":
                            print("Pawn on seventh rank")
                        pass
                    case _:
                        print("This color was not implemented yet")
            case _:
                print("This piece was not implemented yet")

    def _adjust_coord(i, adjx, adjy):
        # find current coord, add the adjustments on


def test_chess():
    print("[DEBUG] Testing Chess")

    aChess = Chess()

    aChess.show_board()

    aChess.find_moves()
