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






class UserList(ListCreateAPIView):
    serializer_class = UserInfoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username', 'user_type', 'is_active']

    # Add PageNumberPagination here
    pagination_class = PageNumberPagination
    # Set the number of items per page as per your requirements
    pagination_class.page_size = 7  

    def get_queryset(self):

        return CustomUser.objects.all().exclude(is_admin=True).order_by('id')


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)  # Paginate the queryset
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class SearchUserList(ListCreateAPIView):
    queryset = CustomUser.objects.all().exclude(is_admin=True)
    serializer_class = UserInfoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email','user_type', 'is_active']  

class UserBlock(APIView):
    def put(self, request, *args, **kwargs):
        # Get the value from the URL parameter
        user_id = kwargs.get('pk')
        print(user_id)
        if user_id is None:
            return Response({'error': 'Please provide a proper input.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the user instance based on the provided pk
            instance =CustomUser.objects.get(pk=user_id)
            print(instance)
        except CustomUser.DoesNotExist:
            return Response({'error': f'User with id={user_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Toggle the value of is_active
        instance.is_active = not instance.is_active
        print(instance)
        serializer = UserInfoSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostList(viewsets.ModelViewSet):
    serializer_class = OwnerPostSerializer
    queryset=Post.objects.all()

   
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        # Check if the user has admin permissions
        if not self.request.user.is_admin:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the 'is_blocked_by_admin' field is present in the request data
        if 'is_blocked_by_admin' in request.data:
            # Block the post if 'is_blocked_by_admin' is set to True
            instance.is_blocked_by_admin = request.data['is_blocked_by_admin']
            instance.save()
            return Response({'detail': 'Post blocked by admin successfully.'}, status=status.HTTP_200_OK)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    


class VerifyPost(APIView):
    def put(self, request, *args, **kwargs):
        # Get the value from the URL parameter
        post_id = kwargs.get('pk')
        print(post_id)
        if post_id is None:
            return Response({'error': 'Please provide a proper input.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the user instance based on the provided pk
            instance =Post.objects.get(pk=post_id)
            print(instance)
        except Post.DoesNotExist:
            return Response({'error': f'User with id={post_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Toggle the value of is_verify
        instance.is_verify = not instance.is_verify
        print(instance)
        serializer = OwnerPostSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)