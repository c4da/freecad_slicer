import numpy as np


def sort_it(fileName, sequence):
    data = []

    f = open(fileName, 'r')
    text = f.readlines()
    for line in text:
        data_line0 = line.strip().replace(' ', '').split(';')
        data_line1 = data_line0[1].replace(' ', '').split(',')

        data_line0 = [float(data_line0[0])]
        data_line1 = [float(x) for x in data_line1]

        data_line = data_line0 + data_line1
        data.append(data_line)

    data = np.array(data)

    origin = np.arange(0, len(data[0, :]), 1)
    for m, n in zip(sequence, origin):
        print(m, n)
        temp = data[:, m].copy()
        data[:, m] = data[:, n]
        data[:, n] = temp

    fileName = fileName.split('.txt')
    f2 = open(fileName[0]+'_seq.txt', 'w')

    for line in data:
        line = (str(line[0]) + ';' + str(line[1:]) + '\n').replace("'", '').replace('[', '').replace(']', '')
        f2.write(line)
    f2.close()

if __name__ == "__main__":

    file = '/home/cada/python3/freecad/saved_data_format.txt'

    # 350.0;49.36261338865444, 34.54760469549561, 55.54760469549561


    keys = [0, 2]
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
