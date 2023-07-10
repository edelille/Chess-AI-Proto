package main

import "fmt"

const (
	BOARD_SIZE = 8
)

var (
	STARTING_BOARD [][]Piece

	PAWN = PieceType{
		ToIcon: "P",
	}
	KNIGHT = PieceType{
		ToIcon: "N",
	}
	BISHOP = PieceType{
		ToIcon: "B",
	}
	ROOK = PieceType{
		ToIcon: "R",
	}
	QUEEN = PieceType{
		ToIcon: "Q",
	}
	KING = PieceType{
		ToIcon: "K",
	}
	KNIGHT_MOVES = []Position{
		{-2, 1},
		{-2, -1},
		{2, -1},
		{2, 1},
		{1, 2},
		{1, -2},
		{-1, 2},
		{-1, -2},
	}

	DIAGONALS = []Position{
		{1, 1}, {1, -1}, {-1, 1}, {-1, -1},
	}
	ORTHOGONALS = []Position{
		{1, 0}, {-1, 0}, {0, 1}, {0, -1},
	}
)

type PieceType struct {
	ToIcon string
}

type Piece struct {
	Type  PieceType
	Color byte
	Empty bool
}

type PiecePosition struct {
	Piece    Piece
	Position Position
	Move     Position
	Capture  bool
}

func (p *PiecePosition) ToCoords() string {
	capture := ""
	if p.Capture {
		capture = "x"
	}

	if p.Piece.Type == PAWN {
		if p.Capture {
			return fmt.Sprintf("%s%s%s%d",
				string(int('A'+p.Position.j)),
				capture,
				string(int('a'+p.Move.j)),
				p.Move.i+1,
			)
		}
		return fmt.Sprintf("%s%d", string(int('a'+p.Move.j)), p.Move.i+1)
	}

	return fmt.Sprintf("%s%s%s%d", p.Piece.Type.ToIcon, capture, string(int('a'+p.Move.j)), p.Move.i+1)
}

type Position struct {
	i int
	j int
}

func (p *Position) ToCoords() string {
	return fmt.Sprintf("%s%d", string(int('A'+p.j)), p.i+1)
}

type ChessGame struct {
	Board       [][]Piece
	ColorToMove byte

	n, m          int
	enPassantFlag int
}

func NewChessGame() *ChessGame {
	return &ChessGame{
		Board:       STARTING_BOARD,
		ColorToMove: 'w',
		n:           len(STARTING_BOARD),
		m:           len(STARTING_BOARD[0]),
	}
}

func (c *ChessGame) PrintBoard() {
	for i := c.n - 1; i >= 0; i-- {
		for j := 0; j < c.m; j++ {
			piece := c.Board[i][j]
			if piece.Empty {
				fmt.Printf("   ")
			} else {
				fmt.Printf(string(piece.Color) + piece.Type.ToIcon + " ")
			}
		}
		fmt.Printf("\n")
	}
}

func (c *ChessGame) printThisBoard(board [][]Piece) {
	for i := c.n - 1; i >= 0; i-- {
		for j := 0; j < c.m; j++ {
			piece := board[i][j]
			if piece.Empty {
				fmt.Printf("  ")
			} else {
				fmt.Printf(piece.Type.ToIcon + " ")
			}
		}
		fmt.Printf("\n")
	}
}

func (c *ChessGame) getAllPieces(board [][]Piece, d byte) []PiecePosition {
	res := []PiecePosition{}
	for i := 0; i < c.n; i++ {
		for j := 0; j < c.m; j++ {
			if !board[i][j].Empty && board[i][j].Color == d {
				res = append(res, PiecePosition{Piece: c.Board[i][j], Position: Position{i, j}})
			}
		}
	}
	return res
}

func (c *ChessGame) getPossibleMoves(board [][]Piece, d byte) []PiecePosition {
	pieces := c.getAllPieces(board, d)

	pre, res := []PiecePosition{}, []PiecePosition{}
	for _, x := range pieces {
		pre = append(pre, c.getMoves(board, x)...)
	}

	for _, x := range pre {
		if c.peekBoard(x) {
			res = append(res, x)
		}
	}

	return res
}

func (c *ChessGame) getMoves(board [][]Piece, p PiecePosition) []PiecePosition {
	res := []PiecePosition{}

	piece, color, position, i, j := p.Piece, p.Piece.Color, p.Position, p.Position.i, p.Position.j

	switch p.Piece.Type {
	case PAWN:
		if color == 'w' {
			if i == 1 && c.peekMove(board, color, i+2, j, true) {
				res = append(res, PiecePosition{piece, position, Position{i + 2, j}, false})
			}
			if c.peekMove(board, color, i+1, j, true) {
				res = append(res, PiecePosition{piece, position, Position{i + 1, j}, false})
			}
			if c.peekMoveMustCapture(board, color, i+1, j+1) {
				res = append(res, PiecePosition{piece, position, Position{i + 1, j + 1}, true})
			}
			if c.peekMoveMustCapture(board, color, i+1, j-1) {
				res = append(res, PiecePosition{piece, position, Position{i + 1, j - 1}, true})
			}
			if i == 4 && abs(j-c.enPassantFlag) == 1 {
				res = append(res, PiecePosition{piece, position, Position{i + 1, c.enPassantFlag}, true})
			}
		} else {
			if i == 6 && c.peekMove(board, color, i-2, j, true) {
				res = append(res, PiecePosition{piece, position, Position{i - 2, j}, false})
			}
			if c.peekMove(board, color, i-1, j, true) {
				res = append(res, PiecePosition{piece, position, Position{i - 1, j}, false})
			}
			if c.peekMoveMustCapture(board, color, i-1, j+1) {
				res = append(res, PiecePosition{piece, position, Position{i - 1, j + 1}, true})
			}
			if c.peekMoveMustCapture(board, color, i-1, j-1) {
				res = append(res, PiecePosition{piece, position, Position{i - 1, j - 1}, true})
			}
			if i == 3 && abs(j-c.enPassantFlag) == 1 {
				res = append(res, PiecePosition{piece, position, Position{i - 1, c.enPassantFlag}, true})
			}
		}
	case KNIGHT:
		for _, x := range KNIGHT_MOVES {
			if c.peekMove(board, color, i+x.i, j+x.j, false) {
				res = append(res, PiecePosition{piece, position, Position{i + x.i, j + x.j}, false})
			}
		}
	case BISHOP:
		for _, x := range DIAGONALS {
			res = append(res, c.getLinearMoves(board, piece, i, j, x.i, x.j)...)
		}
	case ROOK:
		for _, x := range ORTHOGONALS {
			res = append(res, c.getLinearMoves(board, piece, i, j, x.i, x.j)...)
		}
	case QUEEN:
		for _, x := range append(DIAGONALS, ORTHOGONALS...) {
			res = append(res, c.getLinearMoves(board, piece, i, j, x.i, x.j)...)
		}
	case KING:
		for _, x := range append(DIAGONALS, ORTHOGONALS...) {
			if c.peekMove(board, color, i+x.i, j+x.j, false) {
				res = append(res, PiecePosition{
					piece,
					position,
					Position{i + x.i, j + x.j},
					c.isCapture(board, color, i+x.i, j+x.j),
				})
			}
		}
	}

	return res
}

func (c *ChessGame) getLinearMoves(board [][]Piece, piece Piece, i, j, k, l int) []PiecePosition {
	res := []PiecePosition{}
	start := Position{i, j}
	i, j = i+k, j+l
	for i >= 0 && i < c.n && j >= 0 && j < c.m && (board[i][j].Empty || board[i][j].Color != piece.Color) {
		if !board[i][j].Empty && c.isCapture(board, piece.Color, i, j) {
			res = append(res, PiecePosition{piece, start, Position{i, j}, true})
			break
		}
		res = append(res, PiecePosition{piece, start, Position{i, j}, false})

		i += k
		j += l
	}

	return res
}

func (c *ChessGame) getLinearLimit(board [][]Piece, piece Piece, i, j, k, l int) Position {
	i, j = i, j
	for i+k >= 0 && i+k < c.n && j+l >= 0 && j+l < c.m &&
		(c.Board[i+k][j+l].Empty || c.Board[i+k][j+l].Color != piece.Color) {
		i += k
		j += l
		if c.isCapture(board, piece.Color, i, j) {
			break
		}
	}

	return Position{i, j}
}

// returns true if the board is a legal position
func (c *ChessGame) peekBoard(p PiecePosition) bool {
	tempBoard := make([][]Piece, c.n)
	for i, x := range c.Board {
		tempBoard[i] = make([]Piece, c.m)
		copy(tempBoard[i], x)
	}

	piece, color := p.Piece, p.Piece.Color

	from, to := p.Position, p.Move
	tempBoard[to.i][to.j] = tempBoard[from.i][from.j]
	tempBoard[from.i][from.j] = Piece{Empty: true}

	// find the king
	var kp Position
	for i := 0; i < c.n; i++ {
		for j := 0; j < c.m; j++ {
			if tempBoard[i][j].Type == KING && tempBoard[i][j].Color == c.ColorToMove {
				kp = Position{i, j}
				break
			}
		}
	}

	// Check king safety
	for _, x := range ORTHOGONALS { // check orthoganals!
		ll := c.getLinearLimit(tempBoard, piece, kp.i, kp.j, x.i, x.j)
		adj := (abs(kp.i-ll.i) < 2) && (abs(kp.j-ll.j) < 2)
		sq := tempBoard[ll.i][ll.j]
		enemy := c.isCapture(tempBoard, color, ll.i, ll.j)
		atk := sq.Type
		if enemy && (adj && atk == KING) || atk == ROOK || atk == QUEEN {
			return false
		}
	}
	for _, x := range DIAGONALS {
		ll := c.getLinearLimit(tempBoard, piece, kp.i, kp.j, x.i, x.j)
		adj := (abs(kp.i-ll.i) < 2) && (abs(kp.j-ll.j) < 2)
		sq := tempBoard[ll.i][ll.j]
		enemy := c.isCapture(tempBoard, color, ll.i, ll.j)
		atk := sq.Type
		if enemy && (adj && atk == KING) || atk == BISHOP || atk == QUEEN {
			return false
		}
		// Pawn checks
		if enemy && (adj && atk == PAWN) &&
			((color == 'w' && ll.i > kp.i) || (color == 'b' && ll.i < kp.i)) {
			return false
		}
	}
	for _, x := range KNIGHT_MOVES {
		ksi, ksj := kp.i+x.i, kp.j+x.j
		if ksi < 0 || ksi >= c.n || ksj < 0 || ksj >= c.m {
			continue
		}
		atk := tempBoard[ksi][ksj].Type
		enemy := c.isCapture(tempBoard, color, ksi, ksj)
		if enemy && atk == KNIGHT {
			return false
		}
	}

	return true
}

func (c *ChessGame) peekMove(board [][]Piece, color byte, i, j int, noCapture bool) bool {
	if i < 0 || j < 0 || i >= c.n || j >= c.m {
		return false
	}

	if board[i][j].Empty || (!noCapture && board[i][j].Color != color) {
		return true
	}

	return false
}

func (c *ChessGame) peekMoveMustCapture(board [][]Piece, color byte, i, j int) bool {
	if i < 0 || j < 0 || i >= c.n || j >= c.m || board[i][j].Empty || board[i][j].Color == color {
		return false
	}

	return true

}

func (c *ChessGame) isCapture(board [][]Piece, color byte, i, j int) bool {
	return !board[i][j].Empty &&
		(board[i][j].Color == 'w' && color == 'b' ||
			board[i][j].Color == 'b' && color == 'w')
}

func (c *ChessGame) Move(s string) {
	moves := c.getPossibleMoves(c.Board, c.ColorToMove)

	var move PiecePosition
	found := false
	for _, x := range moves {
		if x.ToCoords() == s {
			move = x
			found = true
		}
	}
	if !found {
		return
	}

	c.doMove(move)
	if c.ColorToMove == 'w' {
		if s[1] == '4' {
			c.enPassantFlag = 7 - int('h'-s[0])
			fmt.Println("En Passant potentially possible from white: ", c.enPassantFlag)
		} else {
			c.enPassantFlag = -2
		}
		c.ColorToMove = 'b'
	} else {
		if s[1] == '5' {
			c.enPassantFlag = 7 - int('h'-s[0])
			fmt.Println("En Passant potentially possible from black: ", c.enPassantFlag)
		} else {
			c.enPassantFlag = -2
		}
		c.ColorToMove = 'w'
	}

	if len(c.getPossibleMoves(c.Board, c.ColorToMove)) == 0 {
		c.exitGame()
	}
}

func (c *ChessGame) exitGame() {
	c.PrintBoard()
	fmt.Printf("\nGame has ended, %s has no more moves\n\n", string(c.ColorToMove))
}

func (c *ChessGame) doMove(p PiecePosition) {
	color, pType, from, to := p.Piece.Color, p.Piece.Type, p.Position, p.Move

	// Catch case on en passant
	if pType == PAWN && ((color == 'w' && from.i == 4) || (color == 'b' && from.i == 3)) &&
		to.j == c.enPassantFlag {
		c.Board[to.i][to.j] = c.Board[from.i][from.j]
		c.Board[from.i][from.j] = Piece{Empty: true}
		c.Board[from.i][to.j] = Piece{Empty: true}
		c.enPassantFlag = -2
		return
	}

	c.Board[to.i][to.j] = c.Board[from.i][from.j]
	c.Board[from.i][from.j] = Piece{Empty: true}
}

func testChess() {
	fmt.Println("This is the testing chess main routine\n")

	game := NewChessGame()

	/*
		scholarsMate := []string{
			"E4",
			"E5",
			"Bc4",
			"A6",
			"Qf3",
			"B6",
			"Qxf7",
		}

		pawnCheckmate := []string{
			"h4",
			"g5",
			"Hxg5",
			"Na6",
			"g6",
			"Nb8",
			"e4",
			"Na6",
			"Bc4",
			"Nb8",
			"Gxf7",
		}
	*/

	enPassant := []string{
		"e4",
		"a5",
		"e5",
		"f5",
		"Exf6",
		"a4",
		"b4",
		"Axb3",
	}

	testMoves := enPassant

	for _, x := range testMoves {
		game.Move(x)
	}

	moves := game.getPossibleMoves(game.Board, game.ColorToMove)
	debugPrintMoves(moves)
	game.PrintBoard()
}
