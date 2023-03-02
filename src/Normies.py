# TODO: Define WSUStaff class

# ITSDStaff is a representation of Service Desk staff currently in the Service Desk group in Humanity
# This should be updated each time the humanity API is called, to account for new staff, as well as staff leaving
# Class holds all employee specific information relevant to this roster generator

# chat_weight		- the proportional chance that an employee has of being placed on chat. The chance is equal to their chat_weight to the total chat_weight of all elligible employees
# chat_competency 	- is a value defining an employees proficiency on chat.
#						0 - employee is inelligible to be put on chat, either in early training, has been given permission to not take chat, or is not able to use chat
#						1 - employee is likely currently in training and needs supervision while on chat, or does not want to be on chat often
#						2 - employee is full trained, is willing and able to do chat
# set_lunchtime 	- this is the set lunch time for an employee, this can be due to an agreed upon situation, or an agreed upon standard lunch time

class ITSDStaff():
	def __init__(self, full_name, chat_weight=1, chat_competency=0, pending_competency=0, on_chat=0, set_lunchtime=None, actual_lunchtime=None, email_address="", humanityID = "-1", shift_start = None, shift_end = None, origin = None):

		if(origin != None): # Copy Constructor
			self.copy_constructor(origin)
		else:
			# Staff Details
			self.full_name = full_name
			self.email_address = email_address
			self.humanityID = humanityID

			# Configuration
			self.pending_competency = pending_competency
			self.chat_weight = chat_weight
			self.chat_competency = chat_competency
			self.on_chat = on_chat # Toggle for eligible for chat today
			self.chat_priority = False 
			self.set_lunchtime = set_lunchtime  # Preferred lunch time

			# Changes day-by-day
			self.actual_lunchtime = actual_lunchtime # Allocated lunchtime for today
			self.pendings_time = None # Allocated pendings time
			self.set_chat = False # Flagged for chat today
			self.start_time = shift_start # shift start time -- format as datetime(2019,1,1,8,0)
			self.end_time =  shift_end # shift end time -- format as datetime(2019,1,1,16,0)

		
	# Copy constructor 
	def copy_constructor(self, origin):
		self.full_name = origin.full_name
		self.chat_weight = origin.chat_weight
		self.chat_competency = origin.chat_competency
		self.pending_competency = origin.pending_competency
		self.on_chat = origin.on_chat
		self.chat_priority = origin.chat_priority
		self.set_lunchtime = origin.set_lunchtime
		self.email_address = origin.email_address
		self.humanityID = origin.humanityID

		self.actual_lunchtime = origin.actual_lunchtime
		self.pendings_time = origin.pendings_time # Allocated pendings time
		self.set_chat = origin.set_chat

		self.start_time = origin.start_time
		self.end_time = origin.end_time

	
	# increments chat weight proportional to the employee's chat competency so that more experienced people are more likely to be on chat
	# this should be called whenever the employee is not assigned to chat
	# chat weighting used to more evenly distribute chat, as employees chance of being on chat increases as chat_weight increases
	# @TODO implement more robust chat weighting increment?
	def increment_chat_weight(self):
		self.chat_weight += self.chat_competency

	# toggles employee's eligibility to be on chat
	# this is seperate from chat competency to enable adhoc chat rostering
	def toggle_on_chat(self):
		self.on_chat = not self.on_chat

	# resets users chat_weight to default value
	# this should be called whenever a user is assigned to chat
	def reset_chat_weight(self):
		self.chat_weight = 1


