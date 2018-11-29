from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests


from .models import Greeting

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
    for key,val in request.POST.dict():
        print (key, "=>", val)
    print(request.method + " done printing")
    return HttpResponse('<pre>' + r.text + '</pre>' + "post")
# return HttpResponse('Hello from Python!')
# return render(request, "index.html")

def indexGET(request):
    r = requests.get('http://httpbin.org/status/418')
    print(request.method + " get")
    return HttpResponse('<pre>' + r.text + '</pre>' + "get")
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
