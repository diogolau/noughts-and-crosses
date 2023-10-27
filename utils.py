import json

def request_instructions(client_socket):
    message = {
        "type": 0
    }

    b_message = json.dumps(message).encode()
    client_socket.sendall(b_message)
    
    response = client_socket.recv(1)
