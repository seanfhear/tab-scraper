# noinspection PyUnresolvedReferences
from PyQt5 import QtCore, QtGui, QtWidgets
import tab_scraper
import sys

TOTAL_WIDTH = 1000
SEARCH_WIDTH = 200
SEARCH_ELEMENT_WIDTH = 150
TEXT_BOX_HEIGHT = 30
CHECK_BOX_HEIGHT = 20
BUTTON_HEIGHT = 30
OFFSET = 25
CHECK_BOX_OFFSET = 15
CHECK_BOX_NAMES = ["{}Chords", "{}Tab", "{}GuitarPro", "{}PowerTab", "{}Bass", "{}Ukulele"]
TYPES_DICT = {"Chords": "Chords",
              "Tab": "Tabs",
              "GuitarPro": "Pro",
              "PowerTab": "Power",
              "Bass": "Bass Tabs",
              "Ukulele": "Ukulele Chords"}
TABLE_COLUMNS = ["Type", "Artist", "Title", "Rating", "Votes"]

# TODO remove warning suppressions

# noinspection PyUnresolvedReferences
class MainWindow(object):
    def setup_ui(self, search_window):
        self.results = []
        font = QtGui.QFont()
        font.setPointSize(12)

        window_height = ((OFFSET * 2 + TEXT_BOX_HEIGHT) +
                         ((CHECK_BOX_HEIGHT + CHECK_BOX_OFFSET) * len(CHECK_BOX_NAMES) - CHECK_BOX_OFFSET) +
                         (OFFSET * 2 + BUTTON_HEIGHT))

        search_window.setObjectName("SearchWindow")
        search_window.setMinimumSize(QtCore.QSize(TOTAL_WIDTH, window_height))
        search_window.setMaximumSize(QtCore.QSize(TOTAL_WIDTH, window_height))
        search_window.setFont(font)
        search_window.setTabShape(QtWidgets.QTabWidget.Rounded)

        self.central_widget = QtWidgets.QWidget(search_window)
        self.central_widget.setObjectName("centralwidget")

        self.check_boxes = [" "] * len(CHECK_BOX_NAMES)
        for i, name in enumerate(CHECK_BOX_NAMES):
            self.check_boxes[i] = QtWidgets.QCheckBox(self.central_widget)
            self.check_boxes[i].setGeometry(QtCore.QRect(OFFSET, ((OFFSET * 2 + TEXT_BOX_HEIGHT) +
                                                                  (CHECK_BOX_HEIGHT + CHECK_BOX_OFFSET) * i),
                                                         SEARCH_ELEMENT_WIDTH, CHECK_BOX_HEIGHT))
            self.check_boxes[i].setObjectName(name.format("checkBox"))
            self.check_boxes[i].setText(QtCore.QCoreApplication.translate("UiSearchWindow", name.format("")))

        self.push_button = QtWidgets.QPushButton(self.central_widget)
        self.push_button.setGeometry(QtCore.QRect(OFFSET, ((OFFSET * 2 + TEXT_BOX_HEIGHT) +
                                                           (CHECK_BOX_HEIGHT + CHECK_BOX_OFFSET) *
                                                           len(CHECK_BOX_NAMES) - CHECK_BOX_OFFSET + OFFSET),
                                                  SEARCH_ELEMENT_WIDTH, BUTTON_HEIGHT))
        self.push_button.setObjectName("searchButton")
        self.push_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.push_button.clicked.connect(self.search_tabs)

        self.search_input = QtWidgets.QLineEdit(self.central_widget)
        self.search_input.setGeometry(QtCore.QRect(OFFSET, OFFSET, SEARCH_ELEMENT_WIDTH, TEXT_BOX_HEIGHT))
        self.search_input.setObjectName("lineEdit")
        self.search_input.returnPressed.connect(self.push_button.click)

        self.tableWidget = QtWidgets.QTableWidget(self.central_widget)
        self.tableWidget.setGeometry(QtCore.QRect(SEARCH_WIDTH, OFFSET, TOTAL_WIDTH - SEARCH_WIDTH - OFFSET,
                                                  window_height - OFFSET * 2))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        self.tableWidget.setShowGrid(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(len(TABLE_COLUMNS))
        self.tableWidget.setRowCount(len(self.results))

        for i, header in enumerate(TABLE_COLUMNS):
            item = QtWidgets.QTableWidgetItem()
            item.setText(QtCore.QCoreApplication.translate("Form", header))
            self.tableWidget.setHorizontalHeaderItem(i, item)

        header = self.tableWidget.horizontalHeader()
        for i in range(len(TABLE_COLUMNS)):
            if TABLE_COLUMNS[i] == "Title":
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)

        self.retranslateUi(search_window)
        QtCore.QMetaObject.connectSlotsByName(search_window)

        search_window.setCentralWidget(self.central_widget)


    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("UiSearchWindow", "Tab Search"))
        self.search_input.setPlaceholderText(_translate("UiSearchWindow", "Search query..."))
        self.push_button.setText(_translate("UiSearchWindow", "Search"))

    def search_tabs(self):
        types = []
        for check_box in self.check_boxes:
            if check_box.isChecked():
                types.append(TYPES_DICT[check_box.text()])
        search_string = "%20".join(self.search_input.text().split())
        self.results = tab_scraper.search_tabs(search_string, types)
        self.update_table()

    def update_table(self):
        self.tableWidget.setRowCount(len(self.results))
        for i in range(len(self.results)):
            for j in range(len(self.results[i])):
                item = QtWidgets.QTableWidgetItem()
                item.setText(QtCore.QCoreApplication.translate("Form", self.results[i][j]))
                self.tableWidget.setItem(i, j, item)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    SearchWindow = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(SearchWindow)
    SearchWindow.show()
    sys.exit(app.exec_())
