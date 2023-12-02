
from django.urls import path
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views_accounts import *
from .import views_accounts


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
