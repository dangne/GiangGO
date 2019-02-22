import datetime
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from copy import deepcopy
from time import sleep
from Constants import *

class Go:
    # Game data:
    status      = [[FREE]*9 for _ in range(9)]  # Hold the current status of the game
    prev_status = [[None]*9 for _ in range(9)]  # Hold the previous status of the game
    stone       = [[None]*9 for _ in range(9)]  # (GUI purpose) Hold IDs of stones on the canvas 
    prev_stone  = (None, None)                  # (GUI purpose) Hold ID of the previous stone that the mouse hovered by
    over        = False                         # If game is over => over = True
    turn        = PLAYER_1                      # Indicates game's turn. Initially, it's PLAYER_1's 
    pass_cnt    = 0                             # Count the passes, if 2 then game_over
    is_resign   = False                         # Indicates if one player decided to resign
    replay      = True                          # Indicates if user want to replay

    def __init__(self, game_mode, display, delay):
        self.game_mode      = game_mode
        self.display        = display
        self.delay          = delay
        '''
        In AI vs AI training mode:
            No display
            No delay
            No pause
        '''
        if self.display:
            self.draw_window()
            self.draw_menu()
            self.draw_board()
            self.draw_stones()
            self.draw_text()
            self.draw_buttons()

        # Graphical input only needed if one of the player is HUMAN
        if self.game_mode != (AI, AI):
            self.init_graphical_input()

        # Win count window
        if self.display == True and self.delay == False:
            self.init_win_count()



    ##### GAME INTERFACE
    def draw_window(self):
        # Create Tk object
        self.root = Tk()

        COMSCREEN_W = self.root.winfo_screenwidth()
        COMSCREEN_H = self.root.winfo_screenheight()
        X_CENTER    = (COMSCREEN_W - SCREEN_W)/2
        Y_CENTER    = (COMSCREEN_H - SCREEN_H*1.05)/2

        # Settings
        self.root.title('GiangGo')
        self.root.config(bg = 'white')
        self.root.geometry("%dx%d%+d%+d" % (SCREEN_W, SCREEN_H, X_CENTER, Y_CENTER))
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
        self.canvas.place(x = 0, y = 0)

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
        # Initially, all stones are invisible (FREE_CONFIG)
        self.stone = [[self.canvas.create_oval(X0 - B_R/2 + (CELL_W)*j,
                                               Y0 - B_R/2 + (CELL_W)*i,
                                               X0 + B_R/2 + (CELL_W)*j,
                                               Y0 + B_R/2 + (CELL_W)*i,
                                               FREE_CONFIG,
                                               tags = 'stone') 
                                               for j in range(9)]
                                               for i in range(9)]



    def draw_text(self):
        rate = 0.85
        # Coordinates
        for i in range(9):
            # Horizontal coordiantes
            self.canvas.create_text(X0 + CELL_W*i,
                                    Y0 - CELL_H*rate,
                                    text = str(chr(ord('A') + i)),
                                    font = COORDINATE_FONT) 

            self.canvas.create_text(X0 + CELL_W*i,
                                    YN + CELL_H*rate,
                                    text = str(chr(ord('A') + i)),
                                    font = COORDINATE_FONT) 
            
            # Vertical coordiantes
            self.canvas.create_text(X0 - CELL_W*rate,
                                    Y0 + CELL_H*i,
                                    text = str(i),
                                    font = COORDINATE_FONT) 

            self.canvas.create_text(XN + CELL_W*rate,
                                    Y0 + CELL_H*i,
                                    text = str(i),
                                    font = COORDINATE_FONT) 



    def draw_buttons(self):
        # Small trick to ensure buttons' dimensions in pixel
        def make_button(master, x, y, w, h, *args, **kwargs):
            # Create a frame (which it uses pixel length unit)
            frame = Frame(master, width = w, height = h) 
            frame.pack_propagate(False)
            frame.place(x = x, y = y)

            # Then create a button that fill the whole frame's space
            button = Button(frame, *args, **kwargs)
            button.pack(fill = BOTH, expand = 1)
            return button

        x = (SCREEN_W - 2*BUTTON_W)/3
        y = (SCREEN_H - BUTTON_H - CANVAS_H)/2 + CANVAS_H
        # Pass button
        self.pass_button = make_button(self.root,
                                       x = x,
                                       y = y,
                                       w = BUTTON_W,
                                       h = BUTTON_H,
                                       bg = 'white',
                                       text = 'PASS',
                                       command = self.pass_b)

        # Resign button
        self.resign_button = make_button(self.root,
                                       x = 2*x + BUTTON_W,
                                       y = y,
                                       w = BUTTON_W,
                                       h = BUTTON_H,
                                       bg = 'white',
                                       text = 'RESIGN',
                                       command = self.resign_b)



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



    def init_win_count(self):
        # Win counter window
        self.win_count = Toplevel(bg = 'white') 
        self.win_count.title("Win counter") 
        self.win_count.resizable(True, False)

        # Player 1's number of win
        self.P1_win = StringVar()
        self.P1_win.set('0') 
        Label(self.win_count, text = "Player 1 win: ", bg = 'white').grid(row = 0, column = 0)
        self.P1_text = Label(self.win_count, textvariable = self.P1_win, bg = 'white')
        self.P1_text.grid(row = 0, column = 1)

        # Player 2's number of win
        self.P2_win = StringVar()
        self.P2_win.set('0') 
        Label(self.win_count, text = "Player 2 win: ", bg = 'white').grid(row = 1, column = 0)
        self.P2_text = Label(self.win_count, textvariable = self.P2_win, bg = 'white')
        self.P2_text.grid(row = 1, column = 1)

        # Number of even
        self.even = StringVar()
        self.even.set('0') 
        Label(self.win_count, text = "Even: ", bg = 'white').grid(row = 2, column = 0)
        self.even_text = Label(self.win_count, textvariable = self.even, bg = 'white')
        self.even_text.grid(row = 2, column = 1)



    def new_game(self):
        self.status         = [[FREE]*9 for _ in range(9)]  # Hold the current status of the game
        self.prev_status    = [[None]*9 for _ in range(9)]  # Hold the previous status of the game
        self.over           = False                         # If game is over => over = True
        self.turn           = PLAYER_1                      # Indicates game's turn. Initially, it's PLAYER_1's 
        self.pass_cnt       = 0
        self.is_resign      = False
        self.replay      = True

        for i in range(9):
            for j in range(9):
                self.canvas.itemconfig(self.stone[i][j], FREE_CONFIG)



    def open_game(self):
        # Open file dialog
        filename = askopenfilename(initialdir = "./",
                                   initialfile = initialname,
                                   filetypes = (("Text File", "*.txt"), ("All Files","*.*")),
                                   title = "Choose a file.")

        if len(filename) > 0: # Handling the case when user hit "Cancel"
            try:
                data_in = open(filename, 'r')
    
                # Reset game
                self.new_game()
    
                # Read game turn information
                self.turn = bool(int(data_in.readline()[0]))
    
                # Read game status information
                for i in range(9):
                    data = data_in.readline()
                    # Remove endline character
                    self.status[i] = list(map(int, data[:len(data)-1]))
    
                # Update GUI
                for i in range(9):
                    for j in range(9):
                        self.canvas.itemconfig(self.stone[i][j], [FREE_CONFIG, BLACK_CONFIG, WHITE_CONFIG][self.status[i][j]]) 
            except:
                print("An error occurred. Make sure your file exists.")


    def save_game(self):
        '''
        Data format
        1st line:           A single 0 or 1         (1 = black's turn, 0 = white's turn)
        2nd - 10th line:    9x9 grid of integers    (indicates status of the game)
        '''

        # Define default save name
        t = datetime.datetime.now()
        initialname = "game.record"
        for i in [t.day, t.month, t.year, t.hour, t.minute, t.second, 'txt']:
            initialname += '.' + str(i)

        # Save file dialog
        filename = asksaveasfilename(initialdir = "./",
                                     initialfile = initialname,
                                     filetypes = (("Text File", "*.txt"), ("All Files","*.*")),
                                     title = "Choose a file.")

        if len(filename) > 0: # Handling the case when user hit "Cancel"
            data_out = open(filename, "w")
    
            # Write turn information
            data_out.write(str(int(self.turn)) + '\n')
    
            # Write status information
            for i in range(9):
                for j in range(9):
                    data_out.write(str(self.status[i][j]))
                data_out.write('\n')

            # Announcement
            print("Game is saved")



    def about(self):
        self.about_tab = Toplevel(bg = 'white') 
        self.about_tab.title("About") 
        self.about_tab.geometry("%dx%d" % (POPUP_W, POPUP_H))
        self.about_tab.resizable(False, False)

        about_content = \
"""\
----------------------------------------------------------
|   ABOUT                                                |
----------------------------------------------------------

Authors:        Nguyen Minh Dang
                Nguyen Duc Khoi
Institution:    Ho Chi Minh City University of Technology
Contact:        harrynguyen2769@gmail.com
                khoi.nguyenucd@hcmut.edu.vn




----------------------------------------------------------
|   GAME INFORMATION                                     |
----------------------------------------------------------

Board size:     9x9
Game rule:      Chinese
Handicap:       No 
"""

        self.about_message = Text(self.about_tab, bg = 'white')
        self.about_message.insert(INSERT, about_content)
        self.about_message.pack(side = LEFT, fill = BOTH)
        self.about_message.config(state = DISABLED)



    def pass_b(self):
        self.pass_cnt += 1
        self.turn = not self.turn

        # If two consecutive passes -> Game over
        if self.pass_cnt >= 2:
            self.over = True
            self.result_and_replay()



    def resign_b(self):
        self.is_resign = self.over = True



    def result_and_replay(self):
        # Decide who is the winner
        if self.is_resign:
            win = '2' if self.turn else '1'
        else:
            if self.black_score == self.white_score:
                win = 0
            else:
                win = '2' if self.white_score > self.black_score else '1'

        if self.delay:
            # Show pop-up window
            if win == 0:
                text = 'BOTH PLAYERS ARE EVEN\nReplay?'
            else:
                text = 'PLAYER ' + win + ' WIN!\nReplay?'
            self.replay = messagebox.askyesno("Announcement", text)
        else:
            # Show win counter window
            if win == '1':
                temp = int(self.P1_win.get()) + 1
                print(temp)
                self.P1_win.set(str(temp))
            elif win == '2':
                temp = int(self.P2_win.get()) + 1
                print(temp)
                self.P2_win.set(str(temp))
            else:
                temp = int(self.even.get()) + 1
                print(temp)
                self.even.set(str(temp))
            self.win_count.update()


    
        print("Winner: " + str(win))
        if self.replay:
            self.new_game()



    ##### GAME ENGINE
    def read_console_input(self, move):
        # This method verifies validity for console input moves 
        if move == (9, 9): # Pass 
            self.pass_b()
        elif not self.valid_move(move):
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
        def is_alive(x, y):
            # Use BFS algorithm to check for alive condition
            if not all(0 <= i <= 8 for i in (x, y)): return False
            if self.temp_status[x][y] == FREE: return True
            if self.visited[x][y] or self.temp_status[x][y] != self.color: return False
            self.visited[x][y] = True
            return any(is_alive(x + i, y + j) for (i, j) in ((0, -1), (0, 1), (-1, 0), (1, 0)))
             
        # First, check for elementary conditions
        i, j = move
        if not (all(0 <= _ <= 8 for _ in move) and self.status[i][j] == FREE):
            return False

        self.temp_status        = deepcopy(self.status)
        self.temp_status[i][j]  = BLACK if self.turn else WHITE

        # Second, if pass, check for capture_success 
        if self.capture():
            # If capture success, check for Ko rule 
            return self.prev_status != self.temp_status 
        else:
            # If capture fail, check for alive condition
            self.visited = [[False]*9 for _ in range(9)]
            self.color   = BLACK if self.turn else WHITE 
            return is_alive(i, j)



    def make_move(self, move):
        # IMPORTANT!
        # Call this method only when a move is verified as a valid move 
        i, j = move

        # Announce 
        print('=> Player ' + str(2 - self.turn) + ' played at (' + str(i) + ',' + str(j) + ')\n')

        # Record result (For Ko rule)
        self.prev_status    = deepcopy(self.status)
        self.status         = deepcopy(self.temp_status)
        
        # Update GUI
        for i in range(9):
            for j in range(9):
                self.canvas.itemconfig(self.stone[i][j], [FREE_CONFIG, BLACK_CONFIG, WHITE_CONFIG][self.status[i][j]]) 

        # Switch turn
        self.turn = not self.turn

        # Reset pass counter to 0
        self.pass_cnt = 0

        # Delay
        if self.delay:
            sleep(DELAY)



    def capture(self):
        # This method puts all connected stones into one list then kill them all if capture condition is true
        def BFS(x, y):
            if not all(-1 < i < 9 for i in (x, y)):
                return 
            if self.temp_status[x][y] == FREE:
                self.is_captured = False 
            if self.visited[x][y] or self.temp_status[x][y] != self.opponent_color: 
                return
            self.visited[x][y] = True
            self.connected_stones.append((x, y))
            [BFS(x + i, y + j) for (i, j) in ((0, -1), (0, 1), (-1, 0), (1, 0))]

        self.visited             = [[False]*9 for _ in range(9)]
        self.opponent_color      = WHITE if self.turn else BLACK
        self.is_captured         = True
        self.capture_success     = False

        for i in range(9):
            for j in range(9):
                if not self.visited[i][j] and self.temp_status[i][j] == self.opponent_color:
                    self.is_captured         = True
                    self.connected_stones    = []
                    BFS(i, j)
                    if self.is_captured:
                        self.capture_success = True 
                        for _ in self.connected_stones:
                            self.temp_status[_[0]][_[1]] = FREE

        return self.capture_success



    def grouping_area(self, area_check_list, x, y):
        if x<0 or x>8 or y<0 or y>8 or area_check_list[x][y]==1:
            return 0,0,0

        if self.status[x][y]==0:
            area_check_list[x][y]=1
            cu,bu,wu = self.grouping_area(area_check_list,x-1,y)
            cd,bd,wd = self.grouping_area(area_check_list,x+1,y)
            cl,bl,wl = self.grouping_area(area_check_list,x,y-1)
            cr,br,wr = self.grouping_area(area_check_list,x,y+1)
            c=cu+cd+cl+cr
            b=bu|bd|bl|br
            w=wu|wd|wl|wr
            return c+1,b,w

        if self.status[x][y]==1:
            return 0,1,0

        if self.status[x][y]==2:
            return 0,0,1



    def score(self):
        area_check_list=[[0]*9 for _ in range(9)]
        self.black_score=0
        self.white_score=KOMI

        for i in range(9):
            for j in range(9):
                if self.status[i][j]==0 and area_check_list[i][j]==0:
                    c,b,w=self.grouping_area(area_check_list, i, j)
                    if b==1 and w==0:
                        self.black_score+=c 
                    if b==0 and w==1:
                        self.white_score+=c
                if self.status[i][j]==1:
                    self.black_score+=1
                if self.status[i][j]==2:
                    self.white_score+=1
        return self.black_score,self.white_score



    def is_inside(self, x, y): # Check if the mouse lie inside the game board
        return X0 - CELL_W/2 < x < X0 + BOARD_W + CELL_W/2 and \
               Y0 - CELL_H/2 < y < Y0 + BOARD_H + CELL_H/2



    def get_game_data(self):
        '''
        Data format:
            Game status
            Valid moves
            Score
        '''
        # Get valid moves
        self.valid_moves = [(9, 9)]
        [self.valid_moves.append([i, j])
                for j in range(9)
                for i in range(9)
                if self.valid_move((i, j))]

        game_data = [self.status, self.valid_moves, (self.black_score, self.white_score)]
        return game_data



    def update(self): # Update GUI display
        self.root.update()
