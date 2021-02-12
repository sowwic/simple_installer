from PySide2 import QtWidgets
import simple_installer.common_widgets as common_widgets


class WelcomePage(QtWidgets.QWidget):
    def __init__(self, software_name: str = "Program", parent=None):
        super().__init__(parent)

        self.title_text = f"Welcome to the {software_name} Setup Wizard"
        self.welcome_text = f"""The Setup Wizard will install {software_name} on your computer.\nClick Next to continue or Cancel to exit Setup wizard"""

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.title_label = QtWidgets.QLabel(self.title_text)
        self.title_label.setStyleSheet("font-weight: bold;")
        self.title_label.setWordWrap(1)
        self.message_label = QtWidgets.QLabel(self.welcome_text)
        self.message_label.setWordWrap(1)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.message_label)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def create_connections(self):
        pass


class DirectoryPage(QtWidgets.QWidget):
    def __init__(self, default_dir: str, parent=None):
        super().__init__(parent)
        self.default_dir = default_dir
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.dir_widget = common_widgets.DirectoryWidget(default_dir=self.default_dir)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.dir_widget)
        self.setLayout(self.main_layout)

    def create_connections(self):
        pass


class InstallPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.status_label = QtWidgets.QLabel()
        self.progress_bar = QtWidgets.QProgressBar()
        self.log_output = QtWidgets.QTextEdit()
        self.log_output.setReadOnly(True)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addWidget(self.log_output)
        self.setLayout(self.main_layout)

    def create_connections(self):
        pass


class ResultsPage(QtWidgets.QWidget):
    def __init__(self, software_name: str = "Program", parent=None):
        super().__init__(parent)
        self.software_name = software_name
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.title = QtWidgets.QLabel()
        self.title.setStyleSheet("font-weight: bold;")
        self.message = QtWidgets.QLabel()
        self.message.setWordWrap(1)
        self.description = QtWidgets.QLabel()
        self.description.setStyleSheet("font-weight: bold;")
        self.description.setWordWrap(1)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.message)
        self.main_layout.addWidget(self.description)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def create_connections(self):
        pass

    def set_result(self, status, description=""):
        if status != "success":
            self.title.setText("Installation failed!")
            self.message.setText(f"There was an error during installation of {self.software_name}")
            if description:
                self.description.setText(description)
            return status

        self.title.setText("Installation completed.")
        self.message.setText(f"{self.software_name} was installed successfully")
