# noinspection PyUnresolvedReferences
from PyQt5 import QtCore, QtGui, QtWidgets

WIDTH = 150
TEXT_BOX_HEIGHT = 30
CHECK_BOX_HEIGHT = 20
BUTTON_HEIGHT = 30
OFFSET = 25
CHECK_BOX_OFFSET = 15
CHECK_BOXES = ["{}Chords", "{}Tab", "{}GuitarPro", "{}Power", "{}Bass", "{}Ukulele"]


# noinspection PyUnresolvedReferences
class UiSearchWindow(object):
    def setup_ui(self, search_window):
        font = QtGui.QFont()
        font.setPointSize(12)

        search_window.setObjectName("SearchWindow")
        search_window.setMinimumSize(QtCore.QSize(200, 355))
        search_window.setMaximumSize(QtCore.QSize(200, 355))
        search_window.setFont(font)
        search_window.setTabShape(QtWidgets.QTabWidget.Rounded)

        self.central_widget = QtWidgets.QWidget(search_window)
        self.central_widget.setObjectName("centralwidget")

        self.search_input = QtWidgets.QLineEdit(self.central_widget)
        self.search_input.setGeometry(QtCore.QRect(25, 25, WIDTH, TEXT_BOX_HEIGHT))
        self.search_input.setObjectName("lineEdit")

        self.check_boxes = [" "] * 6
        for i, check_box in enumerate(CHECK_BOXES):
            self.check_boxes[i] = QtWidgets.QCheckBox(self.central_widget)
            self.check_boxes[i].setGeometry(QtCore.QRect(OFFSET, ((OFFSET * 2 + TEXT_BOX_HEIGHT) + (CHECK_BOX_HEIGHT + CHECK_BOX_OFFSET) * i), WIDTH, CHECK_BOX_HEIGHT))
            self.check_boxes[i].setObjectName(check_box.format("checkBox"))
            self.check_boxes[i].setText(QtCore.QCoreApplication.translate("UiSearchWindow", check_box.format("")))

        self.push_button = QtWidgets.QPushButton(self.central_widget)
        self.push_button.setGeometry(QtCore.QRect(25, 300, 150, 30))
        self.push_button.setObjectName("pushButton")

        search_window.setCentralWidget(self.central_widget)

        self.retranslateUi(search_window)
        QtCore.QMetaObject.connectSlotsByName(search_window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("UiSearchWindow", "Tab Search"))
        self.search_input.setPlaceholderText(_translate("UiSearchWindow", "Search query..."))
        self.push_button.setText(_translate("UiSearchWindow", "Search"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SearchWindow = QtWidgets.QMainWindow()
    ui = UiSearchWindow()
    ui.setup_ui(SearchWindow)
    SearchWindow.show()
    sys.exit(app.exec_())
