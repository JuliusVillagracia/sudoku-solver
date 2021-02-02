# Import Necessary Libraries
from tkinter import Tk, Frame, Canvas, Button, Event, Label, StringVar, OptionMenu
from PIL import ImageTk, Image
from copy import deepcopy
from time import sleep

# Import Created Libraries
import algorithm as algo


class GameGUI(Frame):
    def __init__(self, parent):
        # Configure GUI dimensions
        self.board_size = 9  # Configure board size
        self.screen_size = 1  # Screen size
        self.margin = int(20 * self.screen_size)  # Space around the board
        # Dimension of every board cell.
        self.cell_dim = int(50 * self.screen_size)
        self.width = self.height = self.margin * 2 + self.cell_dim * \
            self.board_size  # Width and height of the whole board
        self.menu = self.margin * 2 + self.cell_dim * 2  # Extra space for the menu

        # Configure parent of game frame
        self.parent = parent
        Frame.__init__(self, parent, bg="white")
        self.parent.title("Sudoku")
        self.parent.iconbitmap("grid.ico")
        self.pack(fill='both', expand=1)
        self.parent.geometry(str(self.width) + "x" +
                             str(self.height + self.menu) + "+1000+200")
        self.parent.resizable(0, 0)

        # Initialize puzzle variables
        self.row, self.col = -1, -1
        self.original_puzzle = [
            [1, 2, 3, 0, 0, 0, 0, 0, 0],
            [4, 5, 6, 0, 0, 0, 0, 0, 0],
            [7, 8, 9, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 3, 0, 0, 0],
            [0, 0, 0, 4, 5, 6, 0, 0, 0],
            [0, 0, 0, 7, 8, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 2, 3],
            [0, 0, 0, 0, 0, 0, 4, 5, 6],
            [0, 0, 0, 0, 0, 0, 7, 8, 9]]
        self.puzzle = [
            [1, 2, 3, 0, 0, 0, 0, 0, 0],
            [4, 5, 6, 0, 0, 0, 0, 0, 0],
            [7, 8, 9, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 3, 0, 0, 0],
            [0, 0, 0, 4, 5, 6, 0, 0, 0],
            [0, 0, 0, 7, 8, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 2, 3],
            [0, 0, 0, 0, 0, 0, 4, 5, 6],
            [0, 0, 0, 0, 0, 0, 7, 8, 9]]
        self.collection = {"Solution": None, "Moves": []}
        self.timer = {"Hour": 0, "Minute": 0,
                      "Second": 0, "Millisecond": 0, "Pause": False}
        self.win = False

        # Initialize Frames
        self.game_canvas = None
        self.menu_frame = None
        self.register_frame = None
        self.settings_frame = None

        # Initialize Inner Frames
        self.initBoard()
        self.initMenu()

        # Start-up the timer
        self.updateTimer()

    def initBoard(self):
        # Create the Game Canvas and pack it into the frame
        self.game_canvas = Canvas(
            self, width=self.width, height=self.height, bg='white', highlightthickness=0)
        self.game_canvas.pack(fill='both', side='top')

        # Create Gear Icon for settings at the corner of the canvas
        self.png = Image.open('settings.png')
        self.png = self.png.resize((self.margin, self.margin), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.png)
        self.game_canvas.create_image(
            self.width-self.margin//2, self.margin//2, image=self.img, tags='settings')

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
        self.menu_frame = Frame(self, width=self.width,
                                height=self.menu, padx=self.margin, bg="white")
        self.menu_frame.pack(fill='both')

        # Create a label for the timer
        self.time_label = Label(self.menu_frame, text="{:0>2d}h {:0>2d}m {:0>2d}s".format(
            self.timer["Hour"], self.timer["Minute"], self.timer["Second"]), bg="white", relief='solid', height=self.margin, width=(self.width-self.margin)//2)
        self.time_label.grid(row=0, column=0, columnspan=2,
                             sticky='NSEW', pady=(0, padding))

        # Insert menu buttons into the grid and bind each with a command
        Button(self.menu_frame, text="Solve", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff',
               relief='solid', command=self.solveBoard).grid(row=1, column=0, sticky='NSEW', pady=(0, padding), padx=(0, padding))

        Button(self.menu_frame, text="Reset", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff',
               activebackground='#ffffff', relief='solid', command=self.resetBoard).grid(row=1, column=1, sticky='NSEW', pady=(0, padding))

        Button(self.menu_frame, text="Generate", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff', activebackground='#ffffff',
               relief='solid', command=self.generatePuzzle).grid(row=2, column=0, sticky='NSEW', pady=(0, self.margin), padx=(0, padding))

        Button(self.menu_frame, text="Input", width=(self.width-self.margin)//2, height=self.margin, bg='#ffffff',
               activebackground='#ffffff', relief='solid', command=self.inputPuzzle).grid(row=2, column=1, sticky='NSEW', pady=(0, self.margin))

        # Configure grid formatting to fit equally into the frame
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_rowconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        self.menu_frame.grid_rowconfigure(1, weight=1)
        self.menu_frame.grid_columnconfigure(2, weight=1)
        self.menu_frame.grid_rowconfigure(2, weight=1)
        self.menu_frame.grid_propagate(0)

    def updateTimer(self):
        # Check if the board has been solved
        if algo.completeChecker(self.puzzle) and not algo.boardValidation(self.puzzle):
            # Raise the win flag agter algorithm
            self.win = True
            # Update the puzzle
            self.drawPuzzle()

        # Cap the clock to update only when the menu_frame is visible
        if self.menu_frame and not self.timer["Pause"] and not self.win:
            # Update the timer variable
            if self.timer["Minute"] == 59:
                self.timer["Hour"] += 1
                self.timer["Minute"] = 0
            elif self.timer["Second"] == 59:
                self.timer["Minute"] += 1
                self.timer["Second"] = 0
            elif self.timer["Millisecond"] == 990:
                self.timer["Second"] += 1
                self.timer["Millisecond"] = 0
            else:
                self.timer["Millisecond"] += 10

            # Update the timer label in the menu_frame
            self.time_label.configure(text="{:0>2d}h {:0>2d}m {:0>2d}s".format(
                self.timer["Hour"], self.timer["Minute"], self.timer["Second"]))

            # Recurce the clock to update every second
            self.after(10, self.updateTimer)

    def drawGrid(self):
        # Clear the canvas of any grid lines before drawing new ones
        self.game_canvas.delete("grid_lines")
        self.game_canvas.delete("grid_thick")

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
            self.game_canvas.create_line(
                x0, y0, x1, y1, width=w, fill=color, tags=tag)

            # Horizontal Lines
            x0 = self.margin
            y0 = self.margin + i * self.cell_dim
            x1 = self.width - self.margin
            y1 = self.margin + i * self.cell_dim
            self.game_canvas.create_line(
                x0, y0, x1, y1, width=w, fill=color, tags=tag)

        # Raise the thicker borders above the other components
        self.game_canvas.tag_raise("grid_thick", "grid_lines")

    def drawPuzzle(self):
        # Clear the canvas of any puzzle components before drawing new puzzle
        self.game_canvas.delete("entries")
        if self.game_canvas.find_withtag("locked_cells"):
            self.game_canvas.delete("locked_cells")
        if self.game_canvas.find_withtag("algo_filled"):
            self.game_canvas.delete("algo_filled")
        if self.game_canvas.find_withtag("algo_current") and self.win:
            self.game_canvas.delete("algo_current")
        if self.game_canvas.find_withtag("solved_cells") and not self.win:
            self.game_canvas.delete("solved_cells")

        # Initialze a variable for streak tracking within the algorithm
        streak = True

        # Fill in each cell with the puzzle entry from the current puzzle state
        for i in range(self.board_size):
            for j in range(self.board_size):
                # Differently format cell's containing hint entries
                font = "Inconsolata " + \
                    str(int(20*self.screen_size)) + \
                    " bold" if self.original_puzzle[i][j] != 0 else "Inconsolata " + str(
                        int(20*self.screen_size))
                color = "white" if self.original_puzzle[i][j] != 0 else "black"

                # Check if the cell is filled
                if self.puzzle[i][j] != 0:
                    x0 = self.margin + j * self.cell_dim
                    y0 = self.margin + i * self.cell_dim
                    x1 = (self.margin + j * self.cell_dim) + self.cell_dim
                    y1 = (self.margin + i * self.cell_dim) + self.cell_dim

                    # Check if the win is raised
                    if not self.win:
                        # Check if the algorithm is running
                        if self.collection["Moves"] and self.original_puzzle[i][j] == 0:
                            # Highlight the correct cells in the algorithm
                            if self.puzzle[i][j] == self.collection["Solution"][i][j] and streak:
                                self.game_canvas.create_rectangle(
                                    x0, y0, x1, y1, fill='green', width=0, tags="algo_filled")

                            # Highlight the current cell in the algorithm
                            elif i == self.collection["Moves"][0][0] and j == self.collection["Moves"][0][1]:
                                streak = False
                                self.game_canvas.create_rectangle(
                                    x0, y0, x1, y1, fill='red', width=0, tags="algo_current")

                            # Highlight the filled cells in the algorithm
                            else:
                                streak = False
                                self.game_canvas.create_rectangle(
                                    x0, y0, x1, y1, fill='blue', width=0, tags="algo_filled")
                    else:
                        # Universalize the color when the win flag is raised
                        self.game_canvas.create_rectangle(
                            x0, y0, x1, y1, fill='orange', width=0, tags="solved_cells")

                # Highlight hint entries with gray boxes
                if self.original_puzzle[i][j] != 0:
                    self.game_canvas.create_rectangle(
                        x0, y0, x1, y1, fill='gray', tags="locked_cells")

                # Draw entries into the canvas according to current puzzle state
                if self.puzzle[i][j] != 0:
                    x = self.margin + j * self.cell_dim + self.cell_dim / 2
                    y = self.margin + i * self.cell_dim + self.cell_dim / 2
                    self.game_canvas.create_text(
                        x, y, text=self.puzzle[i][j], tags="entries", fill=color, font=font)

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
            col = (
                x_coor - self.margin) // self.cell_dim if type(event) == Event else x_coor
            row = (
                y_coor - self.margin) // self.cell_dim if type(event) == Event else y_coor

            # Check if cell clicked is already highlighted or not
            if col != self.col or row != self.row:
                # Loop and create cell highlight borders by side
                for i in range(4):
                    x0 = (self.margin + col * self.cell_dim) + \
                        self.cell_dim if i == 3 else self.margin + col * self.cell_dim
                    y0 = (self.margin + row * self.cell_dim) + \
                        self.cell_dim if i == 2 else self.margin + row * self.cell_dim
                    x1 = (self.margin + col * self.cell_dim) + \
                        self.cell_dim if i != 0 else self.margin + col * self.cell_dim
                    y1 = (self.margin + row * self.cell_dim) + \
                        self.cell_dim if i != 1 else self.margin + row * self.cell_dim
                    self.game_canvas.create_line(
                        x0, y0, x1, y1, fill="red", width=3, tags="selected_highlight")
            else:
                # Reset cell coordinates as highlight is removed
                col = row = -1

            # Update the coordinates of the highlighted cell
            self.col = col
            self.row = row

        # Check if settings is clicked
        elif self.width - self.margin < x_coor < self.width and 0 < y_coor < self.margin and not self.collection["Moves"]:
            self.openSettings()

    def keyPressed(self, event):
        # Check if a cell is highlighted
        if self.row != -1 and self.col != -1:
            # Move highlight upwards
            if event.keysym in ['Up', 'w'] and self.row > 0:
                self.cellClicked((self.row-1, self.col))

            # Move highlight downwards
            elif event.keysym in ['Down', 's'] and self.row < self.board_size-1:
                self.cellClicked((self.row+1, self.col))

            # Move highlight to the left
            elif event.keysym in ['Left', 'a'] and self.col > 0:
                self.cellClicked((self.row, self.col-1))

            # Move highlight to the right
            elif event.keysym in ['Right', 'd'] and self.col < self.board_size-1:
                self.cellClicked((self.row, self.col+1))

            # Check if the key is valid
            if self.original_puzzle[self.row][self.col] == 0:
                # Enter the entry for a valid number
                if event.keysym in "123456789":
                    self.puzzle[self.row][self.col] = int(event.char)
                    self.drawPuzzle()

                # Remove the entry if escape and backspace is clicked
                elif event.keysym in ["Delete", "Escape", "BackSpace"]:
                    self.puzzle[self.row][self.col] = 0
                    self.drawPuzzle()

    def display_algo(self):
        # Select the earliest step in the collection and remove it from the list
        self.puzzle[self.collection["Moves"][0][0]
                    ][self.collection["Moves"][0][1]] = self.collection["Moves"][0][2]
        self.collection["Moves"].pop(0)[0]

        # Update the GUI
        self.drawPuzzle()

        # Check if the algorithm still needs to go through anymore steps
        if self.collection["Moves"]:
            # Delayed recursion for next step
            self.after(2, self.display_algo)

    def solveBoard(self):
        # Reset game variables
        self.puzzle = deepcopy(self.original_puzzle)
        self.timer = {"Hour": 0, "Minute": 0,
                      "Second": 0, "Millisecond": 0, "Pause": False}

        # Call the function to run the algorithm
        self.collection = algo.backtrack(deepcopy(self.original_puzzle))

        # Reset win flag and timer
        if self.win:
            self.win = False
            self.updateTimer()

        # Run through each step to the solution
        self.display_algo()

    def resetBoard(self):
        # Only allow button functionality when algorithm isn't running
        if not self.collection["Moves"]:
            # Reset game variables
            self.puzzle = deepcopy(self.original_puzzle)
            self.timer = {"Hour": 0, "Minute": 0,
                          "Second": 0, "Millisecond": 0, "Pause": False}

            # Reset win flag and timer
            if self.win:
                self.win = False
                self.updateTimer()

            # Update the GUI
            self.drawPuzzle()

    def generatePuzzle(self):
        # Only allow button functionality when algorithm isn't running
        if not self.collection["Moves"]:
            pass

    def inputPuzzle(self):
        # Only allow button functionality when algorithm isn't running
        if not self.collection["Moves"]:
            # Reset win flag
            self.win = False

            # Clear out the menu to make room for a new frame
            self.menu_frame.destroy()
            self.menu_frame = None

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
            self.timer = {"Hour": 0, "Minute": 0,
                          "Second": 0, "Millisecond": 0, "Pause": False}

            # Create a new menu frame
            self.register_frame = Frame(
                self, width=self.width, height=self.menu, padx=self.margin, bg="white")
            self.register_frame.pack(fill='both')

            # Create a label for instructions and warnings
            self.prompt = Label(self.register_frame, text="Press the button when you're done",
                                bg="white", relief='solid', width=self.width)
            self.prompt.grid(row=0, column=0, sticky='NSEW',
                             pady=(0, self.margin))

            # Add confirmation button when entry is done
            Button(self.register_frame, text="Enter", bg='#ffffff', activebackground='#ffffff', relief='solid',
                   command=self.enterPuzzle).grid(row=1, column=0, sticky='NSEW', pady=(0, self.margin))

            # Configure grid formatting to fit equally into the frame
            self.register_frame.grid_columnconfigure(0, weight=2)
            self.register_frame.grid_rowconfigure(0, weight=2)
            self.register_frame.grid_columnconfigure(1, weight=1)
            self.register_frame.grid_rowconfigure(1, weight=1)
            # Let the button fill the whole frame
            self.register_frame.grid_propagate(0)

    def enterPuzzle(self):
        # Check if the board is valid
        result = algo.boardValidation(self.puzzle)
        if not result:
            # Clear out the menu to make room for a new frame
            self.register_frame.destroy()
            self.register_frame = None

            # Register the player input into the puzzle
            self.original_puzzle = deepcopy(self.puzzle)
            self.drawPuzzle()

            # Re-intialize the menu
            self.initMenu()

            # Start-up the timer
            self.updateTimer()
        else:
            # Display the error prompt to the interface
            self.prompt.configure(text=result)

    def openSettings(self):
        # Only allow settings to open when algorithm isn't running
        if not self.collection["Moves"]:
            # Pause the timer
            self.timer["Pause"] = True

            # Clear out the frames to transition into settings
            if self.menu_frame != None:
                self.menu_frame.destroy()
                self.menu_frame = None
            if self.register_frame != None:
                self.register_frame.destroy()
                self.register_frame = None
            self.game_canvas.destroy()
            self.game_canvas = None

            # Declare variables to be tracked
            variable = StringVar()
            variable.set("Default")

            # Initialize settings frame
            self.settings_frame = Frame(
                self, width=self.width, height=self.height + self.menu, bg="white")
            self.settings_frame.pack(fill='both')

            # Create a label for the screen size option
            Label(self.settings_frame, text="Screen Size",
                  bg="white", font="cambria 15").pack()

            # Create the options menu for screen sizes
            OptionMenu(self.settings_frame, variable, "Even Smaller", "Smaller", "Default",
                       "Larger", "Even Larger", command=self.updateSettings).pack(fill='both')

            # Create the button to get back to the game
            Button(self.settings_frame, text="Register", width=(self.width-self.margin)//2, height=self.margin,
                   bg='#ffffff', activebackground='#ffffff', relief='solid', command=self.closeSettings).pack()

            # Let the frame be fully filled
            self.settings_frame.pack_propagate(0)

    def closeSettings(self):
        # Restart the timer
        self.timer["Pause"] = False

        # Clear out the settings frame
        self.settings_frame.destroy()
        self.settings_frame = None

        # Re-initialize the game screen
        self.initBoard()
        self.initMenu()

        # Start-up the timer
        self.updateTimer()

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
        self.margin = int(20 * self.screen_size)  # Space around the board
        # Dimension of every board cell.
        self.cell_dim = int(50 * self.screen_size)
        self.width = self.height = self.margin * 2 + self.cell_dim * \
            self.board_size  # Width and height of the whole board
        self.menu = self.margin * 2 + self.cell_dim * 2  # Extra space for the menu
        root.geometry(str(self.width) + "x" + str(self.height +
                                                  self.menu) + "+1000+200")  # Window Size


# Initialize root window
root = Tk()
# Initialize GUI Class
GameGUI(root)
# Instigate Loop
root.mainloop()
