from typing import Optional, List


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def traversal(head: Optional[ListNode]) -> List[int]:
    """
    Input: head = [1, 2, 3, 4, 5]
    Output: [1, 2, 3, 4, 5]
    """
    ans = []
    curr = head

    while curr:
        ans.append(curr.val)
        curr = curr.next

    return ans


def detectCycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Input: head = [3, 2, 0, -4], pos = 1
    Output: Node with value 2
    """
    slow, fast = head, head

    # Cycle detection
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            break
    else:
        return None

    # return slow -> middle node of linked list

    start = head

    # Find the starting node of the cycle
    while start != slow:
        start = start.next
        slow = slow.next

    return start


def mergeTwoLists(
    list1: Optional[ListNode], list2: Optional[ListNode]
) -> Optional[ListNode]:
    """
    Input: list1 = [1, 2, 4], list2 = [1, 3, 4]
    Output: [1, 1, 2, 3, 4, 4]
    """
    dummy = ListNode(0)
    curr = dummy

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
    length = 0
    tmp = head

    while tmp:
        tmp = tmp.next
        length += 1

    startIndex = length - n

    if startIndex == 0:
        return head.next

    dummy = head

    for _ in range(startIndex - 1):
        dummy = dummy.next

    dummy.next = dummy.next.next

    return head


# TODO
def reorderList(head: Optional[ListNode]) -> None:
    """
    Input: head = [1, 2, 3, 4]
    Output: [1, 4, 2, 3]
    """
    # 1. Find middle
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 2. Reverse from middle
    previous = None
    current = slow

    while current:
        nextNode = current.next
        current.next = previous
        previous = current
        current = nextNode

    # 3. Merge
    first = head
    second = previous

    while second.next:
        firstNext = first.next
        secondNext = second.next

        first.next = second
        second.next = firstNext

        first = firstNext
        second = secondNext


def mergeInBetween(list1: ListNode, a: int, b: int, list2: ListNode) -> ListNode:
    """
    Input: list1 = [1,2,3,4,5,6], a = 2, b = 4, list2 = [1000000,1000001,1000002]
    Output: [1,2,1000000,1000001,1000002,5,6]
    """
    startNode = None
    endNode = None

    head = list1
    count = 0

    while head:
        if count == a - 1:
            startNode = head

        if count == b + 1:
            endNode = head
            break

        head = head.next
        count += 1

    # connect start of list1 to list2
    startNode.next = list2

    # find tail of list2
    head = list2

    while head.next:
        head = head.next

    # connect tail of list2 to remaining list1
    head.next = endNode

    return list1


def addTwoNumbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    """
    Input: l1 = [2,4,3], l2 = [5,6,4]
    Output: [7,0,8]
    Explanation: 342 + 465 = 807
    """
    dummy = ListNode()
    current = dummy
    carry = 0

    while True:
        # Base case
        if l1 is None and l2 is None and carry == 0:
            return dummy.next

        value1 = 0 if l1 is None else l1.val
        value2 = 0 if l2 is None else l2.val

        total = value1 + value2 + carry

        digit = total % 10
        carry = total // 10

        current.next = ListNode(digit)
        current = current.next

        if l1 is not None:
            l1 = l1.next

        if l2 is not None:
            l2 = l2.next
