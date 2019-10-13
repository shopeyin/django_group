from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, Permission,User
from .forms import RegistrationForm,AccountAuthenticateForm,UserGroupForm,InvitationForm
from django.contrib.auth import login, authenticate,logout
from .models import MyUser,Team,Invitation

def register_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    else:
        context ={}
        if request.POST:
            form=RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email,password=raw_password)
                login(request,account)
                return redirect('account:profile')
            else:
                context['registration_form'] = form
        else:
            form = RegistrationForm()
            context['registration_form'] = form
        return render(request, 'account/register.html',context)


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticateForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)

            if user:
                login(request, user)
                return redirect('account:profile')
    else:
        form = AccountAuthenticateForm()
    context['login_form'] = form
    return render(request, 'account/login.html',context) 



def profile_view(request):
    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            created_by = MyUser.objects.filter(email=request.user.email).first()
            obj=form.save(commit=False)
            obj.created_by = created_by
            form.save()
            group=Team.objects.get(name=name)
            group.user_set.add(request.user)
            return redirect('account:profile')
    else:
        form = UserGroupForm()
    context = {'form': form}
    
    team = Team.objects.filter(created_by= request.user)
    context['team'] = team

    invitation = Invitation.objects.filter(to_user=request.user)
    context['invitation'] = invitation

    try:
        group = MyUser.objects.filter(groups__name=team[0])
    except IndexError:
        group = []


    num_of_members=group.count()
    context['num_of_members']=num_of_members

    context['group'] = group

    return render(request, 'account/profile.html',context) 


@login_required
def new_invitation(request):
    if request.method =='POST':
        invitation = Invitation(from_user=request.user)
        form = InvitationForm(request.POST ,instance=invitation)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = InvitationForm() 
    context={'form':form}
    return render(request,'account/new_invite.html',context)


@login_required
def view_invitation(request,id):
    context = {}
    invitation = get_object_or_404(Invitation,id=id)
    context['invitation'] = invitation
    return render(request,'account/accept.html',context)



def accept_invitation(request):
    pass

def logout_view(request):
    logout(request)
    return redirect('home')


