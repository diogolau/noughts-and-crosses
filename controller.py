import socket
import selectors
import types
import json
from utils.json_utils import binary_to_json, json_to_binary

class Controller:
    connection_limit = 2
    symbols = [0, 1]

    def __init__(self):
        self.server_state = "000000000000000000"
        self.player_identifier = {}

    def accept_wrapper(self, sock, events, selector):
        if len(events) < Controller.connection_limit + 1:
            conn, addr = sock.accept()
            self.player_identifier[conn.fileno()] = Controller.symbols[0]
            Controller.symbols.pop(0)
            print(f"Accepted connection from {addr}")
            conn.setblocking(False)
            data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            selector.register(conn, events, data)
            token_message = {
                "type": 0,
                "token": self.player_identifier[conn.fileno()]
            }
            b_message = json_to_binary(token_message)
            conn.send(b_message)
        else:
            conn, addr = sock.accept()
            error_message = {
                "type": -1
            }
            b_message = json_to_binary(error_message)
            conn.send(b_message)
            print(f"Reject connection from {addr}")
            conn.close()

    def service_connection(self, key, mask, selector):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                data.outb += recv_data
            else:
                print(f"Closing connection to {data.addr}")
                Controller.symbols.append(self.player_identifier[sock.fileno()])
                del(self.player_identifier[sock.fileno()])
                selector.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Echoing {data.outb!r} to {data.addr}")
                str_dict = json.loads(data.outb)
                print(str_dict["data"])
                if str_dict:
                    sock.send(str_dict["data"].encode())
                data.outb = b""

    def type_handler(self, key, mask, selector, events):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                # From now on, add cases for each type that call another method.
                # Remember to pass the socket and data for each method.
                # Look up at Controller.service_connection to use it as an example,
                # the above method is an echo.
                # Be careful with how many bytes a socket will receive when using
                # socket.recv(num_of_bytes) method.
                request = binary_to_json(recv_data)
                type = request["type"]
                if type == 0:
                    self.accept_wrapper(sock, events, selector)
                elif type == 1:
                    self.service_connection(key, mask, selector)
            else:
                print(f"Closing connection to {data.addr}")
                Controller.symbols.append(self.player_identifier[sock.fileno()])
                del(self.player_identifier[sock.fileno()])
                selector.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
    