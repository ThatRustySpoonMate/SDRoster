# OLD SCRIPT -- USED AS A REFERENCE

import tkinter
# import matplotlib.pyplot as plt
import webbrowser
from datetime import datetime, timedelta
import requests
import json
from tkinter import *
import pyperclip
import random
import win32com.client


"""
Rules of this generator:
- Lunch is not required and therefore will not be allocated for shifts < 5 hours
- If number of staff
- Lunch can be allocated between 10:30am and 3:30pm
- Lunch will be allocated to all staff in 30min intervals 
- Ragu will always be allocated to take lunch at 1:00pm
- Chat main and chat backup will be randomly selected from a pool
"""

# Read saved token from file
tokenFile = open('tokenFile.txt', 'a')
tokenFile = open('tokenFile.txt')
savedToken = tokenFile.read()

todaysDate = datetime.today().strftime('%Y-%m-%d')
# 12 count day for testing
# todaysDate = "2022-09-15"
# 7 count day for testing
#todaysDate = "2022-09-16"
# Thursdays
# todaysDate = "2022-09-29"
# todaysDate = "2022-10-27"
# todaysDate = "2022-11-02"
todaysDate = datetime.strptime(todaysDate, "%Y-%m-%d")
todaysDateStr = datetime.strftime(todaysDate, "%Y-%m-%d")
todaysDateStrFormatted = datetime.strftime(todaysDate, "%d-%m-%Y")

def GeneratePendingsRoster(shiftList):
    counter = 0 # Used to exit the while loop if no staff meet the requirements
    earliestStart = datetime(todaysDate.year, todaysDate.month, todaysDate.day, 8, 00, 00)
    latestEnd = datetime(todaysDate.year, todaysDate.month, todaysDate.day, 18, 00, 00)

    pendingsRoster = []
    availableShifts = shiftList.copy()
    usedShifts = set()

    currentTime = earliestStart
    while currentTime < latestEnd and counter < 15:
        if not availableShifts:
            break
            
        randomInt = random.randint(0, len(availableShifts) - 1)

        # Make sure the allocated time falls within the staff's shift
        shiftStart = datetime.strptime(todaysDateStr + availableShifts[randomInt][1], "%Y-%m-%d%I:%M%p")
        shiftEnd = datetime.strptime(todaysDateStr + availableShifts[randomInt][2], "%Y-%m-%d%I:%M%p")

        if shiftStart <= currentTime <= (shiftEnd + timedelta(hours=-1)):
            # Make sure the same staff is not rostered twice
            if availableShifts[randomInt][0] in usedShifts:
                availableShifts.pop(randomInt)
                continue
            usedShifts.add(availableShifts[randomInt][0])
            pendingsRoster.append([availableShifts[randomInt][0], currentTime.strftime("%I%p")])
            currentTime += timedelta(hours=1)
            availableShifts.pop(randomInt)
        counter+=1

    return pendingsRoster


def createLunchRoster(shiftDetails, selectedDate):
    # shiftDetails contains the following:
    # [0] = Full Name
    # [1] = Shift Start (datetime)
    # [2] = Shift End (datetime)

    lunchRoster = []
    staffCount = len(shiftDetails)
    allocationCycleCounter = 0

    # Create a list of 30-minute time blocks between 10:30am and 3:30pm

    today = datetime.strptime(selectedDate, "%Y-%m-%d")

    # Set the valid range in which lunch can be allocated
    if spreadVar.get() == 1:
        startTime = datetime(today.year, today.month, today.day, 10, 30)  # 10:30AM
        endTime = datetime(today.year, today.month, today.day, 14, 30)  # 2:30PM
    else:
        startTime = datetime(today.year, today.month, today.day, 11, 00)  # 11:00AM
        endTime = datetime(today.year, today.month, today.day, 14, 00)  # 2:00PM

    # Set the invalid range for which lunches can not be allocated due to team meeting
    meetingStart = datetime(today.year, today.month, today.day, 13, 30, 0)  # 1:30PM
    meetingEnd = datetime(today.year, today.month, today.day, 15, 30, 0)  # 3:30PM

    # Special requirement
    raguLunch = datetime(today.year, today.month, today.day, 13, 00, 0) # 1:00PM

    timeBlock = startTime
    timeBlocks = []

    while timeBlock <= endTime:
        # Exclude the 2:30pm to 3:30pm time block on Thursdays
        if not (timeBlock.weekday() == 3 and (meetingStart < timeBlock < meetingEnd)):
            timeBlocks.append(timeBlock)
        timeBlock += timedelta(minutes=30)

    # Sort the shifts list by shift start times
    shiftDetails.sort(key=lambda x: x[1])

    # Allocate a time block to each staff member in a round-robin fashion
    raguRostered = False
    i = 0
    for shift in shiftDetails:
        # Skip shifts that are less than 5 hours
        if (shift[2] - shift[1]).total_seconds() / 3600 <= 5:
            continue
        lunchTime = timeBlocks[i % len(timeBlocks)]
        lunchRoster.append([shiftDetails[i][0], lunchTime.strftime('%I:%M%p'), lunchTime, shiftDetails[i][1]])
        i += 1


    shiftsSortedByLunchStart = sorted(lunchRoster, key=lambda x: x[2])

    sortedRoster = []
    for x in range(len(lunchRoster)):
        if lunchRoster[x][0] == "Navaratnam Raguram":
            raguRostered = True
        else:
            if shiftsSortedByLunchStart[x][1] == '01:00PM' and raguRostered:
                sortedRoster.append(["Navaratnam Raguram", '01:00PM', raguLunch,
                                     shiftsSortedByLunchStart[x][3]])
                raguRostered = False
            sortedRoster.append([lunchRoster[x][0], shiftsSortedByLunchStart[x][1], shiftsSortedByLunchStart[x][2],
                                 shiftsSortedByLunchStart[x][3]])
    return sortedRoster

"""def CreateGraph(shiftList, roster):
    startTimes = []
    endTimes = []

    for shift in shiftList:
        start = datetime.strftime(shift[3], "%H%M")
        start = int(start)
        end = datetime.strftime(shift[4], "%H%M")
        end = int(end)
        # X axis parameter:
        startTimes.append(start)
        endTimes.append(end)

    # Find earliest start and latest end
    earliestStart = startTimes[0]
    latestEnd = endTimes[0]
    for x in startTimes:
        start = int(x)
        if start < earliestStart:
            earliestStart = start
    for x in endTimes:
        end = int(x)
        if end > latestEnd:
            latestEnd = end

    xstaffed = []
    xstaffedFormatted = []
    yplot = []
    xTime = str(earliestStart)
    numberOf30MinIntervals = int((latestEnd - earliestStart) / 50)

    for x in range(numberOf30MinIntervals + 2):
        xTime = str(xTime)
        if len(xTime) == 3:
            xTime = "0" + xTime

        # Convert Time String to 24 hour
        dTime = datetime.strptime(todaysDateStrFormatted + " " + xTime, "%d-%m-%Y %H%M")
        xTime = int(datetime.strftime(dTime, "%H%M"))
        sTime = str(datetime.strftime(dTime, "%I:%M"))

        xstaffed.append(xTime)
        xstaffedFormatted.append(sTime)

        yplot.append(0)
        if xTime % 100 == 0:
            xTime += 30
        else:
            xTime += 70

    # Get number of staff working at each interval
    for shift in shiftList:
        startInt = int(datetime.strftime(shift[3], "%H%M"))
        endInt = int(datetime.strftime(shift[4], "%H%M"))
        for x in range(len(xstaffed)):
            if startInt <= int(xstaffed[x]) < endInt:
                yplot[x] += 1

    # Plot staffed hours
    xi = list(range(len(xstaffed)))
    # plt.fill_between(xi, yplot, color="skyblue")
    # (xi, yplot, color="#0E77B2", label="Rostered Coverage")
    plt.bar(xi, yplot, color="skyblue")
    # Set x and y axis headings
    plt.xlabel("Time")
    plt.ylabel("Number of Staff")
    # Set tick values
    plt.xticks(xi, xstaffedFormatted, rotation='vertical')
    # Set chart title
    plt.title("Daily Coverage")
    # Set window title
    fig = plt.gcf()
    fig.canvas.manager.set_window_title('Coverage Chart')

    # Plot staff hours with lunch factored in
    for lunch in roster:
        lunchStartInt = int(datetime.strftime(lunch[2], "%H%M"))
        lunchEndInt = lunchStartInt + 99
        for x in range(len(xstaffed)):
            if lunchStartInt <= int(xstaffed[x]) <= lunchEndInt:
                yplot[x] -= 1
    # plt.fill_between(xi, yplot, color="#BE7EEE")
    # plt.plot(xi, yplot, color="#9F4FE5", label="Lunch Coverage")
    plt.bar(xi, yplot)
    # plt.legend(loc="upper right")
    # plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.show()"""

def GenerateEmail(emailSubject, bodyText):
    outlook = win32com.client.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = "itds-ace-sdteam@westernsydney.edu.au"
    mail.Subject = emailSubject
    mail.Body = bodyText
    mail.Display(True)

def callback(url):
    webbrowser.open_new(url)

def ShowAlert(text, colour):
    alertLabel.config(text=text, fg=colour)
    alertLabel.grid(row=3, column=0)

def ClearAlert():
    alertLabel.grid_forget()

def CopyToClipboard(text):
    pyperclip.copy(text)
    ShowAlert("Copied", "green")

def Reset():
    for widgets in resultsFrame.winfo_children():
        widgets.destroy()
    for widgets in shiftDetailsFrame.winfo_children():
        widgets.destroy()
    for widgets in pendingsFrame.winfo_children():
        widgets.destroy()

def GoToday():
    global todaysDate
    todaysDate = datetime.today()
    global todaysDateStr
    todaysDateStr = datetime.strftime(todaysDate, "%Y-%m-%d")
    global todaysDateStrFormatted
    todaysDateStrFormatted = datetime.strftime(todaysDate, "%d-%m-%Y")

    dateLabel.config(text=todaysDateStrFormatted)

def GoNextDate():
    global todaysDate
    todaysDate = todaysDate+timedelta(hours=24)
    global todaysDateStr
    todaysDateStr = datetime.strftime(todaysDate, "%Y-%m-%d")
    global todaysDateStrFormatted
    todaysDateStrFormatted = datetime.strftime(todaysDate, "%d-%m-%Y")

    dateLabel.config(text=todaysDateStrFormatted)

def GoPreviousDate():
    global todaysDate
    todaysDate = todaysDate+timedelta(hours=-24)
    global todaysDateStr
    todaysDateStr = datetime.strftime(todaysDate, "%Y-%m-%d")
    global todaysDateStrFormatted
    todaysDateStrFormatted = datetime.strftime(todaysDate, "%d-%m-%Y")

    dateLabel.config(text=todaysDateStrFormatted)

def GenerateRoster(todaysDate):
    Reset()

    token = tokenInput.get()
    requestString = "https://www.humanity.com/api/v2/shifts?start_date=" + todaysDateStr + "&end_date=" + todaysDateStr + "&access_token=" + token

    response = requests.get(requestString)

    statusCode = int(response.text[10])
    shifts = "--Shift Details--"

    if statusCode == 1:

        # Save the token to memory
        tokeFile = open("tokenFile.txt", 'w')
        tokeFile.write(token)

        # Function to format results
        def jprint(obj):
            # create a formatted string of the Python JSON object
            text = json.dumps(obj, sort_keys=True, indent=4)

        # Grab all data
        allData = response.json()['data']
        #formatted_json = json.dumps(allData, indent=4)
        #print(formatted_json)
        # Create blank list to populate info into
        shiftList = []
        lateShiftList = []

        if response.status_code == 200:
            # Initialise employee count
            employeeCount = 0
            employeePosition = 0

            for instanceInfo in allData:

                shiftLength = instanceInfo['length']
                startTime = instanceInfo['start_date']['time']
                startTime = datetime.strptime(todaysDateStr + startTime, "%Y-%m-%d%I:%M%p")
                startTimeStr = datetime.strftime(startTime, "%I:%M%p")
                endTime = instanceInfo['end_date']['time']
                endTime = datetime.strptime(todaysDateStr + endTime, "%Y-%m-%d%I:%M%p")
                endTimeStr = datetime.strftime(endTime, "%I:%M%p")

                # Shifts ending at or after 9:00PM will not be included in the lunch roster
                shiftEnd = datetime.strptime(endTimeStr, "%I:%M%p")
                shiftEndLimit = datetime.strptime("09:00PM", "%I:%M%p")

                # Filter out all shifts that aren't SD Casual
                if (instanceInfo['schedule_name'] == "Casual - SD"
                    or instanceInfo['schedule_name'] == "Full Time - SD"
                    # or instanceInfo['schedule_name'] == "Senior Queue Escalation - SD"
                    # or instanceInfo['schedule_name'] == "Senior Queue Calls - SD"
                    or instanceInfo['schedule_name'] == "Extended Hours Support - SD") \
                        and instanceInfo['employees'] is not None:

                    # Get the employees on that shift and sort their info into an array
                    for employee in instanceInfo['employees']:
                        shift = [employee['name'], startTimeStr, endTimeStr, startTime, endTime, shiftLength,
                                 employeePosition]
                        employeePosition += 1
                        if shiftEnd <= shiftEndLimit:
                            shiftList.append(shift)
                            employeeCount += 1
                        else:
                            lateShiftList.append(shift)

            shiftDetails = []

            if len(shiftList) > 0:
                # Used to hold temp values
                previousStart = None
                previousEnd = None

                # Go through the shifts pulled from humanity and populate the lunch roster iteratively
                for shift in shiftList:
                    # ShiftList contains the following:
                    # [0] = Name
                    # [1] = Shift Start (String)
                    # [2] = Shift End (String)
                    # [3] = Shift Start (DateTime)
                    # [4] = Shift End (DateTime)
                    # [5] = Shift Length

                    # Store shift details to be parsed to the createLunchRoster() function
                    shiftDetails.append([shift[0], shift[3], shift[4]])

                    # Create shift details text to display

                    if previousStart == str(shift[1]) and previousEnd == str(shift[2]):
                        shifts += "\n- " + str(shift[0])
                    else:
                        shifts += "\n\n" + str(shift[1]) + " - " + str(shift[2]) + ":"
                        shifts += "\n- " + str(shift[0])

                    previousStart = str(shift[1])
                    previousEnd = str(shift[2])

                # Call function to generate lunch roster
                roster = createLunchRoster(shiftDetails, todaysDateStr)

                # Get chat roster
                earlyChatTeam = []
                lateChatTeam = []
                for shift in shiftList:
                    if shift[0] == "Sine Hamilton" \
                            or shift[0] == "Sado Shanaa" \
                            or shift[0] == "Isabel Winter-Clinch" \
                            or shift[0] == "Isaac Kemp" \
                            or shift[0] == "Sean Maclean" \
                            or shift[0] == "Dean Kilpatrick" \
                            or shift[0] == "Ethan Harris" \
                            or shift[0] == "Liam McInally" \
                            or shift[0] == "Taylor Ridley" \
                            or shift[0] == "Jonathan Allen":

                        # Assign main to a random staff who starts at 8 from the 'chat people' list
                        earlyChatLimit = datetime.strptime(todaysDateStr + "9:00am", "%Y-%m-%d%I:%M%p")
                        shiftStart = datetime.strptime(todaysDateStr + shift[1], "%Y-%m-%d%I:%M%p")
                        if shiftStart <= earlyChatLimit:
                            earlyChatTeam.append(shift)

                        # Assign backup to a random staff who starts at 10am
                        lateStartLimit = datetime.strptime(todaysDateStr + "09:00am", "%Y-%m-%d%I:%M%p")
                        lateEndLimit = datetime.strptime(todaysDateStr + "10:00am", "%Y-%m-%d%I:%M%p")
                        if lateStartLimit <= shiftStart <= lateEndLimit:
                            lateChatTeam.append(shift)

                # Assign someone from the lists randomly
                mainChat = earlyChatTeam[random.randint(0, (len(earlyChatTeam) - 1))][0]

                if len(lateChatTeam) > 0:
                    backupChat = lateChatTeam[random.randint(0, (len(lateChatTeam) - 1))][0]
                    while backupChat == mainChat:
                        backupChat = lateChatTeam[random.randint(0, (len(lateChatTeam) - 1))][0]

                    # Display results neatly
                    results = "--Lunch & Chat Roster--"
                    results += "\nDate: " + todaysDateStrFormatted

                    results += "\n\n-Chats-\n"
                    results += "\nMain - "
                    if len(earlyChatTeam) > 0:
                        results += mainChat
                    results += "\nBackup - "
                    if len(lateChatTeam) > 0:
                        results += backupChat

                    # Display Lunch Results
                    ClearAlert()
                    results += "\n\n-Lunch-"
                    current_time = roster[0][1]
                    for x in range(len(roster)):
                        # Convert lunch time to a datetime object
                        lunch_time = datetime.strptime(roster[x][1], '%I:%M%p')
                        if current_time != lunch_time:
                            # Print lunch time if it is different from the previous time
                            current_time = lunch_time
                            results += "\n\n" + current_time.strftime('%I:%M%p')
                            results += "\n- " + roster[x][0]
                        else:
                            # Print staff name under the same lunch time heading
                            results += "\n- " + roster[x][0]

                # Display staff count in shift details
                for shift in lateShiftList:
                    employeeCount += 1

                shifts += "\n\n Staff Count: " + str(employeeCount)

                rosterResults = Label(resultsFrame, anchor="center", justify=LEFT, text=results, pady=20, padx=20,
                                      bg="black", fg="white")
                rosterResults.pack(fill="y")

                copyToClipboardBtn = Button(master=resultsFrame, text="Copy to Clipboard", padx="10",
                                            command=lambda: CopyToClipboard(results))
                copyToClipboardBtn.pack(pady=10)

                results = "*Please let a senior know if there's an issue with your allocated lunch.*\n\n" + results
                generateEmailBtn = Button(master=resultsFrame, text="Generate Email", padx="10",
                                          command=lambda: GenerateEmail("Lunch & Chat Roster", results))
                generateEmailBtn.pack(pady=(0, 10))

                shiftDetailsLabel = Label(shiftDetailsFrame, anchor="center", justify=LEFT, text=shifts, pady=20, padx=20,
                                          bg="black", fg="white")
                shiftDetailsLabel.pack(fill="y")

                copyToClipboardBtn1 = Button(master=shiftDetailsFrame, text="Copy to Clipboard", padx="10",
                                             command=lambda: CopyToClipboard(shifts))
                copyToClipboardBtn1.pack(pady=10)
                """showChartBtn = Button(master=shiftDetailsFrame, text="View Chart", padx="10",
                                      command=lambda: CreateGraph(shiftList, roster))
                showChartBtn.pack(pady=(0, 10))"""

                # Generate pendings roster
                if pendingsVar.get() == 1:
                    # Create the text string to display results
                    pendingsResults = "--Pendings & Unassigned--\nDate: " + todaysDateStrFormatted + "\n\n"
                    # Generate it
                    pendingsRoster = GeneratePendingsRoster(shiftList)
                    # Add each pending shift to the string
                    for pendingShift in pendingsRoster:
                        pendingsResults += pendingShift[1] + " - " + pendingShift[0] + "\n\n"
                    # Create label to display reslults
                    pendingsResultsLabel = Label(pendingsFrame, anchor="center", justify=LEFT, text=pendingsResults, pady=20,
                                            padx=20,
                                            bg="black", fg="white")
                    pendingsResultsLabel.pack(fill="y")
                    copyToClipboardBtn2 = Button(master=pendingsFrame, text="Copy to Clipboard", padx="10",
                                                 command=lambda: CopyToClipboard(pendingsResults))
                    copyToClipboardBtn2.pack(pady=10)
                    generatePendingEmailBtn = Button(master=pendingsFrame, text="Generate Email", padx="10",
                                              command=lambda: GenerateEmail("Pendings & Unassigned Roster", pendingsResults))
                    generatePendingEmailBtn.pack(pady=(0, 10))

            else:
                ShowAlert("No one rostered ¯\_(ツ)_/¯.", "red")

        else:
            print("Error. Unable to generate shifts. Who knows why?? I don't ¯\_(ツ)_/¯.")
    else:
        ShowAlert("Invalid token key - Please re-authenticate", "red")

# GUI

# Root (main window)
root = Tk()
# root.geometry("500x500")
root.title("Roster Generator")
root.config(background="black")

mainFrame = Frame(root, bg="black")

# Upper toolbar
toolbar = Frame(mainFrame, bg="#262626")
toolbar.grid(row=0, column=0)

tokenLabel = Label(master=toolbar, text="API Token: ", fg="white", bg="#262626")
tokenLabel.grid(row=0, column=1, pady=10, padx=10)

tokenInput = Entry(master=toolbar, width=40, font="Helvetica 10")
tokenInput.insert(0, savedToken)
tokenInput.grid(row=0, column=2)

generateButton = Button(master=toolbar, text="Generate", padx="10", command=lambda: GenerateRoster(todaysDate))
generateButton.grid(row=0, column=3, padx=10)

pendingsVar = tkinter.IntVar()
# pendingsVar.set(1)
pendingsCheckbox = Checkbutton(master=toolbar, text="Pendings", variable=pendingsVar, fg="black")
pendingsCheckbox.grid(row=0, column=4, padx=10)

spreadVar = tkinter.IntVar()
# spreadVar.set(1)
spreadCheckbox = Checkbutton(master=toolbar, text="Spread", variable=spreadVar, fg="black")
spreadCheckbox.grid(row=0, column=5, padx=10)

getTokenButton = Button(master=toolbar, text="Get Token", padx="10",
                        command=lambda: callback("https://westernsydney.humanity.com/app/admin/apiv2/client_id=a3e3febe12a3375f4e66af282bb05db71be0c4f2/"))
getTokenButton.grid(row=0, column=0, padx=5)

# Date navigation toolbar
dateToolbar = Frame(mainFrame, bg="black", pady=5)
dateToolbar.grid(row=1, column=0)

todayButton = Button(master=dateToolbar, font="Helvetica 10", text="Today", padx="5", command=GoToday)
todayButton.grid(row=0, column=1, padx=10)

prevDayBtn = Button(master=dateToolbar, font="Helvetica 10", text="<", padx="5", command=GoPreviousDate)
prevDayBtn.grid(row=0, column=0)

nextDayBtn = Button(master=dateToolbar, font="Helvetica 10", text=">", padx="5", command=GoNextDate)
nextDayBtn.grid(row=0, column=2)

dateLabel = Label(dateToolbar, font="Helvetica 10", fg="white", bg="black", text=todaysDateStrFormatted)
dateLabel.grid(row=1, column=1)

bodyFrame = Frame(mainFrame, bg="black")
bodyFrame.grid(row=2, column=0, sticky="nsew")

resultsFrame = Frame(bodyFrame, background="black")
resultsFrame.grid(row=1, column=0, sticky="")
shiftDetailsFrame = Frame(bodyFrame, bg="black")
shiftDetailsFrame.grid(row=1, column=1, sticky="nsew")
pendingsFrame = Frame(bodyFrame, background="black")
pendingsFrame.grid(row=1, column=2, sticky="nsew")

bodyFrame.grid_columnconfigure(0, weight=1, uniform="group1")
bodyFrame.grid_columnconfigure(1, weight=1, uniform="group1")

alertLabel = Label(mainFrame, font="Helvetica 12 bold", bg="black")

mainFrame.pack(anchor=CENTER)

root.mainloop()
