# PIP -> NLR, LNR, LRN

from collections import deque
from typing import Optional, Tuple, List


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


def inorder(root: Optional[TreeNode]) -> None:
    """
    Input: root = [1, None, 2, 3]
    Output: Prints: 1, 3, 2
    """
    if root is None:
        return

    inorder(root.left)
    print(root.val)
    inorder(root.right)


def levelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Input: root = [3, 9, 20, None, None, 15, 7]
    Output: [[3], [9, 20], [15, 7]]
    """
    if root is None:
        return []

    ans = []

    queue = deque([root])

    while queue:
        level = []

        for i in range(len(queue)):
            node = queue.popleft()

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

        leftHeight, leftDiameter = dfs(root.left)
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

    def dfs(root: Optional[TreeNode], left: int, right: int) -> bool:
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
        return lowestCommonAncestorBST(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lowestCommonAncestorBST(root.right, p, q)
    return root


def lowestCommonAncestorBT(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Input: root = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], p = 5, q = 1
    Output: 3
    """
    if root == p or root == q:
        return root

    left = lowestCommonAncestorBT(root.left, p, q)
    right = lowestCommonAncestorBT(root.right, p, q)

    if left and right:
        return root

    return left if left else right


def binaryTreePaths(root: Optional[TreeNode]) -> List[str]:
    """
    Input: root = [1, 2, 3, None, 5]
    Output: ["1->2->5", "1->3"]
    """
    ans = []

    def dfs(root: Optional[TreeNode], curr: List[int]) -> None:
        if root is None:
            return

        curr += [root.val]

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
    ans = []

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

    rootValue = preorder[0]
    root = TreeNode(rootValue)

    mid = inorder.index(rootValue)

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

    rootValue = postorder[-1]
    root = TreeNode(rootValue)

    mid = inorder.index(rootValue)

    root.left = constructInorderPostorder(inorder[:mid], postorder[:mid])
    root.right = constructInorderPostorder(inorder[mid + 1 :], postorder[mid:-1])

    return root


# TODO
def constructFromPreorderAndPostorder(
    preorder: List[int], postorder: List[int]
) -> Optional[TreeNode]:
    """
    Input: preorder = [1, 2, 4, 5, 3, 6, 7], postorder = [4, 5, 2, 6, 7, 3, 1]
    Output: [1, 2, 3, 4, 5, 6, 7]
    """
    pass


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
        preorderList = data.split(",")
        i = 0

        def dfs() -> Optional[TreeNode]:
            nonlocal i

            value = preorderList[i]
            i += 1

            if value == "None":
                return None

            root = TreeNode(int(value))

            root.left = dfs()
            root.right = dfs()

            return root

        return dfs()


# TODO
def distanceK(root: TreeNode, target: TreeNode, k: int) -> List[int]:
    """
    Input: root = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], target = 5, k = 2
    Output: [7, 4, 1]
    """
    parent = {}

    def dfs(node):
        if not node:
            return

        if node.left:
            parent[node.left] = node

        if node.right:
            parent[node.right] = node

        dfs(node.left)
        dfs(node.right)

    dfs(root)

    queue = deque([target])
    visited = {target}
    distance = 0

    while queue:
        if distance == k:
            return [node.val for node in queue]

        for _ in range(len(queue)):
            node = queue.popleft()

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
    ans = float("-inf")

    def dfs(root: Optional[TreeNode]) -> int:
        nonlocal ans

        if root is None:
            return 0

        left = max(dfs(root.left), 0)
        right = max(dfs(root.right), 0)

        ans = max(ans, left + right + root.val)

        return max(left, right, 0) + root.val

    dfs(root)

    return ans


def findDuplicateSubtrees(root: TreeNode | None) -> list[TreeNode | None]:
    """
    Input: root = [1, 2, 3, 4, None, 2, 4, None, None, 4]
    Output: [2, 4]
    """

    ans = []

    freq = {}

    def dfs(root: TreeNode | None) -> tuple | None:
        if root is None:
            return None

        left_subtree = dfs(root.left)
        right_subtree = dfs(root.right)

        curr_subtree = (root.val, left_subtree, right_subtree)

        freq[curr_subtree] = freq.get(curr_subtree, 0) + 1

        if freq[curr_subtree] == 2:
            ans.append(root)

        return curr_subtree

    dfs(root)

    return ans


def mergeTwoBST(r1: TreeNode | None, r2: TreeNode | None) -> list[int]:
    """
    Input: r1 = [1, 3, 5], r2 = [2, 4, 6]
    Output: [1, 2, 3, 4, 5, 6]
    """
    arr1: list[int] = []
    arr2: list[int] = []

    inorder(r1, arr1)
    inorder(r2, arr2)

    # merge_two_sorted_arrays(arr1, arr2)

    return arr1 + arr2
