from os import getcwd, listdir
from os.path import isdir, isfile, join, splitext

valid_file_extensions = [".mp3", ".wav", ".ogg", ".flac"]


class FileHandler:
    """Class to handle files"""

    def __init__(self, wd: str = ""):
        if wd:
            self.working_directory = wd
        else:
            self.working_directory = getcwd()

        self.files = []
        self.folders = []
        self.amt_of_files = 0

        if isdir(self.working_directory):
            self.get_files()

    def get_files(self) -> None:
        """Gets files in the current working directory and returns it as a list of files names"""
        self.files = []
        for file in listdir(self.working_directory):
            if isfile(join(self.working_directory, file)):
                ext = splitext(file)[1]
                if ext in valid_file_extensions:
                    self.files.append(file)
            else:
                self.files.append(file)
        self.amt_of_files = len(self.files)
        return

    def set_working_directory(self, new_directory: str) -> None:
        """Sets current working directory and gets files within"""
        if isdir(new_directory):
            self.working_directory = new_directory
            self.get_files()
        else:
            print("Not a valid working directory")
        return
