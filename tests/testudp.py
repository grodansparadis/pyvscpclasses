
import sys
from ctypes import *

sys.path.append('../')
#import vscp.udp as udp
#from vscp.vscp_class import *
#from vscp.vscp_type import *
from vscp import *

def makeClass2StrMeasurement( vscpclass, vscptype, strval ):
    ex = vscp.vscpEventEx()
    return ex

e = vscp.vscpEvent()
ex = vscp.vscpEventEx()

print(type(e), type(ex))

ex.head = 0

# Measurement Temperature str
ex.vscpclass = vscp_class.VSCP_CLASS2_MEASUREMENT_STR
ex.vscptype = vscp_type.VSCP_TYPE_MEASUREMENT_TEMPERATURE
ex.sizedata = 2
ex.dump()

# Temperature
temperature = "27.235"
#temperature = -22.872
b = bytearray()
#b.extend(temperature)
#print(int(temperature[0].encode("hex")), len(b))
ex = makeClass2StrMeasurement( 1, 2, temperature )


# must use vscpEventEx not vscpEvent
frame = udp.makeVscpFrame( 0, ex )

