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
        self.game_status = self.s.recv(1024)

    def play(self):
        self.move = input("What is your move? ")
        self.s.sendall(self.move.encode('utf-8'))

    def destroy(self):
        self.s.close()

# For debugging purpose
def print_game_status(game_status):
    cnt = 0
    for i in agent.game_status[1:len(agent.game_status)]:
        if cnt == 9:
            cnt = 0
            print()
        print(int(i),end = ' ') 
        cnt += 1
    print('\n')

if __name__ == "__main__":
    agent = PsudoAI()
    while 1:
        agent.get_game_status()
        print_game_status(agent.game_status)
        agent.play()
        if agent.move == 'q':
            break
    agent.destroy()
