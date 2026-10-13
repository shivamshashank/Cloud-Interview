# Python interview guide

A generic reference for software-engineering interviews: short answers, examples, common mistakes, and follow-up questions. Covers the main language and practical coding topics; specialized libraries are outside this guide.

**Baseline:** this repository targets Python 3.14+. Implementation-specific points explicitly say CPython.

**How to study:** explain each answer aloud in 2–3 points, predict the example, then write a small variation without looking.

## Contents

1. [Objects, types, mutability, and copying](#1-objects-types-mutability-and-copying)
2. [Collections, strings, and operators](#2-collections-strings-and-operators)
3. [Functions, args, kwargs, and scope](#3-functions-args-kwargs-and-scope)
4. [Classes, self, init, and inheritance](#4-classes-self-init-and-inheritance)
5. [Dataclasses and type hints](#5-dataclasses-and-type-hints)
6. [Decorators and closures](#6-decorators-and-closures)
7. [Iterators, generators, and comprehensions](#7-iterators-generators-and-comprehensions)
8. [Exceptions, context managers, and files](#8-exceptions-context-managers-and-files)
9. [Modules, environments, and packaging](#9-modules-environments-and-packaging)
10. [Memory, performance, and the GIL](#10-memory-performance-and-the-gil)
11. [Threads, processes, and async](#11-threads-processes-and-async)
12. [Testing, debugging, and practical Python](#12-testing-debugging-and-practical-python)
13. [Predict-the-output questions](#13-predict-the-output-questions)
14. [Practice tasks and revision order](#14-practice-tasks-and-revision-order)

## 1. Objects, types, mutability, and copying

### What kind of language is Python?

- Python is dynamically typed: objects have types, and a name can be rebound to a different type.
- It is strongly typed: unrelated types are not generally combined implicitly; `"3" + 2` raises `TypeError`.
- CPython compiles source to bytecode and executes it in an interpreter. “Interpreted” does not mean there is no compilation.

### What are mutable and immutable objects?

- **Mutable:** contents can change without replacing the object. Examples: `list`, `dict`, `set`, `bytearray`.
- **Immutable:** the object's value cannot change after creation. Examples: `int`, `float`, `bool`, `str`, `tuple`, `bytes`, `frozenset`, `None`.
- Immutability is not recursive: a tuple can contain a mutable list. The tuple's references stay fixed while the list changes.

```python
a = [1, 2]
b = a
b.append(3)
if a != [1, 2, 3]:
    raise RuntimeError('Example produced an unexpected result')

x = 10
y = x
x += 1                   # Rebind x; do not mutate the integer 10.
if (x, y) != (11, 10):
    raise RuntimeError('Example produced an unexpected result')

pair = ([1], 2)
pair[0].append(3)
if pair != ([1, 3], 2):
    raise RuntimeError('Example produced an unexpected result')
```

### Does Python pass by value or reference?

- A useful description is **call by sharing**: the parameter becomes another name for the supplied object.
- Mutating a shared mutable object is visible to the caller. Rebinding a local parameter is not.
- This explains why `items.append(x)` changes the caller's list but `items = []` does not replace it.

```python
def update(items):
    items.append(2)
    items = [99]

values = [1]
update(values)
if values != [1, 2]:
    raise RuntimeError('Example produced an unexpected result')
```

### What is the difference between `==` and `is`?

- `==` compares equality, potentially using `__eq__`; `is` checks whether references identify the same object.
- Use `value is None`. Use `==` for strings, numbers, and collection contents.
- Integer caching and string interning are not a reason to use identity for value comparisons.

### Assignment, shallow copy, and deep copy?

- Assignment creates another reference. A shallow copy creates a new outer container but shares nested objects.
- `copy.deepcopy` recursively copies supported objects, tracking already-copied objects to handle cycles and preserve shared relationships.
- Deep copy can be expensive and is not a universal way to copy resources such as files or database connections.

```python
from copy import deepcopy

original = [[1], [2]]
shallow = original.copy()
deep = deepcopy(original)
original[0].append(9)
if shallow != [[1, 9], [2]]:
    raise RuntimeError('Example produced an unexpected result')
if deep != [[1], [2]]:
    raise RuntimeError('Example produced an unexpected result')
```

### What makes an object hashable?

- Its hash must remain stable while used as a key; equal objects must have equal hashes. Unequal objects may collide.
- Lists, dictionaries, and sets are unhashable. A tuple is hashable only when every element is hashable.
- Hashable does not always mean immutable: ordinary user objects default to identity-based equality and hashing. Defining value equality requires careful hash design.

## 2. Collections, strings, and operators

### When should I use each collection?

| Type | Properties | Typical use |
| --- | --- | --- |
| `list` | Ordered, mutable, duplicates allowed | Dynamic sequence or stack |
| `tuple` | Ordered, immutable sequence | Fixed record or composite key if hashable |
| `dict` | Insertion-ordered key/value mapping | Lookup, grouping, frequency tracking |
| `set` | Unique hashable elements, no positional indexing | Membership and deduplication |
| `frozenset` | Immutable set | A set used as a key |
| `deque` | Efficient operations at both ends | BFS queue or sliding window |

Dictionary insertion order is guaranteed in Python 3.7+. Sets do not promise insertion order; sort explicitly when order matters.

### Which operations are expensive?

| Operation | Usual complexity in CPython |
| --- | --- |
| List index / assignment | O(1) |
| List append / pop from end | Amortized O(1) / O(1) |
| List insert or pop at front | O(n) |
| Membership in a list | O(n) |
| Dictionary/set lookup, insert, delete | Average O(1), worst O(n) |
| List slice of k elements | O(k) time and extra space |
| Sorting n elements | O(n log n) worst-case comparisons |
| Heap push/pop | O(log n) |
| Deque append/pop at either end | O(1) |

These assume bounded-cost keys/comparisons. Hashing long strings or comparing large objects can add work.

### `sort()` versus `sorted()`?

- `items.sort()` changes a list and returns `None`; `sorted(iterable)` creates a new list.
- Both are stable: items with equal sort keys keep their relative order. Use `key=` to express ordering.
- `reverse=True` reverses the ordering; it does not change the stability guarantee.

```python
records = [("b", 2), ("a", 2), ("c", 1)]
if sorted(records, key=lambda item: item[1]) != [('c', 1), ('b', 2), ('a', 2)]:
    raise RuntimeError('Example produced an unexpected result')
```

### Common operations and mistakes

- `append(x)` adds one object; `extend(iterable)` adds its elements. `remove(x)` deletes the first equal value; `pop(i)` removes and returns an indexed element.
- `d.get(key, default)` does not insert; `d.setdefault(key, default)` inserts when absent. `defaultdict(factory)` creates missing values on `d[key]` access.
- `zip` stops at the shortest iterable by default; `zip(..., strict=True)` raises on unequal lengths in Python 3.10+. `enumerate` supplies index/value pairs.

```python
from collections import Counter, defaultdict, deque

if Counter('banana')['a'] != 3:
    raise RuntimeError('Example produced an unexpected result')
groups = defaultdict(list)
groups["fruit"].append("apple")
queue = deque([1, 2])
if queue.popleft() != 1:
    raise RuntimeError('Example produced an unexpected result')
if list(enumerate(['a', 'b'], start=1)) != [(1, 'a'), (2, 'b')]:
    raise RuntimeError('Example produced an unexpected result')
```

### Strings, bytes, and slicing

- `str` stores Unicode text; `bytes` stores byte values. Encode text to bytes and decode bytes using an explicit encoding such as UTF-8.
- Strings are immutable. Prefer `"".join(parts)` when building many pieces; repeated concatenation can cause repeated copying.
- `a[start:stop:step]` excludes `stop`; negative indices count from the end. A string's length counts Unicode code points, not necessarily user-perceived characters.

```python
text = "café"
if text.encode('utf-8').decode('utf-8') != text:
    raise RuntimeError('Example produced an unexpected result')
if 'python'[::-1] != 'nohtyp':
    raise RuntimeError('Example produced an unexpected result')
if '-'.join(['a', 'b']) != 'a-b':
    raise RuntimeError('Example produced an unexpected result')
```

### Truthiness and numerical traps

- `None`, zero, and empty built-in containers are false; other objects normally are true unless they customize `__bool__` or `__len__`.
- `and` and `or` short-circuit and return operands, not necessarily booleans. `x or default` replaces valid false values too; use an explicit `None` check when appropriate.
- `/` is true division; `//` floors, so `-3 // 2 == -2`. Floating-point decimal values can be inexact; use `math.isclose` for approximate comparison and `Decimal` for suitable decimal arithmetic.

## 3. Functions, args, kwargs, and scope

### What are `*args` and `**kwargs`?

- In a definition, `*args` collects extra positional arguments into a tuple; `**kwargs` collects extra keyword arguments into a dictionary.
- At a call site, `*values` expands an iterable into positional arguments; `**options` expands a mapping with string keys into keyword arguments.
- The names `args` and `kwargs` are conventions. The stars provide the behavior. Prefer explicit parameters when the interface is known.

```python
def describe(name, *tags, active=True, **metadata):
    return name, tags, active, metadata

if describe('job', 'fast', owner='me') != ('job', ('fast',), True, {'owner': 'me'}):
    raise RuntimeError('Example produced an unexpected result')
options = {"active": False}
if describe(*['job', 'batch'], **options)[2] is not False:
    raise RuntimeError('Example produced an unexpected result')
```

### Positional-only and keyword-only arguments?

- Parameters before `/` are positional-only; those after bare `*` or `*args` are keyword-only.
- Use keyword-only parameters for flags whose meaning should be visible at the call site.
- Supplying one parameter twice, positionally and by keyword, raises `TypeError`. See [function argument rules](https://docs.python.org/3.14/tutorial/controlflow.html#more-on-defining-functions).

```python
def connect(host, /, port=443, *, timeout=5):
    return host, port, timeout

if connect('localhost', timeout=2) != ('localhost', 443, 2):
    raise RuntimeError('Example produced an unexpected result')
```

### Why are mutable default arguments dangerous?

- Defaults are evaluated when the function is defined, not separately for every call.
- A default list can accidentally accumulate state across calls. Use `None`, then create a list inside.
- This applies to dictionaries and other mutable objects too; immutable defaults are usually straightforward.

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

if add_item(1) != [1]:
    raise RuntimeError('Example produced an unexpected result')
if add_item(2) != [2]:
    raise RuntimeError('Example produced an unexpected result')
```

### What is LEGB scope?

- Name lookup generally follows **Local → Enclosing function → Global module → Builtins**.
- Assignment normally makes a name local. `global` targets the module binding; `nonlocal` targets an existing enclosing function binding.
- Reading a name before assigning to that local name causes `UnboundLocalError`. Prefer explicit parameters and returned values over unnecessary global state.

### Are functions objects? What is a lambda?

- Functions can be assigned, passed as arguments, returned, and stored in containers; these are first-class functions.
- A higher-order function accepts or returns functions. `lambda` defines a small anonymous function containing one expression.
- Prefer a named `def` for complex behavior, useful documentation, or clearer tracebacks. Returning `a, b` returns one tuple; no explicit return means `None`.

## 4. Classes, self, init, and inheritance

### What are a class, object, `self`, and `__init__`?

- A class defines behavior and a construction interface; an instance is an object created from it. `self` conventionally names the current instance in an instance method.
- Calling `obj.method(x)` normally supplies `obj` as the first argument automatically. `self` is not a keyword.
- `__init__` initializes an already-created instance and must return `None`; `__new__` creates/returns the instance. Most application classes only customize `__init__`.

```python
class Counter:
    def __init__(self, start=0):
        self.value = start

    def increment(self):
        self.value += 1
        return self.value

counter = Counter(4)
if counter.increment() != 5:
    raise RuntimeError('Example produced an unexpected result')
if Counter.increment(counter) != 6:
    raise RuntimeError('Example produced an unexpected result')
```

### Class variables versus instance variables?

- Class attributes are available through the class and shared through attribute lookup. Instance attributes represent individual state.
- Putting a mutable list on the class can accidentally share it across all instances.
- Assignment such as `self.count = 1` usually creates/shadows an instance attribute rather than changing the class attribute.

```python
class Team:
    category = "engineering"

    def __init__(self):
        self.members = []

a, b = Team(), Team()
a.members.append("A")
if b.members != []:
    raise RuntimeError('Example produced an unexpected result')
```

### Instance method, class method, static method?

| Kind | Automatic first argument | Use |
| --- | --- | --- |
| Instance method | `self`, the instance | Read/change instance state |
| `@classmethod` | `cls`, the class | Alternative constructors supporting subclasses |
| `@staticmethod` | None | Related utility requiring no instance/class state |

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    @classmethod
    def from_text(cls, text):
        x, y = map(int, text.split(","))
        return cls(x, y)

    @staticmethod
    def valid_coordinate(value):
        return isinstance(value, int)

if Point.from_text('2,3').x != 2:
    raise RuntimeError('Example produced an unexpected result')
if not Point.valid_coordinate(4):
    raise RuntimeError('Example produced an unexpected result')
```

### Inheritance, polymorphism, and composition?

- Inheritance expresses an “is-a” relationship; overriding replaces inherited behavior. Python commonly uses duck typing: behavior matters more than explicit ancestry.
- Composition puts collaborating objects inside another object; it often makes responsibilities and testing clearer than deep inheritance.
- `super()` follows the method resolution order, including in multiple inheritance; it does not simply mean “call my named parent.” Inspect `Class.__mro__` when necessary.

### Encapsulation, properties, and naming?

- `_name` means non-public by convention. `__name` triggers name mangling to reduce subclass collisions; it is not access security.
- `@property` exposes a method as attribute access; a setter can validate updates. Keep expensive or surprising operations explicit.
- Python does not provide Java-style signature overloading by repeatedly defining the same method name: the later definition replaces the earlier binding.

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

if Temperature(20).celsius != 20:
    raise RuntimeError('Example produced an unexpected result')
```

### What are dunder methods and protocols?

| Method | Meaning |
| --- | --- |
| `__repr__`, `__str__` | Developer-facing and user-facing representation |
| `__eq__`, `__hash__` | Equality and hashing |
| `__len__`, `__bool__` | Length and truthiness |
| `__iter__`, `__next__` | Iteration |
| `__getitem__`, `__contains__` | Subscription and membership |
| `__call__` | Make an instance callable |
| `__enter__`, `__exit__` | Context-manager behavior |

A protocol describes supported operations. `len(obj)` delegates to the relevant special method. See the [Python data model](https://docs.python.org/3.14/reference/datamodel.html).

**Advanced follow-up:** a descriptor customizes attribute access through methods such as `__get__` and `__set__`; properties are descriptors. A metaclass controls class creation; `type` is the usual metaclass. Know these definitions, but prioritize ordinary classes first.

## 5. Dataclasses and type hints

### What is a dataclass?

- `@dataclass` generates common methods, including initialization, representation, and field-based equality by default.
- Use `field(default_factory=list)` for a fresh mutable field per instance; use `__post_init__` for additional initialization or validation.
- `frozen=True` blocks normal field assignment, not mutation inside nested objects. `slots=True` can reduce instance overhead. Dataclasses do not enforce annotated types. See [dataclass behavior](https://docs.python.org/3.14/library/dataclasses.html).

```python
from dataclasses import dataclass, field

@dataclass
class Job:
    name: str
    retries: int = 0
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.retries < 0:
            raise ValueError("retries must be nonnegative")

a, b = Job("a"), Job("b")
a.tags.append("urgent")
if b.tags != []:
    raise RuntimeError('Example produced an unexpected result')
if Job('a') != Job('a'):
    raise RuntimeError('Example produced an unexpected result')
```

**Hashing follow-up:** with default equality and mutable fields, dataclass instances are normally unhashable. `frozen=True` with equality normally generates hashing, but hashing still fails if a participating field is unhashable. Do not force `unsafe_hash=True` casually.

### Why is no future import needed in Python 3.14?

- Python 3.14 defers function, class, and module annotations by default, so forward references generally do not need quotes or `from __future__ import annotations`.
- Local annotations such as `ans: list[int] = []` and `curr: ListNode | None = head` document expected types; Python does not require these declarations or enforce their types at runtime.
- Annotation readers can still trigger evaluation, so referenced names must then be resolvable. See [the Python 3.14 changes](https://docs.python.org/3.14/whatsnew/3.14.html#pep-649-pep-749-deferred-evaluation-of-annotations).

### Why use type hints?

- Annotations document interfaces and help static checkers and editors; they do not generally validate inputs at runtime.
- `str | None` means a string or `None`; it does not itself make a function argument optional to supply. A default value does that.
- `Any` permits unchecked operations; `object` means an arbitrary object whose operations must be narrowed before use. Avoid spreading `Any` through otherwise typed code.

```python
def first_name(names: list[str]) -> str | None:
    return names[0] if names else None

if first_name([]) is not None:
    raise RuntimeError('Example produced an unexpected result')
```

### `TypedDict`, `Protocol`, ABC, or dataclass?

- `TypedDict` describes dictionary keys for static checking; a dataclass constructs class instances with fields and methods.
- `Protocol` describes structural interfaces: compatible behavior can satisfy them without explicit inheritance.
- An abstract base class can require methods through `@abstractmethod` and prevent instantiation until implemented. Choose it when an explicit inheritance contract helps.

## 6. Decorators and closures

### What is a decorator?

- A decorator receives a function or class and returns its replacement, often adding behavior around an existing function.
- `@decorate` above `def f` is effectively `f = decorate(f)`. Uses include logging, authorization, metrics, caching, and registration.
- Use `functools.wraps` when wrapping functions to preserve metadata and expose the wrapped function for inspection.

```python
from functools import wraps

def require_positive(func):
    @wraps(func)
    def wrapper(value, *args, **kwargs):
        if value <= 0:
            raise ValueError("value must be positive")
        return func(value, *args, **kwargs)
    return wrapper

@require_positive
def double(value):
    return value * 2

if double(3) != 6:
    raise RuntimeError('Example produced an unexpected result')
if double.__name__ != 'double':
    raise RuntimeError('Example produced an unexpected result')
```

### How do parameterized and stacked decorators work?

- A parameterized decorator adds an outer function: configuration → decorator → wrapper.
- `@a` above `@b` produces `a(b(function))`; on invocation, an ordinary outer wrapper runs first.
- Async functions need async-aware wrappers if behavior must surround awaited execution. A sync wrapper may only surround coroutine creation.

### What is a closure? What is late binding?

- A closure retains access to names from its enclosing function scope after that function returns.
- Captured names are generally looked up when called, which surprises people creating lambdas in loops.
- Capture the current value with a default argument or create a separate enclosing function for each value.

```python
def multiplier(factor):
    def multiply(value):
        return value * factor
    return multiply

if multiplier(3)(4) != 12:
    raise RuntimeError('Example produced an unexpected result')
functions = [lambda i=i: i for i in range(3)]
if [func() for func in functions] != [0, 1, 2]:
    raise RuntimeError('Example produced an unexpected result')
```

### When should I cache a function?

- `functools.cache` is unbounded memoization; `lru_cache(maxsize=...)` bounds stored entries.
- Arguments must be hashable. Cache deterministic results when reusing them is valid; think about invalidation and memory.
- Avoid caching mutable return objects that callers modify, side-effecting operations, or live coroutine objects.

## 7. Iterators, generators, and comprehensions

### Iterable versus iterator versus generator?

- An iterable can supply an iterator through `iter(...)`. An iterator returns successive items through `next(...)` and raises `StopIteration` when exhausted.
- A generator is an iterator created by a generator function or expression; it computes values lazily and preserves suspended execution state.
- A generator is usually single-use. Laziness saves materialization memory but can retain referenced objects and delay errors.

```python
def squares(limit):
    for value in range(limit):
        yield value * value

generator = squares(3)
if next(generator) != 0:
    raise RuntimeError('Example produced an unexpected result')
if list(generator) != [1, 4]:
    raise RuntimeError('Example produced an unexpected result')
if list(generator) != []:
    raise RuntimeError('Example produced an unexpected result')
```

### `yield`, `return`, and `yield from`?

- `yield` produces a value and pauses; `return` ends the function. A function containing `yield` returns a generator when called.
- `yield from iterable` delegates iteration and the generator protocol to another iterable/generator.
- Use generators for streaming records or transformations; use a list when repeated traversal or indexing is necessary.

### Comprehensions versus `map` and `filter`?

- List/set/dict comprehensions eagerly build a collection. Generator expressions are lazy.
- `map` and `filter` return lazy iterators in Python 3. A comprehension is often easier to read for a small transformation plus condition.
- Avoid deeply nested comprehensions and comprehensions used only for side effects.

```python
if [x * x for x in range(5) if x % 2 == 0] != [0, 4, 16]:
    raise RuntimeError('Example produced an unexpected result')
if sum((x * x for x in range(3))) != 5:
    raise RuntimeError('Example produced an unexpected result')
if {word: len(word) for word in ['hi', 'python']} != {'hi': 2, 'python': 6}:
    raise RuntimeError('Example produced an unexpected result')
```

## 8. Exceptions, context managers, and files

### How do `try`, `except`, `else`, and `finally` work?

- `except` handles matching exceptions; `else` runs if the `try` suite completes normally; `finally` performs cleanup when leaving the construct during normal interpreter execution.
- Catch specific exceptions and preserve useful context with `raise NewError(...) from exc`. Bare `raise` reraises the current exception.
- Avoid returning from `finally`, which can hide errors or replace a return value. `except Exception` does not catch every `BaseException`, such as `KeyboardInterrupt`.

```python
def parse_count(text):
    try:
        count = int(text)
    except ValueError as exc:
        raise ValueError("count must be an integer") from exc
    if count < 0:
        raise ValueError("count must be nonnegative")
    return count

if parse_count('3') != 3:
    raise RuntimeError('Example produced an unexpected result')
```

### What is a context manager?

- `with` manages resource entry/exit, including cleanup when the block raises. Common examples are files, locks, and database transactions.
- It uses `__enter__` and `__exit__`; a truthy return from `__exit__` suppresses a block exception.
- `contextlib.contextmanager` offers a generator-based form with one `yield` and cleanup in `finally`.

```python
from contextlib import contextmanager

@contextmanager
def tracked_resource(events):
    events.append("open")
    try:
        yield "resource"
    finally:
        events.append("close")

events = []
with tracked_resource(events) as resource:
    if resource != 'resource':
        raise RuntimeError('Example produced an unexpected result')
if events != ['open', 'close']:
    raise RuntimeError('Example produced an unexpected result')
```

### File and serialization essentials

- Open text with an explicit encoding, for example `with open(path, encoding="utf-8") as handle:`. Iterate large files instead of reading everything at once.
- JSON handles a limited data model and needs explicit adaptation for objects such as datetimes; use `json.loads`/`dumps`, not `eval`.
- Pickle is Python-specific and can execute code while loading: never unpickle untrusted data. Prefer `pathlib` for portable path manipulation.

## 9. Modules, environments, and packaging

### Module versus package? Why the main guard?

- A module provides a namespace, often from one `.py` file. A package organizes modules; regular packages use `__init__.py`, while namespace packages can omit it.
- Imports execute module-level code on first loading and ordinarily cache the module in `sys.modules`. Avoid expensive or surprising import-time side effects.
- `if __name__ == "__main__":` keeps script entry behavior separate from importing. Circular imports often indicate responsibilities that should be separated.

### How do you manage dependencies?

- Create a project environment with `python -m venv .venv`; use `python -m pip` to target the selected interpreter.
- `pyproject.toml` commonly stores project/build/tool configuration. Use an appropriate lock or pinned requirements workflow for reproducible dependency resolution.
- A virtual environment isolates Python packages, not the whole operating system. Do not name files `json.py`, `typing.py`, or other names that shadow needed modules.

## 10. Memory, performance, and the GIL

### How is memory managed?

- CPython primarily uses reference counting and also collects unreachable reference cycles. Other Python implementations may differ.
- `del name` removes a binding; it does not guarantee immediate destruction of the object. Other references may remain.
- Use context managers for deterministic resource cleanup. `sys.getsizeof` generally measures the object itself, not the entire reachable object graph.

### What is the GIL?

- In a standard GIL-enabled CPython build, one thread at a time executes Python bytecode; blocking I/O and some native libraries can release the lock.
- This limits parallelism for pure-Python CPU work, but does not make compound shared-state operations safe.
- Optional free-threaded builds can disable the GIL; behavior depends on the build and extensions. Avoid saying all Python always has a GIL. See [threading and the GIL](https://docs.python.org/3.14/library/threading.html#gil-and-performance-considerations).

### How do you optimize Python?

- Measure first using tools such as `timeit`, `cProfile`, and `tracemalloc`; identify algorithmic, I/O, and allocation bottlenecks separately.
- Improve data structures and complexity before small syntax changes. Use sets for repeated membership, deque for BFS, and generators for streaming.
- `__slots__` can reduce per-instance storage and restrict extra attributes in suitable classes; it is not a universal speed improvement or immutability mechanism.

## 11. Threads, processes, and async

| Approach | Useful for | Main tradeoff |
| --- | --- | --- |
| Threads | Blocking I/O and shared-memory coordination | Locks/races; ordinary GIL limits pure-Python CPU parallelism |
| Processes | CPU-heavy Python work across cores | Startup, memory, and interprocess serialization costs |
| Asyncio | Many waiting operations with async-compatible libraries | Blocking calls stall the event-loop thread |

### What do `async`, `await`, and tasks mean?

- Calling `async def` creates a coroutine object; it does not automatically run it. Await it or schedule it as a task.
- `await` can suspend the current coroutine while another task progresses. It does not turn CPU work into parallel execution.
- Tasks schedule coroutines on an event loop. Use bounded concurrency, timeouts, and cancellation cleanup; Python 3.11+ `TaskGroup` provides structured task management. See [asyncio tasks](https://docs.python.org/3.14/library/asyncio-task.html).

```python
import asyncio

async def double_later(value):
    await asyncio.sleep(0)
    return value * 2

async def main():
    return await asyncio.gather(double_later(2), double_later(3))

if asyncio.run(main()) != [4, 6]:
    raise RuntimeError('Example produced an unexpected result')
```

### How do you avoid concurrency bugs?

- Protect compound shared-state invariants with locks or transfer ownership through queues. Do not rely on apparent atomicity of an expression.
- Use `asyncio.sleep` inside async code; move appropriate blocking I/O to `asyncio.to_thread`. Keep CPU-heavy Python work out of the event-loop thread.
- Cancellation should trigger cleanup and normally propagate. Avoid swallowing it; async tasks can race around `await` even on one thread.

**Process follow-up:** process workers often require serializable arguments and importable functions. Protect script entry with the main guard and avoid assuming every platform/version starts processes the same way.

## 12. Testing, debugging, and practical Python

### How do you test a function?

- Cover normal behavior, empty/boundary values, invalid inputs, duplicate values, and relevant state transitions.
- Compare optimized algorithms with a small brute-force reference; use deterministic random seeds for reproducible examples.
- Mock external boundaries rather than the algorithm itself. Patch the name where the code under test looks it up.

### How should explicit validation work?

- Use an `if` check and raise `ValueError` for invalid input or `RuntimeError` for a broken internal assumption.
- These checks remain active during optimized execution. A check for `None` also lets Pylance narrow an optional type before attribute access.
- Return an empty result only when that is expected behavior; otherwise raise an exception that explains the violated condition.

### Logging, debugging, and API handling?

- Use structured, contextual logging and suitable severity levels; `logger.exception(...)` includes the active exception traceback.
- Reduce a bug to a reproducible case, inspect the traceback, and use a debugger before changing unrelated code.
- For network clients, set timeouts, distinguish transient/permanent failures, retry only where safe, and handle pagination and malformed responses. Keep credentials out of logs.

### What should you inspect in AI-generated Python?

- Check assumptions, mutation, complexity, shared defaults, resource cleanup, and whether a claimed library API actually exists in the target version.
- Verify return types, async usage, exception handling, and boundary cases with executable examples.
- Run formatting/static checks and relevant tests; independently explain why the implementation works before accepting it.

## 13. Predict-the-output questions

### Q1. What happens with a shared default?

```python
def collect(value, bucket=[]):
    bucket.append(value)
    return bucket

if collect(1) != [1]:
    raise RuntimeError('Example produced an unexpected result')
if collect(2) != [1, 2]:
    raise RuntimeError('Example produced an unexpected result')
```

- The same default list is reused between calls.
- Fix it with `bucket=None` and allocate inside the function.

### Q2. Why do all matrix rows change?

```python
matrix = [[0] * 2] * 3
matrix[0][0] = 9
if matrix != [[9, 0], [9, 0], [9, 0]]:
    raise RuntimeError('Example produced an unexpected result')
```

- Multiplication repeated references to the same inner list.
- Build independent rows with `[[0] * 2 for _ in range(3)]`.

### Q3. What do loop-created lambdas return?

```python
functions = [lambda: i for i in range(3)]
if [func() for func in functions] != [2, 2, 2]:
    raise RuntimeError('Example produced an unexpected result')
```

- They refer to the same captured binding, whose final value is 2.
- Use `lambda i=i: i` to capture each value as a default.

### Q4. Why is the result `None`?

```python
values = [3, 1, 2]
result = values.sort()
if result is not None:
    raise RuntimeError('Example produced an unexpected result')
if values != [1, 2, 3]:
    raise RuntimeError('Example produced an unexpected result')
```

- `sort` changes the list in place and returns `None`.
- Use `sorted(values)` when you need a new sorted list.

### Q5. Why does list `+=` differ from `+`?

```python
a = [1]
b = a
a += [2]
if b != [1, 2]:
    raise RuntimeError('Example produced an unexpected result')
a = a + [3]
if a != [1, 2, 3] or b != [1, 2]:
    raise RuntimeError('Example produced an unexpected result')
```

- For lists, `+=` extends the existing object; `+` creates a new list.
- Augmented assignment behavior depends on the operand type.

### Q6. Can two equal lists be different objects?

```python
a, b = [1], [1]
if a != b:
    raise RuntimeError('Example produced an unexpected result')
if a is b:
    raise RuntimeError('Example produced an unexpected result')
if (0 or 7) != 7:
    raise RuntimeError('Example produced an unexpected result')
if ([] and 'hello') != []:
    raise RuntimeError('Example produced an unexpected result')
```

- Equality is different from identity.
- Boolean operators short-circuit and return an operand.

## 14. Practice tasks and revision order

### First pass: essential

- Explain mutability, aliasing, shallow/deep copy, equality/identity, and hashability.
- Write a function using `*args`, `**kwargs`, a keyword-only option, and a safe mutable default.
- Build a class with `self`, `__init__`, one class method, and one property; convert a simple record into a dataclass.
- Explain a decorator, a closure, a generator, and a context manager using a short example.

### Second pass: practical depth

- Implement a bounded cache or an iterator; discuss memory and invalidation.
- Stream records from a file and handle malformed records without losing useful error context.
- Explain when to choose threads, processes, or async; identify a race and an event-loop-blocking call.
- Write tests for a stateful class and compare a DSA solution against brute force.

### Final rehearsal: answer in 2–3 points

1. Why can a tuple contain a changing list? **Its references are fixed; the referenced list is mutable.**
2. Does `self` have to be named `self`? **No; it is the standard convention. The instance is supplied automatically for bound instance methods.**
3. Is `__init__` responsible for allocating the object? **No; `__new__` creates it, then `__init__` initializes it.**
4. Does a dataclass validate types? **No; annotations describe fields. Add explicit validation when needed.**
5. Can a frozen dataclass contain mutable state? **Yes; freezing does not recursively freeze nested objects.**
6. Why preserve metadata in a decorator? **It keeps names/docs useful and supports introspection through `__wrapped__`.**
7. Can you iterate a consumed generator again? **Not to replay its values; create a new generator or materialize the values.**
8. Is async the same as parallel execution? **No; it enables cooperative concurrency, commonly while waiting for I/O.**
9. Does the GIL prevent race conditions? **No; synchronize shared invariants explicitly.**
10. What should you do before optimizing? **Measure, identify the bottleneck, then improve the relevant algorithm or operation.**

Use the [DSA collection](DSA/README.md) to practise these language concepts in actual implementations.
