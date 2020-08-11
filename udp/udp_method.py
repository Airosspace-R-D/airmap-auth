import socket
import sys
import struct
import requests
import json
import jwt
import telemetry_pb2
import base64
import time
from time import sleep
from datetime import datetime
from Crypto import Random
from Crypto.Cipher import AES

# simple sawtooth wave simulation

class Simulator:
    def update(self, val, dt, mx, initval): 
        val = val + dt
        if val > mx: 
            val = initval 
        return val  

    def getTimestamp(self):
        d = datetime.now()
        return int(d.microsecond/1000 + time.mktime(d.timetuple())*1000)

    def getLattitude(self):
        self._lat = self.update(self._lat, 0.002, 34.02, 34.015802)
        return  self._lat
    def getLongtitude(self):
        self._lon = self.update(self._lon, 0.002, -118.44, -118.451303) 
        return self._lon
    def getAgl(self):
        self._agl = self.update(self._agl, 1.0, 100.0, 0.0) 
        return self._agl
    def getMsl(self): 
        self._msl = self.update(self._msl, 1.0, 100.0, 0.0) 
        return self._msl
    def getHorizAccuracy(self):
        self._horizAccuracy = self.update(self._horizAccuracy, 1.0, 10.0, 0.0) 
        return self._horizAccuracy
    def getYaw(self):
        self._yaw = self.update(self._yaw, 1.0, 360.0, 0.0) 
        return self._yaw
    def getPitch(self): 
        self._pitch = self.update(self._pitch, 1.0, 90.0, -90.0) 
        return self._pitch
    def getRoll(self): 
        self._roll = self.update(self._roll, 1.0, 90.0, -90.0) 
        return self._roll
    def getVelocityX(self): 
        self._velocity_x = self.update(self._velocity_x, 1.0, 100.0, 10.0) 
        return self._velocity_x
    def getVelocityY(self): 
        self._velocity_y = self.update(self._velocity_y, 1.0, 100.0, 10.0) 
        return self._velocity_y 
    def getVelocityZ(self): 
        self._velocity_z = self.update(self._velocity_z, 1.0, 100.0, 10.0) 
        return self._velocity_z
    def getPressure(self): 
        self._pressure = self.update(self._pressure, 0.1, 1013.0, 1012.0) 
        return self._pressure

    _lat = 34.015802;
    _lon = -118.451303;
    _agl = 0.0;
    _msl = 0.0;
    _horizAccuracy = 0.0;
    _yaw = 0.0;
    _pitch = -90.0;
    _roll = -90.0;
    _velocity_x = 10.0;
    _velocity_y = 10.0;
    _velocity_z = 10.0;
    _pressure = 1012.0;

# anonymous user (returns JWT)

# API key and user ID

# get token
print(API_KEY,USER_ID)
JWT = get_token(API_KEY, USER_ID)
if JWT == -1:
    print("Error with authentication")
    exit(1)
print("JWT: "+JWT)

# get pilot id

pilotID = jwt.decode(JWT, verify=False, algorithms=['HS256'])["sub"]
print("pilotID: "+pilotID)

# create flight plan

planID = create_plan(API_KEY, JWT, pilotID)
if planID == -1:
    print("Error creating plan")
    exit(1)
print("planID: "+planID)

# submit flight plan

flightID = submit_plan(API_KEY, JWT, planID)
if flightID == -1:
    print("Error creating flight")
    exit(1)
print("flightID: "+flightID)

# start comms

secretKey = start_comm(API_KEY, JWT, flightID)
if secretKey == -1:
    print("Error starting communication")
    exit(1)
print("secretKey: "+secretKey)

# decode key

secretKey = base64.b64decode(secretKey)

# messages

position    = telemetry_pb2.Position()
attitude    = telemetry_pb2.Attitude()
speed       = telemetry_pb2.Speed()
barometer   = telemetry_pb2.Barometer()

# addressing information of target
HOSTNAME = 'telemetry.airmap.com'
IPADDR = socket.gethostbyname(HOSTNAME)
PORTNUM = 16060
 
# initialize a socket, SOCK_DGRAM specifies that this is UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

sim = Simulator()

# serial number
counter = 1

try:
    # connect the socket
    s.connect((IPADDR, PORTNUM))

    # send 100 messages at 5Hz
    for i in range(10):

        # update messages 
        timestamp = sim.getTimestamp()
        position.timestamp              = timestamp
        position.latitude               = sim.getLattitude()
        position.longitude              = sim.getLongtitude()
        position.altitude_agl           = sim.getAgl()
        position.altitude_msl           = sim.getMsl()
        position.horizontal_accuracy    = sim.getHorizAccuracy()

        attitude.timestamp              = timestamp
        attitude.yaw                    = sim.getYaw()
        attitude.pitch                  = sim.getPitch()
        attitude.roll                   = sim.getRoll()

        speed.timestamp                 = timestamp
        speed.velocity_x                = sim.getVelocityX()
        speed.velocity_y                = sim.getVelocityY()
        speed.velocity_z                = sim.getVelocityZ()

        barometer.timestamp             = timestamp
        barometer.pressure              = sim.getPressure()

        # build  payload

        # serialize  protobuf messages to string and pack to payload buffer
        bytestring = position.SerializeToString()
        format = '!HH'+str(len(bytestring))+'s'
        payload = struct.pack(format, 1, len(bytestring), bytestring)

        bytestring = attitude.SerializeToString()
        format = '!HH'+str(len(bytestring))+'s'
        payload += struct.pack(format, 2, len(bytestring), bytestring)

        bytestring = speed.SerializeToString()
        format = '!HH'+str(len(bytestring))+'s'
        payload += struct.pack(format, 3, len(bytestring), bytestring)

        bytestring = barometer.SerializeToString()
        format = '!HH'+str(len(bytestring))+'s'
        payload += struct.pack(format, 4, len(bytestring), bytestring)
        print(payload)
        # encrypt payload

        # use PKCS7 padding with block size 16
        def pad(data, BS):
            PS = (BS - len(data)) % BS
            if PS == 0:
                PS = BS
            P = (chr(PS) * PS).encode()
            return data + P

        payload = pad(payload, 16)
        IV = Random.new().read(16)
        aes = AES.new(secretKey, AES.MODE_CBC, IV)
        encryptedPayload = aes.encrypt(payload)
        # send telemetry
        # packed data content of the UDP packet
        format = '!LB'+str(len(flightID))+'sB16s'+str(len(encryptedPayload))+'s'
        PACKETDATA = struct.pack(format, counter, len(flightID), flightID.encode(), 1, IV, encryptedPayload)

        # send the payload
        s.send(PACKETDATA)

        # print timestamp when payload was sent
        print("Sent payload messsage #" , counter ,  "@" , time.strftime("%H:%M:%S"))
        
        # increment sequence number
        counter += 1

        # 5 Hz
        sleep(0.2)

except:
    print("Error sending telemetry")
    exit(1)
 
# close the socket
s.close()

# end comm and flight
if (end_comm(API_KEY, JWT, flightID) == -1):
    print("Error ending communication")
    exit(1)

if (end_flight(API_KEY, JWT, flightID) == -1):
    print("Error ending flight")
    exit(1)