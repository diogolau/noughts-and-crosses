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
            print(response)
            if "next_board" in response.keys():
                print("tá aqui")
                next_board = response["next_board"]
                update_board(next_board)
    
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
        # # Altera o valor do botão entre 0 e 1
        # board[index] = 1 if board[index] == 0 else 0
        # # Atualiza o texto do botão com 'X' ou 'O' com base no novo valor
        # botoes[row][col].config(text='X' if board[index] == 1 else 'O')

    def update_board(next_board_str):
        global board
        next_board = [*next_board_str]

        for index, i in enumerate(next_board):
            next_board[index] = int(i)
        
        for index, var in enumerate(next_board):
            if index <= 8:
                symbol = "X"
            else:
                symbol = "O"

            index_button = index % 9

            row = math.floor(index_button/3)
            col = index_button % 3
            if var:
                buttons[row][col].config(text=symbol)

        board = next_board
    

    root.mainloop()
except KeyboardInterrupt:
    client.close()