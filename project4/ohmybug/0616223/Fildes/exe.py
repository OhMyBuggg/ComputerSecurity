import socket 
target_host = "140.113.207.240" 
target_port = 8814

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

client.connect((target_host, target_port)) 

response = client.recv(4096)

client.send("3735928495\n".encode()) # fd = atoi( buf ) - 0xDEADBEAF; let fd = 0, std input

response = client.recv(4096)

client.send("YOUSHALLNOTPASS\n".encode()) # string == YOUSHALLNOTPASS\n

response = client.recv(4096) 
response = client.recv(4096) 
print(response)