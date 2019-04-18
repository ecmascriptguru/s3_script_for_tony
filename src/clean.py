# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from os import listdir
from os.path import isfile, join
import argparse
import csv
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument("--column_name", type=str, help="the base")
parser.add_argument("--clean_type", type=str, help="the base")
args = parser.parse_args()

path_to_files = 'merged/'
path_to_cleaned = 'cleaned/'
headers_set = []


def clean_string(string):
    return ''.join(e for e in string.lower() if e.isalnum())

def validate_email(col_value):
    try:
        m = re.match(r"^(.*?\@.*?\..*?)$", col_value)
        return m.group(1)
    except:
        return ''

def clean_phone(col_value):
    if col_value.startswith('+'):
        return '+' + clean_string(col_value)
    else:
        return clean_string(col_value)

def only_letters(col_value):
    return re.sub('[^A-Za-z ]+', '', col_value)

def data_set_generator(data_set):
    if args.column_name != None and args.clean_type != None:
        columns_set = args.column_name.split(',')
        for header in columns_set:
            if clean_string(header) in headers_set:
                if args.clean_type == 'email':
                    data_set[clean_string(header)] = validate_email(data_set[clean_string(header)])

                elif args.clean_type == 'phone':
                    data_set[clean_string(header)] = clean_phone(data_set[clean_string(header)])

                elif args.clean_type == 'string':
                    data_set[clean_string(header)] = only_letters(data_set[clean_string(header)])
    #print data_set.keys()
    return data_set

def setup_headers(path, file):
    with open(path + file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            return row
            #break

def write_header(file):
    with open('cleaned/' + args.clean_type + '_cleaned_' + file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers_set)
        writer.writeheader()

def write_data(row, file):
    with open('cleaned/' + args.clean_type + '_cleaned_' + file, 'a+') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=headers_set)
        writer.writerow(data_set_generator(row))

def processing(path, file):
    with open(path + file) as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            write_data(row, file)

if __name__ == '__main__':

    if len([x for x in listdir(path_to_cleaned) if x.endswith('.csv')]) == 0:
        current_path = path_to_files
    else:
        current_path = path_to_cleaned


    for file in listdir(current_path):
        if '.csv' in file:
            headers_set = setup_headers(current_path, file)
            write_header(file)
            if args.column_name != None and args.clean_type != None:
                processing(current_path, file)
                os.remove(current_path + file)
