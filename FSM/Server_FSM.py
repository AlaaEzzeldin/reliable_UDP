# requested file
import socket

from FSM.simple_device import NewConnection


def new_file_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_ip = socket.gethostname()  # Server IP
    serverPort = 12345
    sock.bind((server_ip, serverPort))
    # while True:
    print("Waiting for client...")
    requested_file, client_address = sock.recvfrom(1024)
    print("Received Messages:", requested_file, "from", client_address)

new_file_request()
server = NewConnection('server')
server.on_event('rdt_send_data')
server.on_event('ack0')
server.on_event('rdt_send_data')
