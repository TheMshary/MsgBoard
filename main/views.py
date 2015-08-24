from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.models import User

import json

# from django.contrib.auth.decorators import login_required
# if request.user.pk != obj.user.pk:
#   THROW OUT


# Create your views here.

from main.models import Division, Board, Comment
from main.forms import DivisionForm, BoardForm, CommentForm, UserSignup, UserLogin


# ######################### FRONTPAGES ##################################

def index(request):

    usersignup = UserSignup()
    userlogin = UserLogin()
    creatediv = DivisionForm()
    context = {}

    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                context['password_valid'] = "Login Successful"
            else:
                context['password_valid'] = "Invalid User. Please try again."
        else:
            context['password_valid'] = form.errors
    context['login'] = userlogin
    context['signup'] = usersignup
    context['divform'] = creatediv
    context['title'] = "home page"
    context['divs'] = divs()

    return render_to_response('main.html', context,
                              context_instance=RequestContext(request))


def divs():
    divisions = Division.objects.all()
    divs = []
    for div in divisions:
        divs.append(div)
    return divs


# ######################### MAKE STUFF AND LOGIN ##########################


def mkdiv(request):
    if request.method == 'POST':
        form = DivisionForm()

        if request.method == 'POST':
            form = DivisionForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']

                div, created = Division.objects.get_or_create(
                    name=name, user=request.user)
                if not created:
                    div.save()
                else:
                    print "ERROR :::: Division "+div.name+" already exists"
            else:
                print "ERROR :::: "+str(form.errors)
        else:
            print "ERROR :::: Please contact us about this error so we can fix it ASAP."

        return HttpResponseRedirect('/')
    else:
        return render_to_response('mkdiv.html', context,
                                  context_instance=RequestContext(request))


def mkboard(request, pk):
    form = BoardForm()

    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            div = Division.objects.get(pk=pk)
            board = Board(name=name, user=request.user, division=div)
            board.save()
        else:
            print "ERROR :::: "+str(form.errors)
    else:
        print
        "ERROR :::: Please contact us about this error so we can fix it ASAP."

    return HttpResponseRedirect('/div/'+pk)


def mkcomment(request, pk, parent_comment=None):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            board = Board.objects.get(pk=pk)
            comment = Comment(user=request.user, board=board, text=text,
                              parent_comment=Comment.objects.get(
                                pk=parent_comment))
            comment.save()
        else:
            print "ERROR :::: "+str(form.errors)
    else:
        print "ERROR :::: HAHA LOLOLOLOLOL!!!!!!!"

    return HttpResponseRedirect('/board/'+pk)


@csrf_exempt
def usersignup(request):

    context = {}

    form = UserSignup()
    context['form'] = form

    if request.method == 'POST':
        form = UserSignup(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                new_user = User.objects.create_user(name, email, password)
                context['signup_valid'] = "Thank you for signing up!"

                auth_user = authenticate(username=name, password=password)
                login(request, auth_user)

                return HttpResponseRedirect('/')
            except IntegrityError, e:
                context['signup_valid'] = "A user with that name is already taken. Please try again."

        else:
            context['signup_valid'] = form.errors
    context['signup'] = UserSignup()
    context['login'] = UserLogin()

    return render_to_response('index.html', context,
                              context_instance=RequestContext(request))


def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/')


# ######################### URLs ##################################


def div_url(request, pk):
    context = {}
    div = Division.objects.get(pk=pk)
    form = BoardForm()
    boards = Board.objects.filter(division=div)

    context['div'] = div
    context['title'] = "Division"
    context['form'] = form
    context['boards'] = boards
    return render_to_response('div_page.html', context,
                              context_instance=RequestContext(request))


def board_url(request, pk):
    context = {}
    board = Board.objects.get(pk=pk)
    comments = Comment.objects.filter(board=board)

    context['board'] = board
    context['title'] = "Message Board"
    context['list'] = json.dumps(
        work_plz_v2(comments.filter(parent_comment=None)))
    context['comment_form'] = CommentForm()
    return render_to_response('board_page.html', context,
                              context_instance=RequestContext(request))


def work_plz_v2(comments):
    ilist = []
    for comment in comments:
        comms = Comment.objects.filter(parent_comment=comment)
        if comms is not None:
            ilist.append({'username': comment.user.username, 'txt':
                          comment.text, 'pk': comment.pk,
                          'children': work_plz_v2(comms)})
        else:
            ilist.append({'username': comment.user.username, 'txt':
                          comment.text, 'pk': comment.pk, 'children': None})
    return ilist


def print_work(ilist, ilvl):
    indent = "\t"*ilvl
    for i in ilist:
        if i[1] is not None:
            print "%s%s" % (indent, i[0])
            print_work(i[1], ilvl+1)
        else:
            print "%s%s" % (indent, i[1])
            print "%s%s" % (indent, "None")


# ######################### DATABASE CLEANERS #################################

def clear_divs(request):
    Division.objects.all().delete()
    return HttpResponseRedirect('/')
