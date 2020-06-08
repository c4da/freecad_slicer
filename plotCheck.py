import FreeCAD as App
import numpy as np
import matplotlib.pyplot as plt


def plotGraph(x, y, xname, yname, title, PATH):
    """
    function plots and saves a graph
    :param x:
    :param y:
    :param xname:
    :param yname:
    :param title:
    :return:
    """
    fig = plt.figure()
    plt.title(title)
    plt.xlabel(xname)
    plt.ylabel(yname)

    x = [float(x_) for x_ in x]
    y = [float(y_) for y_ in y]
    x = [0 if np.isnan(x_) else x_ for x_ in x]
    y = [0 if np.isnan(y_) else y_ for y_ in y]


    plt.xticks(np.linspace(min(x), max(x), 10))
    plt.yticks(np.linspace(min(y), max(y), 10))
    # plt.axis('equal')

    # App.Console.PrintMessage('\n')
    # App.Console.PrintMessage('****************************** \n')
    # App.Console.PrintMessage('\n')
    # App.Console.PrintMessage('plotting \n')
    # App.Console.PrintMessage(x)
    # App.Console.PrintMessage(y)
    # App.Console.PrintMessage('\n')

    plt.plot(x, y)
    plt.grid(True)
    # plt.ticklabel_format(axis="y", style="plain", useOffset=False)
    # plt.show(block=False)
    plt.ioff()
    fig.savefig(PATH+title + '_graph.png')
    plt.close(fig)
    return 0


def processData(data):
    return np.array(data)


def makePlots(dataIn, path, name = ''):
    data = processData(dataIn)
    # print(data)

    data_x = data[:, 0]
    data_y = data[:, 1]
    data_z = data[:, 2]
    # App.Console.PrintMessage(data_x)
    # App.Console.PrintMessage(data_y)
    # App.Console.PrintMessage(data_z)

    data_y = [0 if np.isnan(x) else x for x in data_y]

    prev_dist = data_z[0]
    # print('in makeplots printing dataz')
    # print(data_z)
    level_index = []
    j = 0
    for i, dist in enumerate(data_z):
        # App.Console.PrintMessage((prev_dist, dist))
        if prev_dist != dist or i == len(data_z)-1:
            level_index.append(i)
            label = str(prev_dist)
            label = label.split('.')
            title = 'c-section_' + str(label[0]) + name
            # App.Console.PrintMessage(title)
            plotGraph(data_x[j:i], data_y[j:i], 'model - long. coord', 'model - height', title, path)
            j = i
            prev_dist = dist

    return 0
