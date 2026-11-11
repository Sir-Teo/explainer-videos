"""Exact canonical bilingual source pairs; speech/listening remains separate."""
import json
from pathlib import Path

TITLE = '计算机科学，从零搭建 · 第20部分：作为资源的随机性'
CHAPTERS = {'Hook': '几千字节里的高频词', 'LasVegas': '1. 拉斯维加斯与蒙特卡洛', 'Freivalds': '2. 用硬币检验乘积', 'Identity': '3. 这个多项式是零吗？', 'Karger': '4. 用收缩求最小割', 'Primes': '5. 可能素数与素性检验', 'Walks': '6. 求解 SAT 的随机游走', 'Bins': '7. 球与箱，以及两个选择的力量', 'Bloom': '8. 布隆过滤器', 'Stream': '9. 数据流：一遍扫描，很少的内存', 'JobSketch': '10. 几千字节里的作业：账本第9行', 'Distinct': '11. 统计不同元素：HyperLogLog', 'Ams': '12. 为二阶矩画草图', 'Lsh': '13. 近似重复：MinHash 与 LSH', 'ProbMethod': '14. 概率方法', 'Derand': '15. 去掉硬币，以及硬币从哪里来', 'Frontier': '16. 前沿：随机性有用吗？', 'Outro': '回顾、习题，以及它们会在哪里再出现'}
ZH = json.loads(Path(__file__).with_name("narration_source_zh.json").read_text())
PHRASES = {"once": "一次"}
