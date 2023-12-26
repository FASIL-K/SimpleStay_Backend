from rest_framework.generics import ListCreateAPIView ,ListAPIView , CreateAPIView ,RetrieveUpdateAPIView
from .models import Post, PropertyImage
from .serializers import OwnerPostSerializer, PropertyImageSerializer
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response




class PostViewSet(viewsets.ModelViewSet):
    serializer_class = OwnerPostSerializer


    # def get_queryset(self):
    #     owner_id = self.kwargs['owner_id']
    #     pagination_class = PageNumberPagination
    #     pagination_class.page_size = 10
    #     return Post.objects.filter(owner=owner_id)
    def get_queryset(self):
        owner_id = self.kwargs['owner_id']
        queryset = Post.objects.filter(owner=owner_id)
        return queryset 

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        # Check if the 'is_available' field is present in the request data
        if 'is_available' in request.data:
            # Deactivate the post if 'is_available' is set to False
            if not request.data['is_available']:
                instance.is_available = False
                instance.save()
                return Response({'detail': 'Post deactivated successfully.'}, status=status.HTTP_200_OK)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)




class PostUpdate(RetrieveUpdateAPIView):
    queryset = Post.objects.filter(is_available=True)   
    serializer_class = OwnerPostSerializer 



class PostList(ListAPIView):
    queryset = Post.objects.filter(is_available=True)
    filter_backends = (SearchFilter,)
    search_fields = [
        "bhk",
        "build_up_area",        
        "calendar_date",
        "city",
        "deposit_amount",
        "description",
        "furnished_type",
        "id",
        "is_available",
        "ownerinfo",
        "ownerinfo_id",
        "property_type",
        "rentprice",
    ]
    serializer_class = OwnerPostSerializer
    