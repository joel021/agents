import time

from redis.client import PubSub
from threading import Thread

from agents.constants import USER_NAME, PROJECT_MANAGER_AGENT_NAME
from agents.core.message import Message
from agents.utils.jsons import decode_message
from agents.utils.redis_utils import get_redis_conn, publish_message

def listen(pubsub: PubSub, print_all: bool = True):

    print("Service started")

    for message_str in pubsub.listen():
        msg_dict = decode_message(message_str)
        if msg_dict:
            message = Message(**msg_dict)
            if print_all:
                print(f"\n{time.strftime("%Y-%m-%d %H:%M:%S")} {message.sender}: @{message.recipient}\n {message.message}\n")
        else:
            #print(f"\n{time.strftime("%Y-%m-%d %H:%M:%S")} {USER_NAME} - Received an invalid message: {message_str}\n")
            pass

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

        message = Message(sender=USER_NAME, recipient=PROJECT_MANAGER_AGENT_NAME, message=user_message)
        publish_message(redis_instance, message.to_dict())
