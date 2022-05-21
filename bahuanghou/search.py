import numpy as np
import random
import copy
import math


#碰撞计算
def collision(seq):
    mun = 0
    for i in range(0, 8):
        x = seq[i]
        for j in range(i + 1, 8):
            y = seq[j]
            if y - x == j - i or y - x == i - j:
                mun += 1
            if x == y:
                mun += 1
    return mun

#绘图
def draw(seq):
    board = np.array([0] * 81)
    board = board.reshape(9, 9)
    for i in range(1, 9):
        board[seq[i - 1]][i] = 1
    print('对应棋盘如下:')
    for i in board[1:]:
        for j in i[1:]:
            print(j, ' ', end="")
        print()

#爬山算法
def climb(seq):
    while True:
        attack = []
        dicts = []
        count = 0
        for tmp in seq:
            for i in list(range(tmp)) + list(range(tmp+1, 8)):
                seqs_tmp = list(seq)
                seqs_tmp[count] = i
                n = collision(seqs_tmp)
                attack.append(n)
                dicts.append({'seq': seqs_tmp, 'attack': n})
            count = count + 1
            if count == 8:
                break
        mins = min(attack)
        current = collision(seq)
        if mins >= current:  # 跳出
            break
        reqs = []
        for j in dicts:
            if j['attack'] == mins:
                reqs.append(j['seq'])
        seq = random.choice(reqs)
    return seq

#随机重启爬山算法
def randomclimb():
    while True:
        seqs = []
        for i in range(0, 8):
            seqs.append(random.randint(0, 7))
        seqs = climb(seqs)
        a = collision(seqs)
        if a == 0: break
    return seqs



def random_adjust(seq):
    temp = copy.deepcopy(seq)
    x = random.randint(0, 7)
    y = temp[x]
    if y < 6 and y > 1:
        y = random.randint((y - 2), (y + 2))
    elif y == 6:
        y = random.randint((y - 2), (y + 1))
    elif y == 1:
        y = random.randint((y - 1), (y + 2))
    elif y == 7:
        y = random.randint((y - 1), y)
    elif y == 0:
        y = random.randint(y, (y + 1))
    temp[x] = y
    return temp


def tuihuo(T, mins, r, L):
    seq = []
    for i in range(0, 8):
        seq.append(random.randint(0, 7))
    while T > mins:
        for i in range(L):
            weight = collision(seq)
            if weight == 0:  # 碰撞度为0，跳出
                print(seq, collision(seq))
                draw(seq)
                return True
            new_seq = random_adjust(seq)
            new_weight = collision(new_seq)
            if new_weight <= weight:
                seq = new_seq
            else:
                if random.random() < math.exp((weight - new_weight) / T):
                    seq = new_seq
        T = T * r

def tuihuo_test(T, mins, r, L, num):
    for i in range(num):
        if tuihuo(T, mins, r, L):
            break
    if i < (num-1):
        print('成功')
    else:
        print('失败')



# seq = [5,6,7,4,5,6,7,6]
# print(climb(seq),collision(climb(seq)))
# draw(climb(seq))
# print(randomclimb(),collision(randomclimb()))
# draw(randomclimb())
tuihuo_test(5, 0.001, 0.9, 10, 100)
