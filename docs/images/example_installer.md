
```py
import pathlib
import os
import sys
import elevate
from PySide2 import QtWidgets
import simple_installer.pages as pages
from simple_installer import Installer
from simple_installer import InstallerWindow


class dsToolInstaller(Installer):
    def __init__(self, api_token: str) -> None:
        super().__init__(repo_name="S0nic014/dsRenamingTool", api_token=api_token)
        self.tool_version = self.repo.get_latest_release().tag_name
        self.tool_name = self.repo.name
        self.maya_modules_dir = pathlib.Path().home() / "Documents" / "maya" / "modules"
        self.module_file_data = ""

    def post_install(self):
        """Creates .mod file with path to installed tool"""
        installed_path = self.install_dir / self.tool_name
        self.module_file_data = f"+ {self.tool_name} {self.tool_version} {installed_path}"\
                                f"\nscripts: {installed_path}"
        self.create_file(self.maya_modules_dir / f"{self.tool_name}.mod", self.module_file_data)


class dsInstallDialog(InstallerWindow):
    def __init__(self, installer: dsToolInstaller, title="dsRenamingTool Installer"):
        super(dsInstallDialog, self).__init__(installer=installer, title=title)
        self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DriveDVDIcon))

    def create_widgets(self):
        super().create_widgets()
        self.mod_page = pages.DirectoryPage(default_dir=self.installer.maya_modules_dir.as_posix())
        self.mod_page.dir_widget.group.setTitle("Maya modules folder")
        self.stack.insertWidget(2, self.mod_page)

    def create_connections(self):
        super().create_connections()
        self.mod_page.dir_widget.line_edit.textChanged.connect(self.set_modules_dir)

    def set_modules_dir(self, path: str):
        self.installer.maya_modules_dir = pathlib.Path(path)
        print(self.installer.maya_modules_dir)


def main():
    api_token = os.getenv("INSTALLER_TOKEN")
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