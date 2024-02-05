from urllib import response
from rest_framework.generics import RetrieveDestroyAPIView,ListAPIView,UpdateAPIView,ListCreateAPIView
from user.models import CustomUser
from user.serializers import UserInfoSerializer
from rest_framework import status,viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from owner.serializers import OwnerPostSerializer
from owner.models import Post
from rest_framework.decorators import action





class SearchPostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = OwnerPostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['locality','city', 'house_name']  



# class FilterPostList(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = OwnerPostSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_fields = ['locality', 'city', 'house_name']
#     ordering_fields = ['monthly_rent', 'created_at']  # Add more fields as needed

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         # Apply filtering conditions based on query parameters (e.g., bhk_type, property_type)
#         bhk_type = self.request.query_params.get('bhk_type', None)
#         if bhk_type:
#             queryset = queryset.filter(bhk_type=bhk_type)

#         property_type = self.request.query_params.get('property_type', None)
#         if property_type:
#             queryset = queryset.filter(property_type=property_type)
            
#         furnished_type = self.request.query_params.get('furnished_type', None)

#         if furnished_type:
#             queryset = queryset.filter(furnished_type=furnished_type)
#         # Add more filtering conditions as needed


#         min_monthly_rent = self.request.query_params.get('min_monthly_rent', None)
#         max_monthly_rent = self.request.query_params.get('max_monthly_rent', None)

#         if min_monthly_rent is not None:
#             queryset = queryset.filter(monthly_rent__gte=min_monthly_rent)

#         if max_monthly_rent is not None:
#             queryset = queryset.filter(monthly_rent__lte=max_monthly_rent)

#         return queryset


class FilterPostList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = OwnerPostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['locality', 'city', 'house_name']
    ordering_fields = ['monthly_rent', 'created_at']  # Add more fields as needed

    def get_queryset(self):
        queryset = super().get_queryset()   

        # Apply filtering conditions based on query parameters (e.g., bhk_type, property_type)
        bhk_types_param = self.request.query_params.get('bhk_type', '')
        bhk_types = [bhk.strip() for bhk in bhk_types_param.split(',') if bhk.strip()]

        if bhk_types:
            queryset = queryset.filter(bhk_type__in=bhk_types)

        property_types_param = self.request.query_params.get('property_type', '')
        property_types = [property_type.strip() for property_type in property_types_param.split(',') if property_type.strip()]

        if property_types:
            queryset = queryset.filter(property_type__in=property_types)

        furnished_types_param = self.request.query_params.get('furnished_type', '')
        furnished_types = [furnished_type.strip() for furnished_type in furnished_types_param.split(',') if furnished_type.strip()]

        if furnished_types:
            queryset = queryset.filter(furnished_type__in=furnished_types)

        min_monthly_rent = self.request.query_params.get('min_monthly_rent', None)
        max_monthly_rent = self.request.query_params.get('max_monthly_rent', None)

        if min_monthly_rent is not None:
            queryset = queryset.filter(monthly_rent__gte=min_monthly_rent)

        if max_monthly_rent is not None:
            queryset = queryset.filter(monthly_rent__lte=max_monthly_rent)

        return queryset
