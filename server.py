import socket
import sys
import selectors
from controller import Controller
from tictactoe.multiplayer import TicTacToe


def main():
    game = TicTacToe()
    initiate_server(sys.argv[1], sys.argv[2], game)

def initiate_server(host, port, game):
    sel = selectors.DefaultSelector() # Instantiate a selector that will be responsible to store all sockets

    HOST, PORT = host, int(port)

    # Configures the server's socket that will listen to new connections
    listening_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    listening_socket.bind((HOST, PORT))
    listening_socket.listen()
    listening_socket.setblocking(False)

    sel.register(listening_socket, selectors.EVENT_READ, data=None) # Register the server's socket on selector

    con = Controller() # The controller will handle almost all of the server logic
    
    try:
        while True:
            # Looks for new events for the sockets registered on selector
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:                    
                    # Tries to create a new connection
                    con.accept_wrapper(key.fileobj, events, sel)
                else:
                    # Gets the message sent by client's socket and process it
                    con.message_handler(key, mask, sel, events, game)
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        sel.close()
        listening_socket.close()

if __name__ == "__main__":
    main()
