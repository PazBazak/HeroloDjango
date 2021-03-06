from rest_framework import serializers
from api.consts import *
from api.user import CustomUser


class UserMessageDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (ID_FIELD, USERNAME_FIELD)


class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ID_FIELD, USERNAME_FIELD]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [USERNAME_FIELD, PASSWORD_FIELD]

    def create(self, validated_data):
        user = CustomUser.objects.create(username=validated_data[USERNAME_FIELD])
        user.set_password(validated_data[PASSWORD_FIELD])
        user.save()

        return user

