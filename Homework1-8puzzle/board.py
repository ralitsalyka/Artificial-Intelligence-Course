class Puzzle():
    def __init__(self, board, empty_elem=0, previous=None, moves=0, move=''):
        self.board = board
        self.empty_elem = empty_elem
        self.previous = previous
        self.moves = moves
        self.found_nodes = None
        self.direction_array = []
        self.move = move

    def __eq__(self, other):
        return self.board == other.board

    def manhattan_distance(self, final_state):
        distance = 0
        for elem in self.board:
            for e in elem:
                tup1 = self.find_coordinates_of_elem(e)
                tup2 = final_state.find_coordinates_of_elem(e)
                current_sum = (abs((tup1[0]) - (tup2[0])) + abs((tup1[1]) - (tup2[1])))
                if current_sum != 0 and e != 0:
                    distance += current_sum
        return distance

    def find_coordinates_of_elem(self, key):
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                if self.board[i][j] == key:
                    return (i, j)

    def heuristic_function(self, final_state):
        return self.moves + self.manhattan_distance(final_state)

    def is_goal(self):
        flag = True
        size = len(self.board) - 1
        for i in range(0, size):
            for j in range(0, size - 1):

                if self.board[i][j] + 1 != self.board[i][j + 1]:
                    flag = False
                    break
        return flag

    def represent_puzzle(self):
        for i in self.board:
            print(i)