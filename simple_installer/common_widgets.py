from PySide2 import QtWidgets


class DirectoryWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, default_dir: str = "", title: str = "Destination", browse_title: str = "Select directory"):
        """
        Widget containing groupBox, lineEdit and button widgets.
        Button triggers QFileDialog.getExistingDirectory method and sets lineEdit text to path returned from it.

        :param parent: Widget parent, defaults to None
        :type parent: QtWidget, optional
        :param default_dir: Default text to use for lineEdit text, defaults to ""
        :type default_dir: str, optional
        :param title: Group box title, defaults to "Destination"
        :type title: str, optional
        :param browse_title: QFileDialog window title, defaults to "Select directory"
        :type browse_title: str, optional
        """
        super().__init__(parent)
        self.default_dir = default_dir
        self.title = title
        self.browse_title = browse_title

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.group = QtWidgets.QGroupBox(self.title)
        self.line_edit = QtWidgets.QLineEdit(self.default_dir)
        self.browse_button = QtWidgets.QPushButton("Browse...")

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.group_layout = QtWidgets.QHBoxLayout()
        self.group_layout.addWidget(self.line_edit)
        self.group_layout.addWidget(self.browse_button)
        self.group.setLayout(self.group_layout)
        self.main_layout.addWidget(self.group)
        self.main_layout.addStretch()

    def create_connections(self):
        self.browse_button.clicked.connect(self.browse_path)

    def browse_path(self):
        """Get directory path from QFileDialog"""
        path = QtWidgets.QFileDialog.getExistingDirectory(self, self.browse_title, self.line_edit.text())
        if path:
            self.line_edit.setText(path)
