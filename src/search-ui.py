# noinspection PyUnresolvedReferences
from PyQt5 import QtCore, QtGui, QtWidgets

class UiSearchWindow(object):
    def setupUi(self, SearchWindow):
        SearchWindow.setObjectName("SearchWindow")
        SearchWindow.setMinimumSize(QtCore.QSize(200, 355))
        SearchWindow.setMaximumSize(QtCore.QSize(200, 355))
        font = QtGui.QFont()
        font.setPointSize(12)
        SearchWindow.setFont(font)
        SearchWindow.setTabShape(QtWidgets.QTabWidget.Rounded)

        self.centralwidget = QtWidgets.QWidget(SearchWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(25, 25, 150, 30))
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")

        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(25, 80, 150, 20))
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")

        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(25, 115, 150, 20))
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")

        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(25, 150, 150, 20))
        self.checkBox_3.setFont(font)
        self.checkBox_3.setObjectName("checkBox_3")

        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(25, 185, 150, 20))
        self.checkBox_4.setFont(font)
        self.checkBox_4.setObjectName("checkBox_4")

        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.setGeometry(QtCore.QRect(25, 220, 150, 20))
        self.checkBox_5.setFont(font)
        self.checkBox_5.setObjectName("checkBox_5")

        self.checkBox_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6.setGeometry(QtCore.QRect(25, 255, 150, 20))
        self.checkBox_6.setFont(font)
        self.checkBox_6.setObjectName("checkBox_6")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(25, 300, 150, 30))
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        SearchWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SearchWindow)
        QtCore.QMetaObject.connectSlotsByName(SearchWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("SearchWindow", "SearchWindow"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Search query..."))
        self.checkBox.setText(_translate("MainWindow", "Chords"))
        self.checkBox_2.setText(_translate("MainWindow", "Tab"))
        self.checkBox_3.setText(_translate("MainWindow", "GuitarPro"))
        self.pushButton.setText(_translate("MainWindow", "Search"))
        self.checkBox_4.setText(_translate("MainWindow", "Bass"))
        self.checkBox_5.setText(_translate("MainWindow", "Ukulele"))
        self.checkBox_6.setText(_translate("MainWindow", "Power"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SearchWindow = QtWidgets.QMainWindow()
    ui = UiSearchWindow()
    ui.setupUi(SearchWindow)
    SearchWindow.show()
    sys.exit(app.exec_())
