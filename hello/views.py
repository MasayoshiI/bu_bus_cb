from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json


from .models import Greeting

###### test JSON to return to DialogFlow request

testJSON = {
    "speech":"response",
    "displayText":"you're great! displayText",
    "message": {
        "speech": "you're great! speech",
        "type": 0
    },
}

###### TESTJSON ENDS



# Create your views here.
@csrf_exempt
def index(request):
    if(request.method == "GET"):
        return indexGET(request)
    else:
        return processPOST(request)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

def df(request):
    r = requests.get('http://httpbin.org/status/418')
    pretty_print_POST(request);
    return HttpResponse('<pre>' + r.text + '</pre>'  + "df")
# return HttpResponse('Hello from Python!')
# return render(request, "index.html")

def processPOST(request):
    r = requests.get('http://httpbin.org/status/418')
    print(request.method + " post ")
    body = json.loads(request.body)
    print(body)
    json_response = json.dumps(testJSON)
    print(request.method + " done printing")
    return HttpResponse(json_response, content_type='application/json')
#return HttpResponse('<pre>' + r.text + '</pre>' + "post")
# return HttpResponse('Hello from Python!')
# return render(request, "index.html")

def indexGET(request):
    r = requests.get('http://httpbin.org/status/418')
    print(request.method + " get")
    return HttpResponse('<pre>' + r.text + '</pre>' + "get")
# return HttpResponse('Hello from Python!')
# return render(request, "index.html")

