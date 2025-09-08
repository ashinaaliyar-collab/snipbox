import jwt

from datetime import datetime, timedelta, timezone

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from usermanagement.models import UserProfile
from usermanagement.serializers import UserProfileSerializer
from usermanagement.mixins import StandardResponseMixin


class UserProfileCreateView(StandardResponseMixin,generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        password = request.data.get('password')
        try:
            profile = UserProfile.objects.get(mobile_number=mobile_number)
            user = profile.user
        except UserProfile.DoesNotExist:
            return Response({'error': 'Invalid mobile number or password.'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=user.username, password=password)
        if user is not None:
            access_payload = {
                'user_id': user.id,
                'username': user.username,
                'type': 'access',
                'exp': datetime.now(timezone.utc) + timedelta(minutes=160),
            }
            refresh_payload = {
                'user_id': user.id,
                'username': user.username,
                'type': 'refresh',
                'exp': datetime.now(timezone.utc) + timedelta(days=7),
            }
            access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
            refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
            response = Response({'message': 'Login successful'})
            response.set_cookie('access_token', access_token, httponly=True, samesite='Lax')
            response.set_cookie('refresh_token', refresh_token, httponly=True, samesite='Lax')
            return response
        else:
            return Response({'error': 'Invalid mobile number or password.'}, status=status.HTTP_401_UNAUTHORIZED)

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token missing.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != 'refresh':
                return Response({'error': 'Invalid token type.'}, status=status.HTTP_401_UNAUTHORIZED)
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return Response({'error': 'Invalid or expired refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)

        access_payload = {
            'user_id': user.id,
            'username': user.username,
            'type': 'access',
            'exp': datetime.now(timezone.utc) + timedelta(minutes=15),
        }
        refresh_payload = {
            'user_id': user.id,
            'username': user.username,
            'type': 'refresh',
            'exp': datetime.now(timezone.utc) + timedelta(days=7),
        }
        access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
        new_refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
        response = Response({'message': 'Tokens refreshed'})
        response.set_cookie('access_token', access_token, httponly=True, samesite='Lax')
        response.set_cookie('refresh_token', new_refresh_token, httponly=True, samesite='Lax')
        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        response = Response({'message': 'Logged out successfully'})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response