# Local deps
from Normies import WSUStaff # Defines WSU Staff class
from DataCollectors import * # Reading data from text files
import GUIHandler 

# Python bundled deps
import webbrowser
from datetime import datetime, timedelta
import json
import random
import pickle # Used for serializing staff to files as well as converting serialized files to staff objects
import threading

# External deps
import pyperclip
import win32com.client
import requests



"""
' This fuction is called by the GUI to send data to Main (e.g. a request for staff roster details). 
' The function will block the GUI thread (and this thread) until a value is returned.
' TODO: Expand functionality of function to handle all types of requests as this is how data will be sent to the GUI
' ALSO TODO: Cleanup (Maybe put in another module if possible)
"""
def messageFromGUI(reqType):
    reply = ""
    print("Received Request {} from GUI ".format(reqType)) # Debug option

    if(reqType == "reqType1"): # Placeholder values to show logic flow
        reply = "This is a return value"
        
    elif(reqType == "reqType2"): # Placeholder values to show logic flow
        reply = "This is a return value"
        
    else:
        reply = "This is a return value"
        
    
    return reply

def loadStaff():
    # Load only staff that are working today
    return

def saveStaff():
    # If file does not exist for staff member, create it
    return



if __name__ == "__main__":
    
    # Create the GUI Application window
    MainWindow = GUIHandler.RosterWindow(messageFromGUI)
    # Set resolution of GUI Application window
    MainWindow.geometry('{}x{}'.format(GUIHandler.WINDOW_WIDTH, GUIHandler.WINDOW_HEIGHT))

    # Update GUI and respond to User interations -- Can put other checks and logic in this loop if needed
    while True:
        MainWindow.update()