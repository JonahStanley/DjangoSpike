# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

def login(request, in_or_out):
    return render_to_response('login.html', {'in_or_out': in_or_out}, context_instance=RequestContext(request))


def register(request):
    return HttpResponse("TESTING2")

@login_required
def edit_profile(request):
    return HttpResponse("TESTING3")

@login_required
def thread(request):
    return HttpResponse("Thread")