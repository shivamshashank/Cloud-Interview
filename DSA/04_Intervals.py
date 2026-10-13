import heapq
from typing import List, Tuple


class Interval:
    def __init__(self, start: int = 0, end: int = 0) -> None:
        self.start: int = start
        self.end: int = end


def mergeIntervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Input: intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    Output: [[1, 6], [8, 10], [15, 18]]
    """
    intervals.sort(key=lambda x: x[0])

    ans: List[List[int]] = []

    for interval in intervals:
        if len(ans) == 0 or ans[-1][1] < interval[0]:
            ans.append(interval)
        else:
            ans[-1][1] = max(ans[-1][1], interval[1])

    return ans


def eraseOverlapIntervals(intervals: List[List[int]]) -> int:
    """
    Input: intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
    Output: 1
    """
    intervals.sort(key=lambda x: x[0])
    if not intervals:
        return 0
    ans: int = 0
    prevEnd: int = intervals[0][1]

    for start, end in intervals[1:]:
        if start >= prevEnd:
            prevEnd = end
        else:
            ans += 1
            prevEnd = min(prevEnd, end)

    return ans


def insertInterval(
    intervals: List[List[int]], newInterval: List[int]
) -> List[List[int]]:
    """
    Input: intervals = [[1, 3], [6, 9]], newInterval = [2, 5]
    Output: [[1, 5], [6, 9]]
    """
    ans: List[List[int]] = []

    for i, interval in enumerate(intervals):
        if newInterval[1] < interval[0]:
            ans.append(newInterval)
            return ans + intervals[i:]
        elif newInterval[0] > interval[1]:
            ans.append(interval)
        else:
            newInterval = [
                min(interval[0], newInterval[0]),
                max(interval[1], newInterval[1]),
            ]

    ans.append(newInterval)

    return ans


def minMeetingRooms(intervals: List[List[int]]) -> int:
    """
    Input: intervals = [[0, 30], [5, 10], [15, 20]]
    Output: 2
    """
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])
    heap: List[int] = []  # Min-heap of end times

    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)

    return len(heap)


def employeeFreeTime(schedule: List[List[List[int]]]) -> List[List[int]]:
    """
    Input: schedule = [[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]]
    Output: [[3, 4]]
    """
    all_intervals: List[Tuple[int, int]] = []
    for emp in schedule:
        for interval in emp:
            if isinstance(interval, Interval):
                all_intervals.append((interval.start, interval.end))
            else:
                all_intervals.append((interval[0], interval[1]))

    if not all_intervals:
        return []
    all_intervals.sort(key=lambda x: x[0])

    ans: List[List[int]] = []
    prev_end: int = all_intervals[0][1]

    for start, end in all_intervals[1:]:
        if start > prev_end:
            # Common free time gap detected
            ans.append([prev_end, start])
            prev_end = end
        else:
            prev_end = max(prev_end, end)

    return ans
