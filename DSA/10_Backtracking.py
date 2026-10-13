from collections import Counter
from typing import List


def subsets(nums: List[int]) -> List[List[int]]:
    """
    Input: nums = [1, 2, 3]
    Output: [[1, 2, 3], [1, 2], [1, 3], [1], [2, 3], [2], [3], []]
    """
    ans: list[list[int]] = []

    def dfs(i: int, curr: List[int]) -> None:
        if i == len(nums):
            ans.append(curr)
            return

        dfs(i + 1, curr + [nums[i]])
        dfs(i + 1, curr)

    dfs(0, [])

    return ans


def subsetsWithDup(nums: List[int]) -> List[List[int]]:
    """
    Input: nums = [1, 2, 2]
    Output: [[1, 2, 2], [1, 2], [1], [2, 2], [2], []]
    """
    nums.sort()
    ans: list[list[int]] = []

    def dfs(i: int, curr: List[int]) -> None:
        if i == len(nums):
            ans.append(curr)
            return

        dfs(i + 1, curr + [nums[i]])

        while i < len(nums) - 1 and nums[i] == nums[i + 1]:
            i += 1

        dfs(i + 1, curr)

    dfs(0, [])

    return ans


def permute(nums: List[int]) -> List[List[int]]:
    """
    Input: nums = [1, 2, 3]
    Output: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """
    ans: list[list[int]] = []

    def dfs(curr: List[int]) -> None:
        if len(curr) == len(nums):
            ans.append(curr)
            return

        for num in nums:
            if num not in curr:
                dfs(curr + [num])

    dfs([])

    return ans


def permuteUnique(nums: List[int]) -> List[List[int]]:
    """
    Input: nums = [1, 1, 2]
    Output: [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    """
    ans: list[list[int]] = []

    freq: Counter[int] = Counter(nums)

    def dfs(curr: List[int]) -> None:
        if len(curr) == len(nums):
            ans.append(curr)
            return

        for num, count in freq.items():
            if count > 0:
                freq[num] -= 1
                dfs(curr + [num])
                freq[num] += 1

    dfs([])

    return ans


def combinations(n: int, k: int) -> List[List[int]]:
    """
    Input: n = 4, k = 2
    Output: [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    """
    ans: list[list[int]] = []

    def dfs(i: int, curr: List[int]) -> None:
        if len(curr) == k:
            ans.append(curr)
            return

        for j in range(i, n + 1):
            dfs(j + 1, curr + [j])

    dfs(1, [])

    return ans


def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    """
    Input: candidates = [2, 3, 6, 7], target = 7
    Output: [[2, 2, 3], [7]]
    """
    ans: list[list[int]] = []

    def dfs(i: int, curr: List[int], total: int) -> None:
        if total > target or i == len(candidates):
            if total == target:
                ans.append(curr)
            return

        dfs(i, curr + [candidates[i]], total + candidates[i])  # Take again allowed

        dfs(i + 1, curr, total)  # Skip

    dfs(0, [], 0)

    return ans


def combinationSumII(candidates: List[int], target: int) -> List[List[int]]:
    """
    Input: candidates = [10, 1, 2, 7, 6, 1, 5], target = 8
    Output: [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    """
    candidates.sort()
    ans: list[list[int]] = []

    def dfs(i: int, curr: List[int], total: int) -> None:
        if total > target or i == len(candidates):
            if total == target:
                ans.append(curr)
            return

        dfs(i + 1, curr + [candidates[i]], total + candidates[i])  # Take

        # Duplicates
        while i < len(candidates) - 1 and candidates[i] == candidates[i + 1]:
            i += 1

        dfs(i + 1, curr, total)  # Skip

    dfs(0, [], 0)

    return ans


def generatePartitions(s: str) -> List[List[str]]:
    """
    Input: s = "aab"
    Output: [["a", "a", "b"], ["aa", "b"]]
    """
    ans: list[list[str]] = []

    def dfs(i: int, curr: List[str]) -> None:
        if i == len(s):
            ans.append(curr)
            return

        for j in range(i + 1, len(s) + 1):
            word: str = s[i:j]

            if word == word[::-1]:  # Palindrome check
                dfs(j, curr + [word])

    dfs(0, [])

    return ans


def wordBreak(s: str, wordDict: List[str]) -> bool:
    """LC 139. Input: "leetcode", ["leet", "code"]. Output: True.

    Bottom-up reachability avoids exponential repeated suffix exploration.
    O(n * L^2) worst-case time with Python slicing, O(n + dictionary) space;
    L is the longest dictionary word length.
    """
    words: set[str] = set(wordDict)
    max_length: int = max(map(len, words), default=0)
    possible: list[bool] = [True] + [False] * len(s)
    for end in range(1, len(s) + 1):
        for start in range(max(0, end - max_length), end):
            if possible[start] and s[start:end] in words:
                possible[end] = True
                break
    return possible[-1]


def exist(board: List[List[str]], word: str) -> bool:
    """
    Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
    Output: True
    """
    if not word:
        return True
    if not board or not board[0]:
        return False
    rows: int
    cols: int
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True

        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or board[r][c] != word[idx]
        ):
            return False

        # Mark cell as visited
        temp: str = board[r][c]
        board[r][c] = "#"

        found: bool = (
            dfs(r + 1, c, idx + 1)
            or dfs(r - 1, c, idx + 1)
            or dfs(r, c + 1, idx + 1)
            or dfs(r, c - 1, idx + 1)
        )

        # Backtrack
        board[r][c] = temp
        return found

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0] and dfs(r, c, 0):
                return True

    return False
