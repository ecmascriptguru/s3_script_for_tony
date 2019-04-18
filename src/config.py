import os, json


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_FILE = os.path.join(BASE_DIR, 'env.json')
if not os.path.exists(ENV_FILE):
    raise Exception("""ENV file not found.
    You have to place env.json in project root folder.
    You can copy env.json.example file to get the template.
    """)

try:
    with open(ENV_FILE) as f:
        ENV_JSON = json.load(f)
except Exception as e:
    print("Failed to load ENV file.")
    raise Exception(str(e))

class Config(object):
    AWS_ACCESS_KEY = ""
    AWS_SECRET_KEY = ""
    AWS_SOURCE_BUCKET = "source"
    AWS_SOURCE_FOLDER_PATH = "/source/path"
    AWS_DESTINATION_BUCKET = "destination"
    AWS_DESTINATION_FOLDER_PATH = "destination/path"
    DESTINATION_FILE_NAME_TEMPLATE = "result_file_"
