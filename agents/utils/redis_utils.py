import json

from redis import Redis
import redis
from redis.client import PubSub

from agents.config import REDIS_HOST, REDIS_CHANEL, REDIS_PORT


def publish_message(redis_conn: Redis, message: dict):
    try:
        redis_conn.publish(REDIS_CHANEL, json.dumps(message))
    except redis.exceptions.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        return False
    return True

def get_redis_conn() -> tuple[redis.Redis, PubSub]:

    redis_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    pubsub = redis_instance.pubsub()
    pubsub.subscribe(REDIS_CHANEL)
    return redis_instance, pubsub
