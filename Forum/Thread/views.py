# Create your views here.
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from Thread.models import Post
from forms import submit_post


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
    if request.POST:
        if request.POST['todo'] == 'add':
            p = Post(userid=request.POST['userid'], text=request.POST['text'])
            p.save()
        elif request.POST['todo'] == 'del':
            id_to_delete = request.POST['del_id']
            post_to_delete = Post.objects.get(id=id_to_delete)
            post_to_delete.delete()
    posts = Post.objects.order_by('time')
    form = submit_post()
    return render_to_response('thread.html', {'posts': posts, 'form': form}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/forum/")
