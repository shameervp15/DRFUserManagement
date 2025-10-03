from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LogOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data['refresh']
        RefreshToken(refresh_token).blacklist()
        return Response({'message': 'Logged out successfully!'}, status=status.HTTP_200_OK)
