from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, Permission,User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from account.models import MyUser,Team,Invitation


def home_view(request):
    context = {}
    group = Group.objects.all()
    context['group'] = group

    return render(request, 'theapp/home.html',context)


def group_detail_view(request,id):
    context = {}
    group =get_object_or_404(Team,id=id)
    context['group'] = group
    return render(request,'theapp/detail.html',context)


def join_group_view(request,id):
    group = get_object_or_404(Team,id=id)
    group.user_set.add(request.user)
    messages.success(request, 'You have joined  %s group' % group.name)
    return redirect('home')



