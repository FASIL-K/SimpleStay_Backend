from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from .views_accounts import *
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# for customer
router.register(r'property-post/(?P<owner_id>\d+)', PostViewSet, basename='propertypost')

# for user  
# router.register(r'conference', UserConferenceHall, basename='userConference')
router.register(r'post',UserPostViewSet, basename='userPost')
router.register(r'post/(?P<post_id>\d+)', UserPostViewSet, basename='userSinglePost')

urlpatterns = [
    path('', include(router.urls)),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', OwnerRegister.as_view(), name='OwnerRegister'), 
    path('googleowner/', GoogleOwner.as_view(), name='GoogleOwner'),
    path('postlist/',PostList.as_view(), name='PostList'),
    path('property-post/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='propertypost-detail'),
    path('logout/',OwnerLogout.as_view(), name='PostList'),

    
]
