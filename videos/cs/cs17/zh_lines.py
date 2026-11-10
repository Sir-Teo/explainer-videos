"""Exact live Chinese narration source pairs for Part 17."""
import json
from pathlib import Path

TITLE = '计算机科学，从零搭建 · 第17部分：数据结构'
CHAPTERS = {'Hook': '计数能做到常数时间吗？', 'Dictionary': '1. 字典，以及生日界', 'Chaining': '2. 链地址法与全域哈希', 'Probing': '3. 开放寻址', 'Cuckoo': '4. 布谷鸟哈希与完美哈希', 'Bst': '5. 二叉搜索树', 'Balanced': '6. 平衡树：AVL 与红黑树', 'Randomized': '7. 树堆与跳表', 'Splay': '8. 伸展树', 'Btree': '9. B 树', 'Heaps': '10. 优先队列', 'UnionFind': '11. 并查集', 'Tries': '12. 字典树与简洁数据结构', 'Persist': '13. 持久化，以及存储层次', 'Practice': '14. 实践中的哈希表', 'Job': '15. 哈希化的任务', 'Frontier': '16. 前沿：数据结构能有多好？', 'Outro': '回顾、习题，以及它们会在哪里再出现'}
ZH = json.loads(Path(__file__).with_name("narration_source_zh.json").read_text())
PHRASES = {}
