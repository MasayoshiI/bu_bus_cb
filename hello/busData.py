import requests
import json
import datetime

bus_stop_dict = {
    "marsh_plaza":"4160734",
    "cfa":"4160738",
    "stuvi":"4160714",
    "amory":"4114006",
    "stmary":"4149154",
    "blandford":"4068466",
    "hotel":"4068470",
    "huntingtonm6":"4110206",
    "albany":"4068482",
    "huntingtonc2":"4160718",
    "danielsen":"4160722",
    "myles":"4160726",
    "silber":"4160730"
}

data = {}

#establish connection to bu bus server data, load json into program for processing
def read_bus_data():
    global data
    r = requests.get('https://www.bu.edu/bumobile/rpc/bus/livebus.json.php', auth=('user', 'pass'))
    #print(r.status_code, " <-- if 200, successful connection")
    data = json.loads(r.text)

#takes in bus stop string, returns a dictionary {minutes until next arrival:bus_route}#
def get_estimate(stop_str):
    read_bus_data()
    ret = {}
    stop_id = bus_stop_dict[stop_str]
    for bus in data["ResultSet"]["Result"]:
        estimates = bus.get("arrival_estimates")
        #print(bus["id"], " ", bus["route"])
        if(estimates != None):
            for stops in estimates:
                if(stops["stop_id"] == stop_id):
                    time_until = calculate_time_diff(stops["arrival_at"])
                    ret[time_until] = bus["route"]
    print(ret)

#helper function for get_estimate; calculates minutes until arrival
def calculate_time_diff(bus_time):
    current = datetime.datetime.now()
    bus_time_obj = datetime.datetime.strptime(bus_time, '%Y-%m-%dT%H:%M:%S-05:00')
    return (bus_time_obj - current).seconds/60
#    print(current, " bus time", bus_time_obj)
#    print(bus_time_obj - current)



get_estimate("silber")

def returnJSON(time):
    ret = {
        "fulfillmentText": "This is a text response",
        "fulfillmentMessages": [
            {
                "text": {
                    "text": ["next bus to here in " + time]
                }
            }
        ],
    }
    return ret
