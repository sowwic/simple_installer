
```py
import pathlib
import sys
import elevate
from PySide2 import QtWidgets
from PySide2 import QtCore
import simple_installer.pages as pages
from simple_installer import Installer
from simple_installer import InstallerWindow


class dsToolInstaller(Installer):
    def __init__(self, api_token: str) -> None:
        super().__init__(repo_name="S0nic014/dsRenamingTool", api_token=api_token)
        self.tool_version = self.repo.get_latest_release().tag_name
        self.tool_name = self.repo.name
        self.maya_modules_dir = pathlib.Path().home() / "Documents" / "maya" / "modules"
        self.module_file_path = self.maya_modules_dir / f"{self.tool_name}.mod"
        self.module_file_data = ""

    def post_install(self):
        """Creates .mod file with path to installed tool"""
        installed_path = self.install_dir / self.tool_name
        self.module_file_data = f"+ {self.tool_name} {self.version} {installed_path}"\
                                "\nscripts: {installed_path}"
        self.createFile(self.module_file_path, self.module_file_data)


class dsInstallDialog(InstallerWindow):
    def __init__(self, installer: dsToolInstaller, title="dsRenamingTool Installer"):
        super(dsInstallDialog, self).__init__(installer=installer, title=title)
        self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DriveDVDIcon))

    def create_widgets(self):
        super().create_widgets()
        self.mod_page = pages.DirectoryPage(default_dir=self.installer.maya_modules_dir)
        self.mod_page.dirWidget.group.setTitle("Maya modules folder")
        self.stack.insertWidget(2, self.mod_page)

    def createConnections(self):
        super().createConnections()
        self.mod_page.dir_widget.line_edit.textChanged.connect(self.set_modules_dir)

    @QtCore.Slot(str)
    def set_modules_dir(self, path: str):
        self.installer.maya_modules_dir = pathlib.Path(path)


def main():
    api_token = ""
    toolInstall = dsToolInstaller(api_token)
    # Create app
    app = QtWidgets.QApplication(sys.argv)
    window = dsInstallDialog(title="dsRenamingTool Installer", installer=toolInstall)
    window.show()
    app.exec_()


if __name__ == "__main__":
    elevate.elevate(show_console=False)
    main()

```