from rest_framework import serializers
from users.models import UserProfileModel
from django.contrib.auth.models import User


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
        userprofile = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfileModel.objects.create(user=user, **userprofile)
        return user
