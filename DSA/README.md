# DSA practice guide

The [tracker](leetcode_progress.md) contains **131 implemented exercises across 14 topic files**. “Done” records implementation, not interview readiness. This is a broad preparation set; it cannot guarantee the questions an interviewer will choose.

## What was added

| Exercise | File | Main idea |
| --- | --- | --- |
| Group Anagrams | [Arrays](01_Arrays_Hashing.py) | Group by a canonical key |
| Sort Colors | [Two pointers](02_TwoPointers_SlidingWindow.py) | Maintain three partitions in place |
| Reverse Linked List | [Linked lists](06_LinkedList.py) | Save the next node before reversing a pointer |
| Valid Parentheses | [Stacks and tries](14_Stacks_Tries.py) | Match against the latest opening bracket |
| Min Stack | [Stacks and tries](14_Stacks_Tries.py) | Store the minimum at each stack depth |
| Implement Trie | [Stacks and tries](14_Stacks_Tries.py) | Share prefixes; distinguish words from prefixes |

The requested **2D prefix-sum matrix** is `NumMatrix` in the arrays file. Preorder/postorder tree construction and merging two BSTs are now implemented as well.

## Practice order for the remaining week

1. **Arrays and strings:** Two Sum, Group Anagrams, Longest Consecutive Sequence, Subarray Sum Equals K, NumMatrix, longest substring without repeats, Sort Colors.
2. **Pointers, stacks, and intervals:** Reverse Linked List, cycle detection, merge lists, Valid Parentheses, Min Stack, Daily Temperatures, Merge Intervals.
3. **Search and heaps:** binary search boundaries, rotated-array search, Koko Eating Bananas, top-k frequencies, kth largest, merge k sorted lists.
4. **Trees and graphs:** level order, BST validation, LCA, Number of Islands, Rotting Oranges, Course Schedule; then shortest-path and union-find revision.
5. **State and DP:** LRU Cache, RandomizedSet, House Robber, Coin Change, Word Break, LIS. Revise Trie after the core patterns.
6. **Timed practice:** solve two unfamiliar easy/medium variants, explain complexity, and test without reading these solutions. Practise reviewing an AI-generated solution separately: find a counterexample, fix it, and verify the change.

With six hours available daily and a two-hour round covering three subjects, allocate roughly **2–3 hours daily to DSA**, leaving time for system design and AI-assisted coding. This is a preparation allocation, not a prediction of the interview's internal timing. Prioritize independent solving over finishing all 131 questions.

## Correctness and performance fixes

- Fixed zero-target prefix-sum counting, zero-divisor handling, same-index reuse in sorted Two Sum, and empty-input cases in selected routines.
- Corrected binary-tree LCA, root-to-leaf path strings, linked-list splicing, and the linked-node output of heap-based list merging.
- Made RandomizedSet operations average O(1), normalized standalone function signatures, and removed unnecessary third-party typing dependencies. `MedianFinder` uses Python 3.14's native max-heap APIs.
- Reworked repeated recursive DP searches, including Coin Change, Word Break, and ticket costs; added iterative traversals for large island/region/course inputs.
- Corrected the all-letter license-plate boundary and refreshed tracker links to current definitions.

## Run the checks

From the repository root, using Python 3.14 or newer:

```sh
python3 -m unittest discover -s DSA/tests -v
```

The standard-library suite has **22 test methods** with deterministic examples, seeded randomized comparisons, exhaustive small cases, stateful reference models, pointer checks, and larger graph/DP inputs. It covers all topic files, including every rectangle in several small matrices. Tests passed on Python 3.14. Passing tests is evidence for the tested cases, not proof for every input.

## Input and output contracts

- Follow each linked problem's normal constraints unless a function explicitly adds behavior: valid indices, rectangular matrices, sorted inputs where required, and valid tree traversals with distinct values for reconstruction.
- Functions are standalone study implementations. Online judges may require wrapping them in `Solution` and adapting method names or node classes. `employeeFreeTime` returns interval pairs; `inorder` and `mergeTwoBST` return value lists; `mergeKSortedLists` returns a linked-list head and reuses disjoint input nodes.
- Stack reads/pops, RandomizedSet sampling, and median queries require data. Time-based designs assume the timestamp ordering specified by their problems. Bit-difference inputs are nonnegative integers.
- Several tree and backtracking solutions remain recursive. Very deep skewed trees can exceed Python's recursion limit; explain or implement an explicit-stack variant when depth is unbounded. The inorder-based reconstruction routines also use slicing and can take quadratic time on skewed trees.
- Some routines intentionally mutate arrays, grids, or list pointers. Use fresh inputs or copies when comparing solutions.

## Python 3.14 annotations

The solutions target Python 3.14+. Function annotations are deferred by default, so the files omit `from __future__ import annotations`. Local state and instance attributes have explicit annotations, including optional node pointers and container element types. Loop/comprehension variables inherit their inferred types from the typed iterable; reassignments reuse the original declaration. Annotations document types rather than enforce them at runtime. See [Python 3.14 annotation changes](https://docs.python.org/3.14/whatsnew/3.14.html#pep-649-pep-749-deferred-evaluation-of-annotations).

## Static type checks (Pylance/Pyright)

The root `pyrightconfig.json` selects Python 3.14 and standard type checking for every DSA solution and test helper. Run from the repository root:

```sh
npx --yes --package pyright@1.1.414 pyright --project pyrightconfig.json
python3 -m unittest discover -s DSA/tests -v
```

Checked with Pyright 1.1.414: zero errors and warnings. Optional pointers are narrowed before access; explicit checks raise `RuntimeError` for broken internal algorithm invariants, while invalid removal/splice bounds raise `ValueError`. The nested-integer interface is supplied by the judge and its local stubs explicitly raise `NotImplementedError`. Runtime tests and type checks verify different things; run both after edits. No diagnostic suppressions are used.
