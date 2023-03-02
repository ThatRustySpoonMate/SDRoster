import pickle, os, json, datetime# Used for serializing staff to files as well as converting serialized files to staff objects
from Normies import ITSDStaff



objectsFP = "{}//data//".format(os.getcwd())
JSONFP = "{}//integrations//roster.json".format(os.getcwd())
FILE_EXT = ".sus"


# Make sure param1 is full name from the staff object
# Private func
def __loadStaffObject(staffName): 
    # Load the object of the requested staff member, if it does not exist, create it
    allStaffFiles = os.listdir(objectsFP)

    # Search for the .sus file
    found = False
    for fileName in allStaffFiles:
        if(staffName in fileName):
            found = True


    if(found):
        # File is present, load it then return loaded object
        try:
            # de-serialize file contents into an ITSDStaff Object
            inputFilePath = objectsFP + staffName + FILE_EXT
            inputFile = open(inputFilePath, 'rb')
            staffObject = pickle.load(inputFile)
            inputFile.close()
            return staffObject

        except Exception as exc:
            # If failed -- likely due to no or corrupt file contents -- return None so a base object is created and saved
            return None

    else:
        # Unable to locate staff file
        newFile = open(objectsFP + staffName + FILE_EXT, mode = "x", encoding = "UTF-8")
        newFile.close()
        return None

# Private function 
def __saveStaffObject(staffObj):
    # If file does not exist for staff member, create it
    # Load the object of the requested staff member, if it does not exist, create it
    allStaffFiles = os.listdir(objectsFP)

    # Search for the .sus file
    found = False
    for fileName in allStaffFiles:
        if(staffObj.full_name in fileName):
            found = True

    
    if(found):
        # Save object to corresponding file
        outputFilePath = objectsFP + staffObj.full_name + FILE_EXT
        outputFile = open(outputFilePath, 'wb')
        pickle.dump(staffObj, outputFile)
        outputFile.close()

        return True
    else:
        return False

    return
    
# Param1: single dim array of staff details that contain:
#				[0] - Full Name "Joe Blow"
#				[1] - Shift start time - %Y-%m-%d%I:%M%p format -- optional
#				[2] - Shift End time - %Y-%m-%d%I:%M%p format   -- optional
def loadSingleStaff(staffDetails):
    
    staffObj = __loadStaffObject(staffDetails[0])

    if(staffObj != None):
        # If file exists, and we have loaded an object, return it 
        print("File already exists")
        return staffObj
    else:
        # If no file exists, create the object anew and save it to the newly created file
        print("File Doesn't exist, creating it... {}".format(staffDetails[0]))
        newStaff = ITSDStaff(staffDetails[0])
        __saveStaffObject(newStaff)
        return newStaff 

    return

# Param1: 2d array of staff details that contain:
#				[0] - Full Name "Joe Blow"
#				[1] - Shift start time - %Y-%m-%d%I:%M%p format -- optional
#				[2] - Shift End time - %Y-%m-%d%I:%M%p format   -- optional
def loadMultipleStaff(staffDetailsArray):
    output = []

    for staffDetail in staffDetailsArray:
        output.append(loadSingleStaff(staffDetail))

    return output


# Param1: Single staff object
# Returns returns true/false depending on success or error
def saveSingleStaff(staffObj):
    return __saveStaffObject(staffObj)


# Param1: array of staff objects to save
# Returns a same-length array of 1/0s corresponding to save successes vs failures
def saveMultipleStaff(staffDetailsArray):
    status = []

    for staffObj in staffDetailsArray:
       status.append(__saveStaffObject(staffObj) )
    
    return status

# Param1: dict of {staffName:ITSDStaffObject, staffName:ITSDStaffObject}
# Designed to work with StaffWorking dict in Main
# Returns a same-length array of 1/0s corresponding to save successes vs failures
def saveMultipleStaffDict(staffDetailsDict):
    status = []

    for sName, sObj in staffDetailsDict.items():
        status.append(__saveStaffObject(sObj) )
    
    return status


def deleteStaff(staffName):

    allStaffFiles = os.listdir(objectsFP)

    # Search for the .sus file
    found = False
    for fileName in allStaffFiles:
        if(staffName in fileName):
            found = True


    if(found):
        # File is present, try to delete it 
        try:
            # Construct path to file and delete it
            inputFilePath = objectsFP + staffName + FILE_EXT
            os.remove(inputFilePath)
            return True
        except:
            # Unable to delete file
            return False
    else:
        # Unable to find file
        False



def getAllStaffNames():
    allStaffFiles = os.listdir(objectsFP)

    # Loop through each file in directory
    for iter, key  in enumerate(allStaffFiles):
        allStaffFiles[iter] = key.replace(".sus", "")

    return allStaffFiles


def outputToJson(staffWorking):
    rosterFile = open(JSONFP, 'w')

    jsonInput = {}

    for staffName, staffObj in staffWorking.items():
        jsonInput[staffName] = [staffObj.actual_lunchtime.strftime('%I:%M%p'), staffObj.email_address]

    jsonOutput = json.dumps(jsonInput, indent=4) 

    rosterFile.write(jsonOutput)

    rosterFile.close()




if __name__ == "__main__":
    print(__loadStaffObject("Ethan"))
