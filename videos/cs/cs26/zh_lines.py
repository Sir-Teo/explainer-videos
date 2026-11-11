"""Exact bilingual source pairs. Synthesized Chinese listening remains a separate gate."""
import json
from pathlib import Path
TITLE = '计算机科学，从零搭建 · 第26部分：P 与 NP'
CHAPTERS = {'Hook': '找到与检查', 'Polynomial': '1. 什么才算高效', 'Hierarchy': '2. 更多时间，更多问题', 'Np': '3. NP：答案可检查的问题', 'Reductions': '4. 归约与完全性', 'CookLevin': '5. Cook–Levin：SAT 是 NP 完全的', 'Web': '6. 归约之网', 'Everywhere': '7. 无处不在的 NP 完全性', 'Numbers': '8. 强难与弱难', 'CoNp': '9. coNP 与多项式层级', 'Space': '10. 空间：博弈与交替', 'Sqrt': '11. 平方根空间里的时间', 'Ladner': '12. 介于 P 与 NP 完全之间', 'Sat': '13. 实践中的 SAT', 'Barriers': '14. 为什么它难', 'Worlds': '15. 五个可能的世界', 'Frontier': '16. 前沿：关于复杂性的复杂性', 'Outro': '回顾、习题，以及它们会在哪里再出现'}
ZH = json.loads(Path(__file__).with_name("narration_source_zh.json").read_text())
PHRASES = {}
