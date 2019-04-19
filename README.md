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

## Installation
You may need to prepare your virtual environment to keep your env clean
```
$ source venv/bin/activate
```
or when you use virtualenv wrapper
```
$ workon <your_venv_name>
```
Just after getting into the corresponding virtual environment, please install dependencies
```
(your_env_name)user@machine:/path/to/project$ pip install -r requirements.txt
```
Then you are ready to go!

## Configuration
I created a json based environment configuration module.
```json
{
    "AWS_ACCESS_KEY": "BKI4TOKDEHTC5VXB6QUH",
    "AWS_SECRET_KEY": "sFLKDJEIf43453Dd8f*DF7g9s/fe",
    "AWS_SOURCE_BUCKET": "source_bucket",
    "AWS_DESTINATION_BUCKET": "target_bucket",
    "AWS_SOURCE_FOLDER_PATH": "source/path/",
    "AWS_DESTINATION_FOLDER_PATH": "destination/path/"
}
```
Or you can configure by editing config.py file directly. This is placed in `src` directory.
> Don't forget to specify **AWS_ACCESS_KEY**, **AWS_SECRET_KEY**, **AWS_SOURCE_BUCKET** and **AWS_DESTINATION_BUCKET**.
Once you're done, you can give it a try!

## Usage
All of scripts are concentrated into run.py so now it can be executed via run.py
### Gluefile
Just specify what you want to do as following
```
$ python run.py gluefile --column_name=new_column --column_value=new_value
```
Then the script will download all of files 