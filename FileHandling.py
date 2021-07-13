from os import getcwd, listdir
from os.path import isdir, isfile, join

valid_file_extensions = ["mp3"]


class FileHandler:
    """Class to handle files"""

    def __init__(self, wd: str = ""):
        if wd:
            self.working_directory = wd
        else:
            self.working_directory = getcwd()

        self.files = []
        self.amt_of_files = 0

        if isdir(self.working_directory):
            self.get_files()

    def get_files(self) -> None:
        """Gets files in the current working directory and returns it as a list of files names"""
        # TODO: add valid file extensions, a recursive check in the current cwd for music files (optional flag)
        self.files = [file for file in listdir(self.working_directory) if isfile(join(self.working_directory, file))]
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