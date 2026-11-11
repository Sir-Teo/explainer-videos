"""Exact source pairs; no stale prefix translations. Listening is a separate gate."""
import json
from pathlib import Path
TITLE = '计算机科学，从零搭建 · 第25部分：不可判定'
CHAPTERS = {'Hook': '三个问题，三条线索', 'Classes': '1. 可判定与可识别', 'Reductions': '2. 映射归约', 'Rice': '3. Rice 定理', 'Recursion': '4. 知道自己代码的程序', 'Pcp': '5. Post 对应问题', 'Tiles': '6. 铺满平面', 'Hilbert': '7. 希尔伯特第十问题', 'Godel': '8. 经由停机问题的 Gödel', 'Degrees': '9. 谕示与算术层级', 'Kolmogorov': '10. Kolmogorov 复杂度', 'Omega': '11. Chaitin 的 Omega', 'Beavers': '12. 再谈忙碌的海狸', 'Boundary': '13. 可判定性在哪里终止', 'Wild': '14. 实际系统中的不可判定性', 'Frontier': '15. 前沿：其他环上的希尔伯特第十问题', 'Outro': '回顾、习题，以及它们会在哪里再出现'}
ZH = json.loads(Path(__file__).with_name("narration_source_zh.json").read_text())
PHRASES = {}
