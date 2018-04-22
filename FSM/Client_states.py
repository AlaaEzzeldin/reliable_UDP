from FSM.state import State


class Waiting_for_callFrom_below(State):

    def on_event(self, event):
        if event == 'rdt_send_data':
            return Waiting_for_callFrom_below()
        return self
