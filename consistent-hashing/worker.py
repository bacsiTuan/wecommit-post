import redis


class Worker:
    def __init__(self, name):
        self.name = name
        self.redis = redis.Redis(host="localhost", port=6379, db=0)

    def get_symbols(self):
        symbols = self.redis.lrange(f"worker:{self.name}:symbols", 0, -1)
        return [symbol.decode() for symbol in symbols]

    def process_symbols(self):
        symbols = self.get_symbols()
        for symbol in symbols:
            print(f"{self.name} is processing {symbol}")


if __name__ == "__main__":
    worker_name = "worker1"
    worker = Worker(worker_name)
    worker.process_symbols()
