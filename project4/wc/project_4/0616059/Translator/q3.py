import pwn

if __name__=='__main__':
    conn = pwn.remote('140.113.207.240', 8833)
    
    conn.recvuntil('Give me some input:')
    # send arbitrary sentence
    conn.send("shvnlsvs\n")
    
    conn.recvuntil('Anything else to translate?(y/n)')
    # select n
    conn.send("n\n")

    conn.recvuntil('Tell me what are you looking for in my language:')
    # type magic string
    conn.send("\V![\n")

    # print flag
    print(conn.recvline())
    pass