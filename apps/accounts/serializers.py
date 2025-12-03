# Library
from rest_framework import serializers
from rest_framework.serializers import Serializer,ModelSerializer 

# Internal 
from .models import User

class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password','role')
    def validate(self, attrs):
        email = attrs.get("email")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already taken."})

        return attrs