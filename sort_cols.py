import numpy as np


def sort_it(fileName, sequence):
    data = []

    f = open(fileName, 'r')
    text = f.readlines()
    for line in text:
        # 0.0;0.0, 0.0, 0.0,
        data_line0 = line.strip().replace(' ', '').split(';')
        data_line1 = data_line0[1].replace(' ', '').split(',')

        data_line0 = [str(data_line0[0])]
        data_line1 = [str(x) for x in data_line1]
        konst = [str(123)]

        data_line = konst + data_line0 + data_line1

        data.append(data_line)

    data_all = np.array(data)
    # print(data_all[10,:])
    data = data_all[:, 2:].copy()
    data_base = data_all[:, 2:].copy()

    origin = np.arange(0, len(data[0, :]), 1)
    sequenceCheck = []
    for m, n in zip(sequence[:len(data[0, :])], origin):
        # print(m, n)
        if m == n:
            # print(True)
            continue

        elif m < origin[-1]:
            print('swapping: ', m, n)
            sequenceCheck.append([m, n])
            sequenceCheck.append([n, m])
            # temp = data_base[:, m].copy()
            data[:, m] = data_base[:, n].copy()
            # data[:, n] = temp

    fileName = fileName.split('.txt')
    f2 = open(fileName[0]+'_seq.txt', 'w')
    # print(data_all[3198, 1:], data[3198, :])

    for j, y_line in enumerate(data):
        x_line = (str(data_all[j, 0]) + ';')
        x_line2 = (str(data_all[j, 1]) + ';')
        line = x_line+x_line2
        f2.write(line.replace('.',','))

        for i, item in enumerate(y_line):
            f2.write(str(item).replace('.',','))
            if i < len(y_line[1:]):
                f2.write(';')
            else:
                f2.write('\n')
        # + str(line[1:]) + '\n').replace("'", '').replace('[', '').replace(']', '')
        # f2.write(line)
    f2.close()

if __name__ == "__main__":

    file = 'C:\\cada\\freecad_slicer\\saved_data_format_interp.txt'

    # 350.0;49.36261338865444, 34.54760469549561, 55.54760469549561


    keys = [1,3]
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
