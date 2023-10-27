import tkinter as tk
from server import initiate_server

class ServerConfigScreen:
    def __init__(self, master):
        self.master = master
        master.title("Server Configuration")

        self.label_host = tk.Label(master, text="Host:")
        self.label_host.grid(row=0, column=0)

        self.entry_host = tk.Entry(master)
        self.entry_host.grid(row=0, column=1)

        self.label_port = tk.Label(master, text="Port:")
        self.label_port.grid(row=1, column=0)

        self.entry_port = tk.Entry(master)
        self.entry_port.grid(row=1, column=1)

        self.button_initialize = tk.Button(master, text="Initialize Server", command=self.initialize_server)
        self.button_initialize.grid(row=2, column=0)

        self.button_kill = tk.Button(master, text="Kill Server", command=self.kill_server)
        self.button_kill.grid(row=2, column=1)

        self.text_logs = tk.Text(master, height=10, width=40)
        self.text_logs.grid(row=3, columnspan=2)

        self.text_requests_responses = tk.Text(master, height=10, width=40)
        self.text_requests_responses.grid(row=4, columnspan=2)

        self.label_server_state = tk.Label(master, text="Server State: ")
        self.label_server_state.grid(row=5, column=0)

        self.label_server_state_value = tk.Label(master, text="Not Running")
        self.label_server_state_value.grid(row=5, column=1)

    def initialize_server(self):
        host = self.entry_host.get()
        port = self.entry_port.get()
        if host and port:
            initiate_server(host, port)
            self.label_server_state_value.config(text="Running")
            self.text_logs.insert(tk.END, "Server initialized\n")
        else:
            self.text_logs.insert(tk.END, "Please provide host and port\n")

    def kill_server(self):
        self.label_server_state_value.config(text="Not Running")
        self.text_logs.insert(tk.END, "Server killed\n")


if __name__ == '__main__':
    root = tk.Tk()
    my_gui = ServerConfigScreen(root)
    root.mainloop()
