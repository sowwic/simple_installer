import os
import pathlib
import platform
import requests
import shutil
from zipfile import ZipFile
from PySide2 import QtCore
from PySide2 import QtWidgets
from github import Github
from github import Repository
from github import GithubException
from simple_installer import Logger


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
    made_progress = QtCore.Signal(int, int)
    # Status signals
    directory_changed = QtCore.Signal(str)
    repo_changed = QtCore.Signal(Repository.Repository)

    # Exception
    class FailedException(Exception):
        """Raise to progress install dialog to result page with error description"""
        pass

    def __init__(self, install_dir: str = "", repo_name: str = "", api_token=""):
        super().__init__(parent=None)

        # Init data
        self.init_repo(api_token, repo_name)
        self.install_dir = install_dir
        if not self.install_dir.is_dir():
            self.install_dir = self.default_dir

    @property
    def default_dir(self):
        if platform.system() == "Windows":
            return os.getenv("programfiles", "")
        else:
            return "."

    @property
    def install_dir(self) -> pathlib.Path:
        return self._install_dir

    @install_dir.setter
    def install_dir(self, path):
        self._install_dir = pathlib.Path(path)
        self.directory_changed.emit(self._install_dir)

    @property
    def repo(self) -> Repository.Repository:
        return self._repo

    @repo.setter
    def repo(self, repo: Repository):
        self._repo = repo
        self.repo_changed.emit(repo)

    def init_repo(self, api_token, repo_name):
        git = Github(api_token)
        self.repo = git.get_repo(full_name_or_id=repo_name)

    def set_install_dir(self, path: str):
        self.install_dir = path

    def create_file(self, file_path: pathlib.Path, data="", encoding: str = None) -> None:
        Logger.info(f"Creating file {file_path.as_posix()}")
        try:
            file_path.write_text(data, encoding=encoding)
            self.file_created.emit(file_path.as_posix())
            Logger.info(f"Created file: {file_path.as_posix()}")
        except Exception:
            Logger.exception(f"Failed to create file {file_path.as_posix()}")
            raise Installer.FailedException()

    def download_latest_source(self, download_path: pathlib.Path):
        Logger.info(f"Downloading latest release for {self.repo.name}")
        try:
            release = self.repo.get_latest_release()
            self.download_file(release.zipball_url, download_path.as_posix())
        except GithubException:
            Logger.exception(f"Failed to get latest release for {self.repo.full_name}")
            raise Installer.FailedException()

    def download_latest_asset(self, download_dir: pathlib.Path):
        Logger.info(f"Downloading latest asset for {self.repo.name}")
        downloaded_assets = []
        try:
            release = self.repo.get_latest_release()
            for asset in release.get_assets():
                download_path = self.install_dir / asset.name
                self.download_file(asset.browser_download_url, download_path)
                downloaded_assets.append(download_path)
            return downloaded_assets

        except GithubException:
            Logger.exception(f"Failed to get latest asset for {self.repo.full_name}")
            raise Installer.FailedException

    @classmethod
    def download_file(cls, url: str, file_path: pathlib.Path):
        Logger.info(f"Downloading file {url}")
        try:
            with requests.get(url) as req_file:
                with open(file_path.as_posix(), "wb") as local_file:
                    for chunk in req_file.iter_content(chunk_size=8192):
                        if chunk:
                            local_file.write(chunk)
            Logger.info(f"Dowloaded file to: {file_path.as_posix()}")
            return file_path
        except Exception:
            Logger.exception(f"Failed to download from: {url}")
            raise Installer.FailedException

    def extract_file(self, source: pathlib.Path, destination_dir: pathlib.Path, new_extracted_name: str = None):
        Logger.info(f"Extracting temp file {source.as_posix()}")
        try:
            zip_file = ZipFile(source)
            root_folder = zip_file.namelist()[0]
            zip_file.extractall(destination_dir)
            extracted_path = destination_dir / root_folder
            if new_extracted_name:
                final_path = destination_dir / new_extracted_name
                if final_path.is_dir():
                    answer = QtWidgets.QMessageBox.question(None,
                                                            "Existing directory",
                                                            f"Directory {final_path} already exists. Replace it?")
                    if answer == QtWidgets.QMessageBox.Yes:
                        shutil.rmtree(final_path)
                        extracted_path.rename(final_path)
                else:
                    extracted_path.rename(final_path)
            Logger.info(f"Extracted zip to {extracted_path.as_posix()}")
            return extracted_path

        except Exception:
            Logger.exception("Failed to extract file")
            raise Installer.FailedException

    def install(self) -> None:
        pass

    def pre_install(self) -> None:
        """Override"""
        pass

    def post_install(self) -> None:
        """Override"""
        pass

    def cleanup(self) -> None:
        """Override"""
        pass

    def run(self) -> None:
        """Run installation"""
        Logger.info("Initializing ...")
        self.started.emit()

        # Pre
        Logger.info("Running pre install tasks...")
        self.pre_install_started.emit()
        self.pre_install()
        self.pre_install_completed.emit()
        Logger.info("Pre install tasks completed.")

        # Install
        Logger.info("Installing...")
        self.install()
        Logger.info("Install tasks complete.")

        # Post
        Logger.info("Running post install tasks...")
        self.post_install_started.emit()
        self.post_install()
        self.post_install_completed.emit()
        Logger.info("Post install task completed.")

        # Cleanup
        Logger.info("Cleaning up...")
        self.cleanup_started.emit()
        self.cleanup()
        self.cleanup_completed.emit()
        self.done.emit(0)
        Logger.info("Done.")
