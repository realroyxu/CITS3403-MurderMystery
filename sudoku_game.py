from flask import Flask, request, render_template
from sudoku_puzzle import SudokuPuzzle, SudokuGenerator
import ctypes

app = Flask(__name__)
app = Flask(__name__, template_folder='htmls', static_folder='css+js')

# the 2D list of the starting numbers in the sudoku 
play_grid = []

# boolean that is True if a Sudoku has been generated using
#   the SudokuGenerator object, False otherwise
has_generated = False

@app.route('/')
def menu():
    global has_generated
    has_generated = False
    return render_template('mainmenu.html')


@app.route('/input_play')
def input_play():
    return render_template('iplay.html')


@app.route('/input_solve')
def input_solve():
    return render_template('isolve.html')


@app.route('/play', methods=['POST', 'GET'])
def play():
    global play_grid
    global has_generated
    sudoku_grid_list = []
    if request.method == 'POST':

        # if the POST request is from '/input_play' or '/play'
        if 'play' in request.referrer:

            # build 2D list in order to initialize SudokuPuzzle object
            for i in range(9):
                row_list = []
                for j in range(9):
                    id = "" + str(i*9 + j)
                    content = request.form[id]
                    if content == "":
                        row_list.append(0)
                    else:
                        row_list.append(int(content))
                sudoku_grid_list.append(row_list)
            s = SudokuPuzzle(sudoku_grid_list)

            # if the POST request is from '/input_play"
            if '/input_play' in request.referrer:
                play_grid = s.return_array()

                # renders the play.html file
                # is_solved will be "None" since the sudoku is not completed
                # input_array is initialized to play_grid, which contains the starting numbers of a sudoku
                # play_array refers to the compiled 2D list after a user has finished playing a sudoku; in this case, play_array will be None
                return render_template('play.html', is_solved = "None", input_array = play_grid, play_array = None)

            # if the POST request is from '/play" (when the user checks their sudoku)
            elif '/play' in request.referrer:
                # renders the play.html file
                # is_solved is initialized to a boolean of whether the completed sudoku is valid
                # check_array is initialized to a 2D list of booleans that signify if each cell is valid
                # input_array is initialized to play_grid, which contains the starting numbers of a sudoku
                # play_array refers to the compiled 2D list after a user has finished playing the sudoku
                return render_template('play.html', is_solved = s.check_grid(), check_array = s.check_grid_items(), input_array = play_grid, play_array = s.return_array())

        # if the POST request is from the menu page
        elif '/' in request.referrer:

            # obtain the user specified difficulty
            if request.form.get('easy') != None:
                content = request.form.get('easy')
            elif request.form.get('medium') != None:
                content = request.form.get('medium')
            elif request.form.get('hard') != None:
                content = request.form.get('hard')
            else:
                content = request.form.get('expert')
            
            # if a Sudoku hasn't already been generated, create one of the specified difficulty
            if not has_generated:
                g = SudokuGenerator(content)
                play_grid = g.generate_sudoku()
                has_generated = True
            return render_template('play.html', is_solved = "None", input_array = play_grid, play_array=None)
    else:
        return render_template('play.html', is_solved="None", input_array = play_grid, play_array = None)


@app.route('/solution', methods=['POST', 'GET'])
def solution():
    sudoku_grid_list = []
    if request.method == 'POST':

        # build 2D list from inputted numbers in order to initialize SudokuPuzzle object
        for i in range(9):
            row_list = []
            for j in range(9):
                id = "" + str(i*9 + j)
                content = request.form[id]
                if content == "":
                    row_list.append(0)
                else:
                    row_list.append(int(content))
            sudoku_grid_list.append(row_list)

        # Create the solved Sudoku based off of the numbers inputted by the user in '/input_solve'
        s = SudokuPuzzle(sudoku_grid_list)
        s.solve()

        return render_template('solution.html', solved_array = s.return_array())
    else:
        return render_template('mainmenu.html')



if __name__ == "__main__":
    app.run(debug=True, port=5550)