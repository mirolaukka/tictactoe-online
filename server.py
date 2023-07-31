import socket
import threading
import random

HOST = "127.0.0.1"  # Replace with your server IP address if needed
PORT = 65432


class TicTacToeServer:
    def __init__(self):
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen()

        self.players = []
        self.game = None

    def handle_client(self, conn, addr):
        with self.lock:
            if len(self.players) >= 2:
                conn.sendall("The game is full. Try again later.".encode())
                conn.close()
                return

            self.players.append(conn)
            if len(self.players) == 2:
                self.game = TicTacToeGame()

        conn.sendall("Welcome to Tic Tac Toe! Waiting for another player...".encode())

        while len(self.players) < 2:
            pass

        player_num = self.players.index(conn)
        conn.sendall(f"Game is starting. You are player {player_num + 1}".encode())

        while True:
            data = conn.recv(1024)
            if not data:
                break

            with self.lock:
                if self.game is None:
                    break

                player = self.players.index(conn)
                if player == self.game.get_current_player():
                    position = int(data.decode())
                    if self.game.make_move(position):
                        game_over, winner = self.game.check_winner()
                        if game_over:
                            self.send_to_all_clients(self.game.get_board_str())
                            self.send_to_all_clients(f"Game Over! Winner: {winner}")
                            self.game = None
                        else:
                            self.send_to_all_clients(self.game.get_board_str())
                    else:
                        conn.sendall("Invalid move. Try again.".encode())
                else:
                    conn.sendall("Not your turn. Wait for your opponent.".encode())

        with self.lock:
            self.players.remove(conn)
            if not self.players:
                self.game = None

        conn.close()

    def send_to_all_clients(self, message):
        for conn in self.players:
            conn.sendall(message.encode())

    def start(self):
        print("Server started. Waiting for connections...")
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connected by {addr}")
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()


class TicTacToeGame:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = random.randint(0, 1)  # Randomly choose starting player
        self.WINNING_COMBINATIONS = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # Rows
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # Columns
            [0, 4, 8],
            [2, 4, 6],  # Diagonals
        ]

    def make_move(self, position):
        if self.board[position] == " ":
            self.board[position] = "X" if self.current_player == 0 else "O"
            self.current_player = 1 - self.current_player
            return True
        return False

    def check_winner(self):
        for player in ["X", "O"]:
            for combination in self.WINNING_COMBINATIONS:
                if all(self.board[i] == player for i in combination):
                    return True, player

        if all(cell != " " for cell in self.board):
            return True, "Draw"

        return False, None

    def check_draw(self):
        # Implement logic to check if the game is a draw
        pass

    def is_game_over(self):
        # Implement logic to check if the game is over
        pass

    def get_board(self):
        return self.board

    def get_board_str(self):
        return ",".join(self.board)

    def get_current_player(self):
        return self.current_player


if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()
