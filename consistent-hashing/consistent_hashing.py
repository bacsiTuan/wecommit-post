import mmh3


class ConsistentHashing:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []
        self.nodes = nodes or []
        for node in self.nodes:
            self.add_node(node)

    def add_node(self, node):
        for i in range(self.replicas):
            key = self.hash(f"{node}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node):
        for i in range(self.replicas):
            key = self.hash(f"{node}:{i}")
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key):
        if not self.ring:
            return None
        hash_value = self.hash(key)
        idx = self.find_node(hash_value)
        return self.ring[self.sorted_keys[idx]]

    def find_node(self, hash_value):
        for idx, key in enumerate(self.sorted_keys):
            if hash_value <= key:
                return idx
        return 0

    @staticmethod
    def hash(key):
        return mmh3.hash(key)
