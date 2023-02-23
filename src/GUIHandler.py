import tkinter as tk
from tkinter import ttk, messagebox# Can be used to stylize widgets, nice to have, I probably wont use it 
from Normies import ITSDStaff
import random, datetime
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

    def __init__(self, messageToMain, *args, **kwargs):

        global BGND_COL, BTN_COL, TEXT_COL, TEXT_INPT_BG, TEXT_INPT_FG

        self.messageToMain = messageToMain
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.geometry('{}x{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT)) # Set resolution of GUI Application window
        self.showNavBar = False # Hamburger menu toggle
        self.navBarWidth = 100 # Width of nav bar (pixels)
        self.navBarPosX = 10 # Distance from left-hand side that the start of the buttons will be place (pixels)
        self.navBarIncrementY = 50 # Distance between each navigation button in hamburger menu (pixels)
        self.navBarSubsectStartY = 450 # Start of admin section of navbar
        self.darkMode = 0 # Dark Mode Toggle
        self.EEM = 0 # Easter Egg mode: 0 = Deafult, 1 = Pink text/UI elements, 2 = Uwuify'd text/UI elements
        self.activeFrame = None # Stores which frame is currently displayed to the user
        self.prevFrame = None # Stores the frame that navigated to the current frame

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

        for menu in (MainMenu, ConfigurationMenu, LunchRosterMenu, ChatMenu, PendingsMenu, FinalizeMenu, StaffManagementMenu):
            frame = menu(container, self)

            self.frames[menu] = frame
            frame.grid(row = 0, column = 0, sticky="nsew")

        
        # After initialization, show main page
        self.show_frame(MainMenu)
        
    
    # Function to put the passed page as the toplevel page in container
    def show_frame(self, page):
        # Get requested frame from dict
        if(page == None):
            # Requesting to go back to previous page
            frame = self.prevFrame
        else:
            # Go to requested page
            frame = self.frames[page]

        self.prevFrame = self.activeFrame
        self.activeFrame = frame

        # If this is the first time the frame is loaded, run it's first time function
        if(frame.firstLoad == True):
            frame.onFirstLoad()
        else:
            # Otherwise, redraw it's contents
            frame.clear()
            frame.draw()

        # Bring the frame to the top of the container
        frame.tkraise()

    def toggleHamburgerMenu(self):
        self.showNavBar = not self.showNavBar
        self.activeFrame.clear()
        self.activeFrame.draw()
        print("Hamburger Menu status: {}".format(self.showNavBar))



class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        
        self.firstLoad = True # Flag for first time loading of page
        self.APIKeyChecks = 0

        self.canvas = tk.Canvas(self, width = self.controller.navBarWidth, height = WINDOW_HEIGHT) # Used for hamburger menu shade
        # self.canvas becomes master of any buttons created on it
        self.navToMain = tk.Button(self.canvas, text="Home", relief=tk.FLAT, state=tk.DISABLED)
        self.navToLunch = tk.Button(self.canvas, text="Lunch", relief=tk.FLAT, state=tk.DISABLED, command=lambda:self.controller.show_frame(LunchRosterMenu))
        self.navToChat = tk.Button(self.canvas, text="Chats", relief=tk.FLAT, state=tk.DISABLED, command=lambda:self.controller.show_frame(ChatMenu))
        self.navToPendings = tk.Button(self.canvas, text="Pendings", relief=tk.FLAT, state=tk.DISABLED, command=lambda:self.controller.show_frame(PendingsMenu))
        self.navToFinal = tk.Button(self.canvas, text="Finalisation", relief=tk.FLAT, state=tk.DISABLED, command=lambda:self.controller.show_frame(FinalizeMenu))
        self.navBarAdmin = tk.Label(self.canvas, text = "Admin", font=HEADING_FONT)
        self.navToConfig = tk.Button(self.canvas, text="Configuration", relief=tk.FLAT, command=lambda:self.controller.show_frame(ConfigurationMenu))
        self.navToStaffManagement = tk.Button(self.canvas, text="Manage Staff", relief=tk.FLAT, command=lambda:self.controller.show_frame(StaffManagementMenu))

        # Hamburger Menu 
        self.hamburgerOpenIconLight = tk.PhotoImage(file = "{}HamburgerOpenLight.png".format(UI_FOLDER))
        self.hamburgerOpenIconDark = tk.PhotoImage(file = "{}HamburgerOpenDark.png".format(UI_FOLDER))
        self.hamburgerCloseIconLight = tk.PhotoImage(file = "{}HamburgerCloseLight.png".format(UI_FOLDER))
        self.hamburgerCloseIconDark = tk.PhotoImage(file = "{}HamburgerCloseDark.png".format(UI_FOLDER))
        self.HamburgerMenuBtn = tk.Button(master=self, highlightthickness = 0, relief=tk.FLAT, bd=0, command=self.controller.toggleHamburgerMenu)

        
        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Home", font = MENU_FONT)

        # API Key input
        self.APIKeyHeading = CreateElement(controller, tk.Label, master=self, text = "Enter your Humanity API key below: ", font=HEADING_FONT)
        self.APIKeyInput = CreateElement(controller, tk.Text, master=self, height=1, width=40, font=STD_FONT)
        self.APIKeyLoad = CreateElement(controller, tk.Button, master=self, text = "File: Load", font=API_BTN_FONT, command=lambda:self.requestAPIKey(0))
        self.APIKeyRetrieve = CreateElement(controller, tk.Button, master=self, text = "Web: Retrieve", font=API_BTN_FONT, command=lambda:self.requestAPIKey(1))
        self.APICheck = CreateElement(controller, tk.Button, master=self, text="Check", font=API_BTN_FONT, command=self.checkAPIKey)
        self.APICheckMessage = CreateElement(controller, tk.Label, master=self, font=WARN_FONT)
        # Add dark mode toggle
        self.darkModeToggle = CreateElement(controller, tk.Button, master=self, text="Enable dark mode", font=STD_FONT, command = self.toggleDarkMode)  

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, width=2, state=tk.DISABLED, command = lambda:controller.show_frame(LunchRosterMenu) )

        
    def onFirstLoad(self):
        # Draw all UI elements to screen
        self.draw()

        self.firstLoad = False
        pass
        
    
    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.HamburgerMenuBtn.place_forget()
        self.APIKeyInput.place_forget()
        self.nextButton.place_forget()
        self.APIKeyLoad.place_forget()
        self.APIKeyRetrieve.place_forget()
        self.APICheck.place_forget()
        self.darkModeToggle.place_forget()
        self.APICheckMessage.place_forget()
        self.navBarAdmin.place_forget()
        

        self.canvas.delete("all") # Clear canvas 
        self.canvas.place_forget()

    # Renders all UI Elements
    def draw(self):
        self.darkModeToggle.config(text="Enable dark mode" if self.controller.darkMode == 0 else "Disable dark mode")

        self.config(bg=BGND_COL)

        # This is where elements are configured (Colours)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.APIKeyHeading.config(bg = BGND_COL, fg = TEXT_COL)
        self.APIKeyInput.config(bg = TEXT_INPT_BG, fg = TEXT_INPT_FG)
        self.APIKeyLoad.config(bg= BGND_COL, fg=BTN_COL)
        self.APIKeyRetrieve.config(bg= BGND_COL, fg=BTN_COL)
        self.APICheck.config(bg = BGND_COL, fg=BTN_COL)
        self.APICheckMessage.config(bg = BGND_COL, fg=TEXT_COL)
        self.darkModeToggle.config(bg = BGND_COL, fg=BTN_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)


        
        # Handle Hamburger menu first as it is a special case and we want everything to be drawn over top of it
        if(self.controller.showNavBar):
            # Navbar Menu active
            self.canvas.config(bg=NAV_BAR_COL, highlightthickness = 0, relief=tk.FLAT, bd=0)
            self.canvas.create_rectangle(0, 450, self.controller.navBarWidth, WINDOW_HEIGHT, fill=NAV_BAR_SUBSECT_COL)
            # Configuration of navBar buttons
            self.navToMain.config(bg = BGND_COL, fg=BTN_COL)
            self.navToConfig.config(bg = BGND_COL, fg=BTN_COL)
            self.navToStaffManagement.config(bg = BGND_COL, fg=BTN_COL)
            self.navToLunch.config(bg = BGND_COL, fg=BTN_COL)
            self.navToChat.config(bg = BGND_COL, fg=BTN_COL)
            self.navToPendings.config(bg = BGND_COL, fg=BTN_COL)
            self.navToFinal.config(bg = BGND_COL, fg=BTN_COL)
            self.navBarAdmin.config(bg=NAV_BAR_COL, fg=TEXT_COL)
            # Placement of Navbar buttons
            self.navToMain.place(x=self.controller.navBarPosX, y=20)
            self.navToConfig.place(x=self.controller.navBarPosX, y=20 + self.controller.navBarSubsectStartY)
            self.navToStaffManagement.place(x=self.controller.navBarPosX, y= 20 + self.controller.navBarIncrementY + self.controller.navBarSubsectStartY)
            self.navToLunch.place(x=self.controller.navBarPosX, y=20 + 1 * self.controller.navBarIncrementY)
            self.navToChat.place(x=self.controller.navBarPosX, y=20 + 2 * self.controller.navBarIncrementY)
            self.navToPendings.place(x=self.controller.navBarPosX, y=20 + 3 * self.controller.navBarIncrementY)
            self.navToFinal.place(x=self.controller.navBarPosX, y=20 + 4 * self.controller.navBarIncrementY)
            self.navBarAdmin.place(x = self.controller.navBarPosX, y = self.controller.navBarSubsectStartY - 30)
            self.canvas.place(x=0,y=0)
            # TODO: Set hamburgerMenuBtn image to an 'X'
            if(self.controller.darkMode == 0):
                self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerCloseIconLight) 
            else:
                self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerCloseIconDark)
        else:
            # Navbar menu collapsed
            # Swap image of Hamburger Icon based on dark mode setting
            if(self.controller.darkMode == 0):
                self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerOpenIconLight) 
            else:
                self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerOpenIconDark)

        # This is where elements are placed
        self.pageLabel.place( x = (WINDOW_WIDTH / 2 - 36) + (self.controller.showNavBar * self.controller.navBarWidth) , y = HEADING_Y)
        self.APIKeyHeading.place(x = (WINDOW_WIDTH / 2 - 165) + (self.controller.showNavBar * self.controller.navBarWidth), y = HEADING_Y + 70)
        self.APIKeyInput.place(x = (WINDOW_WIDTH / 2 - 170) + (self.controller.showNavBar * self.controller.navBarWidth), y = HEADING_Y + 100)
        self.APIKeyLoad.place(x = (WINDOW_WIDTH / 2 - 100) + (self.controller.showNavBar * self.controller.navBarWidth), y = HEADING_Y + 130)
        self.APIKeyRetrieve.place(x = (WINDOW_WIDTH / 2 - 0) + (self.controller.showNavBar * self.controller.navBarWidth), y = HEADING_Y + 130)
        self.APICheck.place(x = (WINDOW_WIDTH / 2 + 160) + (self.controller.showNavBar * self.controller.navBarWidth), y = HEADING_Y + 95)
        self.darkModeToggle.place(x = (WINDOW_WIDTH / 2 - 64) + (self.controller.showNavBar * self.controller.navBarWidth), y = WINDOW_HEIGHT - 100)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)

        if(self.controller.showNavBar):
            self.HamburgerMenuBtn.place(x=10 + self.controller.navBarWidth, y=10)
        else:
            self.HamburgerMenuBtn.place(x=10, y=10)

        
    
    def requestAPIKey(self, src=0):
        key = ""
        if(src == 0):
            # Requesting API key from file
            key = self.controller.messageToMain(1, 0) # Request main to provide the API key from the file
        else:
            # Requesting API key from Web (Most up to date)
            key = self.controller.messageToMain(1, 1) # Request main to provide the API key from the web browser

        # Once we have received key from main, update key field in GUI
        self.APIKeyInput.delete(1.0, tk.END) # Delete current contents of API key field
        
        self.APIKeyInput.insert(tk.END, key) # Insert received API key

    # Function that checks that sends the entered API Key to Main to check if it is valid
    # Main then sends back SUCCESS or NOSUCCESS depending on if the key is valid
    # This function displays the output of that
    def checkAPIKey(self):
        status = self.controller.messageToMain(4, self.APIKeyInput.get(1.0, tk.END).replace('\n', ""))

        if(status[0] == NOSUCCESS):
            self.APICheckMessage.config(text="API Key: Error")
            self.APICheckMessage.place(x = (WINDOW_WIDTH / 2 - 60) + (self.controller.showNavBar * self.controller.navBarWidth), y = HEADING_Y + 170 )
            self.APIKeyChecks += 1
            # Show error message on third failed attempt
            if(self.APIKeyChecks % 3 == 0):
                # Ask user if they wish to continue with incorrect API key 
                if(messagebox.askyesno("API Key Error", "{}\nDo you wish to proceed regardless?".format(status[1]))):
                    self.enableNavButtons()
                    self.controller.show_frame(LunchRosterMenu)

                
        else:
            self.APICheckMessage.config(text="API Key: Success")
            self.APICheckMessage.place(x = (WINDOW_WIDTH / 2 - 62) + (self.controller.showNavBar * self.controller.navBarWidth), y = HEADING_Y + 170 )
            # Good API Key entered, make nav buttons available

            self.enableNavButtons()
            #messagebox.showinfo("API Key Success", "API Key successful!") 


    # Function that toggles the state of dark mode by modifying colour 'constants' based on dark mode state
    def toggleDarkMode(self):
        global BGND_COL, BTN_COL, TEXT_COL, TEXT_INPT_FG, TEXT_INPT_BG, NAV_BAR_COL, NAV_BAR_SUBSECT_COL
        self.controller.darkMode = not self.controller.darkMode # Flip dark mode toggle

        if(self.controller.EEM != 1):
            # Normal mode
            if(self.controller.darkMode == 0): 
                # Disable Dark Mode
                BGND_COL = WSU_CRIMSON
                TEXT_COL = WSU_BLACK
                BTN_COL = WSU_ORANGE
                TEXT_INPT_BG = LIGHT_GREY
                TEXT_INPT_FG = DARK_GREY
                NAV_BAR_COL = LIGHT_GREY
                NAV_BAR_SUBSECT_COL = MEDIUM_GREY

            else:
                # Enable Dark Mode
                BGND_COL = DARK_GREY
                BTN_COL = WSU_CRIMSON
                TEXT_COL = LIGHT_GREY
                TEXT_INPT_BG = DARK_GREY
                TEXT_INPT_FG = LIGHT_GREY
                NAV_BAR_COL = DARK_SLATE_BLUE  
                NAV_BAR_SUBSECT_COL = WSU_BLACK
        else:
            # Isabel mode
            if(self.controller.darkMode == 0): 
                # Disable IsabelDark Mode
                BGND_COL = DARK_PINK
                TEXT_COL = HOT_PINK
                BTN_COL = HOT_PINK
                TEXT_INPT_BG = DARK_PINK
                TEXT_INPT_FG = HOT_PINK
                NAV_BAR_COL = HOT_PINK

            else:
                # Enable IsabelDark Mode
                BGND_COL = HOT_PINK
                TEXT_COL = DARK_PINK
                BTN_COL = DARK_PINK
                TEXT_INPT_BG = HOT_PINK
                TEXT_INPT_FG = DARK_PINK
                NAV_BAR_COL = DARK_PINK

        self.clear() # Clear the screen 
        self.draw()  # Redraw all elements using new colour scheme

        print(self.controller.messageToMain(0)) # Testing, will delete later


    # Enables all navigation buttons
    def enableNavButtons(self):
        self.navToLunch.config(state = tk.NORMAL)
        self.navToChat.config(state = tk.NORMAL)
        self.navToPendings.config(state = tk.NORMAL)
        self.navToFinal.config(state = tk.NORMAL)
        self.nextButton.config(state = tk.NORMAL)



class LunchRosterMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        self.firstLoad = True # Flag for first time loading of page

        self.staffDisplayRowCounter = 0 # Rows is number of staff working today dived by 2 
        self.staffDisplayColCounter = 0 # Two cols  of staff lunch times will be displayed. 


        self.lunchTimes = {} # Dict of all staff and their lunches 
        self.lunchTimeWidgets = {} # dict of staff name as key and array of label, drop-down widget and stringVar literal of the currently selected option e.g. { "ethan":[tk.label, tk.dropDown, StringVar] }
        self.lunch_options = [ # All possible lunch times that will show up in the drop down menu
            None,
            datetime.time(11, 00).strftime('%I:%M%p'),
            datetime.time(11, 30).strftime('%I:%M%p'),
            datetime.time(12, 00).strftime('%I:%M%p'),
            datetime.time(12, 30).strftime('%I:%M%p'),
            datetime.time(13, 00).strftime('%I:%M%p'),
            datetime.time(13, 30).strftime('%I:%M%p'),
            datetime.time(14, 00).strftime('%I:%M%p'),
            datetime.time(14, 30).strftime('%I:%M%p'),
            datetime.time(15, 00).strftime('%I:%M%p'),
            datetime.time(15, 30).strftime('%I:%M%p')
        ]
        

        # Set background colour
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Lunch Roster", font = MENU_FONT) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Hamburger Menu buton
        self.hamburgerOpenIconLight = tk.PhotoImage(file = "{}HamburgerOpenLight.png".format(UI_FOLDER))
        self.hamburgerOpenIconDark = tk.PhotoImage(file = "{}HamburgerOpenDark.png".format(UI_FOLDER))
        self.HamburgerMenuBtn = tk.Button(master=self, highlightthickness = 0, relief=tk.FLAT, bd=0, command=self.controller.toggleHamburgerMenu)

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(ChatMenu) )
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(MainMenu))



    def onFirstLoad(self):

        # Request a lunch roster to display, this can then be edited by the user
        self.lunchTimes = self.controller.messageToMain(2).copy()
        for k, v in self.lunchTimes.items():
            self.lunchTimes[k] = v.strftime('%I:%M%p')
        
        # Create a label and drop down for each staff member (label) and their lunch times (Drop down)
        for staffName in self.lunchTimes:
            setString = tk.StringVar() # Create rkinter variable for the selected drop-down value
            setString.set(self.lunchTimes[staffName]) # Set this variable to this staff members allocated lunch time
            self.lunchTimeWidgets[staffName] = [ CreateElement(self.controller, tk.Label, master=self, text = staffName, font=DROP_DOWN_LABEL_FONT), tk.OptionMenu(self, setString, *self.lunch_options, command = partial(self.updateLunch, staffName)), setString ]
        

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

        if(self.controller.darkMode == 0):
            self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerOpenIconLight) 
        else:
            self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerOpenIconDark)

        # Loop through all staff lunch labels and drop-down menus and set their colours accordingly
        for staffName in self.lunchTimeWidgets:
            self.lunchTimeWidgets[staffName][0].config(bg = BGND_COL, fg=TEXT_COL)
            self.lunchTimeWidgets[staffName][1].config(bg = BGND_COL, fg=BTN_COL)
            self.lunchTimeWidgets[staffName][1]["highlightthickness"] = 0 # Set border size
            

        # This is where elements are placed
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 80, y = HEADING_Y)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)

        # Loop through all staff lunch labels and drop-down menus and place them 
        increment = 0
        for staffName in self.lunchTimeWidgets:

            self.lunchTimeWidgets[staffName][0].place(x = (staffDisplayCol0 - staffDropDownLabelOffset - (staffPixelsPerCharacterOffset*len(staffName)) ) if self.staffDisplayColCounter == 0 else (staffDisplayCol1 - staffDropDownLabelOffset - (staffPixelsPerCharacterOffset*len(staffName))), y = staffDisplayStartY + (self.staffDisplayRowCounter * staffDisplayIncrementY))
            self.lunchTimeWidgets[staffName][1].place(x = (staffDisplayCol0 + staffDisplayDrpDwnOffset) if self.staffDisplayColCounter == 0 else (staffDisplayCol1 + staffDisplayDrpDwnOffset), y = staffDisplayStartY + (self.staffDisplayRowCounter * staffDisplayIncrementY)) 
 

            self.staffDisplayColCounter = not self.staffDisplayColCounter # Alternate rows
            if(increment % 2 == 1):
                # Every second loop starting from 0
                self.staffDisplayRowCounter += 1
            increment += 1
        
        # Reset counters
        self.staffDisplayColCounter = 0
        self.staffDisplayRowCounter = 0


    def updateLunch(self, staffName, newTime):
        print("Updating lunch for {} to {}".format(staffName, newTime))

        hr = int(newTime.split(":")[0][:2])
        min = int(newTime.split(":")[1][:2])

        if("pm" in newTime.lower()):
            hr += 12

        if( self.controller.messageToMain(3, (staffName, datetime.time(hr, min))) == NOSUCCESS): # Pass back datetime object?
            # Unable to update lunch time
            messagebox.showerror("Override error", "Operation failed\nPlease check inputs and try again.") 

        return

        
        

class ChatMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        self.firstLoad = True # Flag for first time loading of page
        self.chatRoster = {} # Dict of all staff names and either true or false depending if they're on chat or not e.g. {ethan:false, isaac:true}
        self.chatWidgets = {} # dict of staff name as key and array of label, drop-down widget and stringVar literal of the currently selected option e.g. { "ethan":[tk.label, tk.checkBox] }
        self.staffDisplayRowCounter = 0 # Rows is number of staff working today dived by 2 
        self.staffDisplayColCounter = 0 # Two cols  of staff lunch times will be displayed. 


        # Set background colour
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Chat Roster", font = MENU_FONT) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Hamburger Menu buton
        self.hamburgerOpenIconLight = tk.PhotoImage(file = "{}HamburgerOpenLight.png".format(UI_FOLDER))
        self.hamburgerOpenIconDark = tk.PhotoImage(file = "{}HamburgerOpenDark.png".format(UI_FOLDER))
        self.HamburgerMenuBtn = tk.Button(master=self, highlightthickness = 0, relief=tk.FLAT, bd=0, command=self.controller.toggleHamburgerMenu)

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(PendingsMenu) )
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(LunchRosterMenu))

    
    def onFirstLoad(self):
        # Request chat roster from main and store it in member variable
        self.chatRoster = self.controller.messageToMain(5).copy()

        # Create a label and checkbox for each staff member (label) and their chat status (checkbox)
        for staffName in self.chatRoster:
            checkBoxVar = tk.IntVar() # Variable to store status of checkbox (0/1)
            thisLabel = CreateElement(self.controller, tk.Label, master=self, text = staffName, font=DROP_DOWN_LABEL_FONT)
            thisCheckBox = tk.Checkbutton(self, variable=checkBoxVar)
            
            # If this staff is set to be on chats, toggle it's corresponding checkbox
            if(self.chatRoster[staffName]):
                thisCheckBox.toggle()

            self.chatWidgets[staffName] = [ thisLabel, thisCheckBox, checkBoxVar ]

        # Draw all UI elements to screen
        self.draw()

        self.firstLoad = False
        pass


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.nextButton.place_forget()
        self.prevButton.place_forget()

        for staffName in self.chatWidgets:
            self.chatWidgets[staffName][0].place_forget()
            self.chatWidgets[staffName][1].place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        # This is where elements are configured (Colours)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)

        if(self.controller.darkMode == 0):
            self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerOpenIconLight) 
        else:
            self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerOpenIconDark)
        
        # Loop through all staff chat labels and option menus and set their colours accordingly
        for staffName in self.chatWidgets:
            self.chatWidgets[staffName][0].config(bg = BGND_COL, fg=TEXT_COL)
            self.chatWidgets[staffName][1].config(bg = BGND_COL, fg=BTN_COL)
            self.chatWidgets[staffName][1]["highlightthickness"] = 0 # Set border size


        # This is where elements are placed
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 72, y = HEADING_Y)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)

        # Loop through all staff Chat labels and checkboxes and place them 
        increment = 0
        for staffName in self.chatWidgets:

            self.chatWidgets[staffName][0].place(x = (staffDisplayCol0 - (10*len(staffName)) ) if self.staffDisplayColCounter == 0 else (staffDisplayCol1 - (10*len(staffName))), y = staffDisplayStartY + (self.staffDisplayRowCounter * staffDisplayIncrementY))
            self.chatWidgets[staffName][1].place(x = (staffDisplayCol0 + staffDisplayDrpDwnOffset) if self.staffDisplayColCounter == 0 else (staffDisplayCol1 + staffDisplayDrpDwnOffset), y = staffDisplayStartY + (self.staffDisplayRowCounter * staffDisplayIncrementY)) 

            self.staffDisplayColCounter = not self.staffDisplayColCounter # Alternate rows
            if(increment % 2 == 1):
                # Every second loop starting from 0
                self.staffDisplayRowCounter += 1
            increment += 1
        
        # Reset counters
        self.staffDisplayColCounter = 0
        self.staffDisplayRowCounter = 0

    def updateAssigneds(self):
        for staffName in self.chatWidgets:
            self.controller.messageToMain( 7, (staffName, self.chatWidgets[staffName][2].get() ) ) 



class PendingsMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        self.firstLoad = True # Flag for first time loading of page
        self.staffDisplayRowCounter = 0 # Rows is number of staff working today dived by 2 
        self.staffDisplayColCounter = 0 # Two cols  of staff lunch times will be displayed. 
        self.pendingsRoster = {} # Dict of all staff and their pending times, time is None if not selected 
        self.pendingsWidgets = {} # dict of staff name as key and array of label, drop-down widget { "ethan":[tk.label, tk.dropDown] }
        self.pendings_options = [ # All possible lunch times that will show up in the drop down menu
            None,
            datetime.time(8, 00).strftime('%I:%M%p'),
            datetime.time(9, 00).strftime('%I:%M%p'),
            datetime.time(10, 00).strftime('%I:%M%p'),
            datetime.time(11, 00).strftime('%I:%M%p'),
            datetime.time(12, 00).strftime('%I:%M%p'),
            datetime.time(13, 00).strftime('%I:%M%p'),
            datetime.time(14, 00).strftime('%I:%M%p'),
            datetime.time(15, 00).strftime('%I:%M%p'),
            datetime.time(16, 00).strftime('%I:%M%p'),
            datetime.time(17, 00).strftime('%I:%M%p'),
            datetime.time(18, 00).strftime('%I:%M%p')
        ]

        # Set background colour
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Pendings Roster", font = MENU_FONT) #tk.Label(self, text="Home Page", font = STD_FONT, fg = controller.fontCol) 

        # Hamburger Menu buton
        self.hamburgerOpenIconLight = tk.PhotoImage(file = "{}HamburgerOpenLight.png".format(UI_FOLDER))
        self.hamburgerOpenIconDark = tk.PhotoImage(file = "{}HamburgerOpenDark.png".format(UI_FOLDER))
        self.HamburgerMenuBtn = tk.Button(master=self, highlightthickness = 0, relief=tk.FLAT, bd=0, command=self.controller.toggleHamburgerMenu)

        # Navigation buttons
        self.nextButton = CreateElement(controller, tk.Button, master=self, text=">", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(FinalizeMenu) )
        self.prevButton = CreateElement(controller, tk.Button, master=self, text="<", font = NAV_BTN_FONT, width=2, command = lambda:controller.show_frame(ChatMenu))
        
    
    def onFirstLoad(self):
        # Request pendings roster from main and store it in member variable
        self.pendingsRoster = self.controller.messageToMain(6).copy()

        # Create a label and drop down for each staff member (label) and their lunch times (Drop down)
        for staffName in self.pendingsRoster:
            setString = tk.StringVar() # Create tkinter variable for the selected drop-down value
            setString.set(self.pendingsRoster[staffName]) # Set this variable to this staff members allocated pendings time
            self.pendingsWidgets[staffName] = [ CreateElement(self.controller, tk.Label, master=self, text = staffName, font=DROP_DOWN_LABEL_FONT), tk.OptionMenu(self, setString, *self.pendings_options, command = partial(self.updatePendings, staffName)), setString ]

        # Draw all UI elements to screen
        self.draw()

        self.firstLoad = False
        pass


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.nextButton.place_forget()
        self.prevButton.place_forget()

        for staffName in self.pendingsWidgets:
            self.pendingsWidgets[staffName][0].place_forget()
            self.pendingsWidgets[staffName][1].place_forget()


    # Renders all UI Elements
    def draw(self):

        self.controller.frames[ChatMenu].updateAssigneds() # If we have reached this page, force the chat page to push it's checkboxes across to main

        self.config(bg=BGND_COL)

        # This is where elements are configured (Colours)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.nextButton.config(bg = BGND_COL, fg=BTN_COL)
        self.prevButton.config(bg = BGND_COL, fg=BTN_COL)

        if(self.controller.darkMode == 0):
            self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerOpenIconLight) 
        else:
            self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerOpenIconDark)

        # Loop through all staff pendings labels and drop-down menus and set their colours accordingly
        for staffName in self.pendingsWidgets:
            self.pendingsWidgets[staffName][0].config(bg = BGND_COL, fg=TEXT_COL)
            self.pendingsWidgets[staffName][1].config(bg = BGND_COL, fg=BTN_COL)
            self.pendingsWidgets[staffName][1]["highlightthickness"] = 0 # Set border size


        # This is where elements are placed
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 92, y = HEADING_Y)
        self.nextButton.place(x = WINDOW_WIDTH - 50, y = WINDOW_HEIGHT - 50)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)

        # Loop through all staff lunch labels and drop-down menus and place them 
        increment = 0
        for staffName in self.pendingsWidgets:

            self.pendingsWidgets[staffName][0].place(x = (staffDisplayCol0 - (10*len(staffName)) ) if self.staffDisplayColCounter == 0 else (staffDisplayCol1 - (10*len(staffName))), y = staffDisplayStartY + (self.staffDisplayRowCounter * staffDisplayIncrementY))
            self.pendingsWidgets[staffName][1].place(x = (staffDisplayCol0 + staffDisplayDrpDwnOffset) if self.staffDisplayColCounter == 0 else (staffDisplayCol1 + staffDisplayDrpDwnOffset), y = staffDisplayStartY + (self.staffDisplayRowCounter * staffDisplayIncrementY)) 
 

            self.staffDisplayColCounter = not self.staffDisplayColCounter # Alternate rows
            if(increment % 2 == 1):
                # Every second loop starting from 0
                self.staffDisplayRowCounter += 1
            increment += 1
        
        # Reset counters
        self.staffDisplayColCounter = 0
        self.staffDisplayRowCounter = 0

    
    def updatePendings(self, staffName, newTime):
        print("Updating pendings for {} to {}".format(staffName, newTime))
        if( self.controller.messageToMain(8, (staffName, newTime)) == NOSUCCESS):
            # Unable to update lunch time
            messagebox.showerror("Override error", "Operation failed\nPlease check inputs and try again.") 

        return



class FinalizeMenu(tk.Frame): # Overrides and serializing objects etc...

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        self.firstLoad = True # Flag for first time loading of page

        # Set background colour
        self.config(bg=BGND_COL)

        # Hamburger Menu button
        self.hamburgerOpenIconLight = tk.PhotoImage(file = "{}HamburgerOpenLight.png".format(UI_FOLDER))
        self.hamburgerOpenIconDark = tk.PhotoImage(file = "{}HamburgerOpenDark.png".format(UI_FOLDER))
        self.HamburgerMenuBtn = tk.Button(master=self, highlightthickness = 0, relief=tk.FLAT, bd=0, command=self.controller.toggleHamburgerMenu)


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

        if(self.controller.darkMode == 0):
            self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerOpenIconLight) 
        else:
            self.HamburgerMenuBtn.config(width= 32, height=32, image= self.hamburgerOpenIconDark)

        # This is where elements are placed
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 70, y = HEADING_Y)
        self.prevButton.place(x = 20, y = WINDOW_HEIGHT - 50)



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

        # Description of page use
        self.pageDescriptor = CreateElement(controller, tk.Label, master=self, text="Enter any exceptions to regular rostering here", font=HEADING_FONT)

        # Prev page button
        self.closeButton = CreateElement(controller, tk.Button, master=self, text="X", font = MENU_FONT, width=2, command = lambda:controller.show_frame(None))

    
    def onFirstLoad(self):

        # Draw all UI elements to screen
        self.draw()
        self.firstLoad = False
        


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.pageDescriptor.place_forget()
        self.closeButton.place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        # This is where elements are configured (Colours)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.pageDescriptor.config(bg=BGND_COL, fg=TEXT_COL)
        self.closeButton.config(bg = BGND_COL, fg=BTN_COL)
        

        # This is where elements are placed
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 80, y = HEADING_Y)
        self.pageDescriptor.place(x = WINDOW_WIDTH / 2 - 190, y = HEADING_Y + 30)
        self.closeButton.place(x = 20, y = 20)


class StaffManagementMenu(tk.Frame): # Overrides and serializing objects etc...

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent # Reference to parent container
        self.controller = controller # Reference to parent object
        self.firstLoad = True # Flag for first time loading of page

        # Set background colour
        self.config(bg=BGND_COL)

        # Heading
        self.pageLabel = CreateElement(controller, tk.Label, master=self, text="Staff Management", font = MENU_FONT) 

        # Prev page button
        self.closeButton = CreateElement(controller, tk.Button, master=self, text="X", font = MENU_FONT, width=2, command = lambda:controller.show_frame(None))

    
    def onFirstLoad(self):
        # Draw all UI elements to screen
        self.draw()

        self.firstLoad = False
        pass


    # Removes all UI elements
    def clear(self):
        self.pageLabel.place_forget()
        self.closeButton.place_forget()


    # Renders all UI Elements
    def draw(self):

        self.config(bg=BGND_COL)

        # This is where elements are configured (Colours)
        self.pageLabel.config(bg = BGND_COL, fg=TEXT_COL)
        self.closeButton.config(bg = BGND_COL, fg=BTN_COL)

        # This is where elements are placed
        self.pageLabel.place(x = WINDOW_WIDTH / 2 - 70, y = HEADING_Y)
        self.closeButton.place(x = 20, y = 20)



# I can't believe I'm doing this for the uwu.
# Way to ruin the nicely laid out UI code :(
def CreateElement(controller, elementType, **kwargs):
    element = elementType(**kwargs)

    if(controller.EEM == 2):
        element.config(fg=GenerateRandomColour())

    return element


def GenerateRandomColour():
    return ("#%06x" % random.randint(0, 0xFFFFFF) )
