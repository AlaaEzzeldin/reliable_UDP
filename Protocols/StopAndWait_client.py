import socket
from client import requested_file, server_IP, server_port
from FSM.connection import NewConnection

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(requested_file.encode(), (server_IP, server_port))  # request new file



cl = NewConnection('client')
cl.on_event(0)
cl.on_event(1)
