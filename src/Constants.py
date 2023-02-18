import os

# GUI Window parameters
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
HEADING_Y = 25 # Y Position of the heading on pages

# Fonts definition
MENU_FONT = ('Helvetica bold', 18)
HEADING_FONT = ('Helvetica bold', 14)
STD_FONT = ('Helvetica bold', 11)
NAV_BTN_FONT = ('Helvetica bold', 14)
API_BTN_FONT = ('Helvetica bold', 13)
DROP_DOWN_LABEL_FONT = ('Helvetica bold', 13)

# Colours definition
BLACK = "#000000"
WHITE = "#FFFFFF"
DARK_GREY = "#18191A"
HOT_PINK = "#FF69B4"
DARK_PINK = "#E75480"
TURQUOISE = "#30D5C8"
LIGHT_GREY = "#bebebe"

# WSU Colours definition
WSU_CRIMSON = "#990033"
WSU_BLACK = "#262223"
WSU_ORANGE = "#FF5C5E"


# These are not constant as they may be manipulated in the GUI (e.g. Dark Mode edits these)
BGND_COL = WSU_CRIMSON
TEXT_COL = WSU_BLACK
BTN_COL = WSU_ORANGE
TEXT_INPT_BG = LIGHT_GREY
TEXT_INPT_FG = DARK_GREY

# Macro Defintions
SUCCESS = True
NOSUCCESS = False


# Folder Paths
UI_FOLDER = "{}\\SDRoster\\UI\\".format(os.getcwd())
DATA_FOLDER = "{}\\SDRoster\\data\\".format(os.getcwd())
SRC_FOLDER = "{}\\SDRoster\\src\\".format(os.getcwd())
CNFG_FOLDER = "{}\\SDRoster\\config\\".format(os.getcwd())
