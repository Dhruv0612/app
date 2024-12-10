import subprocess

command = "cat cccm_image_location.txt | awk -F'/' '{print $NF}'"
Tar_File = subprocess.run(command, shell=True, text=True, capture_output=True)
print(Tar_File.stdout)
