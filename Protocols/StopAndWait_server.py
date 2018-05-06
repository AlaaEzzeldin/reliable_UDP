from FSM.connection import NewConnection
from server import waiting_for_new_request, Max_sending_window_size ,loss_Probability, random_SeedValue, chunk_size
from simulation_helper import get_must_dropped_packets, print_dropped_seq
import os


os.chdir("C:\\Files\\Engineering\\colllege\\term 8\\Networks\\projects\\reliable_UDP\\Data_files")  # change directory

if Max_sending_window_size > 1:
    print("Stop and wait protocol can't handle more than 1 datagram window size")

elif Max_sending_window_size == 1:
    file, address = waiting_for_new_request()
    requested_file = open(file, "rb")
    server = NewConnection('server')

    # establish a simulation environment
    list_of_dropped = get_must_dropped_packets(file, loss_Probability, chunk_size, random_SeedValue)
    print_dropped_seq(list_of_dropped)
    while 1:
        server.on_event((requested_file, address, list_of_dropped))



