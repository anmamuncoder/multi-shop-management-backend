# Library
from rest_framework import serializers
from rest_framework.serializers import Serializer,ModelSerializer 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
# Internal 
from .models import User
from .tasks import task_send_email_otp

class UserRegisterSerializer(ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email','password','confirm_password','role')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user 
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value
 
    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.pop("confirm_password")  # that remove before saving

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match." })

        return attrs
    
# --------------------------
# User Login Serializer
# -------------------------- 
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer): 
    def validate(self, attrs):
        data = super().validate(attrs) 
        if not self.user.email_verified:
            task_send_email_otp(self.user.id)
            expire_minutes = getattr(settings, "OTP_EXPIRE_MINUTES", 5)
            data['otp'] = f"Otp sent to your email! Please verify your email within {expire_minutes} minutes." 
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role
        token['user_id'] = user.id
        token['email_verified'] = user.email_verified
        return token


# -------------------------- 
# User Profile
# -------------------------- 
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','role','created_at','updated_at')
        read_only_fields  = ('role','created_at','updated_at')

# -------------------------- 
# Re-Send OTP Request
# -------------------------- 
class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, attrs):
        request = self.context['request']
        user = request.user
         
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
 
        if attrs['email'] != user.email:
            raise serializers.ValidationError("Email does not match the authenticated user.")

        return attrs
    
# ---------------------------------
# OTP Verification 
# ---------------------------------
class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
         
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
 
        if attrs['email'] != user.email:
            raise serializers.ValidationError("Email does not match the authenticated user.")
        
        if attrs['otp'] != str(user.email_otp):
            raise serializers.ValidationError("Invalid Otp.")
     
        if not user.email_otp_created_at:
            raise serializers.ValidationError("OTP timestamp missing. Request a new OTP.")
         
        expire_minutes = getattr(settings, "OTP_EXPIRE_MINUTES", 5)

        now = timezone.now()
        otp_age = now - user.email_otp_created_at

        if otp_age > timedelta(minutes=expire_minutes):
            raise serializers.ValidationError("OTP expired. Please request a new one.")

        return attrs
    
