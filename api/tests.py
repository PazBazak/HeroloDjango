from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Message, CustomUser
from .consts import *
from api.serializers.message_serializers import MessageCreateSerializer, MessageFullDisplaySerializer

# region model testing


class MessageModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.sender = CustomUser.objects.create(username="SENDER")
        cls.receiver = CustomUser.objects.create(username="RECEIVER")

        cls.message = Message.objects.create(sender=cls.sender,
                                             receiver=cls.receiver,
                                             message='TEST MESSAGE',
                                             subject='TEST SUBJECT')

    def test_message_content(self):
        self.assertEqual('TEST MESSAGE', self.message.message)

    def test_subject(self):
        self.assertEqual('TEST SUBJECT', self.message.subject)

    def test_sender(self):
        self.assertEqual(self.sender.pk, self.message.sender.pk)

    def test_receiver(self):
        self.assertEqual(self.receiver.pk, self.message.receiver.pk)

    def test_is_read(self):
        self.assertEqual(False, self.message.is_read)

    def test_str(self):
        self.assertEqual("SENDER to RECEIVER", str(self.message))


# endregion


# region serializer testing


class MessageSerializersTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.sender = CustomUser.objects.create(username="SENDER")
        cls.receiver = CustomUser.objects.create(username="RECEIVER")

        cls.message = Message.objects.create(sender=cls.sender,
                                             receiver=cls.receiver,
                                             message='TEST MESSAGE',
                                             subject='TEST SUBJECT')

        cls.message_data = {
            SENDER_FIELD: str(cls.sender.pk),
            RECEIVER_FIELD: str(cls.receiver.pk),
            MESSAGES_FIELD: 'TEST MESSAGE',
            SUBJECT_FIELD: 'TEST SUBJECT',
            IS_READ_FIELD: False
        }

    def test_create_serializer(self):
        create_serializer = MessageCreateSerializer(data=self.message_data)

        self.assertTrue(create_serializer.is_valid())

    def test_display_serializer(self):
        display_serializer = MessageFullDisplaySerializer(self.message)

        message_data = display_serializer.data

        self.assertEqual('TEST MESSAGE', message_data[MESSAGES_FIELD])
        self.assertEqual('TEST SUBJECT', message_data[SUBJECT_FIELD])
        self.assertEqual(False, message_data[IS_READ_FIELD])
        self.assertEqual('SENDER', message_data[SENDER_FIELD][USERNAME_FIELD])
        self.assertEqual('RECEIVER', message_data[RECEIVER_FIELD][USERNAME_FIELD])


# endregion
