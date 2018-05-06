import socket
import os
from simulation_helper import get_must_dropped_packets
from Protocols.settings import write_log

os.chdir("C:\\Files\\Engineering\\colllege\\term 8\\Networks\\projects\\reliable_UDP\\Data_files")  # change directory

# reading input file
server_input_file = open("server_input.txt", "r")
Input_list = server_input_file.read().splitlines()
server_port = int(Input_list[0])
Max_sending_window_size = int(Input_list[1])
random_SeedValue = int(Input_list[2])
loss_Probability = float(Input_list[3])


# initialize the global variables
chunk_size = 500  # size of each data packet
Header_size = 12  # size of header in bytes
server_ip = '127.0.0.1'


def waiting_for_new_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', server_port))
    write_log("Waiting for client...\n")
    requested_file, client_address = sock.recvfrom(100)
    write_log(str(("Server:   Requested file", requested_file, "from", client_address)))
    return requested_file, client_address
