# 📚 Algorithms Lab (DSA Journey)

A structured, topic-by-topic repository for learning, implementing, and testing fundamental **Data Structures and Algorithms (DSA)** concepts.

This project follows a progressive roadmap — starting from basic complexity analysis and building up to advanced topics like graph algorithms, dynamic programming, and benchmarking.

---

## 🚀 Purpose

This repository is designed to:

* Reinforce core DSA concepts through hands-on implementation
* Provide clean, testable Python implementations of algorithms
* Serve as a personal knowledge base and revision guide
* Track learning progress across structured topics
* Experiment with performance and optimization techniques

---

## 🧠 Topics Covered

Each folder represents a focused topic:

```
01_big-o-and-analysis/
02_arrays-and-strings/
03_hashing-and-sets/
04_two-pointers-and-sliding-window/
05_stacks-and-queues/
06_linked-lists/
07_recursion-and-backtracking/
08_sorting/
09_binary-search-and-bounds/
10_heaps-and-priority-queues/
11_trees-basics/
12_binary-search-trees/
13_graphs-basics-bfs-dfs/
14_topological-sort-and-dags/
15_shortest-paths/
16_minimum-spanning-tree-and-union-find/
17_greedy-algorithms/
18_dynamic-programming-1d/
19_dynamic-programming-2d/
20_strings-kmp-trie-rolling-hash/
21_bit-manipulation/
22_computational-geometry-basics/
23_randomized-and-approximation/
24_benchmarking-and-profiling/
```

---

## 📂 Project Structure

Each topic folder typically contains:

* **Core implementations** (algorithms & data structures)
* **Helper modules** (e.g. core nodes, utilities)
* **Tests** (`tests/` folder with unit tests)
* **Optional demos / experiments**

Example:

```
06_linked-lists/
├── linked_list_core.py
├── linked_list_ops.py
├── linked_list_patterns.py
└── tests/
    └── test_linked_lists.py
```

---

## 🧪 Running Tests

Run all tests from the project root:

```bash
python -m unittest discover -s . -p "test_*.py" -q
```

Or run tests for a specific topic:

```bash
python -m unittest 06_linked-lists.tests.test_linked_lists -q
```

---

## ⚙️ Notes on Imports

This project supports:

* running modules directly
* running tests via `unittest`

To handle both, some modules use a fallback import pattern:

```python
try:
    from .module import Something
except ImportError:
    from module import Something
```

---

## 🧰 Topics of Interest

Some highlights include:

* 🔁 Recursion & Backtracking
* ⚡ Sorting & Searching Algorithms
* 🌳 Trees & Binary Search Trees
* 🌐 Graph Algorithms (BFS, DFS, Dijkstra, MST)
* 🧠 Dynamic Programming (1D & 2D)
* 🔐 String Algorithms (KMP, Trie, Rolling Hash)
* 🎲 Randomized Algorithms
* 📊 Benchmarking & Profiling

---

## 📈 Future Improvements

* Add detailed explanations and theory per topic
* Add visualizations for algorithms
* Expand benchmarking comparisons
* Refactor into a proper Python package (optional)
* Add CLI tools for running demos

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙌 Final Notes

This is a **learning-focused repository**, not a production library.
Clarity, experimentation, and progression are prioritized over strict architecture.

---

Happy coding! 🚀
