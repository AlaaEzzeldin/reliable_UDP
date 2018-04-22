# server_states.py
from FSM.state import State


# Start of our states
class Waiting_for_call(State):

    def on_event(self, event):
        if event == 'rdt_send_data':
            return Waiting_for_ACK0()
        return self


class Waiting_for_ACK0(State):
    def on_event(self, event):
        if event == 'ack0':
            return Waiting_for_call()

        return self
# End of our states.
