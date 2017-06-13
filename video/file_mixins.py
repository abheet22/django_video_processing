import time
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import re


def sanitised_file_name(file_name):
    pattern = re.compile(r'\s+')
    file_name = re.sub(pattern,'',file_name)
    return file_name


class VideoFileUploadMixin(object):


    valid_file_extension = settings.FILE_EXTENSION_VIDEO
    valid_file_size = settings.MAX_FILE_SIZE_VIDEO

    def __init__(self,file,file_unique_id,file_path):
        self.file = file
        self.file_unique_id = file_unique_id
        self.file_path = file_path
        self.video_name = None

    def is_file_extension_valid(self):
        file_name = self.file.name
        file_data= file_name.split('.')
        if file_data[-1] in self.valid_file_extension:
            return True
        return False

    def get_file_size(self):
        return self.file.size

    def get_file_format(self):
        return self.file.name.split('.')[-1]

    def upload_file_path(self):
        # /path_to_media/media/intent/responses/intent_id
        folder_path = os.path.join(settings.MEDIA_ROOT,
                                   self.file_path,str(self.file_unique_id))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    def is_file_dimension_valid(self):
        if self.file.size <= self.valid_file_size:
            return True
        else:
            raise Exception("File size is too large")

    def is_file_valid(self):
        if self.is_file_dimension_valid() and\
                            self.is_file_extension_valid():
            return True
        return False

    def get_media_file_access_path(self):
        return os.path.join(
                self.file_path,str(self.file_unique_id),self.video_name)

    def make_file_name_unique(self):
        uploaded_file_name = str(self.file_unique_id) + \
                              '-' + str(time.time()) + '-'\
                                  + sanitised_file_name(
                                                self.file.name)
        return uploaded_file_name

    def get_file_access_path(self, file_name):

        # site_url = settings.SITE_URL
        media_url = settings.MEDIA_URL
        return media_url + \
               self.file_path + '/'+ \
               str(self.file_unique_id) + '/' + file_name

    def file_invalid(self):
        raise Exception("File is not valid.")
    def upload_video_process(self,folder_path):
        try:
            fileStorage = FileSystemStorage(location=folder_path)
            file = ContentFile(self.file.read())
            fileStorage.save(self.video_name, file)
        except:
            raise Exception('Video Upload Failed')
        return

    def upload_file(self):
        if self.is_file_valid():
            folder_path = self.upload_file_path()
            self.video_name = self.make_file_name_unique()
            self.upload_video_process(folder_path)
            file_access_path = self.get_file_access_path(self.video_name)
            return file_access_path
        else:
            return self.file_invalid()


class VideoUploadMixin(VideoFileUploadMixin):

    def is_file_dimension_valid(self):

        if self.file.size <= self.valid_file_size:
            return True
        else:
            raise Exception("Video size is not valid")