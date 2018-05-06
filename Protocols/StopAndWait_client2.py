from client import sliding_window_size, request_file_from_server
from FSM.connection import NewConnection
import socket



if sliding_window_size > 1:
    print("Stop and wait protocol can't handle more than 1 datagram window size")

elif sliding_window_size == 1:

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 34344))
        sock.settimeout(10)
        request_file = "C:\\Files\\Engineering\\colllege\\term 8\\Networks\\projects\\reliable_UDP\\Data_files\\client_received_file.m4a"
        sock.sendto(request_file.encode(), ('127.0.0.1',6000))  # request new file
        sock.settimeout(None)
        cl = NewConnection('client')
        while 1:
            cl.on_event(sock)

