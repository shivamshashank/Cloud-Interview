from typing import List
from collections import deque, Counter


def twoSum(nums: List[int], target: int) -> List[int]:
    """
    Input: nums = [2, 7, 11, 15], target = 9
    Output: [1, 2]
    """
    n = len(nums)
    s, e = 0, n - 1

    while s <= e:
        total = nums[s] + nums[e]

        if total > target:
            e -= 1
        elif total < target:
            s += 1
        else:
            return [s + 1, e + 1]
    
    return []


def removeDuplicates(nums: List[int]) -> int:
    """
    Input: nums = [1, 1, 2]
    Output: 2
    """
    write = 0

    for i in range(1, len(nums)):
        if nums[i] != nums[write]:
            write += 1
            nums[i], nums[write] = nums[write], nums[i]

    return write + 1


def threeSum(nums: List[int]) -> List[List[int]]:
    """
    Input: nums = [-1, 0, 1, 2, -1, -4]
    Output: [[-1, -1, 2], [-1, 0, 1]]
    """
    nums.sort()
    n = len(nums)

    ans: List[List[int]] = []

    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        s, e = i + 1, n - 1

        while s < e:
            total = nums[i] + nums[s] + nums[e]

            if total > 0:
                e -= 1
            elif total < 0:
                s += 1
            else:
                ans.append([nums[i], nums[s], nums[e]])
                s += 1
                e -= 1

                while s < e and nums[s] == nums[s - 1]:
                    s += 1
                while s < e and nums[e] == nums[e + 1]:
                    e -= 1

    return ans


def fourSum(nums: List[int], target: int) -> List[List[int]]:
    """
    Input: nums = [1, 0, -1, 0, -2, 2], target = 0
    Output: [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
    """
    nums.sort()
    n = len(nums)
    
    ans: List[List[int]] = []

    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue

            s, e = j + 1, n - 1

            while s < e:
                total = nums[i] + nums[j] + nums[s] + nums[e]

                if total > target:
                    e -= 1
                elif total < target:
                    s += 1
                else:
                    ans.append([nums[i], nums[j], nums[s], nums[e]])
                    s += 1
                    e -= 1

                    while s < e and nums[s] == nums[s - 1]:
                        s += 1
                    while s < e and nums[e] == nums[e + 1]:
                        e -= 1

    return ans


def findMaxAverage(nums: List[int], k: int) -> float:
    """
    Input: nums = [1, 12, -5, -6, 50, 3], k = 4
    Output: 12.75
    """
    curr: int = sum(nums[:k])
    ans: int = curr

    for i in range(k, len(nums)):
        curr: int = curr + nums[i] - nums[i - k]
        ans: int = max(ans, curr)

    return ans / k


def lengthOfLongestSubstring(s: str) -> int:
    """
    Input: s = "abcabcbb"
    Output: 3
    """
    seen: set[str] = set()
    left: int = 0
    ans: int = 0

    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1

        seen.add(ch)
        ans: int = max(ans, right - left + 1)

    return ans


def characterReplacement(s: str, k: int) -> int:
    """
    Input: s = "ABAB", k = 2
    Output: 4
    """
    freq: List[int] = [0] * 26
    ans: int = 0
    l: int = 0

    for i, ch in enumerate(s):
        freq[ord(ch) - ord("A")] += 1

        while (i - l + 1) - max(freq) > k:
            freq[ord(s[l]) - ord("A")] -= 1
            l += 1

        ans: int = max(ans, i - l + 1)

    return ans


def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    """
    Input: nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    Output: [3, 3, 5, 5, 6, 7]
    """
    dq: deque[int] = deque()  # stores indices
    ans: List[int] = []

    for i, num in enumerate(nums):
        # 1. Maintain monotonic decreasing property
        while dq and nums[dq[-1]] <= num:
            dq.pop()

        dq.append(i)

        # 2. Evict elements that fall out of the sliding window of size k
        if dq[0] <= i - k:
            dq.popleft()

        # 3. Record maximum once the first window of size k is formed
        if i >= k - 1:
            ans.append(nums[dq[0]])

    return ans


def minWindow(s: str, t: str) -> str:
    """
    Input: s = "ADOBECODEBANC", t = "ABC"
    Output: "BANC"
    """
    if not s or not t:
        return ""

    need = Counter(t)
    missing = len(t)
    start = 0
    best_len = float("inf")
    best_range = (0, 0)

    for end, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1

        if missing == 0:
            while need[s[start]] < 0:
                need[s[start]] += 1
                start += 1

            if (end - start + 1) < best_len:
                best_len = end - start + 1
                best_range = (start, end + 1)

            # Pop one character from left to continue search
            need[s[start]] += 1
            missing += 1
            start += 1

    return s[best_range[0] : best_range[1]] if best_len != float("inf") else ""


def trap(height: List[int]) -> int:
    """
    Input: height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    Output: 6
    """
    if not height:
        return 0

    left, right = 0, len(height) - 1
    max_left, max_right = height[left], height[right]
    water = 0

    while left < right:
        if max_left <= max_right:
            left += 1
            max_left = max(max_left, height[left])
            water += max_left - height[left]
        else:
            right -= 1
            max_right = max(max_right, height[right])
            water += max_right - height[right]

    return water
