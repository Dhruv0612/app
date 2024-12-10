import os
import time
import json
import subprocess
import sys

sys.path.append("..")  # to allow use of modules for test
from jfrog_utils import jfrog_files

if __name__ == "__main__":

    # API_key = "AKCpBrw56kcFum3Snx8MLofbCsbhA1zMAwLB6XqjT617wW8s5Efyto5wHgtzEvErDbWmMzN72" # Shreya's API token
    API_key = "cmVmdGtuOjAxOjE3NTkyMjQ3NDY6OG91R1NvdXM4R1pEdmRKY1cxMFVDQW95Z3gz"  # - Sneha's token

    image_folder = "~/web_app/soc/euto-v9-discovery"
    subprocess.run(['~/web_app/flash/Flash.sh', image_folder])


