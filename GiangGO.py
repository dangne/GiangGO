
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
