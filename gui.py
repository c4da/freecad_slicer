# -*- coding: utf-8 -*-
# Create by flachyjoe
from PySide import QtCore, QtGui
import FreeCAD,FreeCADGui,Part
import freecad_items as fi
import FreeCAD as App
import ImportGui as Gui
import Show


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


class myForm(Form):
    def setupWidgets(self):
        self.centralWidget = QtGui.QWidget(self.window)
        self.window.setCentralWidget(self.centralWidget)
        self.layout = QtGui.QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.layout_offset = QtGui.QVBoxLayout()
        self.layout.addLayout(self.layout_offset)

        label_path = QtGui.QLabel()
        label_path.setText('Set path:')
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

    def createTable(self, layout):
        self.tableWidget = QtGui.QTableWidget()
        self.tableWidget.setRowCount(3)
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

    def fillTable(self):
        labels = ['horizontal offset', 'vertical offset', 'increment']
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        for row in range(rows):
            itemHoff = QtGui.QTableWidgetItem(str(0))
            self.tableWidget.setItem(row, 0, itemHoff)
            itemVoff = QtGui.QTableWidgetItem(str(30))
            self.tableWidget.setItem(row, 1, itemVoff)
            itemInc = QtGui.QTableWidgetItem(str(1))
            self.tableWidget.setItem(row, 2, itemInc)

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


    def addTableRow(self):
        self.tableWidget.insertRow(1)

    def delTableRow(self):
        self.tableWidget.removeRow(1)

    def labelWidgets(self):
        self.setText(self.linePath, "/home/cada/python3/freecad/MAKETA.stp")
        self.setText(self.lineEdit, "700, 30, 375")
        # self.setText(self.checkBox, "CheckBox")
        # self.setText(self.radioButton, "RadioButton")

    def on_closeButton_clicked(self):
        print(self.lineEdit.text())
        self.window.close()
        # FreeCADGui.Control.closeDialog()

    def on_calcButton_clicked(self):
        modelPath = self.linePath.text()
        data = self.getTableData()
        origin_offset = self.lineEdit.text()
        fi.calculate(modelPath, data, origin_offset)


if __name__ == "__main__":
    myWindow = myForm("test window", 400, 300)
    myWindow.show()

