import socket
import tkinter as tk
import threading
from tkinter import messagebox

HOST = "127.0.0.1"  # Replace with your server IP address if needed
PORT = 65432


class TicTacToeClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.board = tk.Frame(self.root)
        self.board.pack()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.board,
                    width=10,
                    height=4,
                    command=lambda row=i, col=j: self.on_button_click(row, col),
                )
                self.buttons[i][j].grid(row=i, column=j)

        self.message_label = tk.Label(self.root, text="")
        self.message_label.pack()

        self.listen_thread = threading.Thread(target=self.listen_for_server)
        self.listen_thread.start()

    def listen_for_server(self):
        while True:
            data = self.socket.recv(1024).decode()
            print("Received data:", data)  # Add this line for debugging

            if data.startswith("Game Over!"):
                self.show_winner(data)
                self.root.quit()
                break
            elif data.startswith("Welcome"):
                self.message_label.config(text=data)
            elif data.startswith("Game is starting") or data.startswith(
                "Not your turn"
            ):
                pass
            else:
                self.update_board(data)

    def update_board(self, data):
        board_state = data.split(",")
        print("Board state:", board_state)  # Add this line for debugging
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = board_state[i * 3 + j]

    def on_button_click(self, row, col):
        position = row * 3 + col
        self.socket.sendall(str(position).encode())

    def show_winner(self, data):
        messagebox.showinfo("Game Over", data)

    def on_closing(self):
        self.socket.close()
        self.root.destroy()


if __name__ == "__main__":
    client = TicTacToeClient()
    client.root.mainloop()
