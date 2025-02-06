# Auto software engineer multi agents using a large language model

This is a Python project using poetry as dependency management. Below are the instructions for running it.

- Suggestion to use linux
- Install any python 3
- Install poetry globally to your python 3 $ ```pip3 install poetry```
- Set poetry to create env in the project: $ ```poetry config virtualenvs.in-project true```
- Activate the python environment $ ```poetry shell```
- Install dependencies $ ```poetry install```
- Install mongo database management
- Create a .env based on the .env.example file
- Run the python project with ```python run agents/__main__.py```
- Tests are in /tests folder, run them with ```python -m unittest```



# Redis communication

An example functions to subscribe and send messages using Redis library is as follows:
```Python
import redis
from redis import Redis
import time

def listen_forever(r_connection: Redis, channel: str):

    pubsub = r.pubsub()
    pubsub.subscribe(channel)

    for message in pubsub.listen():
        if message['type'] == 'message':
            if isinstance(message['data'], bytes):
                decoded_message = message['data'].decode('utf-8')
            else:
                decoded_message = message['data']
            print(f"Received message: {decoded_message} from channel {channel}")

def publish_message(r_connection: Redis, channel: str, message: str):
    try:
        r_connection.publish(channel, message)
    except redis.exceptions.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        return False
    return True

```

The following is an example of how to instanciate the Redis subscribe:

```Python
redis_instance = redis.Redis(host='localhost', port=6379, db=0)
channel_name = "my_channel"
```
