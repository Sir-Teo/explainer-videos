"""Exact canonical bilingual source pairs; synthesized listening is separate."""
import json
from pathlib import Path

TITLE = '计算机科学，从零搭建 · 第23部分：优化'
CHAPTERS = {'Hook': '多面体上的最优点', 'LinearPrograms': '1. 线性规划', 'Simplex': '2. 单纯形法', 'Duality': '3. 对偶', 'KleeMinty': '4. 理论上是指数的，实践中却很快', 'PolyTime': '5. 多项式时间：椭球与中心路径', 'Unimodular': '6. 当顶点都是整数时', 'IntegerPrograms': '7. 整数规划', 'Approximation': '8. 近似：覆盖问题', 'Tsp': '9. 旅行商问题', 'MaxCut': '10. 随机超平面：最大割', 'Online': '11. 在线：看不见未来的决策', 'Weights': '12. 乘性权重', 'Convex': '13. 一页纸讲凸优化', 'Frontier': '14. 前沿：更快的线性规划、Hirsch 问题与唯一博弈猜想', 'Outro': '回顾、习题，以及它们会在哪里再出现'}
ZH = json.loads(Path(__file__).with_name("narration_source_zh.json").read_text())
PHRASES = {}
