class InvalidMove(Exception):
    pass

class InvalidLength(InvalidMove):
    def __init__(self):
        super().__init__('Invalid move: Move must involve exactly one position.')

class InvalidPosition(InvalidMove):
    def __init__(self):
        super().__init__(f'Invalid move: Position is already occupied')

class InvalidPlayer(InvalidMove):
    def __init__(self):
        super().__init__(f'Invalid move: Not your turn.')