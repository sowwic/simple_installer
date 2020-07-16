import os
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from dsInstaller import installFn
from dsInstaller import installWidgets
from dsInstaller import pages


class InstallDialog(QtWidgets.QMainWindow):
    def __init__(self, installer: installFn.Installer, parent=None, title="", minSize=[600, 400]):
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
        self.installDirPage = pages.DirectoryPage(defaultDir=self.installer.DEFAULT_DIR)
        # Adjust
        self.installDirPage.dirWidget.pathLineEdit.setText(self.installer.DEFAULT_DIR)

    def createLayouts(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        # Pages
        self.pageStackLayout = QtWidgets.QStackedLayout()
        self.pageStackLayout.addWidget(self.welcomePage)
        self.pageStackLayout.addWidget(self.installDirPage)
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

        # Page layout
        self.pageStackLayout.currentChanged.connect(self.updateButtons)

    def addPage(self, page: QtWidgets.QWidget):
        pass

    def nextPage(self):
        if self.pageStackLayout.currentIndex() < self.pageStackLayout.count() - 1:
            self.pageStackLayout.setCurrentIndex(self.pageStackLayout.currentIndex() + 1)

    def updateButtons(self):
        if self.pageStackLayout.currentIndex() == self.pageStackLayout.count() - 1:
            self.nextButton.setText("Install")
        else:
            self.nextButton.setText("&Next >")

        self.backButton.setEnabled(self.pageStackLayout.currentIndex())

    def prevPage(self):
        if self.pageStackLayout.currentIndex():
            self.pageStackLayout.setCurrentIndex(self.pageStackLayout.currentIndex() - 1)


def darkPallete():
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(45, 45, 45))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(45, 45, 48))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.Highlight, QtCore.Qt.gray)

    return palette
