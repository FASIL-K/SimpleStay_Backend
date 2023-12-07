from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views_accounts import OwnerRegister, GoogleOwner
from .views import PostCreateView,PostList

urlpatterns = [
    path('register/', OwnerRegister.as_view(), name='OwnerRegister'), 
    path('googleowner/', GoogleOwner.as_view(), name='GoogleOwner'),
    path('createpost/', PostCreateView.as_view(), name='PostCreate'),  # Add this line for creating a post
    path('postlist/',PostList.as_view(), name='PostList'),
]
