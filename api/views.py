from .consts import *
from rest_framework import viewsets
from .models import Message
from .user import CustomUser
from api.serializers.user_serializers import UserCreateSerializer, UserDisplaySerializer
from api.serializers.message_serializers import MessageDisplaySerializer, MessageCreateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()

    def get_serializer_class(self):
        if self.action == CREATE:
            return MessageCreateSerializer
        return MessageDisplaySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == CREATE:
            return UserCreateSerializer
        return UserDisplaySerializer

    @action(detail=True)
    def get_messages(self, request, pk=None):
        """
        Get all messages for a specific user
        :return: array of messages
        """
        user = self.get_object()

        messages_queryset = Message.objects.filter(sender__username=user.username)
        messages = MessageDisplaySerializer(messages_queryset, many=True)

        return Response(messages.data)
