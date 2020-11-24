import random


def create_board(count_of_queens, coordinates):
    board = [['_' for row in range(0, count_of_queens)] for i in range(count_of_queens)]
    for i in range(len(coordinates)):
        board[coordinates[i]][i] = '*'
    return board


def print_board(board):
    for row in board:
        print(row)


def set_random_queens(count_of_queens):
    used_row = []
    i = count_of_queens
    x = 0
    while i > 0:
        y = random.randint(0, count_of_queens - 1)
        if y not in used_row:
            used_row.append(y)
            x = x + 1
            i = i - 1
    return used_row


def find_conflicts_of_all_queens(coordinates, count_of_queens):
    dict_of_conflicts = []
    for i  in range(count_of_queens):
        all_conflicts = find_all_conflicts(coordinates, coordinates[i], i, count_of_queens)
        dict_of_conflicts.append(all_conflicts)
    return dict_of_conflicts


def find_all_conflicts(coordinates, current_queen_row, current_queen_column, count_of_queens):
    conflicts_count = 0
    for i in range(count_of_queens):
        if current_queen_column != i and current_queen_row == coordinates[i]:
            conflicts_count += 1
        elif current_queen_column != i and current_queen_row + current_queen_column == i + coordinates[i]:
            conflicts_count += 1
        elif current_queen_column != i and current_queen_row - current_queen_column == coordinates[i] - i:
            conflicts_count += 1
    return conflicts_count


def find_row_with_mimimum_coflicts(coordinates, count_of_queens):
    current_coordinates = [i for i in range(count_of_queens) if coordinates[i] == min(coordinates)]
    return random.choice(current_coordinates)


def find_queen_with_max_conflicts(coordinates, count_of_queens):
    current_coordinates = [i for i in range(count_of_queens) if coordinates[i] == max(coordinates)]
    return random.choice(current_coordinates)


def is_solved(list_of_conflicts):
    return sum(list_of_conflicts) == 0


def Solver(coordinates, count_of_queens, iters=10000):
    find_cordinates = coordinates
    for k in range(iters):
        dict_of_conflicts = find_conflicts_of_all_queens(coordinates, count_of_queens)
        if is_solved(dict_of_conflicts):
            return find_cordinates
        current_queen_column = find_queen_with_max_conflicts(dict_of_conflicts, count_of_queens)
        new_dict_of_conflicts = [find_all_conflicts(coordinates, current_queen_row, current_queen_column, count_of_queens) for current_queen_row in range(count_of_queens)]
        coordinates[current_queen_column] = find_row_with_mimimum_coflicts(new_dict_of_conflicts, count_of_queens)
        find_cordinates = coordinates


if __name__ == '__main__':
    count_of_queens = int(input('Input number of queens: '))
    while (count_of_queens == 2 or count_of_queens == 3):
        count_of_queens = int(input('Please input count different from 2 and 3: '))
    coordinates = set_random_queens(count_of_queens)
    board = create_board(count_of_queens, coordinates)
    print_board(board)
    print('-----')
    coordinate = Solver(coordinates, count_of_queens)
    board = create_board(count_of_queens, coordinate)
    print_board(board)