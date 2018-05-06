from FSM.state import State
from client import client_received_file, client_ip, client_port
import utility


class Waiting_for_0_From_below(State):

    def on_event(self, event):
        # if event == 0:
        try:
            sock = event
            received_packet, server_address = sock.recvfrom(512)
            check_sum, length, seq_number, data = utility.extract_data(received_packet)  # extract the data
            received_file = open(client_received_file, "ab")
            received_file.write(data)  # deliver the data to the upper layer
            received_file.close()
            ack_packet = utility.make_ack_packet(0, 0)  # create ACK packet
            sock.sendto(ack_packet, server_address)  # sen ACK packet to the server
            if utility.expected_seqNumber(0, seq_number):
                return Waiting_for_1_From_below()
            else:
                ack_packet = utility.make_ack_packet(0, 1)  # create ACK packe
                sock.sendto(ack_packet, server_address)  # send ACK packet to the server
        except :
            print("delay in receiving")
        return self


class Waiting_for_1_From_below(State):

    def on_event(self, event):
        # if event == 1:
        try:
            sock = event
            received_packet, server_address = sock.recvfrom(512)
            check_sum, length, seq_number, data = utility.extract_data(received_packet)  # extract the data
            received_file = open(client_received_file, "ab")
            received_file.write(data)  # deliver the data to the upper layer
            received_file.close()
            ack_packet = utility.make_ack_packet(0, 1)  # create ACK packet
            sock.sendto(ack_packet, server_address)  # sen ACK packet to the server
            if utility.expected_seqNumber(1, seq_number):
                return Waiting_for_0_From_below()
            else:
                ack_packet = utility.make_ack_packet(0, 0)  # create ACK packe
                sock.sendto(ack_packet, server_address)  # send ACK packet to the server
        except:
            print("delay in receiving")
        return self
