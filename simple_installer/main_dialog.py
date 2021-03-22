from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from simple_installer import Logger
import simple_installer.installFn as installFn
import simple_installer.pages as pages


class InstallerWindow(QtWidgets.QMainWindow):
    def __init__(self, installer: installFn.Installer,
                 title: str = "Installer",
                 min_size: tuple = (400, 200),
                 initial_size=(400, 200)):
        super().__init__(parent=None)
        self.installer = installer
        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.setWindowTitle(title)
        self.setMinimumSize(*min_size)
        self.resize(*initial_size)
        self.update_buttons()

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
        self.welcome_page = pages.WelcomePage(self.installer.repo.name)
        self.dir_page = pages.DirectoryPage(self.installer.install_dir.as_posix())
        self.install_page = pages.InstallPage()
        self.stack.addWidget(self.welcome_page)
        self.stack.addWidget(self.dir_page)
        self.stack.addWidget(self.install_page)

        # Buttons
        self.back_button = QtWidgets.QPushButton("< &Back")
        self.next_button = QtWidgets.QPushButton("&Next >")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

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
        self.main_widget.setLayout(self.main_layout)

    def create_connections(self):
        self.next_button.clicked.connect(self.next_page)
        self.back_button.clicked.connect(self.previous_page)
        self.cancel_button.clicked.connect(self.close)
        self.stack.currentChanged.connect(self.update_buttons)
        self.dir_page.dir_widget.line_edit.textChanged.connect(self.installer.set_install_dir)
        Logger.signal_handler().emitter.message_logged.connect(self.install_page.log_output.append)
        self.installer.done.connect(lambda: self.cancel_button.setText("Close"))

    @QtCore.Slot()
    def next_page(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)
        if self.stack.currentIndex() == self.stack.indexOf(self.install_page):
            self.installer.run()

    @QtCore.Slot()
    def previous_page(self):
        current_index = self.stack.currentIndex()
        if current_index > 0:
            self.stack.setCurrentIndex(current_index - 1)

    @QtCore.Slot()
    def update_buttons(self):
        current_index = self.stack.currentIndex()
        self.back_button.setDisabled(current_index == 0)
        self.back_button.setVisible(current_index != self.stack.indexOf(self.install_page))
        self.next_button.setVisible(current_index != self.stack.indexOf(self.install_page))


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
