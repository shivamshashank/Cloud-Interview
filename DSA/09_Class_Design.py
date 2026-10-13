from typing import Tuple, Set, List, Dict
from collections import defaultdict, deque
import random


class Node:
    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key: int = key
        self.value: int = value
        self.prev: Node | None = None
        self.next: Node | None = None


# Doubly linked list + hash map
class LRUCache:
    """
    Input: ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"], [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
    Output: [None, None, None, 1, None, -1, None, -1, 3, 4]
    """

    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.cache: dict[int, Node] = {}

        # Dummy nodes
        self.left: Node = Node()  # LRU side
        self.right: Node = Node()  # MRU side

        self.left.next = self.right
        self.right.prev = self.left

    # Remove node from linked list
    def remove(self, node: Node) -> None:
        previous: Node | None = node.prev
        nextNode: Node | None = node.next

        if previous is None or nextNode is None:
            raise RuntimeError('Cannot unlink a node without both neighbors')
        previous.next = nextNode
        nextNode.prev = previous

    # Add node before right (MRU position)
    def insert(self, node: Node) -> None:
        previous: Node | None = self.right.prev

        if previous is None:
            raise RuntimeError('Right sentinel has no predecessor')
        previous.next = node
        node.prev = previous

        node.next = self.right
        self.right.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node: Node = self.cache[key]

        # Move to MRU position
        self.remove(node)
        self.insert(node)

        return node.value

    def put(self, key: int, value: int) -> None:

        # Key already exists
        if key in self.cache:
            self.remove(self.cache[key])

        # Create/update node
        node: Node = Node(key, value)
        self.cache[key] = node

        # Add as most recently used
        self.insert(node)

        # Capacity exceeded
        if len(self.cache) > self.capacity:

            # First real node = LRU
            lru: Node | None = self.left.next

            if lru is None or lru is self.right:
                raise RuntimeError('Cache eviction has no data node')
            self.remove(lru)
            del self.cache[lru.key]


class TimeMap:
    """
    Input: ["TimeMap", "set", "get", "get", "set", "get", "get"], [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
    Output: [None, None, "bar", "bar", None, "bar2", "bar2"]
    """

    def __init__(self) -> None:
        self.store: dict[str, List[Tuple[int, str]]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key in self.store:
            ans: str = ""
            curr: list[tuple[int, str]] = self.store[key]

            s: int = 0
            e: int = len(curr) - 1

            while s <= e:
                mid: int = s + (e - s) // 2

                # timestamp at mid
                if curr[mid][0] <= timestamp:
                    ans = curr[mid][1]  # Possible answer
                    s = mid + 1  # Try to find a later valid timestamp
                else:
                    e = mid - 1

            return ans

        return ""


class RandomizedSet:
    """LC 380. Average O(1) insert, remove and uniformly random getRandom.

    insert(1) -> True; insert(1) -> False; remove(1) -> True.
    getRandom requires a nonempty set. Storage: O(n).
    """
    def __init__(self) -> None:
        self.values: List[int] = []
        self.positions: Dict[int, int] = {}

    def insert(self, val: int) -> bool:
        if val in self.positions:
            return False
        self.positions[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.positions:
            return False
        index: int = self.positions[val]
        last: int = self.values[-1]
        self.values[index] = last
        self.positions[last] = index
        self.values.pop()
        del self.positions[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.values)


# """
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
# """
class NestedInteger:
    def isInteger(self) -> bool:
        """
        @return True if this NestedInteger holds a single integer, rather than a nested list.
        """
        raise NotImplementedError("provided by the online judge")

    def getInteger(self) -> int | None:
        """
        @return the single integer that this NestedInteger holds, if it holds a single integer
        Return None if this NestedInteger holds a nested list
        """
        raise NotImplementedError("provided by the online judge")

    def getList(self) -> List[NestedInteger] | None:
        """
        @return the nested list that this NestedInteger holds, if it holds a nested list
        Return None if this NestedInteger holds a single integer
        """
        raise NotImplementedError("provided by the online judge")


class NestedIterator:
    """
    Input: nestedList = [[1, 1], 2, [1, 1]]
    Output: [1, 1, 2, 1, 1]
    """

    def __init__(self, nestedList: List[NestedInteger]) -> None:
        self.stack: List[int] = []

        def dfs(nestedList: List[NestedInteger]) -> None:
            for nL in reversed(nestedList):
                if nL.isInteger():
                    value: int | None = nL.getInteger()
                    if value is None:
                        raise RuntimeError('Integer-valued entry did not provide an integer')
                    self.stack.append(value)
                else:
                    children: list[NestedInteger] | None = nL.getList()
                    if children is None:
                        raise RuntimeError('List-valued entry did not provide a list')
                    dfs(children)

        dfs(nestedList)

    def next(self) -> int:
        return self.stack.pop()

    def hasNext(self) -> bool:
        return bool(self.stack)


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

    def __init__(self) -> None:
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

    def __init__(self) -> None:
        self.hits: deque[list[int]] = deque()  # stores [timestamp, count]
        self.total: int = 0

    def hit(self, timestamp: int) -> None:
        self.getHits(timestamp)
        if self.hits and self.hits[-1][0] == timestamp:
            self.hits[-1][1] += 1
        else:
            self.hits.append([timestamp, 1])
        self.total += 1

    def getHits(self, timestamp: int) -> int:
        while self.hits and self.hits[0][0] <= timestamp - 300:
            count: int
            _, count = self.hits.popleft()
            self.total -= count
        return self.total
