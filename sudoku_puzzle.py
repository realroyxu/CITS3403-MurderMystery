import random

class SudokuPuzzle:
    def __init__(self, grid):
        """
        Initializes an object of type SudokuPuzzle with a 2D list containing the digits

        Parameters: 
        grid (list): a 2d list that the object uses to initialize self.grid
        """
        self.grid = grid

    def __str__(self):
        """
        Creates and returns a string representation of the SudokuPuzzle object
        """
        string = ''
        for i in range(9):
            for j in range(9):
                string += str(self.grid[i][j]) + " "
            string += "\n"
        
        return string
        
    def input_number(self, x, y, num):
        """
        Inputs a number in the specified x, y location in self.grid

        Parameters:
        x (int): x location where num should be placed
        y (int): y location where num should be placed
        num (int): number between 1-9 that should be inputted in the 
            appropriate x, y location in self.grid
        """
        self.grid[x][y] = num

    def get_grid(self):
        """
        Returns the grid attribute of a SudokuPuzzle object
        """
        return self.grid

    def create_row_column_box_lists(self, x, y):
        """
        Creates three separate lists of all numbers in a given row,
            column, and box
        
        Parameters:
        x (int): x location that should be checked
        y (int): y location that should be checked

        Returns:
        tuple: three elements in the tuple that correspond to the
            row list, column list, and box list
        """
        # create a list of all numbers in a given row
        row_list = self.grid[x]

        # create a list of all numbers in a given column
        column_list = []
        for i in range(9):
            column_list.append(self.grid[i][y])

        # create a list of all numbers in a given box
        box_list = []
        mod_r = (x + 1) % 3
        mod_c = (y + 1) % 3
        if mod_r == 0:
            box_rows = [x, x - 1, x - 2]
        elif mod_r == 1:
            box_rows = [x, x + 1, x + 2]
        else:
            box_rows = [x - 1, x, x + 1]

        if mod_c == 0:
            box_columns = [y, y - 1, y - 2]
        elif mod_c == 1:
            box_columns = [y, y + 1, y + 2]
        else:
            box_columns = [y - 1, y, y + 1]

        for i in box_rows:
            for j in box_columns:
                box_list.append(self.grid[i][j])
                
        return (row_list, column_list, box_list)

    def is_valid_number(self, x, y, num):
        """
        Checks if a single number is valid in a given row, column, or box

        Parameters:
        x (int): x location that should be checked
        y (int): y location that should be checked
        num (int): number between 1-9 that should be checked for validity in
            the appropriate x, y location in self.grid

        Returns:
        boolean: True if the number is valid in the given location
        """
        if self.grid[x][y] != 0:
            return False
        else:
            row_list, column_list, box_list = self.create_row_column_box_lists(x, y)

            # check if num is in any of the lists created
            if num in row_list:
                return False
            elif num in column_list:
                return False
            elif num in box_list:
                return False
            else:
                return True

    def is_valid_puzzle(self):
        """
        Checks each location in self.grid to ensure a valid Sudoku puzzle  
        
        Returns:
        boolean: True if Sudoku puzzle is valid, False if it is not
        """
        for x in range(9):
            for y in range(9):
                if self.grid[x][y] == 0:
                    return False
                else:
                    row_list, column_list, box_list = self.create_row_column_box_lists(x, y)

                    # check if all numbers 1-9 are in each list
                    for num in range(1, 10):
                        if num not in row_list:
                            return False
                        if num not in column_list:
                            return False
                        if num not in box_list:
                            return False
            
        return True

    def get_validity_grid(self):
        """
        Checks each location in self.grid to see if there is more than one
            instance of a number in a given row, column, or box

        Returns:
        list: a 2D list of booleans. Each location corresponds to a location
            in the Sudoku and is False if more than one instance of a number 
            appears in the row, column, or box or is True otherwise
        """
        validity_grid = []
        has_added = False
        for x in range(9):
            row_validity = []
            for y in range(9):
                if self.grid[x][y] == 0:
                    row_validity.append(False)
                    has_added = True
                else:
                    row_list, column_list, box_list = self.create_row_column_box_lists(x, y)
                    num = self.grid[x][y]

                    # append False if there is more than one instance of
                    #   a number in any of the lists
                    if row_list.count(num) > 1 or column_list.count(num) > 1 or box_list.count(num) > 1:
                        row_validity.append(False)
                        has_added = True

                    # if False hasn't been appended, append True
                    if not has_added:
                        row_validity.append(True)
                        has_added = True
                has_added = False
            validity_grid.append(row_validity)
        
        return validity_grid

    def find_empty_location(self):
        """
        Helper method for solve(). Finds a location in self.grid that is 0, which represents an empty location

        Returns:
        tuple: the empty location in the grid. x and y are used to find a specific 
            location in a 2D list
        """
        for x in range(9):
            for y in range(9):
                if self.grid[x][y] == 0:
                    return (x, y)
        
        return None

    def solve_puzzle(self):
        """
        Recursive function that solves a given grid with a backtracking algorithm

        Loops through all possible numbers in a certain cell. If the number is 
            valid (no conflicts in the row, column, or box), it will input the 
            number and continue. If at some point, a cell can not hold any valid 
            numbers, the algorithm will input a different number in an empty cell.

        Returns:
        boolean: True if the solve is valid, False otherwise
        """
        empty_loc = self.find_empty_location()
        
        # if there are no empty locations in the grid, the Sudoku is solved
        if not empty_loc:
            return True
        else:
            x, y = empty_loc

        # input numbers in all grid locations such that every number is valid 
        #   and there are no empty locations
        for i in range(1, 10):
            if self.is_valid_number(x, y, i):
                self.input_number(x, y, i)

                if self.solve_puzzle():
                    return True

                self.input_number(x, y, 0)
    
        return False


class SudokuGenerator:
    def __init__(self, difficulty_level):
        """
        Initializes a SudokuGenerator object with a difficulty_level attribute

        Parameter:
        String: specified difficulty (either "easy", "medium", "hard", or "expert")
        """
        self.difficulty_level = difficulty_level

    def generate_sudoku(self):
        """
        Selects a random Sudoku with a difficulty based on self.difficulty_level

        self.difficulty_level is used to read a .txt file that contains 200 
            sudokus of a given difficulty. A random sudoku is then chosen 
            from the file

        Returns:
        list: a 2D list initialized with digits that correspond to a unique sudoku
        """
        sudoku = []

        # open file containing the sudokus of the specified difficulty
        file_name = 'sudokus/sudokus_' + self.difficulty_level + '.txt'
        file = open(file_name, 'r')
        all_lines = file.readlines()
        
        # choose random line from the file
        rand_num = random.randint(0, 400)
        rand_line = all_lines[rand_num]

        # if the line in the text file is blank, move to the next one
        if len(rand_line) <= 2:
            rand_line = all_lines[rand_num + 1]

        # construct 2D list from the .txt sudoku representation
        for i in range(9):
            grid_row = []
            for j in range(9):
                char = rand_line[i*9+j]
                if char == '.':
                    # append a 0 (representing a blank in the grid) if
                    #   the character is a . in the text file
                    grid_row.append(0)
                else:
                    grid_row.append(char)
            sudoku.append(grid_row)
        
        return sudoku