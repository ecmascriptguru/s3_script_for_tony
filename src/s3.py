import boto3, argparse
from .config import Config, os


class S3Manager:
    resource = None
    bucket = Config.AWS_DESTINATION_BUCKET
    path = Config.AWS_DESTINATION_FOLDER_PATH
    filename = Config.DEFAULT_UPLOAD_FILE_NAME_TEMPLATE

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
        
        if kwargs.get('bucket'):
            self.destination_bucket_name = kwargs.pop('bucket')
        
        if kwargs.get('path'):
            self.destination_bucket_name = kwargs.pop('path')
        
        if kwargs.get('filename'):
            self.destination_bucket_name = kwargs.pop('filename')

    def download_all_files(
            self,
            aws_folder_path=Config.AWS_SOURCE_FOLDER_PATH, 
            download_path=Config.DOWNLOAD_FILES_PATH):
        """Download all of *.csv files from sepcific folder of given S3 bucket.
        - aws_folder_path: optional
        - download_path: optional
        folder path will be taken from config.py unless given
        """
        source_bucket = self.resource.Bucket(Config.AWS_SOURCE_BUCKET)
        for obj in source_bucket.objects.filter(Prefix=aws_folder_path):
            if obj.key.endswith('.csv'):
                file_name = obj.key.split('/')[-1]
                source_bucket.download_file(obj.key, os.path.join(download_path, file_name))

    def upload_all_files(self, filename=None, **kwargs):
        """Upload all csv files existing in merged folder to specified folder 
        of the given destination s3 bucket
        - aws_folder_path: optional, s3 bucket path
        - filename: optional, default name of files uploading to s3 bucket
        """

        if len([x for x in os.listdir(Config.CLEANED_FILES_PATH) if x.endswith('.csv')]) == 0:
            current_path = Config.MERGED_FILES_PATH
        else:
            current_path = Config.CLEANED_FILES_PATH

        target_bucket = self.resource.Bucket(self.bucket)

        if filename is None:
            filename = self.filename

        if not filename.endswith('.csv'):
            filename += '.csv'

        file_index = 0
        for file in os.listdir(current_path):
            if file.endswith('.csv'):
                if filename:
                    if file_index > 0:
                        upload_filename = "%s_%d.csv" % ('.'.join(filename.split('.')[:-1]), file_index)
                    else:
                        upload_filename = "%s.csv" % ('.'.join(filename.split('.')[:-1]))
                else:
                    upload_filename = file
                try:
                    target_bucket.upload_file(
                        os.path.join(current_path, file),
                        os.path.join(Config.AWS_DESTINATION_FOLDER_PATH, upload_filename))
                except Exception as e:
                    print(str(e))


def upload_all():
    parser = argparse.ArgumentParser()
    parser.add_argument("upload", type=None)
    parser.add_argument("--bucket", type=str, help="the base")
    parser.add_argument("--path", type=str, help="the base")
    parser.add_argument("--filename", type=str, help="the base")
    args = parser.parse_args()

    uploader = S3Manager(**args.__dict__)
    uploader.upload_all_files(args.filename)


if __name__ == "__main__":
    upload_all()
