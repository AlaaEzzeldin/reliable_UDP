from FSM.connection import NewConnection
from server import waiting_for_new_request, Max_sending_window_size

# the implementation of the events are inside the states, "event" object for interrupted events

if Max_sending_window_size > 1:
    print("Stop and wait protocol can't handle more than 1 datagram window size")
elif Max_sending_window_size == 1:
    file, address = waiting_for_new_request()
    send_file = open(file, "rb")
    server = NewConnection('server')
    while 1:
        server.on_event((send_file, address))
    send_file.close()
