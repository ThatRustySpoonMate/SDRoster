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
