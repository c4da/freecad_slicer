
import numpy as np
import matplotlib.pyplot as plt
# from scipy.interpolate import UnivariateSpline

def getData(file):
    f = open(file, 'r')
    lines = f.readlines()
    data = []
    for line in lines:
        line = line.replace(' ', '').split(';')
        if 'nan' in line[1]:
            line[1] = 0
        data.append([float(line[0]), float(line[1])])
    data = np.array(data)
    data = data.reshape(len(lines), 2)
    return data

def getDifferences(data1, data2):

    diff = data1-data2
    res = diff[:,1]
    # res = res.reshape(len(diff[:,0]), 2)
    # print(np.shape(res))
    return res

def getLinInterp(x_eval, x, y):
    fp = y
    xp = x
    yinterp = np.interp(x_eval, xp, fp, left=None, right=None, period=None)
    return yinterp

if __name__ == '__main__':
    data01 = getData('D:\\Python3\\freecad_slicer\\presnost01\\saved_data_format.txt')
    data001 = getData('D:\\Python3\\freecad_slicer\\presnost001\\saved_data_format.txt')
    data0001 = getData('D:\\Python3\\freecad_slicer\\presnost0001\\saved_data_format.txt')

    diff01_0001 = getDifferences(data01, data0001)
    diff001_0001 = getDifferences(data001, data0001)
    fig = plt.Figure
    plt.plot(data01[:,0], diff01_0001, label = 'diff 01 - 0001')
    plt.plot(data01[:,0], diff001_0001, label = 'diff 001 - 0001')
    plt.legend()
    plt.show()

