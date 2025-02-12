import time

from redis.client import PubSub
from threading import Thread

from agents.constants import USER_NAME, PROJECT_MANAGER_AGENT_NAME
from agents.core.dto.message_dto import MessageDTO
from agents.db.service.message_service import MessageService
from agents.utils.jsons import decode_message
from agents.core.actuator.redis_comm import get_redis_conn, publish_message

def listen(pubsub: PubSub, print_all: bool = True):

    print("\nService started")
    message_service = MessageService()

    for message_str in pubsub.listen():
        msg_dict = decode_message(message_str)

        if msg_dict:
            message = MessageDTO(**msg_dict)
            message_service.save(msg_dict)
            if print_all and message.sender != USER_NAME:
                print(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} {message.sender}: @{message.recipient}\n {message.message}\n")

def start_user_interaction():

    redis_instance, pubsub = get_redis_conn()
    Thread(target=listen, args=(pubsub,)).start()

    first = True
    while True:

        if first:
            user_message = input(f"Send a message: ")
            first = False
        else:
            user_message = input()

        if user_message.lower() == "exit":
            print("Exiting...")
            break

        message = MessageDTO(sender=USER_NAME, recipient=PROJECT_MANAGER_AGENT_NAME, message=user_message)
        publish_message(redis_instance, message.to_dict())
