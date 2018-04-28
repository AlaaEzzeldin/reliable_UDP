# connection.py
from FSM.Client_states import Waiting_for_0_From_below
from FSM.server_states import Waiting_for_call_0


class NewConnection(object):
    def __init__(self, device_type):
        # Start with a default state.
        if device_type == 'server':
            self.state = Waiting_for_call_0()
        elif device_type == 'client':
            self.state = Waiting_for_0_From_below()

    def on_event(self, event):
        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event)
