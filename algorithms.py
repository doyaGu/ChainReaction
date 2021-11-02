import sys
sys.setrecursionlimit(4000)  # set the maximum depth as 4000


def newBorad(n, m):
    return [[[0, 0] for i in range(m)] for j in range(n)]


def index(coordinate, board):
    return board[coordinate[1]][coordinate[0]]


def isInBoard(n, m, i, j):
    return 0 <= i < m and 0 <= j < n


def possible(gameBoard, n, m, i, j, player):
    current_cell = index((i, j), gameBoard)
    return isInBoard(n, m, i, j) and current_cell[0] in (0, player)


def adjacentCells(n, m, i, j):
    xs, ys = (i - 1, i + 1, i, i), (j, j, j - 1, j + 1)
    for i in range(4):
        if isInBoard(n, m, xs[i], ys[i]):
            yield xs[i], ys[i]


def cellMaximum(i, j, n, m):
    if i == 0 or i == m - 1 or j == 0 or j == n - 1:  # sides
        return 3
    xy = (i, j)
    if xy == (0, 0) or xy == (0, n - 1) or xy == (m - 1, 0) or xy == (m - 1, n - 1):  # corners
        return 2
    else:  # center
        return 4


def put(gameBoard, n, m, i, j, player):
    cell_max = cellMaximum(i, j, n, m)
    gameBoard[j][i][0] = player
    if index((i, j), gameBoard)[1] + 1 <= cell_max:
        gameBoard[j][i][1] += 1
    if index((i, j), gameBoard)[1] == cell_max:
        gameBoard[j][i] = [0, 0]
        for x, y in adjacentCells(n, m, i, j):
            put(gameBoard, n, m, x, y, player)


def getExists(gameBoard, n, m):
    board_index = [(x, y) for y in range(n) for x in range(m)]
    return set(map(lambda cells: gameBoard[cells[1]][cells[0]][0], board_index))


def someone_loose(gameBoard, n, m, players):
    exists = getExists(gameBoard, n, m)
    someone = exists.symmetric_difference(set(players))
    if 0 in someone:
        someone.remove(0)
    if someone:
        return someone.pop()
    else:
        return False


def loose(gameBoard, n, m, player):
    exists = getExists(gameBoard, n, m)
    return player not in exists


def win(gameBoard, n, m, player):
    exists = getExists(gameBoard, n, m)
    return exists == {player, 0}
