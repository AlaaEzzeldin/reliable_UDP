
import socket
import os

os.chdir("C:\\Files\\Engineering\\colllege\\term 8\\Networks\\projects\\reliable_UDP\\Data_files")  # change directory
# needed data in the input file
'''
 IP address of server.
 Well-known port number of server.
 Port number of client.
 Filename to be transferred (should be a large file).
 Initial receiving sliding-window size (in datagram units).

'''
# reading client input file
client_input_file = open("client_input.txt", "r")
Input_list = client_input_file.read().splitlines()
server_IP = Input_list[0]
server_port = int(Input_list[1])
client_port = int(Input_list[2])
requested_file = Input_list[3]
sliding_window_size = int(Input_list[4])
# print("client input file:" ,"server_IP:", server_IP, ",server_port:", server_port, ",client_port:", client_port,
#      ",sliding_window_size:", sliding_window_size)

client_ip = '192.168.1.3'
client_received_file = "client_received_file"
received_file = open(client_received_file, "wb")

