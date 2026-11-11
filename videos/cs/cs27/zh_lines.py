"""Exact bilingual source pairs; Chinese speech/listening remains a production gate."""
import json
from pathlib import Path
TITLE = '计算机科学，从零搭建 · 第27部分：证明与随机性'
CHAPTERS = {'Hook': '不读全文的检查', 'Classes': '1. 随机复杂性类', 'Derandom': '2. 以困难换随机', 'Circuits': '3. 电路下界', 'Communication': '4. 通信复杂性', 'Interactive': '5. 交互式证明', 'Sumcheck': '6. Sum-check 与 IP = PSPACE', 'ZeroKnowledge': '7. 零知识', 'Pcp': '8. PCP 定理', 'Approx': '9. 近似的困难性', 'Ugc': '10. 唯一博弈猜想', 'FineGrained': '11. 细粒度复杂性', 'Parameterized': '12. 参数化复杂性', 'Counting': '13. 计数', 'Average': '14. 平均情形与单向函数', 'Frontier': '15. 前沿：MIP* = RE 与实践中的证明', 'Outro': '回顾、习题，以及它们会在哪里再出现'}
ZH = json.loads(Path(__file__).with_name("narration_source_zh.json").read_text())
PHRASES = {}
