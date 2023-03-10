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
    global ShiftData, ShiftDataTrimmed, NumStaff, RosterDate, LunchWeightsSelected, LunchWeightsDict

    reply = ""
    #print("Main received Request {} from GUI ".format( (reqType, reqParam) )) # Debug option

    if(reqType == 1): # API Key request
        if(reqParam == 0):
            reply = APIKeyHandler.retrieveFromFile()
        else:
            reply = APIKeyHandler.retrieveFromWeb()
        
    elif(reqType == 2): # Request for lunch roster output
        lunchSlots = LunchGenerator.GetLunchSlots(LunchWeightsDict, LunchStart, LunchEnd, NumStaff)

        reply = LunchGenerator.GetStaffLunches(lunchSlots, ShiftData)

        # Apply lunches to staff objects
        for staffName in list(reply.keys()):
            StaffWorking[staffName].actual_lunchtime = reply[staffName]
        
    elif(reqType == 3): # Change assigned lunch
        try:
            # Update the staff member's lunch time in their staff member object
            staffName = reqParam[0]
            lunchTime = reqParam[1]
            StaffWorking[staffName].actual_lunchtime = lunchTime
            # If successful
            reply = GUIHandler.SUCCESS
        except:
            #If unsuccessful
            reply = GUIHandler.NOSUCCESS
    
    elif(reqType == 4): # Requesting to check provided API Key

        if(reqParam == ""):
            return (GUIHandler.NOSUCCESS, "Invalid API Key or API key has expired.")

        # Get staff working today
        ShiftData, NumStaff = ShiftRetreiver.get_shift_data(ShiftTypes, RosterDate, reqParam)

        if(ShiftData != False): # Data is valid
            # Load staff objects into memory 
            for staffDetail in ShiftData:
                StaffWorking[staffDetail[0]] = ObjectSerialization.loadSingleStaff(staffDetail)
                StaffWorking[staffDetail[0]].start_time = staffDetail[1]
                StaffWorking[staffDetail[0]].end_time = staffDetail[2]

            # Store API Key to credentials File
            APIKeyHandler.storeCredentials(reqParam)

            return (GUIHandler.SUCCESS, "API Key Success")

        else: # API Key Error
            return(GUIHandler.NOSUCCESS, "Invalid API Key or API key has expired.")
    

    
    elif(reqType == 5): # Requesting Chat roster output
        reply = ChatRosterGenerator.generateChatRoster()

        # Apply chat roster status to objects
        for sName, allocatedChat in reply.items():
            try:
                StaffWorking[sName].set_chat = allocatedChat
            except:
                pass

    
    elif(reqType == 6): # Requesting Pendings roster output
        reply = PendingsRosterGenerator.generatePendingsRoster()

        # Apply pendings time status to objects
        for sName, allocatedPending in reply.items():
            try:
                StaffWorking[sName].pendings_time = allocatedPending
            except:
                pass
    
    elif(reqType == 7): # Change assigned chats
        try:
            # Update the staff member's chat status in their staff member object
            staffName = reqParam[0]
            chatFlag = reqParam[1]
            StaffWorking[staffName].set_chat = chatFlag
            # If successful
            reply = GUIHandler.SUCCESS
        except Exception as exc:
            #If unsuccessful
            reply = GUIHandler.NOSUCCESS
        
    
    elif(reqType == 8): # Change assigned pendings

        # Update the staff member's pending time in their staff member object
        try:
            staffName = reqParam[0]
            pendingsTime = reqParam[1]
            StaffWorking[staffName].pendings_time = pendingsTime
            reply = GUIHandler.SUCCESS
        except:
            reply = GUIHandler.NOSUCCESS
    
    elif(reqType == 9): # Requesting list of staff names in data file
        reply = ObjectSerialization.getAllStaffNames()

    elif(reqType == 10): # Requesting editable staff information of one staff member (as an object)
        reply = ObjectSerialization.loadSingleStaff(reqParam)
        """
        if(reqParam in list(StaffWorking.keys())):
            # Staff is loaded into memory
            reply = StaffWorking[reqParam]
        else:
            reply = ObjectSerialization.loadSingleStaff(reqParam)
        """
    
    elif(reqType == 11): # Updating editable staff information (When the save button in the staff management page is pressed)
        # reqParam is ITSDStaff object
        
        if(reqParam.full_name in list(StaffWorking.keys())):
            # If object is loaded into memory, edit it in memory and save it to the file
            StaffWorking[reqParam.full_name].copy_constructor(reqParam)
            ObjectSerialization.saveSingleStaff(StaffWorking[reqParam.full_name])
        else:
            # If object is not loaded into memory, load it, make changes and save it 
            thisStaff = ObjectSerialization.loadSingleStaff([reqParam.full_name])
            thisStaff.copy_constructor(reqParam)
            ObjectSerialization.saveSingleStaff(thisStaff)

    elif(reqType == 12): # Request to delete a staff members data file
        reply = ObjectSerialization.deleteStaff(reqParam)
    
    elif(reqType == 13): # Request for roster date
        reply = RosterDate
    
    elif(reqType == 14): # Request for names of assigned chats (From objects)
        # TODO: Add functionality for main/backup chat discrimination
        reply = []

        for sName, sObj in StaffWorking.items():
            if(sObj.set_chat):
                reply.append([sName])
        # Returns 2d array [ [sname, chatType] ]
    
    elif(reqType == 15): # Requesting dict of names and assigned lunches (from objects)
        reply = {}
        workingDate = None
        StaffWorkingCopy = StaffWorking.copy()

        # Strip out NoneType objects 
        for sName, sObj in StaffWorking.items():
            print(sName, sObj.actual_lunchtime)
            if(sObj.actual_lunchtime == None):
                del StaffWorkingCopy[sName]


        workingDict = dict( sorted(StaffWorkingCopy.items(), key=lambda item: item[1].actual_lunchtime) ) # Sort dict by timestamp
        # We need to group together all staff members under the same date, for this we use a dict e.g. { 11:30AM: [Isaac, Ethan]}
        for sName, sObj in workingDict.items():
            # Object has a Lunchtime assigned
            if(workingDate != sObj.actual_lunchtime):
                workingDate = sObj.actual_lunchtime
                reply[workingDate] = [sName]
            else:
                reply[workingDate].append(sName) # This may break
    
    elif(reqType == 16): # Requesting dict of names and assigned pending timeslots
        reply = {}
        workingDate = None
        filteredDict = {}

        # Store all objects that have an assigned time for pendings  
        for sName, sObj in StaffWorking.items():
            if(sObj.pendings_time != None):
                filteredDict[sName] = sObj
        
        workingDict = dict( sorted(filteredDict.items(), key=lambda item: item[1].pendings_time) ) # Sort dict by timestamp
        # We need to group together all staff members under the same date, for this we use a dict e.g. { 11:30AM: [Isaac, Ethan]}
        for sName, sObj in workingDict.items():
            # Object has a Lunchtime assigned
            if(workingDate != sObj.pendings_time):
                workingDate = sObj.pendings_time
                reply[workingDate] = [sName]
            else:
                reply[workingDate].append(sName) # This may break

    elif(reqType == 17): # Set roster generation date (From calendar)
        RosterDate = reqParam
        return GUIHandler.SUCCESS
    
    elif(reqType == 18): # Finalize roster
        for sName, sObj in StaffWorking.items():
            if(not sObj.set_chat): # Not on chat today
                #print("Incrementing {}".format(sName))
                StaffWorking[sName].increment_chat_weight()
            else: # We are on chat today
                #print("Resetting {}".format(sName))
                StaffWorking[sName].reset_chat_weight()
        
        #print("Saving Status: {}".format(ObjectSerialization.saveMultipleStaffDict(StaffWorking)))

        # Could sum the return from saveMultipleStaffDicts call and check if equal to NumStaff. If true, saving successful, if false, atleast one staff was not saved 

    
    elif(reqType == 19): # Read currently selected lunch weights
        reply = LunchWeightsSelected

    elif(reqType == 20): # Write currently selected lunch weights
        LunchWeightsSelected = reqParam
        LunchWeightsDict = CreateTimeSlotWeights(LunchSlotTimes, LunchWeightsSelected)




    elif(reqType == 25): # Finalize roster
        try:
            ObjectSerialization.outputToJson(StaffWorking)
            return GUIHandler.SUCCESS
        except:
            return GUIHandler.NOSUCCESS

        
        
    #print("Returning {}".format(reply))
    return reply



if __name__ == "__main__":

    RosterDate = datetime.today() # Default date that the roster will be generated for
    
    #RosterDate = datetime(2023, 2, 24, 10, 30, 1)
    # Load in config data
    LunchStart = ConfigInterface.readValue("lunchStart")
    LunchEnd = ConfigInterface.readValue("lunchEnd")
    LunchWeightsSelected = ConfigInterface.readValue("lunchWeightsSelected").split(",")
    LunchSlotTimes = convertToDateTime(ConfigInterface.readValue("lunchSlotTimes").split(","), RosterDate )
    ShiftTypes = ConfigInterface.readValue("shiftTypes").split(",")

    NumStaff = 0 # Number of staff working on selected date
    ShiftData = [] # Return from get_shift_data function
    StaffWorking = {} # Dict of all the objects corresponding to staff that are working today, key is staffname, value is object

    LunchWeightsDict = CreateTimeSlotWeights(LunchSlotTimes, LunchWeightsSelected)

    
    # Create the GUI Application window and hand it the communication function so tht it can communicate with Main
    MainWindow = GUIHandler.RosterWindow(messageFromGUI)

    # Update GUI and respond to User interations -- Can put other checks and logic in this loop if needed
    while True:
        MainWindow.update()
        # TODO: Handle GUI being closed -- Quit main