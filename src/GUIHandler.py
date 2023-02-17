# TODO: Write GUI
# TODO: Work out fonts
import tkinter as tk
from tkinter import ttk # Can be used to stylize widgets, nice to have, I probably wont use it 
from Normies import WSUStaff
import random
import os
from Constants import *


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

        global BGND_COL, BTN_COL, TEXT_COL

        self.messageToMainFunc = messageToMainFunc
        tk.Tk.__init__(self, *args, **kwargs)
        self.ShowNavBar = False

        self.EEM = 0 # 0 = Deafult, 1 = Pink text/UI elements, 2 = Uwuify'd text/UI elements
        if("isabel" in os.getlogin().lower()):
            self.EEM = 1  # Isabel Detected
        elif(random.randrange(0, 30) == 23):
            self.EEM = 2  # UWU Mode


        if(self.EEM == 1):
            # Set all colour macros to hot pink
            BGND_COL = DARK_PINK
            TEXT_COL = HOT_PINK
            BTN_COL = HOT_PINK
            

        self.wm_title("Service Desk Daily Roster Generator")

        # Create container for frames (aka menus/pages)
        container = tk.Frame(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0,weight=1)

        # Create and fill dictionary of frames
        self.frames = {}

        for menu in (MainMenu, ConfigurationMenu, LunchRosterMenu, ChatMenu, PendingsMenu, OverrideMenu):
            frame = menu(container, self)

            self.frames[menu] = frame
            frame.grid(row = 0, column = 0, sticky="nsew")

        
        # After initialization, show main page
        self.show_frame(MainMenu)
        
    
    # Function to put the passed page as the toplevel page in container
    def show_frame(self, page):
        frame = self.frames[page]
        frame.clear()
        frame.draw()
        frame.tkraise()



class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller
        self.darkMode = 0

        # Add dark mode toggle
        self.darkModeToggle = CreateElement(controller, tk.Button, master=self, text="Enable dark mode", font=STD_FONT, bg = BGND_COL, fg=TEXT_COL, command = self.enableDarkMode)
        
        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Home", font = HEADING_FONT, bg = BGND_COL, fg = TEXT_COL)
        
        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, bg=BGND_COL, fg=BTN_COL, width=2, command = lambda:controller.show_frame(ConfigurationMenu) )

        # Draw all UI elements to screen
        self.draw()
        

    
    # Removes all UI elements
    def clear(self):
        self.darkModeToggle.place_forget()
        self.pageLabel.place_forget()
        self.nextButton.place_forget()


    # Renders all UI Elements
    def draw(self):
        self.darkModeToggle.config(text="Enable dark mode" if self.darkMode == 0 else "Disable dark mode")

        self.config(bg=BGND_COL)

        self.darkModeToggle.config(bg = BGND_COL, fg=TEXT_COL)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)

        self.darkModeToggle.place(x = 30, y = 50)
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 36, y = HEADING_Y)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        

    def enableDarkMode(self):
        global BGND_COL, BTN_COL, TEXT_COL, x
        self.darkMode = not self.darkMode # Flip dark mode toggle

        if(self.controller.EEM != 1):
            # Normal mode
            if(self.darkMode == 0): 
                # Disable Dark Mode
                BGND_COL = WSU_CRIMSON
                TEXT_COL = WSU_BLACK
                BTN_COL = WSU_ORANGE

            else:
                # Enable Dark Mode
                BGND_COL = DARK_GREY
                BTN_COL = WSU_CRIMSON
                TEXT_COL = LIGHT_GREY
        else:
            # Isabel mode
            if(self.darkMode == 0): 
                # Disable Dark Mode
                BGND_COL = DARK_PINK
                TEXT_COL = HOT_PINK
                BTN_COL = HOT_PINK

            else:
                # Enable Dark Mode
                BGND_COL = HOT_PINK
                TEXT_COL = DARK_PINK
                BTN_COL = DARK_PINK

        self.clear()
        self.draw()

        print(self.controller.messageToMainFunc(1)) # Testing, will delete later
    


        

class ConfigurationMenu(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Configuration", font = HEADING_FONT, bg = BGND_COL, fg = TEXT_COL) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, bg=BGND_COL, fg=BTN_COL, width=2, command = lambda:controller.show_frame(LunchRosterMenu) )
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, bg=BGND_COL, fg=BTN_COL, width=2, command = lambda:controller.show_frame(MainMenu))
        

        self.draw()


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.nextButton.place_forget()
        self.prevButton.place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)

        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 36, y = HEADING_Y)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)




class LunchRosterMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Lunch Roster", font = HEADING_FONT, bg = BGND_COL, fg = TEXT_COL) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, bg=BGND_COL, fg=BTN_COL, width=2, command = lambda:controller.show_frame(ChatMenu) )
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, bg=BGND_COL, fg=BTN_COL, width=2, command = lambda:controller.show_frame(ConfigurationMenu))

    
        self.draw()


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.nextButton.place_forget()
        self.prevButton.place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)

        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 36, y = HEADING_Y)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)


class ChatMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Chat Roster", font = HEADING_FONT, bg = BGND_COL, fg = TEXT_COL) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, bg=BGND_COL, fg=BTN_COL, width=2, command = lambda:controller.show_frame(PendingsMenu) )
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, bg=BGND_COL, fg=BTN_COL, width=2, command = lambda:controller.show_frame(LunchRosterMenu))

        self.draw()


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.nextButton.place_forget()
        self.prevButton.place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)

        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 36, y = HEADING_Y)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)

class PendingsMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Pendings Roster", font = HEADING_FONT, bg = BGND_COL, fg = TEXT_COL) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, bg=BGND_COL, fg=BTN_COL, width=2, command = lambda:controller.show_frame(OverrideMenu) )
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, bg=BGND_COL, fg=BTN_COL, width=2, command = lambda:controller.show_frame(ChatMenu))
        
        self.draw()


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.nextButton.place_forget()
        self.prevButton.place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)

        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 36, y = HEADING_Y)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)

class OverrideMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Finalisation", font = HEADING_FONT, bg = BGND_COL, fg = TEXT_COL) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Navigation buttons
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, bg=BGND_COL, fg=BTN_COL, width=2, command = lambda:controller.show_frame(PendingsMenu))

        self.draw()


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.prevButton.place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)

        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 36, y = HEADING_Y)
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
