import mimetypes
import os
import uuid

from django.conf import settings
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadTo:
    """
    This utility provides a cross-application, cross-model generalised way for
    storing files based on a UUID naming scheme
    """

    def __init__(self, app_name, folder_name, file_manager=False, base_location=''):
        """
        Initialise a callable instance of the class with the given parameters
        :param app_name: the name of the app using this utility
        :param folder_name: the name of the folder where to write the file
        :param file_manager: whether the app using this utility is File Manager
        """

        self.app_name = app_name
        self.folder_name = folder_name
        self.file_manager = file_manager
        self.base_location = base_location

    def __call__(self, instance, filename):
        """
        Compute the location of where to store the file, removing any
        existing file with the same name
        :param instance: the instance to which file is being uploaded
        :param filename: the original name of the file, used for the extension
        :return: the path to the uploaded image
        """

        # Path upto the file
        if self.file_manager:
            if type(instance).__name__ == "File":
                folder_name = str(instance.folder.path)
                self.app_name = str(
                    instance.folder.filemanager.filemanager_name)
            else:
                folder_name = self.folder_name
            if type(instance).__name__ == "FileManager":

                if instance.is_public:
                    self.base_location = 'public'
                else:
                    self.base_location = 'protected'

            elif type(instance).__name__ == 'File':
                if instance.folder.filemanager.is_public:
                    self.base_location = 'public'
                else:
                    self.base_location = 'protected'

        else:
            folder_name = self.folder_name

        path = os.path.join(
            self.app_name,
            folder_name,
        )
        updated_filename = self.get_file_name(path, filename)
        # Full path to the file
        destination = os.path.join(
            self.base_location,
            self.app_name,
            folder_name,
            updated_filename,
        )
        return destination

    def get_file_name(self, path, filename):
        """
        Return Updated file name in case of file already exists 
        :param path: path of folder in which the file will be stored 
        :param filename: the original name of the file
        :return: the path to the uploaded image
        """
        
        name, ext = os.path.splitext(filename)
        newpath = path+'/'+filename
        newname = filename
        counter = 0
        while os.path.exists(newpath):
            newname = name+'_' + str(counter) + ext
            newpath = path+'/'+newname
            counter = counter + 1
        return newname
