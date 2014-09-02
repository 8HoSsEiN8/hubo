import hubo_ach as ha
import ach
import sys
import time

import timeit
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

# Get in the right position for waiving your hand
ref.ref[ha.LSR] = 0.6
#ref.ref[ha.LSP] = -0.3
#ref.ref[ha.LSY] = 1
#ref.ref[ha.LEB] = -2

# Write to the feed-forward channel
r.put(ref)
tic=timeit.default_timer()

while(1):	
	time.sleep(.001)
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	print "Joint = ", state.joint[ha.LSR].pos
	if (abs(state.joint[ha.LSR].pos - ref.ref[ha.LSR]) < 0.01):
		break

print time.time() - tic #elapsed time in seconds
	

	
#time.sleep(2)
#ref.ref[ha.LEB] = 0
# Write to the feed-forward channel
#r.put(ref)



# Close the connection to the channels
r.close()
s.close()

