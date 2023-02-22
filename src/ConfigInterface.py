# TODO: Write functions that interface with serialised data files
import os 
configFP = "{}\\config\\config.txt".format(os.getcwd())

# Function for reading the value of a key from the config file
# param1 - string: The config item you would like to read the value of e.g. lunchStart 
def readValue(configItem):
    output = ""

    with open(configFP, "r") as configFile:
        while configItem not in output:
            output = configFile.readline()
            print(output)
            if(output == "--end--"):
                return None
                
        output = output.split("#")[1]

    return output

# Function for writing the value of a key to the config file
def writeValue(configItem, value):

    with open(configFP, "r") as configFile:
        fileContents = configFile.readlines()
        configFile.writelines() # look into recording the line that needs to be changed and only changing that line instead of reading and writing the whole file contents
        print(fileContents)
        pass

    return


if __name__ == "__main__":
    # Example uses
    #print(readValue("lunchStart"))
    writeValue("lunchStart", "12:00")