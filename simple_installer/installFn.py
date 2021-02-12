import os
import pathlib
import zipfile
import urllib.request
import shutil
import platform
from PySide2 import QtCore
from github import Repository


class InstallFailedException(Exception):
    """Raise to progress install dialog to result page with error description"""
    pass


class Installer(QtCore.QObject):
    # Progress signals
    started = QtCore.Signal()
    pre_install_started = QtCore.Signal()
    pre_install_completed = QtCore.Signal()
    post_install_started = QtCore.Signal()
    post_install_completed = QtCore.Signal()
    cleanup_started = QtCore.Signal()
    cleanup_completed = QtCore.Signal()
    file_created = QtCore.Signal(str)
    done = QtCore.Signal(int)
    made_progress = QtCore.Signal(int, int, str)
    # Status signals
    directory_changed = QtCore.Signal(str)
    repo_changed = QtCore.Signal(Repository)

    def __init__(self, install_dir: pathlib.Path = "", repo_url: str = ""):
        # Init data
        self.install_dir = install_dir
        self.temp_path = pathlib.Path(os.getenv("TEMP"), pathlib.Path.cwd() / "temp") / f"temp_{self.repoName}.zip"
        self.repo = Repository.Repository()

    @property
    def default_dir(self):
        if platform.system() == "Windows":
            return os.getenv("programfiles", "")
        else:
            return ""

    @property
    def install_dir(self):
        return self._install_dir

    @install_dir.setter
    def install_dir(self, path):
        self._install_dir = pathlib.Path(path)
        self.directory_changed.emit(self._install_dir)

    @property
    def repo(self) -> Repository:
        return self._repo

    @repo.setter
    def repo(self, repo: Repository):
        self._repo = repo
        self.repo_changed.emit(repo)

    def create_file(self, file_path: pathlib.Path, data="", encoding: str = None) -> None:
        try:
            if not file_path.exists():
                file_path.mkdir()

            if data:
                file_path.write_text(data, encoding=encoding)

            self.progress.file_created.emit(f"Created file: {file_path.as_posix()}")
        except Exception:
            raise InstallFailedException(f"Failed to create file {file_path.as_posix()}")

    def preInstall(self) -> None:
        """Override"""
        pass

    def postInstall(self) -> None:
        """Override"""
        pass

    def run(self) -> None:
        """Run installation"""
        self.started.emit()
        self.made_progress.emit(0, 6, "Initializing...")

        # Pre
        self.pre_install_started.emit()
        self.preInstall()
        self.pre_install_completed.emit()
        self.made_progress.emit(1, 6, "Pre install tasks completed.")

        # INSTALL
        # self.download_file()
        # self.progress.madeProgress.emit(2, 6)
        # extractedFolder = self.extractTempFile()
        # self.progress.madeProgress.emit(3, 6)
        # self.removeVersion(extractedFolder)
        # self.progress.madeProgress.emit(4, 6)

        # Post
        self.post_install_started.emit()
        self.postInstall()
        self.post_install_completed.emit()
        self.progress.madeProgress.emit(5, 6, "Post install tasks completed")

        # Cleanup
        self.cleanup_started.emit()
        os.remove(self.temp_path)
        self.cleanup_completed.emit()
        self.made_progress(6, 6, "Done.")
        self.done.emit(0)
