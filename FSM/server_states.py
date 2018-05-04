# server_states.py
import server
import socket
import utility
import time
import os
from FSM.state import State


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
os.chdir("C:\\Files\\Engineering\\colllege\\term 8\\Networks\\projects\\reliable_UDP")  # change directory


start_time = time.time()
class Waiting_for_call_0(State):
    def on_event(self, event):
        if 1:
            send_file, address = event
            global sock
            text = send_file.read(500)
            if text== b'':  # test if the file ends
                print("End OF File")
                send_file.close()
                end_time = time.time()
                exec_time = end_time - start_time
                print("Execution time= ", str(exec_time), "secs")
                exit(0)
            data_packet = utility.make_data_packet(0, 0, 0, text)
            sock.sendto(data_packet, address)  # extracting client data when he make the request
            return Waiting_for_ACK_0()
        return self


class Waiting_for_ACK_0(State):
    def on_event(self, event): # if event == 'ack0':
        global sock
        received_packet, client_address = sock.recvfrom(8)
        check_sum, seq_number = utility.extract_data(received_packet)  # extract the ACK sequence number
        if utility.expected_seqNumber(0, seq_number):
            return Waiting_for_call_1()
        return self


class Waiting_for_call_1(State):
    def on_event(self, event):
        send_file, address = event
        global send_time, sock
        text = send_file.read(500)
        if text ==b'':  # test if the file ends
            print("End OF File")
            end_time = time.time()
            exec_time = end_time - start_time
            print("Execution time= ", str(exec_time), "secs")
            exit(0)
        data_packet = utility.make_data_packet(0, 0, 1, text)
        sock.sendto(data_packet, address)  # extracting client data when he make the request
        send_time = time.time()
        return Waiting_for_ACK_1()
    # return self


class Waiting_for_ACK_1(State):
    def on_event(self, event):
        global sock
        received_packet, client_address = sock.recvfrom(8)
        check_sum, seq_number = utility.extract_data(received_packet)  # extract the ACK sequence number
        if utility.expected_seqNumber(1, seq_number):
            return Waiting_for_call_0()
        return self