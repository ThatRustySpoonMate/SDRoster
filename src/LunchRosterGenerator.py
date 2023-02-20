#TODO: Define function 
import datetime

def generateLunchRoster():
    return { "Ethan":datetime.time(11, 30).strftime('%I:%M%p'), "Isaac":datetime.time(12, 00).strftime('%I:%M%p'), "Jack":datetime.time(23, 00).strftime('%I:%M%p') }