#### At first you need to setup serial interface
#### sudo raspi-config -  interfacing - Serial ----enable it
#### sudo apt install python3-requests


#!/usr/bin/python
import sys
import requests
import json
import RPi.GPIO as io
import time
from threading import Timer

import configparser
 
##getting the configurations 
config = configparser.ConfigParser()
config.read('config.ini')
try:
    api_key_header = config['Section 1']['api_key']
    device_id = config['Section 1']['device_id']
except:
    api_key_header = 'uyaclpQvUul4VGsp'
    device_id = '668f802e4c4e11ecb8029600000a0cbd'

io.setmode(io.BCM)
RED_LED = 27
GREEN_LED = 25
BUZZER = 22
RELAY = 17

#set GPIO pins 
io.setup(RED_LED, io.OUT) 
io.setup(GREEN_LED, io.OUT) 
io.setup(BUZZER, io.OUT) 
io.setup(RELAY, io.OUT) 


api_key = "https://api.wod-worx.com/" 
get_request = "access/v1/access-key/list"
post_request = "access/v1/access-event"
list_of_key = []
log_event = []
## database variables
headers = {
    'HTTP_X_ORG_API_KEY':api_key_header, # 'uyaclpQvUul4VGsp',
    'HTTP_X_DEVICE_ID': device_id # '668f802e4c4e11ecb8029600000a0cbd'
}

##QR reader result
ACCESS_OK = "access-guaranteed"
ACCESS_REFUSED = "access-denied"




def barcode_reader():
    """Barcode code obtained from 'brechmos' 
    https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100"""
    hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
           17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
           29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
           45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

    hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',
            17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
            29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ',
            45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}
   

    ss = ""
    shift = False
    done = False

    while not done:
        ## Get the character from the HID
        buffer = fp.read(8)
        for c in buffer:
            if c > 0:

                ##  40 is carriage return which signifies
                ##  we are done looking for characters
                if int(c) == 40:
                    done = True
                    break

                ##  If we are shifted then we have to
                ##  use the hid2 characters.
                if shift:

                    ## If it is a '2' then it is the shift key
                    if int(c) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid2[int(c)]
                        shift = False

                ##  If we are not shifted then use
                ##  the hid characters

                else:

                    ## If it is a '2' then it is the shift key
                    if int(c) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid[int(c)]
    return ss
## Get the list of keys
def get_keys():
    global list_of_key
    try:
        url = api_key + get_request
        response = requests.request("GET", url, headers=headers)

        print("-----" * 5)
        print(json.dumps(response.json(), indent=2))
        result = json.dumps(response.json())
        print("-----" * 5 + "\n")
        response_dict = json.loads(response.text)
        # print(type(response_dict))
        # print(response_dict)
        # print(response_dict["data"]["keys"])
        list_of_key = response_dict["data"]["keys"]
        ## start the thread again after 10 seconds
        timerAgain = Timer(10, get_keys)
        timerAgain.start()
    except Exception as e:
        ##incase of no internet
        print(e)
        timerAgain = Timer(10, get_keys)
        timerAgain.start()



##Post the users events
def send_event(key,access_result):
    global log_event
    try:
        url = api_key + post_request

        files = {
            'accessKeyID': (None, key),
            'eventType': (None, access_result),
        }
        response = requests.request("POST", url, headers=headers ,files =files)
        print(json.dumps(response.json(), indent=2))
        print("-----" * 5 + "\n")
        if len(log_event)>0:
            for events in log_event:
                files = {
                'accessKeyID': (None, events[0]),
                'eventType': (None, events[1]),
                }
                response = requests.request("POST", url, headers=headers ,files =files)
                log_event.shift()
                
    except:
        ## incase of no coverage 
        log_event.append([key,access_result])




def check_key(key):
    global list_of_key
    if key in list_of_key:
        print("LOG : KEY EXIST")
        io.output(GREEN_LED,io.HIGH)
        io.output(RELAY,io.HIGH)
        #beep for one second 1 time
        io.output(BUZZER,io.HIGH)
        time.sleep(1)
        io.output(BUZZER,io.LOW)
        io.output(GREEN_LED,io.LOW)
        io.output(RELAY,io.LOW)

        return ACCESS_OK
    else:
        print("LOG : KEY NOT EXIST")
        io.output(RED_LED,io.HIGH)
        #beep for one second 3 times
        for i in range(3):
            io.output(BUZZER,io.HIGH)
            time.sleep(1)
            io.output(BUZZER,io.LOW)
        io.output(RED_LED,io.LOW)
        return ACCESS_REFUSED

if __name__ == '__main__':

    ## Open serial interface with HID QR reader
    while True:
        try:
            fp = open('/dev/hidraw0', 'rb')
            break
        except Exception as e:
            print(e)
    timerStart = Timer(10, get_keys)
    timerStart.start()

    
    while True:
            try:
                key = barcode_reader()
                print("LOG : QR CODE ", key)
                access_result = check_key(key)
                send_event(key,access_result)
            except KeyboardInterrupt:
                pass
