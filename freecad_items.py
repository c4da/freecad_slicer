# -*- coding: utf-8 -*-

# Macro Begin: /home/cada/python3/freecad/rec.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++

import FreeCAD as App
import FreeCADGui as Gui
import ImportGui
from PySide import QtCore, QtGui
import Show

import numpy as np
import os
import plotCheck
import time
import platform
import data_eval as de
import sort_cols


# ---------------------------------------------------------------------------

def movePart(documentName, x=0, y=0, z=0):
    App.getDocument(documentName).Part__Feature.Placement = App.Placement(App.Vector(x, y, z),
                                                                          App.Rotation(App.Vector(0, 0, 0.),
                                                                                       0), App.Vector(0, 0, 0))


# ---------------------------------------------------------------------------

def interpolate_data(positions, savePath):
    interp_start_x = None
    interp_end_x = None

    dataPlane = dict()
    dataInterp = []

    for pos in positions:
        if pos[2] not in dataPlane:
            dataPlane[pos[2]] = list()
            dataPlane[pos[2]].append(pos)
        else:
            dataPlane[pos[2]].append(pos)

    levels = list(dataPlane.keys())

    for level in levels:
        section = np.array(dataPlane[level])
        section[:, 1] = [0 if np.isnan(x) else x for x in section[:, 1]]

        # for i, point in enumerate(section):
        #     if not np.isnan(point[1]) and interp_start_x == None:
        #         interp_start_x = i
        #         continue
        #
        #     if np.isnan(point[1]) and interp_start_x != None and interp_end_x == None:
        #         interp_end_x = i - 1
        #         break
        #
        # print(level, interp_start_x, interp_end_x)
        # if interp_end_x == None and interp_start_x == None:
        #     del dataPlane[level]
        #     continue

        # x_eval = np.arange(section[interp_start_x, 0], section[interp_end_x, 0], 0.1)
        # x = section[interp_start_x:interp_end_x, 0]
        # y = section[interp_start_x:interp_end_x, 1]
        # y_interp = de.getLinInterp(x_eval, x, y)
        # z = np.ones((1, len(x_eval))) * section[0, 2]

        x = section[:, 0]
        # x_eval = np.arange(0.0, section[-1, 0], 0.1)
        x_eval = np.arange(0.0, 1500.0, 0.1)
        y = section[:, 1]
        z = np.ones((1, len(x_eval))) * section[0, 2]
        y_interp = de.getLinInterp(x_eval, x, y)

        # dataPlane[level] = np.array([x_eval, y_interp])

        f = open(savePath + 'saved_data_format_interp_' + str(level) + '.txt', 'w')

        for i in range(len(x_eval)):
            line = str(round(x_eval[i], 1)) + '; ' + str(round(y_interp[i], 4)) + '\n'
            f.write(line)

        f.close()

        # print(x_eval)
        # print(y_interp)
        # print(section)

        for i in range(len(x_eval)):
            dataInterp.append([x_eval[i], y_interp[i], section[0, 2]])

    return dataInterp


# ---------------------------------------------------------------------------

def printMessage(msg):
    pass


# ---------------------------------------------------------------------------

def getObjects(documentName):
    return App.getDocument(documentName).Objects


# ---------------------------------------------------------------------------

def findObjectViaLabel(documentName, label):
    objects = getObjects(documentName)
    for obj in objects:
        App.Console.PrintMessage(obj.Label + '\n')
        if label in obj.Label:
            print('Found object: ', label)
            App.Console.PrintMessage('Found glass object.\n')
            return obj
    print('Glass was not found. Please, check the name of the glass model.\n')
    App.Console.PrintMessage('Glass was not found. Please, check the name of the glass model.\n')
    return 1


# ---------------------------------------------------------------------------

def findObjectViaName(documentName, name):
    objects = getObjects(documentName)
    for obj in objects:
        App.Console.PrintMessage(obj.Name + '\n')
        if name in obj.Name:
            print('Found glass object.')
            App.Console.PrintMessage('Found glass object.\n')
            return obj
    print('Glass was not found. Please, check the name of the glass model.\n')
    App.Console.PrintMessage('Glass was not found. Please, check the name of the glass model.\n')
    return 1


# ---------------------------------------------------------------------------
def findGlassObj(documentName):
    objects = getObjects(documentName)
    # label = 'glass'
    App.Console.PrintMessage('Listing objects:')
    for obj in objects:
        App.Console.PrintMessage(obj.Label + '\n')
        # if label in obj.Label:
        if 'GLASS' in obj.Label.upper() or 'SKLO' in obj.Label.upper():
            print('Found glass object.')
            App.Console.PrintMessage('Found glass object.\n')
            return obj
        # elif label.upper() in obj.Label:
        #     print('Found GLASS object.')
        #     App.Console.PrintMessage('Found GLASS object.\n')
        #     return obj
    print('Glass was not found. Please, check the name of the glass model.\n')
    App.Console.PrintMessage('Glass was not found. Please, check the name of the glass model.\n')
    return 1


# ---------------------------------------------------------------------------
def showOnlyGlassObject(documentName):
    objects = getObjects(documentName)
    for obj in objects:
        # obj.Visibility = False
        if obj.TypeId == 'Part::Feature':
            # obj.Visibility = False
            if 'GLASS' not in obj.Label.upper() and 'SKLO' not in obj.Label.upper():
                App.ActiveDocument.removeObject(obj.Name)
                App.ActiveDocument.recompute()
            else:
                pass


# ---------------------------------------------------------------------------
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

    for level in levels:
        # deleting negative values because of the Hoffset
        negValues = 0
        checkedPos = []
        # lines[level] = [x for x in lines[level] if x >=0 ]
        for pos in lines[level]:
            if pos[0] < 0:
                negValues += 1
            else:
                checkedPos.append(pos)

        checkedPos += [[0, np.nan, level]] * negValues
        lines[level] = checkedPos

    for level in levels:
        # adding zero values because of the positive Hoffset
        # and cutting the values above x = 1500
        i = 0
        # print(lines[level][:20])

        for pos in lines[level]:
            # print(pos)
            if pos[0] > 1500:
                break
            else:
                i += 1
        lines[level] = lines[level][:i]
        if lines[level][0][0] != 0:
            increment = abs(lines[level][1][0] - lines[level][0][0])
            k = int(lines[level][0][0]/increment) + 1
            missing_data = []
            for j in range(k):
                missing_data.append([j*increment, np.nan, level])

            lines[level] = missing_data + lines[level]
        print(len(lines[level]))
        print(lines[level][0], lines[level][-1], i)


    # for level in levels:
    #     if lines[level][-1][0] < 1500:
    #
    #     for pos in lines[level]:



    f = open(savePath + 'saved_data_format.txt', 'w')

    for i in range(len(lines[levels[0]])):
        f.write(str(round(lines[levels[0]][i][0], 2)))
        f.write('; ')

        for j, level in enumerate(levels):
            f.write(str(round(lines[level][i][1], 2)))
            if j < len(levels) - 1:
                f.write(', ')

        f.write('\n')

    f.close()

    # for level in levels:
    #     f = open(savePath+'saved_data_format_' + str(level) + '.txt', 'w')
    #
    #     for i in range(len(lines[level])):
    #         line = str(round(lines[level][i][0], 1)) + '; ' + str(round(lines[level][i][1], 4)) + '\n'
    #         f.write(line)
    #
    #     f.close()

    # # App.Console.PrintMessage(("\n save path format "+savePath+'\\saved_data_format.txt'))
    # f = open(savePath + 'saved_data_format.txt', 'w')
    # for level in levels:
    #     line = (str(level) + ';' + str(lines[level]) + '\n').replace("'", '').replace('[', '').replace(']', '')
    #     f.write(line)
    # f.write(str(level)+';')
    # f.write(str(lines[level][1:-1])+'\n')
    # f.close()

    return 0


# ---------------------------------------------------------------------------

def formatInterpolatedPositions(positions, savePath):
    """
    kvuli pootoceni globalniho SS z inventoru do SS makety je:
    x_Maketa == -z (hodnoty jsou jiz kladne z predchozi operace)
    z_Maketa == -x (hodnoty jsou jiz kladne z predchozi operace)
    :param positions:
    :param savePath:
    :return:
    """
    # x1;y1(x1, z1);y2(x1, z2);y3(x1, z3)
    # x2;y1(x2, z1);y2(x2, z2);y3(x2, z3)
    # lines = dict()
    # for pos in positions:
    #     # print(pos)
    #     # point = str(pos[1])+'('+str(pos[0])+','+str(pos[2])+');'
    #     point = str(pos[1] + 200)
    #     if pos[2] not in lines:
    #         lines[pos[2]] = list()
    #         lines[pos[2]].append(point)
    #     else:
    #         lines[pos[2]].append(point)

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

    for level in levels:
        # deleting negative values because of the Hoffset
        negValues = 0
        checkedPos = []
        # lines[level] = [x for x in lines[level] if x >=0 ]
        for pos in lines[level]:
            if pos[0] < 0:
                negValues += 1
            else:
                checkedPos.append(pos)

        checkedPos += [[0, 0, level]] * negValues
        lines[level] = checkedPos

    for level in levels:
        # adding zero values because of the positive Hoffset
        # and cutting the values above x = 1500
        i = 0
        # print(lines[level][:20])
        for pos in lines[level]:
            # print(pos)
            if pos[0] > 1500:
                break
            else:
                i += 1
        lines[level] = lines[level][:i]
        if lines[level][0][0] != 0:
            increment = abs(lines[level][1][0] - lines[level][0][0])
            k = int(lines[level][0][0]/increment) + 1
            missing_data = []
            for j in range(k):
                missing_data.append([j*increment, 0, level])

            lines[level] = missing_data + lines[level]
        print(len(lines[level]))
        print(lines[level][0], lines[level][-1], i)



    # App.Console.PrintMessage(("\n save path format "+savePath+'\\saved_data_format.txt'))
    f = open(savePath + 'saved_data_format_interp.txt', 'w')

    for i in range(len(lines[levels[0]])):
        f.write(str(round(lines[levels[0]][i][0], 2)))
        f.write('; ')

        for j, level in enumerate(levels):
            # print(len(lines[level]))
            f.write(str(round(lines[level][i][1], 2)))
            if j < len(levels) - 1:
                f.write(', ')

        f.write('\n')

    f.close()
    # f = open(savePath + 'saved_data_format_interp.txt', 'w')
    # for level in levels:
    #     line = (str(level) + ';' + str(lines[level]) + '\n').replace("'", '').replace('[', '').replace(']', '')
    #     f.write(line)
    #     # f.write(str(level)+';')
    #     # f.write(str(lines[level][1:-1])+'\n')
    # f.close()

    return 0


# ---------------------------------------------------------------------------

def calculate(axisLabel, planes, origin_offset, sortCols, mainPath):
    # modelPath = '/home/cada/python3/freecad/predni.stp'
    # print('clicked calculate')

    selected = Gui.Selection.getSelectionEx()

    if len(selected) != 1:
        print('**')
        print('ERROR: wrong or empty selection!')
        print('Please restart the application and then use ctrl + LMB to select the top face.')
        message_box = QtGui.QMessageBox()
        message_box.setText(str('ERROR: wrong selection!'))
        message_box.addButton("OK", QtGui.QMessageBox.YesRole)
        message_box.exec_()
        return 1

    if str(selected[0].Object) != '<Part::PartFeature>':
        print('**')
        print('ERROR: wrong selection! Face was not found in the selection.')
        print('Please restart the application and then use ctrl + LMB to select the top face and Y axis.')
        # print('Selection: ' + selected[0].Object.Label + ', ' + selected[1].Object.Label)
        print('Selection: ' + selected[0].Object.Label)
        message_box = QtGui.QMessageBox()
        message_box.setText(str('ERROR: wrong selection! Face was not found in the selection.'))
        message_box.addButton("OK", QtGui.QMessageBox.YesRole)
        message_box.exec_()
        return 1

    f = selected[0]
    document = App.activeDocument()
    documentLabel = document.Label

    axisObject = findObjectViaLabel(documentLabel, axisLabel)
    glassObjectSelectedName = f.ObjectName
    glass_obj = f.Object

    App.Console.PrintMessage(('planes ', planes))
    ### End command Std_New
    Gui.runCommand('Std_OrthographicCamera', 1)
    ### Begin command Std_Workbench
    Gui.activateWorkbench("PartDesignWorkbench")
    ### End command Std_Workbench
    ### Begin command Std_Part
    App.activeDocument().Tip = App.activeDocument().addObject('App::Part', 'Part')
    App.activeDocument().Part.Label = 'Part'
    Gui.activateView('Gui::View3DInventor', True)
    Gui.activeView().setActiveObject('part', App.activeDocument().Part)
    App.ActiveDocument.recompute()
    App.activeDocument().addObject('PartDesign::Body', 'Body')
    Gui.activateView('Gui::View3DInventor', True)
    Gui.activeView().setActiveObject('pdbody', App.activeDocument().Body)
    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(App.ActiveDocument.Body)
    App.activeDocument().Part.addObject(App.ActiveDocument.Body)
    App.ActiveDocument.recompute()
    ### Begin command Std_Import
    ### ImportGui.insert(u"" + modelPath, "model1")

    Gui.activeDocument().activeView().viewDefaultOrientation()
    showOnlyGlassObject(documentLabel)

    glassObjectSelectedObject = findObjectViaName(documentLabel, glassObjectSelectedName)
    face = f.SubElementNames[0]

    # glass_obj = Gui.Selection.getSelectionEx()
    App.Console.PrintMessage('\n 1 \n')
    ### Begin command PartDesign_Point
    App.getDocument(documentLabel).getObject('Body').newObject('PartDesign::Point', 'DatumPoint')
    App.activeDocument().recompute()
    App.Console.PrintMessage('\n 1 1  \n')
    Gui.activeDocument().setEdit('DatumPoint')
    App.ActiveDocument.DatumPoint.MapReversed = False
    # App.ActiveDocument.DatumPoint.Support = [(glassObjectSelectedObject,  face), (App.getDocument('model1').Y_Axis, '')]
    App.ActiveDocument.DatumPoint.Support = [(glassObjectSelectedObject, face), (axisObject, '')]
    # App.getDocument('Unnamed').Part__Feature067, 'Face2'
    # App.ActiveDocument.DatumPoint.Support = [(App.getDocument('model1').Y_Axis003, ''),(App.getDocument('model1').Part__Feature067, face)]
    App.ActiveDocument.DatumPoint.MapMode = 'ProximityPoint1'
    App.ActiveDocument.recompute()

    Gui.getDocument(documentLabel).resetEdit()
    document.getObject('DatumPoint').recompute()
    positions = []
    previous_plane = np.array([0, 0, 0])
    App.Console.PrintMessage('4 \n')
    # for i in range(steps):
    # first_pass = False
    # measuring_position = origin_offset  # 700, 30, 375, 4.56
    itemVoff_sum = 0
    parse_origin_offset = origin_offset.split(',')
    origin_offset = [float(x) for x in parse_origin_offset]
    glass_obj.Placement.Base.x = glass_obj.Placement.Base.x - origin_offset[2]
    glass_obj.Placement.Base.y = glass_obj.Placement.Base.y - origin_offset[1]
    glass_obj.Placement.Base.z = glass_obj.Placement.Base.z - origin_offset[0]

    # glass_obj_rot = glass_obj.Placement.Rotation.toEuler()
    # glass_obj_base = (glass_obj.Placement.Base.x, glass_obj.Placement.Base.y, glass_obj.Placement.Base.z)
    starting_pos_x = glass_obj.Placement.Base.x
    starting_pos_y = glass_obj.Placement.Base.y
    starting_pos_z = glass_obj.Placement.Base.z

    App.Console.PrintMessage('5 \n')
    App.Console.PrintMessage('entering calc loop')
    App.Console.PrintMessage(('entering calc loop, planes: ', planes))
    document.recompute()
    planes_absolute_pos_vertical = []

    measure_start = time.time()

    App.ParamGet('User parameter:BaseApp/Preferences/Document').SetBool('DisableRecomputes', True)
    for plane in planes:
        itemHoff, itemVoff, inc = plane
        plane = plane + previous_plane
        document.recompute()
        previous_plane = plane
        itemVoff_sum += itemVoff

        glass_obj.Placement.Base.x = starting_pos_x + itemVoff_sum
        glass_obj.Placement.Base.y = starting_pos_y
        glass_obj.Placement.Base.z = starting_pos_z

        planes_absolute_pos_vertical.append(glass_obj.Placement.Base.x)
        App.Console.PrintMessage('\n')
        App.Console.PrintMessage('new plane, itemVoff_sum')
        App.Console.PrintMessage('\n')
        x = inc
        stepSum = 0
        # App.ActiveDocument.recompute()

        while True:

            document.getObject('DatumPoint').recompute()

            v = document.getObject('DatumPoint').Placement.Base

            if abs(v.x) < 1.e-12 and abs(v.z) < 1.e-12:
                # App.Console.PrintMessage(("\n positions: " + str(stepSum) + str(v.y) + str(itemVoff_sum)))
                positions.append([float(stepSum + itemHoff), float(v.y)*1000, float(itemVoff_sum)])

            else:
                positions.append([float(stepSum + itemHoff), np.nan, float(itemVoff_sum)])

            if stepSum > 1500:
                App.Console.PrintMessage("End of the projection limit -> x = 1500 mm.")
                break

            stepSum += x
            glass_obj.Placement.Base.z = glass_obj.Placement.Base.z + x
            # measuring_position[0] = measuring_position[0] - x

        # measuring_position[2] -= itemVoff_sum

    savePath = mainPath

    if platform.system != 'Linux':
        savePath = savePath + '/'
        savePos = open(savePath + 'saved_data.txt', 'w')
    else:
        savePath = savePath + '\\'
        savePos = open(savePath + 'saved_data.txt', 'w')

    print('save path : ', savePath)
    # x1;y1(x1, z1);y2(x1, z2);y3(x1, z3)
    prev_pos = planes_absolute_pos_vertical[0]

    for pos in positions:
        if pos[2] != prev_pos:
            savePos.write('\n')
        savePos.write(str(pos[0]) + ';' + str(pos[1]) + ';' + str(pos[2]) + '\n')
        prev_pos = pos[2]

    savePos.close()
    positionsArray = np.array(positions)
    data = []

    f = open(savePath + 'saved_data.txt', 'r')
    text = f.readlines()
    f.close()
    for line in text:

        data_line = line.strip().replace(' ', '').split(';')
        if len(data_line) == 3:
            data_line = [float(x) for x in data_line]
            data += [data_line]

    positionsArray = np.array(data)
    positions_interp = interpolate_data(positionsArray, savePath)
    positionsArrayInterp = np.array(positions_interp)
    formatInterpolatedPositions(positions_interp, savePath)
    formatPositions(positionsArray, savePath)
    plotCheck.makePlots(positionsArray, savePath)
    plotCheck.makePlots(positions_interp, savePath, '_interp')

    # new_sequence = [0, 3] #nulty sloupec zustava, prvni sloupec se prohodi s 4
    # new_sequence = sortCols
    file_seq = savePath + 'saved_data_format_interp.txt'
    # file_seq = savePath + 'saved_data_format_interp.txt'
    sort_cols.sort_it(file_seq, sortCols)

    measure_end = time.time()
    print('time: ', measure_end - measure_start)
    return 0
