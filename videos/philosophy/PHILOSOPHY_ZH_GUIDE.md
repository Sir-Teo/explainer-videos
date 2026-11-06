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
| the truth-teller; the surprise exam; the knower | 真话者；突击考试；知者悖论 |
| grounded, ungrounded, paradoxical | 有根的，无根的，悖论的 |
| inclosure schema; dialetheism | 闭包模式；双面真理论 |
| propositions as types; proof assistant | 命题即类型；证明助手 |
| platonism, logicism, formalism, intuitionism | 柏拉图主义，逻辑主义，形式主义，直觉主义 |
| structuralism, fictionalism, indispensability | 结构主义，虚构主义，不可或缺性 |
| Hume's principle; Basic Law V; abstraction principle | 休谟原则；基本定律V；抽象原则 |
| impredicative, predicative; univalence | 非直谓的，直谓的；泛等 |

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
| justified true belief; Gettier case; false lemma; defeater | 得到辩护的真信念；盖蒂尔案例；假引理；挫败者 |
| reliabilism; the generality problem; sensitivity; safety | 可靠主义；普遍性问题；敏感性；安全性 |
| luminous; anti-luminosity; margin for error; the KK principle | 透明的；反透明性；误差余量；KK原则 |
| closure; contextualism; subject-sensitive invariantism | 封闭性；语境主义；主体敏感的不变论 |
| foundationalism; coherentism; infinitism | 基础主义；融贯论；无穷主义 |
| common knowledge; public announcement; the muddy children; the coordinated attack | 共同知识；公开宣告；泥孩子；协同进攻 |
| testimony; peer disagreement; equal weight; higher-order evidence | 证言；同行分歧；同等权重；高阶证据 |
| credence; coherence; probabilism; Dutch book; bookie | 信念度；融贯性；概率主义；荷兰赌；庄家 |
| accuracy; Brier score; (strictly) proper scoring rule; calibration | 准确性；布里尔评分；（严格）恰当评分规则；校准 |
| conditionalization; Jeffrey conditioning; prior; posterior; washing out | 条件化；杰弗里条件化；先验；后验；冲刷 |
| principle of indifference; maximum entropy; Bertrand's paradox | 无差别原则；最大熵；贝特朗悖论 |
| chance; the Principal Principle; admissible; the big bad bug | 机遇；主要原则；可容许的；大坏虫 |
| imprecise credence; credal set; dilation | 不精确的信念度；信度集；扩张 |
| the Lockean thesis; the lottery paradox; the preface paradox; stable belief | 洛克论题；彩票悖论；序言悖论；稳定信念 |
| Sleeping Beauty; halfer; thirder; double halfer; centred worlds | 睡美人；二分之一派；三分之一派；双重二分之一派；中心化世界 |
| SSA; SIA; the Doomsday argument; the presumptuous philosopher; reference class | 自我抽样假设；自我指示假设；末日论证；自以为是的哲学家；参照类 |
| Bayesian network; logical omniscience | 贝叶斯网络；逻辑全知 |
| null hypothesis; alternative; $p$-value; significant; power; confidence interval | 零假设；备择假设；$p$ 值；显著；功效；置信区间 |
| base rate; sensitivity; false-positive rate; PPV; the prosecutor's fallacy | 基础比率；灵敏度；假阳性率；阳性预测值（PPV）；检察官谬误 |
| the garden of forking paths; $p$-hacking; the winner's curse; replication | 分岔小径的花园；$p$ 值操纵；赢家诅咒；重复研究 |
| optional stopping; the likelihood principle; sufficiency; conditionality | 可选停止；似然原则；充分性；条件性 |
| Bayes factor; Lindley's paradox; severity; e-value; e-process; martingale | 贝叶斯因子；林德利悖论；严格性；e值；e过程；鞅 |
| cause; constant conjunction; occasionalism; INUS condition | 原因；恒常结合；偶因论；INUS条件 |
| counterfactual dependence; preemption (early, late); trumping; overdetermination | 反事实依赖；先占（早期、晚期）；压倒；过度决定 |
| screening off; prima facie cause; intervention; invariance | 屏蔽；初显原因；干预；不变性 |
| structural causal model; causal graph; chain, fork, collider; d-separation | 结构因果模型；因果图；链，叉，对撞；d分离 |
| the do-operator; back-door, front-door criterion; the do-calculus; identification | do算子；后门、前门准则；do演算；识别 |
| the ladder of causation; abduction, action, prediction; twin network | 因果之梯；溯因，行动，预测；孪生网络 |
| probability of necessity, of sufficiency (PN, PS, PNS) | 必要性概率，充分性概率（PN，PS，PNS） |
| actual causation; double prevention; bogus prevention; degree of responsibility | 实际因果；双重预防；虚假预防；责任程度 |
| causal Markov condition; faithfulness; common cause principle | 因果马尔可夫条件；忠实性；共同原因原则 |
| Markov equivalence; skeleton; v-structure; CPDAG | 马尔可夫等价；骨架；v结构；CPDAG |
| potential outcomes; ignorability; SUTVA; instrumental variable; difference in differences | 潜在结果；可忽略性；SUTVA；工具变量；双重差分 |
| uplift; persuadables; sleeping dogs; invariant causal prediction | 增益；可被说服者；沉睡的狗；不变因果预测 |
| causal exclusion; supervenience; proportionality; epiphenomenalism | 因果排斥；随附；相称性；副现象论 |

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
| Gettier, Nozick, Sosa, Goldman, Zagzebski | 盖蒂尔，诺齐克，索萨，戈德曼，扎格泽博斯基 |
| Pritchard, DeRose, Dretske, Lehrer, BonJour, Greco, Lackey | 普理查德，德罗斯，德雷斯克，雷勒，邦茹，格雷科，拉基 |
| Dharmottara, Zhuangzi, Sextus Empiricus | 法上，庄子，塞克斯都·恩披里柯 |
| Ann, Bob, Cath (Part 12's card players) | 安，鲍勃，凯丝 |
| Hintikka, Aumann, Halpern, Moses, Rubinstein, Zollman | 欣蒂卡，奥曼，哈尔彭，摩西，鲁宾斯坦，佐尔曼 |
| Ramsey, de Finetti, Joyce, Jeffrey, Jaynes, Bertrand | 拉姆齐，德菲内蒂，乔伊斯，杰弗里，杰恩斯，贝特朗 |
| Kyburg, Makinson, Leitgeb, Elga, Bostrom, Pearl | 凯伯格，梅金森，莱特格布，埃尔加，博斯特罗姆，珀尔 |
| Fisher, Neyman, Pearson, Jeffreys, Lindley, Birnbaum, Mayo, Ioannidis | 费希尔，奈曼，皮尔逊，杰弗里斯，林德利，伯恩鲍姆，梅奥，约阿尼迪斯 |
| Hume, al-Ghazālī, Mill, Mackie, Suppes, Cartwright, Woodward | 休谟，安萨里，密尔，麦基，苏佩斯，卡特赖特，伍德沃德 |
| Spirtes, Glymour, Scheines, Rubin, Halpern, Hall, Kim, Yablo | 斯皮尔特斯，格利穆尔，沙因斯，鲁宾，哈尔彭，霍尔，金在权，亚布罗 |
