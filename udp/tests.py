from methods import *

if __name__ == '__main__':

    API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlhbHxKQnZLbGxQY20wa21NT0M1UU1KcFB1eUdYQk84IiwiYXBwbGljYXRpb25faWQiOiJhcHBsaWNhdGlvbnxYcVFFUjhuVVE1Wm9hcUg1a1hiSkdzWWJvd2dNIiwib3JnYW5pemF0aW9uX2lkIjoiZGV2ZWxvcGVyfHlOUUV3cDZTemJ3TE5RaG0ydlpwd2NaeVo5UTciLCJpYXQiOjE1OTY2MTQyNzF9.xv0-HgxczDfX6y9lfT6p70IemdP8jhhUb4FiXSI_jSo"
    client_id = "530e6df1-f3ba-45fe-b2a5-02072f1dea11"
    username = "rnanthak13@gmail.com"
    password = "Chaos_theory1234"
    
    js = get_token_user(client_id, username, password)
    access_token = js['access_token']
    
    refresh_token = js['refresh_token']
    refreshed = do_token_refresh(client_id, refresh_token)
    
    profile = get_pilot_profile(API_KEY,access_token)
    pilot_id = profile['data']['id']
    
        # print("%s : %s".format(p,profile[p]))

    # print("########## Creating FLight Plan ########")
    manufacturer_name = "AeroSense"
    model_name = "AS-MC02-P"
    print("Manufacture name:",manufacturer_name)
    print("model_name ",model_name)
    print("Obtaining aircraft ID")
    model_id = get_model_id(API_KEY,manufacturer_name,model_name)
    
    print("Obtained model id")
    
    # print("Creating flight plan")
    required = {}
    
    required["pilot_id"] = pilot_id
    required["token"] = access_token
    required["model_id"] = model_id
    required["nickname"] = "lightsaber"

    aircrafts = get_pilot_aircrafts(API_KEY,required)
    aircraft_id = aircrafts[0]["id"]

    data = {
        "takeoff_latitude": 12.934158,
        "takeoff_longitude": 77.609316,
        "pilot_id": pilot_id,
        "aircraft_id": aircraft_id,
        "start_time": "2020-07-08T13:38:44.730Z",
        "end_time": "2020-07-08T14:53:42.000Z",
        "max_altitude_agl": 100,
        
        "rulesets":["ind_airmap_rules",
                    "ind_notam"],
        "buffer": 1,
        "geometry": {"type": "Polygon", "coordinates": [[[ 12.934158,77.609316], 
                                                         [ 12.934796,77.609852],
                                                         [ 12.934183,77.610646],
                                                         [ 12.933551,77.610100],
                                                         [12.934158,77.609316]
                                                        ]]
                    }
    }
    
    created_flightplan = create_flight_plan(API_KEY,access_token,data)
    flight_plan_id = created_flightplan["data"]["id"]
    print("Flight plan id",flight_plan_id)
    
    data = {
        "country":"IND",
        "limit":10,
    }
    flights = get_flights(API_KEY,access_token,data)
    # print(flights)
    print(API_KEY)
    
    print(flights.keys())
    submit_plan = False
    flight_id = ""
    if submit_plan:

        file = open("output.json","w")
        out = get_fligh_brief(API_KEY,access_token,flight_plan_id)
        submission_result = submit_flight_plan(API_KEY,access_token,flight_plan_id)
        json.dump(submission_result,file)
        flight_id = submission_result["data"]["flight_id"]
        file.close()
    else:
        file = open("output.json","r")
        submission_result = json.load(file)
        flight_id = submission_result["data"]["flight_id"]
        file.close()
    
    secret_key = start_comm(API_KEY,access_token,flight_id)
    secretKey = base64.b64decode(secret_key)

    HOSTNAME = 'telemetry.airmap.com'
    IPADDR = socket.gethostbyname(HOSTNAME)
    PORTNUM = 16060


    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    try:
        s.connect((IPADDR, PORTNUM))
        print("Socket Connected")
        
    except:
        print("Socket Connection Problem")
    s.close()
    print("Socket closed")
    end_comm(API_KEY,access_token,flight_id)
    print("Communication Ended")
    
    
    
    