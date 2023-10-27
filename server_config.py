import tkinter as tk

class ServerConfigurationScreen:
    def __init__(self, master):
        self.master = master
        master.title("Server Configuration")

        self.host_label = tk.Label(master, text="Host Port:")
        self.host_label.pack()

        self.host_entry = tk.Entry(master, highlightbackground="white")
        self.host_entry.pack()

        self.send_button = tk.Button(master, text="Send", command=self.send_values)
        self.send_button.pack()

        self.init_button = tk.Button(master, text="Initialize Server", command=self.initialize_server)
        self.init_button.pack()

        self.kill_button = tk.Button(master, text="Kill Server", command=self.kill_server)
        self.kill_button.pack()

        self.logs_textarea = tk.Text(master, highlightbackground="white")
        self.logs_textarea.pack()

        self.summary_textarea = tk.Text(master, highlightbackground="white")
        self.summary_textarea.pack()

        self.server_state_label = tk.Label(master, text="Server State: ")
        self.server_state_label.pack()

    def send_values(self):
        host_port = self.host_entry.get()
        # Logic to handle host port

    def initialize_server(self):
        # Logic to initialize the server here
        pass

    def kill_server(self):
        # Logic to kill the server here
        pass

if __name__ == '__main__':
    root = tk.Tk()
    my_gui = ServerConfigurationScreen(root)
    root.mainloop()
