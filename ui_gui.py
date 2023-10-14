# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Lecture2Text(object):
    def setupUi(self, Lecture2Text):
        Lecture2Text.setObjectName("Lecture2Text")
        Lecture2Text.setEnabled(True)
        Lecture2Text.resize(937, 707)
        Lecture2Text.setMinimumSize(QtCore.QSize(937, 707))
        Lecture2Text.setMaximumSize(QtCore.QSize(937, 707))
        self.centralwidget = QtWidgets.QWidget(Lecture2Text)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_export = QtWidgets.QPushButton(self.centralwidget)
        self.btn_export.setEnabled(False)
        self.btn_export.setGeometry(QtCore.QRect(780, 640, 141, 41))
        self.btn_export.setObjectName("btn_export")
        self.btn_show_text = QtWidgets.QPushButton(self.centralwidget)
        self.btn_show_text.setEnabled(False)
        self.btn_show_text.setGeometry(QtCore.QRect(790, 120, 131, 31))
        self.btn_show_text.setObjectName("btn_show_text")
        self.language = QtWidgets.QComboBox(self.centralwidget)
        self.language.setGeometry(QtCore.QRect(130, 70, 86, 31))
        self.language.setObjectName("language")
        self.language.addItem("")
        self.language.setItemText(0, "")
        self.language.addItem("")
        self.language.addItem("")
        self.language.addItem("")
        self.txt_output = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_output.setGeometry(QtCore.QRect(30, 150, 891, 481))
        self.txt_output.setObjectName("txt_output")
        self.btn_browse = QtWidgets.QPushButton(self.centralwidget)
        self.btn_browse.setGeometry(QtCore.QRect(480, 20, 141, 31))
        self.btn_browse.setObjectName("btn_browse")
        self.btn_convert = QtWidgets.QPushButton(self.centralwidget)
        self.btn_convert.setEnabled(False)
        self.btn_convert.setGeometry(QtCore.QRect(740, 20, 181, 51))
        self.btn_convert.setObjectName("btn_convert")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 110, 71, 31))
        self.label.setObjectName("label")
        self.txt_path = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_path.setGeometry(QtCore.QRect(130, 20, 351, 31))
        self.txt_path.setReadOnly(True)
        self.txt_path.setObjectName("txt_path")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 71, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 91, 31))
        self.label_3.setObjectName("label_3")
        self.txt_progress = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_progress.setGeometry(QtCore.QRect(130, 110, 491, 31))
        self.txt_progress.setReadOnly(True)
        self.txt_progress.setObjectName("txt_progress")
        Lecture2Text.setCentralWidget(self.centralwidget)

        self.retranslateUi(Lecture2Text)
        QtCore.QMetaObject.connectSlotsByName(Lecture2Text)

    def retranslateUi(self, Lecture2Text):
        _translate = QtCore.QCoreApplication.translate
        Lecture2Text.setWindowTitle(_translate("Lecture2Text", "Lecture2Text"))
        self.btn_export.setText(_translate("Lecture2Text", "Export to Doc file"))
        self.btn_show_text.setText(_translate("Lecture2Text", "Show Text"))
        self.language.setItemText(1, _translate("Lecture2Text", "English"))
        self.language.setItemText(2, _translate("Lecture2Text", "Hebrew"))
        self.language.setItemText(3, _translate("Lecture2Text", "Arabic"))
        self.btn_browse.setText(_translate("Lecture2Text", "Browse Lecture"))
        self.btn_convert.setText(_translate("Lecture2Text", "Convert"))
        self.label.setText(_translate("Lecture2Text", "<html><head/><body><p><span style=\" color:#1c71d8;\">Progress:</span></p></body></html>"))
        self.label_2.setText(_translate("Lecture2Text", "<html><head/><body><p><span style=\" color:#1c71d8;\">Language:</span></p></body></html>"))
        self.label_3.setText(_translate("Lecture2Text", "<html><head/><body><p><span style=\" color:#1c71d8;\">Lecture Path:</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Lecture2Text = QtWidgets.QMainWindow()
    ui = Ui_Lecture2Text()
    ui.setupUi(Lecture2Text)
    Lecture2Text.show()
    sys.exit(app.exec_())