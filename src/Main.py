# Local deps
from Normies import WSUStaff # Defines WSU Staff class
from DataCollectors import * # Reading data from text files
import GUIHandler 

# Python bundled deps
import webbrowser
from datetime import datetime, timedelta
import json
from tkinter import *
import random
import pickle # Used for serializing staff to files as well as converting serialized files to staff objects

# External deps
import pyperclip
import win32com.client
import requests


def loadStaff():
    # Load only staff that are working today
    return

def saveStaff():
    # If file does not exist for staff member, create it
    return
