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
        self.titleLabel.setWordWrap(1)
        self.messageLabel = QtWidgets.QLabel(self.welcomeText)
        self.messageLabel.setWordWrap(1)

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


class InstallPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.createWidgets()
        self.createLayouts()
        self.createConnections()

    def createWidgets(self):
        self.statusLabel = QtWidgets.QLabel()
        self.progressBar = QtWidgets.QProgressBar()

    def createLayouts(self):
        self.actionLayout = QtWidgets.QVBoxLayout()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.addLayout(self.actionLayout)
        self.actionLayout.addWidget(self.statusLabel)
        self.actionLayout.addWidget(self.progressBar)
        self.actionLayout.addStretch()

    def createConnections(self):
        pass


class ResultsPage(QtWidgets.QWidget):
    def __init__(self, parent=None, softwareName: str = "Program"):
        super().__init__(parent)
        # Store data
        self.softwareName = softwareName

        self.createWidgets()
        self.createLayouts()
        self.createConnections()

    def createWidgets(self):
        self.resultTitle = QtWidgets.QLabel()
        self.resultTitle.setStyleSheet("font-weight: bold;")
        self.resultText = QtWidgets.QLabel()
        self.resultText.setWordWrap(1)
        self.descriptionText = QtWidgets.QLabel()
        self.descriptionText.setStyleSheet("font-weight: bold;")
        self.descriptionText.setWordWrap(1)

    def createLayouts(self):
        self.actionLayout = QtWidgets.QVBoxLayout()
        self.actionLayout.addWidget(self.resultTitle)
        self.actionLayout.addWidget(self.resultText)
        self.actionLayout.addWidget(self.descriptionText)
        self.actionLayout.addStretch()
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.addLayout(self.actionLayout)

    def createConnections(self):
        pass

    def setResult(self, status, description=""):
        if status != "success":
            self.resultTitle.setText("Installation failed!")
            self.resultText.setText(f"There was and error during installation of {self.softwareName}")
            if description:
                self.descriptionText.setText(description)
            return status

        self.resultTitle.setText("Installation completed.")
        self.resultText.setText(f"{self.softwareName} was installed successfully")
