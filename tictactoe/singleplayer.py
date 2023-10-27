from utils.strdiff import strdiff
from math import inf as infinity
from errors.invalid_move import *

class TicTacToe:
    def __init__(self, difficulty=1):
        self.difficulty = difficulty
        self.board = '0' * 18

    def get_board(self):
        return self._board

    def get_state(self):
        return self._state
    
    def reset(self):
        self._state = 'playing'
        self._board = '0' * 18
        self._current_player = 1

    def has_won(self):
        board = self.get_x() if self._current_player == 1 else self.get_o()
        if board.count('1') < 3:
            return False
        for i in range(3):
            if board[i] == board[i + 3] == board[i + 6] == '1':
                return True
        for i in range(0, 9, 3):
            if board[i] == board[i + 1] == board[i + 2] == '1':
                return True
        if board[0] == board[4] == board[8] == '1':
            return True
        if board[2] == board[4] == board[6] == '1':
            return True
        
    def is_position_occupied(self, position):
        return self._board[position] != '0'
    
    def valid_move(self, move):
        diff = strdiff(self._board, move)
        if len(diff) != 1:
            raise InvalidMove()
        if self._current_player == 1 and diff[0] > 8:
            raise ValueError('Invalid move')
        if self._current_player == 0 and diff[0] < 8:
            raise ValueError('Invalid move')
        if self.is_position_occupied(diff[0]):
            raise ValueError('Invalid move')
        return True
    
    def play(self, board):
        if not self.valid_move(board):
            return
        self._board = board

    def possible_moves(state):
        moves = []
        for i in range(8, 17):
            if state[i] == '0' and state[i - 8] != '1':
                moves.append(state[:i] + '1' + state[i + 1:])
        return moves
