#!/usr/bin/python3

from netmiko import ConnectHandler
import os
import time
import datetime
import json

device_list = '/root/Backup_Scripts/router.json'
backup_filename = 'RTR-Config-Backup-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.cfg'
vlan_filename = 'RTR-Show-VLAN-' + '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'

with open(device_list) as json_file:
    data = json.load(json_file)
    # Change data['router_list'] to data['switch_list'] if you are using switch.json
    for router in data['router_list']:
        cisco_2960 = {
    	    'device_type': 'cisco_ios',
    	    'host':   router['ip'],
    	    'username': 'sshusername',    # Provide SSH username
    	    'password': 'sshpassword',    # Provide SSH password
    	    'secret': 'enablesecret',     # Optional, defaults to ''
	}

        try:
            net_connect = ConnectHandler(**cisco_2960)
        except:
            continue

        net_connect.enable()

        output_run_config = net_connect.send_command("show running-config")
        output_vlan = net_connect.send_command("show vlan-switch")

        net_connect.exit_enable_mode()
        net_connect.disconnect()

        #Create a separate directory for each device if not exists.
        backup_dir = '/root/Network_Device_Backups/Router/'+router['hostname']
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        #Write the device running-config to a file.
        f0 = open(backup_dir+'/'+backup_filename, 'w')
        f0.write(output_run_config)
        f0.close()

        #Write the device VLAN output to a file.
        f1 = open(backup_dir+'/'+vlan_filename, 'w')
        f1.write(output_vlan)
        f1.close()
