from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import CustomUser
from .serializers import UserRegisterSerializer,myTokenObtainPairSerializer,UserGoogleSerializer
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    GenericAPIView,
)
from django.core.mail import send_mail



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer



class UserRegister(CreateAPIView):
    def get_serializer_class(self):
        return UserRegisterSerializer
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.user_type = "user"
            user.set_password(password)
            user.save()
            
            current_site = get_current_site(request)
            mail_subject = 'please activate your account'
            message = render_to_string('user/account_verification.html',
            {
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                'site' : current_site

            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            return Response({ 'msg' : 'a verifiaction link send to your email address', 'data' : serializer.data,'status':status.HTTP_201_CREATED})
        else:
            print('Serializer errors are:', serializer.errors)
            return Response({'status': 'error', 'msg': serializer.errors})


                            

@api_view(['GET'])
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        message = "Congrats, You have been succesfully registered"
        redirect_url =  'http://localhost:5173/login/' + '?message=' + message + '?token' + token
    else:
        message = 'Invalid activation link'
        redirect_url = 'http://localhost:5173/signup/' + '?message=' + message
    
    
    return HttpResponseRedirect(redirect_url)


class GoogleUser(APIView):

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        if CustomUser.objects.filter(email=email).exists():
            try:
                user = get_object_or_404(CustomUser, email__iexact=email)
            except:
                user = None
            if user is not None:
                token=create_jwt_pair_tokens(user)
                response_data = {
                    'status': 'success',
                    'msg': 'Login successfully',
                    'token': token,
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'error', 'msg': 'User not found'})
        else:
            serializer = UserGoogleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.user_type = "user"
                user.is_active = True
                user.is_google = True
                user.set_password(password)
                user.save()
            user = authenticate( email=email, password=password)
            if user is not None:
                token=create_jwt_pair_tokens(user)
                response_data = {
                    'status': 'success',
                    'msg': 'Registration Successfully',
                    'token': token,
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'error', 'msg': serializer.errors})
    


def create_jwt_pair_tokens(user):

    refresh = RefreshToken.for_user(user)

    refresh['email'] = user.email
    refresh['user_type'] = user.user_type
    refresh['is_active'] = user.is_active
    refresh['is_admin'] = user.is_superuser
    refresh['is_google'] = user.is_google

   
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    
    return {
        "access": access_token,
        "refresh": refresh_token,
    }