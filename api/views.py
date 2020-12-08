from .consts import *
from rest_framework import viewsets, status
from .models import Message
from .user import CustomUser
from api.serializers.user_serializers import UserCreateSerializer, UserDisplayDetailSerializer, UserDisplaySerializer
from api.serializers.message_serializers import MessageDisplaySerializer, MessageCreateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()

    def get_serializer_class(self):
        if self.action == CREATE:
            return MessageCreateSerializer
        return MessageDisplaySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == REGISTER:
            return UserCreateSerializer
        elif self.action == RETRIEVE:
            return UserDisplayDetailSerializer
        return UserDisplaySerializer

    # use register for creating new instances
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['post'])
    def register(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)

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
