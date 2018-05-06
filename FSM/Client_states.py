from FSM.state import State
from client import  client_ip, client_port
import utility

client_received_file = "C:\\Files\\Engineering\\colllege\\term 8\\Networks\\projects\\reliable_UDP\\Data_files\\client_received_file"
received_file = open(client_received_file, "ab")


class Waiting_for_0_From_below(State):


    def on_event(self, event):
        try:
            sock = event
            received_packet, server_address = sock.recvfrom(512)
            check_sum, length, seq_number, data = utility.extract_data(received_packet)  # extract the data
            if data  == b'11111eof1111':
                received_file.close()
                print("all the file has been received ^___^")
                exit(0)
            # if correct & expected sequence number
            if utility.expected_seqNumber(0, seq_number):

                try:
                    received_file.write(data)
                    # send ACK packet to the server
                    ack_packet = utility.make_ack_packet(0, 0)
                    sock.sendto(ack_packet, server_address)
                    return Waiting_for_1_From_below()
                except IOError:
                    print("Error: can't find file or write data")

            else:
                print("retransimission")
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
            if data  == b'11111eof1111':
                received_file.close()
                print("all the file has been received ^___^")
                exit(0)
            # if correct & expected sequence number & check_sum == (utility.get_checksum_client(str(data)) ^ 0xffff):
            if utility.expected_seqNumber(1, seq_number):
                # deliver the data to the upper layer
                try:
                    received_file.write(data)
                    # send ACK packet to the server
                    ack_packet = utility.make_ack_packet(0, 1)
                    sock.sendto(ack_packet, server_address)
                    return Waiting_for_0_From_below()

                except IOError:
                    print("Error: can't find file or write data")

            else:
                print("retransimission")
                ack_packet = utility.make_ack_packet(0, 0)  # create ACK packet
                sock.sendto(ack_packet, server_address)  # send ACK packet to the server
        except:
            print("delay in receiving")
        return self