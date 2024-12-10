import json

# Path to the file containing the script output
script_output_file = 'allIP.txt'

# Read the script output from the file
with open(script_output_file, 'r') as f:
    script_output = f.read()

# Parse the script output to extract hostnames and IP addresses
new_ips = {}
for line in script_output.strip().split('\n'):
    parts = line.split()
    hostname = parts[0]
    ip_address = parts[1].strip('()')
    new_ips[hostname] = ip_address

# Load the existing data from data.txt
with open('data.txt', 'r') as f:
    data = json.load(f)

# Update the IP addresses in the data
for entry in data:
    laptop_name = entry["LAPTOP_NAME"]
    if laptop_name in new_ips:
        entry["IP"] = new_ips[laptop_name]

# Save the updated data back to data.txt
with open('data.txt', 'w') as f:
    json.dump(data, f, indent=4)

print("IP addresses have been updated in data.txt.")
