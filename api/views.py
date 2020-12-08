from django.shortcuts import render
from rest_framework import viewsets
from .models import Message
from .user import CustomUser
from .serializers import MessageSerializer, UserSerializer

# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer



