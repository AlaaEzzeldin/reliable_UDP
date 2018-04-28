from FSM.connection import NewConnection
from server import waiting_for_new_request

# the implementation of the events are inside the states, "event" object for interrupted events
file, address = waiting_for_new_request()
send_file = open(file)
server = NewConnection('server')
server.on_event((send_file, address))
server.on_event((send_file, address))
server.on_event((send_file, address))
server.on_event((send_file, address))
server.on_event((send_file, address))
server.on_event((send_file, address))
server.on_event((send_file, address))
server.on_event((send_file, address))
server.on_event((send_file, address))
server.on_event((send_file, address))
server.on_event((send_file, address))
send_file.close()