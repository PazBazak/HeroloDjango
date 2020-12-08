from django.db import models
from django.contrib.auth.models import User
from .consts import *

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receivers")
    message = models.CharField(max_length=MESSAGE_LENGTH)
    subject = models.CharField(max_length=SUBJECT_LENGTH)
    creation_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return MESSAGE_DISPLAY.format(self.sender, self.receiver, self.subject)

