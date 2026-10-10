from typing import List


def productExceptSelf(nums: List[int]) -> List[int]:
    """
    Input: nums = [1, 2, 3, 4]
    Output: [24, 12, 8, 6]
    """
    n = len(nums)
    ans = [1] * n

    for i in range(n - 1):
        ans[i + 1] = ans[i] * nums[i]

    right = 1

    for i in range(n - 1, -1, -1):
        ans[i] *= right
        right *= nums[i]

    return ans


def twoSum(nums: List[int], target: int) -> List[int]:
    """
    Input: nums = [2, 7, 11, 15], target = 9
    Output: [0, 1]
    """
    seen = {}

    for i, num in enumerate(nums):
        if target - num in seen:
            return [i, seen[target - num]]

        seen[num] = i

    return []


def containsDuplicate(nums: List[int]) -> bool:
    """
    Input: nums = [1, 2, 3, 1]
    Output: True
    """
    return len(set(nums)) != len(nums)


class NumArray:
    """
    Input: ["NumArray", "sumRange"], [[[-2, 0, 3, -5, 2, -1]], [0, 2]]
    Output: [None, 1]
    """

    def __init__(self, nums: List[int]):
        self.prefix = {-1: 0}

        for i, num in enumerate(nums):
            self.prefix[i] = self.prefix[i - 1] + num

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right] - self.prefix[left - 1]


def subArraySum(nums: List[int], k: int) -> int:
    """
    Input: nums = [1, 1, 1], k = 2
    Output: 2
    """
    freq = {0: 1}  # stores prefix sum : frequency
    curr = 0
    count = 0
    for num in nums:
        curr += num
        freq[curr] = freq.get(curr, 0) + 1
        count += freq.get(curr - k, 0)
    return count


def checkSubarraySum(nums: List[int], k: int) -> bool:
    """
    Input: nums = [23, 2, 4, 6, 7], k = 6
    Output: True
    """
    prefixSum = {0: -1}  # stores remainder : index
    curr = 0

    for i, num in enumerate(nums):
        curr += num
        remainder = curr % k
        if remainder in prefixSum:
            if i - prefixSum[remainder] > 1:
                return True
        else:
            prefixSum[remainder] = i

    return False


def maxSubArray(nums: List[int]) -> int:
    """
    Input: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    Output: 6
    """
    max_sum: float = float("-inf")
    curr_sum: int = 0

    for num in nums:
        curr_sum += num
        max_sum = max(max_sum, curr_sum)

        if curr_sum < 0:
            curr_sum = 0

    return int(max_sum)


def dailyTemperatures(temperatures: List[int]) -> List[int]:
    """
    Input: temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
    Output: [1, 1, 4, 2, 1, 1, 0, 0]
    """
    n = len(temperatures)
    ans: List[int] = [0] * n
    stack: List[int] = []

    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev = stack.pop()
            ans[prev] = i - prev

        stack.append(i)

    return ans


def largestRectangleArea(heights: List[int]) -> int:
    """
    Input: heights = [2, 1, 5, 6, 2, 3]
    Output: 10
    """
    stack: List[tuple[int, int]] = []  # (start_index, height)
    max_area: int = 0

    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))

    n = len(heights)
    for idx, height in stack:
        max_area = max(max_area, height * (n - idx))

    return max_area


def setZeroes(matrix: List[List[int]]) -> None:
    """
    Input: matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    Output: [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    """
    rows: set[int] = set()
    cols: set[int] = set()
    m, n = len(matrix), len(matrix[0])

    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 0:
                rows.add(i)
                cols.add(j)

    for i in range(m):
        for j in range(n):
            if i in rows or j in cols:
                matrix[i][j] = 0


def moveZeroes(nums: List[int]) -> None:
    """
    Input: nums = [0, 1, 0, 3, 12]
    Output: [1, 3, 12, 0, 0]
    """
    write = 0

    for read, num in enumerate(nums):
        if num != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1


class EncodeDecodeStrings:
    """
    Input: strs = ["lint", "code", "love", "you"]
    Output: ["lint", "code", "love", "you"]
    """

    def encode(self, strs: List[str]) -> str:
        ans = ""
        for s in strs:
            ans += f"{len(s)}#{s}"
        return ans

    def decode(self, s: str) -> List[str]:
        ans: list[str] = []
        length = ""
        i = 0

        while True:
            if i == len(s):
                return ans

            if s[i] == "#":
                ans.append(s[i + 1 : i + 1 + int(length)])
                i = i + 1 + int(length)
                length = ""
            else:
                length += s[i]
                i += 1


def longestConsecutive(nums: List[int]) -> int:
    """
    Input: nums = [100, 4, 200, 1, 3, 2]
    Output: 4
    """
    num_set: set[int] = set(nums)

    ans: int = 0

    for num in nums:
        if num - 1 not in num_set:
            curr: int = 1

            while num + curr in num_set:
                curr += 1

            ans = max(ans, curr)

    return ans


def largestNumber(nums: List[int]) -> str:
    """
    Input: nums = [10, 2]
    Output: "210"
    """
    n = len(nums)

    for i in range(n - 1):
        for j in range(i + 1, n):
            a = str(nums[i])
            b = str(nums[j])

            if a + b < b + a:
                nums[i], nums[j] = nums[j], nums[i]

    if nums[0] == 0:
        return "0"

    return "".join(map(str, nums))


def firstMissingPositive(nums: List[int]) -> int:
    """
    Input: nums = [1, 2, 0]
    Output: 3
    """
    n = len(nums)

    # Loop 1: Remove numbers that cannot be the answer
    for i in range(n):
        if nums[i] <= 0 or nums[i] > n:
            nums[i] = n + 1

    # Loop 2: Mark every positive number that exists
    for i in range(n):
        num = abs(nums[i])

        if 1 <= num <= n:
            index = num - 1
            nums[index] = -abs(nums[index])

    # Loop 3: Find the first number that was not marked
    for i in range(n):
        if nums[i] > 0:
            return i + 1

    return n + 1


def maxIndexDiff(arr: list[int]) -> int:
    """
    Input: arr = [34, 8, 10, 3, 2, 80, 30, 33, 1]
    Output: 6
    Explanation: The maximum value of j - i such that arr[i] <= arr[j] is 6.
                 j = 7, i = 1  (arr[1] = 8, arr[7] = 33)
                 j = 8, i = 0  (arr[0] = 34, arr[8] = 1)
    """
    n = len(arr)

    leftMin = [0] * n
    rightMax = [0] * n

    leftMin[0] = arr[0]
    for i in range(1, n):
        leftMin[i] = min(arr[i], leftMin[i - 1])

    rightMax[n - 1] = arr[n - 1]
    for i in range(n - 2, -1, -1):
        rightMax[i] = max(arr[i], rightMax[i + 1])

    ans = 0
    i = 0
    j = 0

    while i < n and j < n:
        if leftMin[i] <= rightMax[j]:
            ans = max(ans, j - i)
            j += 1
        else:
            i += 1

    return ans


def spiralOrder(matrix: List[List[int]]) -> List[int]:
    """
    Input: matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]
    """
    if not matrix or not matrix[0]:
        return []

    res: list[int] = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Traverse left to right across top row
        for c in range(left, right + 1):
            res.append(matrix[top][c])
        top += 1

        # Traverse downwards along right column
        for r in range(top, bottom + 1):
            res.append(matrix[r][right])
        right -= 1

        # Traverse right to left across bottom row
        if top <= bottom:
            for c in range(right, left - 1, -1):
                res.append(matrix[bottom][c])
            bottom -= 1

        # Traverse upwards along left column
        if left <= right:
            for r in range(bottom, top - 1, -1):
                res.append(matrix[r][left])
            left += 1

    return res


def rotate(matrix: List[List[int]]) -> None:
    """
    Do not return anything, modify matrix in-place instead.
    Input: matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Output: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    """
    n = len(matrix)

    # Step 1: Transpose matrix
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()


def isValidSudoku(board: List[List[str]]) -> bool:
    """
    Input: board = [["5","3",".",".","7",".",".",".","."],
                    ["6",".",".","1","9","5",".",".","."],
                    [".","9","8",".",".",".",".","6","."],
                    ["8",".",".",".","6",".",".",".","3"],
                    ["4",".",".","8",".","3",".",".","1"],
                    ["7",".",".",".","2",".",".",".","6"],
                    [".","6",".",".",".",".","2","8","."],
                    [".",".",".","4","1","9",".",".","5"],
                    [".",".",".",".","8",".",".","7","9"]]
    Output: True
    """
    rows: list[set[str]] = [set() for _ in range(9)]
    cols: list[set[str]] = [set() for _ in range(9)]
    boxes: list[set[str]] = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == ".":
                continue

            box_idx = (r // 3) * 3 + (c // 3)

            if val in rows[r] or val in cols[c] or val in boxes[box_idx]:
                return False

            rows[r].add(val)
            cols[c].add(val)
            boxes[box_idx].add(val)

    return True


def gameOfLife(board: List[List[int]]) -> None:
    """
    Do not return anything, modify board in-place instead.
    Input: board = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    Output: [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
    """
    # State transitions:
    # 0 -> 0: 0
    # 1 -> 1: 1
    # 1 -> 0: 2 (alive -> dead)
    # 0 -> 1: 3 (dead -> alive)
    m, n = len(board), len(board[0])

    for r in range(m):
        for c in range(n):
            live_neighbors = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and board[nr][nc] in (1, 2):
                        live_neighbors += 1

            if board[r][c] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    board[r][c] = 2
            else:
                if live_neighbors == 3:
                    board[r][c] = 3

    for r in range(m):
        for c in range(n):
            if board[r][c] == 2:
                board[r][c] = 0
            elif board[r][c] == 3:
                board[r][c] = 1
