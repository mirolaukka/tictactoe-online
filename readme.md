
# Multiplayer Tic Tac Toe Game

This is a multiplayer Tic Tac Toe game implemented in Python using Tkinter for the graphical user interface (GUI) and sockets for networking. The game allows two players to connect to a server and play Tic Tac Toe against each other on a 3x3 grid.

## Features

- Two players can play Tic Tac Toe on separate client machines connected to a server.
- The server manages game sessions and allows players to join and play together.
- The game GUI is built using Tkinter, providing a user-friendly interface.
- Players take turns making moves, and the server enforces the game rules.

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)
- Sockets (standard library module)

## How to Run

1. Clone the repository to your local machine:

```bash
git clone https://github.com/mirolaukka/tictactoe-online.git
cd tictactoe-online
```

2. Run the server script on the host machine:

```bash
python server.py
```

3. Run the client script on each client machine:

```bash
python client.py
```

4. Enter the server IP address when prompted by the client. The client will connect to the server and display the game board.

5. Two players should connect to the server to start the game. The game will begin automatically once two players are connected.

6. Players can make moves by clicking on the respective cells on the game board.

## Game Rules

- The game follows the standard Tic Tac Toe rules.
- Players take turns to place their respective marks ('X' or 'O') on an empty cell.
- The game ends when one player forms a winning combination of three marks in a row, column, or diagonal.
- If no player forms a winning combination and all cells are filled, the game ends in a draw.

## Known Issues

- The game does not handle edge cases and error scenarios thoroughly as it is a basic implementation.
- There might be some latency in multiplayer gameplay depending on the network connection.

## Contribution

Contributions to this project are welcome! If you find any issues or have ideas for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
