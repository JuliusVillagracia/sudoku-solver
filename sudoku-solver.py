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
    [0, 8, 0, 2, 0, 5, 0, 0, 0],
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

def backtrack(puzzle, coordinates):
    # Split the coordinates to x and y
    x, y = coordinates
    # Set Base Case as the solved puzzle
    if solvedChecker(puzzle):
        return puzzle
    else:
        # Trace possible numbers for the cell
        if puzzle[x][y] == 0:
            for num in range(1, board_size+1):
                if validityChecker(puzzle, x, y, num):
                    puzzle[x][y] = num
                    solution = backtrack(puzzle, nextCoordinates(x, y))
                    if solution:
                        return solution
                    puzzle[x][y] = 0
            # Return false if the algorithm finds no possible number to enter
            return False
        # Skip the cell when it is already filled
        else:
            solution = backtrack(puzzle, nextCoordinates(x, y))
            return solution

# Print results in the terminal
print("\n~ ~ ~ ORIGINAL ~ ~ ~\n")
printBoard(puzzle)

print("\n~ ~ ~ SOLVED ~ ~ ~\n")
answer = backtrack(puzzle, (0, 0))
if answer:
    printBoard(answer)
else:
    print("[!] The sudoku board has no solutions")