from django.urls import path
from .views import (
    register_view,
    logout_view,
    login_view,
    profile_view,
    new_invitation,
    view_invitation,
)

app_name = 'account'


urlpatterns= [
    path('',register_view,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('profile/',profile_view,name='profile'),
    path('invite/',new_invitation,name='invite'), 
    path('view/<int:id>/',view_invitation,name='view'),  
]