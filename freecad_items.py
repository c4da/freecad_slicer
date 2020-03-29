# -*- coding: utf-8 -*-

# Macro Begin: /home/cada/python3/freecad/rec.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++

import FreeCAD as App
import FreeCADGui as Gui
import ImportGui
import Show

import numpy as np
import os
import plotCheck


def movePart(documentName="model", x=0, y=0, z=0):
    App.getDocument(documentName).Part__Feature.Placement = App.Placement(App.Vector(x, y, z),
                                                                          App.Rotation(App.Vector(0, 0, 0.),
                                                                                       0), App.Vector(0, 0, 0))


def printMessage(msg):
    pass


def getObjects(documentName="model"):
    return App.getDocument(documentName).Objects


def findObjectViaLabel(documentName="model", label="glass"):
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


def findGlassObj(documentName="model"):
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


def showOnlyGlassObject(documentName="model"):
    objects = getObjects(documentName)
    # Gui.activateWorkbench("PartWorkbench")
    App.setActiveDocument("model")
    App.ActiveDocument = App.getDocument("model")
    for obj in objects:
        # obj.Visibility = False
        if obj.TypeId == 'Part::Feature':
            # obj.Visibility = False
            if 'GLASS' not in obj.Label:
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
        point = str(pos[1])+'('+str(pos[0])+','+str(pos[2])+');'
        if pos[2] not in lines:
            lines[pos[2]] = list()
            lines[pos[2]].append(point)
        else:
            lines[pos[2]].append(point)

    levels = list(lines.keys())
    App.Console.PrintMessage(("\n levels " + str(levels)))
    levels.sort()
    App.Console.PrintMessage(("\n save path format "+savePath+'\\saved_data_format.txt'))
    f = open(savePath + '\\saved_data_format.txt', 'w')
    for level in levels:
        line = (str(level)+';' + str(lines[level][1:-1])+'\n').replace("'", '')
        f.write(line)
        # f.write(str(level)+';')
        # f.write(str(lines[level][1:-1])+'\n')
    f.close()

    return 0




def calculate(modelPath, planes, origin_offset, origin_x_offsets=0):
    # modelPath = '/home/cada/python3/freecad/predni.stp'
    # print('clicked calculate 1')
    App.Console.PrintMessage(('clicked calculate 2', modelPath))
    App.Console.PrintMessage(('planes ', planes))
    App.newDocument("model")
    App.setActiveDocument("model")
    App.ActiveDocument = App.getDocument("model")
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
    ImportGui.insert(u"" + modelPath, "model")
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewDefaultOrientation()
    showOnlyGlassObject("model")
    glass_obj = findGlassObj("model")
    App.Console.PrintMessage('\n 1 \n')
    ### Begin command PartDesign_Point
    App.getDocument('model').getObject('Body').newObject('PartDesign::Point', 'DatumPoint')
    App.activeDocument().recompute()
    App.Console.PrintMessage('\n 1 1  \n')
    Gui.activeDocument().setEdit('DatumPoint')
    App.ActiveDocument.DatumPoint.MapReversed = False
    App.ActiveDocument.DatumPoint.Support = [(glass_obj, ''),
                                             (App.getDocument('model').Y_Axis003, '')]
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
    parse_origin_offset = origin_offset.split(',')
    origin_offset = [float(x) for x in parse_origin_offset]
    Gui.getDocument('model').resetEdit()
    App.getDocument('model').getObject('DatumPoint').recompute()
    positions = []
    previous_plane = np.array([0, 0, 0])
    App.Console.PrintMessage('4 \n')
    # for i in range(steps):
    # first_pass = False
    # measuring_position = origin_offset  # 375, 30, 700
    itemVoff_sum = 0

    # glass_obj_rot = glass_obj.Placement.Rotation.toEuler()
    # glass_obj_base = (glass_obj.Placement.Base.x, glass_obj.Placement.Base.y, glass_obj.Placement.Base.z)
    starting_pos = glass_obj.Placement.Base.z - origin_offset[2]
    glass_obj.Placement.Base.x = glass_obj.Placement.Base.x - origin_offset[2]
    App.Console.PrintMessage('5 \n')
    App.Console.PrintMessage('entering calc loop')
    App.Console.PrintMessage(('entering calc loop, planes: ', planes))
    App.activeDocument().recompute()
    planes_absolute_pos_vertical = []
    for plane in planes:
        first_pass = False
        itemHoff, itemVoff, inc = plane
        plane = plane + previous_plane
        # measuring_position = origin_offset # 375, 30, 700
        # measuring_position[0] = measuring_position[0] - starting_pos
        # x = 0
        App.activeDocument().recompute()
        previous_plane = plane
        itemVoff_sum += itemVoff
        glass_obj.Placement.Base.z = starting_pos
        glass_obj.Placement.Base.x = glass_obj.Placement.Base.x + itemVoff
        planes_absolute_pos_vertical.append(glass_obj.Placement.Base.x )
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



            App.getDocument('model').getObject('DatumPoint').recompute()
            Gui.getDocument('model').resetEdit()
            # App.getDocument('model').getObject('DatumPoint').recompute()
            # App.Console.PrintMessage('point placement:')
            v = App.getDocument('model').getObject('DatumPoint').Placement.Base
            # App.Console.PrintMessage()
            # App.Console.PrintMessage('\n')
            # App.Console.PrintMessage((v.x, v.y, v.z))
            # App.Console.PrintMessage('\n')
            # App.Console.PrintMessage(
            #     ([measuring_position[0], v.y, measuring_position[2] + itemHoff]))

            if abs(v.x) < 1.e-12 and abs(v.z) < 1.e-12:
                App.Console.PrintMessage(("\n positions: " + str(stepSum) + str(v.y) + str(itemVoff_sum)))
                positions.append([float(stepSum), float(round(v.y, 2)), float(itemVoff_sum)])
                # App.Console.PrintMessage('\n')
                # App.Console.PrintMessage((stepSum, v.y, itemVoff_sum))
                # App.Console.PrintMessage('\n')
                # App.Console.PrintMessage((glass_obj.Placement.Base.x, glass_obj.Placement.Base.y, glass_obj.Placement.Base.z))
                # first_pass = True
            else:
                positions.append([float(stepSum), np.nan, float(itemVoff_sum)])
            # else:
            #     # positions.append([None, None, None])
            #     if first_pass == True:
            #         break

            if stepSum > 1500:
                App.Console.PrintMessage("End of the projection limit.")
                break

            stepSum += x
            glass_obj.Placement.Base.z = glass_obj.Placement.Base.z + x
            # measuring_position[0] = measuring_position[0] - x

        # measuring_position[2] -= itemVoff_sum

    # for i, char in enumerate(''.join(reversed(modelPath))):
    #     if char == '/' or char == "\"":
    #         savePath = modelPath[:-i]
    #         break
    savePath = os.path.dirname(modelPath)
    print(savePath)
    App.Console.PrintMessage(("\n save path ", savePath))
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
    App.Console.PrintMessage(pos)
    formatPositions(positions, savePath)
    plotCheck.makePlots(positions, savePath)
