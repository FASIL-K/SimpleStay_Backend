from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView,ListAPIView
from user.models import CustomUser 

from rest_framework.filters import SearchFilter



class PreviousMessagesView(ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = None

    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = 'chat_'+thread_suffix
        queryset = Message.objects.filter(
            thread_name=thread_name
        )
        return queryset
    
class UserList(ListAPIView):
    serializer_class = UserListSerializer
    queryset=CustomUser.objects.filter(user_type='user')

class CustomerList(ListAPIView):
    serializer_class = UserListSerializer
    queryset = CustomUser.objects.filter(user_type='owner')



class ChatListUsers(ListAPIView):
    serializer_class = UserListSerializer
    lookup_field = 'id'
    filter_backends = [SearchFilter]
    filterset_fields = ['username', 'email']

    def get_queryset(self):
        user_id = self.kwargs.get('id')

        chat_users = Message.objects.filter(sender_id=user_id).values_list(
            'receiver', flat=True).distinct()
        users_query = CustomUser.objects.filter(id__in=chat_users)

        return users_query

    def list(self, request, *args, **kwargs):
        sender_users = Message.objects.filter(
            sender_id=self.kwargs.get('id')).values_list('receiver', flat=True).distinct()
        receiver_users = Message.objects.filter(
            receiver_id=self.kwargs.get('id')).values_list('sender', flat=True).distinct()
        chat_users = set(sender_users).union(receiver_users)

        users_data = []

        for user_id in chat_users:
            try:
                user = CustomUser.objects.get(id=user_id)
                user_data = {
                    'id': user.id,
                    'username': user.name,
                    'email': user.email,
                }
                users_data.append(user_data)
            except CustomUser.DoesNotExist:
                pass

        return Response(users_data, status=status.HTTP_200_OK)