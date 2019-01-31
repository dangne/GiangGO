from socket import *

class Player:
    name = ''
    ready = False

    def __init__(self, name):
        self.name = name
        print('Player', self.name, 'say hi!')

    def play(self):
        pass

    def is_ready(self):
        return self.ready 
