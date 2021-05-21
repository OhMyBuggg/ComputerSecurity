import netifaces

def translate_to_slash(netmask):
    temp = netmask.rsplit('.')
    number = 0
    for i in range(4):
        number = number << 8
        number += int(temp[i])
    slash = 0
    for i in range(32):
        if number % 2 == 1:
            slash = i
            break
        number = number >> 1
    return 32 - slash

def get_local_info():
    
    interfaces = netifaces.interfaces()

    for interface_name in interfaces:
        interface = netifaces.ifaddresses(interface_name)
        try:
            # dictionary
            normal_internet = interface[netifaces.AF_INET][0]
            address = normal_internet['addr']
            netmask = normal_internet['netmask']
            broadcast = normal_internet['broadcast']
            # slash = IPAddress(netmask).netmask_bits()
            slash = translate_to_slash(netmask)
            # obtain gateway
            gws = netifaces.gateways()
            gw = gws['default'][netifaces.AF_INET][0]
            return address, netmask, broadcast, str(slash), gw
        except KeyError:
            print("this interface: ", interface_name, " isn't feasible")
            continue

if __name__=='__main__':
    address, netmask, broadcast, slash, gw = get_local_info()
    print("address: ", address)
    print("netmask: ", netmask)
    print("broadcast: ", broadcast)
    print("slash: ", slash)
    print("gw: ", gw)