from .consts import *
from rest_framework import viewsets, status
from .models import Message
from .user import CustomUser
from api.serializers.user_serializers import UserCreateSerializer, UserDisplaySerializer
from api.serializers.message_serializers import MessageDisplaySerializer, MessageCreateSerializer, \
    MessageFullDisplaySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Q


# region utils

def filter_sender_receiver(username: str):
    """
    Returns the queryset filter for message if the username is in either sender or receiver
    :param username: username
    :return: filter queryset
    """
    return Q(sender__username=username) | Q(receiver__username=username)


def get_user_from_token(token: str):
    """
    :param token: Given token key
    :return: user which attached to that token
    """
    request_token = token
    token = Token.objects.get(key=request_token)

    user = token.user
    return user

# endregion


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()

    def get_serializer_class(self):
        if self.action == CREATE:
            return MessageCreateSerializer
        if self.action == RETRIEVE:
            return MessageFullDisplaySerializer
        return MessageDisplaySerializer

    def destroy(self, request, *args, **kwargs):
        """
        When destroying a record, verifying the logged user is either the sender or receiver in order to do so!
        """
        request_token = request.auth.key
        sender = self.get_object().sender
        receiver = self.get_object().receiver

        users_tokens = Token.objects.filter(user__in=[sender, receiver])

        for token in users_tokens:
            if token.key == request_token:
                instance = self.get_object()
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        """
        When fetching single message, it will return the message only if the logged user is eiter the sender or the
        receiver, and if the receiver fetched the message, it will be changed to read!
        """
        user = get_user_from_token(request.auth.key)
        logged_username = user.username

        instance = self.get_object()
        instance_sender = instance.sender
        instance_receiver = instance.receiver

        # if the logged user is matching either the sender or receiver
        if logged_username == instance_sender.username or logged_username == instance_receiver.username:
            if not instance.is_read:
                if logged_username == instance_receiver.username:
                    instance.is_read = True
                    instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        """
        When writing a new message, the required parameters will be receiver, message, subject
        sender will be taken from the logged user.
        date is auto now.
        is read default is false
        """
        data = request.data
        user = get_user_from_token(request.auth.key)

        # handles QueryDict
        if type(request.data) is not dict:
            request.data._mutable = True

        # adding the sender to the data
        data[SENDER_FIELD] = user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        return UserDisplaySerializer

    # use register for creating new instances
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=[POST])
    def register(self, request, *args, **kwargs):
        """
        Creating a new user, overrides default create
        """
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
        user_token = Token.objects.get(user=user).key

        if request.auth.key != user_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        username = user.username

        messages_queryset = Message.objects.filter(filter_sender_receiver(username))
        messages = MessageFullDisplaySerializer(messages_queryset, many=True)

        return Response(messages.data)

    @action(detail=True)
    def get_unread_messages(self, request, pk=None):
        """
        Get all unread messages for a specific user
        :return: array of messages
        """
        user = self.get_object()
        user_token = Token.objects.get(user=user).key

        if request.auth.key != user_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        username = user.username
        messages_queryset = Message.objects.filter(filter_sender_receiver(username)).filter(is_read=False)
        messages = MessageFullDisplaySerializer(messages_queryset, many=True)

        return Response(messages.data)
