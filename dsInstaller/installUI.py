import time
from PySide2 import QtWidgets
from PySide2 import QtCore
from dsInstaller import installFn
from dsInstaller import pages


class InstallDialog(QtWidgets.QMainWindow):
    def __init__(self, installer: installFn.Installer, parent=None, title: str = "dsInstaller", minSize: list = [600, 400]):
        super().__init__(parent)

        self.installer = installer

        # Setup ui
        self.setMinimumSize(minSize[0], minSize[1])
        self.setWindowTitle(title)

        # Create components
        self.createActions()
        self.createWidgets()
        self.createLayouts()
        self.createConnections()

    def createActions(self):
        pass

    def createWidgets(self):
        self.mainWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.backButton = QtWidgets.QPushButton("< &Back")
        self.nextButton = QtWidgets.QPushButton("&Next >")
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.welcomePage = pages.WelcomePage(softwareName=self.installer.repoName)
        self.installDirPage = pages.DirectoryPage(defaultDir=self.installer.installDir)
        self.installPage = pages.InstallPage()
        self.resultPage = pages.ResultsPage(softwareName=self.installer.repoName)
        # Adjust
        self.installDirPage.dirWidget.pathLineEdit.setText(self.installer.installDir)

    def createLayouts(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        # Pages
        self.pageStackLayout = QtWidgets.QStackedLayout()
        self.pageStackLayout.addWidget(self.welcomePage)
        self.pageStackLayout.addWidget(self.installDirPage)
        self.pageStackLayout.addWidget(self.installPage)
        self.pageStackLayout.addWidget(self.resultPage)

        # Buttons
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(self.backButton)
        self.buttonsLayout.addWidget(self.nextButton)
        self.buttonsLayout.addSpacing(20)
        self.buttonsLayout.addWidget(self.cancelButton)

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.pageStackLayout)
        self.mainLayout.addLayout(self.buttonsLayout)

    def createConnections(self):
        # Buttons
        self.nextButton.clicked.connect(self.nextPage)
        self.backButton.clicked.connect(self.prevPage)
        self.cancelButton.clicked.connect(self.close)
        # Directory
        self.installDirPage.dirWidget.pathLineEdit.textChanged.connect(self.setInstallDir)
        # Progress status
        self.installer.progress.started.connect(self.installPage.statusLabel.setText)
        self.installer.progress.downloadStarted.connect(self.installPage.statusLabel.setText)
        self.installer.progress.downloadFinised.connect(self.installPage.statusLabel.setText)
        self.installer.progress.extractionStarted.connect(self.installPage.statusLabel.setText)
        self.installer.progress.extractionFinised.connect(self.installPage.statusLabel.setText)
        self.installer.progress.preInstallStarted.connect(self.installPage.statusLabel.setText)
        self.installer.progress.preInstallFinised.connect(self.installPage.statusLabel.setText)
        self.installer.progress.postInstallStarted.connect(self.installPage.statusLabel.setText)
        self.installer.progress.postInstallFinised.connect(self.installPage.statusLabel.setText)
        self.installer.progress.fileCreated.connect(self.installPage.statusLabel.setText)
        self.installer.progress.done.connect(self.installPage.statusLabel.setText)
        self.installer.progress.done.connect(self.displayResult)
        # Progress completed operations
        self.installer.progress.madeProgress.connect(self.updateProgressBar)

        # Page layout
        self.pageStackLayout.currentChanged.connect(self.updateButtons)

    @QtCore.Slot(str)
    def setInstallDir(self, text):
        self.installer.installDir = text

    @QtCore.Slot()
    def updateButtons(self):
        """Changes text of next button and enables/disables back button"""
        if self.pageStackLayout.currentIndex() == self.pageStackLayout.indexOf(self.installPage) - 1:
            self.nextButton.setText("&Install")
        else:
            self.nextButton.setText("&Next >")

        self.backButton.setEnabled(self.pageStackLayout.currentIndex())

    @QtCore.Slot()
    def nextPage(self):
        """
        Steps displays next element from pages stacked layout.
        If next page is installation page -> calls installer run method
        """
        if self.pageStackLayout.currentIndex() == self.pageStackLayout.indexOf(self.installPage) - 1:
            self.runInstaller()
            return

        self.pageStackLayout.setCurrentIndex(self.pageStackLayout.currentIndex() + 1)

    @QtCore.Slot()
    def prevPage(self):
        """If current page index is not 0 -> selects previous page from pages stacked layout"""
        if self.pageStackLayout.currentIndex():
            self.pageStackLayout.setCurrentIndex(self.pageStackLayout.currentIndex() - 1)

    @QtCore.Slot(int, int)
    def updateProgressBar(self, value: int, operations: int = 0):
        """
        Calculates persentage done and updates progress bar

        :param value: Value to set or number of operation completed
        :type value: int
        :param operations: Total number of operations, defaults to 0
        :type operations: int, optional
        """
        if not operations:
            self.installPage.progressBar.setValue((value))
            return

        percentage = int((value / operations) * 100)
        self.installPage.progressBar.setValue(percentage)
        QtCore.QCoreApplication.processEvents()
        time.sleep(0.5)

    @QtCore.Slot(str, str)
    def displayResult(self, status: str, description: str = ""):
        """
        Progresses installation to result page

        :param status: status of installtion. Any status besides success will trigger failed message
        :type status: str
        :param description: Any aditional description. Will be displayed after status message, defaults to ""
        :type description: str, optional
        """
        self.pageStackLayout.setCurrentWidget(self.resultPage)
        self.resultPage.setResult(status, description)
        self.cancelButton.setText("Close")

    def runInstaller(self):
        """
        Runs installer.
        InstallFailedException: progresses to result page with exception message as description
        """
        self.pageStackLayout.setCurrentWidget(self.installPage)
        self.backButton.hide()
        self.nextButton.hide()
        time.sleep(0.5)
        try:
            self.installer.run()
        except installFn.InstallFailedException as e:
            self.displayResult("failed", e.args[0])
