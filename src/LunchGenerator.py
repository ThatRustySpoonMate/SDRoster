from datetime import datetime, timedelta
from ShiftRetreiver import  get_shift_data

# This function creates a dsitribution of lunch times across a designated timeframe
# The times are distributed by weight, with certain times being more preferrable
# Times between key times are assigned a weight that is interpolated between adjacent key time
#	time_weight_dict - dictionary of times, and their associated weights. Key should be a datetime object
#	lunches_start - when lunches are elligible to be assigned from
#	lunches_end - the last available timeslot a lunch can be assigned
#	num_staff - number of staff to be assigned
def GetLunchSlots(time_weights_dict, lunches_start, lunches_end, num_staff):
	
	# split dictionary into lists of keys and values
	# need to be in lists so they can be iterated through when interpolating weights
	key_times = list(time_weights_dict.keys())
	key_weights = list(time_weights_dict.values())


	# If no key times are available, it will default to an even distribution, slightly favouring the morning
	# due to the way shifts are handed out, thre may be an additional shift appended at the end
	# to avoid this, the end time should be a lower weighting
	if key_times is None:
		key_times = [
			lunches_start,
			lunches_end
		]
		key_weights = [1,1]
	else:
		# if the first and last key time are not equal to the start or end of lunch, the it will assign default values
		if (key_times[0] != lunches_start):
			key_times.insert(0, lunches_start)
			key_weights.insert(0, 1)		
		if (key_times[len(key_times) - 1] != lunches_end):
			key_times.append(lunches_end)
			key_weights.append(1)

	# Define the time step as a timedelta object
	time_step = timedelta(minutes=30)

	# Calculate the number of time slots

	num_slots = int((key_times[-1] - key_times[0]) / time_step) + 1
	left_time = key_times[0]
	right_time = key_times[-1]
	# Calculate the value for each time slot
	weights = []
	for i in range(num_slots):
		# Calculate the current time slot
		current_time = key_times[0] + i * time_step
		
		# Determine the nearest key times
		for j in range(len(key_times)):
			if current_time >= key_times[j]:
				left_time = key_times[j]
			if current_time < key_times[j]:
				right_time = key_times[j]
				break
		
		# Interpolate the weight for the current time slot
		if left_time == right_time:
			weight = key_weights[j]
		else:
			left_weight = key_weights[j-1]
			right_weight = key_weights[j]
			weight = left_weight + (right_weight - left_weight) * (current_time - left_time) / (right_time - left_time)
		
		# Append the weight to the values list
		weights.append(weight)

	value = num_staff

	total_weight = sum(weights)

	# Initialize a list to store the values for each timeslot
	values = [0] * len(weights)

	# Distribute the value according to the weights
	for i in range(len(weights)):
		weight = weights[i]
		values[i] = int(value * weight / total_weight)
		value -= values[i]
		total_weight -= weight

	# create a dictionary of available times and the number of slots associated with them
	avilable_slots = {}

	for slot in range(num_slots):
		current_time = key_times[0] + slot * time_step
		avilable_slots[current_time.time()] = values[slot]

	return avilable_slots

# This function assigns users to a lunch time
# @TODO expand functionality, currently is first come first serve, early staff are assigned earlier lunches
# Implemting preferred lunches
#	lunch_slots - disctionary of lunch times and their free slots
#	list_of_staff - list of staff to be rostered
def GetStaffLunches(lunch_slots, list_of_staff):
	staff_list = list_of_staff
	lunch_dict = lunch_slots
	lunch_times = list(lunch_dict.keys())
	staff_lunches = {}

	# iterates through the staff and lunch slots
	# if a lunch time has no free slots, it is removed from the list
	# first item of list is always accessed, as it will be the next earliest lunch time
	# after assigning someone to that time, the number of free slots is decreased
	for staff in staff_list:
		while lunch_dict[lunch_times[0]] == 0:
			del lunch_times[0]

		staff_lunches[staff[0]] = lunch_times[0]
		lunch_dict[lunch_times[0]] -= 1

	return staff_lunches
