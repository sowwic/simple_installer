import os
import zipfile
import urllib.request


class Installer(object):

    DEFAULT_DIR = os.getenv("programfiles")

    def __init__(self, installDir: str = "", fileUrl: str = ""):
        # Init data
        self.installDir = installDir
        self.repoName = ""
        self.fileUrl = fileUrl
        self.tempPath = os.path.join(os.getenv("TEMP"), "temp_{0}.zip".format(self.repoName))

    @property
    def fileUrl(self):
        return self._fileUrl

    @fileUrl.setter
    def fileUrl(self, url):
        self._fileUrl = url
        self.repoName = url.split("/")[-3]

    @staticmethod
    def createFile(dirPath: str, fileName: str, fileData=""):
        """Creates file in a given directory

        :param dirPath: Root directory for new file
        :type dirPath: str
        :param fileName: New file name with extension
        :type fileName: str
        :param fileData: Data to write to the file, defaults to ""
        :type fileData: str, optional
        """
        filePath = os.path.join(dirPath, fileName)
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)

        if fileData:
            with open(filePath, "w") as modFile:
                modFile.write(fileData)

    @staticmethod
    def removeVersion(path):
        """Removes -ver from folder name

        :param path: Path to file/dir operate on
        :type path: str
        :return: New path to file/dir
        :rtype: str
        """
        versionedName = path.split("/")[-2]
        cleanName = versionedName.split("-")[0]
        cleanPath = path.replace(versionedName, cleanName)
        os.rename(path, cleanPath)
        return cleanPath

    def downloadFile(self):
        """Downloads file from given fileUrl

        :return: 1 if success
        :rtype: int
        """
        with urllib.request.urlopen(self.fileUrl) as dlFile:
            with open(self.tempPath, "wb") as outFile:
                outFile.write(dlFile.read())
        return 1

    def extractTempFile(self):
        """Extract temporary zip file to installation dir

        :return: Path to extracted root folder
        :rtype: str
        """
        tempZip = zipfile.ZipFile(self.tempPath)
        rootFolder = tempZip.namelist()[0]
        tempZip.extractall(self.installDir)
        return os.path.join(self.installDir, rootFolder)

    def preInstall(self):
        """Override"""
        pass

    def postInstall(self):
        """Override"""
        pass

    def run(self):
        """Run installation"""
        # Pre
        self.preInstall()
        # INSTALL
        self.downloadFile()
        extractedFolder = self.extractTempFile()
        self.removeVersion(extractedFolder)
        # Post
        self.postInstall()
        # Cleanup
        os.remove(self.tempPath)