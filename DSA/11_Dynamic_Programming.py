from typing import List


def climbStairs(n: int) -> int:
    """
    Input: n = 3
    Output: 3
    O(n) time, O(1) space; zero steps has one empty way.
    """
    previous: int
    current: int
    previous, current = 1, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


def houseRobberI(nums: List[int]) -> int:
    """
    Input: nums = [1, 2, 3, 1]
    Output: 4
    O(n) time, O(1) space; empty input returns 0.
    """
    two_back: int
    one_back: int
    two_back = one_back = 0
    for value in nums:
        two_back, one_back = one_back, max(one_back, two_back + value)
    return one_back


def houseRobberII(nums: List[int]) -> int:
    """
    Input: nums = [2, 3, 2]
    Output: 3
    """
    if len(nums) == 1:
        return nums[0]

    return max(houseRobberI(nums[1:]), houseRobberI(nums[:-1]))


def uniquePaths(m: int, n: int) -> int:
    """
    Input: m = 3, n = 7
    Output: 28
    O(m*n) time, O(n) space.
    """
    if m <= 0 or n <= 0:
        return 0
    dp: list[int] = [1] * n
    for _ in range(1, m):
        for col in range(1, n):
            dp[col] += dp[col - 1]
    return dp[-1]


def uniquePathsWithObstacles(obstacleGrid: List[List[int]]) -> int:
    """
    Input: obstacleGrid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    Output: 2
    O(rows*cols) time, O(cols) space.
    """
    if not obstacleGrid or not obstacleGrid[0]:
        return 0
    dp: list[int] = [0] * len(obstacleGrid[0])
    dp[0] = 1
    for row in obstacleGrid:
        for col, blocked in enumerate(row):
            if blocked:
                dp[col] = 0
            elif col:
                dp[col] += dp[col - 1]
    return dp[-1]


def minPathSum(grid: List[List[int]]) -> int:
    """
    Input: grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    Output: 7
    O(rows*cols) time, O(cols) space; leaves input unchanged.
    """
    if not grid or not grid[0]:
        return 0
    dp: list[int] = [0] * len(grid[0])
    for row_index, row in enumerate(grid):
        for col, value in enumerate(row):
            if col == 0:
                dp[col] += value
            elif row_index == 0:
                dp[col] = dp[col - 1] + value
            else:
                dp[col] = value + min(dp[col], dp[col - 1])
    return dp[-1]


def minimumTotal(triangle: List[List[int]]) -> int:
    """
    Input: triangle = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
    Output: 11
    O(n^2) time, O(n) space for n rows.
    """
    if not triangle:
        return 0
    dp: list[int] = triangle[-1][:]
    for row in reversed(triangle[:-1]):
        for col, value in enumerate(row):
            dp[col] = value + min(dp[col], dp[col + 1])
    return dp[0]


def maximalSquare(matrix: List[List[str]]) -> int:
    """
    Input: matrix = [["1","0","1","0","0"],
                     ["1","0","1","1","1"],
                     ["1","1","1","1","1"],
                     ["1","0","0","1","0"]]
    Output: 4
    """
    if not matrix or not matrix[0]:
        return 0

    rows: int
    cols: int
    rows, cols = len(matrix), len(matrix[0])
    dp: list[list[int]] = [[0] * (cols + 1) for _ in range(rows + 1)]
    max_side: int = 0

    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == "1":
                dp[r + 1][c + 1] = 1 + min(
                    dp[r][c + 1],      # top
                    dp[r + 1][c],      # left
                    dp[r][c],          # top-left diagonal
                )
                max_side = max(max_side, dp[r + 1][c + 1])

    return max_side * max_side


def findTargetSumWays(nums: List[int], target: int) -> int:
    """
    Input: nums = [1, 1, 1, 1, 1], target = 3
    Output: 5
    Counts both choices for zero. O(n*S) time, O(S) space for S reachable sums.
    """
    counts: dict[int, int] = {0: 1}
    for value in nums:
        next_counts: dict[int, int] = {}
        for total, count in counts.items():
            for candidate in (total + value, total - value):
                next_counts[candidate] = next_counts.get(candidate, 0) + count
        counts = next_counts
    return counts.get(target, 0)


def canPartition(nums: List[int]) -> bool:
    """
    Input: nums = [1, 5, 11, 5]
    Output: True
    Nonnegative values; O(n*target) time, O(target) space.
    """
    total: int = sum(nums)
    if total % 2:
        return False
    target: int = total // 2
    possible: list[bool] = [False] * (target + 1)
    possible[0] = True
    for value in nums:
        for subtotal in range(target, value - 1, -1):
            possible[subtotal] = possible[subtotal] or possible[subtotal - value]
    return possible[target]


def lengthOfLIS(nums: List[int]) -> int:
    """
    Input: nums = [10, 9, 2, 5, 3, 7, 101, 18]
    Output: 4
    O(n log n) time, O(n) space; strictly increasing subsequence.
    """
    from bisect import bisect_left

    tails: list[int] = []
    for value in nums:
        index: int = bisect_left(tails, value)
        if index == len(tails):
            tails.append(value)
        else:
            tails[index] = value
    return len(tails)


def coinChange(coins: List[int], amount: int) -> int:
    """
    Input: coins = [1, 2, 5], amount = 11
    Output: 3
    O(amount * len(coins)) time, O(amount) space; avoids recursion depth failures.
    """
    if amount < 0 or any(coin <= 0 for coin in coins):
        raise ValueError("amount must be nonnegative and coins positive")
    dp: list[int] = [0] + [amount + 1] * amount
    for subtotal in range(1, amount + 1):
        for coin in coins:
            if coin <= subtotal:
                dp[subtotal] = min(dp[subtotal], 1 + dp[subtotal - coin])
    return dp[amount] if dp[amount] <= amount else -1


def mincostTickets(days: List[int], costs: List[int]) -> int:
    """
    Input: days = [1, 4, 6, 7, 8, 20], costs = [2, 7, 15]
    Output: 11
    Days are strictly increasing; costs has three entries. O(n log n) time, O(n) space.
    """
    from bisect import bisect_left

    dp: list[int] = [0] * (len(days) + 1)
    for i in range(len(days) - 1, -1, -1):
        dp[i] = min(cost + dp[bisect_left(days, days[i] + duration)]
                    for duration, cost in zip((1, 7, 30), costs))
    return dp[0]


def maximumAmount(arr: list[int]) -> int:
    """
    Input: arr = [5, 3, 7, 10]
    Output: 15
    Optimal play from either end; O(n^2) time and space.
    """
    n: int = len(arr)
    if not n:
        return 0
    # dp[i][j] is the best score difference the current player can secure.
    dp: list[list[int]] = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = arr[i]
        for j in range(i + 1, n):
            dp[i][j] = max(arr[i] - dp[i + 1][j], arr[j] - dp[i][j - 1])
    return (sum(arr) + dp[0][-1]) // 2
