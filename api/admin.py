from django.contrib import admin
from .models import Message
from .user import CustomUser

# Register your models here.


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "creation_data", "message", "id")


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


