import socket

HOST = "172.15.5.226"
PORT = 60000

with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    message = input("Type your message to get an echo: ")
    while True:
        message = input("Type your message to get an echo: ")
        if message == "q":
            break
        b_message = message.encode()
        client.sendall(b_message)
        data = client.recv(1024)
        print(data.decode())