"""Exact canonical bilingual source pairs; synthesized speech/listening is reviewed separately."""
import json
from pathlib import Path

TITLE = '计算机科学，从零搭建 · 第22部分：几何'
CHAPTERS = {'Hook': '左边、右边，还是在线上？', 'Orient': '1. 唯一的基本操作', 'Hulls': '2. 凸包', 'Sweep': '3. 扫描线', 'Gallery': '4. 守卫美术馆', 'Voronoi': '5. Voronoi 图', 'Delaunay': '6. Delaunay 三角剖分', 'Lifting': '7. 提升映射', 'Incremental': '8. 随机顺序与反向分析', 'Lp': '9. 平面上的线性规划', 'KdTree': '10. 范围查询', 'PointLocation': '11. 点定位', 'HighDim': '12. 高维空间', 'Duality': '13. 对偶与火腿三明治', 'Planning': '14. 移动机器人', 'Frontier': '15. 前沿：精确性、3SUM 与最近邻', 'Outro': '回顾、习题，以及它们会在哪里再出现'}
ZH = json.loads(Path(__file__).with_name("narration_source_zh.json").read_text())
PHRASES = {}
