from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views_accounts import *
from .import views_accounts


urlpatterns = [
    path('register/', OwnerRegister.as_view(), name='OwnerRegister'), 
    path('googleowner/', GoogleOwner.as_view(), name='OwnerRegister'), 
    
    
]