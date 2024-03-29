# views.py
from django.utils import timezone
from rest_framework import viewsets
from .models import PremiumPackages,PremiumOwner
from .serializer import PremiumPackagesSerializer, PremiumOwnerSerializer
from django.conf import settings
from rest_framework.views import APIView
import stripe
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser
from rest_framework.generics import RetrieveAPIView, ListAPIView
from decouple import config
from .tasks import send_premium_created_email
from datetime import timedelta

class PremiumPackagesViewSet(viewsets.ModelViewSet):
    queryset = PremiumPackages.objects.all()
    serializer_class = PremiumPackagesSerializer


class PremiumPackagesViewOnly(viewsets.ReadOnlyModelViewSet):
    queryset = PremiumPackages.objects.all()
    serializer_class = PremiumPackagesSerializer



stripe.api_key = config('STRIPE_SECRET_KEY')

class StripePayment(APIView):
    def post(self, request):
        try:
            data = request.data
            # print(data, "fdasssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")  # This will print the data received in the request
            userId = data.get('userId')
            planId = data.get('planId')
            # You can use the received data to customize the Stripe session creation
            success_url = f'http://localhost:5173/owner/payment/success/?userId={userId}&planId={planId}'
            cancel_url = 'http://localhost:5173/owner/payment/canceled=true'
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': data.get('currency', 'INR'),
                        'product_data': {
                            'name': data.get('name', 'sample'),
                        },
                        'unit_amount': data.get('unit_amount', 100 * 100),
                    },
                    'quantity': data.get('quantity', 1),
                }],
                mode=data.get('mode', 'payment'),
                success_url=success_url,
                cancel_url=cancel_url,
            )

            

            return Response({"message": session}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class PaymentSuccess(APIView):
#     def post(self, request):
#         userid = self.request.data.get('userId')
#         planid = self.request.data.get('planId')
#         print(planid, userid)
#         if not userid or not planid:
#             return Response({"error": "userId and planId are required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             package = PremiumPackages.objects.get(pk=planid)
#         except PremiumPackages.DoesNotExist:
#             return Response({"error": "Invalid planId"}, status=status.HTTP_400_BAD_REQUEST)

#         premium_customer = PremiumOwner.objects.create(user_id=userid, package=package)
        
#         print(premium_customer.user.email)
#         test_task.delay()

#         send_premium_created_email.delay(premium_customer.user.email)

#         return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)


class PaymentSuccess(APIView):
    def post(self, request):
        userid = request.data.get('userId')
        planid = request.data.get('planId')

        if not userid or not planid:
            return Response({"error": "userId and planId are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            package = PremiumPackages.objects.get(pk=planid)
        except PremiumPackages.DoesNotExist:
            return Response({"error": "Invalid planId"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the current timestamp
        current_time = timezone.now()

        # Check if the user has an active premium package
        try:
            existing_premium = PremiumOwner.objects.get(user_id=userid, is_active=True)
        except PremiumOwner.DoesNotExist:
            existing_premium = None

        if existing_premium:
            # If the user already has an active premium package,
            # update the expiration date and start date of the existing package
            existing_premium.start_date = current_time
            existing_premium.exp_date = current_time + timedelta(days=package.validity)
            existing_premium.save()
            # Send email notification
            send_premium_created_email.delay(existing_premium.user.email)
            return Response({"message": "Your premium package has been extended"}, status=status.HTTP_200_OK)
        else:
            # Check if the user had a previous premium package that has expired
            try:
                expired_premium = PremiumOwner.objects.get(user_id=userid, is_active=False)
                
                # If the expiration date has passed, deactivate the premium package
                if expired_premium.exp_date < current_time:
                    expired_premium.is_active = False
                    expired_premium.user.is_premium = False
                    expired_premium.save()

            except PremiumOwner.DoesNotExist:
                expired_premium = None

            if expired_premium:
                print(expired_premium,"DSADSADAS")
                print(expired_premium.user.is_premium,"FFFFFFFFFFFFFFFFFF")
                # Reactivate the expired premium package
                expired_premium.is_active = True
                expired_premium.user.is_premium = True
                expired_premium.start_date = current_time
                expired_premium.exp_date = current_time + timedelta(days=package.validity)
                expired_premium.save()
                expired_premium.user.save()

                # Send email notification
                send_premium_created_email.delay(expired_premium.user.email)
                return Response({"message": "Your expired premium package has been reactivated"}, status=status.HTTP_200_OK)

            # Create a new premium package entry for the user
            new_premium = PremiumOwner.objects.create(
                user_id=userid,
                package=package,
                start_date=current_time,
                exp_date=current_time + timedelta(days=package.validity)
            )

            # Dispatch Celery tasks, send email, etc.
            send_premium_created_email.delay(new_premium.user.email)

            return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)


class PremiumSalesReport(ListAPIView):
    queryset = PremiumOwner.objects.all()
    serializer_class = PremiumOwnerSerializer


class CheckPremiumStatus(APIView):
    def get(self, request, user_id, format=None):
        try:
            # Check if the user is already a premium user
            is_premium = PremiumOwner.objects.filter(user_id=user_id, is_active=True).exists()

            return Response({"isPremium": is_premium}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)