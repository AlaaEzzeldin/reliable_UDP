# state.py


class State(object):

    def __init__(self):
        print('Processing current state:', str(self))

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__
