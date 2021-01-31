# Import Necessary Libraries
from tkinter import Tk, Frame, Canvas, Button
from PIL import ImageTk, Image
from copy import deepcopy

# Import Other Files
import importlib  
algo = importlib.import_module("sudoku-solver")

class gameGUI(Frame):
    def __init__(self, parent):
        # Configure board size
        self.board_size = 9

        # Configure GUI dimensions
        self.multi = 1 # 0.8, 1, 1.2
        self.margin = int(20 * self.multi) # Space around the board
        self.cell_dim = int(50 * self.multi) # Dimension of every board cell.
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
        self.game_canvas.delete("locked_cells")

        # Fill in each cell with the puzzle entry from the current puzzle state
        for i in range(self.board_size):
            for j in range(self.board_size):
                # Differently format cell's containing hint entries
                font = "Inconsolata " + str(int(20*self.multi)) + " bold" if self.original_puzzle[i][j] != 0 else "Inconsolata " + str(int(20*self.multi))
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
        
        # Raise the border above the boxes
        self.game_canvas.tag_raise("grid_thick", "locked_cells")
        self.game_canvas.tag_raise("grid_lines", "locked_cells")

    def cellClicked(self, event):
        # Check if the cursor is within the canvas when it clicks
        if self.margin < event.x < self.width - self.margin and self.margin < event.y < self.height - self.margin:
            # Clear the canvas selection before highlighting another
            self.game_canvas.delete("selected_highlight")
            
            # Focus on the canvas for key tracking
            self.game_canvas.focus_set()
            
            # Check which cell is selected_highlight in terms of coordinates
            col = (event.x - self.margin) // self.cell_dim
            row = (event.y - self.margin) // self.cell_dim
            
            # Check if cell clicked is already highlighted or not
            if col != self.col or row != self.row:
                # Loop and create cell highlight borders by side 
                for i in range(4):
                    x0 = event.x - (event.x - self.margin) % self.cell_dim + self.cell_dim if i == 3 else event.x - (event.x - self.margin) % self.cell_dim
                    y0 = event.y - (event.y - self.margin) % self.cell_dim + self.cell_dim if i == 2 else event.y - (event.y - self.margin) % self.cell_dim
                    x1 = event.x - (event.x - self.margin) % self.cell_dim + self.cell_dim if i != 0 else event.x - (event.x - self.margin) % self.cell_dim
                    y1 = event.y - (event.y - self.margin) % self.cell_dim + self.cell_dim if i != 1 else event.y - (event.y - self.margin) % self.cell_dim
                    self.game_canvas.create_line(x0, y0, x1, y1, fill="red", width=3, tags="selected_highlight")
            else:
                # Reset cell coordinates as highlight is removed
                col = row = -1

            # Update the coordinates of the highlighted cell
            self.col = col
            self.row = row
        
        # Check if settings is clicked 
        elif self.width - self.margin < event.x < self.width and 0 < event.y < self.margin:
            self.openSettings()

    def keyPressed(self, event):
        pass

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
        pass

    def resetBoard(self):
        pass

    def generatePuzzle(self):
        pass

    def inputPuzzle(self):
        pass

    def openSettings(self):
        pass

# Initialize root window
root = Tk()
# Initialize GUI Class
gameGUI = gameGUI(root)
# Instigate Loop
root.mainloop()