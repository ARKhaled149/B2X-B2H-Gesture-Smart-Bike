from math import e, sqrt
from os import sep
import socket
from _thread import *
import os
import numpy as np
import time
import serial
import socket
from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from pyproj import Proj
from math import sqrt
from os import sep
import os
import requests
from requests.exceptions import ConnectionError
from timeit import default_timer as timer
from datetime import timedelta
import qrcode
from PIL import Image
import sys
from lib_oled96 import ssd1306
from smbus import SMBus
from threading import Timer
import urllib.request
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
###############################################################################################################
myProj = Proj("+proj=utm +zone=32T, +south +ellps=WGS84 +datum=WGS84 +unit=m +no_defs")
# SERIAL_PORT = "/dev/serial0"
# gps = serial.Serial(SERIAL_PORT, baudrate = 18200, timeout = 5)        
i2cbus = SMBus(1)
oled = ssd1306(i2cbus)
commands ={
    "location" : "location",
    "location and speed": "location and speed",
    "speed":"speed"
}
added =  False
start = timer()
# acording to which infrastructure the url_bike_get & url_bike will change
bike_name = 'bike99'
url_bike_get = 'http://0ea136904920.ngrok.io/bikes/getbike'
url_bike_update =   'http://0ea136904920.ngrok.io/bikes/UpdateBike'
url_basestation = 'http://2b2b980253d1.ngrok.io/infrastructures/Nearestbs'
bike = requests.post(url=url_bike_get,data={'Name':f'{bike_name}'}).json()
time.sleep(1)
beacons = requests.get(url = url_basestation,
                        data={'East':f'{bike["data"]["East"]}',
                            'North':f'{bike["data"]["North"]}',
                            'Number':3}).json()
time.sleep(1)
##########################################################################################################
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        print('Connected to internet')
    except:
        print('No Internet')
##########################################################################################################       
def formatDegreesMinutes(coordinates, digits):
        parts = coordinates.split(".")
        if (len(parts) != 2):
            return coordinates
        if (digits > 3 or digits < 2):
            return coordinates
        left = parts[0]
        right = parts[1]
        degrees = str(left[:digits])
        minutes = str(right[:3])
        return degrees + "." + minutes

def getPositionData():
    data = gps.readline()
    if data is None:
        return -1,-1,-1
    message = str(data[0:6])
    if message is None:
        return -1,-1,-1
    substring = 'GPRMC'
    if (substring in message):
        data2 = str(data)
        parts = data2.split(",")
        if parts[2] == 'V':
            print ("GPS receiver warning, no satellites available")
            return -1,-1,-1
        else:
            longitude = formatDegreesMinutes(parts[5], 3)
            latitude = formatDegreesMinutes(parts[3], 2)
            speed = float(parts[7])*1.852
            East, North = myProj(latitude,longitude)
            if longitude is None or latitude is None or speed is None:
                return -1,-1,-1 
            return float(East),float(North),speed
    else:
        return -1,-1,-1
########################################################################################################
def get_beacons():
    if len(beacons) == 0:
        return None
    x = beacons[0]
    beacons.remove(x)
    return x
def Auto_Connect_Distance(added):
    beacon = get_beacons()
    if beacon is None:
        return
    East2 = beacon["East"]
    North2 = beacon["North"]
    print(East2)
    print(North2)
    # actual data from the GPS module
    # East,North,speed =  getPositionData() 
    East = bike["data"]["East"]
    North = bike["data"]["North"]
    print(East)
    print(North)
    server_network_name = beacon["Name"]
    server_network_pasword = beacon["Password"]
    print(server_network_name)
    print(server_network_pasword)
    bike_distance = sqrt((float(East)-float(East2))**2 + (float(North)-float(North2))**2)
    if bike_distance < 20:
        f = open('/home/pi/networks.txt','a+')
        if os.path.getsize('/home/pi/networks.txt') != 0 or added:
            for line in f:
                if server_network_name in line:
                    f.close()
                    return
        else:
            os.system("nmcli device wifi connect "+server_network_name+" password "+server_network_pasword)
            f.write(server_network_name + '\n')
            f.close()
            time.sleep(1)
            x = os.popen("ip -4 route show default").read().split()
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect((x[2],0))
            HOST = str(s.getsockname()[0])
            netname = server_network_name
            netpass = server_network_pasword
            requests.post(url = url_bike_update,
                        data={'East':f'{bike["data"]["East"]}',
                            'North':f'{bike["data"]["North"]}',
                            'Name':f'{bike["data"]["Name"]}',
                            'Speed':f'{bike["data"]["Speed"]}',
                            'Shared':f'{bike["data"]["Shared"]}',
                            'Locked':f'{bike["data"]["Locked"]}',
                            'IP':f'{HOST}',
                            'Port':f'{bike["data"]["Port"]}',
                            "Execute": f'{bike["data"]["Execute"]}',
                            "Command": f'{bike["data"]["Command"]}',
                            'Current_Network_Name':f'{netname}',
                            'Current_Network_Password':f'{netpass}'}).json()
            added = True
            return True
    else:
        print('Not in Range')
        return False   
########################################################################################################
def QRCODE(string):   
    img = qrcode.make(string)
    img = img.resize((63,63), Image.NEAREST)
    img.save('/home/pi/Desktop/QRpng.png')
    draw = oled.canvas
    oled.cls()
    draw.bitmap((0,0), Image.open('/home/pi/Desktop/QRpng.png'), fill=1)
    oled.display()
########################################################################################################
def multi_threaded_client(connection):
    while True:
        command = connection.recv(1024).decode('UTF-8')
        print(command)
        # if command == commands["location and speed"]:
        #     east,north,sp =  getPositionData()
        #     if east is None or north is None or sp is None:
        #         response = f"{-1},{-1},{-1}"
        #     else:
        #         response = f"{east},{north},{sp}"
        # elif command == commands["location"]:
        #     east,north,sp =  getPositionData()
        #     if east is None or north is None or sp is None:
        #         response = f"{-1},{-1}"
        #     else:
        #         response = f"{east},{north}"  
        # elif command == commands["speed"]:
        #     east,north,sp =  getPositionData()
        #     if east is None or north is None or sp is None:
        #         response = f"{-1}"
        #     else:
        #         response = f"{sp}"
        # else:
        #     response =f"{0},{0},{0}" 
        response =f"{5},{6},{7}"
        bike2 = requests.post(url=url_bike_get,data={'Name':f'{bike_name}'}).json()
        # e, n, s = getPositionData()
        e,n,s = 5,6,7
        Updated_bike = requests.post(url = url_bike_update,
                    data={'East':f'{e}',
                          'North':f'{n}',
                          'Name':f'{bike2["data"]["Name"]}',
                          'Speed':f'{s}',
                          'Shared':f'{bike2["data"]["Shared"]}',
                          'Locked':f'{bike2["data"]["Locked"]}',
                          'IP':f'{bike2["data"]["IP"]}',
                          'Port':f'{bike2["data"]["Port"]}',
                          "Execute": f'{bike2["data"]["Execute"]}',
                          "Command": f'{bike2["data"]["Command"]}',
                          'Current_Network_Name':f'{bike2["data"]["Current_Network_Name"]}',
                          'Current_Network_Password':f'{bike2["data"]["Current_Network_Password"]}'}).json()
        time.sleep(4)
        connection.sendall(bytes(response,'UTF-8'))
        EncStrng = bike2["data"]["Command"]
        Execute = bike2['data']['Execute']
        if Execute == 'True':
            QRCODE(EncStrng)
            requests.post(url = url_bike_update,
                        data={'East':f'{bike2["data"]["East"]}',
                            'North':f'{bike2["data"]["North"]}',
                            'Name':f'{bike2["data"]["Name"]}',
                            'Speed':f'{bike2["data"]["Speed"]}',
                            'Shared':f'{bike2["data"]["Shared"]}',
                            'Locked':f'{bike2["data"]["Locked"]}',
                            'IP':f'{bike2["data"]["IP"]}',
                            'Port':f'{bike2["data"]["Port"]}',
                            "Execute": f'{False}',
                            "Command": f'{bike2["data"]["Command"]}',
                            'Current_Network_Name':f'{bike2["data"]["Current_Network_Name"]}',
                            'Current_Network_Password':f'{bike2["data"]["Current_Network_Name"]}'}).json()
            print('Execute Updated')
        else:
            draw = oled.canvas
            oled.cls()
            draw.text((7,7),'Qrcode Expired')
            oled.display()        
    connection.close()

def run_server():
    start2 = timer()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        tmp = os.popen("ip -4 route show default").read().split()
        s1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s1.connect((tmp[2],0))
        HOST2 = str(s1.getsockname()[0])        
        s.bind((HOST2, int(bike['data']['Port'])))
        s.listen(5)
        print("Server started, waiting for clients to connect ")
        print(HOST2,bike['data']['Port'])
        end2 = timer()
        print('Latency3 seconds: ', timedelta(seconds=end2-start2))
        while True:
            conn, addr = s.accept()
            print("Application started! Ok Sending data ")
            print('Connected to: ' + addr[0] + ': ' + str(addr[1]))
            print(os.popen("sudo iwgetid -r").read())
            start_new_thread(multi_threaded_client, (conn, ))
        conn.close()
######################################################################################################################
x = Auto_Connect_Distance(False)
end = timer()
print('Latency auto-connect seconds: ', timedelta(seconds=end-start))
time.sleep(1)
if x:
    run_server()
else:
    print('No Server, Out of Range of Correct Network')