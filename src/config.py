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
    # AWS Credentials
    AWS_ACCESS_KEY = None
    AWS_SECRET_KEY = None

    # AWS bucket and path configuration
    AWS_SOURCE_BUCKET = None
    AWS_DESTINATION_BUCKET = None
    AWS_SOURCE_FOLDER_PATH = "source/path/"
    AWS_DESTINATION_FOLDER_PATH = "destination/path/"

    # Default result file name template you prefer
    DEFAULT_UPLOAD_FILE_NAME_TEMPLATE = "result_file_"

    # Don't need to touch.
    DOWNLOAD_FILES_PATH = os.path.join(BASE_DIR, 'storage', 'downloads')
    CLEANED_FILES_PATH = os.path.join(BASE_DIR, 'storage', 'cleans')
    MERGED_FILES_PATH = os.path.join(BASE_DIR, 'storage', 'merged')


for key in ENV_JSON:
    if hasattr(Config, key):
        setattr(Config, key, ENV_JSON[key])

if __name__ == "__main__":
    pass