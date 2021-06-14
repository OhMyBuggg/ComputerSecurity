import socket 
target_host = "140.113.207.240" 
target_port = 8833

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

client.connect((target_host, target_port)) 

response = client.recv(4096)

client.send("anything\n".encode()) 

response = client.recv(4096)

client.send("n\n".encode()) 

response = client.recv(4096)

client.send("\Va[\n".encode()) 
 
response = client.recv(4096) 
print(response)