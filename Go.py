from tkinter import *
from Constants import *
from copy import deepcopy

class Go:
    mode        = (HUMAN, HUMAN)                # Indicates if the game is HUMAN vs HUMAN or HUMAN vs AI or AI vs AI 
    status      = [[FREE]*9 for _ in range(9)]  # Hold the current status of the game
    prev_status = [[None]*9 for _ in range(9)]  # Hold the previous status of the game
    stone       = [[None]*9 for _ in range(9)]  # (GUI purpose) Hold IDs of stones on the canvas 
    prev_stone  = (None, None)                  # (GUI purpose) Hold ID of the previous stone that the mouse hovered by
    over        = False                         # If game is over => over = True
    turn        = PLAYER_1                      # Indicates game's turn. Initially, it's PLAYER_1's 

    def __init__(self, game_mode = (HUMAN, HUMAN), display = True):
        self.game_mode = game_mode
        # User can decide to turn on or off the display to enhance processing speed
        # For example: in AI vs AI training mode, turning on the display may not be necessary
        if display:
            self.draw_window()
            self.draw_menu()
            self.draw_board()
            self.draw_stones()

        # Graphical input only needed if one of the player is HUMAN
        if self.game_mode != (AI, AI):
            self.init_graphical_input()



    def draw_window(self):
        # Create Tk object
        self.root = Tk()

        # Settings
        self.root.title('GiangGo')
        self.root.config(width = SCREEN_W, height = SCREEN_H, bg = 'white')
        self.root.resizable(False, False)



    def draw_menu(self):
        # Create menu widget
        self.main_menu = Menu(self.root)

        # Create tabs
        self.main_menu.add_command(label = 'New game', command = self.new_game)
        self.main_menu.add_command(label = 'Open game', command = self.open_game)
        self.main_menu.add_command(label = 'Save game', command = self.save_game)
        self.main_menu.add_command(label = 'About', command = self.about)

        # Display menu
        self.root.config(menu = self.main_menu)



    def draw_board(self):
        # Create canvas widget
        self.canvas = Canvas(self.root, width = CANVAS_W, height = CANVAS_H, bg = 'white')
        self.canvas.place(relx = 0.5, rely = 0.5, anchor = CENTER)

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




    def draw_stones(self):
        self.stone = [[self.canvas.create_oval(X0 - B_R/2 + (CELL_W)*j,
                                                Y0 - B_R/2 + (CELL_W)*i,
                                                X0 + B_R/2 + (CELL_W)*j,
                                                Y0 + B_R/2 + (CELL_W)*i,
                                                FREE_CONFIG,
                                                tags = 'stone') 
                                                for j in range(9)]
                                                for i in range(9)]



    def init_graphical_input(self):
        # Hover effect
        def motion(event):
            config = self.canvas.itemconfig
            curr_i = int((event.y - Y0 + CELL_H/2)/CELL_H)
            curr_j = int((event.x - X0 + CELL_W/2)/CELL_W)

            # If previous position is stone-free, terminate previous hover effect
            if None not in self.prev_stone:
                prev_i, prev_j = self.prev_stone
                if self.status[prev_i][prev_j] == FREE:
                    config(self.stone[prev_i][prev_j], FREE_CONFIG)

            # If current position is stone-free, display hover effect
            if self.is_inside(event.x, event.y) and self.status[curr_i][curr_j] == FREE:
                self.prev_stone = (curr_i, curr_j)
                config(self.stone[curr_i][curr_j], BLACK_CONFIG if self.turn else WHITE_CONFIG)

        self.canvas.bind('<Motion>', lambda event : motion(event))
        self.canvas.tag_bind('stone', '<Button-1>', self.read_graphical_input) 

    def read_console_input(self, move):
        config  = self.canvas.itemconfig

        self.prev_status = deepcopy(self.status)
        # Update data
        print(move)
        self.status[move[0]][move[1]] = BLACK if self.turn else WHITE
        # Update GUI
        config(self.stone[move[0]][move[1]], BLACK_CONFIG if self.turn else WHITE_CONFIG)

        self.turn = not self.turn

    def read_graphical_input(self, event):
        #if self.legit_move():
        self.prev_status = deepcopy(self.status)

        config  = self.canvas.itemconfig
        i = int((event.y - Y0 + CELL_H/2)/CELL_H)
        j = int((event.x - X0 + CELL_W/2)/CELL_W)

        if self.is_inside(event.x, event.y) and self.status[i][j] == FREE:
            # Update data
            self.status[i][j] = BLACK if self.turn else WHITE
            # Update GUI
            config(self.stone[i][j], BLACK_CONFIG if self.turn else WHITE_CONFIG)
        self.turn = not self.turn

    def make_move(self, player = 1, move = (-1, -1)):
        pass

    def new_game(self):
        pass

    def open_game(self):
        pass

    def save_game(self):
        pass

    def about(self):
        pass

    def is_inside(self, x, y): # Check if the mouse lie inside the game board
        return X0 - CELL_W/2 < x < X0 + BOARD_W + CELL_W/2 and \
               Y0 - CELL_H/2 < y < Y0 + BOARD_H + CELL_H/2

    def get_status(self): # Return a 82-long integer list. First number indicates self.over
        current_status = [int(self.over)]
        for i in range(9):
            for j in range(9):
                current_status.append(self.status[i][j])

        return current_status

    def update(self): # Update GUI display
        self.root.update()
