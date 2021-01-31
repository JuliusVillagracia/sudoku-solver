# Import Necessary Libraries
from tkinter import Tk, Frame, Canvas, Button, Event, Label, StringVar, OptionMenu
from PIL import ImageTk, Image
from copy import deepcopy

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
        padding = self.margin // 2

        self.menu_frame = Frame(self, width=self.width, height=self.menu, padx=self.margin, bg="white")
        
        Button(self.menu_frame, text="Solve", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.solveBoard).grid(row=0, column=0, sticky='NSEW', pady=(0, padding), padx=(0, padding))
        
        Button(self.menu_frame, text="Reset", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.resetBoard).grid(row=0, column=1, sticky='NSEW', pady=(0, padding))
        
        Button(self.menu_frame, text="Generate", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.generatePuzzle).grid(row=1, column=0, sticky='NSEW', pady=(0, self.margin), padx=(0, padding))
        
        self.input_btn = Button(self.menu_frame, text="Input", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.inputPuzzle)
        self.input_btn.grid(row=1, column=1, sticky='NSEW', pady=(0, self.margin))

        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_rowconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        self.menu_frame.grid_rowconfigure(1, weight=1)

        self.menu_frame.pack(fill='both')
        self.menu_frame.pack_propagate(0)

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
        if self.game_canvas.find_withtag("locked_cells") != ():
            self.game_canvas.delete("locked_cells")

        # Fill in each cell with the puzzle entry from the current puzzle state
        for i in range(self.board_size):
            for j in range(self.board_size):
                # Differently format cell's containing hint entries
                font = "Inconsolata " + str(int(20*self.screen_size)) + " bold" if self.original_puzzle[i][j] != 0 else "Inconsolata " + str(int(20*self.screen_size))
                color = "white" if self.original_puzzle[i][j] != 0 else "black"

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
        
        # Check if there are any cell hint entries and lower them
        if self.game_canvas.find_withtag("locked_cells") != ():
            self.game_canvas.tag_raise("grid_thick", "locked_cells")
            self.game_canvas.tag_raise("grid_lines", "locked_cells")

            # Check if a cell is highlighted and raise the highlight border
            if self.game_canvas.find_withtag("selected_highlight") != ():
                self.game_canvas.tag_raise("selected_highlight", "locked_cells")
                self.game_canvas.tag_raise("selected_highlight", "grid_lines")
                self.game_canvas.tag_raise("selected_highlight", "grid_thick")

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
        elif self.width - self.margin < x_coor < self.width and 0 < y_coor < self.margin:
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
        
        self.input_btn = Button(self.menu_frame, text="Input", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.inputPuzzle)
        self.input_btn.grid(row=1, column=1, sticky='NSEW', pady=(0, self.margin))

        # Configure grid formatting to fit equally into the frame
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_rowconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        self.menu_frame.grid_rowconfigure(1, weight=1)
        self.menu_frame.pack_propagate(0)

    def solveBoard(self):
        self.puzzle = algo.solve(deepcopy(self.original_puzzle))
        if self.puzzle:
            self.drawPuzzle()
        else:
            self.reset_board()

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
        self.enterframe = Frame(self, width=self.width, height=self.menu, padx=self.margin, bg="white")
        self.enterframe.pack(fill='both')

        # Add confirmation button when entry is done
        Button(self.enterframe, text="Enter", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.enterPuzzle).pack(fill='both', pady=(0, self.margin))

        # Let the button fill the whole frame
        self.enterframe.pack_propagate(0)

    def enterPuzzle(self):
        if algo.solve(deepcopy(self.puzzle)):
            # Clear out the menu to make room for a new frame 
            self.enterframe.destroy()

            # Register the player input into the puzzle
            self.original_puzzle = deepcopy(self.puzzle)
            self.drawPuzzle()
            
            # Re-intialize the menu
            self.initMenu()

    def openSettings(self):
        # Clear out the frames to transition into settings 
        self.menu_frame.destroy()
        self.game_canvas.destroy()

        # Declare variables to be tracked
        variable = StringVar()
        variable.set("Default")

        # Initialize settings frame
        self.settingsframe = Frame(self, width=self.width, height=self.height + self.menu, bg="white")
        self.settingsframe.pack(fill='both')

        # Create a label for the screen size option
        Label(self.settingsframe, text="Screen Size", bg="white", font="cambria 15").pack()

        # Create the options menu for screen sizes
        OptionMenu(self.settingsframe, variable, "Even Smaller", "Smaller", "Default", "Larger", "Even Larger", command=self.updateSettings).pack(fill='both')

        # Create the button to get back to the game
        Button(self.settingsframe, text="Register", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.closeSettings).pack()

        # Let the frame be fully filled
        self.settingsframe.pack_propagate(0)

    def closeSettings(self):
        # Clear out the settings frame
        self.settingsframe.destroy()

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