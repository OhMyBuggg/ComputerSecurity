import socket 
target_host = "140.113.207.240" 
target_port = 8831

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

client.connect((target_host, target_port)) 

response = client.recv(4096)

client.send("3735928495\n".encode()) 

response = client.recv(4096)

client.send("YOUSHALLNOTPASS\n".encode()) 

response = client.recv(4096) 
response = client.recv(4096) 
print(response)