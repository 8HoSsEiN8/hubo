
import hubo_ach as ha
import ach
import sys
import time
import datetime
import timeit
from ctypes import *

#tic=timeit.default_timer()
tic=time.time()

#print datetime.time()
#print time.time()
#print time.clock()
#print time.clock()
#print time.clock()
time.sleep(.001)

#toc=timeit.default_timer()
toc=time.time()
print toc - tic #elapsed time in seconds
print tic
print toc

import datetime

print 'Earliest  :', datetime.time.min
print 'Latest    :', datetime.time.max
print 'Resolution:', datetime.time.resolution



start_time = datetime.datetime.now()
time.sleep(0.001)
print "difference =", datetime.datetime.now() - start_time
print datetime.datetime.now()
print datetime.datetime.now()
print datetime.datetime.now()
print datetime.datetime.now()

