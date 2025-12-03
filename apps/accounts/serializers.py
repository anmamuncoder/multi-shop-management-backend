# Library
from rest_framework import serializers
from rest_framework.serializers import Serializer,ModelSerializer 

# Internal 
from .models import User

class UserRegisterSerializer(ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email','password','confirm_password','role')
        extra_kwargs = {
            'password': {'write_only': True}
        }
         
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
    
