"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    black = 0
    white = 0
    for tmp in board:
        for i in tmp:
            if i == X: black += 1
            if i == O: white += 1
    if black <= white: return X
    else: return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = []
    i = 0
    j = 0
    for tmp in board:
        for x in tmp:
            if x == None: action.append((i, j))
            j += 1
        i += 1
        j = 0
    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    uesr = player(board)
    i = action[0]
    j = action[1]
    if uesr == X:
        board[i][j] = X
    if uesr == O:
        board[i][j] = O
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for tmp in board:
        if tmp[0] == tmp[1] == tmp[2] == X:
            return X
        if tmp[0] == tmp[1] == tmp[2] == O:
            return O
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == X:
            return X
        if board[0][i] == board[1][i] == board[2][i] == O:
            return O
    if board[0][0] == board[1][1] == board[2][2] == X:
        return X
    if board[0][0] == board[1][1] == board[2][2] == O:
        return O
    if board[2][0] == board[1][1] == board[0][2] == X:
        return X
    if board[0][0] == board[1][1] == board[2][2] == O:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for tmp in board:
        if tmp[0] == tmp[1] == tmp[2] == X or tmp[0] == tmp[1] == tmp[2] == O:
            return True
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == X or board[0][i] == board[1][i] == board[2][i] == O:
            return True
    if board[0][0] == board[1][1] == board[2][2] == X or board[0][0] == board[1][1] == board[2][2] == O:
        return True
    if board[2][0] == board[1][1] == board[0][2] == X or board[0][0] == board[1][1] == board[2][2] == O:
        return True
    num = 0
    for tmp in board:
        for i in tmp:
            if i == None: num += 1
    if num == 0: return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X: return 1.0
    if win == O: return -1.0
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    num = 0
    for tmp in board:
        for i in tmp:
            if i == None: continue
            num += 1
    if num == 0: return (1, 1)
    user = player(board)
    if user == O:
        acts = actions(board)
        v = 255
        act = (1, 1)
        for action in acts:
            b = copy.deepcopy(board)
            z = maxvalue(result(b, action))
            if z < v:
                v = z
                act = action
        # print(v)
        return act
    if user == X:
        acts = actions(board)
        v = -255
        act = (1, 1)
        for action in acts:
            b = copy.deepcopy(board)
            z = minvalue(result(b, action))
            if z > v:
                v = z
                act = action
        # print(v)
        return act


def minvalue(board):
    if terminal(board):
        return utility(board)
    v = 255
    for action in actions(board):
        b = copy.deepcopy(board)
        v = min(v, (maxvalue(result(b, action)) * 0.8))
    return v


def maxvalue(board):
    if terminal(board):
        return utility(board)
    v = -255
    for action in actions(board):
        b = copy.deepcopy(board)
        v = max(v, (minvalue(result(b, action)) * 0.8))
    return v

# board = [[O, O, EMPTY],[X, X, EMPTY],[EMPTY, EMPTY, EMPTY]]
#
# print(maxvalue(board))
# print(board)

