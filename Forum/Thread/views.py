# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth


def login(request, in_or_out):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            return HttpResponseRedirect("edit-profile")
        else:
            return HttpResponseRedirect("register")
    return render_to_response('login.html', {'in_or_out': in_or_out}, context_instance=RequestContext(request))


def register(request):
    return HttpResponse("TESTING2")


@login_required
def edit_profile(request):
    return HttpResponse("TESTING3")


def thread(request):
    posts = 1
    return render_to_response('thread.html', {'posts': posts}, context_instance=RequestContext(request))
