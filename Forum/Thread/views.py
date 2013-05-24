# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from Thread.models import Post
from forms import *
from django.contrib.auth.models import User


def login(request, in_or_out):
    out = True if "out" in in_or_out else False
    ignore = (request.POST.get('todo') == 'redirect')
    if ignore:
        out = False
    reg = request.GET.get('reg', False)
    next = request.GET.get(u'next', '/forum/')
    valid = True
    if request.POST and not out and not ignore:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(next)
        else:
            valid = False
    if "out" in in_or_out and not ignore:
            auth.logout(request)
    return render_to_response('login.html', {'in_or_out': out, 'reg': reg, 'valid': valid, 'next': next}, context_instance=RequestContext(request))


def register(request):
    duplicate = False
    if request.POST:
        username = request.POST.get('username')
        if User.objects.filter(username=username):
            duplicate = True
        else:
            user = User.objects.create_user(username=username, password=request.POST.get('password'), email=request.POST.get('email'))
            user.firstname = request.POST.get('first_name')
            user.lastname = request.POST.get('last_name'),
            user.save()
            return HttpResponseRedirect("/login/?reg=1")
    form = register_form()
    return render_to_response('register.html', {'form': form, 'duplicate': duplicate}, context_instance=RequestContext(request))


@login_required
def edit_profile(request):
    duplicate = False
    edited = False
    authenticated = True
    curUser = request.user.username
    if request.POST:
        username = request.POST.get('username')
        if request.POST.get('delete') == 'delete':
            olduser = User.objects.get(username=request.user.username)
            auth.logout(request)
            olduser.delete()
            return HttpResponseRedirect("/login/")
        elif request.POST.get('oldpassword') == '':
            authenticated = False
        elif auth.authenticate(username=curUser, password=request.POST.get('oldpassword')) is None:
            authenticated = False
        elif username == request.user.username:
            newuser = User.objects.get(username=username)
            newuser.set_password(request.POST.get('password'))
            newuser.first_name = request.POST.get('firstname')
            newuser.last_name = request.POST.get('lastname')
            newuser.email = request.POST.get('email')
            newuser.save()
            edited = True
        else:
            if User.objects.filter(username=username):
                duplicate = True
            else:
                newuser = User.objects.get(username=request.user.username)
                newuser.username = request.POST.get('username')
                newuser.set_password(request.POST.get('password'))
                newuser.first_name = request.POST.get('firstname')
                newuser.last_name = request.POST.get('lastname')
                newuser.email = request.POST.get('email')
                newuser.save()
                user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
                if user is None and not user.is_active:
                    raise WEIRDERROR
                auth.login(request, user)
                changePosts(curUser, username)
                edited = True
    form = register_form()
    return render_to_response('edit-profile.html', {'form': form, 'user': User.objects.get(username=request.user.username), 'duplicate': duplicate, 'edited': edited, 'authenticated': authenticated}, context_instance=RequestContext(request))


def thread(request):
    if request.POST:
        if not request.user.is_anonymous():
            if request.POST['todo'] == 'add':
                Post.objects.create(username=request.user.username, text=request.POST['text'])
            elif request.POST['todo'] == 'del':
                id_to_delete = request.POST['del_id']
                if Post.objects.filter(id=id_to_delete):
                    post_to_delete = Post.objects.filter(id=id_to_delete)[0]
                    if request.user.username == post_to_delete.username:
                        post_to_delete.delete()
    posts = Post.objects.order_by('time')
    form = submit_post()
    return render_to_response('thread.html', {'posts': posts, 'form': form, 'user': request.user, 'anon': request.user.is_anonymous()}, context_instance=RequestContext(request))


def edit_post(request):
    D = {}
    if request.POST:
        if not request.user.is_anonymous():
            #get id of post to edit
            edit_id = request.POST.get('edit_id', '')
            new_text = request.POST.get('new_text', '')

            #make sure post exists
            try:
                post = Post.objects.get(id=edit_id)
                #check that user owns this post, if so update
            except:
                D = {'error': 'post nonexistant'}
            else:
                if request.user.username == post.username:
                    post.text = new_text
                    post.save()
    return HttpResponseRedirect("/forum/", D)


def changePosts(oldName, newName):
    allPosts = Post.objects.filter(username=oldName)
    for post in allPosts:
        post.username = newName
        post.save()
