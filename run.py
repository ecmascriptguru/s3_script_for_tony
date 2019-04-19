import os, argparse
from src.config import *
from src.s3 import S3Manager


parser = argparse.ArgumentParser()

if __name__ == "__main__":
    s3 = S3Manager()
    s3.download_all_files()
