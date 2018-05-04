import socket
from client import client_ip, client_port, server_IP, server_port, requested_file, client_received_file
from Protocols.settings import write_log, file_path
import utility

# make a file request
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', client_port))
sock.sendto(requested_file.encode(), (server_IP, server_port))  # request new file
print("client requested the file:", requested_file)
event = "".join(('client requested the file:', requested_file, "\n"))
log_file=open(file_path, "a")
write_log(event)
log_file.close()

# receiving data
while 1:
    received_packet, server_address = sock.recvfrom(512)
    check_sum, length, seq_number, data = utility.extract_data(received_packet)  # extract the data
    received_file = open(client_received_file, "ab")
    received_file.write(data)  # deliver the data to the upper layer
    received_file.close()
    ack_packet = utility.make_ack_packet(0, seq_number)  # create ACK packet
    sock.sendto(ack_packet, server_address)  # send ACK packet to the server

