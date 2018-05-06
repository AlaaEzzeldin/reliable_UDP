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


def get_checksum_server(data):
    i = len(data)
    # Handle the case where the length is odd
    if i & 1:
        i -= 1
        sum = ord(data[i])
    else:
        sum = 0
    # Iterate through chars two by two and sum their byte values
    while i > 0:
        i -= 2
        sum += (ord(data[i + 1]) << 8) + ord(data[i])
    # Wrap overflow around
    sum = (sum >> 16) + (sum & 0xffff)
    result = (~ sum) & 0xffff  # One's complement
    return result


def get_checksum_client(data):
    i = len(data)
    # Handle the case where the length is odd
    if i & 1:
        i -= 1
        sum = ord(data[i])
    else:
        sum = 0
    # Iterate through chars two by two and sum their byte values
    while i > 0:
        i -= 2
        sum += (ord(data[i + 1]) << 8) + ord(data[i])
    # Wrap overflow around
    sum = (sum >> 16) + (sum & 0xffff)
    return sum


def check_window_is_Acked():
    for i in range(len(Buffer_list)):
        if Buffer_list[i]["status"] == "unacked":
            return False
        else:
            return True
    return False


def find_min_unacked(Seq_number):
    for i in range(len(Buffer_list)):
        if Buffer_list[i]["status"] == "unacked":  # if there exist unacked datagrams in the window
            smallest_unacked = Buffer_list[i]["seq_number"]
        else:  # all datagrams in the window are acked
            smallest_unacked = Seq_number

        # print("smallest=", smallest_unacked)
        return int(smallest_unacked)


def find_if_un_ack(Seq_number, n):
    i = Seq_number
    unacked = []
    print(i,len(Buffer_list))
    while i < i + n & len(Buffer_list[i])!= 0:
        print((Buffer_list[i]))
        if Buffer_list[i]["status"] == "unacked":  # if there exist unacked datagrams in the window
            unacked[i] = Buffer_list[i]
            i+=1

    return unacked


def mark_as_packed(seq_number):
    for i in range(len(Buffer_list)):
        if seq_number == Buffer_list[i]["seq_number"]:
            Buffer_list[i]["status"] = "acked"


Buffer_list = []
unacked = []
