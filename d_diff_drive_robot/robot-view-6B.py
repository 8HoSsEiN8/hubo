#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2014, Daniel M. Lofaro <dan (at) danLofaro (dot) com>
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
import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

import actuator_sim as ser
#-----------------------------------------------------
#--------[ Do not edit above ]------------------------
#-----------------------------------------------------

# Add imports here
import timeit
import csv
from myFunctions import setVelocity
from myFunctions import setAngleLimit

def sWait(seconds):
	[status, framesize] = t.get(tim, wait=False, last=True)
	tic = tim.sim[0]
	#print "TIC: ", tic
	while(1):	
		[status, framesize] = t.get(tim, wait=False, last=True)
		toc = tim.sim[0]
		if ((toc - tic) > seconds):
			break	
	#print "TOC: ", toc, "\t(", (toc - tic), " seconds )"
	

f = open('6B.csv', 'wt')
writer = csv.writer(f)
writer.writerow( ('Real Time', 'Sim Time') )


#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------
dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_CHAN_VIEW   = 'robot-vid-chan'
ROBOT_TIME_CHAN  = 'robot-time'
# CV setup 
r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()

i=0


print '======================================'
print '============= Robot-View ============='
print '========== Daniel M. Lofaro =========='
print '========= dan@danLofaro.com =========='
print '======================================'
ref.ref[0] = 0
ref.ref[1] = 0
while True:
    [status, framesize] = t.get(tim, wait=False, last=True)
    if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
        pass
        #print 'Sim Time = ', tim.sim[0]
    else:
        raise ach.AchException( v.result_string(status) )

#-----------------------------------------------------
#--------[ Do not edit above ]------------------------
#-----------------------------------------------------
    # Main Loop
    # Def:
    # tim.sim[0] = Sim Time
    F = 20.0
    delT = 1.0 / F
    sWait(delT)
    i=i+1
    
    if (i == 1):
		start_time_r = timeit.default_timer()
		[status, framesize] = t.get(tim, wait=False, last=True)
		start_time_s = tim.sim[0]
		
		buff = setVelocity(0, 1, 57)
		ref = ser.serial_sim(r,ref,buff)
		buff = setVelocity(1, 0, 57)
		ref = ser.serial_sim(r,ref,buff)
		
    if (i == 1300):
		buff = setVelocity(0, 1, 0)
		ref = ser.serial_sim(r,ref,buff)
		buff = setVelocity(1, 0, 0)
		ref = ser.serial_sim(r,ref,buff)
		f.close()
		sys.exit("Done!")
		
    time_r = timeit.default_timer() - start_time_r
    [status, framesize] = t.get(tim, wait=False, last=True)
    time_s = tim.sim[0] - start_time_s
    print "real time: ", time_r, "\tsim time:", time_s
    writer.writerow( (time_r, time_s) )
#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------
