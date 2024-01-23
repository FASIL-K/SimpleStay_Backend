

from django.urls import path
from .views import *

urlpatterns = [

    path('createsaved/',CreateSavedView.as_view(),name='createsaved'),
    path('listsaved/<int:user_id>/',ListSavedbyUser.as_view(),name='listsaved'),
    path('saveview/',IsSavedView.as_view(),name='saveview'),

]

