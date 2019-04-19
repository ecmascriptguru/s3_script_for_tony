import sys, os, argparse, csv
from .config import Config
from .consts import ENCODING_TYPES
from .s3 import S3Manager
from .utils import clean_string, clean_string


class Gluefy(object):
    """Gluefy class
    """
    column_name = 'new_column'
    column_value = 'new_value'
    headers_set = []
    path_to_files = Config.DOWNLOAD_FILES_PATH

    def __init__(self, *args, **kwargs):
        if kwargs.get('column_name'):
            self.column_name = kwargs.pop('column_name')
            
        if kwargs.get('column_value'):
            self.column_value = kwargs.pop('column_value')

    def glue_headers(self, header_row):
        for header in header_row:
            clean_header = clean_string(header)
            if clean_header not in self.headers_set:
                self.headers_set.append(clean_header)

    def setup_headers(self, file):
        with open(file) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                self.glue_headers(row)
                break

    def data_set_generator(self, row):
        data_set = {}
        for header in row.keys():
            try:
                data_set[clean_string(header)] = removeNonAscii(row[header])
            except:
                data_set[clean_string(header)] = row[header]

        data_set[clean_string(self.column_name)] = self.column_value
        return data_set

    def write_header(self):
        with open(os.path.join(Config.MERGED_FILES_PATH, 'merged_file.csv'), 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, fieldnames=self.headers_set)
            writer.writeheader()

    def write_data(self, row):
        with open(os.path.join(Config.MERGED_FILES_PATH, 'merged_file.csv'), 'a+') as csvfile:
            writer = csv.DictWriter(
                csvfile, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, fieldnames=self.headers_set)
            writer.writerow(self.data_set_generator(row))

    def gluefy(self, file, encoding=ENCODING_TYPES.unicode):
        with open(file, encoding=encoding) as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            try:
                for row in csv_reader:
                    self.write_data(row)
            except Exception as e:
                print(str(e))
                if encoding != ENCODING_TYPES.latin:
                    print("Exception found in %s. Retrying with %s..." % (encoding, ENCODING_TYPES.latin))
                    self.gluefy_with_latin(file)

    def gluefy_with_latin(self, file):
        with open(file, encoding=ENCODING_TYPES.latin) as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            try:
                for row in csv_reader:
                    self.write_data(row)
            except Exception as e:
                print("Failed to gluefy due to encoding issue")
                print(str(e))

    def run(self):
        # s3 = S3Manager()
        # s3.download_all_files(download_path=self.path_to_files)

        for file in os.listdir(self.path_to_files):
            if file.endswith('.csv'):
                self.setup_headers(os.path.join(self.path_to_files, file))

        custom_header = clean_string(self.column_name)
        if custom_header not in self.headers_set:
            self.headers_set.append(custom_header)

        self.write_header()

        for file in os.listdir(self.path_to_files):
            if file.endswith('.csv'):
                self.gluefy(os.path.join(self.path_to_files, file))


def gluefile():
    parser = argparse.ArgumentParser()
    parser.add_argument("gluefile", type=None)
    parser.add_argument("--column_name", type=str, help="the base")
    parser.add_argument("--column_value", type=str, help="the base")
    args = parser.parse_args()

    gluefier = Gluefy(column_name=args.column_name, column_value=args.column_value)
    gluefier.run()


if __name__ == '__main__':
    gluefile(parser)
