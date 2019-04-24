import requests
import json
import datetime

class Next_bus:

    def __init__(self, bus_stop):
        self.bus_stop = bus_stop
    
    def find_next_bus(self, bus_stop):
        next_bus_DS = create_next_bus_DS(bus_stop)
        lowest = 1000
        ret = {}
        
        if next_bus_DS != None and len(next_bus_DS) != 0:
            print("next bus exists")
            for key in next_bus_DS:
                if (key < lowest):
                    lowest = key
                if lowest == 1000:
                    ret = return_no_info_for_stop_JSON()
                else:
                    ret = return_next_bus_JSON(round(lowest), bus_stop, next_bus_DS[lowest])
        else:
            ret = return_no_info_for_stop_JSON()
        print(lowest)
        return ret


    def return_next_bus_JSON(self, time, stop, type):
        ret = {
        "fulfillmentText": "This is a text response",
        "fulfillmentMessages": 
        [
            {
                "text": 
                {
                    "text": ["The next bus to " + stop + " is a " + type + " bus that is arriving in " + str(time) + " minutes"]
                }
            }
        ],
        }
        return ret
    data = {}
    #establish connection to bu bus server data, load json into program for processing
    def read_bus_data(self):
        global data
        r = requests.get('https://www.bu.edu/bumobile/rpc/bus/livebus.json.php', auth=('user', 'pass'))
        #print(r.status_code, " <-- if 200, successful connection")
        data = json.loads(r.text)
    def return_no_info_for_stop_JSON(self):
        ret = {}
        stops_with_data = find_stops_with_data()
        if len(stops_with_data) != 0:
            temp = ", ".join(stops_with_data)
            ret = {
            "fulfillmentText": "This is a text response",
            "fulfillmentMessages": 
            [
                {
                    "text": {
                        "text": ["Unfortunately I don't have arrival time data for that stop...try one of these stops instead: " + temp]
                            }
                }
            ],
            }
        else:
            ret = {
            "fulfillmentText": "This is a text response",
            "fulfillmentMessages": 
            [
                {
                    "text": {
                        "text": 
                        ["Unfortunately I don't have data for the next arrival times for bus stops at this moment. Please try again in a bit!"]
                    }
                }
            ],
            }
        return ret

    def find_stops_with_data(self):
        return create_stops_with_data_DS()

    #returns set with names of stops that have data, empty set if no data
    def create_stops_with_data_DS(self):
        print("create_stops_with_data_DS() called")
        read_bus_data()
        seen_stops = set()
        ret = set()
        for bus in data["ResultSet"]["Result"]:
            estimates = bus.get("arrival_estimates")
            if(estimates != None):
                for stops in estimates:
                    seen_stops.add(stops["stop_id"])
        for stop in seen_stops:
            ret.add(bus_stop_dict_inverse[stop])
        return ret

    #takes in bus stop string, returns a dictionary {minutes until next arrival:bus_route}#
    def create_next_bus_DS(self, stop_str):
        print("create_next_bus_DS() called")
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
        print("getting estimate for ", stop_str, " returned ", ret)
        return ret
    
    #helper function for get_estimate; calculates minutes until arrival
    def calculate_time_diff(self, bus_time):
        current = datetime.datetime.now()
        current = current - datetime.timedelta(hours = 5) #adjust for heroku time
        bus_time_obj = datetime.datetime.strptime(bus_time, '%Y-%m-%dT%H:%M:%S-05:00')
        #print(current, " ", bus_time_obj, " ", (bus_time_obj - current).seconds/60)
        return (bus_time_obj - current).seconds/60
    

