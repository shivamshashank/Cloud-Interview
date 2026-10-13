# PIP -> NLR, LNR, LRN

from collections import deque
from typing import Optional, Tuple, List


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional[TreeNode] = None,
        right: Optional[TreeNode] = None,
    ) -> None:
        self.val: int = val
        self.left: TreeNode | None = left
        self.right: TreeNode | None = right


def inorder(root: Optional[TreeNode]) -> List[int]:
    """LC 94. Input: [1, None, 2, 3]. Output: [1, 3, 2].

    Iterative traversal: O(n) time and O(h) stack space, excluding output.
    """
    result: list[int]
    stack: list[TreeNode]
    result, stack = [], []
    while root or stack:
        while root:
            stack.append(root)
            root = root.left
        root = stack.pop()
        result.append(root.val)
        root = root.right
    return result


def levelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Input: root = [3, 9, 20, None, None, 15, 7]
    Output: [[3], [9, 20], [15, 7]]
    """
    if root is None:
        return []

    ans: list[list[int]] = []

    queue: deque[TreeNode] = deque([root])

    while queue:
        level: list[int] = []

        for i in range(len(queue)):
            node: TreeNode = queue.popleft()

            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        ans.append(level)

    return ans


def maxDepth(root: Optional[TreeNode]) -> int:
    """
    Input: root = [3, 9, 20, None, None, 15, 7]
    Output: 3
    """
    if root is None:
        return 0

    return max(maxDepth(root.left), maxDepth(root.right)) + 1


def diameterOfBinaryTree(root: Optional[TreeNode]) -> int:
    """
    Input: root = [1, 2, 3, 4, 5]
    Output: 3
    """

    def dfs(root: Optional[TreeNode]) -> Tuple[int, int]:
        if root is None:
            return (0, 0)

        leftHeight: int
        leftDiameter: int
        leftHeight, leftDiameter = dfs(root.left)
        rightHeight: int
        rightDiameter: int
        rightHeight, rightDiameter = dfs(root.right)

        return (
            max(leftHeight, rightHeight) + 1,
            max(leftHeight + rightHeight, leftDiameter, rightDiameter),
        )

    return dfs(root)[1]


def searchBST(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Input: root = [4, 2, 7, 1, 3], val = 2
    Output: [2, 1, 3]
    """
    if root is None:
        return None

    if val < root.val:
        return searchBST(root.left, val)
    elif val > root.val:
        return searchBST(root.right, val)
    else:
        return root


def isValidBST(root: Optional[TreeNode]) -> bool:
    """
    Input: root = [2, 1, 3]
    Output: True
    """

    def dfs(root: Optional[TreeNode], left: float, right: float) -> bool:
        if root is None:
            return True

        if not left < root.val < right:
            return False

        return dfs(root.left, left, root.val) and dfs(root.right, root.val, right)

    return dfs(root, float("-inf"), float("inf"))


def isSymmetric(root: Optional[TreeNode]) -> bool:
    """
    Input: root = [1, 2, 2, 3, 4, 4, 3]
    Output: True
    """
    if root is None:
        return True

    def dfs(left: Optional[TreeNode], right: Optional[TreeNode]) -> bool:
        if left is None and right is None:
            return True

        if left is None or right is None or left.val != right.val:
            return False

        return dfs(left.left, right.right) and dfs(left.right, right.left)

    return dfs(root.left, root.right)


def lowestCommonAncestorBST(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Input: root = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], p = 2, q = 8
    Output: 6
    """
    if p.val < root.val and q.val < root.val:
        if root.left is None:
            raise ValueError("targets must exist in the BST")
        return lowestCommonAncestorBST(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        if root.right is None:
            raise ValueError("targets must exist in the BST")
        return lowestCommonAncestorBST(root.right, p, q)
    return root


def lowestCommonAncestorBT(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    """
    Input: root = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], p = 5, q = 1
    Output: 3
    """
    if root is None or root == p or root == q:
        return root

    left: TreeNode | None = lowestCommonAncestorBT(root.left, p, q)
    right: TreeNode | None = lowestCommonAncestorBT(root.right, p, q)

    if left and right:
        return root

    return left if left else right


def binaryTreePaths(root: Optional[TreeNode]) -> List[str]:
    """
    Input: root = [1, 2, 3, None, 5]
    Output: ["1->2->5", "1->3"]
    """
    ans: list[str] = []

    def dfs(root: Optional[TreeNode], curr: List[str]) -> None:
        if root is None:
            return

        curr = curr + [str(root.val)]

        if root.left is None and root.right is None:
            ans.append("->".join(curr))

        dfs(root.left, curr)
        dfs(root.right, curr)

    dfs(root, [])

    return ans


def hasPathSum(root: Optional[TreeNode], targetSum: int) -> bool:
    """
    Input: root = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], targetSum = 22
    Output: True
    """

    def dfs(root: Optional[TreeNode], total: int) -> bool:
        if root is None:
            return False

        total += root.val

        if root.left is None and root.right is None and total == targetSum:
            return True

        return dfs(root.left, total) or dfs(root.right, total)

    return dfs(root, 0)


def kthSmallest(root: Optional[TreeNode], k: int) -> int:
    """
    Input: root = [3, 1, 4, None, 2], k = 1
    Output: 1
    """
    ans: list[int] = []

    def inorder(root: Optional[TreeNode]) -> None:
        if root is None:
            return

        inorder(root.left)
        ans.append(root.val)
        inorder(root.right)

    inorder(root)

    return ans[k - 1]


def constructInorderPreorder(
    preorder: List[int], inorder: List[int]
) -> Optional[TreeNode]:
    """
    Input: preorder = [3, 9, 20, 15, 7], inorder = [9, 3, 15, 20, 7]
    Output: [3, 9, 20, None, None, 15, 7]
    """
    if not preorder or not inorder:
        return None

    rootValue: int = preorder[0]
    root: TreeNode = TreeNode(rootValue)

    mid: int = inorder.index(rootValue)

    root.left = constructInorderPreorder(preorder[1 : mid + 1], inorder[:mid])
    root.right = constructInorderPreorder(preorder[mid + 1 :], inorder[mid + 1 :])

    return root


def constructInorderPostorder(
    inorder: List[int], postorder: List[int]
) -> Optional[TreeNode]:
    """
    Input: inorder = [9, 3, 15, 20, 7], postorder = [9, 15, 7, 20, 3]
    Output: [3, 9, 20, None, None, 15, 7]
    """
    if not postorder or not inorder:
        return None

    rootValue: int = postorder[-1]
    root: TreeNode = TreeNode(rootValue)

    mid: int = inorder.index(rootValue)

    root.left = constructInorderPostorder(inorder[:mid], postorder[:mid])
    root.right = constructInorderPostorder(inorder[mid + 1 :], postorder[mid:-1])

    return root


def constructFromPreorderAndPostorder(
    preorder: List[int], postorder: List[int]
) -> Optional[TreeNode]:
    """LC 889. Build any matching tree from valid traversals of distinct values.

    Input: preorder=[1,2,4,5,3,6,7], postorder=[4,5,2,6,7,3,1].
    Output: [1,2,3,4,5,6,7]. A single child is placed on the left.
    The tree need not be unique. O(n) time and O(h) stack space.
    """
    if not preorder:
        return None
    root: TreeNode = TreeNode(preorder[0])
    stack: list[TreeNode] = [root]
    post_index: int = 0
    for value in preorder[1:]:
        while stack and stack[-1].val == postorder[post_index]:
            stack.pop()
            post_index += 1
        node: TreeNode = TreeNode(value)
        if stack[-1].left is None:
            stack[-1].left = node
        else:
            stack[-1].right = node
        stack.append(node)
    return root


class SerializeDeserialize:
    """
    Input: root = [1, 2, 3, None, None, 4, 5]
    Output: [1, 2, 3, None, None, 4, 5]
    """

    def serialize(self, root: Optional[TreeNode]) -> str:
        ans: List[str] = []

        def preorder(root: Optional[TreeNode]) -> None:
            if root is None:
                ans.append("None")
                return

            ans.append(f"{root.val}")
            preorder(root.left)
            preorder(root.right)

        preorder(root)

        return ",".join(ans)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        preorderList: list[str] = data.split(",")
        i: int = 0

        def dfs() -> Optional[TreeNode]:
            nonlocal i

            value: str = preorderList[i]
            i += 1

            if value == "None":
                return None

            root: TreeNode = TreeNode(int(value))

            root.left = dfs()
            root.right = dfs()

            return root

        return dfs()


def distanceK(root: TreeNode, target: TreeNode, k: int) -> List[int]:
    """
    Input: root = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], target = 5, k = 2
    Output: [7, 4, 1]
    """
    parent: dict[TreeNode, TreeNode] = {}

    def dfs(node: TreeNode | None) -> None:
        if not node:
            return

        if node.left:
            parent[node.left] = node

        if node.right:
            parent[node.right] = node

        dfs(node.left)
        dfs(node.right)

    dfs(root)

    queue: deque[TreeNode] = deque([target])
    visited: set[TreeNode] = {target}
    distance: int = 0

    while queue:
        if distance == k:
            return [node.val for node in queue]

        for _ in range(len(queue)):
            node: TreeNode = queue.popleft()

            for neighbor in [node.left, node.right, parent.get(node)]:
                if neighbor and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        distance += 1

    return []


def maxPathSum(root: Optional[TreeNode]) -> int:
    """
    Input: root = [-10, 9, 20, None, None, 15, 7]
    Output: 42
    """
    if root is None:
        raise ValueError("maximum path sum requires a nonempty tree")
    ans: int = root.val

    def dfs(root: Optional[TreeNode]) -> int:
        nonlocal ans

        if root is None:
            return 0

        left: int = max(dfs(root.left), 0)
        right: int = max(dfs(root.right), 0)

        ans = max(ans, left + right + root.val)

        return max(left, right, 0) + root.val

    dfs(root)

    return ans


type Subtree = tuple[int, Subtree, Subtree] | None


def findDuplicateSubtrees(root: TreeNode | None) -> list[TreeNode]:
    """
    Input: root = [1, 2, 3, 4, None, 2, 4, None, None, 4]
    Output: [2, 4]
    """

    ans: list[TreeNode] = []

    freq: dict[Subtree, int] = {}

    def dfs(root: TreeNode | None) -> Subtree:
        if root is None:
            return None

        left_subtree: Subtree = dfs(root.left)
        right_subtree: Subtree = dfs(root.right)

        curr_subtree: Subtree = (root.val, left_subtree, right_subtree)

        freq[curr_subtree] = freq.get(curr_subtree, 0) + 1

        if freq[curr_subtree] == 2:
            ans.append(root)

        return curr_subtree

    dfs(root)

    return ans


def mergeTwoBST(r1: TreeNode | None, r2: TreeNode | None) -> list[int]:
    """Merge BST values in sorted order, preserving duplicates.

    Input (level order): r1=[3,1,5], r2=[4,2,6]. Output: [1,2,3,4,5,6].
    O(m+n) time and space including traversal arrays and output.
    """
    a: list[int]
    b: list[int]
    a, b = inorder(r1), inorder(r2)
    result: list[int] = []
    i: int
    j: int
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    return result + a[i:] + b[j:]
