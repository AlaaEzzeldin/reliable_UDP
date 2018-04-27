# simple_device.py
from FSM.Client_states import Waiting_for_callFrom_below
from FSM.server_states import Waiting_for_call


class NewConnection(object):
    def __init__(self, device_type):
        """

        :rtype: object
        """
        # Start with a default state.
        if device_type == 'server':
            self.state = Waiting_for_call()
        elif device_type == 'client':
            self.state = Waiting_for_callFrom_below()

    def on_event(self, event):
        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event)
