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

# Print results in the terminal
print("\n~ ~ ~ ORIGINAL ~ ~ ~\n")
printBoard(puzzle)

print("\n~ ~ ~ SOLVED ~ ~ ~\n")
# Add Function Call for solution