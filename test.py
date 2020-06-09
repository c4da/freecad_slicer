import numpy as np
import data_eval as de


def formatPositions(positions, savePath):
    """
    kvuli pootoceni globalniho SS z inventoru do SS makety je:
    x_Maketa == -z (hodnoty jsou jiz kladne z predchozi operace)
    z_Maketa == -x (hodnoty jsou jiz kladne z predchozi operace)
    :param positions:
    :param savePath:
    :return:
    """
    # x1;y1(x1, z1),y2(x1, z2),y3(x1, z3)
    # x2;y1(x2, z1),y2(x2, z2),y3(x2, z3)
    lines = dict()
    for pos in positions:

        if pos[2] not in lines:
            lines[pos[2]] = list()
            lines[pos[2]].append(pos)
        else:
            lines[pos[2]].append(pos)

    levels = list(lines.keys())
    # App.Console.PrintMessage(("\n levels " + str(levels)))
    levels.sort()
    f = open(savePath + 'saved_data_format_test.txt', 'w')

    for i in range(len(lines[levels[0]])):
        f.write(str(round(lines[levels[0]][i][0], 2)))
        f.write('; ')

        for j, level in enumerate(levels):
            f.write(str(round(lines[level][i][1], 2)))
            if j < len(levels) - 1:
                f.write(', ')

        f.write('\n')

    f.close()

    return 0


if __name__ == "__main__":

    fileName = '/home/cada/python3/freecad/saved_data.txt'

    data = []

    f = open(fileName, 'r')
    text = f.readlines()
    for line in text:

        data_line = line.strip().replace(' ', '').split(';')
        if len(data_line) == 3:
            data_line = [float(x) for x in data_line]
            data += [data_line]

    data = np.array(data)

    print(data)

    formatPositions(data, '/home/cada/python3/freecad/')
