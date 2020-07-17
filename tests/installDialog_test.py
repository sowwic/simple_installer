import os
from dsInstaller import installUI
from dsInstaller import installFn
from dsInstaller import styles
from PySide2 import QtWidgets

if __name__ == "__main__":
    # Init installer
    Installer = installFn.Installer(fileUrl="https://github.com/S0nic014/dsRenamingTool/archive/1.0.zip")

    # Create app
    app = QtWidgets.QApplication(os.sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    app.setPalette(styles.darkPallete())

    # Create main window
    window = installUI.InstallDialog(title="Test Installer", installer=Installer, minSize=[400, 200])
    window.show()

    app.exec_()
