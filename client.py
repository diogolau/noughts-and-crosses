import socket
from utils.json_utils import dict_to_binary, binary_to_dict
import json
import tkinter as tk
import threading
import math

HOST = "127.0.0.1"
PORT = 60000
CONNECTION_ESTABLISHED = False

try:
    def create_thread(target):
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
    
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    json_config = client.recv(1024)
    json_message = binary_to_dict(json_config)
    if not json_message["connection"]:
        raise KeyboardInterrupt
    
    token = json_message["token"]
    print(f"My token is: {token}")
    CONNECTION_ESTABLISHED = True
    
    next_board = "000000000000000000"

    def receive_data():
        global next_board
        while True:
            response_binary = client.recv(1024)
            response = binary_to_dict(response_binary)
            next_board = response["next_board"]
            update_board(next_board)
            color_the_board(response)
    
    create_thread(receive_data)

    root = tk.Tk()

    root.title("Jogo da Velha")
    board = [0] * 18

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
        global board
        print(next_board_str)
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
    
    def color_the_board(response):
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