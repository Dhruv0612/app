#!/bin/bash

# Define variables
HOSTS=("100.64.10.3" "100.64.10.4" "100.64.10.21")
Flash_File_Path="/home/$USERNAME/web_app/soc/euto-v9-discovery/"
Flash_File_name="ff_all.sh"
SANITY_TEST_PATH="/cccm-sanity-test"

# Start the reboot bootloader in background
nohup /home/$USERNAME/web_app/flash/run_bootloader.sh &
sleep 5

# Count the number of fastboot devices
FB_DEVICE_COUNT=$(fastboot devices | grep "fastboot" | wc -l)

# Check if there are any fastboot devices connected
if [ "$FB_DEVICE_COUNT" -gt 0 ]; then
	echo "Fastboot device detected."
	#fastboot reboot #here run ff_all.sh command for flashing the image
	cd $Flash_File_Path
	bash "$Flash_File_name"

	# Check if the ping was successful and print the output
	sleep 3m
	for host in "${HOSTS[@]}"; do
		PING_OUTPUT=$(ping -c 1 "$host" 2>&1)
		if [[ $? -eq 0 ]]; then
			echo "Ping successful..."
			echo "$PING_OUTPUT"
		else
			echo "Ping failed..."
			echo "$PING_OUTPUT"
		fi
	done
	#cd $SANITY_TEST_PATH
	#python3 adb_enable.py --loop &
	#python3 ./cccm_sanity_test/cccm_sanity_test.py --test_suite ./tests/robot_tests/test_set_sanity_with_update --output_dir ./output/

else
	echo "No fastboot devices detected."
	fastboot reboot
fi
