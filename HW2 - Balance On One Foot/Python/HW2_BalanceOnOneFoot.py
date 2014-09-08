#!/usr/bin/python

def sWait(seconds):
	print "sleeping for: ", seconds, " seconds"
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	stic = state.time
	while(1):	
		time.sleep(.1)
		[statuss, framesizes] = s.get(state, wait=True, last=False)
		if ((state.time - stic) > seconds):
			break	
	
import hubo_ach as ha
import ach
import sys
import time, timeit
from ctypes import *

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
#s.flush()
#r.flush()

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=False)

pos = [.01, .02, .04, .06, .08, .1, .12, .14, .17]
for p in pos:
	ref.ref[ha.LHR] = -p
	ref.ref[ha.LAR] = p

	ref.ref[ha.RHR] = -p
	ref.ref[ha.RAR] = p

	# Write to the feed-forward channel
	r.put(ref)

	sWait(.2)

pos = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
for p in pos:
	ref.ref[ha.RHP] = -p
	ref.ref[ha.RKN] = 2*p
	ref.ref[ha.RAP] = -p

	# Write to the feed-forward channel
	r.put(ref)

	sWait(.1)

sWait(.2)

i = 0
while(1):
	pos = [.1, .4, .5, .7, .8]
	for p in pos:
		ref.ref[ha.LHP] = -p
		ref.ref[ha.LKN] = 2*p
		ref.ref[ha.LAP] = -p
		ref.ref[ha.LSR] = p + .1
		ref.ref[ha.LHR] = -(.17 - (p*.1))
		#ref.ref[ha.LAR] = (.17 + (p*.1))
		#ref.ref[ha.RHR] = -(.17 + (p*.1))
		#ref.ref[ha.RAR] = (.17 + (p*.1))

		# Write to the feed-forward channel
		r.put(ref)

		sWait(.1)
	
	pos = [.7, .5, .4, .1, 0]
	for p in pos:
		ref.ref[ha.LHP] = -p
		ref.ref[ha.LKN] = 2*p
		ref.ref[ha.LAP] = -p
		ref.ref[ha.LSR] = p + .1
		ref.ref[ha.LHR] = -(.17 - (p*.1))
		#ref.ref[ha.LAR] = (.17 + (p*.1))
		#ref.ref[ha.RHR] = -(.17 + (p*.1))
		#ref.ref[ha.RAR] = (.17 + (p*.1))

		# Write to the feed-forward channel
		r.put(ref)

		sWait(.1)
	
	i = i + 1
	if (i > 5):
		break


# Close the connection to the channels
r.close()
s.close()

