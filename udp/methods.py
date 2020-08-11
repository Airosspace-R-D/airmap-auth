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
import requests

def get_token_user(clientid,username,password):
    CLIENT_ID = clientid
    USER_NAME = username 
    PASSWORD = password
    URL = "https://auth.airmap.com/realms/airmap/protocol/openid-connect/token"
    PAYLOAD = {
        'grant_type': 'password',
        'client_id': CLIENT_ID,
        'username': USER_NAME,
        'password': PASSWORD
    }
    resp = requests.post(URL, data=PAYLOAD)
    TOKEN = resp.json()["access_token"]
    return resp.json()

def do_token_refresh(clientid,refresh_token):
    CLIENT_ID = clientid
    URL = "https://auth.airmap.com/realms/airmap/protocol/openid-connect/token"
    PAYLOAD = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'refresh_token':refresh_token
    }
    resp = requests.post(URL, data=PAYLOAD)
    
    TOKEN = resp.json()["access_token"]
    return resp.json()
    

def get_pilot_profile(api_key,token_id):
    try:
        response = requests.get(
            url="https://api.airmap.com/pilot/v2/profile",
            headers={
                "Authorization":"Bearer "+token_id,
                "X-API-Key": api_key
            }
        )
        if(response.status_code == 200):
            return json.loads(response.text)
        else:
            print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(content=response.content))
            return {"Error":response.content}
    except requests.exceptions.RequestException:
        return -1
            
# create plan (returns planID)
def get_model_id(api_key,manufacturer_name,model_name):

    try:
        response = requests.get(
            url = "https://api.airmap.com/aircraft/v2/manufacturer?",
            headers={
                "X-API-KEY":api_key
            }    
        )
        
        if response.status_code == 200:
            manufacturers_data =   json.loads(response.text)["data"]
            manu_id = None
            for item in manufacturers_data:
                if manufacturer_name == item['name']:
                    manu_id = item['id']
                    break
            response = requests.get(
                url = "https://api.airmap.com/aircraft/v2/model?manufacturer="+manu_id,
                headers={
                    "X-API-KEY":api_key
                }   
            )
            if response.status_code == 200:
                
                models = json.loads(response.text)["data"]
                
                for model in models:
                    if model["name"] == model_name:
                        return model["id"]
                    
            else:
                print("No Model in that name")

        else:
            print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(content=response.content))
            return {"Error":response.content}
    except requests.exceptions.RequestException:
        return -1


def create_flight_plan(api_key,token,data):
    try:
        response = requests.post(
            url="https://api.airmap.com/flight/v2/plan",
            headers = {
                "X-API-KEY":api_key,
                "Authorization":"Bearer "+token,
                "Content-Type":"application/json; charset=utf-8"
            },
            data=json.dumps(data)
        )
        if(response.status_code == 200):
            print("Success")
            response = json.loads(response.text)
            print(response)
            return response
        else:
            print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(content=response.content))
            return {"Error":response.content}
    except requests.exceptions.RequestException:
        return -1

def get_pilot_aircrafts(api_key,required):
    """
        required["pilot_id"] = ""
        required["token"] = ""
        required["model_id"] = ""
        required["nickname"] = ""
        
    """
    try:
        response = requests.get(
            url = "https://api.airmap.com/pilot/v2/"+required["pilot_id"]+"/aircraft",
            headers = {
                "X-API-KEY":api_key,
                "Authorization":"Bearer "+required["token"],
                # "Content-Type":"application/json; charset=utf-8"
            },
            # data = {"model_id":required["model_id"],"nickname":required["nickname"]}
        )
        if(response.status_code == 200):
            print("Success")
            data = json.loads(response.text)
            data = data["data"][0]
            # print(data)
            aircrafts = []
            aircrafts.append( {
                    "id":data["id"],"nickname":data["nickname"]})
            print(aircrafts)
            return aircrafts
            
        else:
            print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(content=response.content))
            return {"Error":response.content}
    except requests.exceptions.RequestException:
        return -1


# submit plan (returns flightID)
def submit_flight_plan(api_key,token,planID):
    try:

        response = requests.post(
            url="https://api.airmap.com/flight/v2/plan/"+planID+"/submit",
            headers = {
                "accept":"application/json",
                "authorization":"Bearer "+token,
                "X-API-KEY":api_key
            }
        )
        if response.status_code == 200:
            print("Submited flight plan")
            return json.loads(response.text)
        else:
            print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(content=response.content))
            return {"Error":response.content}
    except requests.exceptions.RequestException:
        return -1



def get_flights(api_key,token,query):
    try:
        
        url  = "https://api.airmap.com/flight/v2/"
        header = {
                "accept":"application/json",
                "authorization":token,
                "X-API-KEY":api_key}

        response = requests.request("GET",url,headers=header,params=query)
        if response.status_code == 200:
            print("Success")
            return json.loads(response.text)
        else:
            print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(content=response.content))
            return {"Error":response.content}
    except requests.exceptions.RequestException:
        return -1



def get_fligh_brief(api_key,token,plan_id):
    try:
        url = "https://api.airmap.com/flight/v2/plan/"+plan_id+"/briefing"

        headers = {
            'accept': "application/json",
            'x-api-key': api_key,
            'authorization': "Bearer "+token
            }
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(content=response.content))
            return {"Error":response.content}
    except requests.exceptions.RequestException:
        return -1



# start comm (returns secretKey)

def start_comm(api_key, token, flightID):
    try:
        response = requests.post(
            url="https://api.airmap.com/flight/v2/"+flightID+"/start-comm",
            headers={
                "X-API-Key": api_key,
                "Authorization": "Bearer "+token
            }
        )
        if response.status_code == 200:
            print("Success in Starting communication")
            return str(json.loads(response.text)["data"]["key"])
        else:
            print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(content=response.content))
            return {"Error":response.content}
    except requests.exceptions.RequestException:
        return -1

# end comm (returns 0)

def end_comm(api_key, token, flightID):
    try:
        response = requests.post(
            url="https://api.airmap.com/flight/v2/"+flightID+"/end-comm",
            headers={
                "X-API-Key": api_key,
                "Authorization": "Bearer "+token
            }
        )
        if response.status_code == 200:
            return 0
        else:
            print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(content=response.content))
            return {"Error":response.content}
    except requests.exceptions.RequestException:
        return -1

# end flight (returns 0)

def end_flight(api_key, token, flightID):
    try:
        response = requests.post(
            url="https://api.airmap.com/flight/v2/"+flightID+"/end",
            headers={
                "X-API-Key": api_key,
                "Authorization": "Bearer "+token
            }
        )
        if response.status_code == 200:
            return 0
        else:
            print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(content=response.content))
            return {"Error":response.content}
    except requests.exceptions.RequestException:
        return -1
