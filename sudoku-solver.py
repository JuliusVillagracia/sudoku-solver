# Initialize variables
board_size = 9
sub_size = 3
# Sample Puzzle
puzzle = [
    [0, 2, 0, 0, 0, 4, 3, 0, 0],
    [9, 0, 0, 0, 2, 0, 0, 0, 8],
    [0, 0, 0, 6, 0, 9, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 7, 2, 5, 0, 3, 6, 8, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 2, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 9, 0, 0, 0, 3],
    [0, 0, 9, 8, 0, 0, 0, 6, 0]
]

'''
Solution:
[
    [8, 2, 7, 1, 5, 4, 3, 9, 6],
    [9, 6, 5, 3, 2, 7, 1, 4, 8],
    [3, 4, 1, 6, 8, 9, 7, 5, 2],
    [5, 9, 3, 4, 6, 8, 2, 7, 1],
    [4, 7, 2, 5, 1, 3, 6, 8, 9],
    [6, 1, 8, 9, 7, 2, 4, 3, 5],
    [7, 8, 6, 2, 3, 5, 9, 1, 4],
    [1, 5, 4, 7, 9, 6, 8, 2, 3],
    [2, 3, 9, 8, 4, 1, 5, 6, 7]
]
'''

# The easy puzzles contain 35-45 given numbers, 
# while the hardest all contain about 25-26.

def printBoard(puzzle):
    # Print Readable Board On Terminal
    for row in range(board_size):
        if row != 0 and row%sub_size == 0:
            print("- "*11)
        for col in range(board_size):
            if col in [3, 6]:
                print("|", end=' ')
            print(puzzle[row][col], end=' ')
        print()

def solvedChecker(puzzle):
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

def backtrack(puzzle, coordinates=(0,0), moves=[]):
    # Split the coordinates to x and y
    x, y = coordinates
    # Set Base Case as the solved puzzle
    if solvedChecker(puzzle):
        return {"Solution": puzzle, "Moves": moves}
    else:
        # Trace possible numbers for the cell
        if puzzle[x][y] == 0:
            for num in range(1, board_size+1):
                if validityChecker(puzzle, x, y, num):
                    # Try the valid number and update the moves list
                    puzzle[x][y] = num
                    moves.append([x, y, num])
                    # Recurse backtrack while passing the next coordinates and the current moves list
                    solution = backtrack(puzzle, coordinates=nextCoordinates(x, y), moves=moves)
                    # Return the found solution board and update moves list
                    if solution:
                        return solution
                    # Reset the invalid and update the moves list
                    puzzle[x][y] = 0
                    moves.append([x, y, 0])
            # Return false if the algorithm finds no possible number to enter
            return False
        # Skip the cell when it is already filled
        else:
            solution = backtrack(puzzle, coordinates=nextCoordinates(x, y), moves=moves)
            return solution

def initialValidation(puzzle):
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
                        check_sub.append(puzzle[sub_size * (x // sub_size) + row2][sub_size * (y // sub_size) + col2])

                # Loop through all possible entries for counting
                for num in range(1, board_size+1):
                    # Check sub matrices
                    if check_sub.count(num) > 1:
                        return "[ ! ] " + str(num) + " was repeated repeatedly across sub matrix (" + str(x // sub_size) + ", " + str(y // sub_size) + ")"

                # Reset Tracker
                check_sub = []

        # Loop through all possible entries for counting
        for num in range(1, board_size+1):
            # Check rows
            if puzzle[x].count(num) > 1:
                return "[ ! ] " + str(num) + " was repeated repeatedly across row " + str(x)
                
            # Check columns
            if check_col.count(num) > 1:
                return "[ ! ] " + str(num) + " was repeated repeatedly across column " + str(x)

        # Reset Tracker
        check_col = []

# Print results in the terminasl
# print("\n~ ~ ~ ORIGINAL ~ ~ ~\n")
# printBoard(puzzle)

# print("\n~ ~ ~ SOLVED ~ ~ ~\n")
# answer = initialValidation(puzzle)
# print('ANS: ', answer, end='\n\n')
# if not answer:
#     printBoard(backtrack(puzzle)["Solution"])
#     print(len(backtrack(puzzle)["Moves"]))
# else:
#     print("[!] The sudoku board has no solutions")