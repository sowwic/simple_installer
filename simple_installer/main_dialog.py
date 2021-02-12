from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
import simple_installer.installFn as installFn
import simple_installer.pages as pages


class InstallerWindow(QtWidgets.QMainWindow):
    def __init__(self, installer: installFn.Installer, title: str = "Installer", min_size: tuple = (600, 400)):
        super().__init__(parent=None)
        self.installer = installer
        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        # Apply dark pallete
        app_instance = QtCore.QCoreApplication.instance()
        app_instance.setStyle(QtWidgets.QStyleFactory.create("fusion"))
        app_instance.setPalette(dark_pallete())

    def create_actions(self):
        pass

    def create_widgets(self):
        # Central widget
        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Pages
        self.stack = QtWidgets.QStackedWidget()
        self.welcome_page = pages.WelcomePage()
        self.dir_page = pages.DirectoryPage(self.installer.DEFAULT_DIR)
        self.install_page = pages.InstallPage()
        self.result_page = pages.ResultsPage()

        # Buttons
        self.back_button = QtWidgets.QPushButton("< &Back")
        self.nextButton = QtWidgets.QPushButton("&Next >")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        # Adjust
        self.install_dir_page.dirWidget.line_edit.setText(self.installer)

        # Buttons

    def create_layouts(self):
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.back_button)
        self.buttons_layout.addWidget(self.next_button)
        self.buttons_layout.addSpacing(20)
        self.buttons_layout.addWidget(self.cancel_button)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.stack)
        self.main_layout.addLayout(self.buttons_layout)

    def create_connections(self):
        pass


def dark_pallete():
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
