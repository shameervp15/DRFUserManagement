from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers
from users.models import UserProfileModel


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = [
            'fullname', 'date_of_birth', 'address', 'geneder', 'mobilenumber'
        ]

class UserSerializer(serializers.ModelSerializer):
    userprofile_serializer = UserProfileSerializer

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfileModel.objects.create(user=user)
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value

class SetNewPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        validate_password(attrs['password'])

        try:
            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            user = User.objects.get(pk=uid)
        except Exception:
            raise serializers.ValidationError({'uid': 'Invalid uid'})

        token = attrs.get('token')
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({'token': 'Invalid or expired token'})

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        print(kwargs)
        user = self.validated_data['user']
        user.set_password(self.validated_data['password'])
        user.save()
        return user