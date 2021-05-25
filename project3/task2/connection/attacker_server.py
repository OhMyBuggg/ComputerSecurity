import socket # Import socket module
import netifaces
import sys



def get_local_info():
    
    interfaces = netifaces.interfaces()

    for interface_name in interfaces:
        interface = netifaces.ifaddresses(interface_name)
        try:
            # dictionary
            normal_internet = interface[netifaces.AF_INET][0]
            address = normal_internet['addr']
            netmask = normal_internet['netmask']
            broadcast = normal_internet['broadcast']
            # obtain gateway
            gws = netifaces.gateways()
            gw = gws['default'][netifaces.AF_INET][0]
            return address, netmask, broadcast, gw
        except KeyError:
            print("this interface: ", interface_name, " isn't feasible")
            continue


if __name__ == '__main__':
    host, _, _, _ = get_local_info()
    port = int(sys.argv[1])                    # Reserve a port for your service.
    print(host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # Create a socket object
    # host = socket.gethostname()     # Get local machine name
    # host="192.168.99.215"
    s.bind((host, port))            # Bind to the port
    s.listen(1)                     # Now wait for client connection.

    print("Server listening....")

    while True:
        conn, addr = s.accept()     # Establish connection with client.
        print ("Got connection from", addr)
        # data = conn.recv(1024)
        # print('Server received', repr(data))

        filename='connection.sh'
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
            conn.send(l)
            print('Sent ',repr(l))
            l = f.read(1024)
            f.close()

        print('Done sending')
        # conn.send('Thank you for connecting')
        conn.close()