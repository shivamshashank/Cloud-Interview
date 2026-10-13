from typing import Optional, List, Dict
from collections import deque, defaultdict
import heapq


def dfsOfGraph(adj: list[list[int]]) -> list[int]:
    'Input: adj = [[1, 2], [0, 2], [0, 1]]\nOutput: [0, 1, 2]\nTraverses only the component reachable from vertex 0.'
    if not adj:
        return []
    visited: set[int]
    result: list[int]
    visited, result = set(), []
    stack: list[int] = [0]
    while stack:
        node: int = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        result.append(node)
        stack.extend(reversed(adj[node]))
    return result


def bfsOfGraph(adj: list[list[int]]) -> list[int]:
    """
    Input: adj = [[1, 2], [0, 2], [0, 1]]
    Output: [0, 1, 2]
    """
    if not adj:
        return []
    n: int = len(adj)
    visited: set[int] = {0}
    ans: list[int] = []

    queue: deque[int] = deque([0])

    while queue:
        node: int = queue.popleft()
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
    'Input: grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]\nOutput: 3\nIterative DFS avoids recursion overflow; O(rows*cols) time/space.'
    if not grid or not grid[0]:
        return 0
    rows: int
    cols: int
    rows, cols = len(grid), len(grid[0])
    visited: set[tuple[int, int]] = set()
    count: int = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or (r, c) in visited:
                continue
            count += 1
            stack: list[tuple[int, int]] = [(r, c)]
            visited.add((r, c))
            while stack:
                row: int
                col: int
                row, col = stack.pop()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr: int
                    nc: int
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1" and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        stack.append((nr, nc))
    return count


def numIslandsBFS(grid: List[List[str]]) -> int:
    """
    Input: grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]
    Output: 3
    """
    if not grid or not grid[0]:
        return 0
    rows: int
    cols: int
    rows, cols = len(grid), len(grid[0])
    visited: set[tuple[int, int]] = set()
    count: int = 0

    def bfs(r: int, c: int) -> None:
        q: deque[tuple[int, int]] = deque()
        visited.add((r, c))
        q.append((r, c))

        while q:
            row: int
            col: int
            row, col = q.popleft()
            directions: list[list[int]] = [[1, 0], [-1, 0], [0, 1], [0, -1]]

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
    if not grid or not grid[0]:
        return 0
    rows: int
    cols: int
    rows, cols = len(grid), len(grid[0])

    q: deque[tuple[int, int]] = deque()
    fresh: int = 0
    minutes: int = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            if grid[r][c] == 1:
                fresh += 1

    while q and fresh > 0:
        for _ in range(len(q)):
            row: int
            col: int
            row, col = q.popleft()
            directions: list[list[int]] = [[1, 0], [-1, 0], [0, 1], [0, -1]]

            for dr, dc in directions:
                r: int
                c: int
                r, c = row + dr, col + dc
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
                    grid[r][c] = 2
                    q.append((r, c))
                    fresh -= 1

        minutes += 1

    return minutes if fresh == 0 else -1


def solve(board: List[List[str]]) -> None:
    'Do not return anything, modify board in-place instead.\nInput: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]\nOutput: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]\nIterative boundary flood fill; O(rows*cols) time/space.'
    if not board or not board[0]:
        return
    rows: int
    cols: int
    rows, cols = len(board), len(board[0])
    stack: list[tuple[int, int]] = [(r, c) for r in range(rows) for c in range(cols)
             if (r in (0, rows - 1) or c in (0, cols - 1)) and board[r][c] == "O"]
    while stack:
        r: int
        c: int
        r, c = stack.pop()
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != "O":
            continue
        board[r][c] = "E"
        stack.extend(((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))
    for r in range(rows):
        for c in range(cols):
            board[r][c] = "O" if board[r][c] == "E" else "X"


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

    rows: int
    cols: int
    rows, cols = len(heights), len(heights[0])
    pacific: set[tuple[int, int]] = set()
    atlantic: set[tuple[int, int]] = set()

    def dfs(r: int, c: int, visited: set[tuple[int, int]]) -> None:
        if (r, c) in visited:
            return
        visited.add((r, c))
        stack: list[tuple[int, int]] = [(r, c)]
        while stack:
            row: int
            col: int
            row, col = stack.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr: int
                nc: int
                nr, nc = row + dr, col + dc
                if (0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited
                        and heights[nr][nc] >= heights[row][col]):
                    visited.add((nr, nc))
                    stack.append((nr, nc))

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
    ans: int = 0

    def dfs(i: int) -> int:
        visited.add(i)

        x: int
        y: int
        r: int
        x, y, r = bombs[i]
        tmp: int = 1

        for j in range(len(bombs)):
            if j in visited:
                continue

            dx: int
            dy: int
            dx, dy, _ = bombs[j]

            if (x - dx) ** 2 + (y - dy) ** 2 <= r**2:
                tmp += dfs(j)

        return tmp

    for i in range(len(bombs)):
        visited: set[int] = set()
        ans = max(ans, dfs(i))

    return ans


def numberOfProvinces(isConnected: List[List[int]]) -> int:
    """
    Input: isConnected = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    Output: 2
    """
    n: int = len(isConnected)

    visited: set[int] = set()
    count: int = 0

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
    def __init__(self, val: int = 0, neighbors: list[Node] | None = None) -> None:
        self.val: int = val
        self.neighbors: list[Node] = neighbors if neighbors is not None else []


def cloneGraph(node: Optional[Node]) -> Optional[Node]:
    """
    Input: adjList = [[2, 4], [1, 3], [2, 4], [1, 3]]
    Output: [[2, 4], [1, 3], [2, 4], [1, 3]]
    """
    oldToNew: dict[Node, Node] = {}

    def dfs(node: Node) -> Node:

        if node in oldToNew:
            return oldToNew[node]

        copy: Node = Node(node.val)
        oldToNew[node] = copy

        for neighbor in node.neighbors:
            copy.neighbors.append(dfs(neighbor))

        return copy

    return dfs(node) if node is not None else None


def courseSchedule(numCourses: int, prerequisites: List[List[int]]) -> bool:
    'Input: numCourses = 2, prerequisites = [[1, 0]]\nOutput: True\nKahn topological sort: O(V+E), avoids recursion on long chains.'
    return len(findOrder(numCourses, prerequisites)) == numCourses


# ==============================================================================
# 1. Topological Sort: Course Schedule II (LC 210)
# ==============================================================================
def findOrder(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    Input: numCourses = 4, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
    Output: [0, 2, 1, 3]
    """
    adj: defaultdict[int, list[int]] = defaultdict(list)
    in_degree: list[int] = [0] * numCourses

    for course, pre in prerequisites:
        adj[pre].append(course)
        in_degree[course] += 1

    queue: deque[int] = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order: list[int] = []

    while queue:
        curr: int = queue.popleft()
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
    adj: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))

    # Min-heap storing (distance_so_far, node)
    min_heap: list[tuple[int, int]] = [(0, k)]
    dist: dict[int, int] = {}

    while min_heap:
        d: int
        u: int
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
    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(range(n))
        self.rank: list[int] = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        root_x: int
        root_y: int
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
    uf: UnionFind = UnionFind(len(accounts))
    email_to_account: Dict[str, int] = {}

    # Step 1: Map each email to account index and union if email seen before
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_account:
                uf.union(i, email_to_account[email])
            else:
                email_to_account[email] = i

    # Step 2: Group emails by their root parent account index
    root_to_emails: defaultdict[int, list[str]] = defaultdict(list)
    for email, acc_idx in email_to_account.items():
        root: int = uf.find(acc_idx)
        root_to_emails[root].append(email)

    # Step 3: Format the merged accounts with sorted emails
    merged_accounts: list[list[str]] = []
    for root, emails in root_to_emails.items():
        name: str = accounts[root][0]
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

    L: int = len(beginWord)
    all_combo_dict: defaultdict[str, list[str]] = defaultdict(list)

    for word in wordList:
        for i in range(L):
            pattern: str = word[:i] + "*" + word[i + 1 :]
            all_combo_dict[pattern].append(word)

    queue: deque[tuple[str, int]] = deque([(beginWord, 1)])
    visited: set[str] = {beginWord}

    while queue:
        current_word: str
        level: int
        current_word, level = queue.popleft()

        for i in range(L):
            intermediate_word: str = current_word[:i] + "*" + current_word[i + 1 :]

            for word in all_combo_dict[intermediate_word]:
                if word == endWord:
                    return level + 1

                if word not in visited:
                    visited.add(word)
                    queue.append((word, level + 1))

            all_combo_dict[intermediate_word] = []  # avoid re-visiting words

    return 0
