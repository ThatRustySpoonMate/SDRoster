# Local deps
from Normies import ITSDStaff # Defines WSU Staff class
from FormattingFunctions import *
import ConfigInterface # Reading data from text files
import GUIHandler, LunchGenerator, ChatRosterGenerator, PendingsRosterGenerator, APIKeyHandler, ObjectSerialization
import ShiftRetreiver

# Python bundled deps
from datetime import datetime, timedelta
import json
import random
import threading

# External deps
import pyperclip
import win32com.client
import requests

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
    global ShiftData, ShiftDataTrimmed, NumStaff

    reply = ""
    print("Main received Request {} from GUI ".format( (reqType, reqParam) )) # Debug option

    if(reqType == 1): # API Key request
        if(reqParam == 0):
            reply = APIKeyHandler.retrieveFromFile()
        else:
            reply = APIKeyHandler.retrieveFromWeb()
        
    elif(reqType == 2): # Request for lunch roster output

        lunchSlots = LunchGenerator.GetLunchSlots(LunchWeightsDict, LunchStart, LunchEnd, NumStaff)

        reply = LunchGenerator.GetStaffLunches(lunchSlots, ShiftData)
        
    elif(reqType == 3): # Change assigned lunch
        try:
            # Update the staff member's lunch time in their staff member object
            staffName = reqParam[0]
            lunchTime = reqParam[1]
            StaffWorking[staffName].set_lunchtime = lunchTime # Update
            # If successful
            reply = GUIHandler.SUCCESS
        except Exception as exc:
            #If unsuccessful
            reply = GUIHandler.NOSUCCESS
    
    elif(reqType == 4): # Requesting to check provided API Key
        # Get staff working today
        ShiftData, NumStaff = ShiftRetreiver.get_shift_data(ShiftTypes, RosterDate, reqParam)

        if(ShiftData != False): # Data is valid
            # Load staff objects into memory 
            for staffDetail in ShiftData:
                StaffWorking[staffDetail[0]] = ObjectSerialization.loadSingleStaff(staffDetail)

            # Store API Key to credentials File
            APIKeyHandler.storeCredentials(reqParam)

            return (GUIHandler.SUCCESS, "API Key Success")

        else: # API Key Error
            return(GUIHandler.NOSUCCESS, "Invalid API Key or API key has expired.")
    

    
    elif(reqType == 5): # Requesting Chat roster output
        reply = ChatRosterGenerator.generateChatRoster()
    
    elif(reqType == 6): # Requesting Pendings roster output
        reply = PendingsRosterGenerator.generatePendingsRoster()
    
    elif(reqType == 7): # Change assigned chats
        try:
            # Update the staff member's chat status in their staff member object
            staffName = reqParam[0]
            chatFlag = reqParam[1]
            StaffWorking[staffName].on_chat = chatFlag
            # If successful
            reply = GUIHandler.SUCCESS
        except Exception as exc:
            #If unsuccessful
            reply = GUIHandler.NOSUCCESS
    
    elif(reqType == 8): # Change assigned pendings
        # Update the staff member's pending time in their staff member object
        reply = GUIHandler.SUCCESS
    
    elif(reqType == 9): # Requesting list of staff names in data file
        reply = ObjectSerialization.getAllStaffNames()

    elif(reqType == 10): # Requesting editable staff information
        if(reqParam in list(StaffWorking.keys())):
            # Staff is loaded into memory
            reply = StaffWorking[reqParam]
        else:
            reply = ObjectSerialization.loadSingleStaff(reqParam)
    
    elif(reqType == 11): # Updating editable staff information
        # If object is loaded into memory, edit it in memory and save it to the file
        # If object is not loaded into memory, load it, make changes and save it 

        pass
        
        
    print("Returning {}".format(reply))
    return reply



if __name__ == "__main__":

    RosterDate = datetime.today() # Date that the roster will be generated for
    #RosterDate = datetime(2023, 2, 24, 10, 30, 1)
    # Load in config data
    LunchStart = ConfigInterface.readValue("lunchStart")
    LunchEnd = ConfigInterface.readValue("lunchEnd")
    LunchWeights = ConfigInterface.readValue("lunchWeights").split(",")
    LunchSlotTimes = convertToDateTime(ConfigInterface.readValue("lunchSlotTimes").split(","), RosterDate )
    ShiftTypes = ConfigInterface.readValue("shiftTypes").split(",")

    NumStaff = 0 # Number of staff working on selected date
    ShiftData = [] # Return from get_shift_data function
    StaffWorking = {} # Array of all the objects corresponding to staff that are working today, key is staffname, value is object
    
    LunchWeightsDict = CreateTimeSlotWeights(LunchSlotTimes, LunchWeights)

    
    # Create the GUI Application window and hand it the communication function so tht it can communicate with Main
    MainWindow = GUIHandler.RosterWindow(messageFromGUI)

    # Update GUI and respond to User interations -- Can put other checks and logic in this loop if needed
    while True:
        MainWindow.update()
        # TODO: Handle GUI being closed -- Quit main