import numpy as np


def sort_it(fileName, sequence):
    data = []

    f = open(fileName, 'r')
    text = f.readlines()
    for line in text:
        # 0.0;0.0, 0.0, 0.0,
        data_line0 = line.strip().replace(' ', '').split(';')
        data_line1 = data_line0[1].replace(' ', '').split(',')

        data_line0 = [float(data_line0[0])]
        data_line1 = [float(x) for x in data_line1]

        data_line = data_line0 + data_line1
        data.append(data_line)

    data_all = np.array(data)
    data = data_all[:, 1:].copy()
    data_base = data_all[:, 1:].copy()

    origin = np.arange(0, len(data[0, :]), 1)
    sequenceCheck = []
    for m, n in zip(sequence, origin):
        # print(m, n)
        if m == n:
            # print(True)
            continue

        else:
            print('swapping: ', m, n)
            sequenceCheck.append([m, n])
            sequenceCheck.append([n, m])
            # temp = data_base[:, m].copy()
            data[:, m] = data_base[:, n].copy()
            # data[:, n] = temp

    fileName = fileName.split('.txt')
    f2 = open(fileName[0]+'_seq.txt', 'w')
    print(data_all[3198, 1:], data[3198, :])

    for j, y_line in enumerate(data):
        x_line = (str(data_all[j, 0]) + ';')
        f2.write(x_line)
        for i, item in enumerate(y_line):
            f2.write(str(item))
            if i < len(y_line[1:]):
                f2.write(',')
            else:
                f2.write('\n')
        # + str(line[1:]) + '\n').replace("'", '').replace('[', '').replace(']', '')
        # f2.write(line)
    f2.close()

if __name__ == "__main__":

    file = '/home/cada/python3/freecad/saved_data_format_interp.txt'

    # 350.0;49.36261338865444, 34.54760469549561, 55.54760469549561


    keys = [0, 3, 2, 1]
    sort_it(file, keys)

    # data = []
    #
    # f = open(file, 'r')
    # text = f.readlines()
    # for line in text:
    #     data_line0 = line.strip().replace(' ', '').split(';')
    #     data_line1 = data_line0[1].replace(' ', '').split(',')
    #
    #     data_line0 = [float(data_line0[0])]
    #     data_line1 = [float(x) for x in data_line1]
    #
    #     data_line = data_line0 + data_line1
    #     data.append(data_line)
    #
    # data = np.array(data)
    #
    # print(data[5, :])
    # origin = np.arange(0, len(data[0, :]), 1)
    # for m, n in zip(keys, origin):
    #     temp = data[:, m].copy()
    #     data[:, m] = data[:, n]
    #     data[:, n] = temp
    #
    # print(data[5, :])
