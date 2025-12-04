from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny   
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
# Internal
from .serializers import UserRegisterSerializer,CustomTokenObtainPairSerializer, UserSerializer,ResendOTPSerializer,OTPVerifySerializer
from .tasks import task_send_email_otp
from .models import User
# External 
from apps.base.utils import make_token_key

class RegisterView(APIView): 
    serializer_class = UserRegisterSerializer 
    permission_classes = [AllowAny]
    response_keys = ['access']  # Response Fileds 
    access_keys = ['id','email','role','email_verified']             # Fields to add to access token 

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        access_token, refresh_token = make_token_key(user,self.access_keys) 

        # Prepare response json keys
        response_data = {}
        for key in self.response_keys:
            if key == 'access':
                response_data['access'] = str(access_token)
            elif key == 'refresh':
                response_data['refresh'] = str(refresh_token)
            elif hasattr(user, key):
                response_data[key] = getattr(user, key)

        # Email OTP Send
        task_send_email_otp(user.id)

        response_data['otp'] = "Otp send you mail! Please verify you mail with in 5 minutes"
        return Response(response_data, status=status.HTTP_201_CREATED) 
    
# --------------------------
# User Login View
# --------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# --------------------------
# User Profile View
# --------------------------
class UserView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return self.update_user(request, full_update=True)

    def patch(self, request, *args, **kwargs):
        return self.update_user(request, full_update=False)
    
    def update_user(self, request, full_update=False): 
        user = request.user
        old_email = user.email
        new_email = request.data.get("email")

        # Email Unique Check
        if new_email and new_email != old_email:
            if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                return Response({"email": "This email is already used by another user."},status=status.HTTP_400_BAD_REQUEST)
            
        # Update User
        serializer = UserSerializer(user,data=request.data,partial=not full_update)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Message set
        msg = "Updated successfully."
        if new_email and new_email != old_email:
            user.email_verified = False
            user.save(update_fields=['email_verified'])
            msg = "Your email is not verified! Login again and verify it."

        return Response({"user": serializer.data, "message": msg},status=status.HTTP_200_OK)
    
# --------------------------
# User Resend OTP
# --------------------------
class SendOTPView(APIView):
    serializer_class = ResendOTPSerializer  
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({"detail": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
 
        # Email OTP Send
        task_send_email_otp(user.id)
        expire_minutes = getattr(settings, "OTP_EXPIRE_MINUTES", 5)

        return Response({"detail": f"OTP sent successfully! Validation within {expire_minutes} minute"}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    serializer_class = OTPVerifySerializer 

    def post(self, request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user.email_verified = True
        user.email_otp = None
        user.email_otp_created_at = None

        user.save(update_fields=['email_verified','email_otp','email_otp_created_at'])
        
        access_token, refresh_token = make_token_key(user,['id','email','email_verified']) 

        return Response({"access": str(access_token), "refresh": str(refresh_token)}, status=status.HTTP_200_OK)
