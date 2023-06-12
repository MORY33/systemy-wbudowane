from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework import permissions, status
from .serializers import UserSerializer
import sys

sys.path.append("..")
from JWT.JWT import create_jwt_pair_for_user, delete_token

class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.create_user(username=username, password=password)
                auth.login(request, user)
                token = create_jwt_pair_for_user(user)
                return Response({'success': 'User created successfully.', 'token': token},
                                status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                token = create_jwt_pair_for_user(user)
                return Response({'success': 'Logged in successfully.', 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def logout(self, request):
        print(request.user)
        if request.user.is_authenticated:
            delete_token(request.user)
        auth.logout(request)

        return Response({'success': 'Logged out successfully.'}, status=status.HTTP_200_OK)
