import socket
import threading
import time
from concurrent.futures import thread

import utility
from Protocols.settings import write_log
from server import Max_sending_window_size, waiting_for_new_request, loss_Probability, random_SeedValue
from simulation_helper import get_must_dropped_packets, get_decision, print_dropped_seq

max_window_size = Max_sending_window_size
EOF: bool = False
chunk_size = 500
Lock_packet_sending = threading.Lock()
base = 0


class thread_sender(threading.Thread):

    def __init__(self, requested_file, socket_server, list_of_dropped, max_window_size):
        threading.Thread.__init__(self)
        self.socket_server = socket_server
        self.max_window_size = max_window_size
        self.requested_file = requested_file
        self.list_of_dropped_And_corrupted = list_of_dropped
        self.start()

    def run(self):
        global base, Lock_packet_sending
        curr_seq_number = 0
        EOF = False
        while not EOF:
            Lock_packet_sending.acquire()
            while curr_seq_number < (
                    int(base) + max_window_size):  # the next seq number packet is within the window range
                try:
                    text = self.requested_file.read(500)
                except:
                    IOError
                    print("can't read file\n")
                if text == b'':  # EOF
                    EOF = True
                    write_log("Server:   End file transmitted file")
                    curr_seq_number -= 1
                    break
                else:
                    if get_decision(self.list_of_dropped_And_corrupted,
                                        curr_seq_number):  # packet lost or corrupted
                        data_packet = utility.make_data_packet(0, text.__len__(), curr_seq_number, text)
                        self.socket_server.sendto(data_packet, client_address)
                        # write_log("".join(("Server:   buffer now includes:", str(curr_seq_number))))
                        curr_seq_number += 1
                    else:
                        curr_seq_number += 1
                        print("dropped", curr_seq_number)
                    write_log("".join(("Server:   send packet with sequence number", str(curr_seq_number))))
                    new_dict = {"seq_number": curr_seq_number, 'packet': data_packet, 'status': 'unacked',
                                    "send_time": time.time()}
                    utility.Buffer_list.append(new_dict)

            Lock_packet_sending.release()

            if EOF:
                break
        data_packet = b'11111eof1111'  # pattern to detect the end of file
        self.socket_server.sendto(data_packet, client_address)


class ack_receiver(threading.Thread):
    def __init__(self, socket_server, list_of_dropped, max_window_size):
        threading.Thread.__init__(self)
        threading.Thread.__init__(self)
        self.socket_server = socket_server
        self.max_window_size = max_window_size
        self.dropped_packets = list_of_dropped
        self.start()

   # def retransimission(self, list, curr_seq_number):



    def run(self):
        global base, Lock_packet_sending
        current_seq_number = 0
        while base + self.max_window_size > current_seq_number:
            received_packet, client_address = self.socket_server.recvfrom(8)
            if received_packet != b'':  # if ACK
                print(received_packet)
                check_sum, ack_seq_number = utility.extract_data(received_packet)  # extract the ACK sequence number
                print("seq=", ack_seq_number)
                utility.mark_as_packed(ack_seq_number)  # mark this packet as acked
                write_log("".join(("Server:   packet with sequence number= ", str(ack_seq_number), "  ",
                                   utility.Buffer_list[ack_seq_number]["status"])))
                Lock_packet_sending.acquire()
                base = utility.find_min_unacked(ack_seq_number)
                '''
                                buffer = utility.find_if_un_ack(base, max_window_size)
                print(buffer, base, ack_seq_number)
                for i in range(len(buffer)):
                    data_packet = buffer[i]['packet']
                    Lock_packet_sending.acquire()
                    self.socket_server.sendto(data_packet, client_address)
                    write_log("".join(("Server:   retransmit packet with sequence number", str(buffer[i]['seq_number']))))
                    buffer[i]['status'] = "acked"
                    # write_log("".join(("Server:   buffer now includes:", str(curr_seq_number))))
                    Lock_packet_sending.release()
                '''


                Lock_packet_sending.release()



def serve_new_client(requested_file):
    send_file = open(requested_file, "rb")
    # establish a simulation environment
    list_of_dropped = get_must_dropped_packets(requested_file, loss_Probability, chunk_size, random_SeedValue)
    print_dropped_seq(list_of_dropped)

    # create new socket to send the data
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create new socket for this client
    socket_server.bind(('', 12345))

    start_time = time.time()
    sender_thread = thread_sender(send_file, socket_server, list_of_dropped, max_window_size)
    thread_ack_receiver = ack_receiver(socket_server, list_of_dropped, max_window_size)

    sender_thread.join()
    thread_ack_receiver.join()
    end_time = time.time()
    exec_time = end_time - start_time
    print(exec_time)


while 1:
    # waiting for new request
    requested_file, client_address = waiting_for_new_request()
    serve_new_client(requested_file)

    thread.start_new_thread(serve_new_client, requested_file)
    thread.join()


