import redis
from consistent_hashing import ConsistentHashing


class Master:
    def __init__(self, workers):
        self.redis = redis.Redis(host="localhost", port=6379, db=0)
        self.workers = workers
        self.consistent_hashing = ConsistentHashing(workers)

    def assign_symbols(self, symbols):
        assignment = {}
        for symbol in symbols:
            worker = self.consistent_hashing.get_node(symbol)
            assignment[symbol] = worker
            self.redis.rpush(f"worker:{worker}:symbols", symbol)
        return assignment

    def rebalance_symbols(self):
        symbols_to_reassign = []
        for worker in self.workers:
            symbols = self.redis.lrange(f"worker:{worker}:symbols", 0, -1)
            for symbol in symbols:
                symbol = symbol.decode()
                correct_worker = self.consistent_hashing.get_node(symbol)
                if correct_worker != worker:
                    symbols_to_reassign.append((symbol, correct_worker, worker))

        for symbol, correct_worker, old_worker in symbols_to_reassign:
            self.redis.lrem(f"worker:{old_worker}:symbols", 1, symbol)
            self.redis.rpush(f"worker:{correct_worker}:symbols", symbol)

        return symbols_to_reassign

    def add_worker(self, new_worker):
        self.consistent_hashing.add_node(new_worker)
        self.workers.append(new_worker)
        return self.rebalance_symbols()

    def remove_worker(self, worker_to_remove):
        # Remove worker from consistent hashing ring
        self.consistent_hashing.remove_node(worker_to_remove)
        self.workers.remove(worker_to_remove)

        # Get symbols from the removed worker and reassign them
        symbols_to_reassign = self.redis.lrange(
            f"worker:{worker_to_remove}:symbols", 0, -1
        )
        reassigned_symbols = []

        for symbol in symbols_to_reassign:
            symbol = symbol.decode()
            correct_worker = self.consistent_hashing.get_node(symbol)
            self.redis.rpush(f"worker:{correct_worker}:symbols", symbol)
            reassigned_symbols.append((symbol, correct_worker))

        # Clean up Redis by removing the old worker's symbol list
        self.redis.delete(f"worker:{worker_to_remove}:symbols")

        return reassigned_symbols

    def get_assignment(self):
        assignment = {}
        for worker in self.workers:
            symbols = self.redis.lrange(f"worker:{worker}:symbols", 0, -1)
            assignment[worker] = [symbol.decode() for symbol in symbols]
        return assignment


if __name__ == "__main__":
    workers = ["worker1", "worker2", "worker3"]
    master = Master(workers)

    symbols = ["PERLUSDT", "DODOUSDT", "CTSIUSDT", "ACHBUSD", "TRBBUSD", "ALGOBUSD", "KP3RUSDT", "LINAUSDT",
               "RAYBUSD", "REEFUSDT", "ATABUSD", "SUPERUSDT", "CTKBUSD", "STXUSDT", "DOCKUSDT", "KDAUSDT",
               "FTTBUSD", "MBLBUSD", "MANABUSD", "WANUSDT", "NEBLBUSD", "DUSKUSDT", "OOKIBUSD", "STPTBUSD",
               "FARMBUSD", "SXPBUSD", "RADUSDT", "HOOKUSDT", "ONTBUSD", "BAKEUSDT", "ARKBUSD", "MDXBUSD",
               "AUTOUSDT", "NULSUSDT", "HOTBUSD", "XLMUSDT", "EGLDUSDT", "ATAUSDT", "AGLDUSDT", "FLOWUSDT",
               "LSKBUSD", "TOMOUSDT", "LITUSDT", "QTUMUSDT", "IQBUSD", "TKOUSDT", "JUVUSDT", "XMRUSDT",
               "LOOMUSDT", "LSKUSDT", "USDPUSDT", "CELOBUSD", "SNTBUSD", "ICPBUSD", "PENDLEUSDT", "ARBUSD",
               "RSRBUSD", "BTCUSDT", "AUTOBUSD", "DASHUSDT", "WAXPUSDT", "RLCUSDT"]
    print(len(symbols)) #62
    master.assign_symbols(symbols)
    assignment = master.get_assignment()
    print("Initial Symbol Assignment:", assignment)

    # Add a new worker and rebalance the symbols
    # new_worker = "worker4"
    # reassigned_symbols = master.add_worker(new_worker)
    # print(f"Reassigned Symbols: {reassigned_symbols}")

    # Remove a worker and rebalance the symbols
    # worker_to_remove = "worker2"
    # reassigned_symbols = master.remove_worker(worker_to_remove)
    # print(f"Reassigned Symbols After Removing {worker_to_remove}: {reassigned_symbols}")

    new_assignment = master.get_assignment()
    print("New Symbol Assignment:", new_assignment)
