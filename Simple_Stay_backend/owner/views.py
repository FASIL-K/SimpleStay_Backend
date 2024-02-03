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
from premium.models import PremiumOwner
from premium.serializer import PremiumOwnerSerializer

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
        print(request.data,'date')
        
        serializer = OwnerPostSerializer(data=request.data, context={'request': request})

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
        "amenities"
    ]
    serializer_class = OwnerPostSerializer



    

# class UserDetailsAPIView(generics.RetrieveAPIView):
#     serializer_class = CustomUserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)    

class UserDetailsAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user_instance = self.get_object()
        user_serializer = self.get_serializer(user_instance)

        try:
            premium_owner_instance = PremiumOwner.objects.get(user=user_instance)
            premium_owner_serializer = PremiumOwnerSerializer(premium_owner_instance)

            # Combine user and premium owner details
            combined_data = {
                "user_details": user_serializer.data,
                "premium_owner_details": premium_owner_serializer.data,
            }

            return Response(combined_data)
        except PremiumOwner.DoesNotExist:
            # If the user is not a premium owner, return only user details
            return Response(user_serializer.data)

class UserProfileUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
from math import radians, sin, cos, sqrt, atan2
import requests
from django.http import JsonResponse

def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate distance
    distance = R * c

    return round(distance, 2)

def categorize_place_type(place_type):
    # Custom function to categorize place types
    if 'school' in place_type:
        return 'school'
    elif 'pharmacy' in place_type:
        return 'pharmacy'
    elif 'restaurant' in place_type or 'food' in place_type:
        return 'restaurant'
    elif 'hospital' in place_type:
        return 'hospital'
    elif 'police_station' in place_type:
        return 'police'
    elif 'movie_theater' in place_type:
        return 'movie_theater'  
    elif 'bakery' in place_type:
        return 'Bakery'
    else:
        return 'other'

def fetch_nearby_places(request):
    # Extract the parameters from the frontend request or pass them as needed
    location = request.GET.get('location','11.248881548999604,75.83958249038224')
    radius = request.GET.get('radius', '5000')
    
    # Specify the priority categories
    priority_categories = ['school','pharmacy','Shopping mall','bakery', 'restaurant','Grocery store','Hypermarket','hospital', 'police', 'Movie theater', ]
    
    # Maximum number of places to display for each category
    max_places_per_category = 1

    api_key = 'AIzaSyDH8DKerF4jGQdGzE77cAN3or2rU7CiBJw'
    places_data = []

    for category in priority_categories:
        # Replace spaces in category with underscores
        formatted_category = category.replace(' ', '_')
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={formatted_category}&key={api_key}'
        
        try:
            response = requests.get(url)
            data = response.json()

            if 'results' in data:
                places = data['results'][:max_places_per_category]
                for place in places:
    # Skip places with the category 'locality'
                    if 'locality' in place['types']:
                        continue

                    # Calculate distance and add it to the place data
                    place['distance'] = haversine_distance(location.split(',')[0], location.split(',')[1], place['geometry']['location']['lat'], place['geometry']['location']['lng'])
                    # Categorize place type
                    place['category'] = categorize_place_type(place['types'][0])

                    # Extract only necessary information for the response
                    place_data = {
                        'name': place['name'],
                        'category': place['category'],
                        'type': place['types'][0],  # Include the 'type' key
                        'distance': place['distance'],
                        'geometry': place['geometry']['location']
                    }
                    places_data.append(place_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Sort the places first by category priority, then by distance
    sorted_places_data = sorted(places_data, key=lambda x: (priority_categories.index(x['category']) if x['category'] in priority_categories else float('inf'), x['distance']))

    return JsonResponse({'results': sorted_places_data})



