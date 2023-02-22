#TODO: Define function 
import datetime

def generatePendingsRoster():
    return { "Ethan":datetime.time(8, 00).strftime('%I:%M%p'), "Isaac":datetime.time(12, 00).strftime('%I:%M%p'), "Jack":datetime.time(22, 00).strftime('%I:%M%p') }