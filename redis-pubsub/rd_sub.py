from redis_om import get_redis_connection
import json
redis = get_redis_connection(
    host="localhost",
    port=6379,
    password="",
    decode_responses=True,
)
CHANNEL = 'test'
if __name__ == '__main__':
    pub = redis.pubsub()
    pub.subscribe(CHANNEL)

    for message in pub.listen():
        if message is not None and isinstance(message, dict) and message.get("data") != 1:
            data = json.loads(message.get('data'))
            # print(data["tuan"])
            print(f"Message: {data}")
