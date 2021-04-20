import netifaces
from netaddr import IPAddress
import math

# interfaces = netifaces.ifaddresses('wlp3s0')
# # dictionary
# normal_internet = interfaces[netifaces.AF_INET][0]
# address = normal_internet['addr']
# netmask = normal_internet['netmask']
# broadcast = normal_internet['broadcast']
# slash = IPAddress(netmask).netmask_bits()

# print(address + ' ' + netmask + ' ' + broadcast + ' ' + str(slash))
netmask = "255.255.255.0"
temp = netmask.rsplit('.')
print(temp)
number = 0
for i in range(4):
    number = number << 8
    number += int(temp[i])
    # number = number << (8*i)
    print(number)
slash = 0
for i in range(32):
    print(number)
    if number % 2 == 1:
        slash = i
        break
    number = number >> 1
print( slash)