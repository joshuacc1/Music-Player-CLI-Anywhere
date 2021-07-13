from os import getcwd, listdir
from os.path import isdir, isfile, join


class FileHandling:
    """Class to handle files"""

    def __init__(self):
        self.files = []
        self.working_directory = getcwd()
        self.amt_of_files = 0

    def get_files(self) -> None:
        """Gets files in the current working directory and returns it as a list of files names"""
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
