from enum import Enum


class ChatEventName(str, Enum):
    new_message = "new_message"
    delete_message = "delete_message"
    update_message = "update_message"
