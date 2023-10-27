import tictactoe

game = tictactoe.TicTacToe()

print(game.get_board())
print(game.get_current_player())
print(game.get_state())
print(game.get_x())
print(game.get_o())

game.set_board(1, '100000000000000000')
game.set_board(0, '100000000000000010')
print(game.get_board())
game.set_board(1, '110000000000000010')
game.set_board(0, '110000000000000011')
game.set_board(1, '111000000000000011')
print(game.get_state());