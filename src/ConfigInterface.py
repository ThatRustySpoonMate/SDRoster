# TODO: Write functions that interface with serialised data files
import os, datetime, time

DELIMITER = "#"
configFP = "{}\\config\\config.txt".format(os.getcwd())

# Function for reading the value of a key from the config file
# param1 - string: The config item you would like to read the value of e.g. lunchStart 
def readValue(configItem, thisDate=datetime.datetime.today().date()):

    output = ""

    with open(configFP, "r") as configFile:
        while configItem not in output:
            output = configFile.readline().replace("\n", "") # Continue reading line-by-line
            if(output == "--end--"):
                return None
                
        output = parseLine(output)
    
    # Return different data types for certain config items
    if(configItem == "lunchStart" or configItem == "lunchEnd"): # Handle datetime returns
        output = datetime.datetime(thisDate.year, thisDate.month, thisDate.day, int(output.split(":")[0]), int(output.split(":")[1])) 
    
    return output

# Takes a string to search with 
# Returns array of strings. 
# array contains all config items with the search term in them 
def readValues(configItemKey):
    output = []
    readLine = ""

    with open(configFP, "r") as configFile:

        while(readLine != "--end--"):
            readLine = configFile.readline().replace("\n", "")

            if(configItemKey in readLine):
                output.append(readLine) # Continue reading line-by-line

    return output

def parseLine(line):
    return line.split(DELIMITER)[1]
            


# Function for writing the value of a key to the config file
def writeValue(configItem, value):
    successful = False

    with open(configFP, "r+") as configFile:
        fileContents = configFile.readlines() # Read file contents as an array 

        # Loop through all lines in the array
        iter = 0
        for iter in range(0, len(fileContents)):

            # Locate string to change 
            if fileContents[iter].split(DELIMITER)[0] == configItem:
                fileContents[iter] = fileContents[iter][:len(configItem)+1] + value + "\n" # Overwrite the value for the given key
                successful = True
            iter += 1 

        
    with open(configFP, "w") as configFile2: # Opens file in writing mode and clears the contents
        configFile2.writelines(fileContents) # Write the new array back to the file
    
    return successful


if __name__ == "__main__":
    # Example uses
    #print(readValue("lunchStart"))
    #print(writeValue("lunchStart", "11:00"))
    print(readValues("lunchWeights"))
    pass