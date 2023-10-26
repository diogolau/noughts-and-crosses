import socket
import sys
import selectors
import types
import json


def main():
    initiate_server(sys.argv[1], sys.argv[2])

def initiate_server(host, port):
    LIMIT_CONNECTIONS = 2
    SERVER_STATE = "000000000000000000"
    SYMBOLS = ["X", "O"]
    PLAYER_IDENTIFIER = {}

    sel = selectors.DefaultSelector()

    HOST, PORT = host, int(port)

    listening_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    listening_socket.bind((HOST, PORT))
    listening_socket.listen()
    print(f"Listening on {HOST, PORT}")
    listening_socket.setblocking(False)

    sel.register(listening_socket, selectors.EVENT_READ, data=None)
    
    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    def accept_wrapper(sock, events):
                        if len(events) < LIMIT_CONNECTIONS + 1:
                            conn, addr = sock.accept()
                            PLAYER_IDENTIFIER[conn.fileno()] = SYMBOLS[0]
                            SYMBOLS.pop(0)
                            print(f"Accepted connection from {addr}")
                            conn.setblocking(False)
                            data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
                            events = selectors.EVENT_READ | selectors.EVENT_WRITE
                            sel.register(conn, events, data)
                        else:
                            conn, addr = sock.accept()
                            print(f"Reject connection from {addr}")
                            conn.close()
                    
                    accept_wrapper(key.fileobj, events)
                else:
                    def service_connection(key, mask):
                        sock = key.fileobj
                        data = key.data
                        if mask & selectors.EVENT_READ:
                            recv_data = sock.recv(1024)
                            if recv_data:
                                data.outb += recv_data
                            else:
                                print(f"Closing connection to {data.addr}")
                                SYMBOLS.append(PLAYER_IDENTIFIER[sock.fileno()])
                                del(PLAYER_IDENTIFIER[sock.fileno()])
                                sel.unregister(sock)
                                sock.close()
                        if mask & selectors.EVENT_WRITE:
                            if data.outb:
                                print(f"Echoing {data.outb!r} to {data.addr}")
                                str_dict = json.loads(data.outb)
                                print(str_dict["data"])
                                if "type" in str_dict.keys():
                                    sock.send(str_dict["data"].encode())
                                data.outb = b""

                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        sel.close()
        listening_socket.close()

if __name__ == "__main__":
    main()
