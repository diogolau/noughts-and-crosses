import selectors
import types
from utils.json_utils import binary_to_dict, dict_to_binary
from errors.invalid_move import InvalidLength, InvalidPlayer, InvalidPosition

class Controller:
    connection_limit = 2
    symbols = [1, 0]

    def __init__(self):
        self.server_state = "000000000000000000"
        self.player_identifier = {}

    def accept_wrapper(self, sock, events, selector):
        '''
        Accepts a new connection if the limit has not been reached, or rejects it otherwise.
        '''
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
            print(self.player_identifier)
            b_message = dict_to_binary(token_message)
            conn.send(b_message)
        else:
            conn, addr = sock.accept()
            error_message = {
                "connection": False
            }
            b_message = dict_to_binary(error_message)
            conn.send(b_message)
            print(f"Reject connection from {addr}")
            conn.close()
    
    def message_handler(self, key, mask, selector, events, game, is_multiplayer=True):
        '''
        Handle all messages sent by a socket, executing a new move or closing the connection with a client's socket.
        '''
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            try:
                recv_data = sock.recv(1024)
            except ConnectionResetError:
                recv_data = 0
            if recv_data:
                # Remember to pass the socket and data for each method.
                # Be careful with how many bytes a socket will receive when using
                # socket.recv(num_of_bytes) method.
                request = binary_to_dict(recv_data)
                if "play" in request.keys():
                    self.play_game(sock, request, game, selector, is_multiplayer)
            else:
                print(f"Closing connection to {data.addr}")
                Controller.symbols.append(self.player_identifier[sock.fileno()])
                del(self.player_identifier[sock.fileno()])
                selector.unregister(sock)
                sock.close()

                game.reset()
                self.server_state = game.get_board()
                response_dict = {
                    "next_board": self.server_state,
                    "status": "00",
                    "colored_board": "000000000"
                }
                response_b = dict_to_binary(response_dict)
                
                for key, event in selector.select():
                    try:
                        socket = key.fileobj
                        socket.send(response_b)
                    except OSError:
                        ...


    def play_game(self, socket, request, game, selector, is_multiplayer):
        '''
        Executes a new move in the game.
        '''
        try:
            response_dict = game.set_board(self.player_identifier[socket.fileno()], request["play"])
            self.server_state = response_dict["next_board"]
            if len(self.player_identifier) != 2 and is_multiplayer:
                game.reset()
                self.server_state = '0' * 18
                response_dict["next_board"] = self.server_state
                response_dict["status"] = "00"
            response_b = dict_to_binary(response_dict)
            for key, event in selector.select():
                socket = key.fileobj
                socket.send(response_b)
        except InvalidLength:
            error_message = {
                "next_board": self.server_state, 
                "status": -1, 
                "colored_board": "000000000"
            }
            response = dict_to_binary(error_message)
            socket.send(response)
        except InvalidPlayer:
            error_message = {
                "next_board": self.server_state, 
                "status": -1, 
                "colored_board": "000000000"
            }
            response = dict_to_binary(error_message)
            socket.send(response)
        except InvalidPosition:
            error_message = {
                "next_board": self.server_state, 
                "status": -1, 
                "colored_board": "000000000"
            }
            response = dict_to_binary(error_message)
            socket.send(response)