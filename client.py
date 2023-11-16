import socket
from utils.json_utils import dict_to_binary, binary_to_dict
import tkinter as tk
import threading
import math
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])
CONNECTION_ESTABLISHED = False

try:
    def create_thread(target):
        '''
        General function that creates a new thread.
        '''
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
    

    # Configuration of the client socket and connecting it to the server
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Receiving the config information from the server
    json_config = client.recv(1024)
    json_message = binary_to_dict(json_config)
    
    # End client's program execution if connection couldn't be established
    if not json_message["connection"]:
        raise KeyboardInterrupt
    

    # Set the token to the client
    token = json_message["token"]

    CONNECTION_ESTABLISHED = True
    
    next_board = "000000000000000000"

    def receive_data():
        '''
        Function that will be responsible for receive messages sent by the server.
        '''
        global next_board
        while True:
            response_binary = client.recv(1024)
            response = binary_to_dict(response_binary)
            next_board = response["next_board"]
            update_board(next_board)
            if response["status"] == "1":
                color_the_board(response, reset=True)
            else:
                color_the_board(response)
    
    # Start the receive_data in another thread
    create_thread(receive_data)

    # Creates the tkinter window and start the board
    root = tk.Tk()
    root.title(f"Jogo da Velha - Jogador {token if token else 2}")
    board = [0] * 18

    # Set up buttons for tic tac toe
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            btn = tk.Button(root, text='', font=('normal', 14), width=5, height=2,
                            command=lambda row=i, col=j: play(row, col))
            btn.grid(row=i, column=j)
            row.append(btn)
        buttons.append(row)

    def play(row, col):
        '''
        Handle a new move and send it to server.
        '''
        global token
        index = 3 * row + col - 9 * (token-1)
        play_board = board.copy()
        play_board[index] = 1
        for index, i in enumerate(play_board):
            play_board[index] = str(i)
        request_board = ''.join(play_board)
        request = {
            "token": token,
            "play": request_board
        }
        request_b = dict_to_binary(request)
        client.send(request_b)

    def update_board(next_board_str):
        '''
        Update the board when receive a message from the server.
        '''
        global board
        next_board = [*next_board_str]

        board_x = next_board[:9]
        board_o = next_board[9:]

        updated_buttons = []

        def update_button(symbol, index, update_x=False):
            index_button = index
            row = math.floor(index_button/3)
            col = index_button % 3
        
            if int(button_state):
                buttons[row][col].config(text=symbol)
            elif index not in updated_buttons:
                buttons[row][col].config(text='')

            if update_x:
                updated_buttons.append(index)

        for index, button_state in enumerate(board_x):
            symbol = "X"
            update_button(symbol, index, update_x=True)
                
        for index, button_state in enumerate(board_o):
            symbol = "O"
            update_button(symbol, index)

        board = next_board
    
    def color_the_board(response, reset=False):
        '''
        Color the board if is the case.
        '''
        if reset:
            buttons_to_color = [*response["colored_board"]]

            for index, button_state in enumerate(buttons_to_color):
                row = math.floor(index/3)
                col = index % 3

                buttons[row][col].config(bg="white")

        if response["status"] != "00":
            if response["status"] == "11":
                pass
            else:
                buttons_to_color = [*response["colored_board"]]
                
                for index, button_state in enumerate(buttons_to_color):
                    if int(button_state):
                        row = math.floor(index/3)
                        col = index % 3

                        buttons[row][col].config(bg="green")

    root.mainloop()
except KeyboardInterrupt:
    client.close()