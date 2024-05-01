class sudoku():
    """
        sudoku(myString) -> sudoku object

        Creates a sudoku object. The string argument MUST be atleast 81 
        characters or an out-of-bounds error will occur.

        mySudokuObject = sudoku("  1624  769   7 135   1  8  69  18   4  6 79  5  824   1 7   268 62   79  213   8")
    """

    def __init__(self, boardStr):
        self.board = [None]*9

        i = 0

        for y in range(9):
            self.board[y] = [None]*9
            for x in range(9):
                self.board[y][x] = boardStr[i]
                i += 1
            
    def getBoard(self):
        """
            sudokuObject.getBoard -> str

            Returns the sudoku board as a plain string. No Arguments.
        """
        boardStr = ""
        for y in range(9):
            for x in range(9):
                boardStr += self.board[y][x]
        return boardStr

    def validateCell(self, x, y, val):
        for rowPos in range(9):
            if (self.board[y][rowPos] == val):
                return False

        for colPos in range(9):
            if (self.board[colPos][x] == val):
                return False
            
        for cellY in range(y // 3 * 3, y // 3 * 3 + 2):
            for cellX in range(x // 3 * 3, x // 3 * 3 + 2):
                if (self.board[cellY][cellX] == val):
                    return False

        return True

    def solve(self, x=0, y=0):
        """
            sudokuObject.solve -> None

            Solves the sudoku recursively. No arguments.
        """
        if x > 8:
            y += 1
            x = 0
            if y > 8:
                return True

        if self.board[y][x] != ' ':
            if self.solve(x + 1, y):
                return True
        else:
            for i in range(1, 10):
                if self.validateCell(x, y, str(i)):
                    self.board[y][x] = str(i)
                    if self.solve(x + 1, y):
                        return True
                    self.board[y][x] = ' '