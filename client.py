import socket
import json

HOST = "127.0.0.1"
PORT = 60000

try:
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    while True:
        data = input("Type your message to get an echo: ")
        if data == "q":
            break
        message = {
            "type": 0,
            "data": data
        }

        b_message = (json.dumps(message)).encode()
        client.sendall(b_message)
        data = client.recv(1024)
        print(data.decode())
except KeyboardInterrupt:
    client.close()