# encoding=utf-8
import sys, os
import argparse
import csv
from config import Config


parser = argparse.ArgumentParser()
parser.add_argument("--column_name", type=str, help="the base")
parser.add_argument("--column_value", type=str, help="the base")
args = parser.parse_args()

path_to_files = Config.DOWNLOAD_FILES_PATH
headers_set = []

def clean_string(string):
    return ''.join(e for e in string.lower() if e.isalnum())

def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<128)

def glue_headers(header_row):
    for header in header_row:
        clean_header = clean_string(header)
        if clean_header not in headers_set:
            headers_set.append(clean_header)

def setup_headers(file):
    with open(file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            glue_headers(row)
            break

def data_set_generator(row):
    data_set = {}
    for header in row.keys():
        try:
            data_set[clean_string(header)] = removeNonAscii(row[header])
        except:
            data_set[clean_string(header)] = row[header]

    if args.column_name != None and args.column_value != None:
        data_set[clean_string(args.column_name)] = args.column_value

    return data_set

def write_header():
    with open(os.path.join(Config.MERGED_FILES_PATH, 'merged_file.csv'), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers_set)
        writer.writeheader()

def write_data(row):
    with open(os.path.join(Config.MERGED_FILES_PATH, 'merged_file.csv'), 'a+') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers_set)
        writer.writerow(data_set_generator(row))
        
def processing(file, encoding='utf-8'):
    with open(file, encoding=encoding) as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        try:
            for row in csv_reader:
                write_data(row)
        except Exception as e:
            print("Exception found in %s. Retrying..." % encoding)
            try:
                processing(file, encoding='latin')
            except Exception as e:
                print(str(e))


if __name__ == '__main__':

    for file in os.listdir(path_to_files):
        if '.csv' in file:
            setup_headers(os.path.join(path_to_files, file))

    if args.column_name != None and args.column_value != None:
        custom_header = clean_string(args.column_name)
        if custom_header not in headers_set:
            headers_set.append(custom_header)

    write_header()

    for file in os.listdir(path_to_files):
        if '.csv' in file:
            processing(os.path.join(path_to_files, file))

