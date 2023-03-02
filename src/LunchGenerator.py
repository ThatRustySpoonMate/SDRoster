from datetime import datetime, timedelta
from ShiftRetreiver import  get_shift_data
import Normies

def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))

# This function creates a distribution of lunch weights across a designated timeframe
# Weights refer to how favourable a time slot is for a person to be assigned to, higher relative weight == more lunch slots
# Times between key times are assigned a weight that is interpolated between adjacent key time
#	time_weight_dict - dictionary of times, and their associated weights. Key should be a datetime object
#	lunches_start - when lunches are elligible to be assigned from
#	Returns a dictionary of times and their associated weights
def GetLunchSlots(time_weights_dict, lunches_start, lunches_end, time_interval):
	
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
	time_step = timedelta(minutes=time_interval)

	# Calculate the number of time slots

	num_slots = int((key_times[-1] - key_times[0]) / time_step) + 1
	left_time = key_times[0]
	right_time = key_times[-1]
	# Calculate the value for each time slot
	weights = {}
	for i in range(num_slots):
		# Calculate the current time slot
		current_time = key_times[0] + i * time_step
		weight = 0
		print(current_time)
		# Determine the nearest key times
		for j in range(len(key_times)):
			if current_time >= key_times[j]:
				left_time = key_times[j]
			if current_time <= key_times[j]:
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
		weights[datetime.strftime(current_time, "%I:%M%p")] = weight

	return weights

# This function assigns users to a lunch time
# @TODO expand functionality, currently is first come first serve, early staff are assigned earlier lunches
# Implemting preferred lunches
#	lunch_slots - disctionary of lunch times and their free slots
#	list_of_staff - list of staff to be rostered
def GetStaffLunches(lunch_weight_dict, list_of_staff, lunch_interval, roster_date):
	staff_list = list_of_staff
	lunch_weights = list(lunch_weight_dict.items())
	lunch_times = list(lunch_weight_dict.keys())
	staff_lunches = {}

	# assign users to their preferred lunch
	for name,staff in staff_list.items():
		if staff_list[name].set_lunchtime is not None and staff_list[name].start_time.date is roster_date.date:
			staff_list[name].actual_lunch = roster_date.date + staff_list[name].set_lunchtime.hours() 	

	start_time = hour_rounder(min([staff_list[name].start_time for name,staff in staff_list.items()])) # get start time from the earliest start time in the list of valid staff
	end_time = hour_rounder(max([staff_list[name].start_time for name,staff in staff_list.items()])) # get end time from the latest start time in the list of valid staff

	# Holds staff in hour batches based on their start time
	staff_hour_batches = {}

	# Create a set for each hour interval from start time to end time
	current_time = start_time
	while current_time < end_time:
		staff_hour_batches[datetime.strftime(current_time, "%I:%M%p")] = set()
		current_time += timedelta(hours=lunch_interval)

	# Add staff to each hour batch
	for name,staff in staff_list.items():
		time = hour_rounder(staff_list[name].start_time) # Rounding required for people starting before opening
		for interval_start in staff_hour_batches:
			interval_end = interval_start + timedelta(hours=lunch_interval)
			if interval_start <= time < interval_end:
				staff_hour_batches[interval_start].add(staff)

	total_weight = sum(lunch_weight_dict.values())

	# Initialize a list to store the values for each timeslot
	# lunch_slots = [0] * len(lunch_weight_dict.items())
	lunch_slots = {}
	# iterate through each batch, which are assigned to a window of valid lunch times
	lunch_start_time = min([time for time,weight in lunch_weight_dict.items()]) # get start of lunchtime
	for batch_time,batch in staff_hour_batches.items():
		num_staff = len(batch)
		for time in range(lunch_start_time, lunch_start_time + timedelta(hours=2)):
			weight = lunch_weight_dict[time]
			lunch_slots[time] += int(num_staff * weight / total_weight)
			num_staff -= lunch_slots[time]
			total_weight -= weight
		lunch_start_time += timedelta(hours=2)

	print(lunch_slots)

	# iterates through the staff and lunch slots
	# if a lunch time has no free slots, it is removed from the list
	# first item of list is always accessed, as it will be the next earliest lunch time
	# after assigning someone to that time, the number of free slots is decreased
	for name,staff in staff_list.items():
		for time in lunch_slots:
			while lunch_slots[time] == 0:
				del lunch_times[time]

			staff_lunches[staff.name] = lunch_times[time]
			lunch_slots[time] -= 1

	return staff_lunches
