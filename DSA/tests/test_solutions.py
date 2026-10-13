"""Run: python3 -m unittest discover -s DSA/tests -v (standard library only)."""

import importlib.util
import itertools
import math
import random
import statistics
import unittest
from collections import Counter, OrderedDict, deque
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(prefix):
    path = next(ROOT.glob(prefix + '_*.py'))
    spec = importlib.util.spec_from_file_location('dsa_' + prefix, path)
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load the solution module')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


A, W, B, I, H, L, T, G, C, R, D, M, BIT, S = [load(f'{i:02}') for i in range(1, 15)]


def linked(values, cls=L.ListNode):
    dummy = tail = cls()
    for value in values:
        tail.next = cls(value)
        tail = tail.next
    return dummy.next


def values(head):
    result, seen = [], set()
    while head:
        if id(head) in seen:
            raise AssertionError('unexpected linked-list cycle')
        seen.add(id(head))
        result.append(head.val)
        head = head.next
    return result


def tree(items):
    if not items or items[0] is None:
        return None
    root = T.TreeNode(items[0])
    queue = deque([root])
    it = iter(items[1:])
    while queue:
        node = queue.popleft()
        for side in ('left', 'right'):
            value = next(it, None)
            if value is not None:
                child = T.TreeNode(value)
                setattr(node, side, child)
                queue.append(child)
    return root


def traversals(root):
    if root is None:
        return [], [], []
    lp, li, lo = traversals(root.left)
    rp, ri, ro = traversals(root.right)
    return [root.val] + lp + rp, li + [root.val] + ri, lo + ro + [root.val]


def canonical(groups):
    return sorted(tuple(group) for group in groups)


class SolutionsTest(unittest.TestCase):
    def test_arrays_examples(self):
        self.assertEqual(A.productExceptSelf([1, 2, 3, 4]), [24, 12, 8, 6])
        pair = A.twoSum([3, 3], 6)
        self.assertEqual(set(pair), {0, 1})
        self.assertTrue(A.containsDuplicate([1, 2, 1]))
        self.assertEqual(A.NumArray([-2, 0, 3, -5, 2, -1]).sumRange(0, 2), 1)
        self.assertEqual(A.maxSubArray([-3, -1, -2]), -1)
        self.assertEqual(A.dailyTemperatures([73,74,75,71,69,72,76,73]), [1,1,4,2,1,1,0,0])
        self.assertEqual(A.largestRectangleArea([2,1,5,6,2,3]), 10)
        matrix = [[1,1,1],[1,0,1],[1,1,1]]
        A.setZeroes(matrix)
        self.assertEqual(matrix, [[1,0,1],[0,0,0],[1,0,1]])
        nums = [0,1,0,3,12]; A.moveZeroes(nums)
        self.assertEqual(nums, [1,3,12,0,0])
        codec = A.EncodeDecodeStrings()
        for strings in ([], [''], ['12#', '🙂', '', '#abc']):
            self.assertEqual(codec.decode(codec.encode(strings)), strings)
        self.assertEqual(A.longestConsecutive([1]*1000 + list(range(1, 1000))), 999)
        self.assertEqual(A.largestNumber([3,30,34,5,9]), '9534330')
        self.assertEqual(A.largestNumber([0,0]), '0')
        self.assertEqual(A.firstMissingPositive([3,4,-1,1]), 2)
        self.assertEqual(A.maxIndexDiff([34,8,10,3,2,80,30,33,1]), 6)
        self.assertEqual(A.spiralOrder([[1,2,3],[4,5,6]]), [1,2,3,6,5,4])
        matrix = [[1,2],[3,4]]; A.rotate(matrix)
        self.assertEqual(matrix, [[3,1],[4,2]])
        board = [['.']*9 for _ in range(9)]
        self.assertTrue(A.isValidSudoku(board))
        board[0][0] = board[1][1] = '5'
        self.assertFalse(A.isValidSudoku(board))
        board = [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]; A.gameOfLife(board)
        self.assertEqual(board, [[0,0,0],[1,0,1],[0,1,1],[0,1,0]])

    def test_prefix_sums_against_brute_force(self):
        rng = random.Random(7)
        for _ in range(150):
            nums = [rng.randint(-3,3) for _ in range(rng.randrange(9))]
            sums = [(j-i, sum(nums[i:j])) for i in range(len(nums)) for j in range(i+1,len(nums)+1)]
            for k in range(-3,4):
                self.assertEqual(A.subArraySum(nums,k), sum(total == k for _,total in sums), (nums,k))
                expected = any(length >= 2 and (total % k == 0 if k else total == 0) for length,total in sums)
                self.assertEqual(A.checkSubarraySum(nums,k), expected, (nums,k))

    def test_num_matrix_all_rectangles(self):
        rng = random.Random(304)
        for rows in range(1,6):
            for cols in range(1,6):
                matrix = [[rng.randint(-9,9) for _ in range(cols)] for _ in range(rows)]
                original = [row[:] for row in matrix]
                obj = A.NumMatrix(matrix)
                for r1 in range(rows):
                    for r2 in range(r1,rows):
                        for c1 in range(cols):
                            for c2 in range(c1,cols):
                                expected = sum(matrix[r][c] for r in range(r1,r2+1) for c in range(c1,c2+1))
                                self.assertEqual(obj.sumRegion(r1,c1,r2,c2), expected)
                self.assertEqual(matrix, original)

    def test_new_anagrams_colors_parentheses(self):
        words = ['eat','tea','tan','ate','nat','bat','','','éa','aé']
        groups = A.groupAnagrams(words)
        self.assertEqual(Counter(itertools.chain.from_iterable(groups)), Counter(words))
        self.assertEqual(len(groups), 5)
        for group in groups:
            self.assertTrue(all(Counter(word) == Counter(group[0]) for word in group))
        for n in range(7):
            for seq in itertools.product(range(3), repeat=n):
                nums = list(seq); S_before = sorted(nums)
                self.assertIsNone(W.sortColors(nums))
                self.assertEqual(nums,S_before)
        for text, answer in [('',True),('([]{})',True),('([)]',False),(']',False),('(',False),('a',False)]:
            self.assertEqual(S.isValidParentheses(text), answer)

    def test_windows_examples(self):
        self.assertEqual(W.twoSum([2,7,11,15],9),[1,2])
        self.assertEqual(W.twoSum([1,2,4],8),[])
        self.assertEqual(W.removeDuplicates([]),0)
        nums=[1,1,2,2,3]; n=W.removeDuplicates(nums)
        self.assertEqual(nums[:n],[1,2,3])
        self.assertEqual(canonical(W.threeSum([-1,0,1,2,-1,-4])),[(-1,-1,2),(-1,0,1)])
        self.assertEqual(canonical(W.fourSum([1,0,-1,0,-2,2],0)),[(-2,-1,1,2),(-2,0,0,2),(-1,0,0,1)])
        self.assertEqual(W.findMaxAverage([1,12,-5,-6,50,3],4),12.75)
        self.assertEqual(W.lengthOfLongestSubstring('abba'),2)
        self.assertEqual(W.characterReplacement('AABABBA',1),4)
        self.assertEqual(W.maxSlidingWindow([1,3,-1,-3,5,3,6,7],3),[3,3,5,5,6,7])
        self.assertEqual(W.minWindow('ADOBECODEBANC','ABC'),'BANC')
        self.assertEqual(W.minWindow('a','aa'),'')
        self.assertEqual(W.trap([0,1,0,2,1,0,1,3,2,1,2,1]),6)

    def test_arrays_windows_random(self):
        rng=random.Random(11)
        for _ in range(120):
            nums=[rng.randrange(5) for _ in range(rng.randrange(1,9))]
            self.assertEqual(A.productExceptSelf(nums),[math.prod(nums[:i]+nums[i+1:]) for i in range(len(nums))])
            self.assertEqual(A.maxIndexDiff(nums),max(j-i for i in range(len(nums)) for j in range(i,len(nums)) if nums[i]<=nums[j]))
            self.assertEqual(A.largestRectangleArea(nums),max(min(nums[i:j])*(j-i) for i in range(len(nums)) for j in range(i+1,len(nums)+1)))
            k=rng.randint(1,len(nums))
            self.assertEqual(W.maxSlidingWindow(nums,k),[max(nums[i:i+k]) for i in range(len(nums)-k+1)])
            text=''.join(map(str,nums))
            expected=max(len(text[i:j]) for i in range(len(text)) for j in range(i,len(text)+1) if len(set(text[i:j]))==j-i)
            self.assertEqual(W.lengthOfLongestSubstring(text),expected)
            self.assertEqual(W.trap(nums),sum(max(0,min(max(nums[:i+1]),max(nums[i:]))-nums[i]) for i in range(len(nums))))

    def test_search_greedy(self):
        self.assertEqual(B.binarySearch([-1,0,3,5,9,12],9),4)
        self.assertEqual(B.searchRange([5,7,7,8,8,10],8),[3,4])
        self.assertEqual(B.searchRange([],8),[-1,-1])
        self.assertEqual(B.minEatingSpeed([3,6,7,11],8),4)
        for n in range(1,12):
            for offset in range(n):
                nums=list(range(n)); nums=nums[offset:]+nums[:offset]
                for target in range(-1,n+1):
                    self.assertEqual(B.searchInRotatedSortedArray(nums,target), nums.index(target) if target in nums else -1)
        self.assertEqual(B.findPeakElement([1,2,3,1]),2)
        self.assertTrue(B.searchMatrix([[1,3,5],[7,9,11]],9))
        self.assertFalse(B.searchMatrixII([[1,4],[2,5]],3))
        self.assertFalse(B.canJump([3,2,1,0,4]))
        self.assertEqual(B.jump([2,3,1,1,4]),2)
        self.assertEqual(B.leastInterval(list('AAABBB'),2),8)
        self.assertEqual(B.canCompleteCircuit([1,2,3,4,5],[3,4,5,1,2]),3)

    def test_intervals(self):
        self.assertEqual(I.mergeIntervals([[1,3],[2,6],[8,10],[15,18]]),[[1,6],[8,10],[15,18]])
        self.assertEqual(I.eraseOverlapIntervals([[1,2],[2,3],[3,4],[1,3]]),1)
        self.assertEqual(I.eraseOverlapIntervals([]),0)
        self.assertEqual(I.insertInterval([[1,3],[6,9]],[2,5]),[[1,5],[6,9]])
        self.assertEqual(I.minMeetingRooms([[0,30],[5,10],[15,20]]),2)
        self.assertEqual(I.minMeetingRooms([[0,1],[1,2]]),1)
        self.assertEqual(I.employeeFreeTime([[[1,2],[5,6]],[[1,3]],[[4,10]]]),[[3,4]])
        self.assertEqual(I.employeeFreeTime([[I.Interval(1,2)],[I.Interval(3,4)]]),[[2,3]])
        self.assertEqual(I.employeeFreeTime([]),[])

    def test_heaps(self):
        rng=random.Random(215)
        for _ in range(100):
            nums=[rng.randint(-10,10) for _ in range(rng.randint(1,20))]
            k=rng.randint(1,len(nums))
            self.assertEqual(H.findKthLargestElement(nums,k),sorted(nums,reverse=True)[k-1])
            finder=H.MedianFinder()
            for i,value in enumerate(nums):
                finder.addNum(value)
                self.assertEqual(finder.findMedian(),statistics.median(nums[:i+1]))
        self.assertEqual(set(H.topKFrequentElements([1,1,1,2,2,3],2)),{1,2})
        groups=[[-3,1,1],[],[-3,2],[0,8]]
        heads=[linked(group,H.ListNode) for group in groups]
        merged=H.mergeKSortedLists(heads)
        self.assertIsInstance(merged,H.ListNode)
        self.assertEqual(values(merged),sorted(itertools.chain.from_iterable(groups)))
        self.assertIsNone(H.mergeKSortedLists([]))

    def test_linked_lists(self):
        self.assertEqual(L.traversal(linked([1,2,3])),[1,2,3])
        for n in range(10):
            expected=list(range(n)); head=linked(expected)
            self.assertEqual(values(L.reverseList(head)),expected[::-1])
            head=linked(expected); L.reorderList(head)
            order=[]; left,right=0,n-1
            while left<=right:
                order.append(left)
                if left<right: order.append(right)
                left+=1; right-=1
            self.assertEqual(values(head),order)
        head=linked([1,2,3]); tail=head.next.next; tail.next=head.next
        self.assertIs(L.detectCycle(head),head.next)
        self.assertIsNone(L.detectCycle(linked([1,2,3])))
        self.assertEqual(values(L.mergeTwoLists(linked([1,2,4]),linked([1,3,4]))),[1,1,2,3,4,4])
        for n in range(1,8):
            for remove in range(1,n+1):
                expected=list(range(n));del expected[n-remove]
                self.assertEqual(values(L.removeNthFromEnd(linked(range(n)),remove)),expected)
        self.assertEqual(values(L.mergeInBetween(linked(range(6)),2,4,linked([100,101]))),[0,1,100,101,5])
        self.assertEqual(values(L.mergeInBetween(linked([1,2]),0,1,None)),[])
        self.assertEqual(values(L.addTwoNumbers(linked([9,9,9]),linked([1]))),[0,0,0,1])

    def test_pointer_validation_and_integer_results(self):
        for n in (0, -1, 3):
            head = linked([1, 2])
            with self.assertRaises(ValueError):
                L.removeNthFromEnd(head, n)
            self.assertEqual(values(head), [1, 2])
        with self.assertRaises(ValueError):
            L.removeNthFromEnd(None, 1)
        for a, b in ((-1, 0), (1, 0), (3, 3), (0, 2)):
            head = linked([1, 2])
            with self.assertRaises(ValueError):
                L.mergeInBetween(head, a, b, None)
            self.assertEqual(values(head), [1, 2])
        self.assertEqual(T.maxPathSum(tree([-3])), -3)
        with self.assertRaises(ValueError):
            T.maxPathSum(None)
        result = D.minPathSum([[10**30, 1], [2, 3]])
        self.assertEqual(result, 10**30 + 4)
        self.assertIsInstance(result, int)
        self.assertIsNone(G.cloneGraph(None))

    def test_tree_queries(self):
        root=tree([3,5,1,6,2,0,8,None,None,7,4])
        if root is None or root.left is None:
            raise RuntimeError('Test fixture does not contain the expected tree nodes')
        if root.left.left is None or root.left.right is None:
            raise RuntimeError('Test fixture does not contain the expected tree nodes')
        if root.left.right.right is None:
            raise RuntimeError('Test fixture does not contain the expected tree nodes')
        self.assertIs(T.lowestCommonAncestorBT(root,root.left.left,root.left.right.right),root.left)
        self.assertEqual(T.levelOrder(root),[[3],[5,1],[6,2,0,8],[7,4]])
        self.assertEqual(T.maxDepth(root),4)
        self.assertEqual(T.diameterOfBinaryTree(tree([1,2,3,4,5])),3)
        bst=tree([4,2,6,1,3,5,7])
        if bst is None or bst.left is None:
            raise RuntimeError('Test fixture does not contain the expected tree nodes')
        if bst.left.left is None or bst.left.right is None:
            raise RuntimeError('Test fixture does not contain the expected tree nodes')
        self.assertTrue(T.isValidBST(bst))
        self.assertFalse(T.isValidBST(tree([5,1,4,None,None,3,6])))
        self.assertEqual(T.searchBST(bst,3).val,3)
        self.assertEqual(T.lowestCommonAncestorBST(bst,bst.left.left,bst.left.right).val,2)
        self.assertTrue(T.isSymmetric(tree([1,2,2,3,4,4,3])))
        self.assertEqual(T.binaryTreePaths(tree([1,2,3,None,5])),['1->2->5','1->3'])
        self.assertTrue(T.hasPathSum(tree([1,2,3]),3))
        self.assertEqual(T.kthSmallest(bst,4),4)
        self.assertEqual(set(T.distanceK(root,root.left,2)),{7,4,1})
        self.assertEqual(T.maxPathSum(tree([-10,9,20,None,None,15,7])),42)
        self.assertEqual(sorted(n.val for n in T.findDuplicateSubtrees(tree([1,2,3,4,None,2,4,None,None,4]))),[2,4])
        self.assertEqual(T.mergeTwoBST(tree([3,1,5]),tree([4,2,6])),[1,2,3,4,5,6])
        self.assertEqual(T.mergeTwoBST(None,None),[])

    def test_tree_construction_and_codec(self):
        rng=random.Random(889)
        for size in range(35):
            nodes=[T.TreeNode(i) for i in range(size)]
            available=nodes[:1]
            for node in nodes[1:]:
                parent=rng.choice(available)
                side=rng.choice([s for s in ('left','right') if getattr(parent,s) is None])
                setattr(parent,side,node)
                if parent.left and parent.right: available.remove(parent)
                available.append(node)
            root=nodes[0] if nodes else None
            pre,ino,post=traversals(root)
            self.assertEqual(T.inorder(root),ino)
            self.assertEqual(traversals(T.constructInorderPreorder(pre,ino)),(pre,ino,post))
            self.assertEqual(traversals(T.constructInorderPostorder(ino,post)),(pre,ino,post))
            rebuilt=T.constructFromPreorderAndPostorder(pre,post)
            actual=traversals(rebuilt)
            self.assertEqual((actual[0],actual[2]),(pre,post))
            codec=T.SerializeDeserialize()
            self.assertEqual(traversals(codec.deserialize(codec.serialize(root))),(pre,ino,post))

    def test_graphs(self):
        adj=[[1,2],[0,2],[0,1]]
        self.assertEqual(G.dfsOfGraph(adj),[0,1,2]);self.assertEqual(G.bfsOfGraph(adj),[0,1,2])
        self.assertEqual(G.dfsOfGraph([]),[]);self.assertEqual(G.bfsOfGraph([]),[])
        grid=[list('11000'),list('11000'),list('00100'),list('00011')]
        self.assertEqual(G.numIslandsDFS(grid),3);self.assertEqual(G.numIslandsBFS(grid),3)
        self.assertEqual(G.orangesRotting([[2,1,1],[1,1,0],[0,1,1]]),4)
        board=[list('XXXX'),list('XOOX'),list('XXOX'),list('XOXX')];G.solve(board)
        self.assertEqual(board,[list('XXXX'),list('XXXX'),list('XXXX'),list('XOXX')])
        self.assertEqual(G.pacificAtlantic([[1]]),[[0,0]])
        self.assertEqual(G.maximumDetonation([[2,1,3],[6,1,4]]),2)
        self.assertEqual(G.numberOfProvinces([[1,1,0],[1,1,0],[0,0,1]]),2)
        node=G.Node(1);other=G.Node(2);node.neighbors=[other];other.neighbors=[node]
        clone=G.cloneGraph(node)
        self.assertIsNot(clone,node);self.assertIs(clone.neighbors[0].neighbors[0],clone)
        self.assertFalse(G.courseSchedule(2,[[1,0],[0,1]]))
        order=G.findOrder(4,[[1,0],[2,0],[3,1],[3,2]])
        self.assertEqual(set(order),set(range(4)))
        self.assertTrue(all(order.index(a)<order.index(b) for a,b in [(0,1),(0,2),(1,3),(2,3)]))
        self.assertEqual(G.networkDelayTime([[2,1,1],[2,3,1],[3,4,1]],4,2),2)
        self.assertEqual(G.networkDelayTime([],2,1),-1)
        accounts=[['J','a','b'],['J','b','c'],['M','d']]
        self.assertEqual(sorted(G.accountsMerge(accounts)),[['J','a','b','c'],['M','d']])
        self.assertEqual(G.ladderLength('hit','cog',['hot','dot','dog','lot','log','cog']),5)

    def test_large_graph_inputs(self):
        grid=[['1']*2000]
        self.assertEqual(G.numIslandsDFS(grid),1)
        self.assertEqual(G.numIslandsBFS(grid),1)
        self.assertTrue(G.courseSchedule(3000,[[i,i-1] for i in range(1,3000)]))
        board=[['O']*2000];G.solve(board);self.assertEqual(board,[['O']*2000])
        self.assertEqual(len(G.pacificAtlantic([[1]*50 for _ in range(50)])),2500)

    def test_stateful_structures_against_models(self):
        rng=random.Random(146)
        for capacity in (0,1,3):
            obj=C.LRUCache(capacity); model=OrderedDict()
            for _ in range(200):
                key=rng.randrange(6)
                if rng.randrange(2):
                    value=rng.randrange(100);obj.put(key,value)
                    model.pop(key,None);model[key]=value
                    if len(model)>capacity:model.popitem(last=False)
                else:
                    expected=model.get(key,-1)
                    self.assertEqual(obj.get(key),expected)
                    if key in model:model.move_to_end(key)
        obj=C.RandomizedSet();model=set()
        for _ in range(500):
            value=rng.randrange(20)
            if rng.randrange(2):
                self.assertEqual(obj.insert(value),value not in model);model.add(value)
            else:
                self.assertEqual(obj.remove(value),value in model);model.discard(value)
            self.assertEqual(set(obj.values),model)
            self.assertEqual(obj.positions,{v:i for i,v in enumerate(obj.values)})
            if model:self.assertIn(obj.getRandom(),model)
        obj=C.TimeMap();obj.set('foo','a',1);obj.set('foo','b',4)
        self.assertEqual([obj.get('foo',t) for t in (0,1,3,4,5)],['','a','a','b','b'])
        self.assertEqual(obj.get('missing',99),'')
        logger=C.Logger()
        self.assertEqual([logger.shouldPrintMessage(t,'x') for t in (1,2,10,11)],[True,False,False,True])
        hits=C.HitCounter()
        for timestamp in range(1,1001):hits.hit(timestamp)
        self.assertEqual(hits.getHits(1000),300)
        self.assertLessEqual(len(hits.hits),300)
        self.assertEqual(hits.getHits(1300),0)

    def test_nested_iterator(self):
        class Nested:
            def __init__(self,value):self.value=value
            def isInteger(self):return isinstance(self.value,int)
            def getInteger(self):return self.value
            def getList(self):return [Nested(x) for x in self.value]
        obj=C.NestedIterator([Nested([1,1]),Nested(2),Nested([[],[3]])])
        result=[]
        while obj.hasNext():
            self.assertIs(type(obj.hasNext()),bool)
            result.append(obj.next())
        self.assertEqual(result,[1,1,2,3]);self.assertIs(obj.hasNext(),False)
        self.assertFalse(C.NestedIterator([]).hasNext())

    def test_min_stack_and_trie(self):
        obj=S.MinStack();model=[];rng=random.Random(155)
        for _ in range(500):
            if not model or rng.randrange(2):
                value=rng.randint(-20,20);obj.push(value);model.append(value)
            else:obj.pop();model.pop()
            if model:self.assertEqual((obj.top(),obj.getMin()),(model[-1],min(model)))
        obj=S.Trie()
        obj.insert('apple');self.assertTrue(obj.search('apple'));self.assertFalse(obj.search('app'))
        self.assertTrue(obj.startsWith('app'));self.assertFalse(obj.startsWith('b'))
        for word in ('app','', 'aé','apple'):obj.insert(word)
        for word in ('app','', 'aé','apple'):self.assertTrue(obj.search(word))
        self.assertFalse(obj.search('a'))

    def test_backtracking(self):
        self.assertEqual(len(R.subsets([1,2,3])),8)
        self.assertEqual(canonical(R.subsetsWithDup([1,2,2])),[(),(1,),(1,2),(1,2,2),(2,),(2,2)])
        self.assertEqual(canonical(R.permute([1,2,3])),sorted(itertools.permutations([1,2,3])))
        self.assertEqual(canonical(R.permuteUnique([1,1,2])),[(1,1,2),(1,2,1),(2,1,1)])
        self.assertEqual(canonical(R.combinations(4,2)),list(itertools.combinations(range(1,5),2)))
        self.assertEqual(canonical(R.combinationSum([2,3,6,7],7)),[(2,2,3),(7,)])
        self.assertEqual(canonical(R.combinationSumII([10,1,2,7,6,1,5],8)),[(1,1,6),(1,2,5),(1,7),(2,6)])
        self.assertEqual(canonical(R.generatePartitions('aab')),[('a','a','b'),('aa','b')])
        self.assertTrue(R.wordBreak('leetcode',['leet','code']))
        self.assertFalse(R.wordBreak('a'*200+'b',['a','aa','aaa','aaaa']))
        board=[list('ABCE'),list('SFCS'),list('ADEE')];original=[r[:] for r in board]
        self.assertTrue(R.exist(board,'ABCCED'));self.assertFalse(R.exist(board,'ABCB'))
        self.assertEqual(board,original)
        self.assertTrue(R.exist([],''));self.assertFalse(R.exist([],'a'))

    def test_dynamic_programming_examples_and_large(self):
        self.assertEqual(D.climbStairs(3),3)
        self.assertEqual(D.houseRobberI([2,7,9,3,1]),12)
        self.assertEqual(D.houseRobberII([2,3,2]),3)
        self.assertEqual(D.houseRobberII([]),0)
        self.assertEqual(D.uniquePaths(3,7),28)
        self.assertEqual(D.uniquePathsWithObstacles([[0,0,0],[0,1,0],[0,0,0]]),2)
        self.assertEqual(D.uniquePathsWithObstacles([[1]]),0)
        self.assertEqual(D.minPathSum([[1,3,1],[1,5,1],[4,2,1]]),7)
        self.assertEqual(D.minimumTotal([[2],[3,4],[6,5,7],[4,1,8,3]]),11)
        self.assertEqual(D.maximalSquare([list('10100'),list('10111'),list('11111'),list('10010')]),4)
        self.assertEqual(D.findTargetSumWays([1,1,1,1,1],3),5)
        self.assertEqual(D.findTargetSumWays([0,0,0],0),8)
        self.assertTrue(D.canPartition([1,5,11,5]));self.assertFalse(D.canPartition([1,2,5]))
        self.assertEqual(D.lengthOfLIS([10,9,2,5,3,7,101,18]),4)
        self.assertEqual(D.coinChange([1,2,5],11),3)
        self.assertEqual(D.coinChange([2],3),-1)
        self.assertEqual(D.coinChange([1],10000),10000)
        self.assertEqual(D.lengthOfLIS(list(range(2500))),2500)
        self.assertEqual(D.mincostTickets([1,4,6,7,8,20],[2,7,15]),11)
        self.assertEqual(D.mincostTickets(list(range(1,366)),[2,7,15]),187)
        self.assertEqual(D.maximumAmount([5,3,7,10]),15)

    def test_dp_against_exhaustive_choices(self):
        rng=random.Random(11)
        for _ in range(100):
            nums=[rng.randrange(6) for _ in range(rng.randrange(9))]
            subsets=[(mask,[nums[i] for i in range(len(nums)) if mask>>i&1]) for mask in range(1<<len(nums))]
            self.assertEqual(D.canPartition(nums),any(2*sum(seq)==sum(nums) for _,seq in subsets))
            self.assertEqual(D.houseRobberI(nums),max(sum(seq) for mask,seq in subsets if not mask & (mask<<1)))
            self.assertEqual(D.lengthOfLIS(nums),max(len(seq) for _,seq in subsets if all(a<b for a,b in zip(seq,seq[1:]))))
            target=rng.randint(-8,8)
            self.assertEqual(D.findTargetSumWays(nums,target),sum(sum(v*sign for v,sign in zip(nums,signs))==target for signs in itertools.product((-1,1),repeat=len(nums))))
            @lru_cache(None)
            def game(i,j,turn):
                if i>j:return 0
                if turn:return max(nums[i]+game(i+1,j,False),nums[j]+game(i,j-1,False))
                return min(game(i+1,j,True),game(i,j-1,True))
            self.assertEqual(D.maximumAmount(nums),game(0,len(nums)-1,True))

    def test_miscellaneous_and_bits(self):
        self.assertEqual(M.find_plate(0),'00000')
        self.assertEqual(M.find_plate(99999),'99999')
        self.assertEqual(M.find_plate(100000),'0000A')
        self.assertEqual(M.find_plate(1000000),'000YQ')
        first_letters=sum(10**(5-i)*26**i for i in range(5))
        self.assertEqual(M.find_plate(first_letters),'AAAAA')
        self.assertEqual(M.find_plate(first_letters+26**5-1),'ZZZZZ')
        with self.assertRaises(ValueError):M.find_plate(-1)
        with self.assertRaises(ValueError):M.find_plate(first_letters+26**5)
        rng=random.Random(12)
        for _ in range(100):
            rows,cols=rng.randint(1,6),rng.randint(1,6)
            matrix=[[rng.randint(-5,5) for _ in range(cols)] for _ in range(rows)]
            a=rng.randint(1,min(rows,cols))
            expected=min(sum(matrix[r][c] for r in range(i,i+a) for c in range(j,j+a)) for i in range(rows-a+1) for j in range(cols-a+1))
            self.assertEqual(M.minimum_water(matrix,a),expected)
            x,y=rng.randrange(10000),rng.randrange(10000)
            self.assertEqual(BIT.bit_difference(x,y),bin(x^y).count('1'))


if __name__ == '__main__':
    unittest.main()
