#!/bin/python3

from netmiko import ConnectHandler
import time
import datetime
import os
import shutil

tftp_server = '192.168.100.100'
tftp_location = '/tftpboot'

backup_filename = 'WLC-Config-Backup-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.cfg'
backup_location = '/root/Network_Device_Backups/WLC/'

net_connect = ConnectHandler(device_type='cisco_wlc', host='172.16.0.1', username='sshusername', password='sshpassword')

net_connect.find_prompt()

config_commands = ['transfer upload mode tftp',
        	   'transfer upload datatype config',
        	   'transfer upload filename '+backup_filename,
		   'transfer upload path .',
        	   'transfer upload serverip '+tftp_server,
]

# Sending backup configuration settings to device
net_connect.send_config_set(config_commands)

# Initiating transfer
output1 = net_connect.send_command_timing('transfer upload start')

# Confirming start of transfer
output2 = net_connect.send_command_timing('y')

#time.sleep(5)

# Disconnect from device
net_connect.disconnect()

file_path = tftp_location+backup_filename

while not os.path.exists(file_path):
    time.sleep(65)

if os.path.isfile(file_path):
    shutil.move(file_path, backup_location)
