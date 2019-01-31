from socket import *

class Player:
    ready = False

    def __init__(self, name, is_human):
        self.name = name
        self.is_human = is_human
        print('Player', self.name, 'say hi!')

    def play(self):
        pass

    def is_ready(self):
        return self.ready 
