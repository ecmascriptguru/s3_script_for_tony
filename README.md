# s3_script_for_tony

## Original requirements (Communication history)
there are 2 script files here - first is gluefile.py
python gluefile.py --column_name "new_column" --column_value "some_value"

This is where we need to define the s3 bucket and sub folder that we will grab all csv's from. we can define the s3 bucket in the code, and the folder in the CLI

this script takes all the csv's (once downloaded from s3) and merges them into a single file.

Second script is clean.py


this clean the combined csv - for this project you dont need to worry about this file right now.

We need a 3rd script that takes the merged or the cleaned file and uploads it back to s3 in a defined folder - with a new file name we will define in the CLI

Step 1 - gluefile.py - will download, then merge the files with the current script functionality.
Step 2 - is an upload script to Upload back to the specified bucket. - where we define the file we want to upload (either email_cleaned_merged_file.csv or merged_file.csv), and thefolder name for the upload bucket

