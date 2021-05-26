
# test paramiko This is to set the policy to use when connecting to a server that doesn't have a host key in either the system or local HostKeys object
# https://stackoverflow.com/questions/10670217/paramiko-unknown-server#43093883
# success connect

import paramiko



client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.99.213', username='csc2021', password='csc20210')
stdin, stdout, stderr = client.exec_command('ls')
for line in stdout:
    print('... ' + line.strip('\n'))
client.close()