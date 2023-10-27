import socket
from utils.json_utils import binary_to_json, json_to_binary

HOST = "127.0.0.1"
PORT = 60000

try:
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    json_config = client.recv(1024)
    json_message = binary_to_json(json_config)
    if not json_message["connection"]:
        raise KeyboardInterrupt
    
    token = json_message["token"]
    
    play = None
    while True:
        if play == 'q':
            raise KeyboardInterrupt
        elif play:
            message = {
                "token": token,
                "play": play
            }
            b_message = json_to_binary(message)
            client.sendall(b_message)
            response = binary_to_json(client.recv(1024))
            print(response["status"])

        else:
            pass

        play = input("Play: ")

        
except KeyboardInterrupt:
    client.close()