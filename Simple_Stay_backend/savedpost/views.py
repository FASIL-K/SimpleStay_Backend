from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from .models import SavedPost
from .serializers import SavedListSerializer,SavedCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status

# Create your views here.

class CreateSavedView(CreateAPIView):
    queryset=SavedPost.objects.all()
    serializer_class=SavedCreateSerializer
    permission_classes = (IsAuthenticated,)


class ListSavedbyUser(ListAPIView):
    serializer_class=SavedListSerializer
    filter_backends = [SearchFilter]
    search_fields=['title','topic__topic']
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        
        return SavedPost.objects.filter(user=self.kwargs['user_id']).order_by('-created_at')

class IsSavedView(RetrieveUpdateDestroyAPIView):
    serializer_class=SavedCreateSerializer
    queryset=SavedPost.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        
        user_id=request.GET.get('user_id')
        post_id=request.GET.get('post_id')  

        Is_saved=SavedPost.objects.filter(user=user_id,post=post_id).exists()

        return Response({'detail':'saved checked successfully','saved':Is_saved},status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        
        user_id=request.GET.get('user_id')
        post_id=request.GET.get('post_id')


        Is_saved=SavedPost.objects.filter(user=user_id,post=post_id).first()
        if Is_saved:
            Is_saved.delete()

            return Response({'detail':'item deleted from saved',"saved":False},status=status.HTTP_301_MOVED_PERMANENTLY)
        else:
            return Response({'detail':"saved not found"},status=status.HTTP_404_NOT_FOUND)
