from methods import *
username = "rnanthak13@gmail.com"
password = "Chaos_theory1234"

#Mav command python3 mavproxy.py --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out telemetry.airmap.com:16060
if __name__ == '__main__':
    #API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlhbHxMUU5vbExMaEFheTI0UklxR0pkd0Vmb1g0Z0pxIiwiYXBwbGljYXRpb25faWQiOiJhcHBsaWNhdGlvbnw5RTNYd2F2dDh5cXBKd2hFeVBQTXB1TXh4MlJBIiwib3JnYW5pemF0aW9uX2lkIjoiZGV2ZWxvcGVyfFh6R01YbEpJOXptbUJEZndwNmFLUElsUTkyM2QiLCJpYXQiOjE1OTY2OTY0NDB9.7wsWdRI4g8y1BZ8OBc-Lniz3zO90dzfMKtqifWYKQkk"
    API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlhbHxwQUFNWlBxaEx2T2Q2cGZSR2JkMlhDQkdRcTdNIiwiYXBwbGljYXRpb25faWQiOiJhcHBsaWNhdGlvbnx3ZURHZ01oTldtek55c1A4S0xEdlRsQW5QTE0iLCJvcmdhbml6YXRpb25faWQiOiJkZXZlbG9wZXJ8MnpvYmI3eWh4ZVk0cWtDM1BSeDBaSEtNejIzOCIsImlhdCI6MTQ3MTM3OTc0Mn0.MeO0jt6holPt0jdPJvRJrTBi380WsbOPGCEO6u-tfSo"
    client_id = "87b7374e-5a0c-497a-96a0-37393f649fef"
    
    js = get_token_user(client_id, username, password)
    access_token = js['access_token']
    print("Access Token: ",access_token)
    print()
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
    print("Obtained model id: ",model_id)
    
    # print("Creating flight plan")
    required = {}
    
    required["pilot_id"] = pilot_id
    required["token"] = access_token
    required["model_id"] = model_id
    required["nickname"] = "lightsaber"

    aircrafts = get_pilot_aircrafts(API_KEY,required)
    print("Aircrafts :",aircrafts)
    aircraft_id = aircrafts[0]["id"]
    print("Choosing aircraft: ",aircraft_id)
    
    data = {
        "takeoff_latitude": 13.44166667,
        "takeoff_longitude": 80.23194444,
        "pilot_id": pilot_id,
        "aircraft_id": aircraft_id,
        "start_time": "2020-08-20T20:43:44.730Z",
        "end_time":   "2020-08-20T20:50:42.000Z",
        "max_altitude_agl": 100,
        "rulesets":["ind_airmap_rules",
                    "ind_notam"],
        "buffer": 1,
        "geometry": {"type": "Polygon", "coordinates": [[[ 80.23194444,13.44166667], 
                                                         [ 80.23194444,13.44266667],
                                                         [ 80.23394444,13.44266667],
                                                         [ 80.23394444,13.44166667],
                                                         [ 80.23194444,13.44166667]
                                                        ]]
                    }
    }
    print()
    print("\nCreating Flight plan for geometry",data["geometry"])
    created_flightplan = create_flight_plan(API_KEY,access_token,data)
    flight_plan_id = created_flightplan["data"]["id"]
    print("Flight plan id",flight_plan_id)
    
    # print(API_KEY)
    
    # print(flights.keys())
    submit_plan = False
    flight_id = "flight|P58bXJB6eQWkqhg5YXgyA5Kyd0uoMK3ZZ3baXycQEXA49YxxP0"
    print()
    print("Submiting Flight Plan")
    if submit_plan:
        file = open("output.json","w")
        out = get_fligh_brief(API_KEY,access_token,flight_plan_id)
        submission_result = submit_flight_plan(API_KEY,access_token,flight_plan_id)
        try:
            json.dump(submission_result,file)
            flight_id = submission_result["data"]["flight_id"]
            print("Flight ID: ",flight_id)
        except:
            print("Error in submitting plan")
            print(submission_result)
            file.close()
            exit()
        file.close()
        
    else:
        file = open("output.json","r")
        submission_result = json.load(file)
        flight_id = submission_result["data"]["flight_id"]
        file.close()
    
    # flight_id = "flight|G7BDmG6IgezoleUkWaAbzuJlP7pe"
    print("Starting communication")
    secret_key = start_comm(API_KEY,access_token,flight_id)
    print("Secret Key: ",secret_key)
    
    secretKey = base64.b64decode(secret_key)

    HOSTNAME = 'telemetry.airmap.com'
    IPADDR = socket.gethostbyname(HOSTNAME)
    PORTNUM = 16060
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    try:
        s.connect((IPADDR, PORTNUM))
        print("Socket Connected")
        k = input("Type soemthing to close")
        
    except:
        print("Socket Connection Problem")
    s.close()
    print("Socket closed")
    end_comm(API_KEY,access_token,flight_id)
    # end_flight(API_KEY,access_token,flight_id)
    print("Communication Ended")
    
    
    
    