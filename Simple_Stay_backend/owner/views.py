from rest_framework.generics import ListCreateAPIView ,ListAPIView , CreateAPIView ,RetrieveUpdateAPIView
from .models import Post, PropertyImage
from .serializers import OwnerPostSerializer, PropertyImageSerializer,UserProfileUpdateSerializer,CustomUserSerializer
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import F
from rest_framework.permissions import IsAuthenticated
from user.models import CustomUser
from rest_framework.views import APIView
from rest_framework import generics


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = OwnerPostSerializer
    # permission_classes = (IsAuthenticated,)

    
    # def get_queryset(self):
    #     owner_id = self.kwargs['owner_id']
    #     pagination_class = PageNumberPagination   
    #     pagination_class.page_size = 10
    #     return Post.objects.filter(owner=owner_id)
    
    def get_queryset(self):
        owner_id = self.kwargs['owner_id']
        queryset = Post.objects.filter(owner=owner_id,is_blocked_by_admin=False).order_by('-created_at')
        return queryset

    def create(self, request, *args, **kwargs):
        owner_id = self.kwargs['owner_id']
        request.data['owner'] = owner_id
        serializer = OwnerPostSerializer(data=request.data)

        if serializer.is_valid():
            post_instance = serializer.save()

            # Associate PropertyImage with the created Post instance
            form_data = {'post': post_instance.id}
            data = []
            flag = True

            for image in request.FILES.getlist('image'):
                form_data['image'] = image
                serializer1 = PropertyImageSerializer(data=form_data)

                if serializer1.is_valid():
                    serializer1.save(post=post_instance)  # Pass the post_instance to save
                    data.append(serializer1.data)
                else:
                    flag = False

            if flag:
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=[], status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
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


def get_owner_details(owner_id):
    # Retrieve user details based on owner_id
    try:
        user = CustomUser.objects.get(pk=owner_id)
        owner_details = {
            'username': user.username,
            'email': user.email,
            # Add other user details as needed
        }
        return owner_details
    except CustomUser.DoesNotExist:
        return {}



class UserPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OwnerPostSerializer
    queryset = Post.objects.filter(is_available=True)




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



    

class UserDetailsAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)    


class UserProfileUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user