import sys
from ctypes import *

sys.path.append('../')
from vscp import *

# GUID conversion
gg = vscp.guid()
print("After creation:", gg.getAsString())

gg.setFromString("00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF")
print("guid = ", gg.getAsString())

gg.reverse()
print("reverse guid = ", gg.getAsString())
print("guid[2] = ", gg.getAt(2), format("%02X" % gg.getAt(2)))
gg.setAt(2,33)
print("setat(2,33) guid[2] = ", gg.getAt(2), format("%02X" % gg.getAt(2)))

print("LSB = ", gg.getLSB(), format("%02X" % gg.getLSB()))
gg.setLSB(12)
print("setLSB(12) LSB = ", gg.getLSB(), format("%02X" % gg.getLSB()))

print("setLSB(12) LSB = ", gg.getNickname(), format("%02X" % gg.getNickname()))

print("Nickname = ", format("%02X" % gg.getNickname()), "Nickname ID", format("%04X" % gg.getNicknameID()))

gg.setNickname(99)
print("After setNickname (99) - Nickname = ", format("%02X" % gg.getNickname()), "Nickname ID", format("%04X" % gg.getNicknameID()))

gg.setNicknameID(0xaa55)
print("After setNicknameID (0xAA55) - Nickname = ", format("%02X" % gg.getNickname()), "Nickname ID", format("%04X" % gg.getNicknameID()))

gg.clear()
print("After clear() guid = ", gg.getAsString())
print("isNULL() = ", gg.isNULL())
gg.setNicknameID(0xaa55)
print("(False) isNULL() = ", gg.isNULL())

print("(False) isSame() = ", \
    gg.isSame( gg.getArrayFromString("99:99:99:00:00:00:00:00:00:00:00:10:10:10:10:00")))

print("guid = ", gg.getAsString())
print("(True) isSame() = ", \
    gg.isSame( gg.getArrayFromString("00:00:00:00:00:00:00:00:00:00:00:00:00:00:AA:55")))

a = vscp.guidarray(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0xAA,0x55)
b = vscp.guidarray(11,0,0,0,0,0,0,0,0,0,0,0,0,0,0xAA,0x55)

print("(True) isSame() = ", gg.isSame(a))
print("(False) isSame() = ", gg.isSame(b))


