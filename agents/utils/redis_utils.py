import json

from redis import Redis
import redis
from redis.client import PubSub

from agents.config import REDIS_HOST, REDIS_CHANEL, REDIS_PORT
from agents.constants import EVERYONE
from agents.core.message import Message


def publish_message(redis_conn: Redis, channel: str, message: str):
    try:
        redis_conn.publish(channel, message)
    except redis.exceptions.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        return False
    return True

def get_redis_conn(agent_name: str) -> tuple[redis.Redis, PubSub]:

    redis_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    pubsub = redis_instance.pubsub()
    pubsub.subscribe(REDIS_CHANEL)

    message_str = json.dumps(Message(
        sender=agent_name,
        recipient=EVERYONE,
        message="I am ready to interact! I am listening.",
    ).to_dict())
    publish_message(redis_instance, REDIS_CHANEL, message_str)

    return redis_instance, pubsub
