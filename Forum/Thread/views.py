# Create your views here.
from django.http import HttpResponse


def hello(request):
    return HttpResponse("hi")


def login(request, in_or_out):
    return HttpResponse("TESTING")


def register(request):
    return HttpResponse("TESTING2")


def edit_profile(request):
    return HttpResponse("TESTING3")

def thread(request):
    return HttpResponse("Thread")