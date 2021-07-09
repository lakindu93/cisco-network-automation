#!/usr/bin/python3

from netmiko import ConnectHandler
import sys
import os
import time
import datetime
import shutil

ftp_server = '192.168.100.100'
ftp_location = '/home/asaftpuser/'

backup_filename = 'FW-Config-Backup-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.tar.gz'

backup_location = '/root/Network_Device_Backups/ASA/'


cisco_asa = {
    'device_type': 'cisco_asa',
    'host': '192.168.1.1',
    'username': 'sshusername',
    'password': 'sshpassword',
    'secret': 'enablesecret',
}

try:
    net_connect = ConnectHandler(**cisco_asa)
except:
    print >> sys.stderr, "Unable to connec to ASA."
    sys.exit(1)

net_connect.enable()

backup_command = "backup location ftp:"
result = net_connect.send_command_timing(backup_command)

ftp_url = 'ftp://asaftpuser:password@192.168.100.100/'+backup_filename

if 'Press return to continue or enter a backup location' in result:
    result += net_connect.send_command_timing(ftp_url)


net_connect.exit_enable_mode()
net_connect.disconnect()

file_path = ftp_location+backup_filename

while not os.path.exists(file_path):
    time.sleep(10)

if os.path.isfile(file_path):
    shutil.move(file_path, backup_location)
