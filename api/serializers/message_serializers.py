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
        fields = (ID_FIELD, SENDER_FIELD, RECEIVER_FIELD, DATE_FIELD)

    creation_data = serializers.SerializerMethodField()

    def get_creation_data(self, obj):
        """
        Used in order to format the date when displaying!
        """
        return obj.creation_data.strftime(DATE_FORMAT)


class MessageFullDisplaySerializer(serializers.ModelSerializer):
    sender = UserMessageDisplaySerializer(many=False)
    receiver = UserMessageDisplaySerializer(many=False)

    class Meta:
        model = Message
        fields = ALL_FIELDS

    creation_data = serializers.SerializerMethodField()

    def get_creation_data(self, obj):
        """
        Used in order to format the date when displaying!
        """
        return obj.creation_data.strftime(DATE_FORMAT)

