

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views_accounts import *
from .import views_accounts

urlpatterns = [

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegister.as_view(),name = 'register'),
    path('googleuser/', GoogleUser.as_view(),name = 'googleuser'),
    path('activate/<uidb64>/<token> ', views_accounts.activate, name='activate'),

]
