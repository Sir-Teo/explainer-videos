"""Exact canonical bilingual source pairs; generated speech remains a separate review."""
import json
from pathlib import Path

TITLE = '计算机科学，从零搭建 · 第18部分：图'
CHAPTERS = {'Hook': '七座桥', 'Euler': '1. 欧拉的桥，以及怎样存储一张图', 'Bfs': '2. 广度优先搜索', 'Dfs': '3. 深度优先搜索', 'Topo': '4. 拓扑排序', 'Scc': '5. 强连通分量', 'Dijkstra': '6. 迪杰斯特拉算法', 'Bellman': '7. 负权边', 'AllPairs': '8. 全源最短路径', 'AStar': '9. 用更少搜索求精确路线', 'Mst': '10. 最小生成树', 'Flow': '11. 流与割', 'Matching': '12. 匹配', 'Hard': '13. 容易与困难', 'PageRank': '14. PageRank', 'Planar': '15. 平面图与四色', 'Frontier': '16. 注明模型与日期的研究成果', 'Outro': '回顾、习题，以及它们会在哪里再出现'}
ZH = json.loads(Path(__file__).with_name("narration_source_zh.json").read_text())
PHRASES = {'five': '五', 'four': '四', 'six': '六'}
