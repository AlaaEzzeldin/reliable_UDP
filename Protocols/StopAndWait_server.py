from FSM.connection import NewConnection
from server import waiting_for_new_request

# the implementation of the events are inside the states, "event" object for interrupted events
file, address = waiting_for_new_request()
server = NewConnection('server')
server.on_event((file, address))
server.on_event((file, address))
server.on_event((file, address))
server.on_event((file, address))