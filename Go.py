from tkinter import *
from socket import *
from GlobalVariables import *

class Go:
    game_over = False
    game_status = [[FREE]*9 for _ in range(9)]
    prev_game_status = [[None]*9 for _ in range(9)]

    def __init__(self, game_mode = HUMAN_VS_HUMAN, display = True):
        def draw_window():
            # Create Tk object
            self.root = Tk()

            # Settings
            self.root.title('GiangGo')
            self.root.config(width = SCREEN_W, height = SCREEN_H, bg = 'white')
            self.root.resizable(False, False)
            #self.root.bind('<Motion>', lambda event : motion(event))

        def draw_menu():
            # Create menu widget
            self.main_menu = Menu(self.root)

            # Create tabs
            self.main_menu.add_command(label = 'New game', command = self.new_game)
            self.main_menu.add_command(label = 'Open game', command = self.open_game)
            self.main_menu.add_command(label = 'Save game', command = self.save_game)
            self.main_menu.add_command(label = 'About', command = self.about)

            # Display menu
            self.root.config(menu = self.main_menu)

        def draw_board():
            # Create canvas widget
            self.canvas = Canvas(self.root, width = CANVAS_W, height = CANVAS_H, bg = 'white')

            # Draw lines
            [[self.canvas.create_line(X0 + (CELL_W)*i,
                                      Y0,
                                      X0 + (CELL_W)*i, 
                                      YN,
                                      width = 3 if i == 0 or i == 8 else 1),
              self.canvas.create_line(X0,
                                      Y0 + (CELL_H)*i,
                                      XN,
                                      Y0 + (CELL_H)*i,
                                      width = 3 if i == 0 or i == 8 else 1)]
                                      for i in range(9)]

            # Draw star points
            [self.canvas.create_oval(X0 - S_R/2 + (CELL_W)*j, 
                                     Y0 - S_R/2 + (CELL_W)*i,
                                     X0 + S_R/2 + (CELL_W)*j, 
                                     Y0 + S_R/2 + (CELL_W)*i,
                                     fill = 'black')
                                     for (i, j) in [(2,2), (2,6), (6,2), (6,6), (4,4)]]

            # Display canvas
            self.canvas.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        
        if display:
            draw_window()
            draw_menu()
            draw_board()
            self.root.mainloop()

    def make_move(self, player = 1, move = (-1, -1)):
        captured = [[False]*9 for _ in range(9)]
        def check_over():
            pass

        def check_capture():
            pass

    def new_game(self):
        pass

    def open_game(self):
        pass

    def save_game(self):
        pass

    def about(self):
        pass

    def is_over(self):
        return self.game_over

    def get_status(self):
        return self.game_status
