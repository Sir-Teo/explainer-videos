"""Exact canonical bilingual source pairs; speech/listening remains separate."""
import json
from pathlib import Path

TITLE = '计算机科学，从零搭建 · 第19部分：伟大的范式'
CHAPTERS = {'Hook': '一百万位数字', 'Greedy': '1. 贪心，与交换论证', 'Matroid': '2. 贪心何时正确：拟阵', 'Karatsuba': '3. 三次乘法代替四次', 'Strassen': '4. 七次乘法代替八次', 'FftOne': '5. 快速傅里叶变换（上）：用值代替系数', 'FftTwo': '6. 快速傅里叶变换（下）：蝶形', 'BigMul': '7. FFT 能乘什么', 'Closest': '8. 最近点对', 'Dp': '9. 动态规划', 'Edit': '10. 编辑距离', 'Knapsack': '11. 背包问题与伪多项式时间', 'Chain': '12. 矩阵链与最优搜索树', 'TreeDp': '13. 树、图与序列上的动态规划', 'Search': '14. 回溯与舞蹈链', 'MaxSub': '15. 一个问题，四种范式', 'Frontier': '16. 前沿：乘法能有多快？', 'Outro': '回顾、习题，以及它们会在哪里再出现'}
ZH = json.loads(Path(__file__).with_name("narration_source_zh.json").read_text())
PHRASES = {}
