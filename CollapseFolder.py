__author__ = 'James Hertan'
#November 2015

from os import listdir, rename, makedirs
from os.path import exists, join, isfile
from datetime import date, datetime

class CollapseFolder:
    """
    Create an arbitrary object and provide a directory to archive the directories loose files into a CURRENT_YEAR folder.
    """
    def __init__(self, folder_to_process_path):
        self.path = folder_to_process_path
        self.today = date.today()
        self.target_directory_name = str(self.today.year)

        try:
            self.loose_files = [file for file in listdir(self.path) if isfile(join(self.path, file))]
        except FileNotFoundError as e:
            print("Path not found.\n{}".format(e))
        finally:
            if exists(self.path):
                self.move_files()
            else:
                print("The path entered for processing is invalid.\nBatch process ending...")

    def target_directory_exists(self):
        """
        Input: path, target_directory_name
        Output: True if target_directory_name exists, else false
        """
        return True if (exists(join(self.path, self.target_directory_name))) else False

    def create_target_directory(self):
        """
        Input: path, target_directory_name
        Output: creates a new folder in the path with target_directory_name
        """
        try:
            makedirs(join(self.path, self.target_directory_name))
            print("Folder '{}' created.".format(self.target_directory_name))
        except FileExistsError as e:
            print("Can not create a new folder for {}.\n '{}'".format(self.target_directory_name, e))

    def move_files(self):
        """
        Input: path, target_directory_name, loose_files of the path directory
        Dependencies: A method 'target_directory_exists' to create the target directory if it doesn't exist.
        """
        logger = list()
        logger_filename = join(self.path,'CollapseFolder_Log_' + str(self.today.month) + '_' + str(self.today.day) + '_' + str(self.today.year) + '.txt')


        if not self.target_directory_exists():   #target directory exists?
            self.create_target_directory()

        for file in self.loose_files:           #move files
            if file == logger_filename:
                continue
            else:
                try:
                    rename(join(self.path, file), join(self.path, self.target_directory_name, file))
                    print("{} moved!".format(file))
                    logger.append(file)
                except FileExistsError as e:
                    pass

        if exists(logger_filename):             #log what we've done
            with open(logger_filename, 'a') as file_log:
                file_log.write('CollapseFolder process run on ' + str(self.today.month) + '/' + str(self.today.day) + '/' + str(self.today.year) + ' at ' + str(datetime.now().hour) + ':' + str(datetime.now().minute) + ':' + str(datetime.now().second)+ '.\n')
                file_log.write("Moved {} files from '{}' to '{}'\n\n".format(len(logger), self.path, join(self.path, self.target_directory_name)))
                for n, file in enumerate(logger):
                    file_log.write(str(n+1) + ': ' + file + '\n')
                file_log.write('************\n')
                print("Existing log file updated: '{}'".format(self.path))
        else:
            with open(logger_filename, 'w+') as file_log:
                file_log.write('CollapseFolder process run on ' + str(self.today.month) + '/' + str(self.today.day) + '/' + str(self.today.year) + str(datetime.now().hour) + ':' + str(datetime.now().minute) + ':' + str(datetime.now().second) + '.\n')
                file_log.write("Moved {} files from '{}' to '{}.'\n\n".format(len(logger), self.path, join(self.path, self.target_directory_name)))
                for n, file in enumerate(logger):
                    file_log.write(str(n+1) + ': ' + file + '\n')
                file_log.write('************\n')
                print("Log file generated here: '{}'".format(self.path))



def main():
    path = 'C:\FOLDER1\FOLDER2'   #path folder goes here....
    p = CollapseFolder(path)


if __name__ == "__main__":
    main()
