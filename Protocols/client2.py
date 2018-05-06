import socket
from client import client_ip, client_port, server_IP, server_port, requested_file, client_received_file
from Protocols.settings import write_log, file_path
import utility
import time

# make a file request
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', client_port))
sock.sendto(requested_file.encode(), (server_IP, server_port))  # request new file


event = "".join(('Client:   client requested the file:', requested_file, "\n"))
# write_log(event)
received_file = open(client_received_file, "ab")
EOF =0
# receiving data



while 1:
    received_packet, server_address = sock.recvfrom(512)
    if received_packet == "":
        received_file.close()
        write_log("all the file has been received ^___^")
        exit(0)
    elif received_packet != b'':
        check_sum, length, seq_number, data = utility.extract_data(received_packet)  # extract the data
        write_log("".join(("Client:   received packet with seq_number= ", str(seq_number))))
        received_file.write(data)  # deliver the data to the upper layer
        ack_packet = utility.make_ack_packet(0, seq_number)  # create ACK packet
        sock.sendto(ack_packet, server_address)  # send ACK packet to the server
        write_log("".join(("Client:   ack is sent for packet with seq_number=  ", str(seq_number))))

