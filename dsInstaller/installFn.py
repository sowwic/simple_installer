import os
import zipfile
import urllib.request
import shutil
from PySide2 import QtCore


class Status(QtCore.QObject):
    """Helper class for status related signals"""
    installDirChanged = QtCore.Signal(str)
    fileUrlChanged = QtCore.Signal(str)
    repoNameChanged = QtCore.Signal(str)


class Progress(QtCore.QObject):
    """Helper class for progress related signals"""
    started = QtCore.Signal(str)
    downloadStarted = QtCore.Signal(str)
    downloadFinised = QtCore.Signal(str)
    extractionStarted = QtCore.Signal(str)
    extractionFinised = QtCore.Signal(str)
    preInstallStarted = QtCore.Signal(str)
    preInstallFinised = QtCore.Signal(str)
    postInstallStarted = QtCore.Signal(str)
    postInstallFinised = QtCore.Signal(str)
    fileCreated = QtCore.Signal(str)
    done = QtCore.Signal(str)
    madeProgress = QtCore.Signal(int, int)


class InstallFailedException(Exception):
    """Raise to progress install dialog to result page with error description"""
    pass


class Installer(object):

    # TODO: Add defaults for other OS
    DEFAULT_DIR = os.getenv("programfiles")

    def __init__(self, installDir: str = "", fileUrl: str = ""):
        # Init data
        self.progress = Progress()
        self.status = Status()
        self.installDir = installDir
        self.repoName = ""
        self.fileUrl = fileUrl
        self.tempPath = os.path.join(os.getenv("TEMP"), "temp_{0}.zip".format(self.repoName))

    @property
    def installDir(self):
        return self._installDir

    @installDir.setter
    def installDir(self, path: str):
        self._installDir = path
        self.status.installDirChanged.emit(path)

    @property
    def fileUrl(self):
        return self._fileUrl

    @fileUrl.setter
    def fileUrl(self, url: str):
        self._fileUrl = url
        self.repoName = url.split("/")[-3]
        self.status.fileUrlChanged.emit(url)
        self.status.repoNameChanged.emit(self.repoName)

    @staticmethod
    def removeVersion(path) -> str:
        """ Removes version or tree name from downloaded zip.
        Example: dsTool-1.0 -> dsTool
        ! Will delete an already existing directory to avoid FileAlreadyExists exception

        :param path: Path to removed version from
        :type path: str
        :raises InstallFailedException: Aborts installation
        :return: Path to a renamed directory
        :rtype: str
        """
        try:
            versionedName = path.split("/")[-2]
            cleanName = versionedName.split("-")[0]
            cleanPath = path.replace(versionedName, cleanName)
            if os.path.isdir(cleanPath):
                shutil.rmtree(cleanPath)

            os.rename(path, cleanPath)
            return cleanPath
        except Exception:
            raise InstallFailedException(f"Failed to rename directory {path}")

    def downloadFile(self):
        """Downloads file from given fileUrl

        :raises InstallFailedException: Aborts installation
        """
        self.progress.downloadStarted.emit(f"Downloading {self.fileUrl}")
        try:
            with urllib.request.urlopen(self.fileUrl) as dlFile:
                with open(self.tempPath, "wb") as outFile:
                    outFile.write(dlFile.read())
            self._returnStatus = "success"
            self.progress.downloadFinised.emit(f"Download file saved as: {self.tempPath}")
        except Exception:
            raise InstallFailedException(f"Failed to download file {self.fileUrl}")

    def extractTempFile(self) -> str:
        """Extract temporary zip file to installation dir

        :raises InstallFailedException: Aborts installation
        :return: Path to exracted directory
        :rtype: str
        """
        self.progress.extractionStarted.emit(f"Extracting {self.tempPath}")
        try:
            tempZip = zipfile.ZipFile(self.tempPath)
            rootFolder = tempZip.namelist()[0]
            tempZip.extractall(self.installDir)
            extractedPath = os.path.join(self.installDir, rootFolder)
            self.progress.extractionFinised.emit(f"Extracted to {extractedPath}")
            return extractedPath
        except Exception:
            raise InstallFailedException(f"Failed to exract file {self.tempPath}")

    def createFile(self, dirPath: str, fileName: str, fileData="") -> str:
        """Creates file in a given directory

        :param dirPath: Root directory for new file
        :type dirPath: str
        :param fileName: New file name with extension
        :type fileName: str
        :param fileData: Data to write to the file, defaults to ""
        :type fileData: str, optional
        :raises InstallFailedException: Aborts installation
        """
        try:
            filePath = os.path.join(dirPath, fileName)
            if not os.path.isdir(dirPath):
                os.mkdir(dirPath)

            if fileData:
                with open(filePath, "w") as modFile:
                    modFile.write(fileData)

            self.progress.fileCreated.emit(f"Created file: {filePath}")
            return filePath
        except Exception:
            raise InstallFailedException(f"Failed to create file {filePath}")

    def preInstall(self):
        """Override"""
        pass

    def postInstall(self):
        """Override"""
        pass

    def run(self) -> None:
        """Run installation"""
        self.progress.started.emit("Initializing")
        self.progress.madeProgress.emit(0, 6)

        # Pre
        self.preInstall()
        self.progress.madeProgress.emit(1, 6)

        # INSTALL
        self.downloadFile()
        self.progress.madeProgress.emit(2, 6)
        extractedFolder = self.extractTempFile()
        self.progress.madeProgress.emit(3, 6)
        self.removeVersion(extractedFolder)
        self.progress.madeProgress.emit(4, 6)

        # Post
        self.postInstall()
        self.progress.madeProgress.emit(5, 6)

        # Cleanup
        os.remove(self.tempPath)
        self.progress.madeProgress.emit(6, 6)
        self.progress.done.emit("success")
