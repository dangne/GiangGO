from Constants import *
import socket

class PseudoAI:
    def __init__(self, port):
        self.setup_networking(port)

    def setup_networking(self, port): # Networking configuration 
        self.host = '127.0.0.1' 
        self.port = 5000 + port

        print(self.host, self.port)

        # Create socket object
        self.s = socket.socket()
        self.s.connect((self.host, self.port))

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
    agent = PseudoAI(PLAYER_2)
    #agent2 = PseudoAI(PLAYER_2)
    while 1:
        # Turn 1
        agent.get_game_status()
        print_game_status(agent.game_status)
        agent.play()
        if agent.move == 'q':
            break

        # Turn 2
        #agent2.get_game_status()
        #print_game_status(agent2.game_status)
        #agent2.play()
        #if agent2.move == 'q':
        #    break

    agent.destroy()
    #agent2.destroy()
