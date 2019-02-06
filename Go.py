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
    move_count  = 0

    def __init__(self, game_mode, display = True):
        self.game_mode = game_mode
        # User can decide to turn on or off the display to enhance processing speed
        # For example: in AI vs AI training mode, turning on the display may not be necessary
        if display:
            self.draw_window()
            self.draw_menu()
            self.draw_board()
            self.draw_stones()
            self.draw_text()

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



    def draw_text(self):
        for i in range(9):
            self.canvas.create_text(X0 + CELL_W*i, Y0 - CELL_H/3, text = str(i))
            self.canvas.create_text(X0 - CELL_W/3, Y0 + CELL_H*i, text = str(i))

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
        # This method verifies validity for console input moves 
        if not self.valid_move(move):
            print("Invalid move. Please try again.")
        else:
            self.make_move(move)



    def read_graphical_input(self, event):
        # This method verifies validity for graphical input moves 
        i = int((event.y - Y0 + CELL_H/2)/CELL_H)
        j = int((event.x - X0 + CELL_W/2)/CELL_W)

        if not (self.is_inside(event.x, event.y) and self.valid_move((i, j))):
            print("Invalid move. Please try again.")
        else:
            self.make_move((i,j))



    def valid_move(self, move):
        # First, check for elementary conditions
        (i, j) = move
        if not (all(0 <= _ <= 8 for _ in move) and self.status[i][j] == FREE):
            return False

        self.temp_status        = deepcopy(self.status)
        self.temp_status[i][j]  = BLACK if self.turn else WHITE


        # Second, if pass, check for capture_success 
        if self.capture_check():
            # If capture success, check for Ko rule 
            return self.prev_status != self.temp_status 
        else:
            # If capture fail, check for liberties
            #opponent_color  = WHITE if self.turn else BLACK
            color           = BLACK if self.turn else WHITE
            self.visited    = [[False]*9 for _ in range(9)]
            self.capture_success = True
            self.live_check(color, i, j)

            # If capture_success == fail then the stone lives => valid move
            return not self.capture_success



    def make_move(self, move):
        # IMPORTANT!
        # Call this method only when a move is verified as a valid move 
        (i, j) = move

        # Announce 
        self.move_count += 1
        print(str(self.move_count) + '. Player ' + str(2 - self.turn) + ' played at (' + str(i) + ',' + str(j) + ')')

        # Record result (For Ko rule)
        self.prev_status    = deepcopy(self.status)
        self.status         = deepcopy(self.temp_status)
        
        # Update GUI
        for i in range(9):
            for j in range(9):
                self.canvas.itemconfig(self.stone[i][j], [FREE_CONFIG, BLACK_CONFIG, WHITE_CONFIG][self.status[i][j]]) 

        # Switch turn
        self.turn = not self.turn



    def live_check(self, opponent_color, x, y):
        if not all(0 <= i <= 8 for i in (x, y)) or self.visited[x][y]:
            return 

        if self.temp_status[x][y] == FREE:
            self.capture_success = False
            return
        else:
            self.visited[x][y] = True

        if self.temp_status[x][y] != opponent_color:
            return 
        [self.live_check(opponent_color, x+i, y+j) for (i, j) in ((0,-1), (0,1), (-1,0), (1,0))]
        if self.capture_success:
            self.temp_status[x][y] = FREE



    def capture_check(self):
        self.visited        = [[False]*9 for _ in range(9)]
        self.live_status    = [[True]*9 for _ in range(9)]
        success             = False
        opponent_color      = WHITE if self.turn else BLACK

        for i in range(9):
            for j in range(9):
                if not self.visited[i][j] and self.temp_status[i][j] == opponent_color:
                    self.capture_success = True
                    self.live_check(opponent_color, i, j)
                    if self.capture_success:
                        success = True 

        return success


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
