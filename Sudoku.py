#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
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

@author: Pranav Shrestha
"""

import sys
from time import time
import numpy as np

start = time()

# List of global variables for execution
out_filename = 'output.txt'
src_filename = 'sudoku_grids.txt'

# Generate a dictionary of each cell's neighbors [20 each]
neighbors = {
    i : set(
        range(i/9*9, i/9*9 + 9) +               # Generate row neighbors
        range(i%9, 81, 9) +                     # Generate column neighbors
        [9*(i/27*3 + k/3) + i%9/3*3 + k%3 for k in range(9)] # 3x3 neighbors
    ).difference(set([i])) # Remove this cell
    
    for i in range(81)}

# Helper dicitonaries to improve runtime efficiency
# Mapping of each 9-bit int to a set of digits 001101101->(1,3,4,6,7)
hasher = {i:set([j+1 for j in range(9) if (i>>j)%2]) for i in range(512)}
lenmap = {i:len(hasher[i]) for i in range(512)}

encodr = {1<<i: i+1 for i in range(9)}       # reverse mapping of decodr
decodr = {i+1:1<<i for i in range(9)}        # maps 1->000000001, 2->000000010
removr = {1<<i:511-(1<<i) for i in range(9)} # maps 1->111111110, 2->111111101

def remove(grid, n, val):
    ''' Recursively remove value v from all neighbors of cell n in grid '''

    for i in neighbors[n]:
        # For all cells that have not been set, i.e. |D|>1
        if lenmap[grid[i]] > 1:

            # Remove v from domain using bit-manipulation
            grid[i] &= removr[val]

            # IMPOSSIBLE case since the cell had |D| > 1 before removal
            if lenmap[grid[i]]==0: return False
            
            # If a cell becomes "set", recurse remove()
            elif lenmap[grid[i]]==1:
                if remove(grid, i, grid[i]) is False: return False

        # If cell is set but not the same value, there is conflict
        elif grid[i] == val: return False

    # No conflict on removal. Helps in forward-checking
    return True

def backtrack(grid):
    '''
        Runs backtracking algorithm.
        Minimum value heuristic: Chooses cell with least branches
    '''

    # Compute the cell with least branching
    mincel = -1  # Minimum cell (argmin)
    minlen = 10  # Minimum length heuristic (min)

    for i in range(81):
        tmp = lenmap[grid[i]]
        if tmp == 1: continue
        if tmp == 2: mincel = i; break
        if tmp < minlen: minlen, mincel = tmp, i
    
    # Base Case: Everything has already been set
    if mincel < 0: return grid
    
    # For each value in the chosen cell's domain
    for val in hasher[grid[mincel]]:

        # Clone the grid to deal with backtracking overwrites
        tmpgrd = grid[:]

        # Update the value of the chosen cell
        tmpgrd[mincel] = decodr[val]
        if remove(tmpgrd, mincel, decodr[val]):

            # Backtracking with the new value and check if result is found
            result = backtrack(tmpgrd)
            if result is not False: return result
    
    # None of the values in the cell's domain matches. Backtrack up.
    return False

def solveGrid(grid):
    ''' Convert a string grid into an int[81] list and run backtracking '''

    # Convert to int[81] with 511 = 111111111 = {1,2,3,4,5,6,7,8,9} mapping
    g = [511 if i=='0' else decodr[int(i)] for i in grid]

    # For each set value (|D|=1), run arc consistency on the node
    for i in range(81):
        if lenmap[g[i]]==1:
            if not remove(g, i, g[i]):
                print "Unsolvable"
                return False

    # Solve the grid using backtracking, if possible
    solved = backtrack(g)

    # Return False for UNSOLVABLE or a string concatenation of the grid
    if solved is False: return False
    else: return "".join([str(encodr[i]) for i in solved])


def pf_util(i):
    ''' Helper function for printing strings pf = printer function '''
    if lenmap[i]==1: return ' '*4+str(encodr[i])+' '*4
    return ''.join([str(k) if k in hasher[i] else ' ' for k in range(1,10)])

def print_grid(g):
    ''' Prints the grid including possibilities in a very specific format '''
    for i in range(81):
        if i%27==0: print '-'*108
        print '|'+pf_util(g[i])+'|',
        if i%9==8: print
    print '-'*108

def write_solved(board, f_name=out_filename, mode='w+'):
    ''' Write solved board to desired file, overwriting by default. '''

    outfile = open(f_name, mode)
    outfile.write(board)
    outfile.write('\n')
    outfile.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:  # Run a single board, as done during grading
        board = solveGrid(sys.argv[1].strip())
        write_solved(board)

    else:
        print "Running all from sudokus_start"

        #  Read boards from source.
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print "Error reading the sudoku file %s" % src_filename
            exit()

        times = []
        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):
            if len(line) < 9: continue

            # Solve the board str->str
            start = time()
            board = solveGrid(line.strip())
            times.append(time()-start)

            # Append solved board to output.txt
            write_solved(board, mode='a+')
        times = np.array(times)

        print "Min time: %.2e" % times.min()
        print "Max time: %.2e" % times.max()
        print "Avg time: %.2e ± %.2e\n" % (times.mean(), times.std())

        print "Finished %d board(s) in file in %.2e seconds." % (
                                    len(times), times.sum())
