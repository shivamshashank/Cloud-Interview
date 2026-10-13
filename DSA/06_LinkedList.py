from typing import Optional, List


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val: int = val
        self.next: ListNode | None = next


def traversal(head: Optional[ListNode]) -> List[int]:
    """
    Input: head = [1, 2, 3, 4, 5]
    Output: [1, 2, 3, 4, 5]
    """
    ans: list[int] = []
    curr: ListNode | None = head

    while curr:
        ans.append(curr.val)
        curr = curr.next

    return ans


def detectCycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Input: head = [3, 2, 0, -4], pos = 1
    Output: Node with value 2
    """
    slow: ListNode | None
    fast: ListNode | None
    slow, fast = head, head

    # Cycle detection
    while fast and fast.next:
        if slow is None:
            raise RuntimeError('Cycle traversal unexpectedly reached the end of the list')
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            break
    else:
        return None

    start: ListNode | None = head

    # Find the starting node of the cycle
    while start != slow:
        if start is None or slow is None:
            raise RuntimeError('Detected cycle has an invalid traversal path')
        start = start.next
        if slow is None:
            raise RuntimeError('Cycle traversal unexpectedly reached the end of the list')
        slow = slow.next

    return start


def mergeTwoLists(
    list1: Optional[ListNode], list2: Optional[ListNode]
) -> Optional[ListNode]:
    """
    Input: list1 = [1, 2, 4], list2 = [1, 3, 4]
    Output: [1, 1, 2, 3, 4, 4]
    """
    dummy: ListNode = ListNode(0)
    curr: ListNode = dummy

    while list1 and list2:
        if list1.val < list2.val:
            dummy.next = list1
            list1 = list1.next
        else:
            dummy.next = list2
            list2 = list2.next

        dummy = dummy.next

    dummy.next = list1 or list2

    return curr.next


def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    Input: head = [1, 2, 3, 4, 5], n = 2
    Output: [1, 2, 3, 5]
    """
    if n <= 0:
        raise ValueError("n must be positive")
    dummy: ListNode = ListNode(0, head)
    fast: ListNode = dummy
    slow: ListNode = dummy
    for _ in range(n):
        successor: ListNode | None = fast.next
        if successor is None:
            raise ValueError("n exceeds the list length")
        fast = successor
    while fast.next is not None:
        fast = fast.next
        successor = slow.next
        if successor is None:
            raise RuntimeError('List traversal unexpectedly reached the end')
        slow = successor
    removed: ListNode | None = slow.next
    if removed is None:
        raise RuntimeError('Validated removal has no target node')
    slow.next = removed.next
    return dummy.next


def reorderList(head: Optional[ListNode]) -> None:
    """
    Input: head = [1, 2, 3, 4]
    Output: [1, 4, 2, 3]
    """
    if head is None or head.next is None:
        return

    # Split into disjoint halves; the first is at least as long as the second.
    slow: ListNode = head
    fast: ListNode | None = head.next
    while fast is not None and fast.next is not None:
        successor: ListNode | None = slow.next
        if successor is None:
            raise RuntimeError('List traversal unexpectedly reached the end')
        slow = successor
        fast = fast.next.next
    second: ListNode | None = reverseList(slow.next)
    slow.next = None

    # Weave the reversed second half into the first half.
    first: ListNode | None = head
    while second is not None:
        if first is None:
            raise RuntimeError('First list half is shorter than the second half')
        first_next: ListNode | None = first.next
        second_next: ListNode | None = second.next
        first.next = second
        second.next = first_next
        first, second = first_next, second_next


def mergeInBetween(list1: ListNode, a: int, b: int, list2: ListNode | None) -> ListNode | None:
    """Replace zero-based indices a through b (inclusive) with list2.

    Input: [1,2,3,4,5,6], a=2, b=4, list2=[100,101].
    Output: [1,2,100,101,6]. Valid bounds required; supports a=0 and empty list2.
    O(len(list1) + len(list2)) time, O(1) extra space.
    """
    if a < 0 or b < a:
        raise ValueError("require 0 <= a <= b")
    dummy: ListNode = ListNode(0, list1)
    before: ListNode = dummy
    for _ in range(a):
        successor: ListNode | None = before.next
        if successor is None:
            raise ValueError("a exceeds the list bounds")
        before = successor
    after: ListNode | None = before.next
    for _ in range(b - a + 1):
        if after is None:
            raise ValueError("b exceeds the list bounds")
        after = after.next
    before.next = list2
    while before.next is not None:
        before = before.next
    before.next = after
    return dummy.next


def addTwoNumbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    """
    Input: l1 = [2,4,3], l2 = [5,6,4]
    Output: [7,0,8]
    Explanation: 342 + 465 = 807
    """
    dummy: ListNode = ListNode()
    current: ListNode = dummy
    carry: int = 0

    while True:
        # Base case
        if l1 is None and l2 is None and carry == 0:
            return dummy.next

        value1: int = 0 if l1 is None else l1.val
        value2: int = 0 if l2 is None else l2.val

        total: int = value1 + value2 + carry

        digit: int = total % 10
        carry = total // 10

        current.next = ListNode(digit)
        current = current.next

        if l1 is not None:
            l1 = l1.next

        if l2 is not None:
            l2 = l2.next


def reverseList(head: Optional[ListNode]) -> Optional[ListNode]:
    """LC 206: Reverse Linked List (Easy).

    Input: 1->2->3. Output: 3->2->1. Empty input returns None.
    Save the next node before reversing each link. O(n) time, O(1) space.
    """
    previous: ListNode | None = None
    while head:
        successor: ListNode | None = head.next
        head.next = previous
        previous, head = head, successor
    return previous
