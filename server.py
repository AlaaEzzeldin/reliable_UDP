import socket
import os

os.chdir("C:\\Files\\Engineering\\colllege\\term 8\\Networks\\projects")  # change directory

# reading input file
server_input_file = open("reliable_UDP\Data_files\server_input.txt", "r")
Input_list = server_input_file.read().splitlines()
server_port = int(Input_list[0])
Max_sending_window_size = Input_list[1]
Random_SeedValue = Input_list[2]
loss_Probability = Input_list[3]
# print("server input file:", "server_port", server_port, ",Max_sending_window_size:", Max_sending_window_size,
#    ",Random_SeedValue:", Random_SeedValue, ",loss_Probability:", loss_Probability)

# initialize the global variables


def waiting_for_new_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #server_ip = socket.gethostname()  # Server IP
    server_ip= '127.0.0.1'
    sock.bind((server_ip, server_port))
    print("Waiting for client...")
    requested_file, client_address = sock.recvfrom(100)
    print("Received Messages:", requested_file, "from", client_address)
    print(requested_file)
    return requested_file, client_address


# establish a connect and as for new file


