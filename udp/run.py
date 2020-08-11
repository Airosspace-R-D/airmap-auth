import flask
import methods 
import json
from flask import request, jsonify
import sqlite3


app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.


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