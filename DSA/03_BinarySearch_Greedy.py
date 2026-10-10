from typing import Dict, List


def binarySearch(nums: List[int], target: int) -> int:
    """
    Input: nums = [-1, 0, 3, 5, 9, 12], target = 9
    Output: 4
    """
    s, e = 0, len(nums) - 1

    while s <= e:
        mid = s + (e - s) // 2

        if nums[mid] > target:
            e = mid - 1
        elif nums[mid] < target:
            s = mid + 1
        else:
            return mid

    return -1


def searchRange(nums: List[int], target: int) -> List[int]:
    """
    Input: nums = [5, 7, 7, 8, 8, 10], target = 8
    Output: [3, 4]
    """

    def binarySearch(position: str) -> int:
        s, e = 0, len(nums) - 1
        index = -1

        while s <= e:
            mid = s + (e - s) // 2

            if nums[mid] > target:
                e = mid - 1
            elif nums[mid] < target:
                s = mid + 1
            else:
                index = mid

                if position == "first":
                    e = mid - 1
                else:
                    s = mid + 1

        return index

    return [binarySearch("first"), binarySearch("last")]


def minEatingSpeed(piles: List[int], h: int) -> int:
    """
    Input: piles = [3, 6, 7, 11], h = 8
    Output: 4
    """
    s = 1
    e = max(piles)

    while s <= e:
        mid = s + (e - s) // 2

        hours = 0

        for p in piles:
            hours += p // mid
            if p % mid > 0:
                hours += 1

        if hours > h:
            s = mid + 1
        else:
            e = mid - 1

    return s


def searchInRotatedSortedArray(nums: List[int], target: int) -> int:
    """
    Input: nums = [4, 5, 6, 7, 0, 1, 2], target = 0
    Output: 4
    """
    s, e = 0, len(nums) - 1

    while s <= e:
        mid = s + (e - s) // 2

        if nums[mid] == target:
            return mid

        # Left half is sorted
        if nums[s] <= nums[mid]:
            if nums[s] <= target < nums[mid]:
                e = mid - 1
            else:
                s = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[e]:
                s = mid + 1
            else:
                e = mid - 1

    return -1


def findPeakElement(nums: List[int]) -> int:
    """
    Input: nums = [1, 2, 3, 1]
    Output: 2
    """
    s, e = 0, len(nums) - 1

    while s <= e:
        mid = s + (e - s) // 2

        if (mid == 0 or nums[mid] > nums[mid - 1]) and (
            mid == len(nums) - 1 or nums[mid] > nums[mid + 1]
        ):
            return mid
        elif mid > 0 and nums[mid - 1] > nums[mid]:
            e = mid - 1
        else:
            s = mid + 1

    return -1


def searchMatrix(matrix: List[List[int]], target: int) -> bool:
    """
    Input: matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], target = 3
    Output: True
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    s, e = 0, m * n - 1

    while s <= e:
        mid = s + (e - s) // 2
        mid_val = matrix[mid // n][mid % n]

        if mid_val == target:
            return True
        elif mid_val < target:
            s = mid + 1
        else:
            e = mid - 1

    return False


def searchMatrixII(matrix: List[List[int]], target: int) -> bool:
    """
    Input: matrix = [[1, 4, 7, 11, 15],
                     [2, 5, 8, 12, 19],
                     [3, 6, 9, 16, 22],
                     [10, 13, 14, 17, 24],
                     [18, 21, 23, 26, 30]], target = 5
    Output: True
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    r, c = 0, n - 1

    while r < m and c >= 0:
        if matrix[r][c] == target:
            return True
        elif matrix[r][c] > target:
            c -= 1
        else:
            r += 1

    return False


def canJump(nums: List[int]) -> bool:
    """
    Input: nums = [2, 3, 1, 1, 4]
    Output: True
    """
    max_reach = 0
    for i, num in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + num)
    return True


def jump(nums: List[int]) -> int:
    """
    Input: nums = [2, 3, 1, 1, 4]
    Output: 2
    """
    jumps = 0
    curr_end = 0
    farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == curr_end:
            jumps += 1
            curr_end = farthest

    return jumps


def leastInterval(tasks: List[str], n: int) -> int:
    """
    Input: tasks = ["A", "A", "A", "B", "B", "B"], n = 2
    Output: 8
    """
    freq: Dict[str, int] = {}
    for task in tasks:
        freq[task] = freq.get(task, 0) + 1
    max_freq: int = max(freq.values())
    max_freq_count: int = sum(1 for count in freq.values() if count == max_freq)

    return max(len(tasks), (max_freq - 1) * (n + 1) + max_freq_count)


def canCompleteCircuit(gas: List[int], cost: List[int]) -> int:
    """
    Input: gas = [1, 2, 3, 4, 5], cost = [3, 4, 5, 1, 2]
    Output: 3
    """
    if sum(gas) < sum(cost):
        return -1

    curr_tank = 0
    start_index = 0

    for i in range(len(gas)):
        curr_tank += gas[i] - cost[i]
        if curr_tank < 0:
            start_index = i + 1
            curr_tank = 0

    return start_index
