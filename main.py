# -*- coding: utf-8 -*-

# Macro Begin: /home/cada/python3/freecad/rec.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
import FreeCAD
import ImportGui
import Points
import Show

path = '/home/cada/python3/freecad/'
fileNameGlass = 'predni_surf.step'
fileNamePoints = 'points.asc'

App.newDocument("model")
App.setActiveDocument("model")
App.ActiveDocument=App.getDocument("model")
Gui.ActiveDocument=Gui.getDocument("model")
Gui.activeDocument().activeView().viewDefaultOrientation()
### End command Std_New
Gui.runCommand('Std_OrthographicCamera',1)
### Begin command Std_Workbench
Gui.activateWorkbench("PartDesignWorkbench")
### End command Std_Workbench
### Begin command Std_Part
App.activeDocument().Tip = App.activeDocument().addObject('App::Part','Part')
App.activeDocument().Part.Label = 'Part'
Gui.activateView('Gui::View3DInventor', True)
Gui.activeView().setActiveObject('part', App.activeDocument().Part)
App.ActiveDocument.recompute()
App.activeDocument().addObject('PartDesign::Body','Body')
Gui.activateView('Gui::View3DInventor', True)
Gui.activeView().setActiveObject('pdbody', App.activeDocument().Body)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(App.ActiveDocument.Body)
App.activeDocument().Part.addObject(App.ActiveDocument.Body)
App.ActiveDocument.recompute()
### Begin command Std_Import
ImportGui.insert(u"/home/cada/python3/freecad/predni.stp","model")
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().viewDefaultOrientation()
App.getDocument("model").Part__Feature.Placement=App.Placement(App.Vector(-900,800,-500), App.Rotation(App.Vector(0.991233,0.126557,0.0379443),19.67), App.Vector(0,0,0))

### Begin command PartDesign_Point
App.getDocument('model').getObject('Body').newObject('PartDesign::Point','DatumPoint')
App.activeDocument().recompute()
Gui.getDocument('model').setEdit(App.getDocument('model').getObject('Body'),0,'DatumPoint.')
tv = Show.TempoVis(App.ActiveDocument, tag= 'PartGui::TaskAttacher')
tvObj = App.getDocument('model').getObject('DatumPoint')
dep_features = tv.get_all_dependent(App.getDocument('model').getObject('Body'), 'DatumPoint.')
if tvObj.isDerivedFrom('PartDesign::CoordinateSystem'):
	visible_features = [feat for feat in tvObj.InList if feat.isDerivedFrom('PartDesign::FeaturePrimitive')]
	dep_features = [feat for feat in dep_features if feat not in visible_features]
	del(visible_features)
tv.hide(dep_features)
del(dep_features)
if not tvObj.isDerivedFrom('PartDesign::CoordinateSystem'):
		if len(tvObj.Support) > 0:
			tv.show([lnk[0] for lnk in tvObj.Support])
del(tvObj)
Gui.Selection.clearSelection()
Gui.Selection.addSelection('model','p_X2_0159_X0_edn_X_ED_skl_o','Part__Feature.Face75',214.647,-183.617,-58.2989)
Gui.Selection.clearSelection()
Gui.Selection.addSelection('model','p_X2_0159_X0_edn_X_ED_skl_o','Origin002.Y_Axis002.',0,294.622,0)
App.getDocument('model').getObject('DatumPoint').MapReversed = False
App.getDocument('model').getObject('DatumPoint').Support = [(App.getDocument('model').getObject('Part__Feature'),'Face75'),(App.getDocument('model').getObject('Y_Axis002'),'')]
App.getDocument('model').getObject('DatumPoint').MapMode = 'ProximityPoint1'
App.getDocument('model').getObject('DatumPoint').recompute()
Gui.getDocument('model').resetEdit()

# point = App.getDocument('model').getObject('DatumPoint')
# point.MapReversed = False
# point.Support = [(App.getDocument('model').getObject('Part__Feature'),'Face75'),(App.getDocument('model').getObject('Y_Axis002'),'')]
# point.MapMode = 'ProximityPoint1'
App.getDocument('model').getObject('DatumPoint').recompute()
Gui.getDocument('model').resetEdit()
App.Console.PrintMessage('point placement:')
App.Console.PrintMessage(App.getDocument('model').getObject('DatumPoint').Placement)
# App.Console.PrintMessage('moving object:')
# App.getDocument("model").Part__Feature.Placement=App.Placement(App.Vector(-839,599,-474), App.Rotation(App.Vector(0.991233,0.126557,0.0379443),19.67), App.Vector(0,0,0))
# App.getDocument('model').getObject('DatumPoint').recompute()
# Gui.getDocument('model').resetEdit()
App.getDocument('model').getObject('DatumPoint').recompute()
App.Console.PrintMessage('point placement:')
App.Console.PrintMessage(App.getDocument('model').getObject('DatumPoint').Placement)

positions = []
steps = 2
x = 1
for i in range(steps):
	x += 1
	# App.Console.PrintMessage('moving object')
	App.getDocument("model").Part__Feature.Placement = App.Placement(App.Vector(-720-x, 599, -474), App.Rotation(
	App.Vector(0.991233, 0.126557, 0.0379443), 19.67), App.Vector(0, 0, 0))
	App.getDocument('model').getObject('DatumPoint').recompute()
	Gui.getDocument('model').resetEdit()
	App.getDocument('model').getObject('DatumPoint').recompute()
	# App.Console.PrintMessage('point placement:')
	v = App.getDocument('model').getObject('DatumPoint').Placement.Base
	# App.Console.PrintMessage()
	if abs(v.x) < 1.e-12 and abs(v.z) < 1.e-12:
		positions.append([v.x, v.y, v.z])
	else:
		positions.append([None, None, None])
savePos = open('/home/cada/python3/freecad/positions.txt', 'w')

for pos in positions:
	savePos.write(str(pos))
	savePos.write('\n')
	# App.Console.PrintMessage(pos)