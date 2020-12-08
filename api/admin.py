from django.contrib import admin
from .models import Message
from .user import CustomUser

# Register your models here.

admin.site.register(Message)
admin.site.register(CustomUser)

