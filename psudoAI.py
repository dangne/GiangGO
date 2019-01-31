import socket

class PsudoAI:
    def __init__(self):
        self.setup_networking()

    def setup_networking(self):
        # Networking configuration 
        host = '127.0.0.1'
        port = 5000

        # Create socket object
        self.s = socket.socket()
        self.s.connect((host, port))

    def get_game_status(self):
        self.game_over = s.recv(1024)

    def play(self):
        self.move = input("What is your move? ")
        self.s.sendall(self.move.encode('utf-8'))

    def destroy(self):
        self.s.close()

# Testing module
if __name__ == "__main__":
    agent = PsudoAI()
    while 1:
        agent.play()
        if agent.move == 'q':
            break
    agent.destroy()


