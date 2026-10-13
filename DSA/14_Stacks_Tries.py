
def isValidParentheses(s: str) -> bool:
    """LC 20: Valid Parentheses (Easy).

    Input: "([]{})" -> True; "([)]" -> False. Empty input is valid.
    Match each closing bracket with the most recent opening bracket.
    Non-bracket characters are rejected. O(n) time and O(n) space.
    """
    closing: dict[str, str] = {')': '(', ']': '[', '}': '{'}
    stack: list[str] = []
    for char in s:
        if char in '([{':
            stack.append(char)
        elif char not in closing or not stack or stack.pop() != closing[char]:
            return False
    return not stack


class MinStack:
    """LC 155: Min Stack (Medium).

    push(-2), push(0), push(-3), getMin() -> -3; pop(), getMin() -> -2.
    Each entry stores its value and the minimum at that stack depth.
    All operations O(1); O(n) storage. Reads/pops require a nonempty stack.
    """
    def __init__(self) -> None:
        self.stack: list[tuple[int, int]] = []

    def push(self, val: int) -> None:
        minimum: int = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, minimum))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word: bool = False


class Trie:
    """LC 208: Implement Trie (Medium; optional revision after core patterns).

    insert("apple"), search("apple") -> True, search("app") -> False,
    startsWith("app") -> True. insert("app") makes search("app") True.
    O(L) per operation; storage O(total inserted characters).
    """
    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        node: TrieNode = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def _find(self, text: str) -> TrieNode | None:
        node: TrieNode | None = self.root
        for char in text:
            node = node.children.get(char)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node: TrieNode | None = self._find(word)
        return node is not None and node.is_word

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None
