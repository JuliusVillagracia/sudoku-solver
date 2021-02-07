# Import necessary libraries
from random import randint, random, shuffle

# Initialize variables
board_size = 9
sub_size = 3

def printBoard(puzzle):
    # Print Readable Board On Terminal
    print()
    for row in range(board_size):
        if row != 0 and row % sub_size == 0:
            print("- "*11)
        for col in range(board_size):
            if col in [3, 6]:
                print("|", end=' ')
            print(puzzle[row][col], end=' ')
        print()


def completeChecker(puzzle):
    # Check if the puzzle has been populated completely
    for row in range(board_size):
        if 0 in puzzle[row]:
            return False
    return True


def validityChecker(puzzle, x, y, num):
    # Check the validity horizontally
    if num in puzzle[x]:
        return False
    # Check the validity vertically
    for row in range(board_size):
        if num == puzzle[row][y]:
            return False
    # Solve for the beginning of the sub matrix
    sub_row = int(x - x % sub_size)
    sub_col = int(y - y % sub_size)
    # Check the validity within the sub matrix
    for row in range(sub_size):
        for col in range(sub_size):
            if num == puzzle[sub_row + row][sub_col + col]:
                return False
    return True


def nextCoordinates(x, y):
    # Check if out of bounds then iterate coordinates
    if y == board_size-1:
        return x + 1, 0
    else:
        return x, y + 1


def backtrack(puzzle, coordinates=(0, 0), moves=[]):
    # Split the coordinates to x and y
    x, y = coordinates
    # Set Base Case as the solved puzzle
    if completeChecker(puzzle) and not boardValidation(puzzle):
        return {"Solution": puzzle, "Moves": moves, "Skip": False}
    else:
        # Trace possible numbers for the cell
        if puzzle[x][y] == 0:
            for num in range(1, board_size+1):
                if validityChecker(puzzle, x, y, num):
                    # Try the valid number and update the moves list
                    puzzle[x][y] = num
                    moves.append([x, y, num])
                    # Recurse backtrack while passing the next coordinates and the current moves list
                    solution = backtrack(
                        puzzle, coordinates=nextCoordinates(x, y), moves=moves)
                    # Return the found solution board and update moves list
                    if solution["Solution"] != "Unsolvable":
                        return solution
                    # Reset the invalid and update the moves list
                    puzzle[x][y] = 0
                    moves.append([x, y, 0])
            # Return false if the algorithm finds no possible number to enter
            return {"Solution": "Unsolvable", "Moves": [], "Skip": False} # False
        # Skip the cell when it is already filled
        else:
            solution = backtrack(
                puzzle, coordinates=nextCoordinates(x, y), moves=moves
            )
            return solution


def boardValidation(puzzle):
    # Initialize variables for tracking
    check_col = []
    check_sub = []

    # Loop through the board and verify that it is valid before backtracking
    for x in range(board_size):
        for y in range(board_size):
            # Track columns as it loops
            check_col.append(puzzle[y][x])

            # Only track sub matrices in the beggining of each sub section
            if x % sub_size == 0 and y % sub_size == 0:
                for row2 in range(sub_size):
                    for col2 in range(sub_size):
                        check_sub.append(
                            puzzle[sub_size * (x // sub_size) + row2][sub_size * (y // sub_size) + col2])

                # Loop through all possible entries for counting
                for num in range(1, board_size+1):
                    # Check sub matrices
                    if check_sub.count(num) > 1:
                        return "[!] " + str(num) + " was repeated across sub matrix (" + str(x // sub_size) + ", " + str(y // sub_size) + ")"

                # Reset Tracker
                check_sub = []

        # Loop through all possible entries for counting
        for num in range(1, board_size+1):
            # Check rows
            if puzzle[x].count(num) > 1:
                return "[!] " + str(num) + " was repeated across row " + str(x)

            # Check columns
            if check_col.count(num) > 1:
                return "[!] " + str(num) + " was repeated across column " + str(x)

        # Reset Tracker
        check_col = []


def generatePuzzle():
    # Initialize a blank slate
    puzzle = [[0 for col in range(board_size)]
              for row in range(board_size)]

    # Crawl through each sub matrix
    for row in range(sub_size):
        for col in range(sub_size):
            # Randomize coordinates
            x = randint(0, 2) * 3
            y = randint(0, 2) * 3
            # Initialize possible moves and shuffle it
            possible = [val for val in range(1, board_size+1)]
            shuffle(possible)
            # Keep looping until a possibile entry is found
            while possible:
                # Choose one from the list and remove it from the possibility list
                num = possible.pop()
                # Update the puzzle when it is a valid move
                if validityChecker(puzzle, row + x, col + y, num):
                    puzzle[row + x][col + y] = num
    
    # Solve the template puzzle
    puzzle = backtrack(puzzle, moves=[])["Solution"]

    # Initialzie variable for total cells
    total_cells = board_size * board_size 
    # Randomize the difficulty
    relative_difficulty = random()
    # Set a 20% chance for the puzzle to have less hints than average
    if relative_difficulty > 0.2:
        removal = total_cells - randint(int(total_cells*0.45), int(total_cells*0.55))
    else:
        removal = total_cells - randint(int(total_cells*0.30), int(total_cells*0.35))
    # Remove a number of entries within the puzzle
    for i in range(removal):
        while True:
            # Randomize coordinates
            x = randint(0, 8)
            y = randint(0, 8)
            # Only stop when a non-zero entry is found
            if puzzle[x][y] != 0:
                puzzle[x][y] = 0
                break
    # Return the generated puzzle
    return puzzle


def solvabilityChecker(puzzle):
    # Initialize a blank slate
    invalid_moves = [[[] for col in range(board_size)]
              for row in range(board_size)]

    # Loop through the board and find each hint
    for x in range(board_size):
        for y in range(board_size):
            if puzzle[x][y]:
                # Check rows and columns
                for line in range(board_size):
                    # Update invalid moves for the rows
                    if not puzzle[line][y] and puzzle[x][y] not in invalid_moves[line][y]:
                        invalid_moves[line][y].append(puzzle[x][y])
                        # If the valid moves are reduced to one, update the puzzle and recurse the algorithm
                        if len(invalid_moves[line][y]) == 8:
                            for i in range(1, board_size+1): 
                                if i not in invalid_moves[line][y]:
                                    puzzle[line][y] = i
                                    break
                            return solvabilityChecker(puzzle)

                    # Update invalid moves for the columns
                    if not puzzle[x][line] and puzzle[x][y] not in invalid_moves[x][line]:
                        invalid_moves[x][line].append(puzzle[x][y])
                        # If the valid moves are reduced to one, update the puzzle and recurse the algorithm
                        if len(invalid_moves[x][line]) == 8:
                            for i in range(1, board_size+1): 
                                if i not in invalid_moves[x][line]:
                                    puzzle[x][line] = i
                                    break
                            return solvabilityChecker(puzzle)

                # Calculate start of each sub matrix
                sub_row = x - x % sub_size
                sub_col = y - y % sub_size

                # loop through each cell in the sub matrix of the current entry
                for row in range(sub_size):
                    for col in range(sub_size):
                        # Update invalid moves for the sub matrix
                        if not puzzle[sub_row + row][sub_col + col] and puzzle[x][y] not in invalid_moves[sub_row + row][sub_col + col]:
                            invalid_moves[sub_row + row][sub_col + col].append(puzzle[x][y])
                            # If the valid moves are reduced to one, update the puzzle and recurse the algorithm
                            if len(invalid_moves[sub_row + row][sub_col + col]) == 8:
                                for i in range(1, board_size+1): 
                                    if i not in invalid_moves[sub_row + row][sub_col + col]:
                                        puzzle[sub_row + row][sub_col + col] = i
                                        break
                                return solvabilityChecker(puzzle)

    # Finally, if everything seems correct, check validity of the puzzle
    return boardValidation(puzzle)
