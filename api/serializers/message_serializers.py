from rest_framework import serializers
from api.consts import *
from api.models import Message
from api.serializers.user_serializers import UserMessageDisplaySerializer


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ALL_FIELDS


class MessageDisplaySerializer(serializers.ModelSerializer):
    sender = UserMessageDisplaySerializer(many=False)
    receiver = UserMessageDisplaySerializer(many=False)

    class Meta:
        model = Message
        fields = ALL_FIELDS

    creation_data = serializers.SerializerMethodField()

    def get_creation_data(self, obj):
        return obj.creation_data.strftime(DATE_FORMAT)

