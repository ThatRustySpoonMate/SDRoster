import datetime

# Function that takes in an array of time slots, and the corresponding weights for each time slot and creates a dict
# Params should be of equal length
def CreateTimeSlotWeights(timeSlotsIn, weightsIn):
    output = {}

    if(len(timeSlotsIn) != len(weightsIn) ):
        return False

    for iter in range(0, len(timeSlotsIn)):
        output[ datetime.time( int(timeSlotsIn[iter].split(":")[0]) , int(timeSlotsIn[iter].split(":")[1] )) ] = weightsIn[iter]

    return output