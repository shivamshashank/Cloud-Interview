from collections import Counter
import heapq
from typing import Dict, Tuple
from typing_extensions import List


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None):
        self.val = val
        self.next = next


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
        count, num = heapq.heappop(heap)
        ans.append(num)

    return ans


def mergeKSortedLists(lists: List[ListNode | None]) -> List[int]:
    """
    Input: lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    Output: [1, 1, 2, 3, 4, 4, 5, 6]
    """
    heap: List[int] = []

    for node in lists:
        while node:
            heapq.heappush(heap, node.val)
            node = node.next

    dummy = ListNode(0)
    ans: ListNode = dummy

    while heap:
        dummy.next = ListNode(heapq.heappop(heap))
        dummy = dummy.next

    result: List[int] = []
    node = ans.next
    while node:
        result.append(node.val)
        node = node.next
    return result


class MedianFinder:
    """
    Input: ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"], [[], [1], [2], [], [3], []]
    Output: [None, None, None, 1.5, None, 2.0]
    """

    def __init__(self):
        self.small: List[int] = []  # max heap
        self.large: List[int] = []  # min heap

    def addNum(self, num: int) -> None:
        if len(self.small) == 0:
            heapq.heappush_max(self.small, num)
        elif num > self.small[0]:
            heapq.heappush(self.large, num)
        else:
            heapq.heappush_max(self.small, num)

        # Balance
        if len(self.large) - len(self.small) > 1:
            heapq.heappush_max(self.small, heapq.heappop(self.large))
        elif len(self.small) - len(self.large) > 1:
            heapq.heappush(self.large, heapq.heappop_max(self.small))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return self.small[0]
        if len(self.large) > len(self.small):
            return self.large[0]

        return (self.small[0] + self.large[0]) / 2
