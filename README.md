# rig-web-app

#### How to Launch

This app is intended to run only thorugh titan@pegasus.
```
python3 launch_app.py
```

#### Data
There is a data.txt file, if you need to add or edit any of the laptop/rig details, please use that.
For download to a laptop working, we need to run these command from titan.

```
sshpass -p <password> ssh -o StrictHostKeyChecking=no <laptop_username>@<laptop_IP> 'mkdir -p ~/.ssh && chmod 700 ~/.ssh'
sshpass -p <password> ssh -o StrictHostKeyChecking=no <laptop_username>@<laptop_IP> 'touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'
sshpass -p '<password>' ssh-copy-id -o StrictHostKeyChecking=no <laptop_username>@<laptop_IP>
```

##### Note :
There might be static paths in the code so, please run the app from /home/titan/web_app/ only for working results.