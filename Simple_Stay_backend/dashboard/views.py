from urllib import response
from rest_framework.generics import RetrieveDestroyAPIView,ListAPIView,UpdateAPIView,ListCreateAPIView
from user.models import CustomUser
from user.serializers import UserInfoSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination








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