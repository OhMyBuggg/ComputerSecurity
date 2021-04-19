import netifaces
from netaddr import IPAddress


interfaces = netifaces.ifaddresses('wlp3s0')
# dictionary
normal_internet = interfaces[netifaces.AF_INET][0]
address = normal_internet['addr']
netmask = normal_internet['netmask']
broadcast = normal_internet['broadcast']
slash = IPAddress(netmask).netmask_bits()

print(address + ' ' + netmask + ' ' + broadcast + ' ' + str(slash))