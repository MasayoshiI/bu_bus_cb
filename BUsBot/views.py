from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import datetime




###### test JSON to return to DialogFlow request
estimated_time = "";
testJSON = {
    "fulfillmentText": "This is a text response",
    "fulfillmentMessages": [
        {
            "text": {
                            "text": ["next bus to here in " + estimated_time]
            }
        }
    ],
}

###### TESTJSON ENDS

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
    r = requests.get('http://httpbin.org/status/418')
    print(request.method + " post ")
    body = json.loads(request.body) #translates
    #print(body)
    dict = {}
    bus_stop = ""
    if body["queryResult"]["parameters"]["next_bus"] == "next":
        bus_stop = body["queryResult"]["parameters"]["startingStation1"]
        dict = get_estimate(bus_stop)
    lowest = 1000
    if dict != None:
        for key in dict:
            if (key < lowest):
                lowest = key
    print("lowest: ", lowest)
    ret = returnJSON(round(lowest), bus_stop, dict[lowest])
    json_response = json.dumps(ret)
    print(request.method + " done printing")
    return HttpResponse(json_response, content_type='application/json')

#processes GET requests (accessing index heroku URL)
def processGET(request):
    r = requests.get('http://httpbin.org/status/418')
    print(request.method + " get")
    return HttpResponse('<pre>' + r.text + '</pre>' + "get")

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
    print("get estimate for ", stop_str, " returned ", ret)
    return ret

#helper function for get_estimate; calculates minutes until arrival
def calculate_time_diff(bus_time):
    current = datetime.datetime.now()
    current = current - datetime.timedelta(hours = 5) #adjust for heroku time
    bus_time_obj = datetime.datetime.strptime(bus_time, '%Y-%m-%dT%H:%M:%S-05:00')
    print(current, " ", bus_time_obj, " ", (bus_time_obj - current).seconds/60)
    return (bus_time_obj - current).seconds/60


def returnJSON(time, stop, type):
    ret = {
        "fulfillmentText": "This is a text response",
        "fulfillmentMessages": [
            {
                "text": {
                    "text": ["next bus to " + stop + " is a " + type + " bus that is arriving in " + str(time) + " minutes"]
                }
            }
        ],
    }
    return ret

print(get_estimate("silber"))
