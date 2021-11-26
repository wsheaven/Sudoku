import json

def read_board():
    '''Ask the user for a filename where the board is saved'''
    valid = False
    board = []
    while not valid:
        try:
            filename = input("What is the filename? (If new game enter 'board.json') ")
            with open(filename) as infile:
                data = json.load(infile)
                

                # Populate the new board from the file.

                for info in data["board"]:
                    board.append(info)

            # If the file loads and we can import the data then leave the while loop.

            valid = True

        # If the file is not found then prompt the user to try again

        except:
            print("Try again")
    return board
    

def is_board_solved(board):
    '''Checks if the board is solved. If it is it will return True otherwise False. '''
    # Check each row and make sure that there is no 0 and no numbers twice, if there are return False.     
    for rows in range(9):
        row = []
        for columns in range(9):
            row.append(board[rows][columns])
            if row.count(board[rows][columns]) > 1 or board[rows][columns] == 0:
                return False
            assert 1 <= board[rows][columns] <= 9

    # Check each column to ensure that there is no duplicate numbers or numbers twice, if there are return False.
    for columns in range(9):
        column = []
        for rows in range(9):
            column.append(board[rows][columns]) 
            if column.count(board[rows][columns]) > 1 or board[rows][columns] == 0:
                return False
            assert 1 <= board[rows][columns] <= 9

    # Check each 3x3 square for duplicates or empty spaces, if there are any return False.
    start_column = 0
    end_column = 3
    for _ in range(3):
        start_row = 0
        end_row = 3
        for _ in range(3):
            grid = []
            for columns in range(start_column, end_column):
                for rows in range(start_row, end_row):
                    grid.append(board[rows][columns])
                    if grid.count(board[rows][columns]) > 1 or board[rows][columns] == 0:
                        return False            
            start_row += 3
            end_row += 3
        start_column += 3
        end_column += 3
    
    # If the program has reached this far no duplicates or empty spaces have been found meaning the board has been solved.
    return True

def save_board(board):
    '''Save the board to a file named board1.json'''
    save_board = {
        "board" : board
    }

    try: 
        save_name = input("Where would you like to save this board? please enter in the format 'name.json' " )
        with open(save_name, "w") as f:
            json.dump(save_board, f)
    except:
        print("Invalid name")
    print(f"The board has been saved to {save_name}")
    

def display_board(board):
    '''Print out a formated board'''
    print("   A B C  D E F  G H I  ")
    for row in range(9):
        if row == 3 or row == 6:
            print("  -------+------+------")
        print(f"{row + 1}  ", end='')
        for column in range(9):
            seperator = "  |  |  \n"
            if board[row][column] >= 1:
                print(f'{board[row][column]} ', end ="")
            elif board[row][column] == 0:
                print("  ", end ="")
            if seperator[column] != ' ':
                print(seperator[column], end ="")


    

def get_square_choice():
    ''' Get the square choice from the user or allow them to save and quit. '''

    valid = False
    column_int = [0, "A", "B", "C", "D", "E", "F", "G", "H", "I"]
    square = input("\nWhat square would you like to select? (ie A1) or enter 'q' to save and quit ")

    # If the user enters q then return empty cordinates and the true boolean to save and quit.  
    if square.lower() == "q":
        return 0, 0, True

    # Make sure the input is in a valid format, first try format A1 then format 1A. if it is niether ask the user again. 
    while not valid:
        try:
            try:
                row_position = int(square[1]) - 1
                column_position = int(column_int.index(square[0].upper())) - 1
                valid = True
            except:
                row_position = int(square[0]) - 1
                column_position = int(column_int.index(square[1].upper())) - 1
                valid = True
        except:
            square = input('Please try again, remember to enter in this format "A1" ')

    return row_position, column_position, False

def get_input(row, column, board):
    '''Get the users input for what value they want to place on the selected square. '''
    assert 0 <= row <= 8
    assert 0 <= column <= 8

    number = input("Please enter an integer between 1-9 or 's' to see the possible values \n")

    # If the user enters s then show them all the legal moves for the selected square. 
    if number.lower() == 's':
        print(valid_numbers(row, column, board)[0])

    # Get the users input and ensure that it is valid. 
    valid = False
    while not valid:
        try:
            number = int(number)
            if 1 <= number and number <= 9:
                valid = True
            else:
                number = input("Please enter an integer between 1-9 ")
        except:
            number = input("Please enter an integer between 1-9 ")
    return number

def valid_numbers(row_position, column_position, board):
    '''Find all legal moves for a selected square and return them. '''

    assert 0 <= row_position <= 8
    assert 0 <= column_position <= 8

    grid_numbers = []
    row_numbers = []
    column_numbers = []
    valid_numbers = []

    # Calculate the starting square for the 3x3 grid that holds the selected square. 
    grid_start_row = (row_position // 3) * 3
    grid_end_row = grid_start_row + 3
    grid_start_column = (column_position // 3) * 3
    grid_end_column = grid_start_column + 3

    # If the square is already full then print to indicate and return the empty list as well as the bool False
    # to indicate that the user should be asked for a different square.  
    if board[row_position][column_position] != 0:
        print("Thas spot is filled")
        return valid_numbers, False

    # add each number from the selected grid into a list.  
    for column in range(grid_start_column, grid_end_column):
                for row in range(grid_start_row, grid_end_row):
                    if board[row][column] != 0:
                        grid_numbers.append(board[row][column])

    # add each number from the selected row into a list.
    for row in range(9):
        if board[row][column_position] != 0:
            column_numbers.append(board[row][column_position])

    # add each number from the selected column into a list.
    for column in range(9):
        if board[row_position][column] != 0:
            row_numbers.append(board[row_position][column])

    # Check each number from 1-9 and if it is not in any of the lists it is valid and add it to the list valid. 
    for viable in range(1,10):
        if viable not in column_numbers and viable not in row_numbers and viable not in grid_numbers:
            valid_numbers.append(viable)

    # Return the list of valid numbers along with the bool True to indicate the user has selected a viable square. 
    return valid_numbers, True

def validate_input(valid_numbers, input):
    '''Make sure that the integer the user entered is a legal move. '''
    assert 1 <= input <= 9
    return valid_numbers.count(input) >= 1


def apply_input(board, row_position, column_position, input):
    '''Apply the users input to the board'''
    assert 0 <= row_position <= 8
    assert 0 <= column_position <= 8

    board[row_position][column_position] = input

def play_game(board):
    """ Play the game of Sudoku. display the board and get the users actions."""
    display_board(board)
    row, column, save = get_square_choice()

    # If the variable save is True then it indicates that the user wants to quit and save. Return the board and the bool True to indicate this. 
    if save:
        return board, True, 

    # Get the valid numbers for the user selected square. If the square is full then ask the user for a different square. 
    valid_nums,  valid = valid_numbers(row,column,board)
    while not valid:
        row, column, save = get_square_choice()
        if save:
            return board, True, 
        valid_nums,  valid = valid_numbers(row,column,board)

    # Get the users input, check it check that it is a legal move. If it is then apply it to the board otherwise tell the user it is invalid.     
    choice = get_input(row, column, board)
    if validate_input(valid_nums, choice):
        apply_input(board, row, column, choice)
    else: 
        print("\nThat is not a valid move\n")

    # If you have gotten this far then the user wishes to continue playing, return the board and the bool False to indicate. 
    return board, False, 

def main():
    """The game of Sudoku"""
    board = read_board()
    # as long as the user does not want to quit and the board is not solved continue playing. 
    # Once either of those conditions are True save the board and indicate to the user it has been saved. 
    valid = False
    while not valid:
        board, valid = play_game(board)
        if is_board_solved(board):
            print("You Have won!")
            valid = True
    save_board(board)
    


# Uncomment next 3 lines to test get_square_choice function. 
# print(get_square_choice())
# print(get_square_choice())
# print(get_square_choice())


main()



  