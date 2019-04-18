import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class Config(object):
    AWS_ACCESS_KEY = ""
    AWS_SECRET_KEY = ""
    AWS_SOURCE_BUCKET = "source"
    AWS_SOURCE_FOLDER_PATH = "/source/path"
    AWS_DESTINATION_BUCKET = "destination"
    AWS_DESTINATION_FOLDER_PATH = "destination/path"
    DESTINATION_FILE_NAME_TEMPLATE = "result_file_"
