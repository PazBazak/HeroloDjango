from rest_framework import serializers
from api.consts import *
from api.models import Message
from api.user import CustomUser


class UserMessageDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (ID_FIELD, USERNAME_FIELD)


class UserDisplaySerializer(serializers.ModelSerializer):
    class MessageUserDisplaySerializer(serializers.ModelSerializer):
        sender = UserMessageDisplaySerializer(many=False)
        receiver = UserMessageDisplaySerializer(many=False)

        class Meta:
            model = Message
            fields = ALL_FIELDS

    messages = MessageUserDisplaySerializer(many=True)

    class Meta:
        model = CustomUser
        fields = [ID_FIELD, USERNAME_FIELD, MESSAGES_FIELD]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [USERNAME_FIELD, PASSWORD_FIELD]