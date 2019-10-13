from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate
from .models import MyUser,Team,Invitation

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required  Add a valid email address')

    class Meta:
        model = MyUser 
        fields =  ['email', 'username','password1', 'password2']



class AccountAuthenticateForm(forms.ModelForm):
    password=forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email','password')
    
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email,password=password):
            raise forms.ValidationError("Invalid login")


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        exclude = ['created_by','is_admin']



class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = '__all__'
        exclude = ['from_user']
    