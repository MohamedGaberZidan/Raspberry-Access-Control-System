import configparser 
import sys
import os
api_key = sys.argv[1]
device_id = sys.argv[2]

config = configparser.ConfigParser()
config['Section 1'] = {'api_key': str(api_key), 'device_id': str(device_id)}

with open('config.ini', 'w') as configfile:
   config.write(configfile)
   
print("Rebooting the system")
os.system('sudo shutdown -r now')
