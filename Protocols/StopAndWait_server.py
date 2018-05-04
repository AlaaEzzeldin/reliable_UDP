from FSM.connection import NewConnection
from server import waiting_for_new_request, Max_sending_window_size
import os
import time
# the implementation of the events are inside the states, "event" object for interrupted events
os.chdir("C:\\Files\\Engineering\\colllege\\term 8\\Networks\\projects\\reliable_UDP\\Data_files")  # change directory


if Max_sending_window_size > 1:
    print("Stop and wait protocol can't handle more than 1 datagram window size")
elif Max_sending_window_size == 1:
    file, address = waiting_for_new_request()
    send_file = open(file, "rb")
    server = NewConnection('server')

    while 1:
        server.on_event((send_file, address))



