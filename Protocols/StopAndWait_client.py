from client import sliding_window_size, request_file_from_server
from FSM.connection import NewConnection


if sliding_window_size > 1:
    print("Stop and wait protocol can't handle more than 1 datagram window size")

elif sliding_window_size == 1:

    sock = request_file_from_server()
    cl = NewConnection('client')
    while 1:
        cl.on_event(sock)

