from copy import deepcopy
import os
import math
from time import sleep
INITIAL_BOARD = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
PLAYER_SIGN = 'X'
COMPUTER_SIGN = 'O'
EMPTY_PLACE = '_'


class Board():
    def __init__(self, board):
        self.board = board

    def __getitem__(self, index):
        return self.board[index]

    def __setitem__(self, index, value):
        self.board[index] = value

    def print_board(self):
        for row in self.board:
            string = row[0] + ' | ' + row[1] + ' | ' + row[2]
            print(string)
            print('     ')

    def check_is_empty_place(self, move):
        return self.board[move[0]][move[1]] == '_'

    def make_move_on_board(self, move, sign):
        self.board[move[0]][move[1]] = sign
        return self.board

    def is_board_full(self):
        for elem in self.board:
            for el in elem:
                if el is '_':
                    return False
        return True

    def winning_states(self):
        brd = self.board
        winning_states = [[brd[0][0], brd[0][1], brd[0][2]],
                          [brd[1][0], brd[1][1], brd[1][2]],
                          [brd[2][0], brd[2][1], brd[2][2]],
                          [brd[0][0], brd[1][0], brd[2][0]],
                          [brd[0][1], brd[1][1], brd[2][1]],
                          [brd[0][2], brd[1][2], brd[2][2]],
                          [brd[0][0], brd[1][1], brd[2][2]],
                          [brd[2][0], brd[1][1], brd[0][2]]
                          ]
        if ['X', 'X', 'X'] in winning_states:
            return True
        elif ['O', 'O', 'O'] in winning_states:
            return True
        else:
            return False

    def utility(self):
        brd = self.board
        diagonals = [[brd[0][0], brd[1][1], brd[2][2]],
                     [brd[2][0], brd[1][1], brd[0][2]]
                     ]

        rows_and_columns = [[brd[0][0], brd[0][1], brd[0][2]],
                            [brd[1][0], brd[1][1], brd[1][2]],
                            [brd[2][0], brd[2][1], brd[2][2]],
                            [brd[0][0], brd[1][0], brd[2][0]],
                            [brd[0][1], brd[1][1], brd[2][1]],
                            [brd[0][2], brd[1][2], brd[2][2]],
                            ]

        if ['X', 'X', 'X'] in diagonals:
            return -1
        elif ['X', 'X', 'X'] in rows_and_columns:
            return -1
        elif ['O', 'O', 'O'] in diagonals:
            return 1
        elif ['O', 'O', 'O'] in rows_and_columns:
            return 1
        elif not self.is_board_full():
            return -2
        return 0


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


def max_value(board, alpha, beta, initDepth, bestDepth):
    best = -math.inf
    next_move = (0, 0)
    isTerminalState = board.utility()
    if isTerminalState == -1:
        return (-1, next_move, initDepth, bestDepth)
    elif isTerminalState == 1:
        return (1, next_move, initDepth, bestDepth)
    elif isTerminalState == 0:
        return (0, next_move, initDepth, bestDepth)

    for i in reversed(range(0, 3)):
        for j in reversed(range(0, 3)):
            current_board = deepcopy(board)
            if current_board[i][j] == EMPTY_PLACE:
                depth = initDepth
                current_board[i][j] = COMPUTER_SIGN
                new_best = min_value(current_board, alpha, beta, depth + 1, bestDepth)
                depth = new_best[2]
                bestDepth = new_best[3]
                if new_best[0] > best or (new_best[0] == best and depth < bestDepth):
                    best = new_best[0]
                    next_move = (i, j)
                    bestDepth = depth
                if best >= beta:
                    return (best, next_move, depth, bestDepth)
                alpha = max(best, alpha)
    return (best, next_move, depth, bestDepth)


def min_value(board, alpha, beta, initDepth, bestDepth):
    best = math.inf
    next_move = (0, 0)
    isTerminalState = board.utility()
    if isTerminalState == -1:
        return (-1, next_move, initDepth, bestDepth)
    elif isTerminalState == 1:
        return (1, next_move, initDepth, bestDepth)
    elif isTerminalState == 0:
        return (0, next_move, initDepth, bestDepth)

    for i in range(0, 3):
        for j in range(0, 3):
            current_board = deepcopy(board)
            if current_board[i][j] == EMPTY_PLACE:
                depth = initDepth
                current_board[i][j] = PLAYER_SIGN
                new_best = max_value(current_board, alpha, beta, depth + 1, bestDepth)
                depth = new_best[2]
                bestDepth = new_best[3]
                if new_best[0] < best or (new_best[0] == best and depth < bestDepth):
                    best = new_best[0]
                    next_move = (i, j)
                    bestDepth = depth
                if best <= alpha:
                    return (best, next_move, depth, bestDepth)
                beta = min(best, beta)
    return (best, next_move, depth, bestDepth)


def ai_move(board):
    depth = 0
    bestDepth = 11
    board_copy = deepcopy(board)
    (m, move, d, bd) = max_value(board_copy, -math.inf, math.inf, depth, bestDepth)
    board[move[0]][move[1]] = 'O'
    return board


def human_move(board, starting_sign):
    move = input_move()
    make_move(board, move, starting_sign)
    return board


def execute():
    first_player = choose_who_is_first()
    board = Board(INITIAL_BOARD)
    os.system('clear')
    board.print_board()
    current_turn = start_playing_sign(first_player)
    while True:
        isTerminalState = board.utility()
        if isTerminalState != -2:
            return isTerminalState
        if current_turn == 'X':
            board = deepcopy(human_move(board, current_turn))
            os.system('clear')
            board.print_board()
            current_turn = 'O'
        else:
            board = deepcopy(ai_move(board))
            current_turn = 'X'
        os.system('clear')
        board.print_board()


if __name__ == '__main__':
    terrminalState = execute()
    if terrminalState == -1:
        print('You win!')
    elif terrminalState == 1:
        print('You lose!')
    else:
        print("Equal!")

