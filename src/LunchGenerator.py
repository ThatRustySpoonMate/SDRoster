from datetime import datetime, timedelta
from ShiftRetreiver import  get_shift_data

def GetLunchSlots(weighted_times, time_weights, lunches_start, lunches_end, num_staff):
	# Define the key times as datetime objects
	key_times = weighted_times
	key_weights = time_weights

	if key_times is None:
		key_times = [
			lunches_start,
			lunches_end
		]
		key_weights = [1,1]
	else:
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

	results = {}

	for slot in range(num_slots):
		current_time = key_times[0] + slot * time_step
		results[current_time] = values[slot]

	return results

def GetStaffLunches(lunchslots, list_of_staff):
	staff_list = list_of_staff
	lunch_dict = lunchslots
	lunch_times = list(lunch_dict.keys())
	staff_lunches = {}

	for staff in staff_list:
		while lunch_dict[lunch_times[0]] == 0:
			del lunch_times[0]

		staff_lunches[staff[0]] = lunch_times[0]
		lunch_dict[lunch_times[0]] -= 1

	return staff_lunches