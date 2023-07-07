import numpy as np
import itertools


X_AXIS = 8
Y_AXIS = 8
Z_AXIS = 1
NUM_SQUARES = X_AXIS * Y_AXIS * Z_AXIS
_X_MAP = [ "A", "B", "C", "D", "E", "F", "G", "H" ]
_X_MAP_INV = { "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
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
_STARTING_BOARD[0] += _WHITE
_STARTING_BOARD[1] += _WHITE
_STARTING_BOARD[-2] += _BLACK
_STARTING_BOARD[-1] += _BLACK

# A Chess game, retrieve current moves, current board status, etc.
class Chess():
    def __init__(self, board=None):
        self.board = np.zeros(NUM_SQUARES).reshape(X_AXIS, Y_AXIS)
        self.whiteTurn = True
        self.moveHistory = []
        self.boardHistory = []

        if board is None:
            self.setup_board()

    def setup_board(self):
        self.board = _STARTING_BOARD

    def show_board(self, board=None):
        # First reverse the chess board to print from the other side
        tgtBoard = self.board if board is None else board
        for x in reversed(tgtBoard):
            print("\t".join(str(y) for y in x))


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

            for i in range(len(possible_moves)):
                x = possible_moves[i]

    # receive a move command like: "1. >E4<" and plays the move
    def move(self, mstr):
        print("Attempting to move {}".format(mstr))
        moves = self._find_moves_for_color("white" if self.whiteTurn else "black")
        flat_board = self.board.flatten()
        if mstr not in moves:
            print("[ERROR] move was invalid: {}".format(mstr))
            print("White's turn?: ", self.whiteTurn)
            print("all moves: ", moves) #[self._lookup_square(x) for x in moves])
            self.whiteTurn = not self.whiteTurn
            return False


        match len(mstr):
            case 2: # anything here is a valid pawn move
                tgtI = self._lookup_i(mstr)
                found = False
                testI = tgtI
                while not found:
                    testI = self._adjust_coord(testI, 0, -1 if self.whiteTurn else 1)
                    _, found = self._check_square(testI)
                self._move_piece(testI, tgtI)
            case 3: # Any other piece simple without captures
                pieceClass = mstr[0]
                pieceSquare = mstr[1:]
                tgtI = self._lookup_i(pieceSquare)

                match pieceClass:
                    case "N":
                        # Check all possible knight moves for same color knight, then move it
                        possible_moves = self._find_knight_moves(tgtI)
                        target = _KNIGHT + (_WHITE if self.whiteTurn else _BLACK)
                        for x in possible_moves:
                            if flat_board[x] == target:
                                self._move_piece(x, tgtI)
                                break
                    case "B":
                        # Find the Bishop
                        pOfB = tgtI % 2
                        target = _BISHOP + (_WHITE if self.whiteTurn else _BLACK)
                        i = next(i for i,v in enumerate(flat_board) if v == target and i % 2 != pOfB)
                        self._move_piece(i, tgtI)
                    case "R":
                        target = _ROOK + (_WHITE if self.whiteTurn else _BLACK)
                        it = (i for i,v in enumerate(flat_board) if v == target)
                        i = next(it)
                        while tgtI not in self._find_rook_moves(i):
                            i = next(it)
                        self._move_piece(i, tgtI)
                    case "Q":
                        target = _QUEEN + (_WHITE if self.whiteTurn else _BLACK)
                        it = (i for i,v in enumerate(flat_board) if v == target)
                        i = next(it)
                        while tgtI not in self._find_queen_moves(i):
                            i = next(it)
                        self._move_piece(i, tgtI)
                    case _:
                        print("This piece was not implemented yet")
            case 4:
                # Usually a capture?
            case _:
                print("invalid move length, must be between 2-5")
                return

        self.moveHistory.append(mstr)
        self.boardHistory.append(self.board)
        self.whiteTurn = not self.whiteTurn

        enemyMoves = self._find_moves_for_color("white" if self.whiteTurn else "black")

        # Catch for checkmate and stalemate
        if len(enemyMoves) == 0:
            # check for checkmate first
            if self._illegal_board_checker(0, 0):
                print("This is just stalemate :)")
                return
            else:
                self._enter_checkmate()
                return

    def _move_piece(self, fromI, toI, test=False):
        tempBoard = self.board.copy()

        fromX = fromI % X_AXIS
        fromY = int((fromI - fromX)/Y_AXIS)
        toX = toI % X_AXIS
        toY = int((toI - toX)/Y_AXIS)

        tempBoard[toY][toX] = tempBoard[fromY][fromX]
        tempBoard[fromY][fromX] = 0

        if not test:
            self.board = tempBoard.copy()

        return tempBoard

    def _lookup_square(self, i):
        x = i % X_AXIS
        y = int(i / Y_AXIS)

        return("{}{}".format(_X_MAP[x], _Y_MAP[y]))

    def _lookup_i(self, square):
        x = _X_MAP_INV[square[0].upper()]
        y = int(square[1]) - 1
        return y * X_AXIS + x

    def _translate_move(self, ptype, i):
        match ptype:
            case "pawn":
                if False:
                    return ""
                else:
                    return self._lookup_square(i)
            case "knight":
                if False: # all special cases
                    return ""
                else:
                    return "N" + self._lookup_square(i).lower()
            case "bishop":
                if False:
                    return ""
                else:
                    return "B" + self._lookup_square(i).lower()
            case "rook":
                if False:
                    return ""
                else:
                    return "R" + self._lookup_square(i).lower()
            case "queen":
                if False:
                    return ""
                else:
                    return "Q" + self._lookup_square(i).lower()
            case "king":
                if False:
                    return ""
                else:
                    return "K" + self._lookup_square(i).lower()
            case _:
                print("This piece was not implemented yet")
                pass

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
        if j < 0 or i == j:
            return False
        elif not self._illegal_board_checker(i, j):
            return False
        elif self.board.flatten()[j] != 0:
            piece, found = self._check_square(j)
            if self._is_opposite_color(i, j):
                return True
            else:
                return False
        else:
            return True

    def _boundary_move_checker(self, i, j, altColor=False):
        if j < 0 or i == j:
            return False
        elif self.board.flatten()[j] != 0:
            piece, found = self._check_square(j)
            if self._is_opposite_color(i, j):
                return False if altColor else True
            else:
                return True if altColor else False
        else:
            return True

    def _illegal_board_checker(self, i, j):
        testBoard = self._move_piece(i, j, test=True)
        flat_testBoard = testBoard.flatten()

        # check if the king is within attacking distance of enemy players
        tgtKing = _KING + (_WHITE if self.whiteTurn else _BLACK)
        # Find the King
        whereKing = np.where(flat_testBoard == tgtKing)
        if len(whereKing[0]) == 0: # king is not found, return false
            return False
        tgtI = whereKing[0][0]

        enemyColor = _BLACK if self.whiteTurn else _WHITE

        # Find all the knights first
        nMoves = self._find_knight_moves(tgtI, altColor=True)
        tgtKnight = _KNIGHT + enemyColor
        for x in nMoves:
            if flat_testBoard[x] == tgtKnight:
                return False

        # Find all straight viewers
        tgtQueen = _QUEEN + enemyColor
        tgtRook = _ROOK + enemyColor
        rMoves = self._find_rook_moves(tgtI, altColor=True)
        for x in rMoves:
            if flat_testBoard[x] in [tgtQueen, tgtRook]:
                return False

        # Find all diagonal viewers
        tgtBishop = _BISHOP + enemyColor
        bMoves = self._find_bishop_moves(tgtI, altColor=True)
        for x in bMoves:
            if flat_testBoard[x] in [tgtQueen, tgtBishop]:
                return False

        # Find all direct touchers now
        tgtPawn = _PAWN + enemyColor
        tgtKing = _PAWN + enemyColor
        kMoves = self._find_king_moves(tgtI, altColor=True)
        for x in kMoves:
            if flat_testBoard[x] in [tgtQueen, tgtBishop]:
                return False

        return True

    def _find_moves_for_color(self, color):
        move_list = []
        piece_list = []
        flat_board = self.board.flatten()

        match color:
            case "white":
                for i in range(len(flat_board)):
                    x = flat_board[i]
                    piece_type = _PIECE_MAP[x % 10]
                    if int(x / 10) * 10 == _WHITE:
                        moves = self._find_moves_for_piece(i, piece_type, color)
                        piece_list.append({
                            "square": self._lookup_square(i),
                            "piece": piece_type,
                            "moves": moves,
                        })
            case "black":
                for i in range(len(flat_board)):
                    x = flat_board[i]
                    piece_type = _PIECE_MAP[x % 10]
                    if int(x / 10) * 10 == _BLACK:
                        moves = self._find_moves_for_piece(i, piece_type, color)
                        piece_list.append({
                            "square": self._lookup_square(i),
                            "piece": piece_type,
                            "moves": moves,
                        })
            case _:
                print("This color has not been implemented yet")

        for x in piece_list:
            debug=False #x['piece'] == 'king'
            if debug:
                print("\tpiece: {}".format(x["piece"]))
                print("\tsquare: {}".format(x["square"]))
                if len(x["moves"]) > 0:
                    print("\tmoves:")
            for y in x["moves"]:
                if debug:
                    print("\t\t{}".format(self._translate_move(x["piece"], y)))
                move_list.append(self._translate_move(x["piece"], y))

        return move_list

    # Returns an array of all possible moves in strings
    def _find_moves_for_piece(self, i, ptype, pcolor):
        possible_moves = []
        flat_board = self.board.flatten()
        match ptype:
            case "pawn":
                possible_moves = self._find_pawn_moves(i)
            case "knight":
                possible_moves = self._find_knight_moves(i)
            case "bishop":
                possible_moves = self._find_bishop_moves(i)
            case "rook":
                possible_moves = self._find_rook_moves(i)
            case "queen":
                possible_moves = self._find_queen_moves(i)
            case "king":
                possible_moves = self._find_king_moves(i)
            case _:
                print("The {} was not implemented yet".format(ptype))
                pass

        # check and declare illegal moves
        possible_moves = list(filter(lambda x: self._illegal_move_checker(i, x), possible_moves))

        return possible_moves

    def _find_pawn_moves(self, i, altColor=False):
        moves = []
        direction = 0

        # Now check squares in front and to the diagonals, including the first move
        if self.whiteTurn:
            if self._rank(i) == "2":
                moves.append(self._adjust_coord(i, 0, 2))
            direction = 1
        else:
            if self._rank(i) == "7":
                moves.append(self._adjust_coord(i, 0, -2))
            direction = -1
        nMoves = [(-1, direction), (0, direction), (1, direction)]
        for x in nMoves:
            moves.append(self._adjust_coord(i, x[0], x[1]))

        return moves

    def _find_knight_moves(self,i, altColor=False):
        moves = []
        knight_moves = list(itertools.permutations([-2, -1, 1, 2], r=2))
        for x in knight_moves:
            if x[0] == x[1] or x[0] == -1*x[1]:
                continue
            moves.append(self._adjust_coord(i, x[0], x[1]))
        return moves

    def _find_bishop_moves(self, i, altColor=False):
        moves = []
        directions = list(itertools.product([1, -1], repeat=2))
        for x in directions:
            j = 1
            while True:
                tgtI = self._adjust_coord(i, j * x[0], j * x[1])
                if tgtI < 0:
                    break
                if self._boundary_move_checker(i, tgtI, altColor=altColor):
                    moves.append(tgtI)
                else:
                    break
                j += 1
        return moves

    def _find_rook_moves(self, i, altColor=False):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for x in directions:
            j = 1
            while True:
                tgtI = self._adjust_coord(i, j * x[0], j * x[1])
                if tgtI < 0:
                    break
                if self._boundary_move_checker(i, tgtI):
                    moves.append(tgtI)
                else:
                    break
                j += 1
        return moves

    def _find_queen_moves(self, i, altColor=False):
        return self._find_rook_moves(i) + self._find_bishop_moves(i)

    def _find_king_moves(self, i, altColor=False):
        moves = []
        directions = list(itertools.product([-1, 0, 1], repeat=2))
        for x in directions:
            tgtI = self._adjust_coord(i, x[0], x[1])
            if tgtI < 0:
                continue
            if self._boundary_move_checker(i, tgtI):
                moves.append(tgtI)
        return moves

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

    def _enter_checkmate(self):
        losingColor = "white" if self.whiteTurn else "black"
        winningColor = "black" if self.whiteTurn else "white"
        print("This is checkmate on the {} position".format(losingColor))
        print("Congratulations to {}".format(winningColor))

def test_chess():
    print("[DEBUG] Testing Chess")

    aChess = Chess()

    scholars_mate = [
        "E4",
        "E5",
        "Bc4",
        "Nc6",
        "Qf3",
        "D6",
        "Nc3",
        "H6",
        "Qf7",
    ]

    pawn_captures = [
        "D4",
        "E5",
        "E5"
    ]

    #line = scholars_mate
    line = pawn_captures

    for x in line:
        aChess.move(x)

    aChess.show_board()
