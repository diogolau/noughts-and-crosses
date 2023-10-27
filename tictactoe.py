from utils.strdiff import strdiff

class TicTacToe:
    def __init__(self):
        self._state = 'playing'
        self._board = '0' * 18
        self._current_player = 1

    def get_x(self):
        return self._board[:9]
    
    def get_o(self):
        return self._board[9:]
    
    def get_board(self):
        return self._board
    
    def get_current_player(self):
        return self._current_player
    
    def get_state(self):
        return self._state
    
    def reset(self):
        self._state = 'playing'
        self._board = '0' * 18
        self._current_player = 1
    
    def has_won(self):
        if self._state != 'playing':
            return False
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
        
    def is_draw(self):
        return self._board.count('0') == 0 and not self.has_won()
    
    def is_position_occupied(self, position):
        return self._board[position] != '0'
    
    def valid_move(self, move):
        diff = strdiff(self._board, move)
        if len(diff) != 1:
            raise ValueError('Invalid move')
        if self._current_player == 1 and diff[0] > 8:
            raise ValueError('Invalid move')
        if self._current_player == 0 and diff[0] < 8:
            raise ValueError('Invalid move')
        if self.is_position_occupied(diff[0]):
            raise ValueError('Invalid move')
        return True


    def set_board(self, player, board):
        if player != self._current_player:
            return
        if not self.valid_move(board):
            return
        self._board = board
        if self.has_won():
            self._state = 'won'
            return 'won'
        if self.is_draw():
            self._state = 'draw'
            return 'draw'
        self._current_player = 1 - self._current_player

