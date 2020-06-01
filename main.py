# -*- coding: utf-8 -*-
# Create by flachyjoe
import os

os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())

from PySide import QtCore, QtGui
import FreeCAD, FreeCADGui, Part
import freecad_items as fi
import FreeCAD as App
import ImportGui as Gui
import Show

import sys
from os import path

# ========================================================================

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

# ---------------------------------------------------------------------------

def getDefaultValues(fileName):
    f = open(fileName, 'r')
    lines = f.readlines()

    axisName = lines[0].split('=')
    axisName = axisName[1].strip().replace(' ', '')

    offset = lines[1].split('=')
    offset = offset[1].strip().replace(' ', '')

    planesNum = lines[2].split('=')
    planesNum = planesNum[1].strip().replace(' ', '')

    verticalOffset = lines[3].split('=')
    verticalOffset = verticalOffset[1].strip().replace(' ', '')

    horizontalOffset = lines[4].split('=')
    horizontalOffset = horizontalOffset[1].strip().replace(' ', '')

    increment = lines[5].split('=')
    increment = increment[1].strip().replace(' ', '')

    return axisName, offset, planesNum, verticalOffset, horizontalOffset, increment


# ========================================================================

class Form(object):
    def __init__(self, title, width, height):
        self.window = QtGui.QMainWindow()
        self.title = title
        self.window.setObjectName(_fromUtf8(title))
        self.window.setWindowTitle(_translate(self.title, self.title, None))
        self.window.resize(width, height)

    def setupWidgets(self):
        pass

    def labelWidgets(self):
        pass

    def show(self):
        self.setupWidgets()
        self.labelWidgets()
        self.window.show()

    def setText(self, control, text):
        control.setText(_translate(self.title, text, None))

# ========================================================================

class myForm(Form):
    def setupWidgets(self):
        self.centralWidget = QtGui.QWidget(self.window)
        self.window.setCentralWidget(self.centralWidget)
        self.layout = QtGui.QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.layout_offset = QtGui.QVBoxLayout()
        self.layout.addLayout(self.layout_offset)

        label_path = QtGui.QLabel()
        label_path.setText('Set axis name:')
        self.layout_offset.addWidget(label_path)

        self.linePath = QtGui.QLineEdit()
        self.linePath.setGeometry(QtCore.QRect(30, 40, 350, 22))
        self.layout_offset.addWidget(self.linePath)

        label_origin = QtGui.QLabel()
        label_origin.setText('Set origin offset:')
        self.layout_offset.addWidget(label_origin)

        self.lineEdit = QtGui.QLineEdit()
        self.lineEdit.setGeometry(QtCore.QRect(30, 40, 350, 22))
        self.layout_offset.addWidget(self.lineEdit)

        self.default_path, self.default_offset, self.default_planesNum, self.default_verticalOffset, self.default_horizontalOffset, self.default_increment = getDefaultValues(
            'default_values.txt')

        self.createTable(self.layout)

        #
        # self.pushButton = QtGui.QPushButton(self.centralWidget)
        buttonsLayout = QtGui.QHBoxLayout()

        self.calcButton = QtGui.QPushButton('Calculate')
        # self.pushButton = QtGui.QPushButton('Abaqus path')
        self.calcButton.setGeometry(QtCore.QRect(30, 170, 120, 80))
        self.calcButton.clicked.connect(self.on_calcButton_clicked)
        buttonsLayout.addWidget(self.calcButton)

        self.closeButton = QtGui.QPushButton('Close')
        # self.pushButton = QtGui.QPushButton('Abaqus path')
        self.closeButton.setGeometry(QtCore.QRect(30, 170, 120, 80))
        self.closeButton.clicked.connect(self.on_closeButton_clicked)
        buttonsLayout.addWidget(self.closeButton)
        self.layout.addLayout(buttonsLayout)

        # self.checkBox = QtGui.QCheckBox(self.centralWidget)
        # self.checkBox.setGeometry(QtCore.QRect(30, 90, 81, 20))
        # self.checkBox.setChecked(True)

        # self.radioButton = QtGui.QRadioButton(self.centralWidget)
        # self.radioButton.setGeometry(QtCore.QRect(30, 130, 95, 20))

    # ---------------------------------------------------------------------------
    def createTable(self, layout):
        self.tableWidget = QtGui.QTableWidget()
        self.tableWidget.setRowCount(int(self.default_planesNum))
        self.tableWidget.setColumnCount(3)
        labels = ['horizontal offset', 'vertical offset', 'increment']
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeColumnToContents(1)
        layout.addWidget(self.tableWidget)

        layoutButtons = QtGui.QHBoxLayout()
        layout.addLayout(layoutButtons)

        pushButtonAddPlane = QtGui.QPushButton('Add plane')
        pushButtonAddPlane.setGeometry(QtCore.QRect(30, 170, 120, 80))
        pushButtonAddPlane.clicked.connect(self.addTableRow)
        layoutButtons.addWidget(pushButtonAddPlane)

        pushButtonRmPlane = QtGui.QPushButton('Remove plane')
        pushButtonRmPlane.setGeometry(QtCore.QRect(30, 170, 120, 80))
        pushButtonRmPlane.clicked.connect(self.delTableRow)
        layoutButtons.addWidget(pushButtonRmPlane)
        self.fillTable()

    # ---------------------------------------------------------------------------

    def fillTable(self):
        labels = ['horizontal offset', 'vertical offset', 'increment']
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        for row in range(rows):
            itemHoff = QtGui.QTableWidgetItem(str(self.default_horizontalOffset))
            self.tableWidget.setItem(row, 0, itemHoff)
            itemVoff = QtGui.QTableWidgetItem(str(self.default_verticalOffset))
            self.tableWidget.setItem(row, 1, itemVoff)
            itemInc = QtGui.QTableWidgetItem(str(self.default_increment))
            self.tableWidget.setItem(row, 2, itemInc)

    # ---------------------------------------------------------------------------

    def getTableData(self):

        data = []
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()

        for row in range(rows):
            itemHoff = float(self.tableWidget.item(row, 0).text())
            itemVoff = float(self.tableWidget.item(row, 1).text())
            itemInc = float(self.tableWidget.item(row, 2).text())

            data.append([itemHoff, itemVoff, itemInc])

        return data

    # ---------------------------------------------------------------------------

    def addTableRow(self):
        rows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rows)

    # ---------------------------------------------------------------------------

    def delTableRow(self):
        rows = self.tableWidget.rowCount()
        self.tableWidget.removeRow(rows-1)

    # ---------------------------------------------------------------------------

    def labelWidgets(self):
        self.setText(self.linePath, self.default_path)
        self.setText(self.lineEdit, self.default_offset)

    # ---------------------------------------------------------------------------

    def on_closeButton_clicked(self):
        print(self.lineEdit.text())
        self.window.close()
        # FreeCADGui.Control.closeDialog()

    # ---------------------------------------------------------------------------

    def on_calcButton_clicked(self):
        attributes = self.linePath.text()
        data = self.getTableData()
        origin_offset = self.lineEdit.text()
        # buttonReply = QtGui.QMessageBox.question(self, 'Error', "File does not exists.",
        #                                    QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        # if os.path.isfile(modelPath\):
        #     print("CAD file exist")
        App.Console.PrintMessage((attributes, data, origin_offset))
        results = fi.calculate(attributes, data, origin_offset, os.path.dirname(os.path.abspath(__file__)))
        if results == 0:
            message_box = QtGui.QMessageBox()
            message_box.setText(str('All done!'))
            message_box.addButton("OK", QtGui.QMessageBox.YesRole)
            message_box.exec_()
        else:
            message_box = QtGui.QMessageBox()
            message_box.setText(str('An Error has occured. Please see the command line for details. \nAnd restart the application.'))
            message_box.addButton("OK", QtGui.QMessageBox.YesRole)
            message_box.exec_()
            # message_box.show()
            # buttonReply = QtGui.QMessageBox.question(self, 'Notification:', "All done!",
            #                                          QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        # else:
        #     # buttonReply = QtGui.QMessageBox.question(self, 'Error:', "File does not exists.",
        #     #                                          QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        #     message_box = QtGui.QMessageBox()
        #     message_box.setText(str('File does not exists!'))
        #     message_box.addButton("OK", QtGui.QMessageBox.YesRole)
        #     message_box.exec_()
        #     # message_box.show()
        #     print("CAD file does not exist")

# ========================================================================

if __name__ == "__main__":
    myWindow = myForm("Curvature analyzer", 400, 300)
    myWindow.show()
