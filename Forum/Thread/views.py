# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from Thread.models import Post
from forms import submit_post
from django.contrib.auth.models import User


def login(request, in_or_out):
    out = True if "out" in in_or_out else False
    reg = False
    valid = True
    if request.POST:
        if "false" in request.POST.get('registered'):
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect("/forum/")
            else:
                valid = False
        if "true" in request.POST.get('registered'):
            user = User.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password'), firstname=request.POST.get('firstname'), lastname=request.POST.get('lastname'))
            user.save()
            reg = True
    if "out" in in_or_out:
            auth.logout(request)
    return render_to_response('login.html', {'in_or_out': out, 'reg': reg, 'valid': valid}, context_instance=RequestContext(request))


def register(request):
    return render_to_response('register.html', context_instance=RequestContext(request))


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
