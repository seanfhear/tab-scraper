from PyQt5 import QtCore, QtGui, QtWidgets
from src import utils
import sys
import os
from configparser import ConfigParser

VERSION = 'v.0.1.2'
TOTAL_WIDTH = 1000
SEARCH_WIDTH = 200
SEARCH_ELEMENT_WIDTH = 150
TEXT_BOX_HEIGHT = 30
CHECK_BOX_HEIGHT = 20
BUTTON_HEIGHT = 30
BUTTON_WIDTH = 150
DIRECTORY_BUTTON_WIDTH = 30
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


class MainWindow(object):
    def setup_ui(self, search_window):
        self.status = ''
        self.results = []
        font = QtGui.QFont()
        font.setPointSize(12)

        window_height = ((OFFSET * 2 + TEXT_BOX_HEIGHT) +
                         ((CHECK_BOX_HEIGHT + CHECK_BOX_OFFSET) * len(CHECK_BOX_NAMES) - CHECK_BOX_OFFSET) +
                         (OFFSET * 2 + BUTTON_HEIGHT)) * 2

        search_window.setObjectName("SearchWindow")
        search_window.setWindowTitle("Tab Scraper " + VERSION)
        search_window.setMinimumSize(QtCore.QSize(TOTAL_WIDTH, window_height))
        search_window.setMaximumSize(QtCore.QSize(TOTAL_WIDTH, window_height))
        search_window.setFont(font)
        search_window.setTabShape(QtWidgets.QTabWidget.Rounded)

        self.central_widget = QtWidgets.QWidget(search_window)
        self.central_widget.setObjectName("centralwidget")

        self.check_boxes = [" "] * len(CHECK_BOX_NAMES)
        for i, name in enumerate(CHECK_BOX_NAMES):
            self.check_boxes[i] = QtWidgets.QCheckBox(self.central_widget)
            self.check_boxes[i].setGeometry(QtCore.QRect(OFFSET,
                                                         ((OFFSET * 2 + TEXT_BOX_HEIGHT) +
                                                          (CHECK_BOX_HEIGHT + CHECK_BOX_OFFSET) * i),
                                                         SEARCH_ELEMENT_WIDTH,
                                                         CHECK_BOX_HEIGHT))
            self.check_boxes[i].setObjectName(name.format("checkBox"))
            self.check_boxes[i].setText(name.format(""))

        self.search_button = QtWidgets.QPushButton(self.central_widget)
        self.search_button.setGeometry(QtCore.QRect(OFFSET,
                                                    ((OFFSET * 2 + TEXT_BOX_HEIGHT) +
                                                     (CHECK_BOX_HEIGHT + CHECK_BOX_OFFSET) *
                                                     len(CHECK_BOX_NAMES) - CHECK_BOX_OFFSET + OFFSET),
                                                    BUTTON_WIDTH,
                                                    BUTTON_HEIGHT))
        self.search_button.setObjectName("searchButton")
        self.search_button.setText("Search")
        self.search_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_button.clicked.connect(self.search_tabs)

        self.download_button = QtWidgets.QPushButton(self.central_widget)
        self.download_button.setGeometry(QtCore.QRect(OFFSET,
                                                      ((OFFSET * 2 + TEXT_BOX_HEIGHT) +
                                                       (CHECK_BOX_HEIGHT + CHECK_BOX_OFFSET) *
                                                       len(CHECK_BOX_NAMES) - CHECK_BOX_OFFSET + OFFSET +
                                                       (OFFSET + BUTTON_HEIGHT)),
                                                      BUTTON_WIDTH - DIRECTORY_BUTTON_WIDTH,
                                                      BUTTON_HEIGHT))
        self.download_button.setObjectName("downloadButton")
        self.download_button.setText("Download")
        self.download_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.download_button.clicked.connect(self.download_tab)

        self.set_directory_button = QtWidgets.QPushButton(self.central_widget)
        self.set_directory_button.setGeometry(QtCore.QRect(OFFSET + (BUTTON_WIDTH - DIRECTORY_BUTTON_WIDTH),
                                                           ((OFFSET * 2 + TEXT_BOX_HEIGHT) +
                                                            (CHECK_BOX_HEIGHT + CHECK_BOX_OFFSET) *
                                                            len(CHECK_BOX_NAMES) - CHECK_BOX_OFFSET + OFFSET +
                                                            (OFFSET + BUTTON_HEIGHT)),
                                                           DIRECTORY_BUTTON_WIDTH,
                                                           BUTTON_HEIGHT))
        self.set_directory_button.setObjectName("downloadButton")
        self.set_directory_button.setText("...")
        self.set_directory_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.set_directory_button.clicked.connect(self.set_download_location)

        self.status_message = QtWidgets.QLabel(self.central_widget)
        self.status_message.setGeometry(QtCore.QRect(OFFSET,
                                                     ((OFFSET * 2 + TEXT_BOX_HEIGHT) +
                                                      (CHECK_BOX_HEIGHT + CHECK_BOX_OFFSET) *
                                                      len(CHECK_BOX_NAMES) - CHECK_BOX_OFFSET + OFFSET +
                                                      (OFFSET + BUTTON_HEIGHT) * 2),
                                                     BUTTON_WIDTH,
                                                     BUTTON_HEIGHT))
        status_font = QtGui.QFont()
        status_font.setPointSize(10)
        self.status_message.setFont(status_font)
        self.status_message.setText(self.status)


        self.search_input = QtWidgets.QLineEdit(self.central_widget)
        self.search_input.setGeometry(QtCore.QRect(OFFSET, OFFSET, SEARCH_ELEMENT_WIDTH, TEXT_BOX_HEIGHT))
        self.search_input.setObjectName("lineEdit")
        self.search_input.returnPressed.connect(self.search_button.click)
        self.search_input.setPlaceholderText("Search query...")

        self.tableWidget = QtWidgets.QTableWidget(self.central_widget)
        self.tableWidget.setGeometry(QtCore.QRect(SEARCH_WIDTH, OFFSET, TOTAL_WIDTH - SEARCH_WIDTH - OFFSET,
                                                  window_height - OFFSET * 2))
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.tableWidget.setShowGrid(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(len(TABLE_COLUMNS))
        self.tableWidget.setRowCount(len(self.results))

        for i, header in enumerate(TABLE_COLUMNS):
            item = QtWidgets.QTableWidgetItem()
            item.setText(header)
            self.tableWidget.setHorizontalHeaderItem(i, item)

        header = self.tableWidget.horizontalHeader()
        for i in range(len(TABLE_COLUMNS)):
            if TABLE_COLUMNS[i] == "Title":
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)

        QtCore.QMetaObject.connectSlotsByName(search_window)
        search_window.setCentralWidget(self.central_widget)

    def search_tabs(self):
        types = []
        for check_box in self.check_boxes:
            if check_box.isChecked():
                types.append(TYPES_DICT[check_box.text()])
        search_string = "%20".join(self.search_input.text().split())
        if len(search_string) > 0:
            self.results = utils.search_tabs(search_string, types)
            self.update_table()

    def update_table(self):
        self.tableWidget.setRowCount(len(self.results))
        for i in range(len(self.results)):
            for j in range(len(TABLE_COLUMNS)):
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.results[i][j])
                self.tableWidget.setItem(i, j, item)

    def download_tab(self):
        self.status_message.setText('Downloading...')
        self.status_message.repaint()
        if len(self.results) > 0:
            row = self.results[self.tableWidget.currentRow()]
            url = row[-2]
            is_file = False
            if row[0] == "Pro" or row[0] == "Power":
                is_file = True

            if is_file:
                utils.download_file(url, row[0], row[1].replace("/", ""))
            else:
                utils.download_tab(url, row[0], row[1].replace("/", ""), row[2], row[6])
        self.status_message.setText('Download finished')
        #self.central_widget.update()

    def set_download_location(self):
        dialog = QtWidgets.QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")

        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the pyInstaller bootloader
            # extends the sys module by a flag frozen=True
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(os.path.splitext(__file__)[0]))
        settings_file = os.path.join(application_path, "settings.cfg")

        config = ConfigParser()
        config.read(settings_file)

        config.set('MAIN', 'destination_root', folder_path)
        with open(settings_file, 'w+') as f:
            config.write(f)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    SearchWindow = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(SearchWindow)
    SearchWindow.show()
    sys.exit(app.exec_())
