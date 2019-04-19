# encoding=utf-8
import sys, os, argparse, csv, re
from .config import Config
from .utils import clean_string, validate_email, clean_phone, only_letters


class CLEAN_TYPE:
    email = 'email'
    phone = 'phone'
    string = 'string'


class Cleaner(object):
    column_name = 'email'
    clean_type = CLEAN_TYPE.email
    merged_file_path = Config.MERGED_FILES_PATH
    cleaned_file_path = Config.CLEANED_FILES_PATH
    headers_set = []

    def __init__(self, *args, **kwargs):
        if kwargs.get('column_name'):
            self.column_name = kwargs.pop('column_name')
            
        if kwargs.get('clean_type'):
            self.clean_type = kwargs.pop('clean_type')

    def data_set_generator(self, data_set):
        columns_set = self.column_name.split(',')
        for header in columns_set:
            if clean_string(header) in self.headers_set:
                if self.clean_type == CLEAN_TYPE.email:
                    data_set[clean_string(header)] = validate_email(data_set[clean_string(header)])

                elif self.clean_type == CLEAN_TYPE.phone:
                    data_set[clean_string(header)] = clean_phone(data_set[clean_string(header)])

                elif self.clean_type == CLEAN_TYPE.string:
                    data_set[clean_string(header)] = only_letters(data_set[clean_string(header)])
        return data_set
    
    def setup_headers(self, path, file):
        with open(os.path.join(path, file)) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                return row
    
    def write_header(self, file):
        with open(os.path.join(
                Config.CLEANED_FILES_PATH, self.clean_type + '_cleaned_' + file), 'w+') as csvfile:
            writer = csv.DictWriter(
                csvfile, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, fieldnames=self.headers_set)
            writer.writeheader()

    def write_data(self, row, file):
        with open(os.path.join(
                Config.CLEANED_FILES_PATH, self.clean_type + '_cleaned_' + file), 'a+') as csvfile:
            writer = csv.DictWriter(
                csvfile, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, fieldnames=self.headers_set)
            writer.writerow(self.data_set_generator(row))

    def clean(self, path, file):
        with open(os.path.join(path, file)) as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                self.write_data(row, file)
    
    def run(self):
        if len([x for x in os.listdir(self.cleaned_file_path) if x.endswith('.csv')]) == 0:
            current_path = self.merged_file_path
        else:
            current_path = self.cleaned_file_path


        for file in os.listdir(current_path):
            if file.endswith('.csv'):
                self.headers_set = self.setup_headers(current_path, file)
                self.write_header(file)

                self.clean(current_path, file)
                os.remove(os.path.join(current_path, file))


def clean():
    parser = argparse.ArgumentParser()
    parser.add_argument("clean", type=None)
    parser.add_argument("--column_name", type=str, help="the base")
    parser.add_argument("--clean_type", type=str, help="the base")
    args = parser.parse_args()

    cleaner = Cleaner(column_name=args.column_name, clean_type=args.clean_type)
    cleaner.run()



if __name__ == '__main__':
    clean()
