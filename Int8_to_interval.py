"""
http://www.selfadsi.org/deep-inside/microsoft-integer8-attributes.htm
In other cases, an Integer8 value has to be interpreted as a time interval. Time intervals are always negative numbers. Their absolute value can be read as a Microsoft Filetime structure then, expressing 100-nanosecond steps which determine the length of the time interval.
"""

import sys
from struct import pack, unpack

def getInterval(value):
    if '0x' in value:
        uint64 = pack('Q', int(value, 16))
        int64 = unpack('q', uint64)[0]
    else:
        int64 = int(value)
    return -(int64 / 10000000 / 60)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} <Integer8_value>'.format(sys.argv[0]))
        exit(1)
    print('Interval in minutes: {}'.format(getInterval(sys.argv[1])))
