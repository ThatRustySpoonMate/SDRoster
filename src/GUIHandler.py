import tkinter as tk
from tkinter import ttk # Can be used to stylize widgets, nice to have, I probably wont use it 
from Normies import WSUStaff
import random
import os
from Constants import *
from functools import partial # This is pure magic

# TODO: Expand GUI

class RosterWindow(tk.Tk):

    """
    Args:
    screenName: str | None = None,
    baseName: str | None = None,
    className: str = "Tk",
    useTk: bool = True,
    sync: bool = False,
    use: str | None = None
    """

    def __init__(self, messageToMainFunc, *args, **kwargs):

        global BGND_COL, BTN_COL, TEXT_COL, TEXT_INPT_BG, TEXT_INPT_FG

        self.messageToMainFunc = messageToMainFunc
        tk.Tk.__init__(self, *args, **kwargs)
        self.ShowNavBar = False

        self.EEM = 0 # 0 = Deafult, 1 = Pink text/UI elements, 2 = Uwuify'd text/UI elements
        if("isabel" in os.getlogin().lower()): # Change to Isabel's staff number
            self.EEM = 1  # Isabel Detected
        elif(random.randrange(0, 30) == 23):
            self.EEM = 2  # UWU Mode


        if(self.EEM == 1):
            # Set all colour macros to hot pink
            BGND_COL = DARK_PINK
            TEXT_COL = HOT_PINK
            BTN_COL = HOT_PINK
            TEXT_INPT_BG = DARK_PINK
            TEXT_INPT_FG = HOT_PINK
            

        self.wm_title("Service Desk Daily Roster Generator")

        # Create container for frames (aka menus/pages)
        container = tk.Frame(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0,weight=1)

        # Create and fill dictionary of frames
        self.frames = {}

        for menu in (MainMenu, ConfigurationMenu, LunchRosterMenu, ChatMenu, PendingsMenu, FinalizeMenu):
            frame = menu(container, self)

            self.frames[menu] = frame
            frame.grid(row = 0, column = 0, sticky="nsew")

        
        # After initialization, show main page
        self.show_frame(MainMenu)
        
    
    # Function to put the passed page as the toplevel page in container
    def show_frame(self, page):
        # Get requested frame from dict
        frame = self.frames[page]

        # If this is the first time the frame is loaded, run it's first time function
        if(frame.firstLoad == True):
            frame.onFirstLoad()
        else:
            # Otherwise, redraw it's contents
            frame.clear()
            frame.draw()

        # Bring the frame to the top of the container
        frame.tkraise()



class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        self.darkMode = 0 # Flag for dark mode enabled
        
        self.firstLoad = True # Flag for first time loading of page

        # Add dark mode toggle
        self.darkModeToggle = CreateElement(controller, tk.Button, master=self, text="Enable dark mode", font=STD_FONT, command = self.toggleDarkMode)
        
        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Home", font = MENU_FONT)

        # API Key input
        self.APIKeyHeading = CreateElement(controller, tk.Label, master=self, text = "Enter your Humanity API key below: ", font=HEADING_FONT)
        self.APIKeyInput = CreateElement(controller, tk.Text, master=self, height=1, width=40, font=STD_FONT)
        self.APIKeyLoad = CreateElement(controller, tk.Button, master=self, text = "File: Load", font=API_BTN_FONT, command=lambda:self.requestAPIKey(0))
        self.APIKeyRetrieve = CreateElement(controller, tk.Button, master=self, text = "Web: Retrieve", font=API_BTN_FONT, command=lambda:self.requestAPIKey(1))
        
        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(ConfigurationMenu) )

        

    def onFirstLoad(self):
        # Draw all UI elements to screen
        self.draw()

        self.firstLoad = False
        pass
        
    
    # Removes all UI elements
    def clear(self):
        self.darkModeToggle.place_forget()
        self.pageLabel.place_forget()
        self.APIKeyInput.place_forget()
        self.nextButton.place_forget()
        self.APIKeyLoad.place_forget()
        self.APIKeyRetrieve.place_forget()

    # Renders all UI Elements
    def draw(self):
        self.darkModeToggle.config(text="Enable dark mode" if self.darkMode == 0 else "Disable dark mode")

        self.config(bg=BGND_COL)

        # This is where elements are configured (Colours)
        self.darkModeToggle.config(bg = BGND_COL, fg=BTN_COL)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.APIKeyHeading.config(bg = BGND_COL, fg = TEXT_COL)
        self.APIKeyInput.config(bg = TEXT_INPT_BG, fg = TEXT_INPT_FG)
        self.APIKeyLoad.config(bg= BGND_COL, fg=BTN_COL)
        self.APIKeyRetrieve.config(bg= BGND_COL, fg=BTN_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)


        # This is where elements are placed
        self.darkModeToggle.place(x = WINDOW_WIDTH / 2 - 64, y = WINDOW_HEIGHT - 100)
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 36, y = HEADING_Y)
        self.APIKeyHeading.place(x = WINDOW_WIDTH / 2 - 165, y = HEADING_Y + 70)
        self.APIKeyInput.place(x = WINDOW_WIDTH / 2 - 170, y = HEADING_Y + 100)
        self.APIKeyLoad.place(x = WINDOW_WIDTH / 2 - 100, y = HEADING_Y + 130)
        self.APIKeyRetrieve.place(x = WINDOW_WIDTH / 2 - 0, y = HEADING_Y + 130)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
    
    def requestAPIKey(self, src=0):
        key = ""
        if(src == 0):
            # Requesting API key from file
            key = self.controller.messageToMainFunc(1, 0) # Request main to provide the API key from the file
        else:
            # Requesting API key from Web (Most up to date)
            key = self.controller.messageToMainFunc(1, 1) # Request main to provide the API key from the web browser

        # Once we have received key from main, update key field in GUI
        self.APIKeyInput.delete(1.0, tk.END) # Delete current contents of API key field
        
        self.APIKeyInput.insert(tk.END, key) # Insert received API key



    def toggleDarkMode(self):
        global BGND_COL, BTN_COL, TEXT_COL, TEXT_INPT_FG, TEXT_INPT_BG
        self.darkMode = not self.darkMode # Flip dark mode toggle

        if(self.controller.EEM != 1):
            # Normal mode
            if(self.darkMode == 0): 
                # Disable Dark Mode
                BGND_COL = WSU_CRIMSON
                TEXT_COL = WSU_BLACK
                BTN_COL = WSU_ORANGE
                TEXT_INPT_BG = LIGHT_GREY
                TEXT_INPT_FG = DARK_GREY

            else:
                # Enable Dark Mode
                BGND_COL = DARK_GREY
                BTN_COL = WSU_CRIMSON
                TEXT_COL = LIGHT_GREY
                TEXT_INPT_BG = DARK_GREY
                TEXT_INPT_FG = LIGHT_GREY
        else:
            # Isabel mode
            if(self.darkMode == 0): 
                # Disable Isabel Dark Mode
                BGND_COL = DARK_PINK
                TEXT_COL = HOT_PINK
                BTN_COL = HOT_PINK
                TEXT_INPT_BG = DARK_PINK
                TEXT_INPT_FG = HOT_PINK

            else:
                # Enable IsabelDark Mode
                BGND_COL = HOT_PINK
                TEXT_COL = DARK_PINK
                BTN_COL = DARK_PINK
                TEXT_INPT_BG = HOT_PINK
                TEXT_INPT_FG = DARK_PINK

        self.clear() # Clear the screen 
        self.draw()  # Redraw all elements using new colour scheme

        print(self.controller.messageToMainFunc(0)) # Testing, will delete later
    



class ConfigurationMenu(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        self.firstLoad = True # Flag for first time loading of page
        

        # Set background colour
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Configuration", font = MENU_FONT) 

        self.pageDescriptor = CreateElement(controller, tk.Label, master=self, text="Enter any exceptions to regular rostering here", font=HEADING_FONT)

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(LunchRosterMenu) )
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(MainMenu))
        

    
    def onFirstLoad(self):

        # Draw all UI elements to screen
        self.draw()
        self.firstLoad = False
        


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.pageDescriptor.place_forget()
        self.nextButton.place_forget()
        self.prevButton.place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        # This is where elements are configured (Colours)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.pageDescriptor.config(bg=BGND_COL, fg=TEXT_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)

        # This is where elements are placed
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 80, y = HEADING_Y)
        self.pageDescriptor.place(x = WINDOW_WIDTH / 2 - 190, y = HEADING_Y + 30)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)




class LunchRosterMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        self.firstLoad = True # Flag for first time loading of page
        self.lunchTimes = {} # Dict of all staff and their lunches 
        self.lunchTimeWidgets = {} # dict of staff name as key and array of label, drop-down widget and stringVar literal of the currently selected option e.g. { "ethan":[tk.label, tk.dropDown, StringVar] }
        self.lunch_options = [ # All possible lunch times that will show up in the drop down menu
            None,
            "11:00",
            "11:30",
            "12:00",
            "12:30",
            "1:00",
            "1:30",
            "2:00",
            "2:30",
            "3:00",
            "3:30"
        ]
        

        # Set background colour
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Lunch Roster", font = MENU_FONT) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(ChatMenu) )
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(ConfigurationMenu))



    def onFirstLoad(self):

        # Request a lunch roster to display, this can then be edited by the user
        self.lunchTimes = self.controller.messageToMainFunc(2).copy()
        
        # Create a label and drop down for each staff member (label) and their lunch times (Drop down)
        for staffName in self.lunchTimes:
            setString = tk.StringVar() # Create rkinter variable for the selected drop-down value
            setString.set(self.lunchTimes[staffName]) # Set this variable to this staff members allocated lunch time
            self.lunchTimeWidgets[staffName] = [ CreateElement(self.controller, tk.Label, master=self, text = staffName, font=DROP_DOWN_LABEL_FONT), tk.OptionMenu(self, setString, *self.lunch_options, command = partial(self.updateLunch, staffName)), setString ]
            print(staffName)
        

        # Draw all UI elements to screen
        self.draw()
        self.firstLoad = False


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.nextButton.place_forget()
        self.prevButton.place_forget()

        for staffName in self.lunchTimeWidgets:
            self.lunchTimeWidgets[staffName][0].place_forget()
            self.lunchTimeWidgets[staffName][1].place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        # This is where elements are configured (Colours)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)

        for staffName in self.lunchTimeWidgets:
            self.lunchTimeWidgets[staffName][0].config(bg = BGND_COL, fg=TEXT_COL)
            self.lunchTimeWidgets[staffName][1].config(bg = BGND_COL, fg=TEXT_COL)
            

        # This is where elements are placed
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 80, y = HEADING_Y)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)

        for staffName in self.lunchTimeWidgets:
            self.lunchTimeWidgets[staffName][0].place(x = 150, y = 250)
            self.lunchTimeWidgets[staffName][1].place(x = 200, y = 250)


    def updateLunch(self, staffName, lunchTime):
        print("Updating lunch for {} to {}".format(staffName, lunchTime))
        self.controller.messageToMainFunc(2, (staffName, lunchTime))
        return

        
        

class ChatMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        self.firstLoad = True # Flag for first time loading of page

        # Set background colour
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Chat Roster", font = MENU_FONT) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(PendingsMenu) )
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(LunchRosterMenu))

    
    def onFirstLoad(self):
        # Draw all UI elements to screen
        self.draw()

        self.firstLoad = False
        pass


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.nextButton.place_forget()
        self.prevButton.place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        # This is where elements are configured (Colours)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)

        # This is where elements are placed
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 72, y = HEADING_Y)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)

class PendingsMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        self.firstLoad = True # Flag for first time loading of page

        # Set background colour
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Pendings Roster", font = MENU_FONT) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(FinalizeMenu) )
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(ChatMenu))
        
    
    def onFirstLoad(self):
        # Draw all UI elements to screen
        self.draw()

        self.firstLoad = False
        pass


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.nextButton.place_forget()
        self.prevButton.place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        # This is where elements are configured (Colours)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)


        # This is where elements are placed
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 92, y = HEADING_Y)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)

class FinalizeMenu(tk.Frame): # Overrides and serializing objects etc...

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        self.firstLoad = True # Flag for first time loading of page

        # Set background colour
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Finalisation", font = MENU_FONT) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Navigation buttons
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(PendingsMenu))

    
    def onFirstLoad(self):
        # Draw all UI elements to screen
        self.draw()

        self.firstLoad = False
        pass


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.prevButton.place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)


        # This is where elements are configured (Colours)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)

        # This is where elements are placed
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 70, y = HEADING_Y)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)



# I can't believe I'm doing this for the uwu.
# Way to ruin the nicely laid out UI code :(
def CreateElement(controller, elementType, **kwargs):
    element = elementType(**kwargs)

    if(controller.EEM == 2):
        element.config(fg=GenerateRandomColour())

    return element


def GenerateRandomColour():
    return ("#%06x" % random.randint(0, 0xFFFFFF) )
