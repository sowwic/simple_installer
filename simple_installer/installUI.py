import time
from PySide2 import QtWidgets
from PySide2 import QtCore
from simple_installer import installFn
from simple_installer import pages


class InstallDialog(QtWidgets.QMainWindow):
    def __init__(self, installer: installFn.Installer, parent=None, title: str = "Installer", minSize: list = [600, 400]):
        super().__init__(parent)

        self.installer = installer

        # Setup ui
        self.setMinimumSize(minSize[0], minSize[1])
        self.setWindowTitle(title)

        # Create components
        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_actions(self):
        pass

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.back_button = QtWidgets.QPushButton("< &Back")
        self.nextButton = QtWidgets.QPushButton("&Next >")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.welcome_page = pages.WelcomePage(softwareName=self.installer.repoName)
        self.install_dir_page = pages.DirectoryPage(defaultDir=self.installer.installDir)
        self.progress_page = pages.InstallPage()
        self.result_page = pages.ResultsPage(softwareName=self.installer.repoName)
        # Adjust
        self.install_dir_page.dirWidget.line_edit.setText(self.installer.installDir)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        # Pages
        self.page_stack_layout = QtWidgets.QStackedLayout()
        self.page_stack_layout.addWidget(self.welcome_page)
        self.page_stack_layout.addWidget(self.install_dir_page)
        self.page_stack_layout.addWidget(self.progress_page)
        self.page_stack_layout.addWidget(self.result_page)

        # Buttons
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.back_button)
        self.buttons_layout.addWidget(self.next_button)
        self.buttons_layout.addSpacing(20)
        self.buttons_layout.addWidget(self.cancel_button)

        self.main_widget.setLayout(self.main_layout)
        self.main_layout.addLayout(self.page_stack_layout)
        self.main_layout.addLayout(self.buttons_layout)

    def create_connections(self):
        # Buttons
        self.next_button.clicked.connect(self.nextPage)
        self.back_button.clicked.connect(self.prevPage)
        self.cancel_button.clicked.connect(self.close)
        # Directory
        self.install_dir_page.dirWidget.line_edit.textChanged.connect(self.setInstallDir)
        # Progress status
        self.installer.progress.started.connect(self.progress_page.statusLabel.setText)
        self.installer.progress.downloadStarted.connect(self.progress_page.statusLabel.setText)
        self.installer.progress.downloadFinised.connect(self.progress_page.statusLabel.setText)
        self.installer.progress.extractionStarted.connect(self.progress_page.statusLabel.setText)
        self.installer.progress.extractionFinised.connect(self.progress_page.statusLabel.setText)
        self.installer.progress.preInstallStarted.connect(self.progress_page.statusLabel.setText)
        self.installer.progress.preInstallFinised.connect(self.progress_page.statusLabel.setText)
        self.installer.progress.postInstallStarted.connect(self.progress_page.statusLabel.setText)
        self.installer.progress.postInstallFinised.connect(self.progress_page.statusLabel.setText)
        self.installer.progress.fileCreated.connect(self.progress_page.statusLabel.setText)
        self.installer.progress.done.connect(self.progress_page.statusLabel.setText)
        self.installer.progress.done.connect(self.display_result)
        # Progress completed operations
        self.installer.progress.madeProgress.connect(self.updateProgressBar)

        # Page layout
        self.page_stack_layout.currentChanged.connect(self.updateButtons)

    @QtCore.Slot(str)
    def setInstallDir(self, text):
        self.installer.installDir = text

    @QtCore.Slot()
    def updateButtons(self):
        """Changes text of next button and enables/disables back button"""
        if self.page_stack_layout.currentIndex() == self.page_stack_layout.indexOf(self.progress_page) - 1:
            self.next_button.setText("&Install")
        else:
            self.next_button.setText("&Next >")

        self.back_button.setEnabled(self.page_stack_layout.currentIndex())

    @QtCore.Slot()
    def nextPage(self):
        """
        Steps displays next element from pages stacked layout.
        If next page is installation page -> calls installer run method
        """
        self.page_stack_layout.setCurrentIndex(self.page_stack_layout.currentIndex() + 1)

    @QtCore.Slot()
    def prevPage(self):
        """If current page index is not 0 -> selects previous page from pages stacked layout"""
        if self.page_stack_layout.currentIndex():
            self.page_stack_layout.setCurrentIndex(self.page_stack_layout.currentIndex() - 1)

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
            self.progress_page.progressBar.setValue((value))
            return

        percentage = int((value / operations) * 100)
        self.progress_page.progressBar.setValue(percentage)
        QtCore.QCoreApplication.processEvents()
        time.sleep(0.5)

    @QtCore.Slot(str, str)
    def display_result(self, status: str, description: str = ""):
        """
        Progresses installation to result page

        :param status: status of installtion. Any status besides success will trigger failed message
        :type status: str
        :param description: Any aditional description. Will be displayed after status message, defaults to ""
        :type description: str, optional
        """
        self.page_stack_layout.setCurrentWidget(self.result_page)
        self.result_page.setResult(status, description)
        self.cancel_button.setText("Close")

    def run_installer(self):
        """
        Runs installer.
        InstallFailedException: progresses to result page with exception message as description
        """
        self.page_stack_layout.setCurrentWidget(self.progress_page)
        self.back_button.hide()
        self.next_button.hide()
        time.sleep(0.5)
        try:
            self.installer.run()
        except installFn.InstallFailedException as e:
            self.display_result("failed", e.args[0])
