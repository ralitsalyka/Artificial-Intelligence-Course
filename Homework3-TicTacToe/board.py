class Board():
    def __init__(self, board):
        self.board = board

    def __getitem__(self, index):
        return self.board[index]

    def __setitem__(self, index, value):
        self.board[index] = value

    def print_board(self):
        for row in self.board:
            print(row)

    def check_is_empty_place(self, move):
        return self.board[move[0]][move[1]] == '_'

    def make_move_on_board(self, move, sign):
        self.board[move[0]][move[1]] = sign
        return self.board

    def is_board_full(self):
        full = True
        for elem in self.board:
            if elem is '_':
                full = False
        return full

    def winning_states(self, sign):
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
        if [sign, sign, sign] in winning_states:
            return True
        else:
            return False

    def utility(self, sign):
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

        if [sign, sign, sign] in diagonals and sign == 'X':
            return 1
        elif [sign, sign, sign] in rows_and_columns and sign == 'X':
            return 1
        elif [sign, sign, sign] in diagonals and sign == 'O':
            return -1
        elif [sign, sign, sign] in rows_and_columns and sign == 'O':
            return -1
        else:
            return 0
