import socket
import json
from utils.json_utils import binary_to_json

HOST = "127.0.0.1"
PORT = 60000

try:
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    json_config = client.recv(1024)
    json_message = binary_to_json(json_config)
    if json_message["type"] == -1:
        raise KeyboardInterrupt
    
    token = json_message["token"]
    
    data = None
    while True:
        if data == 'q':
            break
        if data == 'g':
            message = {
                "type": 0
            }
            b_message = (json.dumps(message)).encode()
            client.sendall(b_message)
            data = client.recv(1024)
            print(data)
        else:
            message = {
                "type": 1,
                "token": token,
                "data": data
            }

        data = input("Play: ")

        
except KeyboardInterrupt:
    client.close()