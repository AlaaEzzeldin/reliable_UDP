from FSM.state import State
from client import client_received_file, client_ip, client_port
import utility


class Waiting_for_0_From_below(State):

    def on_event(self, event):
        try:
            sock = event
            received_packet, server_address = sock.recvfrom(512)
            check_sum, length, seq_number, data = utility.extract_data(received_packet)  # extract the data

            # if correct & expected sequence number
            if (check_sum == utility.get_checksum_client(str(data)) ^ 0xffff) & utility.expected_seqNumber(0, seq_number):

                # deliver the data to the upper layer
                received_file = open(client_received_file, "ab")
                received_file.write(data)
                print(data)
                received_file.close()

                # send ACK packet to the server
                ack_packet = utility.make_ack_packet(0, 0)
                sock.sendto(ack_packet, server_address)
                return Waiting_for_1_From_below()

            else:
                print("retransimission")
                print("here to put ")
                ack_packet = utility.make_ack_packet(0, 1)  # create ACK packet
                sock.sendto(ack_packet, server_address)  # send ACK packet to the server
        except :
            print("delay in receiving")
        return self


class Waiting_for_1_From_below(State):

    def on_event(self, event):
        try:
            sock = event
            received_packet, server_address = sock.recvfrom(512)
            check_sum, length, seq_number, data = utility.extract_data(received_packet)  # extract the data
            print(len(data))
            print(check_sum)
            print(utility.get_checksum_client(str(data)) ^ 0xffff)

            # if correct & expected sequence number
            if (check_sum == utility.get_checksum_client(str(data))):
                # deliver the data to the upper layer
                received_file = open(client_received_file, "ab")
                received_file.write(data)
                print(data)
                received_file.close()

                # send ACK packet to the server
                ack_packet = utility.make_ack_packet(0, 1)
                sock.sendto(ack_packet, server_address)
                return Waiting_for_0_From_below()

            else:
                print("retransimission")
                print("here to put ", (check_sum == utility.get_checksum_client(str(data)) ^ 0xffff))
                ack_packet = utility.make_ack_packet(0, 0)  # create ACK packet
                sock.sendto(ack_packet, server_address)  # send ACK packet to the server
        except:
            print("delay in receiving")
        return self