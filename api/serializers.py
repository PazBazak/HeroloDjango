from .models import Message
from rest_framework import serializers
from .consts import *
from .user import CustomUser


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ALL_FIELDS

    creation_data = serializers.SerializerMethodField()

    def get_creation_data(self, obj):
        return obj.creation_data.strftime(DATE_FORMAT)


class UserSerializer(serializers.ModelSerializer):
    # messages = MessageSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = [ID_FIELD, USERNAME_FIELD, MESSAGES_FIELD]


