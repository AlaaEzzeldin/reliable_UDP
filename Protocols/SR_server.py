import os

from server import Max_sending_window_size, waiting_for_new_request
import utility
import socket
from Protocols.settings import write_log, file_path, log_file
import time

# initialize some parameters
base: int = 0
next_Seq_number = 0
N = Max_sending_window_size
Buffer_list = []
EOF: bool = False
# waiting for new request
requested_file, client_address = waiting_for_new_request()
send_file = open(requested_file, "rb")
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create new socket for this client
socket_server.bind(('', 12345))


def check_window_is_Acked():
    for i in range(len(Buffer_list)):
        if Buffer_list[i]["status"] == "unacked":
            return False
        else:
            return True


def find_min_unacked():
    for i in range(len(Buffer_list)):
        if Buffer_list[i]["status"] == "unacked":  # if there exist unacked datagrams in the window
            smallest_unacked = Buffer_list[i]["seq_number"]
        else:  # all datagrams in the window are acked
            smallest_unacked = next_Seq_number
        # print("smallest=", smallest_unacked)
        return int(smallest_unacked)


def mark_as_packed(seq_number):
    for i in range(len(Buffer_list)):
        if seq_number == Buffer_list[i]["seq_number"]:
            Buffer_list[i]["status"] = "acked"


while 1:
    if next_Seq_number < (int(base) + N):  # the next seq number packet is within the window range
        text = send_file.read(500)
        if text == b'':  # EOF
            EOF = True
            write_log("Server:   End file transmitted file")
            last_seq_number = next_Seq_number - 1
        else:
            data_packet = utility.make_data_packet(0, text.__len__(), next_Seq_number, text)
            socket_server.sendto(data_packet, client_address)
            if next_Seq_number == 0:
                start_time = time.clock()
            write_log("".join(("Server:   send packet with sequence number", str(next_Seq_number))))
            new_dict = {"seq_number": next_Seq_number, 'packet': data_packet, 'status': 'unacked'}
            Buffer_list.append(new_dict)
            write_log("".join(("Server:   buffer now includes:", str(next_Seq_number))))
            next_Seq_number = next_Seq_number + 1

    if EOF & check_window_is_Acked():
        log_file.close()
        end_time = time.clock()
        exec_time = end_time - start_time
        write_log("".join(("Execution time= ", str(exec_time), "secs")))
        exit(0)
    received_packet, client_address = socket_server.recvfrom(8)

    if received_packet != "":  # if ACK
        check_sum, ack_seq_number = utility.extract_data(received_packet)  # extract the ACK sequence number
        mark_as_packed(int(ack_seq_number))
        write_log("".join(("Server:   packet with sequence number= ", str(ack_seq_number), "  ",
                           Buffer_list[ack_seq_number]["status"])))
        if ack_seq_number == base:
            base = find_min_unacked()


