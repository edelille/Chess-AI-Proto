package main

import "fmt"

func debugPrintMoves(arr []PiecePosition) {
	if len(arr) == 0 {
		fmt.Println("No moves to print")
		return
	}

	lastLetter := arr[0].ToCoords()[0]
	for i, x := range arr {
		y := x.ToCoords()
		if y[0] != lastLetter || i == 0 {
			fmt.Printf("\n")
			lastLetter = y[0]
		} else {
			fmt.Printf(", ")
		}
		fmt.Printf("%s", y)
	}
	fmt.Println()
}
