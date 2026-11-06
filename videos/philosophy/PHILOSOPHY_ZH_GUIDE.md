# Chinese edition of *Philosophy, Built* (哲学，从零搭建)

Narration is translated in `videos/philosophy/philosophyN/zh_lines.py` (literal lines by their English prefix,
computed lines as templates with the source's placeholders spelled exactly), filled into `narration_zh.json` by
`python tools/zh_lines.py philosophyN`; `--todo` lists what is missing. On-screen text lives in
`videos/philosophy/philosophy_text_zh.json` (exact `strings`, `phrases` inside `\text{}` and `\textit{}`, regex
`patterns` for names and years); `python tools/collect_text.py --check philosophyN` lists what is still English, and
`python tools/collect_text.py --lang zh philosophyN` dry-runs the Chinese build.

- Spoken Mandarin, short sentences; the same content and order as the English.
- Keep every `<bookmark mark='x'/>`, in order, before the words it times.
- Full-width punctuation; quotations in “”; book and paper titles in 《》; numbers as digits (第4部分, 第12章, 1920年).
- Formulas, variables and logic symbols stay as they are (p, q, B_i, □, ◇, ⊨, K3, LP, FDE, S4, GL, LTL).
- Sanskrit, Pali, Greek and Latin terms keep their romanization, in italics on screen, with a Chinese gloss on first use
  (catuṣkoṭi 四句, syādvāda 或然论, *de re* 从物).
- Code (`\texttt{...}`) stays in English.
- The Reasoner is always 推理机; the Wall 墙; the Price List 代价清单.

## Series terms

| English | 中文 |
|---|---|
| Philosophy, Built | 哲学，从零搭建 |
| the Reasoner | 推理机 |
| the Wall (a brick in the Wall) | 墙（墙上的一块砖） |
| the Price List | 代价清单 |
| minimal inconsistent set (MUS) | 极小不一致集 |
| minimal correction set (an exit) | 极小修正集（一条出路） |
| payoff: where this comes back | 这些会在哪里再出现 |

## Logic

| English | 中文 |
|---|---|
| argument, premise, conclusion | 论证，前提，结论 |
| valid, sound | 有效，可靠 |
| entailment, consequence | 衍推，后承 |
| tautology | 重言式 |
| satisfiable, unsatisfiable | 可满足，不可满足 |
| countermodel | 反模型 |
| truth table | 真值表 |
| connective | 联结词 |
| conjunction, disjunction, negation, conditional | 合取，析取，否定，条件句 |
| modus ponens | 肯定前件式 |
| modus tollens | 否定后件式 |
| disjunctive syllogism | 析取三段论 |
| excluded middle, non-contradiction | 排中律，矛盾律 |
| explosion (ex falso) | 爆炸（从假得出一切） |
| bivalence | 二值原则 |
| syllogism, mood, figure | 三段论，式，格 |
| quantifier, universal, existential | 量词，全称，存在 |
| structure, domain, interpretation | 结构，论域，解释 |
| natural deduction (Fitch) | 自然演绎（菲奇式） |
| sequent calculus | 相继式演算 |
| tableau, branch, closed, open | 表列，分支，封闭，开放 |
| completeness, soundness, compactness | 完全性，可靠性，紧致性 |
| decidable, semi-decidable | 可判定，半可判定 |
| resolution, unification | 归结，合一 |
| SAT solver, CDCL | SAT求解器，冲突驱动子句学习 |
| modal logic | 模态逻辑 |
| necessarily, possibly | 必然，可能 |
| possible world, accessibility relation | 可能世界，可及关系 |
| frame, model, valuation | 框架，模型，赋值 |
| reflexive, symmetric, transitive, Euclidean, serial | 自反，对称，传递，欧几里得，持续 |
| correspondence | 对应 |
| canonical model | 典范模型 |
| bisimulation | 互模拟 |
| filtration | 过滤 |
| strict implication | 严格蕴涵 |
| deontic logic, obligation, permission | 道义逻辑，义务，允许 |
| tense logic, temporal logic | 时态逻辑，时序逻辑 |
| model checking | 模型检测 |
| safety, liveness | 安全性，活性 |
| fixed point (least, greatest) | 不动点（最小，最大） |
| logical matrix, designated value | 逻辑矩阵，被指定的值 |
| gap, glut | 空隙，过剩 |
| paraconsistent, dialetheism | 弗协调，双面真理论 |
| relevance logic, variable sharing | 相干逻辑，变元共享 |
| first-degree entailment (FDE) | 一度衍推 |
| bilattice; truth order, information order | 双格；真值序，信息序 |
| intuitionistic logic, BHK | 直觉主义逻辑，BHK解释 |
| fuzzy set, t-norm, residuum | 模糊集，t-范数，剩余 |
| linear logic; weakening, contraction, exchange | 线性逻辑；弱化，收缩，交换 |
| quantum logic, orthocomplement | 量子逻辑，正交补 |
| logical constant, permutation invariance | 逻辑常项，置换不变性 |
| logical pluralism, monism, anti-exceptionalism | 逻辑多元论，一元论，反例外论 |

## Vagueness and paradox

| English | 中文 |
|---|---|
| the sorites (the heap, the bald man) | 谷堆悖论（谷堆，秃头者） |
| tolerance | 容忍 |
| borderline case, penumbra | 边界情形，半影区 |
| sharpening (precisification) | 精确化 |
| supervaluationism, super-true | 超赋值主义，超真 |
| degree theory | 程度论 |
| epistemicism, margin for error | 认知主义，误差余地 |
| contextualism | 语境主义 |
| higher-order vagueness, definitely | 高阶模糊，确定地 |
| nihilism | 虚无论 |
| the liar | 说谎者 |
| revenge | 复仇 |

## Traditions and terms

| English | 中文 |
|---|---|
| catuṣkoṭi (the four corners) | 四句 |
| Nāgārjuna, *Mūlamadhyamakakārikā* | 龙树，《中论》 |
| emptiness (śūnyatā) | 空 |
| the unanswered questions | 无记 |
| anekāntavāda | 非一端论 |
| syādvāda, saptabhaṅgī | 或然论，七支 |
| Mohists, School of Names | 墨家，名家 |
| Nyāya | 正理派 |
| the Master Argument | 主论证 |

## Names

| English | 中文 |
|---|---|
| Aristotle, Chrysippus, Diodorus Cronus, Eubulides | 亚里士多德，克吕西波，狄奥多罗斯·克洛诺斯，欧布利德斯 |
| Leibniz, Boole, Frege, Russell | 莱布尼茨，布尔，弗雷格，罗素 |
| Gödel, Tarski, Gentzen, Church, Turing | 哥德尔，塔斯基，根岑，丘奇，图灵 |
| Kripke, Lewis (C. I.; David), Prior, Quine | 克里普克，刘易斯（C·I；大卫），普赖尔，蒯因 |
| Łukasiewicz, Kleene, Bochvar, Post | 卢卡西维茨，克莱尼，博奇瓦尔，波斯特 |
| Belnap, Dunn, Anderson, Priest | 贝尔纳普，邓恩，安德森，普里斯特 |
| Brouwer, Heyting, Kolmogorov | 布劳威尔，海廷，柯尔莫哥洛夫 |
| Zadeh, Hájek, Girard, Lambek | 扎德，哈耶克，吉拉尔，兰贝克 |
| Fine, Williamson, Sorensen, Wright, Sainsbury | 法恩，威廉森，索伦森，赖特，塞恩斯伯里 |
| Birkhoff, von Neumann, Putnam, Dummett | 伯克霍夫，冯·诺依曼，普特南，达米特 |
| Ann, Bo, Cy, Di (the example people) | 安，博，赛，迪 |
