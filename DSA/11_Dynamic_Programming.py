from typing import List


def climbStairs(n: int) -> int:
    """
    Input: n = 3
    Output: 3
    """
    memo = {}

    def dfs(i: int) -> int:
        if i < 3:
            return i

        if i in memo:
            return memo[i]

        memo[i] = dfs(i - 1) + dfs(i - 2)

        return memo[i]

    return dfs(n)


def houseRobberI(nums: List[int]) -> int:
    """
    Input: nums = [1, 2, 3, 1]
    Output: 4
    """
    n = len(nums)

    if n == 1:
        return nums[0]

    memo = {0: nums[0], 1: max(nums[0], nums[1])}

    def dfs(i: int) -> int:
        if i in memo:
            return memo[i]

        memo[i] = max(dfs(i - 2) + nums[i], dfs(i - 1))

        return memo[i]

    return dfs(n - 1)


def houseRobberII(nums: List[int]) -> int:
    """
    Input: nums = [2, 3, 2]
    Output: 3
    """
    if len(nums) == 1:
        return nums[0]

    return max(houseRobberI(nums[1:]), houseRobberI(nums[:-1]))


def uniquePaths(self, m: int, n: int) -> int:
    """
    Input: m = 3, n = 7
    Output: 28
    """
    memo = {}

    def dfs(i: int, j: int) -> int:
        if i == m - 1 or j == n - 1:
            return 1

        if (i, j) in memo:
            return memo[(i, j)]

        memo[(i, j)] = dfs(i + 1, j) + dfs(i, j + 1)

        return memo[(i, j)]

    return dfs(0, 0)


def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
    """
    Input: obstacleGrid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    Output: 2
    """
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    memo = {}

    def dfs(i: int, j: int) -> int:
        if i >= m or j >= n or obstacleGrid[i][j] == 1:
            return 0

        if i == m - 1 and j == n - 1:
            return 1

        if (i, j) in memo:
            return memo[(i, j)]

        memo[(i, j)] = dfs(i + 1, j) + dfs(i, j + 1)

        return memo[(i, j)]

    return dfs(0, 0)


def minPathSum(self, grid: List[List[int]]) -> int:
    """
    Input: grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    Output: 7
    """
    m, n = len(grid), len(grid[0])
    memo = {}

    def dfs(i: int, j: int) -> None:
        if i >= m or j >= n:
            return float("inf")

        if i == m - 1 and j == n - 1:
            return grid[i][j]

        if (i, j) in memo:
            return memo[(i, j)]

        memo[(i, j)] = grid[i][j] + min(dfs(i + 1, j), dfs(i, j + 1))

        return memo[(i, j)]

    return dfs(0, 0)


def minimumTotal(self, triangle: List[List[int]]) -> int:
    """
    Input: triangle = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
    Output: 11
    """
    n = len(triangle)

    memo = {}

    def dfs(i: int, j: int) -> int:
        if i == n - 1:
            return triangle[i][j]

        if (i, j) in memo:
            return memo[(i, j)]

        memo[(i, j)] = triangle[i][j] + min(dfs(i + 1, j), dfs(i + 1, j + 1))

        return memo[(i, j)]

    return dfs(0, 0)


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

    rows, cols = len(matrix), len(matrix[0])
    dp = [[0] * (cols + 1) for _ in range(rows + 1)]
    max_side = 0

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


def findTargetSumWays(self, nums: List[int], target: int) -> int:
    """
    Input: nums = [1, 1, 1, 1, 1], target = 3
    Output: 5
    """
    n = len(nums)

    memo = {}

    def dfs(i: int, total: int) -> None:
        if i == n:
            if total == target:
                return 1
            return 0

        if (i, total) in memo:
            return memo[(i, total)]

        memo[(i, total)] = dfs(i + 1, total + nums[i]) + dfs(i + 1, total - nums[i])

        return memo[(i, total)]

    return dfs(0, 0)


def canPartition(self, nums: List[int]) -> bool:
    """
    Input: nums = [1, 5, 11, 5]
    Output: True
    """
    n = len(nums)
    total = sum(nums)

    if total % 2 != 0:
        return False

    memo = {}

    def dfs(i: int, curr: int) -> bool:
        if i == n or 2 * curr > total:
            return False

        if 2 * curr == total:
            return True

        if (i, curr) in memo:
            return memo[(i, curr)]

        memo[(i, curr)] = dfs(i + 1, curr) or dfs(i + 1, curr + nums[i])

        return memo[(i, curr)]

    return dfs(0, 0)


def lengthOfLIS(self, nums: List[int]) -> int:
    """
    Input: nums = [10, 9, 2, 5, 3, 7, 101, 18]
    Output: 4
    """
    n = len(nums)
    memo = {}

    def dfs(i: int, prev: int) -> int:
        if i == n:
            return 0

        if (i, prev) in memo:
            return memo[(i, prev)]

        skip = dfs(i + 1, prev)

        take = 0

        if prev == -1 or nums[i] > nums[prev]:  # Take
            take = 1 + dfs(i + 1, i)

        memo[(i, prev)] = max(skip, take)

        return memo[(i, prev)]

    return dfs(0, -1)


def coinChange(coins: List[int], amount: int) -> int:
    """
    Input: coins = [1, 2, 5], amount = 11
    Output: 3
    """
    memo = {}

    def dfs(amount: int) -> int:
        if amount == 0:
            return 0

        if amount < 0:
            return float("inf")

        ans = float("inf")

        for coin in coins:
            if (amount - coin) not in memo:
                memo[amount - coin] = 1 + dfs(amount - coin)

            ans = min(ans, memo[amount - coin])

        return ans

    ans = dfs(amount)

    return -1 if ans == float("inf") else ans


def mincostTickets(days: List[int], costs: List[int]) -> int:
    """
    Input: days = [1, 4, 6, 7, 8, 20], costs = [2, 7, 15]
    Output: 11
    """

    def dfs(i: int) -> int:
        if i >= len(days):
            return 0

        ans = float("inf")

        for duration, cost in [(1, costs[0]), (7, costs[1]), (30, costs[2])]:
            j = i

            while j < len(days) and days[j] < days[i] + duration:
                j += 1

            ans = min(ans, cost + dfs(j))

        return ans

    return dfs(0)


def maximumAmount(arr: list[int]) -> int:
    """
    Input: arr = [5, 3, 7, 10]
    Output: 15
    """

    def dfs(arr: list[int], turn: str) -> int:
        if len(arr) == 0:
            return 0

        if turn == "first":
            take_left = arr[0] + dfs(arr[1:], "second")
            take_right = arr[-1] + dfs(arr[:-1], "second")
            return max(take_left, take_right)
        else:
            opp_take_left = dfs(arr[1:], "first")
            opp_take_right = dfs(arr[:-1], "first")
            return min(opp_take_left, opp_take_right)

    return dfs(arr, "first")
