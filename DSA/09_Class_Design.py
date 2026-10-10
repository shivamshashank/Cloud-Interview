from typing import Tuple, Set, List, Dict
from collections import defaultdict, deque
import random


class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


# TODO -> Hard -> Design Pattern + Doubly Linked List + Hash Map
class LRUCache:
    """
    Input: ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"], [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
    Output: [None, None, None, 1, None, -1, None, -1, 3, 4]
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}

        # Dummy nodes
        self.left = Node()  # LRU side
        self.right = Node()  # MRU side

        self.left.next = self.right
        self.right.prev = self.left

    # Remove node from linked list
    def remove(self, node):
        previous = node.prev
        nextNode = node.next

        previous.next = nextNode
        nextNode.prev = previous

    # Add node before right (MRU position)
    def insert(self, node):
        previous = self.right.prev

        previous.next = node
        node.prev = previous

        node.next = self.right
        self.right.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]

        # Move to MRU position
        self.remove(node)
        self.insert(node)

        return node.value

    def put(self, key: int, value: int) -> None:

        # Key already exists
        if key in self.cache:
            self.remove(self.cache[key])

        # Create/update node
        node = Node(key, value)
        self.cache[key] = node

        # Add as most recently used
        self.insert(node)

        # Capacity exceeded
        if len(self.cache) > self.capacity:

            # First real node = LRU
            lru = self.left.next

            self.remove(lru)
            del self.cache[lru.key]


class TimeMap:
    """
    Input: ["TimeMap", "set", "get", "get", "set", "get", "get"], [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
    Output: [None, None, "bar", "bar", None, "bar2", "bar2"]
    """

    def __init__(self):
        self.store: dict[str, List[Tuple[int, str]]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key in self.store:
            ans = ""
            curr = self.store[key]

            s = 0
            e = len(curr) - 1

            while s <= e:
                mid = s + (e - s) // 2

                # timestamp at mid
                if curr[mid][0] <= timestamp:
                    ans = curr[mid][1]  # Possible answer
                    s = mid + 1  # Try to find a later valid timestamp
                else:
                    e = mid - 1

            return ans

        return ""


class RandomizedSet:
    """
    Input: ["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"], [[], [1], [2], [2], [], [1], [2], []]
    Output: [None, True, False, True, 2, True, False, 2]
    """

    def __init__(self):
        self.store: Set[int] = set()

    def insert(self, val: int) -> bool:
        if val in self.store:
            return False

        self.store.add(val)

        return True

    def remove(self, val: int) -> bool:
        if val not in self.store:
            return False

        self.store.remove(val)

        return True

    def getRandom(self) -> int:
        randIndex = random.randint(0, len(self.store) - 1)

        return list(self.store)[randIndex]


# """
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
# """
class NestedInteger:
    def isInteger(self) -> bool:
        """
        @return True if this NestedInteger holds a single integer, rather than a nested list.
        """

    def getInteger(self) -> int:
        """
        @return the single integer that this NestedInteger holds, if it holds a single integer
        Return None if this NestedInteger holds a nested list
        """

    def getList(self) -> List[NestedInteger]:
        """
        @return the nested list that this NestedInteger holds, if it holds a nested list
        Return None if this NestedInteger holds a single integer
        """


class NestedIterator:
    """
    Input: nestedList = [[1, 1], 2, [1, 1]]
    Output: [1, 1, 2, 1, 1]
    """

    def __init__(self, nestedList: List[NestedInteger]):
        self.stack: List[int] = []

        def dfs(nestedList: List[NestedInteger]) -> None:
            for nL in reversed(nestedList):
                if nL.isInteger():
                    self.stack.append(nL.getInteger())
                else:
                    dfs(nL.getList())

        dfs(nestedList)

    def next(self) -> int:
        return self.stack.pop()

    def hasNext(self) -> bool:
        return self.stack


# Your NestedIterator object will be instantiated and called as such:
# i, v = NestedIterator(nestedList), []
# while i.hasNext(): v.append(i.next())


# ==============================================================================
# 5. Logger Rate Limiter (LC 359)
# ==============================================================================
class Logger:
    """
    Input: ["Logger", "shouldPrintMessage", "shouldPrintMessage", "shouldPrintMessage", "shouldPrintMessage", "shouldPrintMessage", "shouldPrintMessage"], [[], [1, "foo"], [2, "bar"], [3, "foo"], [8, "bar"], [10, "foo"], [11, "foo"]]
    Output: [None, True, True, False, False, False, True]
    """

    def __init__(self):
        self.msg_to_time: Dict[str, int] = {}

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if (
            message not in self.msg_to_time
            or timestamp - self.msg_to_time[message] >= 10
        ):
            self.msg_to_time[message] = timestamp
            return True
        return False


# ==============================================================================
# 6. Design Hit Counter (LC 362)
# ==============================================================================
class HitCounter:
    """
    Input: ["HitCounter", "hit", "hit", "hit", "getHits", "hit", "getHits", "getHits"], [[], [1], [2], [3], [4], [300], [300], [301]]
    Output: [None, None, None, None, 3, None, 4, 3]
    """

    def __init__(self):
        self.hits = deque()  # stores [timestamp, count]
        self.total = 0

    def hit(self, timestamp: int) -> None:
        if self.hits and self.hits[-1][0] == timestamp:
            self.hits[-1][1] += 1
        else:
            self.hits.append([timestamp, 1])
        self.total += 1

    def getHits(self, timestamp: int) -> int:
        while self.hits and self.hits[0][0] <= timestamp - 300:
            _, count = self.hits.popleft()
            self.total -= count
        return self.total
