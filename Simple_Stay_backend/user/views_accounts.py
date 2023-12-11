import requests  # Make sure to import the 'requests' module
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
from datetime import datetime, timedelta




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer


class UserRegister(CreateAPIView):
    def get_serializer_class(self):
        return UserRegisterSerializer

    def post(self, request):
        try:
            print('Request Data:', request.data)
        # Your existing code here
        except Exception as e:
            print(f"Error during registration: {str(e)}")

            return Response({'status': 'error', 'msg': 'An error occurred during registration.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if an inactive user with the same email already exists
        existing_user = CustomUser.objects.filter(email=email).first()
        print(existing_user,'fwvdscassd')
        if existing_user:
            
            if not existing_user.is_verify:
                # User is inactive and has not clicked the link, resend the verification email
                current_site = get_current_site(request)
                mail_subject = 'Please activate your account'
                message = render_to_string('user/account_verification.html', {
                    'user': existing_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(existing_user.pk)),
                    'token': default_token_generator.make_token(existing_user),
                })

                # Ensure email is valid before sending
                if email and '@' in email:
                    send_mail(
                        mail_subject,
                        message,
                        'simplestayinfo@gmail.com',  # Replace with your actual "from" email address
                        [email],
                        fail_silently=False,
                        html_message=message,  # Set the HTML message
                    )

                    return Response({'status': 'success', 'msg': 'Verification email resent.'}, status=status.HTTP_200_OK)

                else:
                    return Response({'status': 'error', 'msg': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)

            # User is active, cannot register
            return Response({'status': 'error', 'msg': 'User is already active. Cannot register.'}, status=status.HTTP_400_BAD_REQUEST)

        # Continue with the registration process
        serializer = UserRegisterSerializer(data=request.data)
        print(serializer,'DSCDASCFDASCDSA')
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.user_type = "user"
            user.set_password(password)
            user.save()
            print(user,'FECADFCESAFC')

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('user/account_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            # Ensure email is valid before sending
            if email and '@' in email:
                send_mail(
                    mail_subject,
                    message,
                    'simplestayinfo@gmail.com',  # Replace with your actual "from" email address
                    [email],
                    fail_silently=False,
                    html_message=message,  # Set the HTML message
                )

                return Response({
                    'msg': 'A verification link has been sent to your email address',
                    'data': serializer.data,
                    'status': status.HTTP_201_CREATED
                })
            else:
                return Response({'status': 'error', 'msg': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            print('Serializer errors are:', serializer.errors)
            return Response({'status': 'error', 'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



                            

# @api_view(['GET'])
# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = CustomUser._default_manager.get(pk=uid)
#     except (TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
#         user = None
    
#     if user is not None and default_token_generator.check_token(user,token):
#         user.is_verify = True
#         user.is_active =True
#         user.save()
#         message = "Congrats, You have been succesfully registered"
#         redirect_url =  'http://localhost:5173/login/' + '?message=' + message + '?token' + token
#     else:
#         message = 'Invalid activation link'
#         redirect_url = 'http://localhost:5173/signup/' + '?message=' + message
    
    
#     return HttpResponseRedirect(redirect_url)


@api_view(['GET'])
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Check if the verification link has expired (e.g., 5 minutes limit)
        link_creation_time = user.date_joined  # Adjust this based on your user model field
        expiration_time = link_creation_time + timedelta(minutes=5)

        if datetime.now() <= expiration_time:
            user.is_verify = True
            user.is_active = True
            user.save()
            message = "Congrats, You have been successfully registered"
            redirect_url = 'http://localhost:5173/login/' + '?message=' + message + '?token' + token
        else:
            message = 'Verification link has expired. Please request a new one.'
            redirect_url = 'http://localhost:5173/signup/' + '?message=' + message
    else:
        message = 'Invalid activation link'
        redirect_url = 'http://localhost:5173/signup/' + '?message=' + message

    return HttpResponseRedirect(redirect_url)



class GoogleUser(APIView):
    # permission_classes = [AllowAny]


    def post(self, request):
        try:
            print('Request Data:', request.data)
        # Your existing code here
        except Exception as e:
            print(f"Error during registration: {str(e)}")

            return Response({'status': 'error', 'msg': 'An error occurred during registration.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        access_token = request.data.get('access_token')
        google_token_info = self.validate_google_token(access_token)

        if google_token_info is None:
            return Response({'status': 'error', 'msg': 'Invalid Google access token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        email = google_token_info.get('email')

        # Check if the user with the provided email already exists
        existing_user = CustomUser.objects.filter(email=email).first()

        if existing_user:
            # User already exists, perform login
            token = create_jwt_pair_tokens(existing_user)
            response_data = {
                'status': 'success',
                'msg': 'Login successfully',
                'token': token,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # User does not exist, proceed with Google signup
            user = CustomUser(email=email, user_type="user", is_active=True, is_google=True)
            user.save()

            # Perform login after successful signup
            token = create_jwt_pair_tokens(user)
            response_data = {
                'status': 'success',
                'msg': 'Registration and Login Successfully',
                'token': token,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
    
    def validate_google_token(self, access_token):
        google_token_info_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
        params = {'access_token': access_token}
        response = requests.get(google_token_info_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return None







def create_jwt_pair_tokens(user):

    refresh = RefreshToken.for_user(user)

    refresh['email'] = user.email
    refresh['user_type'] = user.user_type
    refresh['is_active'] = user.is_active
    refresh['is_admin'] = user.is_admin
    refresh['is_google'] = user.is_google

   
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    
    return {
        "access": access_token,
        "refresh": refresh_token,
    }