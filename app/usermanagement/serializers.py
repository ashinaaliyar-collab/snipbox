import uuid
from django.contrib.auth.models import User

from rest_framework import serializers

from usermanagement.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = ('mobile_number', 'full_name', 'password')
        extra_kwargs = {
            'mobile_number': {'unique': True},
        }

    def validate_mobile_number(self, value):
        if UserProfile.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number must be unique.")
        return value

    def validate_full_name(self, value):
        if not value:
            raise serializers.ValidationError("Full name is required.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        full_name = validated_data.get('full_name', '')
        # Generate a unique username
        base_username = ''.join(full_name.split()).lower() or 'user'
        unique_suffix = uuid.uuid4().hex[:6]
        username = f"{base_username}_{unique_suffix}"
        while User.objects.filter(username=username).exists():
            unique_suffix = uuid.uuid4().hex[:6]
            username = f"{base_username}_{unique_suffix}"
        user = User.objects.create_user(username=username, password=password)
        validated_data['user'] = user
        return super().create(validated_data)