# Part2 used-caption Unicode control scan

No additional malformed single-backslash Unicode control symbols were found in the actual translated outputs of1,458 unique collected Part2 caption records across all16 scenes. This includes 1306 Tex/MathTex records and152 Text records;812 records changed under translation (804 Tex/MathTex). The frozen table snapshot and all inputs/outputs are preserved in `scan.json` with source collection paths and line references.

The scanner follows backslash-run parity: an odd run immediately followed by non-ASCII non-whitespace is suspicious. Thus a malformed `\（` is caught, while the corrected `\ （` control-space form and a legitimate `\\` line break are not. It scans only captions actually present in Part2 collection logs, not unrelated shared-table entries.

Both known corrected captions were also typeset independently with the project's TeX preamble and Chinese XeLaTeX/xeCJK template in a private runtime directory. Both returned exit0 and produced XDV:

- `observed DPLL decisions \ (median, log scale)` → `已观察到的DPLL决策次数\ （中位数，对数刻度）`
- `modern semi-gradient analogue: \ temporal-difference learning \ (Part 26)` → `现代半梯度对应形式：\ 时序差分学习\ （第26部分）`

`report.json`/`compile-result.json` preserve exact keys/values, TeX hashes and compiler logs. No additional repair keys are proposed. This does not compile-check every caption, rerender a chapter, verify future/uncollected numeric variants, or certify layout. No repository edits, data/model compute, synthesis-cache changes, commits or pushes.
