#Sudoku

A simple program to solve 9x9 Sudoku grids.
Algorithm used: Backtracking using arc-consistency

Systematically checks through every possible combination, and "backtracks"
once it finds an "invalid" configuration. The next cell is chosen using a
minimum value heuristic.

- The cell with the least number of possibilities is first chosen.
- Each possibility is tried out iteratively until correct solution is found.
- Each time a possibility is tried
	- The value is removed from all of the cell's neighbors.
	- If any of the removal causes another value to be set, the process is repeated recursively.
- The next cell is then chosen in the same method until the board has been solved.