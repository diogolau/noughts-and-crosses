import tkinter as tk
from tkinter import Entry, Label, Button
import subprocess
import threading

def iniciar_servidor(host, porta, aviso_label):
    comando = f"python server.py {host} {porta}"
    try:
        output = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, text=True)
        aviso_label.config(text=output)
    except subprocess.CalledProcessError as e:
        error_message = e.output.strip().split('\n')[-1]
        aviso_label.config(text=f"Falha ao iniciar o servidor: {error_message}")

def iniciar_servidor_em_thread(host, porta, aviso_label):
    # Executa iniciar_servidor em uma thread para não bloquear a interface
    threading.Thread(target=iniciar_servidor, args=(host, porta, aviso_label)).start()

def iniciar_interface():
    root = tk.Tk()
    root.title("Iniciar Servidor")

    label_host = Label(root, text="Host:")
    label_host.pack()

    entry_host = Entry(root)
    entry_host.pack()

    label_porta = Label(root, text="Porta:")
    label_porta.pack()

    entry_porta = Entry(root)
    entry_porta.pack()

    aviso_label = Label(root, text="")
    aviso_label.pack()

    botao_iniciar = Button(root, text="Iniciar Servidor", command=lambda: iniciar_servidor_em_thread(entry_host.get(), entry_porta.get(), aviso_label))
    botao_iniciar.pack()

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()