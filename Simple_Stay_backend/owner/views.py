from rest_framework.generics import ListCreateAPIView ,ListAPIView , CreateAPIView ,RetrieveUpdateAPIView
from .models import Post
from .serializers import OwnerPostSerializer
from rest_framework.filters import SearchFilter




class PostCreateView(CreateAPIView):
    queryset = Post.objects.filter(is_available=True)
    serializer_class = OwnerPostSerializer
    



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
