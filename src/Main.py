# Local deps
from Normies import ITSDStaff # Defines WSU Staff class
from DataCollectors import * # Reading data from text files
import GUIHandler, LunchRosterGenerator, ChatRosterGenerator, PendingsRosterGenerator, APIKeyRetriever
import ShiftRetreiver

# Python bundled deps
from datetime import datetime, timedelta
import json
import random
import pickle # Used for serializing staff to files as well as converting serialized files to staff objects
import threading

# External deps
import pyperclip
import win32com.client
import requests

workingStaff = {} # Dict of all staff names and their staff object, mainly accessed via messageFromGUI function e.g. {ethan: ethanObj,...}

"""
' This fuction is called by the GUI to send data to Main (e.g. a request for staff roster details). 
' The function will block program execution (including GUI) until a value is returned.
' TODO: Expand functionality of function to handle all types of requests as this is how data will be sent to the GUI
' ALSO TODO: Cleanup (Maybe put in another module if possible)

' reqTypes: 
    - 0 = Reserved for testing
        No reqParam used
    - 1 = API Key Request
        0 = From file
        1 = From Web
    - 2 = Request staff lunch times
        No reqParam used
    - 3 = Override of staffmember lunch
        param will be a tuple of the staff member's name and their updated lunch time
    - 4 = Check API Key
        apiKey <string>
"""
def messageFromGUI(reqType, reqParam = 0):
    reply = ""
    print("Main received Request {} from GUI ".format( (reqType, reqParam) )) # Debug option

    if(reqType == 1): # API Key request
        if(reqParam == 0):
            reply = APIKeyRetriever.retrieveFromFile()
        else:
            reply = APIKeyRetriever.retrieveFromWeb()
        
    elif(reqType == 2): # Request for lunch roster output
        reply = LunchRosterGenerator.generateLunchRoster()
        
    elif(reqType == 3): # Change assigned lunch
        try:
            # Update the staff member's lunch time in their staff member object
            staffName = reqParam[0]
            lunchTime = reqParam[1]
            workingStaff[staffName].set_lunchtime = lunchTime
            # If successful
            reply = GUIHandler.SUCCESS
        except Exception as exc:
            #If unsuccessful
            reply = GUIHandler.NOSUCCESS
    
    elif(reqType == 4): # Requesting to check provided API Key
        # If successful, save it to tokenFile and load in staff objects using the token
        return (GUIHandler.NOSUCCESS, "Error message here")
    
    elif(reqType == 5): # Requesting Chat roster output
        reply = ChatRosterGenerator.generateChatRoster()
    
    elif(reqType == 6): # Requesting Pendings roster output
        reply = PendingsRosterGenerator.generatePendingsRoster()
    
    elif(reqType == 7): # Change assigned chats
        try:
            # Update the staff member's chat status in their staff member object
            staffName = reqParam[0]
            chatFlag = reqParam[1]
            workingStaff[staffName].on_chat = chatFlag
            # If successful
            reply = GUIHandler.SUCCESS
        except Exception as exc:
            #If unsuccessful
            reply = GUIHandler.NOSUCCESS
    
    elif(reqType == 8): # Change assigned pendings
        # Update the staff member's pending time in their staff member object
        reply = GUIHandler.SUCCESS
        
        
    print("Returning {}".format(reply))
    return reply

def loadStaff():
    # Load only staff that are working today
    return

def saveStaff():
    # If file does not exist for staff member, create it
    return



if __name__ == "__main__":

    # Get staff working today
    ShiftRetreiver.get_shift_data()
    
    # Create the GUI Application window and hand it the communication function so tht it can communicate with Main
    MainWindow = GUIHandler.RosterWindow(messageFromGUI)

    # Update GUI and respond to User interations -- Can put other checks and logic in this loop if needed
    while True:
        MainWindow.update()
        # TODO: Handle GUI being closed -- Quit main