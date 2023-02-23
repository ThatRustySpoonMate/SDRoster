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
WARN_FONT = ('Helvetica bold', 13)

# Colours definition
BLACK = "#000000"
WHITE = "#FFFFFF"
DARK_GREY = "#18191A"
HOT_PINK = "#FF69B4"
DARK_PINK = "#E75480"
TURQUOISE = "#30D5C8"
LIGHT_GREY = "#bebebe"
MEDIUM_GREY = "#7D7F7C"
DARK_SLATE_BLUE = "#06394f"
CHEESE_YELLOW = "#ffa600"

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
NAV_BAR_COL = LIGHT_GREY 
NAV_BAR_SUBSECT_COL = MEDIUM_GREY

# Macro Defintions
SUCCESS = True
NOSUCCESS = False


# Folder Paths
UI_FOLDER = "{}\\UI\\".format(os.getcwd())
DATA_FOLDER = "{}\\data\\".format(os.getcwd())
SRC_FOLDER = "{}\\src\\".format(os.getcwd())
CNFG_FOLDER = "{}\\config\\".format(os.getcwd())


# Placement of dynamic content on lunch/chat/pendings pages
staffDisplayCol0 = 150 # Starting X position of col0 staff lunch
staffDisplayCol1 = WINDOW_WIDTH / 2 + staffDisplayCol0 # Starting X position of col1 staff lunch
staffDisplayStartY = 100 # Starting Y position of col0 row0 staff lunch
staffDisplayIncrementY = 50 # Gap between each row of staff lunches 
staffDisplayDrpDwnOffset = 0 # Gap between start of staff name and start of drop-down selector
staffDropDownLabelOffset = 40 # Offset between lunch drop-down menu and their name
staffPixelsPerCharacterOffset = 6 # Move the lunch drop-down menu name this many pixels * length of their name 

