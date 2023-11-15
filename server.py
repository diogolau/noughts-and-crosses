import socket
import sys
import selectors
from controller import Controller
from tictactoe.multiplayer import TicTacToe


def main():
    game = TicTacToe()
    initiate_server(sys.argv[1], sys.argv[2], game)

def initiate_server(host, port, game):
    sel = selectors.DefaultSelector()

    HOST, PORT = host, int(port)

    listening_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    listening_socket.bind((HOST, PORT))
    listening_socket.listen()
    print(f"Listening on {HOST, PORT}")
    listening_socket.setblocking(False)

    sel.register(listening_socket, selectors.EVENT_READ, data=None)

    con = Controller()
    
    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:                    
                    con.accept_wrapper(key.fileobj, events, sel)
                else:
                    # con.service_connection(key, mask, sel)
                    con.message_handler(key, mask, sel, events, game)
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        sel.close()
        listening_socket.close()

if __name__ == "__main__":
    main()
