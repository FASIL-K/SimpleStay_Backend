from user.models import CustomUser
from .serializers import OwnerSerializer,  UserGoogleSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveUpdateDestroyAPIView,CreateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail


from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from user.views_accounts import *


class OwnerRegister(CreateAPIView):
    def get_serializer_class(self):
        return OwnerSerializer

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
        serializer = OwnerSerializer(data=request.data)
        print(serializer,'DSCDASCFDASCDSA')
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.user_type = "owner"
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
        

class GoogleOwner(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')


        if not CustomUser.objects.filter(email=email).exists():
            serializer = UserGoogleSerializer(data = request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.user_type = 'owner'
                user.is_active = True
                user.is_google = True
                user.set_password(password)
                user.save()

        
        user = authenticate(request, email=email, password=password)
        if user is not None:

            token=create_jwt_pair_tokens(user)

            response_data = {
                'status' : 'success',
                'token' : token,
                'msg' : 'Account has been registered succesfully',
            }

            return Response (data=response_data, status = status.HTTP_201_CREATED)
        else:
            return Response (data={'status' : '400' , 'msg' : 'Login failed'})
        


def create_jwt_pair_tokens(user):
    
    refresh = RefreshToken.for_user(user)

    refresh['email'] = user.email
    refresh['id'] = user.id
    refresh['name'] = user.name
    refresh['user_type'] = user.user_type
    refresh['is_active'] = user.is_active

   
    access_token = str(refresh.access_token) # type: ignore
    refresh_token = str(refresh)

    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


class OwnerLogout(APIView):
    permission_classes =(IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'detail': 'Logout successful.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        