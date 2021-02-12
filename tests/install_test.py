from PySide2 import QtWidgets
import sys
import elevate
import simple_installer


def test_install():
    # Init installer
    installer = simple_installer.Installer(fileUrl="https://github.com/S0nic014/dsRenamingTool/archive/1.0.zip")

    # Create app
    app = QtWidgets.QApplication(sys.argv)
    # Create main window
    window = simple_installer.InstallerWindow(installer, title="Test installer", min_size=(400, 200))
    window.show()
    app.exec_()


if __name__ == "__main__":
    elevate.elevate(show_console=False)
    test_install()
