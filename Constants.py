# Game dimension 
SCREEN_W        = 648 
SCREEN_H        = 720
CANVAS_W        = SCREEN_W
CANVAS_H        = CANVAS_W
BOARD_W         = CANVAS_W * 0.75
BOARD_H         = CANVAS_H * 0.75
CELL_W          = BOARD_W/8
CELL_H          = BOARD_H/8
S_R             = SCREEN_W * 0.0075         # Star points radius
B_R             = CELL_W * 0.87             # Stones radius
X0              = (CANVAS_W - BOARD_W)/2    # Begin x, y coordinates of game board
Y0              = (CANVAS_H - BOARD_H)/2
XN              = X0 + BOARD_W              # End x,y coordinates of game board
YN              = Y0 + BOARD_H
BUTTON_W        = SCREEN_W*0.35
BUTTON_H        = (SCREEN_H - CANVAS_H)*0.6
POPUP_W         = SCREEN_W/1.25
POPUP_H         = SCREEN_H/2

# Font configurations
COORDINATE_FONT = ("Arial", 15) # Font size of coordinates


FREE            = 0
FREE_CONFIG     = {'fill' : '', 'width' : 0}
BLACK           = 1
BLACK_CONFIG    = {'fill' : 'black', 'width' : 3}
WHITE           = 2
WHITE_CONFIG    = {'fill' : 'white', 'width' : 3}


KOMI            = 7
PLAYER_1        = True
PLAYER_2        = False
HUMAN           = True
AI              = False
PLAYER_COLOR = ['White','Black']

DELAY           = 0.05
