import socket

import utility
import time
import os
from FSM.state import State
from simulation_helper import get_decision

os.chdir("C:\\Files\\Engineering\\colllege\\term 8\\Networks\\projects\\reliable_UDP")  # change directory

start_time = time.time()
number_of_packet = 0
buffer_one_packet = {}


class Waiting_for_call_0(State):
    def on_event(self, event):
        if 1:
            send_file, address, list_of_dropped, send_socket = event
            global number_of_packet, start_time, buffer_one_packet
            text = send_file.read(500)
            if text == b'':  # test if the file ends
                utility.end_of_file(start_time)
                send_file.close()
            else:
                data_packet = utility.make_data_packet(utility.get_checksum_server(str(text)), 0, 0, text)
                buffer_one_packet = data_packet
                if not get_decision(list_of_dropped, number_of_packet):  # drop or not
                    print("Packet loss   ", number_of_packet)
                    number_of_packet += 1
                    send_socket.settimeout(2)
                    pass
                else:
                    send_socket.sendto(data_packet, address)  # extracting client data when he make the request
                    send_socket.settimeout(2)
                    number_of_packet += 1
        return Waiting_for_ACK_0()


class Waiting_for_ACK_0(State):
    def on_event(self, event):
        send_file, address, list_of_dropped, send_socket = event
        try:
            received_packet, client_address = send_socket.recvfrom(8)
            check_sum, seq_number = utility.extract_data(received_packet)  # extract the ACK sequence number
            if utility.expected_seqNumber(0, seq_number):
                return Waiting_for_call_1()
        except socket.timeout:
            print("time out")
            print("retransmission")
            send_socket.sendto(buffer_one_packet, address)
        return Waiting_for_ACK_0()


class Waiting_for_call_1(State):
    def on_event(self, event):
        send_file, address, list_of_dropped ,send_socket= event
        global number_of_packet, start_time, buffer_one_packet
        text = send_file.read(500)
        if text == b'':  # test if the file ends
            send_file.close()
            utility.end_of_file(start_time)
        else:
            data_packet = utility.make_data_packet(utility.get_checksum_server(str(text)), 0, 1, text)
            buffer_one_packet = data_packet
            if not get_decision(list_of_dropped, number_of_packet):  # drop or not
                print("Packet loss   ", number_of_packet)
                number_of_packet += 1
                send_socket.settimeout(2)
                pass
            else:
                send_socket.sendto(data_packet, address)  # extracting client data when he make the request
                send_socket.settimeout(2)
                number_of_packet += 1
        return Waiting_for_ACK_1()



class Waiting_for_ACK_1(State):
    def on_event(self, event):
        send_file, address, list_of_dropped, send_socket = event
        try:
            received_packet, client_address =send_socket.recvfrom(8)
            check_sum, seq_number = utility.extract_data(received_packet)  # extract the ACK sequence number
            if utility.expected_seqNumber(1, seq_number):
                return Waiting_for_call_0()
        except socket.timeout:
            print("time out")
            print("retransmission")
            send_socket.sendto(buffer_one_packet, address)
        return Waiting_for_ACK_1()
