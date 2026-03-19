from .base import EvictionStrategy

class Node:
    def __init__(self, key):
        self.key = key
        self.visited = False
        self.prev = None
        self.next = None

class SIEVEStrategy(EvictionStrategy):
    def __init__(self):
        self._nodes = {}
        self._head = None
        self._tail = None
        self._hand = None

    def add(self, key):
        node = Node(key)
        self._nodes[key] = node
        if self._head is None:
            self._head = self._tail = node
            self._hand = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node

    def access(self, key):
        self._nodes[key].visited = True

    def evict(self):
        while True:
            if self._hand is None:
                self._hand = self._tail
            node = self._hand
            if not node.visited:
                self._hand = node.prev
                self._remove_node(node)
                del self._nodes[node.key]
                return node.key
            node.visited = False
            self._hand = node.prev

    def remove(self, key):
        node = self._nodes.pop(key)
        if self._hand is node:
            self._hand = node.prev
        self._remove_node(node)

    def _remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self._head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self._tail = node.prev