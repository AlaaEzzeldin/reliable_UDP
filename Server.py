import socket

'''
Well-known port number for server.
Maximum sending sliding-window size (in datagram units).
Random generator seedvalue.
Probability p of datagram loss (real number in the range [ 0.0 , 1.0 ]).
'''

# reading input file
server_input_file = open("server_input.txt", "r")
Input_list = server_input_file.read().splitlines()
server_port = int(Input_list[0])
Max_sending_window_size = Input_list[1]
Random_SeedValue = Input_list[2]
loss_Probability = Input_list[3]
print("server input file:", "server_port", server_port, ",Max_sending_window_size:", Max_sending_window_size,
      ",Random_SeedValue:", Random_SeedValue, ",loss_Probability:", loss_Probability)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Server_ip = socket.gethostname()  # Server IP
print(Server_ip)
sock.bind((Server_ip, server_port)) # attaching a specific port to the created socket
while True:
    print("Waiting for client...")
    requested_file, client_address = sock.recvfrom(1024)
    print("Received Messages:", requested_file, "from", client_address)

