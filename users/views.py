from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from users.serializers import UserProfileSerializer, UserSerializer
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

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        return self.request.user.profile
