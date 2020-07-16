from PySide2 import QtWidgets
from PySide2 import QtGui


class DirectoryWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, defaultDir: str = "", title="Destination", browseTitle="Select directory"):
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
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, self.browseTitle, "home")
        if not dirPath:
            return
        self.pathLineEdit.setText(dirPath)
