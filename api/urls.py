from django.urls import path, include
from rest_framework import routers
from .views import MessageViewSet, UserViewSet

router = routers.DefaultRouter()

router.register('messages', MessageViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
