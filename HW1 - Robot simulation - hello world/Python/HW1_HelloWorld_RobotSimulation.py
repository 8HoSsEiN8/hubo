#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2013, Daniel M. Lofaro
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */

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

# Get in the right position for waiving your hand
ref.ref[ha.LSR] = 0.5
ref.ref[ha.LSP] = -0.3
ref.ref[ha.LSY] = 1
ref.ref[ha.LEB] = -2

# Write to the feed-forward channel
r.put(ref)

tic = timeit.default_timer()
while(1):	# Check how long it will take to go to the waving position
	time.sleep(.005)
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	print "Joint LSR = ", state.joint[ha.LSR].pos
	if (abs(state.joint[ha.LSR].pos - ref.ref[ha.LSR]) < 0.01):
		print "Time to get to position: ", (timeit.default_timer() - tic) # elapsed time in seconds
		break

period = 1
nWaves = 30
while(1):	# Start waiving and time yourself
	tic = timeit.default_timer()
	ref.ref[ha.LEB] = -1
	r.put(ref)
	time.sleep(period/2.0)
	ref.ref[ha.LEB] = -2.5
	r.put(ref)
	time.sleep(period/2.0)	
	nWaves = nWaves - 1
	if (nWaves < 0):
		print "waving done!"
		break
	print "Period is: ", (timeit.default_timer() - tic) # elapsed time in seconds
	print nWaves, " waves left!"

# Go back to zeros
ref.ref[ha.LSR] = 0
ref.ref[ha.LSP] = 0
ref.ref[ha.LSY] = 0
ref.ref[ha.LEB] = 0

# Write to the feed-forward channel
r.put(ref)

# Close the connection to the channels
r.close()
s.close()

