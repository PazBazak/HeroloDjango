

# region utils


DATE_FORMAT = "%a %B %d, %Y"


# endregion


# region models


MESSAGE_LENGTH = 512
SUBJECT_LENGTH = 128

MESSAGE_DISPLAY = "{} to {}"


# endregion


# region user


NO_VALUE_ERROR_MESSAGE = 'The {} must be set'


# endregion


# region serializers


ALL_FIELDS = '__all__'
ID_FIELD = 'id'
USERNAME_FIELD = 'username'
MESSAGES_FIELD = 'messages'
PASSWORD_FIELD = 'password'
SENDER_FIELD = 'sender'
RECEIVER_FIELD = 'receiver'
SUBJECT_FIELD = 'subject'
DATE_FIELD = 'creation_data'
IS_READ_FIELD = 'is_read'

# endregion


# region views


CREATE = 'create'
REGISTER = 'register'
RETRIEVE = 'retrieve'
LIST = 'list'
POST = 'post'


# endregion
