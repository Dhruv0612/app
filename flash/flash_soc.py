import os
import time
import json
import subprocess
import sys

sys.path.append("..")  # to allow use of modules for test
from jfrog_utils import jfrog_files

def removeprefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

if __name__ == "__main__":

    API_key = "cmVmdGtuOjAxOjE3NTkyMjQ3NDY6OG91R1NvdXM4R1pEdmRKY1cxMFVDQW95Z3gz"  # - Sneha's token

    temp_folder = "./"

    jfrog_tool = jfrog_files.Jfrog(API_key, "JLR")
    file_to_download = sys.argv[1]
    temp_folder = "./download/" + sys.argv[2] + "/"
    file_to_download = removeprefix(file_to_download,"https://artifactory-gdd.sdo.jlrmotor.com/artifactory/")
    file_to_download = removeprefix(file_to_download,"artifactory-gdd.sdo.jlrmotor.com/artifactory/")
    jfrog_tool.jf_download(file_to_download, temp_folder) 
    downloaded_file = file_to_download.split("/")[-1]


