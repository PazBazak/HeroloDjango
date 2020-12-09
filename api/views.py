from .consts import *
from rest_framework import viewsets, status
from .models import Message
from .user import CustomUser
from api.serializers.user_serializers import UserCreateSerializer, UserDisplayDetailSerializer, UserDisplaySerializer
from api.serializers.message_serializers import MessageDisplaySerializer, MessageCreateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token


# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()

    def get_serializer_class(self):
        if self.action == CREATE:
            return MessageCreateSerializer
        return MessageDisplaySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.action == REGISTER:
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]

        return super(UserViewSet, self).get_permissions()

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        returned_data = serializer.data

        # reference to the created user
        user = CustomUser.objects.get(username=serializer.data[USERNAME_FIELD])

        # getting the user token
        token = Token.objects.get(user=user)

        returned_data['token'] = token.key

        return Response(returned_data, status=status.HTTP_201_CREATED, headers=headers)

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
