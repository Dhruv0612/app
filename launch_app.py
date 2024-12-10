import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import subprocess
import time

app = Flask(__name__)

# Load data from file
def load_data():
    with open('data.txt', 'r') as file:
        return json.load(file)

# Save data to file
def save_data(data):
    with open('data.txt', 'w') as file:
        json.dump(data, file, indent=4)

# Load initial data
data = load_data()

@app.route('/')
def index():
    global data
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/update/<int:index>', methods=['POST'])
def update(index):
    global data
    data[index]['RIG_CONNECTED'] = request.form['RIG_CONNECTED']
    data[index]['ADSP_VERSION'] = request.form['ADSP_VERSION']
    data[index]['VIP_VERSION'] = request.form['VIP_VERSION']
    data[index]['SOC_VERSION'] = request.form['SOC_VERSION']
    save_data(data)
    return redirect(url_for('index'))

@app.route('/play/<int:index>', methods=['POST'])
def play(index):
    global data
    row_data = data[index]
    return jsonify(row_data)

@app.route('/submit', methods=['POST'])
def submit():
    build_link = request.form.get('build_link')
    index = int(request.form.get('index'))
    laptop_name = data[index]['LAPTOP_NAME']
    ip = data[index]['IP']
    password = data[index]['PASSWORD']
    username = data[index]['USERNAME']
    build_name = build_link.rpartition('/')[-1]
    cmd_rm_host = f"rm -rf ./download/{laptop_name}"
    print(cmd_rm_host)
    process = subprocess.run(cmd_rm_host.split())

    cmd_mkdir_host = f"mkdir -p ./download/{laptop_name}"
    print(cmd_mkdir_host)
    process = subprocess.run(cmd_mkdir_host.split())

    # Call another Python script with build link, laptop name, and IP as arguments
    process = subprocess.Popen(['python3', './flash/flash_soc.py', build_link, laptop_name])
    process.wait()
    
    cmd_rm_client = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{ip} 'rm -rf ~/web_app'"
    print(cmd_rm_client)
    process = subprocess.run(cmd_rm_client, shell=True)

    cmd_mkdir_client = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{ip} 'mkdir -p ~/web_app'"
    print(cmd_mkdir_client)
    process = subprocess.run(cmd_mkdir_client, shell=True)

    cmd_scp = f"sshpass -p '{password}' scp -r ./download/{laptop_name}/ {username}@{ip}:~/web_app/"
    print(cmd_scp)
    subprocess.run(cmd_scp.split())

    cmd_scpp = f"sshpass -p '{password}' scp -r ./flash {username}@{ip}:~/web_app/"
    print(cmd_scpp)
    subprocess.run(cmd_scpp.split())

    #cmd_scppp = f"sshpass -p '{password}' scp -r ./Flash.sh {username}@{ip}:~/web_app/"
    #print(cmd_scppp)
    #subprocess.run(cmd_scppp.split())

    cmd_extract = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{ip} 'tar -xvf ~/web_app/{laptop_name}/{build_name} -C ~/web_app'"
    print(cmd_extract)
    process = subprocess.run(cmd_extract, shell=True)

    cmd_rm_client_tar = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{ip} 'rm -rf ~/web_app/{laptop_name}'"
    print(cmd_rm_client_tar)
    process = subprocess.run(cmd_rm_client_tar, shell=True)

    return redirect(url_for('index'))

@app.route('/update_availability/<int:index>', methods=['POST'])
def update_availability(index):
    global data
    data[index]['AVAILABILITY'] = request.form['availability']
    save_data(data)
    return jsonify({"status":"success"})

@app.route('/get_availability/<int:index>', methods=['GET'])
def get_availability(index):
    global data
    availability = data[index]['AVAILABILITY']
    return jsonify({"availability":availability})

@app.route('/flash/<int:index>', methods=['POST'])
def flash(index):
    global data
    laptop_name = data[index]['LAPTOP_NAME']
    ip = data[index]['IP']
    password = data[index]['PASSWORD']
    username = data[index]['USERNAME']

    # Define the full path for run_bootloader.sh and Flash.sh 
    run_bootloader_path = f"/home/{username}/web_app/flash/run_bootloader.sh" 
    flash_script_path = f"/home/{username}/web_app/flash/Flash.sh"


    #cmd_bootl = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{ip} 'nohup {run_bootloader_path} &'"
    #print(cmd_bootl)
    #process = subprocess.run(cmd_bootl, shell=True)

    cmd_flash = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{ip} 'export USERNAME={username} && bash {flash_script_path}'"
    print(cmd_flash)
    process = subprocess.run(cmd_flash, shell=True)

    if process.returncode == 0:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "failure"})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
