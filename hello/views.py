from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json


from .models import Greeting

###### test JSON to return to DialogFlow request

testJSON = {
"speech": "this text is spoken out loud if the platform supports voice interactions",
"displayText": "this text is displayed visually",
"messages": {
    "type": 1,
        "title": "card title",
            "subtitle": "card text",
                "imageUrl": "https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png"
},
"data": {
    "google": {
    "expectUserResponse": true,
    "richResponse": {
        "items": [
                  {
                  "simpleResponse": {
                  "textToSpeech": "this is a simple response"
                  }
                  }
                  ]
}
    },
        "facebook": {
"text": "Hello, Facebook!"
    },
        "slack": {
"text": "This is a text response for Slack."
}
},
"contextOut": [
               {
               "name": "context name",
               "lifespan": 5,
               "parameters": {
               "param": "param value"
               }
               }
               ],
"source": "example.com",
"followupEvent": {
    "name": "event name",
        "parameters": {
"param": "param value"
}
}

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
    return json_response
#return HttpResponse('<pre>' + r.text + '</pre>' + "post")
# return HttpResponse('Hello from Python!')
# return render(request, "index.html")

def indexGET(request):
    r = requests.get('http://httpbin.org/status/418')
    print(request.method + " get")
    return HttpResponse('<pre>' + r.text + '</pre>' + "get")
# return HttpResponse('Hello from Python!')
# return render(request, "index.html")

