from datetime import datetime
import requests

# The types of shifts that can be assigned in humanity
#@TODO decouple from being hardcoded, if new shift types are introduced, currently the source code will
# need to be edited, this should be adjustable in the GUI
shift_types = {"Casual - SD", "Full Time - SD", "Senior Queue Escalation - SD", "Senior Queue Calls - SD", "Extended Hours Support - SD"}

# This file is used for calling Humanity's API, GET Shifts
# link to API reference: https://platform.humanity.com/reference/get-shifts

# When the API is called, the response will contain all shifts visible to the caller
# Response needs to be trimmed to contain only Service Desk employees, as well as contain only data relevantt ot the roster generator

# API call requires date range, and the access token as part of the call
# API returns all information about a shift, documentation doesn't seem to include a list of all provided fields

# Required Data after trimming:
#	name
#	shift start
#	shift end
#	shift length

# This function calls the API uses today's date as the date range
# This function also validates that the call was completed successfully
# Checking for valid keys and the API response
# 	Return value - array of formatted shift objects that contain:
#				[0] - Full Name "Joe Blow"
#				[1] - Shift start time - %Y-%m-%d%I:%M%p format
#				[2] - Shift End time - %Y-%m-%d%I:%M%p format
def get_shift_data():
	# Gets the current date and formats into a string to be used in API call
	# Formats a datetime object into a string, format is year-month-day i.e 2022-06-25
	today_date = datetime.today().strftime('%Y-%m-%d')

	# @TODO load token file correctly, below lines are temporary
	api_token_file = open('tokenFile.txt') # place holder file opening
	api_token = api_token_file.read() 

	request_url = "https://www.humanity.com/api/v2/shifts?start_date=" + today_date + "&end_date=" + today_date + "&access_token=" + api_token

	# URL for testing
	# request_url = "https://www.humanity.com/api/v2/shifts?start_date=asfasf" + "&end_date=" + "2023-02-17" + "&access_token=" + api_token

	api_response = requests.get(request_url)

	# Return code for API call for valid API key
	# 1 - valid key
	status_code = int(api_response.text[10])

	# if API key is valid
	if status_code == 1:
		
		# this is the raw response data from the API, not gauranteed to contain shift data, may be an error
		raw_shift_data = api_response.json()['data']

		# returned without errors
		if api_response.status_code == 200:
			formatted_shift_data = trim_data(raw_shift_data, today_date)

			if not formatted_shift_data:
				print("No shifts after formatting raw shift data")
			else:
				print(formatted_shift_data)
				return formatted_shift_data
		else: # returns with errors
			#@TODO proper GUI feedback
			api_error_data = api_response.json()
			print(api_error_data['data']) # prints general error message
			print(api_error_data['error']) # print specific hint error
			
	else:
		# temp output
		#@TODO GUI prompt for new key
		api_error_data = api_response.json()
		print(api_error_data['data']) # prints general error message
		print(api_error_data['error']) # print specific hint error
		



# This function takes in a response and removes data note required for the roster generator
#	shift_list - Raw response data from API call, should be in the form of an object array
#	today_date - datetime object containing the current day
# 	Return value - array of shift objects that contain:
#				[0] - Full Name "Joe Blow"
#				[1] - Shift start time - %Y-%m-%d%I:%M%p format
#				[2] - Shift End time - %Y-%m-%d%I:%M%p format
def trim_data(raw_shift_data, today_date):
	shifts = []

	# iterate through all the raw shift data
	for item in raw_shift_data:
		
		# check if the shift has a valid shift title, there are employees to roster
		if item['schedule_name'] in shift_types and item['employees'] is not None:
			
			# get the length of the shift, as well as the start and end times
			shift_length = item['length']
			start_time = datetime.strptime(today_date + item['start_date']['time'], "%Y-%m-%d%I:%M%p") # datetime object
			end_time = datetime.strptime(today_date + item['end_date']['time'], "%Y-%m-%d%I:%M%p") # datetime object

			# iterate through items, creating a shift for an employee
			for employee in item['employees']:
				employee_shift = [employee['name'], start_time, end_time, shift_length]
				shifts.append(employee_shift)

	return shifts

if __name__ == "__main__" :
    return_val = get_shift_data()
		
		
