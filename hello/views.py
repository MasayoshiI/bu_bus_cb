from django.shortcuts import render
from django.http import HttpResponse
import requests

from .models import Greeting

# Create your views here.
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(request.headers + " hey" )
    return HttpResponse('<pre>' + r.text + '</pre>' + "index")
    # return HttpResponse('Hello from Python!')
    # return render(request, "index.html")


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

req = requests.Request('POST','http://stackoverflow.com',headers={'X-Custom':'Test'},data='a=1&b=2')
prepared = req.prepare()

def pretty_print_POST(req):
    """
        At this point it is completely built and ready
        to be fired; it is "prepared".
        
        However pay attention at the formatting used in
        this function because it is programmed to be pretty
        printed and may differ from the actual request.
        """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
