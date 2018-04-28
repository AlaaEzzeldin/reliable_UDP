import socket
from client import requested_file, server_IP, server_port
from FSM.connection import NewConnection

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(requested_file.encode(), (server_IP, server_port))  # request new file

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(('192.168.113.1', 50000))

cl = NewConnection('client')
while 1:
    cl.on_event(socket)
    cl.on_event(socket)
