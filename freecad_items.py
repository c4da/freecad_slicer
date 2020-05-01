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
import data_eval as de


def movePart(documentName="model1", x=0, y=0, z=0):
    App.getDocument(documentName).Part__Feature.Placement = App.Placement(App.Vector(x, y, z),
                                                                          App.Rotation(App.Vector(0, 0, 0.),
                                                                                       0), App.Vector(0, 0, 0))


def interpolate_data(positions):
    positions_arr = np.array(positions)
    positions_arr = positions_arr.reshape(len(positions), 3)
    # print(positions_arr)
    interp_start_x = None
    interp_end_x = None
    # print(positions)
    for i, pos in enumerate(positions):
        # print(pos)
        if not np.isnan(pos[1]) and not np.isnan(positions[i + 1][1]) and not np.isnan(positions[i + 2][1]) and \
                interp_start_x is None:
            interp_start_x = i
            print('interp start interval set at: ', i)
            continue
        if not np.isnan(pos[1]) and interp_start_x != None and np.isnan(positions[i + 1][1]) and \
                np.isnan(positions[i + 2][1]):
            print('interp end interval set at: ', i)
            interp_end_x = i
            break
    # print(interp_start_x, interp_end_x)

    x = positions_arr[interp_start_x:interp_end_x, 0]
    y = positions_arr[interp_start_x:interp_end_x, 1]
    x_eval = np.arange(positions_arr[interp_start_x, 0], positions_arr[interp_end_x, 0], 0.1)

    y_interp = de.getLinInterp(x_eval, x, y)
    data_z = np.ones((1, len(x_eval))) * positions_arr[0, 2]

    data = []
    for i, x in enumerate(x_eval):
        y = y_interp[i]
        z = data_z[0, i]
        pos = [x, y, z]
        data.append(pos)
    return data


def printMessage(msg):
    pass


def getObjects(documentName="model1"):
    return App.getDocument(documentName).Objects


def findObjectViaLabel(documentName="model1", label="glass"):
    objects = getObjects(documentName)
    for obj in objects:
        App.Console.PrintMessage(obj.Label + '\n')
        if label in obj.Label:
            print('Found glass object.')
            App.Console.PrintMessage('Found glass object.\n')
            return obj
    print('Glass was not found. Please, check the name of the glass model.\n')
    App.Console.PrintMessage('Glass was not found. Please, check the name of the glass model.\n')
    return 1

def findObjectViaName(documentName="model1", name=""):
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


def findGlassObj(documentName="model1"):
    objects = getObjects(documentName)
    label = 'glass'
    App.Console.PrintMessage('Listing objects:')
    for obj in objects:
        App.Console.PrintMessage(obj.Label + '\n')
        if label in obj.Label:
            print('Found glass object.')
            App.Console.PrintMessage('Found glass object.\n')
            return obj
        elif label.upper() in obj.Label:
            print('Found GLASS object.')
            App.Console.PrintMessage('Found GLASS object.\n')
            return obj
    print('Glass was not found. Please, check the name of the glass model.\n')
    App.Console.PrintMessage('Glass was not found. Please, check the name of the glass model.\n')
    return 1


def showOnlyGlassObject(documentName="model1"):
    objects = getObjects(documentName)
    # Gui.activateWorkbench("PartWorkbench")
    App.setActiveDocument("model1")
    App.ActiveDocument = App.getDocument("model1")
    for obj in objects:
        # obj.Visibility = False
        if obj.TypeId == 'Part::Feature':
            # obj.Visibility = False
            if 'GLASS' not in obj.Label.upper() and 'SKLO' not in obj.Label.upper():
                App.ActiveDocument.removeObject(obj.Name)
                App.ActiveDocument.recompute()
            else:
                pass


def formatPositions(positions, savePath):
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
    lines = dict()
    for pos in positions:
        # point = str(pos[1])+'('+str(pos[0])+','+str(pos[2])+');'
        point = str(pos[1] + 200)
        if pos[0] not in lines:
            lines[pos[0]] = list()
            lines[pos[0]].append(point)
        else:
            lines[pos[0]].append(point)

    levels = list(lines.keys())
    # App.Console.PrintMessage(("\n levels " + str(levels)))
    levels.sort()
    # App.Console.PrintMessage(("\n save path format "+savePath+'\\saved_data_format.txt'))
    f = open(savePath + '\\saved_data_format.txt', 'w')
    for level in levels:
        line = (str(level) + ';' + str(lines[level]) + '\n').replace("'", '').replace('[', '').replace(']', '')
        f.write(line)
        # f.write(str(level)+';')
        # f.write(str(lines[level][1:-1])+'\n')
    f.close()

    return 0


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
    lines = dict()
    for pos in positions:
        # print(pos)
        # point = str(pos[1])+'('+str(pos[0])+','+str(pos[2])+');'
        point = str(pos[1] + 200)
        if pos[0] not in lines:
            lines[pos[0]] = list()
            lines[pos[0]].append(point)
        else:
            lines[pos[0]].append(point)

    levels = list(lines.keys())
    # App.Console.PrintMessage(("\n levels " + str(levels)))
    levels.sort()
    # App.Console.PrintMessage(("\n save path format "+savePath+'\\saved_data_format.txt'))
    f = open(savePath + '\\saved_data_format_interp.txt', 'w')
    for level in levels:
        line = (str(level) + ';' + str(lines[level]) + '\n').replace("'", '').replace('[', '').replace(']', '')
        f.write(line)
        # f.write(str(level)+';')
        # f.write(str(lines[level][1:-1])+'\n')
    f.close()

    return 0


def calculate(modelPath, planes, origin_offset):
    # modelPath = '/home/cada/python3/freecad/predni.stp'
    # print('clicked calculate')

    selected = Gui.Selection.getSelectionEx()

    if len(selected) != 2:
        print('**')
        print('ERROR: wrong or empty selection!')
        print('Please restart the application and then use ctrl + LMB to select the top face and Y axis.')
        message_box = QtGui.QMessageBox()
        message_box.setText(str('ERROR: wrong selection!'))
        message_box.addButton("OK", QtGui.QMessageBox.YesRole)
        message_box.exec_()
        return 1

    if str(selected[0].Object) != '<Part::PartFeature>':
        print('**')
        print('ERROR: wrong selection! Face was not found in the selection.')
        print('Please restart the application and then use ctrl + LMB to select the top face and Y axis.')
        print('Selection: ' + selected[0].Object.Label + ', ' + selected[1].Object.Label)
        message_box = QtGui.QMessageBox()
        message_box.setText(str('ERROR: wrong selection! Face was not found in the selection.'))
        message_box.addButton("OK", QtGui.QMessageBox.YesRole)
        message_box.exec_()
        return 1

    if str(selected[1].Object) != '<GeoFeature object>':
        print('**')
        print('ERROR: wrong selection! Axis was not found in the selection.')
        print('Please restart the application and then use ctrl + LMB to select the top face and Y axis.')
        print('Selection: ' + selected[0].Object.Label + ', ' + selected[1].Object.Label)
        message_box = QtGui.QMessageBox()
        message_box.setText(str('ERROR: wrong selection! Axis was not found in the selection.'))
        message_box.addButton("OK", QtGui.QMessageBox.YesRole)
        message_box.exec_()
        return 1

    if str(selected[1].Object) == '<GeoFeature object>' and 'AXIS' not in selected[1].Object.Label.upper():
        print('**')
        print('ERROR: wrong selection! Axis was not found in the selection.')
        print('Please restart the application and then use ctrl + LMB to select the top face and Y axis.')
        print('Selection: '+selected[0].Object.Label+', '+selected[1].Object.Label)
        message_box = QtGui.QMessageBox()
        message_box.setText(str('ERROR: wrong selection! Axis was not found in the selection.'))
        message_box.addButton("OK", QtGui.QMessageBox.YesRole)
        message_box.exec_()
        return 1

    f = selected[0]
    axis = selected[1]
    glassObjectSelectedName = f.ObjectName

    App.Console.PrintMessage(('clicked calculate 2', modelPath))
    App.Console.PrintMessage(('planes ', planes))
    App.newDocument("model1")
    App.setActiveDocument("model1")
    App.ActiveDocument = App.getDocument("model1")
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
    ImportGui.insert(u"" + modelPath, "model1")
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewDefaultOrientation()
    showOnlyGlassObject("model1")

    glass_obj = findGlassObj("model1")
    glassObjectSelectedObject = findObjectViaName('model1', glassObjectSelectedName)
    face = f.SubElementNames[0]


    # glass_obj = Gui.Selection.getSelectionEx()
    App.Console.PrintMessage('\n 1 \n')
    ### Begin command PartDesign_Point
    App.getDocument('model1').getObject('Body').newObject('PartDesign::Point', 'DatumPoint')
    App.activeDocument().recompute()
    App.Console.PrintMessage('\n 1 1  \n')
    Gui.activeDocument().setEdit('DatumPoint')
    App.ActiveDocument.DatumPoint.MapReversed = False
    # App.ActiveDocument.DatumPoint.Support = [(glassObjectSelectedObject,  face), (App.getDocument('model1').Y_Axis, '')]
    App.ActiveDocument.DatumPoint.Support = [(glassObjectSelectedObject, face), (axis.Object, '')]
    # App.getDocument('Unnamed').Part__Feature067, 'Face2'
    # App.ActiveDocument.DatumPoint.Support = [(App.getDocument('model1').Y_Axis003, ''),(App.getDocument('model1').Part__Feature067, face)]
    App.ActiveDocument.DatumPoint.MapMode = 'ProximityPoint1'
    App.ActiveDocument.recompute()
    # Gui.ActiveDocument.resetEdit()
    # Gui.getDocument('model').setEdit(App.getDocument('model').getObject('Body'), 0, 'DatumPoint.')
    # App.Console.PrintMessage('2 0 \n')
    # tv = Show.TempoVis(App.ActiveDocument, tag='PartGui::TaskAttacher')
    # tvObj = App.getDocument('model').getObject('DatumPoint')
    # App.Console.PrintMessage('2 0 1 \n')
    # dep_features = tv.get_all_dependent(App.getDocument('model').getObject('Body'), 'DatumPoint.')
    # App.Console.PrintMessage('2 1 \n')
    # if tvObj.isDerivedFrom('PartDesign::CoordinateSystem'):
    #     visible_features = [feat for feat in tvObj.InList if feat.isDerivedFrom('PartDesign::FeaturePrimitive')]
    #     dep_features = [feat for feat in dep_features if feat not in visible_features]
    #     del visible_features
    # tv.hide(dep_features)
    # del dep_features
    # App.Console.PrintMessage('2 2 \n')
    # if not tvObj.isDerivedFrom('PartDesign::CoordinateSystem'):
    #     if len(tvObj.Support) > 0:
    #         tv.show([lnk[0] for lnk in tvObj.Support])
    # del tvObj
    # Gui.Selection.clearSelection()
    # App.Console.PrintMessage('3 \n')
    # App.getDocument('model').getObject('DatumPoint').MapReversed = False
    # App.getDocument('model').getObject('DatumPoint').Support = [
    #     (glass_obj, ''),
    #     (App.getDocument('model').getObject('Y_Axis'), '')]
    # App.getDocument('model').getObject('DatumPoint').MapMode = 'ProximityPoint1'
    # App.getDocument('model').getObject('DatumPoint').recompute()
    # Gui.getDocument('model').resetEdit()
    # App.getDocument('model').getObject('DatumPoint').recompute()
    # Gui.getDocument('model').resetEdit()


    Gui.getDocument('model1').resetEdit()
    App.getDocument('model1').getObject('DatumPoint').recompute()
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
    glass_obj.Placement.Base.y = glass_obj.Placement.Base.y - origin_offset[1] - 200
    glass_obj.Placement.Base.z = glass_obj.Placement.Base.z - origin_offset[0]

    # glass_obj_rot = glass_obj.Placement.Rotation.toEuler()
    # glass_obj_base = (glass_obj.Placement.Base.x, glass_obj.Placement.Base.y, glass_obj.Placement.Base.z)
    starting_pos_x = glass_obj.Placement.Base.x
    starting_pos_y = glass_obj.Placement.Base.y
    starting_pos_z = glass_obj.Placement.Base.z

    App.Console.PrintMessage('5 \n')
    App.Console.PrintMessage('entering calc loop')
    App.Console.PrintMessage(('entering calc loop, planes: ', planes))
    App.activeDocument().recompute()
    planes_absolute_pos_vertical = []
    measure_start = time.time()

    App.ParamGet('User parameter:BaseApp/Preferences/Document').SetBool('DisableRecomputes', True)
    for plane in planes:
        itemHoff, itemVoff, inc = plane
        plane = plane + previous_plane
        App.activeDocument().recompute()
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
            # App.Console.PrintMessage((first_pass, measuring_position[0], measuring_position[1]))
            # measuring_position[1] = measuring_position[1] - itemVoff_sum
            # measuring_position[0] = measuring_position[0]
            # App.Console.PrintMessage(
            #     (glass_obj.Placement.Base.x, glass_obj.Placement.Base.y, glass_obj.Placement.Base.z))
            # App.Console.PrintMessage('moving object')
            # App.getDocument("model").Part__Feature.Placement = App.Placement(App.Vector(measuring_position[0] - x, measuring_position[1], measuring_position[2]), App.Rotation(
            #     App.Vector(0, 0, 0), 1), App.Vector(0, 0, 0))

            # glass_obj.Placement = App.Placement(App.Vector(measuring_position[0], measuring_position[1]- x, measuring_position[2]), App.Rotation(glass_obj_rot))

            App.getDocument('model1').getObject('DatumPoint').recompute()
            # Gui.getDocument('model').resetEdit()

            # App.getDocument('model').getObject('DatumPoint').recompute()
            # App.Console.PrintMessage('point placement:')
            v = App.getDocument('model1').getObject('DatumPoint').Placement.Base
            # App.Console.PrintMessage()
            # App.Console.PrintMessage('\n')
            # App.Console.PrintMessage((v.x, v.y, v.z))
            # App.Console.PrintMessage('\n')
            # App.Console.PrintMessage(
            #     ([measuring_position[0], v.y, measuring_position[2] + itemHoff]))

            if abs(v.x) < 1.e-12 and abs(v.z) < 1.e-12:
                # App.Console.PrintMessage(("\n positions: " + str(stepSum) + str(v.y) + str(itemVoff_sum)))
                positions.append([float(stepSum), float(v.y), float(itemVoff_sum)])

            else:
                positions.append([float(stepSum), np.nan, float(itemVoff_sum)])

            if stepSum > 1500:
                App.Console.PrintMessage("End of the projection limit.")
                break

            stepSum += x + itemHoff
            glass_obj.Placement.Base.z = glass_obj.Placement.Base.z + x + itemHoff
            # measuring_position[0] = measuring_position[0] - x

        # measuring_position[2] -= itemVoff_sum

    savePath = os.path.dirname(modelPath)
    print(savePath)
    # App.Console.PrintMessage(("\n save path ", savePath))
    # App.Console.PrintMessage(("\n positions: ", positions))
    savePos = open(savePath + '\\saved_data.txt', 'w')
    # x1;y1(x1, z1);y2(x1, z2);y3(x1, z3)
    prev_pos = planes_absolute_pos_vertical[0]

    for pos in positions:
        if pos[2] != prev_pos:
            savePos.write('\n')
        savePos.write(str(pos[0]) + ';' + str(pos[1]) + ';' + str(pos[2]) + '\n')
        prev_pos = pos[2]

    savePos.close()
    # App.Console.PrintMessage(pos)
    positions_interp = interpolate_data(positions)
    formatInterpolatedPositions(positions_interp, savePath)
    # print('*'*20)
    # print('y_interp: ', positions_interp)
    formatPositions(positions, savePath)
    # print('*' * 20)
    plotCheck.makePlots(positions, savePath)
    # print('*' * 20)
    plotCheck.makePlots(positions_interp, savePath, '_interp')
    # print('*' * 20)

    measure_end = time.time()
    print('time: ', measure_end - measure_start)
    return 0
