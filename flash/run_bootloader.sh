#!/usr/bin/expect

# Set timeout for expect commands
set timeout 60

# Define variables
set host "100.64.10.3"
set username "root"
set password "root"

# Start the SSH session
spawn ssh $username@$host

# Handle the password prompt
expect {
	"*?assword:*" {
		send "$password\r"
	}
	"yes/no" {
		send "yes\r"
		expect "*?assword:*"
		send "$password\r"
	}
}

# Interact with the session
expect "# "
send "reboot bootloader\r"
expect "# "
send "exit\r"
