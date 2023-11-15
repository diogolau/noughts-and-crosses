from utils.strdiff import strdiff
from utils.str_replace import replace_indexes
from errors.invalid_move import *
import json

EMPTY_BOARD = '0' * 9

'''

The state of the game is represented by a string of 18 characters (board)
The first 9 characters represent the X player (X-semi-board)
The last 9 characters represent the O player (O-semi-board)
A 0 represents an empty position
A 1 represents a position occupied by a player

'''
class TicTacToe:
    def __init__(self):
        self._state = 'playing'
        self._board = '0' * 18

    def get_x(self):
        return self._board[:9]
    
    def get_o(self):
        return self._board[9:]
    
    def get_board(self):
        return self._board
    
    def get_state(self):
        return self._state
    
    def count_x(self):
        return self.get_x().count('1')
    
    def count_o(self):
        return self.get_o().count('1')
    
    def current_player(self):
        if self.count_x() == self.count_o():
            return 1
        return 0
    
    def get_status(self):
        if self._state == 'won':
            if self.has_won() == 1:
                return '01'
            return '10'
        if self._state == 'draw':
            return '11'
        return '00'
    
    def reset(self):
        self._state = 'playing'
        self._board = '0' * 18
        
    def row_filled(self, semi_board, positions=False):
        for i in range(0, 9, 3):
            if semi_board[i] == semi_board[i + 1] == semi_board[i + 2] == '1':
                return True if positions else i
        return False

    def column_filled(self, semi_board, positions=False):
        for i in range(3):
            if semi_board[i] == semi_board[i + 3] == semi_board[i + 6] == '1':
                return True if positions else i
        return False
    
    def diagonal_filled(self, semi_board, positions=False):
        if semi_board[0] == semi_board[4] == semi_board[8] == '1':
            return True if positions else 1
        if semi_board[2] == semi_board[4] == semi_board[6] == '1':
            return True if positions else -1
        return False
    
    '''
    Returns 1 if X has won
    Returns 0 if O has won
    Returns -1 if no one has won
    '''
    def has_won(self):
        if self._state != 'playing':
            return -1
        board_x = self.get_x()
        board_o = self.get_o()
        if self.row_filled(board_x) or self.column_filled(board_x) or self.diagonal_filled(board_x):
            return 1
        if self.row_filled(board_o) or self.column_filled(board_o) or self.diagonal_filled(board_o):
            return 0
        return -1

    def is_draw(self):
        return self._board.count('1') == 9 and not self.has_won()

    def is_position_occupied(self, position):
        return self._board[position] != '0'
    
    def valid_move(self, move):
        diff = strdiff(self._board, move)
        print(len(diff))
        if len(diff) != 1:
            raise InvalidLength()
        if self.current_player() == 1 and diff[0] > 8:
            raise InvalidPlayer()
        if self.current_player() == 0 and diff[0] < 8:
            raise InvalidPlayer()
        if self.is_position_occupied(diff[0]):
            raise InvalidPosition()
        return True

    def set_board(self, player, board):
        if player != self.current_player():
            raise InvalidPlayer()
        if not self.valid_move(board):
            return
        self._board = board
        win = self.has_won()
        if win != -1:
            self._state = 'won'
        if self.is_draw():
            self._state = 'draw'
        return self.build_response()
    
    def get_colored_board(self):
        if self._state != 'won':
            return '0' * 9
        semi_board = self.get_x() if self.has_won() == 1 else self.get_o()
        if self.row_filled(semi_board):
            i = self.row_filled(semi_board, True)
            return replace_indexes(EMPTY_BOARD, [i, i + 1, i + 2], '1')
        if self.column_filled(semi_board):
            i = self.column_filled(semi_board, True)
            return replace_indexes(EMPTY_BOARD, [i, i + 3, i + 6], '1')
        if self.diagonal_filled(semi_board):
            i = self.diagonal_filled(semi_board, True)
            if i == 1:
                return replace_indexes(EMPTY_BOARD, [0, 4, 8], '1')
            return replace_indexes(EMPTY_BOARD, [2, 4, 6], '1')
        return EMPTY_BOARD
    
    def build_response(self):
        next_board = self.get_board()
        status = self.get_status()
        colored_board = self.get_colored_board()
        return {'next_board': next_board, 'status': status, 'colored_board': colored_board}


