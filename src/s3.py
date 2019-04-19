import boto3
from .config import Config, os


class S3Manager:
    resource = None

    def __init__(self, *args, **kwargs):
        # Check if required config was given for AWS S3
        if not Config.AWS_ACCESS_KEY or not Config.AWS_SECRET_KEY or\
            not Config.AWS_SOURCE_BUCKET or not Config.AWS_DESTINATION_BUCKET:
            raise Exception("AWS INFO Not found. Check config.py")

        # Initialize s3 resource
        self.resource = boto3.resource(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY)
        

    def download_all_files(self, folder_path=Config.AWS_SOURCE_FOLDER_PATH):
        """Download all of *.csv files from sepcific folder of given S3 bucket.
        - folder_path: optional
        folder path will be taken from config.py unless given
        """
        source_bucket = self.resource.Bucket(Config.AWS_SOURCE_BUCKET)
        for obj in source_bucket.objects.filter(Prefix=folder_path):
            if obj.key.endswith('.csv'):
                file_name = obj.key.split('/')[-1]
                source_bucket.download_file(obj.key, os.path.join(Config.DOWNLOAD_FILES_PATH, file_name))

    def upload_all_files(
            self, folder_path=Config.AWS_DESTINATION_FOLDER_PATH, file_name=None):
        """Upload all csv files existing in merged folder to specified folder 
        of the given destination s3 bucket
        - folder_path: optional, s3 bucket path
        - file_name: optional, default name of files uploading to s3 bucket
        """
        target_bucket = self.resource.Bucket(Config.AWS_DESTINATION_BUCKET)
        for file in os.listdir(Config.MERGED_FILES_PATH):
            if file.endswith('.csv'):
                pass
