"""Exact canonical bilingual source pairs; listening remains a separate gate."""
import json
from pathlib import Path
TITLE = '计算机科学，从零搭建 · 第24部分：实践中的算法'
CHAPTERS = {'Hook': '同样的大 O，不同的世界', 'PrefixSums': '1. 前缀和', 'Fenwick': '2. Fenwick 树', 'SegmentTrees': '3. 线段树', 'RangeMin': '4. 区间最小值与最近公共祖先', 'Monotone': '5. 双指针与单调栈', 'Searching': '6. 搜索答案', 'Bits': '7. 比特与四个俄罗斯人算法', 'Splitting': '8. 折半搜索与平方根分块', 'Layouts': '9. 算法工程（上）：布局', 'Simd': '10. 算法工程（下）：SIMD 与哈希', 'Sorting': '11. 实践中的排序', 'Benchmarking': '12. 诚实地做基准测试', 'Craft': '13. 作为手艺的解题', 'TheJob': '14. 工程优化后的 Job', 'Frontier': '15. 前沿：学习索引与预测', 'Outro': '回顾、习题，以及它们会在哪里再出现'}
ZH = json.loads(Path(__file__).with_name("narration_source_zh.json").read_text())
PHRASES = {}
