from PySide2 import QtWidgets
from dsInstaller import installWidgets


class WelcomePage(QtWidgets.QWidget):
    def __init__(self, parent=None, softwareName: str = "Program"):
        super().__init__(parent)

        self.titleText = f"Welcome to the {softwareName} Setup Sizard"
        self.welcomeText = f"""The Setup Wizard will install {softwareName} on your computer.\nClick Next to continue or Cancel  to exit Setup wizard"""
    
        self.createWidgets()
        self.createLayouts()
        self.createConnections()

    def createWidgets(self):
        self.titleLabel = QtWidgets.QLabel(self.titleText)
        self.titleLabel.setStyleSheet("font-weight: bold;")
        self.messageLabel = QtWidgets.QLabel(self.welcomeText)

    def createLayouts(self):
        self.actionLayout = QtWidgets.QVBoxLayout()
        self.actionLayout.addWidget(self.titleLabel)
        self.actionLayout.addWidget(self.messageLabel)
        self.actionLayout.addStretch()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.addLayout(self.actionLayout)

    def createConnections(self):
        pass


class DirectoryPage(QtWidgets.QWidget):
    def __init__(self, defaultDir: str, parent=None):
        super().__init__(parent)
        # Store data
        self.defaultDir = defaultDir

        self.createWidgets()
        self.createLayouts()
        self.createConnections()

    def createWidgets(self):
        self.dirWidget = installWidgets.DirectoryWidget(defaultDir=self.defaultDir)

    def createLayouts(self):
        self.actionLayout = QtWidgets.QVBoxLayout()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.addLayout(self.actionLayout)
        self.actionLayout.addWidget(self.dirWidget)
        self.actionLayout.addStretch()

    def createConnections(self):
        pass
