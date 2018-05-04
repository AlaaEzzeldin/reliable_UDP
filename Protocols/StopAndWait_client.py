import socket
from client import requested_file, server_IP, server_port, client_port, client_ip, sliding_window_size
from FSM.connection import NewConnection

if sliding_window_size > 1:
    print("Stop and wait protocol can't handle more than 1 datagram window size")
elif sliding_window_size == 1 :
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server_IP, client_port))
    print(server_IP, server_port)
    print(client_port, client_ip)
    sock.sendto(requested_file.encode(), (server_IP, server_port))  # request new file
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.bind((client_ip, client_port))
    cl = NewConnection('client')
    while 1:
        cl.on_event(socket)
