from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from .views_accounts import OwnerRegister, GoogleOwner
from .views import PostList, PostViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# for customer
router.register(r'property-post/(?P<owner_id>\d+)', PostViewSet, basename='propertypost')
# for user
# router.register(r'conference', UserConferenceHall, basename='userConference')
# router.register(r'cowork',UserCoWorkView, basename='userCoWork')

urlpatterns = [
    path('', include(router.urls)),

    path('register/', OwnerRegister.as_view(), name='OwnerRegister'), 
    path('googleowner/', GoogleOwner.as_view(), name='GoogleOwner'),
    path('postlist/',PostList.as_view(), name='PostList'),
    path('property-post/<int:owner_id>/<int:post_id>/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='propertypost-detail'),

    
]
