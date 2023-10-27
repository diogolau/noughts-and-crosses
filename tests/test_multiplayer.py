from tictactoe.multiplayer import TicTacToe

game = TicTacToe()

def test_initial_state():
    assert game.get_board() == '0' * 18