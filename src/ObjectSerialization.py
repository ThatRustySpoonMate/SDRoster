import pickle, os # Used for serializing staff to files as well as converting serialized files to staff objects
from Normies import ITSDStaff


objectsFP = "{}//data//".format(os.getcwd())
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
        return staffObj
    else:
        # If no file exists, create the object anew and save it to the newly created file
        newStaff = ITSDStaff(staffDetails[0], 1, 0, 0, 0, None, None) # Maybe change default behaviour for new staff?
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


if __name__ == "__main__":
    print(__loadStaffObject("Ethan"))


def getAllStaffNames():
    allStaffFiles = os.listdir(objectsFP)

    # Loop through each file in directory
    for iter, key  in enumerate(allStaffFiles):
        allStaffFiles[iter] = key.replace(".sus", "")

    return allStaffFiles
