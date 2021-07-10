import socket 
target_host = "140.113.207.240" 
target_port = 8824

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

client.connect((target_host, target_port)) 

response = client.recv(4096)

client.send("anything\n".encode()) # input anything

response = client.recv(4096)

client.send("n\n".encode()) # choose no

response = client.recv(4096)

client.send("\Va[\n".encode()) # input \Va[ or \V![
 
response = client.recv(4096) 
print(response)