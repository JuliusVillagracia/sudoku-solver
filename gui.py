# Import Necessary Libraries
from tkinter import Tk, Frame, Canvas, Button, Event, Label, StringVar, OptionMenu
from PIL import ImageTk, Image
from copy import deepcopy
from time import sleep

# Import Other Files
import importlib  
algo = importlib.import_module("sudoku-solver")

class gameGUI(Frame):
    def __init__(self, parent):
        # Configure GUI dimensions
        self.board_size = 9 # Configure board size
        self.screen_size = 1 # Screen size
        self.margin = int(20 * self.screen_size) # Space around the board
        self.cell_dim = int(50 * self.screen_size) # Dimension of every board cell.
        self.width = self.height = self.margin * 2 + self.cell_dim * self.board_size  # Width and height of the whole board
        self.menu = self.margin * 2 + self.cell_dim * 2 # Extra space for the menu

        # Configure parent of game frame
        self.parent = parent
        Frame.__init__(self, parent, bg="white")
        self.parent.title("Sudoku")
        self.parent.iconbitmap("grid.ico")
        self.pack(fill='both', expand=1)
        self.parent.geometry(str(self.width) + "x" + str(self.height + self.menu) + "+1000+200")
        self.parent.resizable(0,0)

        # Initialize puzzle variables
        self.row, self.col = -1, -1
        self.original_puzzle = [
            [0, 2, 0, 0, 0, 4, 3, 0, 0],
            [9, 0, 0, 0, 2, 0, 0, 0, 8],
            [0, 0, 0, 6, 0, 9, 0, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 7, 2, 5, 0, 3, 6, 8, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 2, 0, 5, 0, 0, 0],
            [1, 0, 0, 0, 9, 0, 0, 0, 3],
            [0, 0, 9, 8, 0, 0, 0, 6, 0]]
        self.puzzle = [
            [0, 2, 0, 0, 0, 4, 3, 0, 0],
            [9, 0, 0, 0, 2, 0, 0, 0, 8],
            [0, 0, 0, 6, 0, 9, 0, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 7, 2, 5, 0, 3, 6, 8, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 2, 0, 5, 0, 0, 0],
            [1, 0, 0, 0, 9, 0, 0, 0, 3],
            [0, 0, 9, 8, 0, 0, 0, 6, 0]]
        self.collection = []
        self.timer = False

        # Initialize Frames
        self.game_canvas = None
        self.menu_frame = None
        self.register_frame = None
        self.settings_frame = None

        # Initialize Inner Frames
        self.initBoard()
        self.initMenu()

    def initBoard(self):
        # Create the Game Canvas and pack it into the frame
        self.game_canvas = Canvas(self, width=self.width, height=self.height, bg='white', highlightthickness=0)
        self.game_canvas.pack(fill='both', side='top')

        # Create Gear Icon for settings at the corner of the canvas
        self.png = Image.open('settings.png')
        self.png = self.png.resize((self.margin, self.margin), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.png)
        self.game_canvas.create_image(self.width-self.margin//2, self.margin//2, image=self.img, tags='settings')

        # Draw the board contents within the canvas
        self.drawPuzzle()
        self.drawGrid()

        # Bind keys to the canvas for tracking
        self.game_canvas.bind("<Button-1>", self.cellClicked)
        self.game_canvas.bind("<Key>", self.keyPressed)
    
    def initMenu(self):
        # Initialize padding across the buttons
        padding = self.margin // 2

        # Create the Menu Frame and pack it into the frame
        self.menu_frame = Frame(self, width=self.width, height=self.menu, padx=self.margin, bg="white")
        self.menu_frame.pack(fill='both')
        
        # Insert menu buttons into the grid and bind each with a command
        Button(self.menu_frame, text="Solve", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.solveBoard).grid(row=0, column=0, sticky='NSEW', pady=(0, padding), padx=(0, padding))
        
        Button(self.menu_frame, text="Reset", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.resetBoard).grid(row=0, column=1, sticky='NSEW', pady=(0, padding))
        
        Button(self.menu_frame, text="Generate", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.generatePuzzle).grid(row=1, column=0, sticky='NSEW', pady=(0, self.margin), padx=(0, padding))
        
        Button(self.menu_frame, text="Input", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.inputPuzzle).grid(row=1, column=1, sticky='NSEW', pady=(0, self.margin))

        # Configure grid formatting to fit equally into the frame
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_rowconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        self.menu_frame.grid_rowconfigure(1, weight=1)
        self.menu_frame.grid_propagate(0)

    def drawGrid(self):
        # Clear the canvas of any grid lines before drawing new ones
        self.game_canvas.delete("grid_lines")
        
        # Loop and create horizontal and vertical lines across
        for i in range(self.board_size + 1):
            color = "black" if i % 3 == 0 else "gray"
            w = 3 if i % 3 == 0 else 1
            tag = "grid_thick" if i % 3 == 0 else "grid_lines"

            # Vertical Lines
            x0 = self.margin + i * self.cell_dim
            y0 = self.margin
            x1 = self.margin + i * self.cell_dim
            y1 = self.height - self.margin
            self.game_canvas.create_line(x0, y0, x1, y1, width=w, fill=color, tags=tag)

            # Horizontal Lines
            x0 = self.margin
            y0 = self.margin + i * self.cell_dim
            x1 = self.width - self.margin
            y1 = self.margin + i * self.cell_dim
            self.game_canvas.create_line(x0, y0, x1, y1, width=w, fill=color, tags=tag)
        
        # Raise the thicker borders above the other components
        self.game_canvas.tag_raise("grid_thick", "grid_lines")

    def drawPuzzle(self):
        # Clear the canvas of any puzzle components before drawing new puzzle
        self.game_canvas.delete("entries")
        if self.game_canvas.find_withtag("locked_cells"):
            self.game_canvas.delete("locked_cells")
        if self.game_canvas.find_withtag("algo_filled"):
            self.game_canvas.delete("algo_filled")

        # Initialze a variable for streak tracking within the algorithm
        streak = True

        # Fill in each cell with the puzzle entry from the current puzzle state
        for i in range(self.board_size):
            for j in range(self.board_size):
                # Differently format cell's containing hint entries
                font = "Inconsolata " + str(int(20*self.screen_size)) + " bold" if self.original_puzzle[i][j] != 0 else "Inconsolata " + str(int(20*self.screen_size))
                color = "white" if self.original_puzzle[i][j] != 0 else "black"

                # Check if the algorithm is running
                if self.collection and self.puzzle[i][j] != 0 and self.original_puzzle[i][j] == 0:
                    x0 = self.margin + j * self.cell_dim
                    y0 = self.margin + i * self.cell_dim
                    x1 = (self.margin + j * self.cell_dim) + self.cell_dim
                    y1 = (self.margin + i * self.cell_dim) + self.cell_dim
                    
                    # Highlight the correct cells in the algorithm
                    if self.puzzle[i][j] == self.collection[-1][0][i][j] and self.puzzle[i][j] == self.collection[-1][0][i][j] and streak:
                        self.game_canvas.create_rectangle(x0, y0, x1, y1, fill='green', width=0, tags="algo_filled")
                    
                    # Highlight the current cell in the algorithm
                    elif i == self.collection[0][1] and j == self.collection[0][2]:
                        streak = False
                        self.game_canvas.create_rectangle(x0, y0, x1, y1, fill='red', width=0, tags="algo_filled")
                    
                    # Highlight the filled cells in the algorithm
                    else:
                        streak = False
                        self.game_canvas.create_rectangle(x0, y0, x1, y1, fill='blue', width=0, tags="algo_filled")

                # Highlight hint entries with gray boxes
                if self.original_puzzle[i][j] != 0:
                    x0 = self.margin + j * self.cell_dim
                    y0 = self.margin + i * self.cell_dim
                    x1 = (self.margin + j * self.cell_dim) + self.cell_dim
                    y1 = (self.margin + i * self.cell_dim) + self.cell_dim
                    self.game_canvas.create_rectangle(x0, y0, x1, y1, fill='gray', tags="locked_cells")
                
                # Draw entries into the canvas according to current puzzle state
                if self.puzzle[i][j] != 0:
                    x = self.margin + j * self.cell_dim + self.cell_dim / 2
                    y = self.margin + i * self.cell_dim + self.cell_dim / 2
                    self.game_canvas.create_text(x, y, text=self.puzzle[i][j], tags="entries", fill=color, font=font)
        
        # Update object stacking in the canvas
        if self.game_canvas.find_withtag("locked_cells"):
            # Raise the priority of the grid
            self.game_canvas.tag_raise("grid_lines")
            self.game_canvas.tag_raise("grid_thick")

            # Check if a cell is highlighted and raise the highlight border
            if self.game_canvas.find_withtag("selected_highlight"):
                self.game_canvas.tag_raise("selected_highlight")
                
    def cellClicked(self, event):
        # Extract screen coordinates when function is called from button
        if type(event) == Event:
            x_coor = event.x
            y_coor = event.y
        
        # Extract from a tuple when function is called key press
        elif type(event) == tuple:
            y_coor, x_coor = event

        # Check if the cursor is within the canvas when it clicks
        if (type(event) == tuple) or (self.margin < x_coor < self.width - self.margin and self.margin < y_coor < self.height - self.margin):
            # Clear the canvas selection before highlighting another
            self.game_canvas.delete("selected_highlight")
            
            # Focus on the canvas for key tracking
            self.game_canvas.focus_set()
            
            # Check which cell is selected_highlight in terms of coordinates unless function is called by key press in which case retain the extracted tuple
            col = (x_coor - self.margin) // self.cell_dim if type(event) == Event else x_coor
            row = (y_coor - self.margin) // self.cell_dim if type(event) == Event else y_coor
            
            # Check if cell clicked is already highlighted or not
            if col != self.col or row != self.row:
                # Loop and create cell highlight borders by side 
                for i in range(4):
                    x0 = (self.margin + col * self.cell_dim) + self.cell_dim if i == 3 else self.margin + col * self.cell_dim
                    y0 = (self.margin + row * self.cell_dim) + self.cell_dim if i == 2 else self.margin + row * self.cell_dim
                    x1 = (self.margin + col * self.cell_dim) + self.cell_dim if i != 0 else self.margin + col * self.cell_dim
                    y1 = (self.margin + row * self.cell_dim) + self.cell_dim if i != 1 else self.margin + row * self.cell_dim
                    self.game_canvas.create_line(x0, y0, x1, y1, fill="red", width=3, tags="selected_highlight")
            else:
                # Reset cell coordinates as highlight is removed
                col = row = -1

            # Update the coordinates of the highlighted cell
            self.col = col
            self.row = row
        
        # Check if settings is clicked 
        elif self.width - self.margin < x_coor < self.width and 0 < y_coor < self.margin and not self.collection:
            self.openSettings()

    def keyPressed(self, event):
        # Check if a character exists for the key pressed
        if event.char != '':
            # Check if a cell is highlighted
            if self.row != -1 and self.col != -1:
                # Move highlight upwards
                if event.char == 'w' and self.row > 0:
                    self.cellClicked((self.row-1, self.col))
                
                # Move highlight downwards
                elif event.char == 's' and self.row < self.board_size-1:
                    self.cellClicked((self.row+1, self.col))
                
                # Move highlight to the left
                elif event.char == 'a' and self.col > 0:
                    self.cellClicked((self.row, self.col-1))
                
                # Move highlight to the right
                elif event.char == 'd' and self.col < self.board_size-1:
                    self.cellClicked((self.row, self.col+1))

                # Check if the key is valid
                if self.original_puzzle[self.row][self.col] == 0:
                    # Enter the entry for a valid number
                    if event.char in "123456789":
                        self.puzzle[self.row][self.col] = int(event.char)
                        self.drawPuzzle()

                    # Remove the entry if escape and backspace is clicked
                    elif event.char in ["\x08", "\x1b"]:
                        self.puzzle[self.row][self.col] = 0
                        self.drawPuzzle()

    def display_algo(self):
        # Select the earliest step in the collection and remove it from the list
        self.puzzle = self.collection.pop(0)[0]

        # Check if the algorithm still needs to go through anymore steps
        if self.collection:
            # Update the GUI
            self.drawPuzzle()

            # Delayed recursion for next step
            self.after(2, self.display_algo)
        else:
            # Lock the puzzle in place once solved
            self.original_puzzle = deepcopy(self.puzzle) # Subject to change
            
            # Update the GUI
            self.drawPuzzle()

    def solveBoard(self):
        # Call the function to run the algorithm
        self.backtrack(deepcopy(self.original_puzzle), (0, 0)) # make result to be collection in sudoku-solver.py
        self.display_algo()

        # if self.puzzle:
        #     self.display_algo()
        # else:
        #     self.reset_board()

    def backtrack(self, puzzle, coordinates):
        # Split the coordinates to x and y
        x, y = coordinates
        # Set Base Case as the solved puzzle
        if algo.solvedChecker(puzzle):
            return puzzle
        else:
            # Trace possible numbers for the cell
            # Add each change to a list collection
            if puzzle[x][y] == 0:
                for num in range(1, algo.board_size+1):
                    if algo.validityChecker(puzzle, x, y, num):
                        puzzle[x][y] = num
                        self.collection.append([deepcopy(puzzle), x, y])

                        solution = self.backtrack(puzzle, algo.nextCoordinates(x, y))
                        if solution:
                            self.collection.append([deepcopy(puzzle), x, y])
                            return solution
                        
                        puzzle[x][y] = 0
                        self.collection.append([deepcopy(puzzle), x, y])
                # Return false if the algorithm finds no possible number to enter
                return False
            # Skip the cell when it is already filled
            else:
                solution = self.backtrack(puzzle, algo.nextCoordinates(x, y))
                return solution

    def resetBoard(self):
        self.puzzle = deepcopy(self.original_puzzle)
        self.drawPuzzle()

    def generatePuzzle(self):
        pass

    def inputPuzzle(self):
        # Clear out the menu to make room for a new frame 
        self.menu_frame.destroy()

        # re-initialize the board to get it ready for input
        self.original_puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.drawPuzzle()

        # Create a new menu frame
        self.register_frame = Frame(self, width=self.width, height=self.menu, padx=self.margin, bg="white")
        self.register_frame.pack(fill='both')

        # Create a label for instructions and warnings
        self.prompt = Label(self.register_frame, text="Press the button when you're done", bg="white", relief='solid', width=self.width)
        self.prompt.grid(row=0, column=0, sticky='NSEW', pady=(0, self.margin))

        # Add confirmation button when entry is done
        Button(self.register_frame, text="Enter", bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.enterPuzzle).grid(row=1, column=0, sticky='NSEW', pady=(0, self.margin))

        # Configure grid formatting to fit equally into the frame
        self.register_frame.grid_columnconfigure(0, weight=2)
        self.register_frame.grid_rowconfigure(0, weight=2)
        self.register_frame.grid_columnconfigure(1, weight=1)
        self.register_frame.grid_rowconfigure(1, weight=1)
        # Let the button fill the whole frame
        self.register_frame.grid_propagate(0)

    def enterPuzzle(self):
        result = algo.solve(deepcopy(self.puzzle))
        if type(result) == list:
            # Clear out the menu to make room for a new frame 
            self.register_frame.destroy()

            # Register the player input into the puzzle
            self.original_puzzle = deepcopy(self.puzzle)
            self.drawPuzzle()
            
            # Re-intialize the menu
            self.initMenu()
        else:
            self.prompt.configure(text = "Invalid Input")

    def openSettings(self):
        # Clear out the frames to transition into settings 
        self.menu_frame.destroy()
        self.game_canvas.destroy()
        if self.register_frame != None:
            self.register_frame.destroy()

        # Declare variables to be tracked
        variable = StringVar()
        variable.set("Default")

        # Initialize settings frame
        self.settings_frame = Frame(self, width=self.width, height=self.height + self.menu, bg="white")
        self.settings_frame.pack(fill='both')

        # Create a label for the screen size option
        Label(self.settings_frame, text="Screen Size", bg="white", font="cambria 15").pack()

        # Create the options menu for screen sizes
        OptionMenu(self.settings_frame, variable, "Even Smaller", "Smaller", "Default", "Larger", "Even Larger", command=self.updateSettings).pack(fill='both')

        # Create the button to get back to the game
        Button(self.settings_frame, text="Register", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.closeSettings).pack()

        # Let the frame be fully filled
        self.settings_frame.pack_propagate(0)

    def closeSettings(self):
        # Clear out the settings frame
        self.settings_frame.destroy()

        # Re-initialize the game screen
        self.initBoard()
        self.initMenu()

    def updateSettings(self, option):
        # Update the screen size according to the option picked
        if option == "Even Smaller":
            self.screen_size = 0.6
        elif option == "Smaller":
            self.screen_size = 0.8
        elif option == "Default":
            self.screen_size = 1
        elif option == "Larger":
            self.screen_size = 1.2
        elif option == "Even Larger":
            self.screen_size = 1.4
        
        # Reconfigure GUI settings
        self.board_size = 9
        self.margin = int(20 * self.screen_size) # Space around the board
        self.cell_dim = int(50 * self.screen_size) # Dimension of every board cell.
        self.width = self.height = self.margin * 2 + self.cell_dim * self.board_size  # Width and height of the whole board
        self.menu = self.margin * 2 + self.cell_dim * 2 # Extra space for the menu
        root.geometry(str(self.width) + "x" + str(self.height + self.menu) + "+1000+200") # Window Size

# Initialize root window
root = Tk()
# Initialize GUI Class
gameGUI = gameGUI(root)
# Instigate Loop
root.mainloop()