from email import message
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from users.serializers import (
    UserProfileSerializer, UserSerializer, PasswordResetRequestSerializer,
    SetNewPasswordSerializer
)


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

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        message = "If your account exists, a reset link has been sent to your email."
        try:
            user = User.objects.get(email__iexact=email)
            print("Not exist sending email")
        except User.DoesNotExist:
            return Response({"message": message}, status=status.HTTP_200_OK)

        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        frontend = settings.FRONTEND_DOMAIN.rstrip('/')
        reset_url = f"{frontend}/reset-password?uid={uid}&token={token}"
        subject = "Reset your password"
        text_message = f"Use the link below to reset your password:\n\n{reset_url}\n\nIf you didn't request this, ignore this email."
        html_message = f"<p>Use the link below to reset your password:</p><p><a href='{reset_url}'>{reset_url}</a></p>"
        print("sending email")
        send_mail(subject, text_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)
        print("Sent............")

        return Response({"message": message}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

