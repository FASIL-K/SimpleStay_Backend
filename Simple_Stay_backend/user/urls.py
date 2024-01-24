

from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView
from .views_accounts import *
from.views import *

from .import views_accounts
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import (TokenRefreshView)
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegister.as_view(),name = 'register'),
    path('googleuser/', GoogleUser.as_view(),name = 'googleuser'),
    path('activate/<uidb64>/<token> ', views_accounts.activate, name='activate'),
    path('resend-verification-email/', UserRegister.as_view(), name='resend_verification_email'),
    # path('authentication/',views_accounts.Authentication.as_view(), name='Authentication'), 
    path('logout/',views_accounts.logout.as_view(), name='logout'), 
    # path('logout/', views_accounts.LogoutView.as_view(), name ='logout'),

    # path('token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
    # path('refreshtoken/',views_accounts.RefreshTokenAuto.as_view(),name ='RefreshTokenAuto'),
    path('searchpost/', SearchPostList.as_view(),name = 'searchpost'),

]

