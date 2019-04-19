"""Utilities
"""
import re

def clean_string(string):
    return ''.join(e for e in string.lower() if e.isalnum())

def removeNonAscii(s): 
    return "".join(i for i in s if ord(i) < 128)

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
