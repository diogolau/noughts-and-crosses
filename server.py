import socket
import sys
import selectors
import types
import json

def main():
    LIMIT_CONNECTIONS = 2

    sel = selectors.DefaultSelector()

    HOST, PORT = sys.argv[1], int(sys.argv[2])

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
                        if len(events) < LIMIT_CONNECTIONS:
                            conn, addr = sock.accept()
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
