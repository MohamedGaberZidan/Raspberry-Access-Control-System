# This is project is developed using RPI for making Multiple Door Access Control system 

Hardware included:
PI

Relay

LED

Buzzer

QR reader

RFID reader

Software:
python script connected to a database using rest api 

# Steps for installation

# NOTE
Your PI user name should be pi as multiple files depend on the path 

# At first you need to setup serial interface
$ sudo raspi-config  #-choose  interfacing - Serial ----enable it


# Run these commands in the terminal

$ git clone https://github.com/soofdev/wodworx-acs-rpi.git

$ cd Raspberry-Access-Control-System

$ pip install -r requirements.txt

$ chmod u+x uninstall.sh

$ chmod u+x install.sh

$ ./install

## After rebooting the system will automatically open a terminal everytime you reboot the pi and will run the script 
$ reboot 
## For uninstalling  run this command in the terminal
$ ./uninstall

## For updating the apikey and the device id  replace your apikey and device id by your_api_key your_device_id and run it the system will automaticall reboot after updating
$ cd Raspberry-Access-Control-System

$ python update.py your_api_key your_device_id
