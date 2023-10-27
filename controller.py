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
                "connection": True,
                "token": self.player_identifier[conn.fileno()]
            }
            b_message = json_to_binary(token_message)
            conn.send(b_message)
        else:
            conn, addr = sock.accept()
            error_message = {
                "connection": False
            }
            b_message = json_to_binary(error_message)
            conn.send(b_message)
            print(f"Reject connection from {addr}")
            conn.close()
    
    def message_handler(self, key, mask, selector, events):
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
                self.service_connection(sock, request) 
            else:
                print(f"Closing connection to {data.addr}")
                Controller.symbols.append(self.player_identifier[sock.fileno()])
                del(self.player_identifier[sock.fileno()])
                selector.unregister(sock)
                sock.close()

    def service_connection(self, socket, request):
        if "play" in request.keys():
            response = {
                "next_board": '000000000000000000',
                "status": '00',
                "colored_board": "000000000"
            }
            socket.send(json_to_binary(response))


    
    