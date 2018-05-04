from server import server_port, Max_sending_window_size
import utility
import socket
from Protocols.settings import write_log, file_path

base = 0
next_Seq_number = 0
N = Max_sending_window_size

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', server_port))
print("Waiting for client...")
file, client_address = sock.recvfrom(100)
print("Received Messages:", file, "from", client_address)
send_file = open(file, "rb")
buffer = []
EOF = 0

socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server.bind(('', 12345))
while 1:
    if next_Seq_number < (base+N):  # the next seq number packet is within the window range
        text = send_file.read(512)
        if utility.end_of_file(text):  # EOF
            print("EOF")
            EOF = 1
            log_file = open(file_path, "")
            write_log("End file transmitted file")
            log_file.close()

            break
        else:
            data_packet = utility.make_data_packet(0, text.__len__(), next_Seq_number, text)
            socket_server.sendto(data_packet, client_address)
            log_file = open(file_path, "a")
            write_log("".join(("send packet with sequence number", next_Seq_number.__str__(), "\n")))
            log_file.close()
            buffer.insert(next_Seq_number, data_packet)
            log_file = open(file_path, "a")
            write_log("".join(("buffer now includes:", str(next_Seq_number), "\n")))
            log_file.close()
            next_Seq_number = next_Seq_number + 1

    received_packet, client_address = socket_server.recvfrom(8)

    if received_packet != "":  # if ACK
        check_sum, ack_seq_number = utility.extract_data(received_packet)  # extract the ACK sequence number
        print("acknowledge sequence number=", ack_seq_number)
        log_file = open(file_path, "a")
        write_log("".join(("acknowledge sequence number=", str(ack_seq_number))))
        log_file.close()
        if ack_seq_number == base:
           print("base=seq")

print("end")






