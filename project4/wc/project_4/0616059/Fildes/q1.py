import pwn

if __name__=='__main__':
    conn = pwn.remote('140.113.207.240', 8831)

    # type magic number let fd equal 0
    conn.recvuntil('Give me a magic number')
    conn.send('3735928495\n')

    # type magic string
    conn.recvuntil('OK, then give me a magic string')
    conn.send('YOUSHALLNOTPASS\n')

    # conn.interactive()
    print(conn.recvallS())
    
    conn.close()
    pass