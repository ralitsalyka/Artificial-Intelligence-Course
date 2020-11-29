from math import *
from copy import deepcopy
from board import *


def next_state_of_puzzle_graph(puzzle, position):
    next_nodes = []
    x = position[0]
    y = position[1]
    board = deepcopy(puzzle.board)
    if x - 1 >= 0:
        tmp = board[x][y]
        board[x][y] = board[x - 1][y]
        board[x - 1][y] = tmp
        next_nodes.append(Puzzle(board, (x - 1, y), puzzle, puzzle.moves + 1, 'Down'))
        board = deepcopy(puzzle.board)
    if y - 1 >= 0:
        tmp = board[x][y]
        board[x][y] = board[x][y - 1]
        board[x][y - 1] = tmp
        next_nodes.append(Puzzle(board, (x, y - 1), puzzle, puzzle.moves + 1, 'Right'))
        board = deepcopy(puzzle.board)
    if x + 1 <= 2:
        tmp = board[x][y]
        board[x][y] = board[x + 1][y]
        board[x + 1][y] = tmp
        next_nodes.append(Puzzle(board, (x + 1, y), puzzle, puzzle.moves + 1, 'Up'))
        board = deepcopy(puzzle.board)
    if y + 1 <= 2:
        tmp = board[x][y]
        board[x][y] = board[x][y + 1]
        board[x][y + 1] = tmp
        next_nodes.append(Puzzle(board, (x, y + 1), puzzle, puzzle.moves + 1, 'Left'))
        board = deepcopy(puzzle.board)
    return next_nodes


def find_zero_coordinates(puzzle):
    for x in range(0, len(puzzle.board)):
        for y in range(0, len(puzzle.board)):
            if puzzle.board[x][y] == 0:
                return (x, y)


def ida_algorithm_using(initial_puzzle, final_puzzle, goal):
    final_goal = final_puzzle
    treshold = initial_puzzle.heuristic_function(final_puzzle)
    while not goal:
        new_treshold = treshold + 1
        stack = [initial_puzzle]
        visited = [initial_puzzle]
        tup = stack_function(stack, visited, final_puzzle, treshold)
        final_goal = tup[0]
        goal = tup[1]
        treshold = new_treshold
    return final_goal


def stack_function(stack, visited, final_puzzle, treshold):
    flag = False
    while stack != []:
        elem = stack.pop()
        if elem == final_puzzle:
            flag = True
            final_puzzle = elem
            break
        position = find_zero_coordinates(elem)
        elem.found_nodes = next_state_of_puzzle_graph(elem, position)
        for next_node in elem.found_nodes:
            if next_node not in visited:
                treshold_of_next_node = next_node.heuristic_function(final_puzzle)
                if treshold_of_next_node < treshold:
                    stack.append(next_node)
                    visited.append(next_node)
    return (final_puzzle, flag)


def get_all_directions(initial_puzzle, final_puzzle):
    previous_puzzle = final_puzzle.previous
    count = 0
    direction = [final_puzzle.move]
    while previous_puzzle.previous is not initial_puzzle:
        previous_puzzle = previous_puzzle.previous
        direction.append(previous_puzzle.move)
        count += 1
    return direction


def create_goal(puzzle, n, pos):
    final_puzzle = []
    row = int(sqrt(n + 1))
    if pos == -1:
        final_puzzle = list(range(1, n + 1))
        final_puzzle.append(0)
    else:
        final_puzzle = list(range(1, pos + 1))
        final_puzzle.append(0)
        for i in range(pos + 1, n + 1):
            final_puzzle.append(i)
    final_goal = create_board(final_puzzle, row)
    return final_goal


def create_board(final_puzzle, row):
    final_goal = []
    current_goal = []
    count = 0
    for elem in final_puzzle:
        if count == row:
            final_goal.append(current_goal)
            current_goal = []
            count = 0
        current_goal.append(elem)
        count += 1
    final_goal.append(current_goal)
    return Puzzle(final_goal)


def execute_function():
    num = input("Enter number of tiles.: ")
    pos = int(input("Enter final position of empty tile: "))
    count_of_rows = int(sqrt(int(num) + 1))
    puzzle_tiles = []
    for i in range(0, count_of_rows):
        current_row = input("Enter numbers in row with white space betwen them: ")
        puzzle_tiles.append([int(elem) for elem in current_row.split(' ')])
    coordinates_of_zero = find_zero_coordinates(Puzzle(puzzle_tiles))
    initial_board = Puzzle(puzzle_tiles, coordinates_of_zero)
    final_board = create_goal(initial_board, int(num), pos)
    goal = False
    final = ida_algorithm_using(initial_board, final_board, goal)
    final.represent_puzzle()
    direction = get_all_directions(initial_board, final)
    print('--------------------')
    for i in direction:
        print(i)


if __name__ == "__main__":
    execute_function()