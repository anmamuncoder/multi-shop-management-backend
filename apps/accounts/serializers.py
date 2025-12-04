# Library
from rest_framework import serializers
from rest_framework.serializers import Serializer,ModelSerializer 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
            raise serializers.ValidationError({"otp": "Otp sent to your email! Please verify your email within 5 minutes."} )
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

