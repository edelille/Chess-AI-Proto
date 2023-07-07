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
}

func (p *PiecePosition) ToCoords() string {
	if p.Piece.Type == PAWN {
		return fmt.Sprintf("%s%d", string(int('A'+p.Move.j)), p.Move.i+1)
	}

	return fmt.Sprintf("%s%s%d", p.Piece.Type.ToIcon, string(int('a'+p.Move.j)), p.Move.i+1)
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

	n, m int
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
	n, m := len(c.Board), len(c.Board[0])

	for i := n - 1; i >= 0; i-- {
		for j := 0; j < m; j++ {
			piece := c.Board[i][j]
			if piece.Empty {
				fmt.Printf("  ")
			} else {
				fmt.Printf(piece.Type.ToIcon + " ")
			}
		}
		fmt.Printf("\n")
	}
}

func (c *ChessGame) getAllPieces(d byte) []PiecePosition {
	res := []PiecePosition{}
	n, m := len(c.Board), len(c.Board[0])

	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			if !c.Board[i][j].Empty && c.Board[i][j].Color == d {
				res = append(res, PiecePosition{c.Board[i][j], Position{i, j}, Position{}})
			}
		}
	}
	return res
}

func (c *ChessGame) getPossibleMoves(d byte) []PiecePosition {
	pieces := c.getAllPieces(d)

	res := []PiecePosition{}
	for _, x := range pieces {
		res = append(res, c.getMoves(x)...)
	}

	return res
}

func (c *ChessGame) getMoves(p PiecePosition) []PiecePosition {
	res := []PiecePosition{}

	piece, color, position, i, j := p.Piece, p.Piece.Color, p.Position, p.Position.i, p.Position.j

	switch p.Piece.Type {
	case PAWN:
		if color == 'w' {
			if i == 1 && c.peekMove(color, i+2, j) {
				res = append(res, PiecePosition{piece, position, Position{i + 2, j}})
			}
			if c.peekMove(color, i+1, j) {
				res = append(res, PiecePosition{piece, position, Position{i + 1, j}})
			}
		} else {
			if i == 1 && c.peekMove(color, i-2, j) {
				res = append(res, PiecePosition{piece, position, Position{i - 2, j}})
			}
			if c.peekMove(color, i-1, j) {
				res = append(res, PiecePosition{piece, position, Position{i - 1, j}})
			}
		}
	case KNIGHT:
		knightMoves := []Position{
			{-2, 1},
			{-2, -1},
			{2, -1},
			{2, 1},
			{1, 2},
			{1, -2},
			{-1, 2},
			{-1, -2},
		}
		for _, x := range knightMoves {
			if c.peekMove(color, i+x.i, j+x.j) {
				res = append(res, PiecePosition{piece, position, Position{i + x.i, j + x.j}})
			}
		}
	case BISHOP:
		res = append(res, c.getLinearMoves(piece, i, j, 1, 1)...)
		res = append(res, c.getLinearMoves(piece, i, j, 1, -1)...)
		res = append(res, c.getLinearMoves(piece, i, j, -1, 1)...)
		res = append(res, c.getLinearMoves(piece, i, j, -1, -1)...)
	}

	return res
}

func (c *ChessGame) getLinearMoves(piece Piece, i, j, k, l int) []PiecePosition {
	res := []PiecePosition{}
	start := Position{i, j}
	i, j = i+k, j+l
	for i >= 0 && i < c.n && j >= 0 && j < c.m && (c.Board[i][j].Empty || c.Board[i][j].Color != piece.Color) {
		res = append(res, PiecePosition{piece, start, Position{i, j}})
		i += k
		j += l
	}

	return res
}

func (c *ChessGame) peekMove(color byte, i, j int) bool {
	n, m := len(c.Board), len(c.Board[0])
	if i < 0 || j < 0 || i >= n || j >= m {
		return false
	}

	if c.Board[i][j].Empty || c.Board[i][j].Color != color {
		return true
	}

	return false
}

func (c *ChessGame) Move(s string) {
	moves := c.getPossibleMoves(c.ColorToMove)

	for _, x := range moves {
		if x.ToCoords() == s {
			c.doMove(x.Position, x.Move)
			if c.ColorToMove == 'w' {
				c.ColorToMove = 'b'
			} else {
				c.ColorToMove = 'w'
			}
			return
		}
	}

	fmt.Println("Nothing was moved :/")

}

func (c *ChessGame) doMove(from, to Position) {
	c.Board[to.i][to.j] = c.Board[from.i][from.j]
	c.Board[from.i][from.j] = Piece{Empty: true}
}

func init() {
	// Board Size
	n, m := BOARD_SIZE, BOARD_SIZE
	STARTING_BOARD = make([][]Piece, n)
	for i := 0; i < n; i++ {
		STARTING_BOARD[i] = make([]Piece, m)
	}

	// Initialize the starting board position
	for i := 0; i < n; i++ {

		piece := Piece{
			Empty: true,
		}

		piece.Color = 'w'
		if i > n/2 {
			piece.Color = 'b'
		}

		for j := 0; j < m; j++ {
			switch i {
			case 0, n - 1:
				piece.Empty = false
				switch j {
				case 0, m - 1:
					piece.Type = ROOK
				case 1, m - 2:
					piece.Type = KNIGHT
				case 2, m - 3:
					piece.Type = BISHOP
				case 3:
					piece.Type = QUEEN
				case 4:
					piece.Type = KING
				}
			case 1, n - 2:
				piece.Empty = false
				piece.Type = PAWN
			}
			STARTING_BOARD[i][j] = piece
		}
	}
}

func testChess() {
	fmt.Println("This is the testing chess main routine\n")

	game := NewChessGame()

	testMoves := []string{
		"E4",
		"E5",
		"Bc4",
	}

	for _, x := range testMoves {
		game.Move(x)
	}

	game.PrintBoard()

	moves := game.getPossibleMoves('w')

	for _, x := range moves {
		fmt.Println(x.ToCoords())
	}

}
