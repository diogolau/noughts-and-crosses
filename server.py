from controller import Controller
import socket
import sys
import selectors
import types




def main():
    initiate_server(sys.argv[1], sys.argv[2])

def initiate_server(host, port):
    LIMIT_CONNECTIONS = 2
    SERVER_STATE = "000000000000000000"
    SYMBOLS = [0, 1]
    PLAYER_IDENTIFIER = {}

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
                    con.type_handler(key, mask, sel)
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        sel.close()
        listening_socket.close()

if __name__ == "__main__":
    main()
