from PyQt5 import QtCore, QtWidgets
import sys
from random import randint
from PyQt5.QtGui import QPixmap
import math


class Ui_Dialog(QtWidgets.QWidget):
    def __init(self):
        super().__init__()
        self.label = QtWidgets.QLabel("Another window % d" % randint(0, 100))
    def setupUi(self, list):
        self.setObjectName("Claster Window")
        self.resize(480, 640)
        self.list = list
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(10, 600, 461, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setGeometry(QtCore.QRect(10, 30, 451, 561))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 449, 559))
        self.verticalLayout2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.buttonBox)
        QtCore.QMetaObject.connectSlotsByName(self)
        for i in range(len(list)):
            self.horizontalLayout = QtWidgets.QHBoxLayout()
            self.verticalLayoutInside = QtWidgets.QVBoxLayout()
            object = QtWidgets.QLabel(list[i].text)
            self.lab = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.pixmap = QPixmap(list[i].img_path)
            self.pixmap = self.pixmap.scaled(320, 240)
            self.lab.setPixmap(self.pixmap)
            self.verticalLayoutInside.addWidget(self.lab)
            self.verticalLayoutInside.addWidget(object)
            self.horizontalLayout.addLayout(self.verticalLayoutInside)
            self.verticalLayout2.addLayout(self.horizontalLayout)
        self.resizeEvent = self.resizeWind
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        self.close()

    def reject(self):
        self.close()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


    def resizeWind(self, event):
        times = math.floor(self.width()/330)-1
        difference = abs(self.width() - (times+1)*330)
        if difference > 120 and difference < 180:
            if times != -1:
                self.deleteItemsOfLayout(self.verticalLayout2)
                for i in range(len(self.list)):
                    if (i % (times+1) == 0):
                        self.horizontalLayout = QtWidgets.QHBoxLayout()
                    self.verticalLayoutInside = QtWidgets.QVBoxLayout()
                    object = QtWidgets.QLabel(self.list[i].text)
                    self.lab = QtWidgets.QLabel(self.scrollAreaWidgetContents)
                    self.pixmap = QPixmap(self.list[i].img_path)
                    self.pixmap = self.pixmap.scaled(320, 240)
                    self.lab.setPixmap(self.pixmap)
                    self.verticalLayoutInside.addWidget(self.lab)
                    self.verticalLayoutInside.addWidget(object)
                    self.horizontalLayout.addLayout(self.verticalLayoutInside)
                    if (i % (times+1) == times):
                        self.verticalLayout2.addLayout(self.horizontalLayout)
                self.verticalLayout2.addLayout(self.horizontalLayout)

    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())


def init(app, list):
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog, list)
    Dialog.show()
    app.exec_()
