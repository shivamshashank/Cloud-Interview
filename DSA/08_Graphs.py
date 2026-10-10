from typing import Optional, List, Dict
from collections import deque, defaultdict
import heapq


def dfsOfGraph(adj):
    """
    Input: adj = [[1, 2], [0, 2], [0, 1]]
    Output: [0, 1, 2]
    """
    n = len(adj)
    visited = set()
    ans = []

    def dfs(node):
        visited.add(node)
        ans.append(node)

        # Adjacency List
        for neighbor in adj[node]:
            if neighbor not in visited:
                dfs(neighbor)

        # Adjacency Matrix
        # for neighbor in range(n):
        #     if adj[node][neighbor] == 1 and neighbor not in visited:
        #         dfs(neighbor)

    dfs(0)

    return ans


def bfsOfGraph(adj):
    """
    Input: adj = [[1, 2], [0, 2], [0, 1]]
    Output: [0, 1, 2]
    """
    n = len(adj)
    visited = {0}
    ans = []

    queue = deque([0])

    while queue:
        node = queue.popleft()
        ans.append(node)

        # Adjacency List
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

        # Adjacency Matrix
        # for neighbor in range(n):
        #     if adj[node][neighbor] == 1 and neighbor not in visited:
        #         visited.add(neighbor)
        #         queue.append(neighbor)

    return ans


def numIslandsDFS(grid: List[List[str]]) -> int:
    """
    Input: grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]
    Output: 3
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    def dfs(r: int, c: int) -> None:
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or grid[r][c] == "0"
            or (r, c) in visited
        ):
            return

        visited.add((r, c))

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in visited:
                dfs(r, c)
                count += 1

    return count


def numIslandsBFS(self, grid: List[List[str]]) -> int:
    """
    Input: grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]
    Output: 3
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    def bfs(r: int, c: int) -> None:
        q = deque()
        visited.add((r, c))
        q.append((r, c))

        while q:
            row, col = q.popleft()
            directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

            for dr, dc in directions:
                r, c = row + dr, col + dc
                if (
                    0 <= r < rows
                    and 0 <= c < cols
                    and grid[r][c] == "1"
                    and (r, c) not in visited
                ):
                    visited.add((r, c))
                    q.append((r, c))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in visited:
                bfs(r, c)
                count += 1

    return count


def orangesRotting(grid: List[List[int]]) -> int:
    """
    Input: grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    Output: 4
    """
    rows, cols = len(grid), len(grid[0])

    q = deque()
    fresh = 0
    minutes = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            if grid[r][c] == 1:
                fresh += 1

    while q and fresh > 0:
        for _ in range(len(q)):
            row, col = q.popleft()
            directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
                    grid[r][c] = 2
                    q.append((r, c))
                    fresh -= 1

        minutes += 1

    return minutes if fresh == 0 else -1


def solve(board: List[List[str]]) -> None:
    """
    Do not return anything, modify board in-place instead.
    Input: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
    Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
    """
    if not board or not board[0]:
        return

    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != "O":
            return
        board[r][c] = "E"  # Mark as escaped / connected to border
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    # Traverse boundary cells
    for r in range(rows):
        if board[r][0] == "O":
            dfs(r, 0)
        if board[r][cols - 1] == "O":
            dfs(r, cols - 1)

    for c in range(cols):
        if board[0][c] == "O":
            dfs(0, c)
        if board[rows - 1][c] == "O":
            dfs(rows - 1, c)

    # Flip remaining 'O' to 'X' (captured), and restore 'E' to 'O'
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O":
                board[r][c] = "X"
            elif board[r][c] == "E":
                board[r][c] = "O"


def pacificAtlantic(heights: List[List[int]]) -> List[List[int]]:
    """
    Input: heights = [[1, 2, 2, 3, 5],
                      [3, 2, 3, 4, 4],
                      [2, 4, 5, 3, 1],
                      [6, 7, 1, 4, 5],
                      [5, 1, 1, 2, 4]]
    Output: [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
    """
    if not heights or not heights[0]:
        return []

    rows, cols = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()

    def dfs(r: int, c: int, visited: set) -> None:
        visited.add((r, c))
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and (nr, nc) not in visited
                and heights[nr][nc] >= heights[r][c]
            ):
                dfs(nr, nc, visited)

    for r in range(rows):
        dfs(r, 0, pacific)
        dfs(r, cols - 1, atlantic)

    for c in range(cols):
        dfs(0, c, pacific)
        dfs(rows - 1, c, atlantic)

    return [list(coord) for coord in (pacific & atlantic)]


def maximumDetonation(bombs: List[List[int]]) -> int:
    """
    Input: bombs = [[2, 1, 3], [6, 1, 4]]
    Output: 2
    """
    ans = 0

    def dfs(i: int) -> int:
        visited.add(i)

        x, y, r = bombs[i]
        tmp = 1

        for j in range(len(bombs)):
            if j in visited:
                continue

            dx, dy, _ = bombs[j]

            if (x - dx) ** 2 + (y - dy) ** 2 <= r**2:
                tmp += dfs(j)

        return tmp

    for i in range(len(bombs)):
        visited = set()
        ans = max(ans, dfs(i))

    return ans


def numberOfProvinces(isConnected: List[List[int]]) -> int:
    """
    Input: isConnected = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    Output: 2
    """
    n = len(isConnected)

    visited = set()
    count = 0

    def dfs(i: int) -> None:
        if i in visited:
            return

        visited.add(i)

        for j in range(n):
            if isConnected[i][j] == 1:
                dfs(j)

    for i in range(n):
        if i not in visited:
            dfs(i)
            count += 1

    return count


# This node class is only for the problem
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def cloneGraph(node: Optional[Node]) -> Optional[Node]:
    """
    Input: adjList = [[2, 4], [1, 3], [2, 4], [1, 3]]
    Output: [[2, 4], [1, 3], [2, 4], [1, 3]]
    """
    oldToNew = {}

    def dfs(node: Optional[Node]) -> Optional[Node]:
        if node is None:
            return None

        if node in oldToNew:
            return oldToNew[node]

        copy = Node(node.val)
        oldToNew[node] = copy

        for neighbor in node.neighbors:
            copy.neighbors.append(dfs(neighbor))

        return copy

    return dfs(node)


def courseSchedule(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    Input: numCourses = 2, prerequisites = [[1, 0]]
    Output: True
    """
    graph = {i: [] for i in range(numCourses)}

    for course, preReq in prerequisites:
        graph[course].append(preReq)

    visiting = set()

    def dfs(course):
        if course in visiting:
            return False

        if graph[course] == []:
            return True

        visiting.add(course)

        for preReq in graph[course]:
            if not dfs(preReq):
                return False

        visiting.remove(course)

        graph[course] = []

        return True

    for course in range(numCourses):
        if not dfs(course):
            return False

    return True


# ==============================================================================
# 1. Topological Sort: Course Schedule II (LC 210)
# ==============================================================================
def findOrder(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    Input: numCourses = 4, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
    Output: [0, 2, 1, 3]
    """
    adj = defaultdict(list)
    in_degree = [0] * numCourses

    for course, pre in prerequisites:
        adj[pre].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []

    while queue:
        curr = queue.popleft()
        order.append(curr)

        for nxt in adj[curr]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)

    return order if len(order) == numCourses else []


# ==============================================================================
# 2. Dijkstra's Algorithm: Network Delay Time (LC 743)
# ==============================================================================
def networkDelayTime(times: List[List[int]], n: int, k: int) -> int:
    """
    Input: times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]], n = 4, k = 2
    Output: 2
    """
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))

    # Min-heap storing (distance_so_far, node)
    min_heap = [(0, k)]
    dist = {}

    while min_heap:
        d, u = heapq.heappop(min_heap)

        if u in dist:
            continue
        dist[u] = d

        for v, weight in adj[u]:
            if v not in dist:
                heapq.heappush(min_heap, (d + weight, v))

    return max(dist.values()) if len(dist) == n else -1


# ==============================================================================
# 3. Disjoint Set Union (DSU): Accounts Merge (LC 721)
# ==============================================================================
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1


def accountsMerge(accounts: List[List[str]]) -> List[List[str]]:
    """
    Input: accounts = [["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["John", "johnsmith@mail.com", "john00@mail.com"], ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]
    Output: [["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"], ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]
    """
    uf = UnionFind(len(accounts))
    email_to_account: Dict[str, int] = {}

    # Step 1: Map each email to account index and union if email seen before
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_account:
                uf.union(i, email_to_account[email])
            else:
                email_to_account[email] = i

    # Step 2: Group emails by their root parent account index
    root_to_emails = defaultdict(list)
    for email, acc_idx in email_to_account.items():
        root = uf.find(acc_idx)
        root_to_emails[root].append(email)

    # Step 3: Format the merged accounts with sorted emails
    merged_accounts = []
    for root, emails in root_to_emails.items():
        name = accounts[root][0]
        merged_accounts.append([name] + sorted(emails))

    return merged_accounts


# ==============================================================================
# 4. Implicit Graph BFS: Word Ladder (LC 127)
# ==============================================================================
def ladderLength(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """
    Input: beginWord = "hit", endWord = "cog", wordList = ["hot", "dot", "dog", "lot", "log", "cog"]
    Output: 5
    """
    if endWord not in wordList or not beginWord or not endWord or not wordList:
        return 0

    L = len(beginWord)
    all_combo_dict = defaultdict(list)

    for word in wordList:
        for i in range(L):
            pattern = word[:i] + "*" + word[i + 1 :]
            all_combo_dict[pattern].append(word)

    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        current_word, level = queue.popleft()

        for i in range(L):
            intermediate_word = current_word[:i] + "*" + current_word[i + 1 :]

            for word in all_combo_dict[intermediate_word]:
                if word == endWord:
                    return level + 1

                if word not in visited:
                    visited.add(word)
                    queue.append((word, level + 1))

            all_combo_dict[intermediate_word] = []  # avoid re-visiting words

    return 0
