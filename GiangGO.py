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
HUMAN_VS_HUMAN  = 0
HUMAN_VS_AI     = 1
AI_VS_AI        = 2

# 

class Go:
    def __init__(self):
        # Internal variables
        self.h_lines = [None]*9
        self.v_lines = [None]*9
        self.mode = HUMAN_VS_HUMAN


        # Main window
        self.root = Tk()
        self.root.title('GiangGo')
        self.root.config(width = SCREEN_W, height = SCREEN_H, bg = 'white')
        self.root.resizable(False, False)


        # Menu
        self.main_menu = Menu(self.root)
        self.main_menu.add_command(label = 'New game')
        self.main_menu.add_command(label = 'Open game')
        self.main_menu.add_command(label = 'Save game')
        self.main_menu.add_command(label = 'About')
        self.root.config(menu = self.main_menu)


        # Main canvas
        self.canvas = Canvas(self.root, width = CANVAS_W, height = CANVAS_H, bg = 'white')
        def setup_board():                  # This will be the static elements of the game
            x_0 = (CANVAS_W - BOARD_W)/2    # Begin x, y coordinates
            y_0 = (CANVAS_H - BOARD_H)/2
            x_n = x_0 + BOARD_W             # End x,y coordinates
            y_n = y_0 + BOARD_H
            r = 7                           # Star points radius

            # Draw lines
            for i in range(9):
                self.v_lines[i] = self.canvas.create_line(x_0 + (BOARD_W/8)*i, y_0, x_0 + (BOARD_W/8)*i, y_n)
                self.h_lines[i] = self.canvas.create_line(x_0, y_0 + (BOARD_H/8)*i, x_n, y_0 + (BOARD_H/8)*i)
    
                # Border lines must be bolder
                [self.canvas.itemconfig(i, width = 3) for i in [self.v_lines[0], self.v_lines[8], self.h_lines[0], self.h_lines[8]]]
            
            # Draw star points
            for i in [2, 6]:
                for j in [2, 6]: 
                    self.canvas.create_oval(x_0 - r/2 + (BOARD_W/8)*j, y_0 - r/2 + (BOARD_W/8)*i, x_0 + r/2 + (BOARD_W/8)*j, y_0 + r/2 + (BOARD_W/8)*i, fill = 'black')
            self.canvas.create_oval(x_0 - r/2 + (BOARD_W/8)*4, y_0 - r/2 + (BOARD_W/8)*4, x_0 + r/2 + (BOARD_W/8)*4, y_0 + r/2 + (BOARD_W/8)*4, fill = 'black')
            
            
        setup_board()


        # Display all widgets
        self.canvas.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    def new_game(self):
        pass



master = Go()
master.root.mainloop()
