import os

from server import server_port, Max_sending_window_size
import utility
import socket
from Protocols.settings import write_log, file_path

base: int = 0
next_Seq_number = 0
N = Max_sending_window_size

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', server_port))


print("Waiting for client...\n")
log_file = open(file_path, "a")
write_log("Waiting for client...\n")
log_file.close()

file, client_address = sock.recvfrom(100)

print("Requested file", file, "from", client_address)
log_file = open(file_path, "a")
write_log(str(("Requested file", file, "from", client_address,"\n")))
log_file.close()

send_file = open(file, "rb")
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server.bind(('', 12345))

buffer = []
EOF = 0
Buffer_dict = {}
Buffer_list = []


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
        text = send_file.read(512)
        if text.decode() == "":  # EOF
            print("EOF")
            EOF = 1
            log_file = open(file_path, "a")
            write_log("End file transmitted file")
            log_file.close()
            break
        else:
            data_packet = utility.make_data_packet(0, text.__len__(), next_Seq_number, text)
            socket_server.sendto(data_packet, client_address)
            log_file = open(file_path, "a")
            write_log("".join(("send packet with sequence number", next_Seq_number.__str__(), "\n")))
            log_file.close()
            new_dict = {"seq_number": next_Seq_number, 'packet': data_packet, 'status': 'unacked'}
            Buffer_list.append(new_dict)
            log_file = open(file_path, "a")
            write_log("".join(("buffer now includes:", str(next_Seq_number), "\n")))
            log_file.close()
            next_Seq_number = next_Seq_number + 1

    received_packet, client_address = socket_server.recvfrom(8)

    if received_packet != "":  # if ACK
        check_sum, ack_seq_number = utility.extract_data(received_packet)  # extract the ACK sequence number
        mark_as_packed(int(ack_seq_number))
        print("acknowledge sequence number=", ack_seq_number, Buffer_list[ack_seq_number]["status"])
        if ack_seq_number == base:
            base = find_min_unacked()


print("end")
