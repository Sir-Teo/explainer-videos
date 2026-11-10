"""Exact canonical bilingual source pairs; speech/listening remains separate."""
import json
from pathlib import Path

TITLE = '计算机科学，从零搭建 · 第21部分：字符串'
CHAPTERS = {'Hook': '四种方法找 Queequeg', 'Naive': '1. 最直接的匹配', 'RabinKarp': '2. 滚动哈希', 'Kmp': '3. Knuth、Morris 与 Pratt：从不回头', 'BoyerMoore': '4. Boyer 与 Moore：向前跳', 'AhoCorasick': '5. 一次匹配许多模式', 'SuffixTree': '6. 后缀树', 'SuffixArray': '7. 后缀数组', 'Bwt': '8. Burrows–Wheeler 变换', 'FmIndex': '9. 搜索压缩文本：FM 索引', 'Lz': '10. 压缩（上）：Lempel 与 Ziv', 'Entropy': '11. 压缩（下）：给符号编码', 'Align': '12. 序列比对', 'Diff': '13. Myers 的 diff', 'Rsync': '14. 大规模的滚动哈希：rsync 与分块', 'Period': '15. 周期、回文与 Lyndon 词', 'Frontier': '16. 前沿：和信息量一样小的索引', 'Outro': '回顾、习题，以及它们会在哪里再出现'}
ZH = json.loads(Path(__file__).with_name("narration_source_zh.json").read_text())
PHRASES = {}
