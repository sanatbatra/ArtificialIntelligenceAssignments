import pandas as pd
import sys
from collections import defaultdict
import math


def read_data():
    df = pd.read_excel(r'./prog4Data.xlsx')
    data = df.to_dict('records')
    return data


def train_naive_bayes(train_data, train_size):

    count = defaultdict(int)
    count_a6 = defaultdict(int)

    for instance in train_data:
        count_a6[instance['a6']] += 1
        for i in range(1,6):
            a_str = 'a' + str(i)
            count[(i, instance[a_str], instance['a6'])] += 1

    lp_a6 = {}
    lp = {}
    for i in range(1,4):
        lp_a6[i] = -1 * math.log(float(count_a6[i] + 0.1) / float(train_size + 0.3), 2)

    for attrib_no in range(1,6):
        for attrib_val in range(1,5):
            for a6_val in range(1,4):
                lp[(attrib_no, attrib_val, a6_val)] = -1 * math.log(float(count[(attrib_no, attrib_val, a6_val)] + 0.1) /
                                                                    float(count_a6[a6_val] + 0.4), 2)

    return lp, lp_a6


def test_naive_bayes(test_data, test_size, lp, lp_a6):
    correct = 0
    total_actual_a6_3 = 0
    correct_a6_3 = 0
    total_pred_a6_3 = 0
    for instance in test_data:
        sum = [lp_a6[1], lp_a6[2], lp_a6[3]]
        for a6_val in range(1, 4):
            for attrib_no in range(1, 6):
                sum[a6_val-1] += lp[(attrib_no, instance['a'+str(attrib_no)], a6_val)]

        prediction = sum.index(min(sum)) + 1
        if prediction == instance['a6']:
            correct += 1

        if prediction == 3:
            total_pred_a6_3 += 1

        if instance['a6'] == 3:
            total_actual_a6_3 += 1
            if prediction == 3:
                correct_a6_3 += 1

    accuracy = '{:.4f}'.format(float(correct)/float(test_size))
    if total_pred_a6_3 == 0:
        precision = '0/0'
    else:
        precision = '{:.4f}'.format(float(correct_a6_3)/float(total_pred_a6_3))
    if total_actual_a6_3 == 0:
        recall = '0/0'
    else:
        recall = '{:.4f}'.format(float(correct_a6_3)/float(total_actual_a6_3))
    print('Accuracy = %s   Precision = %s    Recall = %s' % (accuracy, precision, recall))


def print_lp(lp, lp_a6):
    print('{:.4f}'.format(lp_a6[1]) + '   {:.4f}'.format(lp_a6[2]) + '    {:.4f}'.format(lp_a6[3]))
    for attrib_no in range(1, 6):
        print('\n')
        for a6_val in range(1,4):
            print('{:.4f}'.format(lp[(attrib_no, 1, a6_val)]) + '   {:.4f}'.format(lp[(attrib_no, 2, a6_val)]) +
                  '    {:.4f}'.format(lp[(attrib_no, 3, a6_val)]) + '    {:.4f}'.format(lp[(attrib_no, 4, a6_val)]))

    print('\n')


if __name__ == '__main__':
    data = read_data()
    args = sys.argv
    train_size = int(args[1])
    test_size = int(args[2])
    print_verbose = False
    if len(args) > 3:
        if args[3] != '-v':
            print('Wrong input_assignment2! Use "-v" instead')
            exit()
        else:
            print_verbose = True

    train_data = data[:train_size]
    test_data = data[-test_size:]
    lp, lp_a6 = train_naive_bayes(train_data, train_size)
    if print_verbose:
        print_lp(lp, lp_a6)
    test_naive_bayes(test_data, test_size, lp, lp_a6)
