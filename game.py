from assgn3_reinforcement_learning import run


def play(correct_dice, l_target, u_target, ):
    x = 0
    y = 0
    turn = 0
    print('\n\n\nScore: You - %s, Computer - %s' % (y, x))
    while True:
        if turn == 0:
            dice_to_roll = correct_dice[x][y]
            print('\nRoll %s dice for the computer.' % dice_to_roll)
            x += int(input('Enter score rolled: '))
            print('Score: You - %s, Computer - %s' % (y, x))
            if x > u_target:
                print('You won!')
                break

            elif x >= l_target:
                print('The computer won!')
                break

            else:
                turn = 1

        else:
            print('\n Your turn. You can roll a maximum of %s dice' % ndice)
            y += int(input('Enter score rolled: '))
            print('Score: You - %s, Computer - %s' % (y, x))
            if y > u_target:
                print('The computer won!')
                break

            elif y >= l_target:
                print('You won!')
                break

            else:
                turn = 0


if __name__=='__main__':
    ndice = int(input('Enter maximum number of die that can be rolled in a turn: '))
    nsides = 6
    ltarget = int(input('Enter the lowest winning score: '))
    utarget = int(input('Enter the highest winning score: '))
    m = 100
    ngames = 100000
    correctdice, probabilities = run(ndice, nsides, ltarget, utarget, m, ngames)
    play(correctdice, ltarget, utarget)
