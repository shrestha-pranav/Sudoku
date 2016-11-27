#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A simple program to solve 9x9 Sudoku grids.
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

@author: Pranav Shrestha
"""


class Sudoku(object):

    def __init__(self, sudokuGrid):
        """
        Initializes a sudokuGrid using either an array or string
        """
        if type(sudokuGrid) == list:
            #Basic comparison to check for 9x9 array
            if(len(sudokuGrid)==9 and len(sudokuGrid[0]==9)):
                self.grid = sudokuGrid[:]
        elif type(sudokuGrid) == str:
            self.grid = [[int(sudokuGrid[i * 9 + j]) for j in range(9)]
                         for i in range(9)]        
        else:
            raise TypeError('Grid provided was not string or array')

    def printGrid(self):
        """
        Prints the Sudoku Grid using formatting methods
        """
        print ('/' + '-' * 23 + '\\')
        for (i, row) in enumerate(self.grid):
            print (('|' + ' {} {} {} |' * 3).format(*[x if x != 0 else ' ' 
                for x in row]))
            if i == 8:
                print ('\\' + '-' * 23 + '/')
            elif i % 3 == 2:
                print ('|' + '-' * 23 + '|')

    def nextCell(self, row, column):
        """
        Returns the co-ordinates of the next empty cell.
        Returns -1, -1 if there is no empty cell after (row, column)
        """
        for j in range(column, 9):
            if self.grid[row][j] == 0:
                return row, j

        for i in range(row + 1, 9):
            for j in range(0, 9):
                if self.grid[i][j] == 0:
                    return i, j
        return -1, -1

    def isValid(self, row, column, checkValue):
        """
        Checks if the checkValue is valid for (row,column)
        """
        
        #Checking for duplicate in row and column
        for i in range(9):
            if checkValue == self.grid[row][i] \
                or checkValue == self.grid[i][column]:
                return False

        #Checking for duplicate in 3x3 subgrid
        subgridX, subgridY = 3 * int(row / 3), 3 * int(column / 3)
        for i in range(subgridX, subgridX + 3):
            for j in range(subgridY, subgridY + 3):
                if checkValue == self.grid[i][j]:
                    return False

        return True

    def solveGrid(self, row=0, column=0):
        """
        Implementation of the backtracking algorithm
        """
        
        #Find next empty cell in the Sudoku grid
        row, column = self.nextCell(row, column)
        
        #If there are no empty cells found
        if row == -1:
            return True
        
        #Check every value (1-9) in the selected cell
        for checkValue in range(1, 10):
            #If value is valid, check the next cell
            if self.isValid(row, column, checkValue):
                self.grid[row][column] = checkValue
                if self.solveGrid(row, column):
                    return True
                #Return grid to initial state if value isn't correct
                self.grid[row][column] = 0

        #If no value is valid, return false
        return False


if __name__ == '__main__':
    """
    Simple test class with preset grid
    """
    s = "0030206009003050010018064000081029007000"\
    "00008006708200002609500800203009005010300"
    sudoku_grid = Sudoku(s)
    sudoku_grid.printGrid()
    sudoku_grid.solveGrid()
    sudoku_grid.printGrid()