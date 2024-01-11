from urllib import response
from rest_framework.generics import RetrieveDestroyAPIView,ListAPIView,UpdateAPIView,ListCreateAPIView
from user.models import CustomUser
from user.serializers import UserInfoSerializer
from rest_framework import status,viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from owner.serializers import OwnerPostSerializer
from owner.models import Post
from rest_framework.decorators import action





class SearchPostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = OwnerPostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['locality','city', 'house_name']  
