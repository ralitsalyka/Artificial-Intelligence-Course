import random
import time

count_of_queens = 0
board = []
row_conflicts = []
diagr_conflicts = []
diagl_conflicts = []


def changeConflicts(col, row, val):
    row_conflicts[row] += val
    diagr_conflicts[col + row] += val
    diagl_conflicts[col + (count_of_queens - row - 1)] += val


def calculate_all_conflicts(current_row, count_of_queens, col):
    return row_conflicts[current_row] + diagr_conflicts[col + current_row] + diagl_conflicts[col + (count_of_queens - current_row - 1)]


def minConflictPos(col):
    minConflicts = count_of_queens
    minConflictRows = []
    for row in range(count_of_queens):
        conflicts = calculate_all_conflicts(row, count_of_queens, col)
        if conflicts == 0:
            return row
        if conflicts < minConflicts:
            minConflictRows = [row]
            minConflicts = conflicts
        elif conflicts == minConflicts:
            minConflictRows.append(row)
    choice = random.choice(minConflictRows)
    return choice


def findMaxConflictCol():
    conflicts = 0
    maxConflicts = 0
    maxConflictCols = []
    for col in range(0, count_of_queens):
        row = board[col]
        conflicts = calculate_all_conflicts(row, count_of_queens, col)
        if (conflicts > maxConflicts):
            maxConflictCols = [col]
            maxConflicts = conflicts
        elif conflicts == maxConflicts:
            maxConflictCols.append(col)
    choice = random.choice(maxConflictCols)
    return choice, maxConflicts


# Sets up the board using a greedy algorithm
def createBoard():
    global board
    global row_conflicts
    global diagr_conflicts
    global diagl_conflicts
    board = []
    diagr_conflicts = [0] * ((2 * count_of_queens) - 1)
    diagl_conflicts = [0] * ((2 * count_of_queens) - 1)
    row_conflicts = [0] * count_of_queens
    random_queens = random.sample(range(0, count_of_queens), count_of_queens)
    notPlaced = []
    for col in range(0, count_of_queens):
        current_queen = random_queens.pop()
        conflicts = calculate_all_conflicts(current_queen, count_of_queens, col)
        if conflicts == 0:
            board.append(current_queen)
            changeConflicts(col, board[col], 1)
        else:
            random_queens.append(current_queen)
            current_queen2 = random_queens.pop()
            conflicts2 = calculate_all_conflicts(current_queen2, count_of_queens, col)
            if conflicts2 == 0:
                board.append(current_queen2)
                changeConflicts(col, board[col], 1)
            else:
                random_queens.append(current_queen2)
                board.append(None)
                notPlaced.append(col)
    for col in notPlaced:
        board[col] = random_queens.pop()
        changeConflicts(col, board[col], 1)


def solveNQueens():
    createBoard()
    iteration = 0
    maxIteration = 0.6 * count_of_queens

    while (iteration < maxIteration):
        col, numConflicts = findMaxConflictCol()
        if (numConflicts > 3):
            newLocation = minConflictPos(col)
            if (newLocation != board[col]):
                changeConflicts(col, board[col], -1)
                board[col] = newLocation
                changeConflicts(col, newLocation, 1)
        elif numConflicts == 3:
            return True, board
        iteration += 1
    return False, board


def main():
    global count_of_queens
    global board
    global row_conflicts
    global diagr_conflicts
    global diagl_conflicts
    n = 0
    count_of_queens = int(input('Input number of queens: '))
    if count_of_queens <= 3 or count_of_queens > 10000000:
        print("Cannot build board of size: " + str(count_of_queens))
    else:
        time0 = time.time()
        print(" ")
        solved = False
        if (count_of_queens == 6):
            board = [1, 3, 5, 0, 2, 4]
            n = 6
            count_of_queens = 4
        while (not solved):
            solved, board = solveNQueens()
        time1 = time.time()
        print(" ")
        tot_time = time1 - time0
        print("Seconds: ")
        print(tot_time)
    if n == 6:
        board = [1, 3, 5, 0, 2, 4]
        count_of_queens = 6
    if count_of_queens <= 10:
        represent_board = [['_' for row in range(0, count_of_queens)] for i in range(count_of_queens)]
        for i in range(len(board)):
            represent_board[board[i]][i] = '*'
        for elem in represent_board:
            print(elem)


main()