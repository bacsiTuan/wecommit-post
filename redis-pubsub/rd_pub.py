from redis_om import get_redis_connection
import time
import json

redis = get_redis_connection(
    host="localhost",
    port=6379,
    password="",
    decode_responses=True,
)
CHANNEL = 'test'
data = {
    "tuan": time.time(),
}
if __name__ == "__main__":
    while True:
        pub = redis.publish(
            channel=CHANNEL,
            message=json.dumps({
                "tuan": time.time(),
            })
        )
        time.sleep(1)
