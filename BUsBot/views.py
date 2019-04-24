from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import datetime
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles import finders


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

bus_stop_dict_inverse = {
    "4160734":"marsh_plaza",
    "4160738":"cfa",
    "4160714":"stuvi",
    "4114006":"amory",
    "4149154":"stmary",
    "4068466":"blandford",
    "4068470":"hotel",
    "4110206":"huntingtonm6",
    "4068482":"albany",
    "4160718":"huntingtonc2",
    "4160722":"danielsen",
    "4160726":"myles",
    "4160730":"silber",
    #TODO: figure out what stops these are--also need to add these to non inverse dict
    "4221172":"temp",
    "4221926":"temp",
    "4117702":"temp",
    "4160750":"temp",
    "4221170":"temp",
    "4149166":"temp",
    "4160746":"temp",
    "4160742":"temp",
    "4221168":"temp",
    "4117694":"temp",
    "4149158":"temp",
    "4117698":"temp",
    "4149162":"temp",
    "4221178":"temp"
}

#NOTES: use command "heroku logs --tail" on terminal to see print statements
#URLs are encoded in urls.py

# Create your views here.
@csrf_exempt #for security clearance, not sure what vulnerabilities it leads to
#requests to gentle-dawn URL get processed with the method
def index(request):
    if(request.method == "GET"):
        return processGET(request)
    else:
        return processPOST(request)

#test function for /df URL
def df(request):
    r = requests.get('http://httpbin.org/status/418')
    return HttpResponse('<pre>' + r.text + '</pre>'  + "df")

#processes POST requests from dialog flow
def processPOST(request):
    body = json.loads(request.body) #translates
    print("printing body")
    print(body);
    print("done printing body")
    ret = ""
    if body["queryResult"]["parameters"]["next"] == "next_arrival_time":
        bus_stop = body["queryResult"]["parameters"]["station"]
        ret = find_next_bus(bus_stop)
    json_response = json.dumps(ret)
    print(ret)
    print(request.method + " done printing")
    return HttpResponse(json_response, content_type='application/json')

#processes GET requests (accessing index heroku URL)
def processGET(request):
    r = requests.get('http://httpbin.org/status/418')
    print(request.method + " get")
    return HttpResponse('<pre>' + r.text + '</pre>' + "get")


#TODO: need to figure out how root is found to access static privacypolicy.txt
def privacypolicy(request):
    path = finders.find('privacypolicy.txt')
    #searched_locations = finders.searched_locations
    print(path);
    policy = open(path, "r")
    return HttpResponse(policy.read())

data = {}
#establish connection to bu bus server data, load json into program for processing
def read_bus_data():
    global data
    r = requests.get('https://www.bu.edu/bumobile/rpc/bus/livebus.json.php', auth=('user', 'pass'))
    #print(r.status_code, " <-- if 200, successful connection")
    data = json.loads(r.text)




def find_next_bus(bus_stop):
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


def find_stops_with_data():
    return create_stops_with_data_DS()



#takes in bus stop string, returns a dictionary {minutes until next arrival:bus_route}#
def create_next_bus_DS(stop_str):
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
                    time_until = helper_calculate_time_diff(stops["arrival_at"])
                    ret[time_until] = bus["route"]
    print("getting estimate for ", stop_str, " returned ", ret)
    return ret



#returns set with names of stops that have data, empty set if no data
def create_stops_with_data_DS():
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


#helper function for get_estimate; calculates minutes until arrival
def helper_calculate_time_diff(bus_time):
    current = datetime.datetime.now()
    current = current - datetime.timedelta(hours = 5) #adjust for heroku time
    bus_time_obj = datetime.datetime.strptime(bus_time, '%Y-%m-%dT%H:%M:%S-05:00')
    #print(current, " ", bus_time_obj, " ", (bus_time_obj - current).seconds/60)
    return (bus_time_obj - current).seconds/60


def return_next_bus_JSON(time, stop, type):
    ret = {
        "fulfillmentText": "This is a text response",
        "fulfillmentMessages": [
            {
                "text": {
                    "text": ["The next bus to " + stop + " is a " + type + " bus that is arriving in " + str(time) + " minutes!"]
                }
            }
        ],
    }
    return ret

def return_no_info_for_stop_JSON():
    ret = {}
    stops_with_data = find_stops_with_data()
    if len(stops_with_data) != 0:
        temp = ", ".join(stops_with_data)
        ret = {
            "fulfillmentText": "This is a text response",
            "fulfillmentMessages": [
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
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": ["Unfortunately I don't have data for the next arrival times for bus stops at this moment. Please try again in a bit!"]
                    }
                }
            ],
        }
    return ret


###for printing POST requests
#def print_POST(request):
#    print ()
#
#
###ALERT MODULE##
#
def alert(request):
    print("ouch")
#