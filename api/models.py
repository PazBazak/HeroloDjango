from django.db import models
from django.contrib.auth.models import User
from .consts import *
from .user import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='senders')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="receivers")
    message = models.CharField(max_length=MESSAGE_LENGTH)
    subject = models.CharField(max_length=SUBJECT_LENGTH)
    creation_data = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return MESSAGE_DISPLAY.format(self.sender, self.receiver)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Django signal to create a token each time a user model is created.
    """
    if created:
        Token.objects.create(user=instance)


