import struct
from Protocols.settings import protocol_type
import time

# set packets formats
data_packet_format = "!III500s"  # I for unsigned int, S for string
ack_packet_format = "!II"


# print(struct.calcsize(data_packet_format))  # check the size of Data packet (512 bytes)
# print(struct.calcsize(ack_packet_format))


def make_data_packet(check_sum, length, seq_number, data):
    global data_packet
    if protocol_type == "sr":
        data_packet = struct.pack(data_packet_format, check_sum, length, seq_number, data)
    return data_packet


def make_ack_packet(check_sum, seq_number):
    global ack_packet
    if protocol_type == "sr":
        ack_packet = struct.pack(ack_packet_format, check_sum, seq_number)
    return ack_packet


def extract_data(packet):
    if len(packet) == 512:  # data packet
        check_sum, length, seq_number, data = struct.unpack(data_packet_format, packet)
        return check_sum, length, seq_number, data
    elif len(packet) == 8:  # ACK packet
        check_sum, seq_number = struct.unpack(ack_packet_format, packet)
        return check_sum, seq_number


def expected_seqNumber(expected_seq, received_seq):
    if expected_seq == received_seq:
        return 1
    else:
        return 0


def end_of_file(start_time):
        print("End OF File")
        end_time = time.time()
        exec_time = end_time - start_time
        print("Execution time= ", str(exec_time), "secs")
        exit(0)



class Packet(object):
    "Stores name and place pairs"

    def __init__(self, seq_number, data_packet, status):
        self.seq_number = seq_number
        self.data_packet = data_packet
        self.status = status


Buffer_list = []