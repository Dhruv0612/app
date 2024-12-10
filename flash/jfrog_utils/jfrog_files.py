import os
import subprocess
import datetime
import logging
import tarfile



def Subprocess_Read(process):
    # function to read data being output from
    Data = []
    while True:
        output = process.stdout.readline()
        string = output.decode().strip()
        if string != '':
            #print(string)
            Data.append(string)
        else:
            break
    return Data

class Jfrog():
    def __init__(self, API_key, JLR_NGI = "JLR"):   
        self.JLR_NGI = JLR_NGI
        self.URL = '--url'     
        self.URL_address_NGI = 'https://artifactory.jlrngi.com/artifactory/'
        self.URL_address_JLR = 'https://artifactory-gdd.sdo.jlrmotor.com/artifactory/'  
        if self.JLR_NGI == "NGI":
            self.URL_address = self.URL_address_NGI
        else:
            self.URL_address = self.URL_address_JLR
        self.app = r'jf'
        self.arg1 = 'rt'
        self.password = '--password'  # updated to use password field instead of API Key
        self.password_value = API_key
        self.option = 's'  # s = search, dl = Download        
        os.environ["CI"] = "true"  # required to stop configure prompts
    
    def jf_proxy(self):
        os.environ["HTTP_PROXY"] = "http://10.224.132.196:83/"  # possibly required in JLR site
        os.environ["HTTPS_PROXY"] = "http://10.224.132.196:83/"  # possibly required in JLR site
        # os.environ["NO_PROXY"] = "true"
        print("Setting CI to true and HTTP and HTTPS Proxy")

    def jf_proxy_remove(self):
        print("Removing proxy")
        try:
            os.environ.pop("HTTP_PROXY")
        except:
            print("no HTTP Proxy to remove")

        try:
            os.environ.pop("HTTPS_PROXY")
        except:
            print("no HTTPS Proxy to remove")

    def jf_search(self, folder):
        self.option = 's'        
        self.location = folder    
        process = subprocess.Popen(
            [self.app, self.arg1, self.option, self.URL, self.URL_address, self.password, self.password_value, self.location],
            stdout=subprocess.PIPE,
            )  # Search API
        print("Reading from Search Subprocess")
        data = Subprocess_Read(process)
        print("Reading Complete, Killing process")
        process.kill()
        
        return data

    def jf_string_search(self, string, folder):
        results = self.jf_search(folder)
        paths = []
        for row in results:
            if "path" in row:
                data = row.replace("\"path\": \"", "")
                data = data.replace("\",", "")
                paths.append(data)
        counter = 0
        results = []
        for row in paths:
            if string in row:
                counter += 1
                print(row)
                results.append(row)
        if counter == 0:
            print("software not found")

        return results
    
    def jf_download(self, file, location): 
        print("Downloading file: " + str (file))       
        print("To folder: " + str(location))
        self.option = 'dl'  
        self.location = file
        self.destination = location
        self.structure = '--flat'
        process = subprocess.Popen(
            [
                self.app,
                self.arg1,
                self.option,
                self.URL,
                self.URL_address,
                self.password,
                self.password_value,
                self.structure,
                self.location,
                self.destination,
            ],
            stdout=subprocess.PIPE,
        )  # Download API
        data = Subprocess_Read(process)
        for row in data:
            if "\"status\": \"success\"" in row:
                print("Download Success")
                success = True
                break
            else:
                success = False

        if success != True:
            print("Download Failed")
        return success

    def unpack_software(self, file, location, delete = False):
        print("File to unpack is:" + str(file))
        print("Location to put software is: " + str(location))
        if os.name == "posix":
            folder_name = file.split("/")[-1]
            folder_name = folder_name.replace(".tar.gz", "")
            folder_name = folder_name.replace(".tar.xz", "")
            folder_name = folder_name.replace(".tar", "")
        elif os.name == "nt":
            folder_name = file.split("\\")[-1]
            folder_name = folder_name.replace(".tar.gz", "")
            folder_name = folder_name.replace(".tar.xz", "")
            folder_name = folder_name.replace(".tar", "")
        
        new_folder = location + folder_name
        print("New folder is : " + new_folder)
        if not os.path.exists(new_folder):
            print("Folder did not already exists, creating")
            os.makedirs(new_folder)
        
        TAR_file = tarfile.open(file, ignore_zeros = True)    # extracting file        
        if os.name == "posix":
            TAR_file.extractall(new_folder + "/")
        elif os.name == "nt":
            TAR_file.extractall(new_folder + "\\")
        TAR_file.close()
        print("File extracted")
        print(os.listdir(new_folder))

        if delete:
            print("deleteing file")
            os.remove(file)

        for file in os.listdir(new_folder):
            File = new_folder + "\\" + file
            if "tar.xz" in File:
                print("tar.xz in File: " + str(File))
                TAR_file = tarfile.open(File, ignore_zeros = True)
                TAR_file.extractall(new_folder + "\\")
                TAR_file.close()
                os.remove(File)
            
        return new_folder

            

        
if __name__ == "__main__":
    API_key = "" # insert API key jere
    jfrog_tool = Jfrog(API_key) #########dont committt
    
    search_string = "cccm-image_0.1.53.tar.gz"
    search_folder = "cccm-pub-bin/cccm-image/images/"
    results = jfrog_tool.jf_string_search(search_string, search_folder)

    temp_folder = "C:\\CCCM\\Daily_Builds\\Temp\\"
    if len(results) == 1:
        jfrog_tool.jf_download(results[0], temp_folder) 
        downloaded_file = results[0].split("/")[-1]      
    
        file = temp_folder + downloaded_file
        software_store = "C:\\CCCM\\Daily_Builds\\"
        downloaded_software = jfrog_tool.unpack_software(file, software_store)
    