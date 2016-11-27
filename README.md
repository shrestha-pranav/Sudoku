#Sudoku

Implementation of a Python class to solve 9x9 Sudoku grids.

API:

1. Sudoku(string) - Constructor creates a new Sudoku object  
	  -string is a 81 character string with empty cells represented as 0
2. Sudoku(grid) - Constructor creates a new Sudoku object  
	  -grid is a 9x9 list, each cell representing element in each inner list
3. grid.printGrid() - prints the Sudoku object 'grid'
4. grid.solveGrid() - solves the Sudoku object 'grid'

Algorithm used: Backtracking

Systematically checks through every possible combination, and "backtracks"
once it finds an "invalid" configuration. 

- Starts from first cell, and traverses through columns then rows. 
- If the cell if filled, continue on to next empty cell.
- If cell is not filled(0):
      - Try out first value(1)
      - If valid, check the next cell
      - If invalid, try the next value(2)
      - If every value(1-9) is invalid, consider the previous cell invalid.
