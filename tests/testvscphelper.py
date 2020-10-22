# FILE: vscphelper.py
#
# VSCP UDP functionality
#
# This file is part of the VSCP (http://www.vscp.org)
#
# The MIT License (MIT)
#
# Copyright (c) 2000-2020 Ake Hedman, Grodans Paradis AB <info@grodansparadis.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
from ctypes import *
import time

sys.path.append('../')
from vscp.vscphelper import *
from vscp import *

print("------------------------------------------------------------------------")
h1 = newSession()
if (0 == h1 ):
    closeSession(h1)
    raise ValueError('Unable to open vscphelp library session')

print("------------------------------------------------------------------------")
print("\n\nConnection in progress...")
rv = open(h1,"192.168.1.7:9598","admin","secret")
if vscp.VSCP_ERROR_SUCCESS == rv :
    print("Command success: open on channel 1")
else:
    closeSession(h1)
    raise ValueError('Command error: open on channel 1  Error code=%d' % rv )

if ( vscp.VSCP_ERROR_SUCCESS == isConnected(h1) ):
    print("CONNECTED!")
else:
    print("DISCONNECTED!")

print("------------------------------------------------------------------------")
print("command: noop")
rv = lib.vscphlp_noop( h1 )
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: ''noop''  Error code=%d' % rv )

print("------------------------------------------------------------------------")
print("command: doCommand")
command = "NOOP\r\n"
rv = doCommand( h1, command )
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: ''doCommand''  Error code=%d' % rv )    

print("------------------------------------------------------------------------")
print("command: Get sever version")
(rv,v1,v2,v3) = getVersion(h1)
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: ''getVersion''  Error code=%d' % rv )
print("Server version = %d.%d.%d" % (v1.value,v2.value,v3.value))

print("------------------------------------------------------------------------")
ex = vscp.vscpEventEx()
ex.timestamp = 0
ex.vscpclass = 10
ex.vscptype = 99
ex.sizedata = 3
ex.data[0] = 1
ex.data[1] = 2
ex.data[2] = 3
print("command: sendEventEx")
rv = sendEventEx(h1,ex)
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: sendEventEx  Error code=%d' % rv )

e = vscp.vscpEvent()
e.timestamp = 0
e.vscpclass = 20
e.vscptype = 9
e.sizedata = 3
p = (c_ubyte*3)()
p[0] = 11
p[1] = 22
p[2] = 33
e.pdata = cast(p, POINTER(c_ubyte))

print("------------------------------------------------------------------------")
print("command: sendEvent")
rv = sendEvent(h1,e)
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: sendEvent  Error code=%d' % rv )
e.pdata = None    

print("------------------------------------------------------------------------")
print("Waiting for incoming data...")

cntAvailable = c_uint(0)
while cntAvailable.value==0:
    print('Still waiting...')
    time.sleep(1)
    isDataAvailable(h1,cntAvailable)

print('%d event(s) is available' % cntAvailable.value)

for i in range(0,cntAvailable.value):
    ex = vscp.vscpEventEx()
    if vscp.VSCP_ERROR_SUCCESS == receiveEventEx(h1,ex):
        ex.dump()

print("------------------------------------------------------------------------")
print("Empty VSCP server queue")
rv = clearDaemonEventQueue(h1)
if vscp.VSCP_ERROR_SUCCESS == rv:
    print("Server queue now is empty")
else:
    print("Failed to clear server queue", rv )

print("------------------------------------------------------------------------")
print("Enter receive loop. Will lock channel on just receiving events")
if vscp.VSCP_ERROR_SUCCESS == enterReceiveLoop(h1):
    print("Now blocking receive - will take forever if no events is received")
    
    rv = -1
    while vscp.VSCP_ERROR_SUCCESS != rv:
        ex = vscp.vscpEventEx()
        rv = blockingReceiveEventEx(h1,ex, 1000 )
        
        if vscp.VSCP_ERROR_SUCCESS == rv: 
            ex.dump()
        else:
            if vscp.VSCP_ERROR_TIMEOUT != rv:
                print("Blocking receive failed with error code = %d" % rv )
                break;
            print("Waiting for event in blocking mode rv=%d" % rv)

    if vscp.VSCP_ERROR_SUCCESS == quitReceiveLoop(h1):
        print("Successfully left receive loop")
    else:
        print("failed to leave receive loop")

else:    
    print("Failed to enter receive loop!")

# Set filter
print("------------------------------------------------------------------------")
filter = vscp.vscpEventFilter()
filter.mask_class = 0xFFFF                      # All bits should be checked
filter.filter_class = vscp_class.CLASS1_MEASUREMENT   # Only CLASS1.MEASUREMENT received
rv = setFilter( h1, filter )
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: setFilter  Error code=%d' % rv )

print("Enter receive loop. Will lock channel for 60 seconds or unit CLASS1.MEASUREMENT event received")
if vscp.VSCP_ERROR_SUCCESS == enterReceiveLoop(h1):
       
    cnt = 0   
    rv = -1
    while vscp.VSCP_ERROR_SUCCESS != rv:
        ex = vscp.vscpEventEx()
        rv = blockingReceiveEventEx(h1,ex, 1000 )
        
        if vscp.VSCP_ERROR_SUCCESS == rv: 
            ex.dump()
        else: 
            print("Waiting for CLASS1.MEASUREMENT event in blocking mode rv=%d" % rv)

        cnt += 1
        if ( cnt > 60 ):
            print("Not received within 60 seconds. We quit!")
            break

    if vscp.VSCP_ERROR_SUCCESS == quitReceiveLoop(h1):
        print("Successfully left receive loop")
    else:
        print("failed to leave receive loop")

else:    
    print("Failed to enter receive loop!")


# Clear filter
print("------------------------------------------------------------------------")
print("Clear filter")
filter = vscp.vscpEventFilter()
filter.clear()
rv = setFilter( h1, filter )
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: setFilter  Error code=%d' % rv )  

# Get statistics
print("------------------------------------------------------------------------")
print("Get statistics")
statistics = vscp.VSCPStatistics()
rv = getStatistics( h1, statistics )
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: setStatistics  Error code=%d' % rv )      
print("Received frames = %d" % statistics.cntReceiveFrames)
print("Transmitted frames = %d" % statistics.cntTransmitFrames)
print("Receive data = %d" % statistics.cntReceiveData)
print("Transmitted data = %d" % statistics.cntTransmitData)
print("Overruns = %d" % statistics.cntOverruns)
     
# Get status
print("------------------------------------------------------------------------")
print("Get status")
status = vscp.VSCPStatus()
rv = getStatus( h1, status )
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: getStatus  Error code=%d' % rv )
print("Channel status = %d" % status.channel_status) 
print("Channel status = %d" % status.lasterrorcode) 
print("Channel status = %d" % status.lasterrorsubcode)

# Get DLL version
print("------------------------------------------------------------------------")
print("Get DLL version")
(rv,dllversion) = getDLLVersion( h1 )
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: getStatus  Error code=%d' % rv )
print("DLL version = %d" % dllversion.value)

# Get vendor string
print("------------------------------------------------------------------------")
print("Get vendor string")
(rv,strvendor) = getVendorString( h1 )
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: getVendorString  Error code=%d' % rv )
print("Vendor string = %s" % strvendor)

# Get driver info string
print("------------------------------------------------------------------------")
print("Get driver info string")
(rv,strdriverinfo) = getDriverInfo( h1 )
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: getDriverInfo  Error code=%d' % rv )
print("Driver info string = %s" % strdriverinfo)

print("------------------------------------------------------------------------")
print("command: close")
rv = close(h1)
if vscp.VSCP_ERROR_SUCCESS != rv :
    closeSession(h1)
    raise ValueError('Command error: close  Error code=%d' % rv )

print("------------------------------------------------------------------------")
print("command: closeSession")
closeSession(h1)


