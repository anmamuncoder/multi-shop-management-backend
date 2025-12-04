from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny   
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
# Internal
from .serializers import UserRegisterSerializer,CustomTokenObtainPairSerializer, UserSerializer
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