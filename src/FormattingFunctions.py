import datetime

# Function that takes in an array of time slots, and the corresponding weights for each time slot and creates a dict
# Params should be of equal length
def CreateTimeSlotWeights(timeSlotsIn, weightsIn):
    output = {}

    if(len(timeSlotsIn) != len(weightsIn) ):
        return False

    for iter in range(0, len(timeSlotsIn)):
        output[timeSlotsIn[iter]] = int(weightsIn[iter])

    return output

# 
# param1: Array of string times
#   e.g. [11:00, 12:00, 13:00, 14:00, 15:00]
# param2: Date of roster generation
#   e.g. datetime.datetime(year, month, day)
# Returns 
def convertToDateTime(timeList, thisDate=datetime.datetime.today().date()):
    output = []

    for time in timeList:
        output.append( datetime.datetime(thisDate.year, thisDate.month, thisDate.day, int(time.split(":")[0]), int(time.split(":")[1])) )

    return output


# param1: string time
#   e.g. "01:00PM"
#   output: datetime.time(13, 00)
def convertStringTimeToDateTime(stringTime):

    hr = int(stringTime.split(":")[0][:2])
    min = int(stringTime.split(":")[1][:2])

    if("pm" in stringTime.lower() and hr != 12):
        hr += 12

    return datetime.time(hr, min)

# Used by GUI Handler for displaying email
# param1: list of names e.g. [Ethan Harris, Isaac Kemp, Jack Holton]
# returns formatted string: "Ethan Harris\nIsaac Kemp\nJack Holton"
def convertListNamesToString(listIn):
    reply = ""

    for name in listIn:
        reply += " - " + name + "\n"

    return reply


# The aim of this function is to 
def validateEmail(email):
    emailValid = True


    # This is very unoptimal but I don't have time to improve it
    try:
        int(email[:8])
    except:
        emailValid = False
    
    if("@westernsydney.edu.au" not in email[7:]):
        emailValid = False
    
    if(email == ""):
        emailValid = True

    return emailValid
