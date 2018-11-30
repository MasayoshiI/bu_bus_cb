from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import busData.py


from .models import Greeting

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
def index(request):
    if(request.method == "GET"):
        return processGET(request)
    else:
        return processPOST(request)

#default function for heroku apps, function for /db URL
def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})

#test function for /df URL
def df(request):
    r = requests.get('http://httpbin.org/status/418')
    return HttpResponse('<pre>' + r.text + '</pre>'  + "df")

#processes POST requests from dialog flow
def processPOST(request):
    r = requests.get('http://httpbin.org/status/418')
    print(request.method + " post ")
    body = json.loads(request.body) #translates
    print(body)
    dict = {}
    if(body["queryResult"]["parameters"]["next_bus"] == "next"){
        bus_stop = body["queryResult"]["parameters"]["startingStation1"]
        dict = busData.get_estimate(bus_stop)
    }
    lowest = 1000
    for key in dict:
        if (key < lowest):
            lowest = key
    global estimated_time = lowest
    json_response = json.dumps(testJSON)
    print(request.method + " done printing")
    return HttpResponse(json_response, content_type='application/json')

#processes GET requests (accessing index heroku URL)
def processGET(request):
    r = requests.get('http://httpbin.org/status/418')
    print(request.method + " get")
    return HttpResponse('<pre>' + r.text + '</pre>' + "get")

