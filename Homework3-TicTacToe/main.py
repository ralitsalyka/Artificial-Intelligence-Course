from board import Board
from copy import deepcopy


INITIAL_BOARD = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
PLAYER_SIGN = 'X'
COMPUTER_SIGN = 'O'


def choose_who_is_first():
    first_player = int(input('Choose 1 for start first or 2 for second: '))
    while first_player != 1 and first_player != 2:
        first_player = int(input('Choose 1 for start first or 2 for second: '))
    return first_player


def input_move():
    input_coordinates = input('Input your move as a coordinates: ')
    coordinates = input_coordinates.split(', ')
    tuple_coordinates = (int(coordinates[0]), int(coordinates[1]))
    return tuple_coordinates


def make_move(board, move, sign):
    is_empty_move = False
    while not is_empty_move:
        if board.check_is_empty_place(move):
            board.make_move_on_board(move, sign)
            is_empty_move = True
    return board


def start_playing_sign(first_player):
    current_player_sign = ''
    if first_player == 1:
        current_player_sign = PLAYER_SIGN
    else:
        current_player_sign = COMPUTER_SIGN
    return current_player_sign


def getChildren(board, player):
    children = []
    for i in range(3):
        for j in range(3):
            elem = board[i][j]
            if elem != '_':
                pass
            else:
                next_state = deepcopy(board)
                sign = start_playing_sign(player)
                next_state[i][j] = sign
                children.append(next_state)
    return children


if __name__ == '__main__':
    first_player = choose_who_is_first()
    initial_board = Board(INITIAL_BOARD)
    initial_board.print_board()
    move = input_move()
    lst = getChildren(Board([['X', 'X', 'O'], ['O', '_', '_'], ['_', 'O', 'O']]), 1)
#    for elem in lst:
#        elem.print_board()
