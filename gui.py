# Import Necessary Libraries
from tkinter import Tk, Frame, Canvas
from PIL import ImageTk, Image

# Import Other Files
import importlib  
algo = importlib.import_module("sudoku-solver")

class gameGUI(Frame):
    def __init__(self, parent):
        # Configure GUI dimensions
        self.multi = 1 # 0.8, 1, 1.2
        self.margin = int(20 * self.multi) # Pixels around the board
        self.side = int(50 * self.multi) # Width of every board cell.
        self.width = self.height = self.margin * 2 + self.side * 9  # Width and height of the whole board
        self.menu = self.margin * 2 + self.side * 2

        # Configure parent of game frame
        self.parent = parent
        Frame.__init__(self, parent, bg="white")
        self.parent.title("Sudoku")
        self.parent.iconbitmap("grid.ico")
        self.pack(fill='both', expand=1)
        self.parent.geometry(str(self.width) + "x" + str(self.height + self.menu) + "+1000+200")
        self.parent.resizable(0,0)

        # Initialize puzzle variables
        self.row, self.col = 0, 0
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
        self.drawGrid()
        self.drawPuzzle()

        # Bind keys to the canvas for tracking
        self.game_canvas.bind("<Button-1>", self.cellClicked)
        self.game_canvas.bind("<Key>", self.keyPressed)
    
    def drawGrid(self):
        pass

    def drawPuzzle(self):
        pass

    def cellClicked(self, event):
        pass

    def keyPressed(self, event):
        pass

# Initialize root window
root = Tk()
# Initialize GUI Class
gameGUI = gameGUI(root)
# Instigate Loop
root.mainloop()