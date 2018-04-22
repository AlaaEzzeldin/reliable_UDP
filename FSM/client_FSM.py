import socket
#from Client import requested_file, server_IP, server_port

# request file
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##ock.sendto(requested_file.encode(), (server_IP, server_port))