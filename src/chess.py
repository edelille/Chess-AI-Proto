import numpy as np
import itertools


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

            possible_moves = self._find_moves_for_piece(i, piece_type, piece_color)

            print("{}\t{}\t{}\t{}\n".format(i, self._lookup_square(i), piece_color, piece_type))
            print("Possible Moves: ")
            for i in range(len(possible_moves)):
                x = possible_moves[i]
                print("\t[{}]:\t{}\t{}".format(i, x, self._lookup_square(x)))


    def _lookup_square(self, i):
        x = i % X_AXIS
        y = int(i / Y_AXIS)

        return("{}{}".format(_X_MAP[x], _Y_MAP[y]))

    def _rank(self, i):
        return _Y_MAP[int(i / Y_AXIS)]

    def _rank_j(self, i):
        return int(i / Y_AXIS)

    def _file(self, i):
        return _X_MAP[int(i / X_AXIS)]

    def _file_j(self, i):
        return int(i % X_AXIS)

    # checks and returns the piece in the square if found
    def _is_opposite_color(self, i, j):
        return int(self.board.flatten()[i] / 10) != int(self.board.flatten()[j] / 10)

    def _check_square(self, i):
        return self.board.flatten()[i], self.board.flatten()[i] != 0

    def _illegal_move_checker(self, i, j):
        if j < 0:
            return False
        elif self.board.flatten()[j] != 0:
            piece, found = self._check_square(j)
            if self._is_opposite_color(i, j):
                return True
            else:
                return False
        else:
            return True

    # Returns an array of all possible moves in strings
    def _find_moves_for_piece(self, i, ptype, pcolor):
        possible_moves = []
        match ptype:
            case "pawn":
                match pcolor:
                    case "white":
                        if self._rank(i) == "2":
                            possible_moves.append(self._adjust_coord(i, 0, 2))
                        possible_moves.append(self._adjust_coord(i, 0, 1))
                    case "black":
                        if self._rank(i) == "7":
                            possible_moves.append(self._adjust_coord(i, 0, -2))
                        possible_moves.append(self._adjust_coord(i, 0, -1))
            case "knight":
                knight_moves = list(itertools.permutations([-2, -1, 1, 2], r=2))
                for x in knight_moves:
                    if x[0] == x[1] or x[0] == -1*x[1]:
                        continue
                    print(x)
                    possible_moves.append(self._adjust_coord(i, x[0], x[1]))
            case "bishop":
                pass
            case _:
                print("This piece was not implemented yet")
                pass

        # check and declare illegal moves
        possible_moves = list(filter(lambda x: self._illegal_move_checker(i, x), possible_moves))


        return possible_moves

    def _adjust_coord(self, i, adjx, adjy):
        # find current coord, add the adjustments on the board, returning the 
        # index of the square

        # Determine i's actual position
        # position (x, y) = y * x_axis + x
        x = self._file_j(i) + adjx
        y = self._rank_j(i) + adjy

        # Illegal moves
        if x >= X_AXIS or y >= Y_AXIS or x < 0 or y < 0:
            return -1

        return y * X_AXIS + x







def test_chess():
    print("[DEBUG] Testing Chess")

    aChess = Chess()

    aChess.find_moves()

    aChess.show_board()
