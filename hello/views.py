from flask import Flask,request,make_response
import os,json
#import pyowm
#import os
from django.shortcuts import render
from django.http import HttpResponse
import requests

app = Flask(__name__)
#owmapikey=os.environ.get('OWMApiKey') #or provide your key here
#owm = pyowm.OWM(owmapikey)

#geting and sending response to dialogflow
#@app.route('/webhook', methods=['POST'])

def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')
    # return HttpResponse('Hello from Python!')
    # return render(request, "index.html")

@app.route('/')
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>' + "hit")
    # return HttpResponse('Hello from Python!')
    # return render(request, "index.html")

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

@app.route('/getthis')
def dothis(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>' + "hit2")
# return HttpResponse('Hello from Python!')
# return render(request, "index.html")

def webhook():
    req = request.get_json(silent=True, force=True)
    
    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)
    
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#processing the request from dialogflow
def processRequest(req):

    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    latlon_res = observation.get_location()
    lat=str(latlon_res.get_lat())
    lon=str(latlon_res.get_lon())

    wind_res=w.get_wind()
    wind_speed=str(wind_res.get('speed'))

    humidity=str(w.get_humidity())

    celsius_result=w.get_temperature('celsius')
    temp_min_celsius=str(celsius_result.get('temp_min'))
    temp_max_celsius=str(celsius_result.get('temp_max'))

    fahrenheit_result=w.get_temperature('fahrenheit')
    temp_min_fahrenheit=str(fahrenheit_result.get('temp_min'))
    temp_max_fahrenheit=str(fahrenheit_result.get('temp_max'))
    speech = "Today the weather in " + city + ": \n" + "Temperature in Celsius:\nMax temp :"+temp_max_celsius+".\nMin Temp :"+temp_min_celsius+".\nTemperature in Fahrenheit:\nMax temp :"+temp_max_fahrenheit+".\nMin Temp :"+temp_min_fahrenheit+".\nHumidity :"+humidity+".\nWind Speed :"+wind_speed+"\nLatitude :"+lat+".\n  Longitude :"+lon

    return {
        "speech": speech,
        "displayText": speech,
        "source": "dialogflow-weather-by-satheshrgs"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')



#from django.shortcuts import render
#from django.http import HttpResponse
#import requests
#
#from .models import Greeting
#
## Create your views here.
#def index(request):
#    r = requests.get('http://httpbin.org/status/418')
#    print(r.text)
#    return HttpResponse('<pre>' + r.text + '</pre>')
#    # return HttpResponse('Hello from Python!')
#    # return render(request, "index.html")
#
#
#def db(request):
#
#    greeting = Greeting()
#    greeting.save()
#
#    greetings = Greeting.objects.all()
#
#    return render(request, "db.html", {"greetings": greetings})
