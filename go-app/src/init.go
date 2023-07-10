package main

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
