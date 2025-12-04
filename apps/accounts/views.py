from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny   
from rest_framework_simplejwt.views import TokenObtainPairView
# Internal
from .serializers import UserRegisterSerializer,CustomTokenObtainPairSerializer
from .tasks import task_send_email_otp
# External 
from apps.base.utils import make_token_key

class RegisterView(APIView): 
    serializer_class = UserRegisterSerializer 
    permission_classes = [AllowAny]
    response_keys = ['access']  # Response Fileds 
    access_keys = ['id','email','role']             # Fields to add to access token 

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
