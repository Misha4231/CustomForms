from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User

class CustomRegsitrationSerializer(RegisterSerializer):
    email = serializers.EmailField(required = True)
    
    def validate_email(self, email):
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        
        return email
    
    def save(self, request):
        return super().save(request)