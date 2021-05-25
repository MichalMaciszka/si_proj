# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clasters.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap


class Ui_Dialog(QtWidgets.QWidget):
    def setupUi(self, list):
        self.resize(560, 640)
        self.horizontalLayoutAll = QtWidgets.QHBoxLayout(self)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(470, 10, 81, 621))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setGeometry(QtCore.QRect(10, 30, 451, 561))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(20, 20, 361, 591))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.buttons = {}
        self.lengths = {}
        self.horizontalLayoutAll.addWidget(self.scrollArea)
        self.horizontalLayoutAll.addWidget(self.buttonBox)
        for i in list:
            if (i % 2 == 0):
                self.horizontalLayout = QtWidgets.QHBoxLayout()
                self.verticalLayout.addLayout(self.horizontalLayout)
            self.verticalLayoutInside = QtWidgets.QVBoxLayout()
            self.buttons[i] = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.buttons[i].clicked.connect(list[i].show)
            self.lab = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.pixmap = QPixmap(list[i].list[0].img_path)
            self.pixmap = self.pixmap.scaled(180, 144)
            self.lab.setPixmap(self.pixmap)
            self.verticalLayoutInside.addWidget(self.lab)
            self.verticalLayoutInside.addWidget(self.buttons[i])
            self.horizontalLayout.addLayout(self.verticalLayoutInside)
            self.lengths[i] = len(list[i].list)
        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def accept(self):
        self.close()

    def reject(self):
        self.close()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        i = 1
        for but in self.buttons:
            self.buttons[but].setText(_translate("Dialog", "Klaster " + str(i) + " (" + str(self.lengths[but]) + ")"))
            i +=1


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())