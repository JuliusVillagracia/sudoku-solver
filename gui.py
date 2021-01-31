# Import Necessary Libraries
from tkinter import Tk, Frame, Canvas, Button
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
        self.drawGrid()
        self.drawPuzzle()

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
        self.game_canvas.delete("lines")
        for i in range(10):
            color = "black" if i % 3 == 0 else "gray"
            w = 3 if i % 3 == 0 else 1

            x0 = self.margin + i * self.side
            y0 = self.margin
            x1 = self.margin + i * self.side
            y1 = self.height - self.margin
            self.game_canvas.create_line(x0, y0, x1, y1, width=w, fill=color, tags="lines")

            x0 = self.margin
            y0 = self.margin + i * self.side
            x1 = self.width - self.margin
            y1 = self.margin + i * self.side
            self.game_canvas.create_line(x0, y0, x1, y1, width=w, fill=color, tags="lines")

    def drawPuzzle(self):
        pass

    def cellClicked(self, event):
        pass

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

# Initialize root window
root = Tk()
# Initialize GUI Class
gameGUI = gameGUI(root)
# Instigate Loop
root.mainloop()