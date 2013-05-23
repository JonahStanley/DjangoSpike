# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from Thread.models import Post
from forms import *
from django.contrib.auth.models import User


def login(request, in_or_out):
    out = True if "out" in in_or_out else False
    reg = request.GET.get('reg', False)
    valid = True
    if request.POST and not out:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/forum/")
        else:
            valid = False
    if "out" in in_or_out:
            auth.logout(request)
    return render_to_response('login.html', {'in_or_out': out, 'reg': reg, 'valid': valid}, context_instance=RequestContext(request))


def register(request):
    if request.POST:
        user = User.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password'), email=request.POST.get('email'))
        user.firstname = request.POST.get('first_name')
        user.lastname = request.POST.get('last_name'),
        user.save()
        return HttpResponseRedirect("/login/?reg=1")
    form = register_form()
    return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def edit_profile(request):
    return HttpResponse("TESTING3")


@login_required
def thread(request):
    if request.POST:
        if request.POST['todo'] == 'add':
            Post.objects.create(userid=request.POST['userid'], text=request.POST['text'])
        elif request.POST['todo'] == 'del':
            id_to_delete = request.POST['del_id']
            post_to_delete = Post.objects.get(id=id_to_delete)
            post_to_delete.delete()
    posts = Post.objects.order_by('time')
    form = submit_post()
    return render_to_response('thread.html', {'posts': posts, 'form': form, 'user': request.user}, context_instance=RequestContext(request))
