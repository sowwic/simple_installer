from PySide2 import QtWidgets
import os
import sys
import elevate
import simple_installer


def test_install():
    # Init installer
    api_token = os.getenv("INSTALLER_TOKEN")
    installer = simple_installer.Installer(repo_name="S0nic014/dsPlayblast",
                                           api_token=api_token)
    # Create app
    app = QtWidgets.QApplication(sys.argv)
    window = simple_installer.InstallerWindow(installer, title="Test installer")
    window.show()
    app.exec_()


if __name__ == "__main__":
    elevate.elevate(show_console=False)
    test_install()
