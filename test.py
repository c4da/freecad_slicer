import numpy as np
import data_eval as de

def interpolate_data(positions):

    interp_start_x = None
    interp_end_x = None

    dataPlane = dict()
    dataPlaneInterp = dict()


    for pos in positions:
        if pos[2] not in dataPlane:
            dataPlane[pos[2]] = list()
            dataPlane[pos[2]].append(pos)
        else:
            dataPlane[pos[2]].append(pos)

    levels = list(dataPlane.keys())

    for level in levels:
        section = np.array(dataPlane[level])

        for i, point in enumerate(section):
            if not np.isnan(point[1]) and interp_start_x == None:
                interp_start_x = i
                continue

            if np.isnan(point[1]) and interp_start_x != None and interp_end_x == None:
                interp_end_x = i - 1
                break

        print(level, interp_start_x, interp_end_x)
        if interp_end_x == None and interp_start_x == None:
            del dataPlane[level]
            continue

        x_eval = np.arange(section[interp_start_x, 0], section[interp_end_x, 0], 0.1)
        x = section[interp_start_x:interp_end_x, 0]
        y = section[interp_start_x:interp_end_x, 1]
        y_interp = de.getLinInterp(x_eval, x, y)
        z = np.ones((1, len(x_eval))) * section[0, 2]

        dataPlane[level] = np.array([x_eval, y_interp])

        f = open('/home/cada/python3/freecad/saved_data_format_interp_'+str(level)+'.txt', 'w')

        for i in range(len(x_eval)):
            line = str(round(x_eval[i], 1)) + '; ' + str(round(y_interp[i], 4)) +'\n'
            f.write(line)

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
            data +=[data_line]


    data = np.array(data)

    print(data)

    interpolate_data(data)