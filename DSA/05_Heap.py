from collections import Counter
import heapq
from typing import Dict, Tuple, List


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val: int = val
        self.next: ListNode | None = next


def findKthLargestElement(nums: List[int], k: int) -> int:
    """
    Input: nums = [3, 2, 1, 5, 6, 4], k = 2
    Output: 5
    """
    heap: List[int] = []

    for num in nums:
        if len(heap) == k:
            if heap[0] < num:
                heapq.heappop(heap)
                heapq.heappush(heap, num)
        else:
            heapq.heappush(heap, num)

    return heap[0]


def topKFrequentElements(nums: List[int], k: int) -> List[int]:
    """
    Input: nums = [1, 1, 1, 2, 2, 3], k = 2
    Output: [1, 2]
    """
    heap: List[Tuple[int, int]] = []

    freq: Dict[int, int] = Counter(nums)

    ans: List[int] = []

    for num, count in freq.items():
        if len(heap) == k:
            if heap[0][0] < count:
                heapq.heappop(heap)
                heapq.heappush(heap, (count, num))
        else:
            heapq.heappush(heap, (count, num))

    while heap:
        count: int
        num: int
        count, num = heapq.heappop(heap)
        ans.append(num)

    return ans


def mergeKSortedLists(lists: List[ListNode | None]) -> ListNode | None:
    """LC 23. Merge disjoint sorted linked lists and return the head.

    Input: [[1, 4, 5], [1, 3, 4], [2, 6]]. Output: 1->1->2->3->4->4->5->6.
    Reuses input nodes. O(N log k) time, O(k) extra space.
    """
    heap: list[tuple[int, int, ListNode]] = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(heap)
    dummy: ListNode
    tail: ListNode
    dummy = tail = ListNode()
    while heap:
        source: int
        node: ListNode
        _, source, node = heapq.heappop(heap)
        successor: ListNode | None = node.next
        tail.next = node
        tail = node
        if successor:
            heapq.heappush(heap, (successor.val, source, successor))
    tail.next = None
    return dummy.next


class MedianFinder:
    """LC 295. addNum(1), addNum(2), findMedian() -> 1.5.

    Uses Python 3.14's native max-heap operations.
    addNum: O(log n); findMedian: O(1); storage: O(n).
    """
    def __init__(self) -> None:
        self.small: list[int] = []  # Lower half; same size as upper or one larger.
        self.large: list[int] = []

    def addNum(self, num: int) -> None:
        heapq.heappush_max(self.small, num)
        heapq.heappush(self.large, heapq.heappop_max(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush_max(self.small, heapq.heappop(self.large))

    def findMedian(self) -> float:
        if not self.small:
            raise ValueError("median requires at least one value")
        if len(self.small) > len(self.large):
            return self.small[0]
        return (self.small[0] + self.large[0]) / 2
