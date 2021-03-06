# This program evaluates the running time of the mechanisms. With R changes.

import random
import math
import time
from copy import deepcopy
# Let there be 1000 users.
n = 1000
# Let the upper bound of the users' unit costs be 10.
k_max = 10.0
# Remaining tasks number is 1000.
rt = 1000
# the maximum payment to each user is 100.
Pm = 100
# Total budget of the platform is 10000.
R = 10000
# Platform utility
u_p = R
# The outputs will be stored in the text file loss_truthful_dis.txt
f = open('running_time_R.txt', 'w')
# Test samples 1000
n_test = 1000;

class SensingUser:
	'''the class for a user participating in sensing.'''
	k = 0;	# the unit cost
	upper_k = 0;	# the upper cost bound
	lower_k = 0;	# the lower cost bound
	s = 0;	# the user strategy
	n_tasks = 0;	# sensing task number of this user
	p = 0;	# payment to this user
	u = 0;	# user utility
	def __init__(self):
		# The initial s_i = kappa_i
		self.s = self.k = random.uniform(0.01, k_max)
		# additionally we have the cost bounds
		self.upper_k = self.k + random.uniform(0.01, k_max/2.0)
		self.lower_k = self.k - random.uniform(0.01, k_max/2.0)
		if self.upper_k > k_max:
			self.upper_k = k_max
		if self.lower_k < 0:
			self.lower_k = 0.01

n=100	# Initially we have 100 participating users.
R = 0
while R<10000:	
	R = R + 1000;	
	
	# our mechanism
	run_time = time.time()	# start timing...
	Pm = R/n
	remaining = rt	# remaining tasks
	
	for i in range(n_test):
		# Initialize the users.
		users = []
		for i in range(n):
			users.append(SensingUser())

		# Compute the d.
		d = k_max
		for user in users:
			if user.upper_k - user.lower_k < 2*d:
				d = (user.upper_k - user.lower_k)/2

		# Compute the m.
		m = 1
		while (m+1)*(m+2)*d < Pm:
			m = m+1

		# Recorrect the d
		if m*d > k_max:
			d = k_max / m

		# Let us compute the sensing time and the payment for each user.
		# Also we calculate each user utility and the platform utility.
		for user in users:
			user.n_tasks = m - math.floor(user.s / d)
			if user.n_tasks > remaining:
				user.n_tasks = 0
			if user.n_tasks < 0:
				user.n_tasks = 0
			user.p = d * user.n_tasks * (2*m + 1 - user.n_tasks) / 2.0
			user.u = user.p - user.k * user.n_tasks
			u_p = u_p - user.p	
			remaining = remaining - user.n_tasks
	
	result1 = (time.time()-run_time)/n_test*1000
	
	# infocom 13 mechanism
	run_time = time.time()	# start timing...
	
	for i in range(n_test):
		remaining = rt	# remaining tasks
		# Initialize the users.
		users = []
		for i in range(n):
			users.append(SensingUser())

		# Let us compute the sensing time and the payment for each user.
		# Also we calculate each user utility and the platform utility.
		m = 100
		d = 0.1
		for user in users:
			sum = 0
			for k in range(n/100):
				sum = sum + users[k].s
			user.n_tasks = m - math.floor(sum / n / d*100)
			if user.n_tasks > remaining:
				user.n_tasks = 0
			if user.n_tasks < 0:
				user.n_tasks = 0
			user.p = d * user.n_tasks * (2*m + 1 - user.n_tasks) / 2.0
			user.u = user.p - user.k * user.n_tasks
			u_p = u_p - user.p	
			remaining = remaining - user.n_tasks
	
	result2 = (time.time()-run_time)/n_test*1000
	
	# Output the statistical results.
	f.write('{0:f} {1:f} {2:f} \n'.format(R, result1, result2)) #ms
	
f.close()
