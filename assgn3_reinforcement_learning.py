import sys
from collections import defaultdict
import random


def run(n_dice, n_sides, l_target, u_target, m, n_games):
    win_count = defaultdict(int)
    lose_count = defaultdict(int)

    for game_no in range(0, n_games):
        scores = [(0, 0, -1)]
        turn = 0
        while True:
            if turn == 0:
                x, y, z = scores[-1]
            else:
                y, x, z = scores[-1]

            f = [0.0]
            for j in range(1, n_dice+1):
                denominator = win_count[(x, y, j)] + lose_count[(x, y, j)]
                if denominator == 0:
                    f.append(0.5)
                else:
                    f.append(float(win_count[(x, y, j)])/float(denominator))

            max_f = 0.0
            b = -1
            for i in range(1, n_dice+1):
                freq = f[i]
                if freq > max_f:
                    max_f = freq
                    b = i

            g = 0.0
            for i in range(1, n_dice+1):
                if i == b:
                    continue
                g += f[i]

            t = 0

            for j in range(0, n_dice+1):
                t += win_count[(x, y, j)] + lose_count[(x, y, j)]

            t = float(t)
            p = [0.0]

            pb = float(((t*f[b])+m))/float((t*f[b])+(n_dice*m))
            for j in range(1, n_dice + 1):
                if j == b:
                    p.append(pb)

                else:

                    p1 = ((1-pb) * float((t*f[j])+m))/float((g*t)+((n_dice-1)*m))
                    p.append(p1)

            u = [0.0]
            for j in range(1, n_dice + 1):
                prev = u[-1]
                u.append(prev+p[j])

            i = random.uniform(0, 1)
            n_dice_to_roll = None
            for j in range(1, n_dice + 1):
                if i < u[j]:
                    n_dice_to_roll = j
                    break

            if turn == 0:
                scores[-1] = (x, y, n_dice_to_roll)

            else:
                scores[-1] = (y, x, n_dice_to_roll)

            score_this_turn = 0
            for i in range(0, n_dice_to_roll):
                score_this_turn += random.randint(1, n_sides)

            x += score_this_turn

            if x > u_target:
                if turn == 0:
                    win = 1
                else:
                    win = 0

                break

            elif x >= l_target:
                if turn == 0:
                    win = 0

                else:
                    win = 1

                break

            else:
                if turn == 0:
                    scores.append((x, y, -1))
                    turn = 1
                else:
                    scores.append((y, x, -1))
                    turn = 0

        if win == 0:
            for i in range(0, len(scores)):
                x, y, j = scores[i]
                if i % 2 == 0:
                    win_count[(x, y, j)] += 1
                else:
                    lose_count[(y, x, j)] += 1

        else:
            for i in range(0, len(scores)):
                x, y, j = scores[i]
                if i % 2 == 0:
                    lose_count[(x, y, j)] += 1
                else:
                    win_count[(y, x, j)] += 1

    correct_dice = []
    probabilities = []
    for x in range(0, l_target):
        correct_dice1 = []
        probabilities1 = []
        for y in range(0, l_target):
            correct_dice1.append(0.0)
            probabilities1.append(0.0)
        correct_dice.append(correct_dice1)
        probabilities.append(probabilities1)

    for x in range(0, l_target):
        for y in range(0, l_target):
            if y == 0:
                if x != 0:
                    correct_dice[x][y] = 0
                    probabilities[x][y] = 0
                    continue

            f = [0.0]
            for j in range(1, n_dice+1):
                denominator = win_count[(x, y, j)] + lose_count[(x, y, j)]
                if denominator == 0:
                    f.append(0.5)
                else:
                    f.append(float(win_count[(x, y, j)])/float(denominator))

            max_f = 0
            b = 1
            for i in range(1, n_dice+1):
                freq = f[i]
                if freq > max_f:
                    max_f = freq
                    b = i

            correct_dice[x][y] = b
            denominator = win_count[(x, y, b)] + lose_count[(x, y, b)]
            if denominator == 0:
                probabilities[x][y] = -1
            else:
                probabilities[x][y] = float(win_count[(x, y, b)])/float(denominator)

    for x in range(0, l_target):
        s = ""
        for y in range(0, l_target):
            s += str(correct_dice[x][y]) + "  "

        print(s)

    print('\n')

    for x in range(0, l_target):
        s = ""
        for y in range(0, l_target):
            s += "{:.4f}".format(probabilities[x][y]) + " "

        print(s)

    return correct_dice, probabilities


if __name__ == '__main__':
    args = sys.argv
    ndice = int(args[1])
    nsides = int(args[2])
    ltarget = int(args[3])
    utarget = int(args[4])
    m = int(args[5])
    ngames= int(args[6])
    run(ndice, nsides, ltarget, utarget, m, ngames)
