
from django.urls import path
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views_accounts import *
from .views import *


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('listuser/', UserList.as_view(),name = 'listuser'),
    path('user_block_unblock/<int:pk>/',UserBlock.as_view(),name='userblock'),
    path('searchuser/', SearchUserList.as_view(),name = 'searchuser'),



]
