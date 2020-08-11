import flask
import methods 
import json
import sqlite3
import socket
import struct
from Crypto.Cipher import AES
from flask import request, jsonify


app = flask.Flask(__name__)
app.config["DEBUG"] = True


position    = methods.telemetry_pb2.Position()
attitude    = methods.telemetry_pb2.Attitude()
speed       = methods.telemetry_pb2.Speed()
barometer   = methods.telemetry_pb2.Barometer()

HOSTNAME = 'telemetry.airmap.com'
IPADDR = socket.gethostbyname(HOSTNAME)
PORTNUM = 16060

# Create some test data for our catalog in the form of a list of dictionaries.
def pad(data, BS):
    PS = (BS - len(data)) % BS
    if PS == 0:
        PS = BS
    P = (chr(PS) * PS).encode()
    return data + P



@app.route('/home', methods=['GET'])
def home():
    return '''<h1>Home of UDP protocol with AirMAP</h1>'''


# A route to return all of the available entries in our catalog.
@app.route('/airmap/get_token', methods=['POST'])
def get_token():
    if request.method == "POST":
        print(request.data)
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        if len(data.keys())>0:
            client_id = data["client_id"]
            username = data["username"]
            password = data["password"]
            returned = str(methods.get_token_user(client_id,username,password))
            return returned

        else:
            return "Invalid data received"
        
        # return request.data
        # return request.form
    else:
        return "Use POST method"
    # return jsonify(books)

@app.route('/airmap/do_token_refresh',methods=['POST'])
def do_token_refresh():
    if request.method == "POST":
        print(request.data)
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        if len(data.keys())>0:
            client_id = data["client_id"]
            username = data["refresh_token"]

            returned = str(methods.do_token_refresh(client_id,username))
            return returned
        else:
            return "Invalid data received"
        
    else:
        return "Use POST method"

@app.route('/airmap/get_pilot_profile',methods=['POST'])
def get_pilot_profile():
    if request.method == "POST":
        print(request.data)
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        if len(data.keys())>0:
            api_key = data["api_key"]
            token_id = data["token_id"]
            return  str(methods.get_pilot_profile(api_key,token_id))
            
        else:
            return "Invalid data received"
        
    else:
        return "Use POST method"

@app.route('/airmap/get_model_id',methods=['POST'])
def get_model_id():
    if request.method == "POST":
        print(request.data)
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        if len(data.keys())>0:
            api_key = data["api_key"]
            manufacturer_name = data["manufacturer_name"]
            model_name = data["model_name"]
            return  str(methods.get_model_id(api_key,manufacturer_name,model_name))
            
        else:
            return "Invalid data received"
        
    else:
        return "Use POST method"


@app.route('/airmap/create_flight_plan',methods=['POST'])
def create_flight_plan():
    if request.method == "POST":
        print(request.data)
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        if len(data.keys())>0:
            api_key = data["api_key"]
            token = data["token"]
            dataa = data["data"]
            return  str(methods.create_flight_plan(api_key,token,dataa))
        else:
            return "Requires {api_key,token,data}"
        
    else:
        return "Use POST method"

@app.route('/airmap/get_pilot_aircrafts',methods=['POST'])
def get_pilot_aircrafts():
    if request.method == "POST":
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        if len(data.keys())>0:
            api_key = data["api_key"]
            required = data["required"]
            return  str(methods.get_pilot_aircrafts(api_key,required))
        else:
            return "Requires {api_key,required}"
        
    else:
        return "Use POST method"

@app.route('/airmap/submit_flight_plan',methods=['POST'])
def submit_flight_plan():
    if request.method == "POST":
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        if len(data.keys())>0:
            api_key = data["api_key"]
            token = data["token"]
            plan_id = data["plan_id"]
            return  str(methods.submit_flight_plan(api_key,token,plan_id))
        else:
            return "Requires {api_key,token,plan_id}"
        
    else:
        return "Use POST method"

@app.route('/airmap/get_flights',methods=['POST'])
def get_flights():
    if request.method == "POST":
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        
        if len(data.keys())>0:
            api_key = data["api_key"]
            token = data["token"]
            query = data["query"]
            return  str(methods.get_flights(api_key,token,query))
        else:
            return "Requires {api_key,token,query}"
        
    else:
        return "Use POST method"

@app.route('/airmap/get_flight_brief',methods=['POST'])
def get_flight_brief():
    if request.method == "POST":
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        
        if len(data.keys())>0:
            api_key = data["api_key"]
            token = data["token"]
            plan_id = data["plan_id"]
            return  str(methods.get_fligh_brief(api_key,token,plan_id))
        else:
            return "Requires {api_key,token,plan_id}"
        
    else:
        return "Use POST method"

@app.route('/airmap/start_comm',methods=['POST'])
def start_comm():
    if request.method == "POST":
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        
        if len(data.keys())>0:
            api_key = data["api_key"]
            token = data["token"]
            flight_id = data["flight_id"]
            return  str(methods.start_comm(api_key,token,flight_id))
        else:
            return "Requires {api_key,token,flight_id}"
        
    else:
        return "Use POST method"

@app.route('/airmap/send_data',methods=['POST'])
def send_data():
    if request.method == "POST":
        data = None 
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        if len(data.keys())>0:
            timestamp = data["timestamp"]
            position.timestamp = timestamp
            position.latitude = data["latitude"]
            position.longitude = data["longitude"]
            position.altitude_agl           = data["altitude_agl"]
            position.altitude_msl           = data["altitude_msl"]
            position.horizontal_accuracy    = data["horizontal_accuracy"]

            attitude.timestamp              = timestamp
            attitude.yaw                    = data["yaw"]
            attitude.pitch                  = data["pitch"]
            attitude.roll                   = data["roll"]

            speed.timestamp                 = timestamp
            speed.velocity_x                = data["vel_x"]
            speed.velocity_y                = data["vel_y"]
            speed.velocity_z                = data["vel_z"]

            barometer.timestamp             = timestamp
            barometer.pressure              = data["pressure"]
            counter                         = data["counter"]
            flight_id                       = data["flight_id"]
            secretKey = data["secret_key"]

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
            
            payload = pad(payload, 16)
            IV = methods.Random.new().read(16)
            aes = methods.AES.new(secretKey, AES.MODE_CBC, IV)
            encryptedPayload = aes.encrypt(payload)
            
            format = '!LB'+str(len(flight_id))+'sB16s'+str(len(encryptedPayload))+'s'
            PACKETDATA = struct.pack(format, counter, len(flight_id), flight_id.encode(), 1, IV, encryptedPayload)
            s.send(PACKETDATA)
            return "Packet Sent successfully"
    else:
        return "Use POST method"

@app.route('/airmap/end_comm',methods=['POST'])
def end_comm():
    if request.method == "POST":
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        
        if len(data.keys())>0:
            api_key = data["api_key"]
            token = data["token"]
            flight_id = data["flight_id"]
            return  str(methods.end_comm(api_key,token,flight_id))
        else:
            return "Requires {api_key,token,flight_id}"
        
    else:
        return "Use POST method"

@app.route('/airmap/end_flight',methods=['POST'])
def end_flight():
    if request.method == "POST":
        data = None
        try:
            data = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            return "Empty"
        
        if len(data.keys())>0:
            api_key = data["api_key"]
            token = data["token"]
            flight_id = data["flight_id"]
            return  str(methods.end_comm(api_key,token,flight_id))
        else:
            return "Requires {api_key,token,flight_id}"
        
    else:
        return "Use POST method"


app.run()