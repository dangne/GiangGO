# Date created: 29/01/2019
# This game I made in the progress of making the Go playing Machine Learning (ML) model
# This 9x9 Go game has three modes: Human vs Human, Human vs ML and ML vs ML
# The ML model was implemented seperately from this game
# And For the second and third modes, the ML model will send and receive data from this app through TCP 
# This game acts as a server in this networking model

# Import modules
from tkinter import *
from socket import *

# Constants
SCREEN_W        = 720
SCREEN_H        = 720
CANVAS_W        = SCREEN_W
CANVAS_H        = SCREEN_H
BOARD_W         = CANVAS_W * 0.8
BOARD_H         = CANVAS_H * 0.8
X0              = (CANVAS_W - BOARD_W)/2    # Begin x, y coordinates
Y0              = (CANVAS_H - BOARD_H)/2
XN              = X0 + BOARD_W              # End x,y coordinates
YN              = Y0 + BOARD_H
CELL_W          = BOARD_W/8
CELL_H          = BOARD_H/8
S_R             = SCREEN_W * 0.0075         # Star points radius
B_R             = CELL_W * 0.87             # Bricks radius
HUMAN_VS_HUMAN  = 0
HUMAN_VS_AI     = 1
AI_VS_AI        = 2
FREE            = '_'
FREE_CONFIG     = {'fill' : '', 'width' : 0}
BLACK           = 'black'
BLACK_CONFIG    = {'fill' : 'black', 'width' : 3}
WHITE           = 'white'
WHITE_CONFIG    = {'fill' : 'white', 'width' : 3}

# 

class Go:
    def __init__(self):
        # Internal variables
        self.h_lines        = [None]*9
        self.v_lines        = [None]*9
        self.stones         = [[None]*9 for _ in range(9)]
        self.mode           = HUMAN_VS_HUMAN 
        self.player         = BLACK
        self.prev_stone     = None      # Previous stone that mouse hovered on



        # Main window
        self.root = Tk()
        self.root.title('GiangGo')
        self.root.config(width = SCREEN_W, height = SCREEN_H, bg = 'white')
        self.root.resizable(False, False)
        self.root.bind('<Motion>', lambda event : motion(event))



        # Menu
        self.main_menu = Menu(self.root)
        self.main_menu.add_command(label = 'New game', command = self.new_game)
        self.main_menu.add_command(label = 'Open game')
        self.main_menu.add_command(label = 'Save game')
        self.main_menu.add_command(label = 'About')
        self.root.config(menu = self.main_menu)



        # Main canvas
        self.canvas = Canvas(self.root, width = CANVAS_W, height = CANVAS_H, bg = 'white')
        def setup_board():                  # This will be the static elements of the game
            # Draw lines
            for i in range(9):
                self.v_lines[i] = self.canvas.create_line(X0 + (CELL_W)*i,
                                                          Y0,
                                                          X0 + (CELL_W)*i, 
                                                          YN)
                self.h_lines[i] = self.canvas.create_line(X0,
                                                          Y0 + (CELL_H)*i,
                                                          XN,
                                                          Y0 + (CELL_H)*i)
                # Border lines must be bolder
                [self.canvas.itemconfig(i, width = 3) for i in [self.v_lines[0], self.v_lines[8],
                                                                self.h_lines[0], self.h_lines[8]]]

            # Draw star points
            for i in [2, 6]:
                for j in [2, 6]: 
                    self.canvas.create_oval(X0 - S_R/2 + (CELL_W)*j, 
                                            Y0 - S_R/2 + (CELL_W)*i,
                                            X0 + S_R/2 + (CELL_W)*j, 
                                            Y0 + S_R/2 + (CELL_W)*i,
                                            fill = 'black')
            self.canvas.create_oval(X0 - S_R/2 + (CELL_W)*4,
                                    Y0 - S_R/2 + (CELL_W)*4, 
                                    X0 + S_R/2 + (CELL_W)*4,
                                    Y0 + S_R/2 + (CELL_W)*4, 
                                    fill = 'black')
        setup_board()
            


        # Bricks manager
        for i in range(9):
            for j in range(9):
                self.stones[i][j] = self.canvas.create_oval(X0 - B_R/2 + (CELL_W)*j,
                                                            Y0 - B_R/2 + (CELL_W)*i,
                                                            X0 + B_R/2 + (CELL_W)*j,
                                                            Y0 + B_R/2 + (CELL_W)*i,
                                                            FREE_CONFIG,
                                                            tags = ('stone', FREE))
        self.canvas.tag_bind('stone', '<Button-1>', lambda event : click(event))


        def motion(event):
            cget    = self.canvas.itemcget 
            config  = self.canvas.itemconfig

            if self.prev_stone != None and FREE in cget(self.prev_stone, 'tags'):
                config(self.prev_stone, FREE_CONFIG)
            if X0 - CELL_W/2 < event.x < X0 + BOARD_W + CELL_W/2 and Y0 - CELL_H/2 < event.y < Y0 + BOARD_H + CELL_H/2:
                i = int((event.y - Y0 + CELL_H/2)/CELL_H)
                j = int((event.x - X0 + CELL_W/2)/CELL_W)
                if FREE in cget(self.stones[i][j], 'tags'):
                    self.prev_stone = self.stones[i][j]
                    config(self.stones[i][j], BLACK_CONFIG if self.player == BLACK else WHITE_CONFIG)

        def click(event):
            cget    = self.canvas.itemcget 
            config  = self.canvas.itemconfig

            if X0 - CELL_W/2 < event.x < X0 + BOARD_W + CELL_W/2 and Y0 - CELL_H/2 < event.y < Y0 + BOARD_H + CELL_H/2:
                i = int((event.y - Y0 + CELL_H/2)/CELL_H)
                j = int((event.x - X0 + CELL_W/2)/CELL_W)
                if FREE in cget(self.stones[i][j], 'tags'):
                    config(self.stones[i][j], BLACK_CONFIG if self.player == BLACK else WHITE_CONFIG, tags = BLACK if self.player == BLACK else WHITE)
                    self.player = BLACK if self.player == WHITE else WHITE

        # Display all widgets
        self.canvas.place(relx = 0.5, rely = 0.5, anchor = CENTER)



    def new_game(self):
        self.player = BLACK
        for i in range(9):
            for j in range(9):
                self.canvas.itemconfig(self.stones[i][j], FREE_CONFIG, tags = ('stone', FREE))

master = Go()
master.root.mainloop()

'''
Todo list:
    - Structurize code
    - Complete Human vs AI and AI vs AI mode
    - Complete "Open game"
    - Complete "Save game"
    - Complete "About"
'''
