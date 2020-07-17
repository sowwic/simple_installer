from PySide2 import QtWidgets
from PySide2 import QtGui


class DirectoryWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, defaultDir: str = "", title: str = "Destination", browseTitle: str = "Select directory"):
        """
        Widget containing groupBox, lineEdit and button widgets.
        Button triggers QFileDialog.getExistingDirectory method and sets lineEdit text to path returned from it.

        :param parent: Widget parent, defaults to None
        :type parent: QtWidget, optional
        :param defaultDir: Default text to use for lineEdit text, defaults to ""
        :type defaultDir: str, optional
        :param title: Group box title, defaults to "Destination"
        :type title: str, optional
        :param browseTitle: QFileDialog window title, defaults to "Select directory"
        :type browseTitle: str, optional
        """
        super().__init__(parent)
        self.defaultDir = defaultDir
        self.title = title
        self.browseTitle = browseTitle

        self.createWidgets()
        self.createLayouts()
        self.createConnections()

    def createWidgets(self):
        self.group = QtWidgets.QGroupBox(self.title)
        self.pathLineEdit = QtWidgets.QLineEdit(self.defaultDir)
        self.browseButton = QtWidgets.QPushButton("Browse...")

    def createLayouts(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.groupLayout = QtWidgets.QHBoxLayout()
        self.groupLayout.addWidget(self.pathLineEdit)
        self.groupLayout.addWidget(self.browseButton)
        self.group.setLayout(self.groupLayout)
        self.mainLayout.addWidget(self.group)
        self.mainLayout.addStretch()

    def createConnections(self):
        self.browseButton.clicked.connect(self.browseDirPath)

    def browseDirPath(self):
        """Get directory path from QFileDialog"""
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, self.browseTitle, self.pathLineEdit.text())
        if not dirPath:
            return
        self.pathLineEdit.setText(dirPath)
