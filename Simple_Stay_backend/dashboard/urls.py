
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
    path('listproperty/', PostList.as_view({'get': 'list'}), name='postlist'),
    path('listproperty/<int:pk>/update/', PostList.as_view({'put': 'update'}), name='post-update'),

    path('post_verification/<int:pk>/',VerifyPost.as_view(),name='postverification'),

    path('usercount/<str:type>/', UserCountAPIView.as_view(), name='user_count_viewer'),
    path('premium/', TotalRevenueAPI.as_view(), name='total_premium_sales'),
    # path('conference/', ConferenceHallSales.as_view(), name='ConferenceHallSales'),
    # path('admin/cowork/', CoworkingSpaceSales.as_view(), name='CoworkingSpaceSales'),
    path('premiumplan/', PremiumSales.as_view(), name='PremiumSales'),




]
