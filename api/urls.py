from django.urls import path, include
from rest_framework import routers
from .views import MessageViewSet, UserViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()

router.register('messages', MessageViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token, name='login')
]
