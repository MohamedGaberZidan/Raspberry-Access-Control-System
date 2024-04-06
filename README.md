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

# Run these commands in the terminal
$ git clone https://github.com/MohamedGaberZidan/Raspberry-Access-Control-System.git
$ cd Raspberry-Access-Control-System
$ pip install -r requirements.txt
$ chmod u+x uninstall.sh
$ chmod u+x install.sh
$ ./install

## After rebooting the system will automatically open a terminal everytime you reboot the pi and will run the script 
$ reboot 
## For uninstalling  run this command in the terminal
$ ./uninstall

## For updating the apikey and the device id  replace your apikey and device id by your_api_key your_device_id and run it
$ cd Raspberry-Access-Control-System
$ python update.py your_api_key your_device_id
