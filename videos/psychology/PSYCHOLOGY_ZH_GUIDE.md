# Chinese edition of *Psychology, Built* (心理学，从零搭建)

Narration is translated in `videos/psychology/psychN/zh_lines.py` (literal lines by their English prefix, computed
lines as templates with the source's placeholders spelled exactly, format spec included: `{d['a']:.0f}`);
`python tools/zh_lines.py psychN --todo` lists what is missing, `--verify` checks the latest render line by line.
On-screen text lives in `videos/psychology/psychology_text_zh.json` (exact `strings`, `phrases` inside `\text{}` and
`\textit{}`, regex `patterns`); `python tools/collect_text.py psychN` records a part's strings,
`python tools/collect_text.py --check psychN` lists what is still English, and
`python tools/collect_text.py --lang zh psychN` dry-runs the Chinese build.

- Spoken Mandarin, short sentences; the same content and order as the English.
- Keep every `<bookmark mark='x'/>`, in order, before the words it times.
- Full-width punctuation; quotations in “”; book and paper titles in 《》; numbers as digits (第4部分, 第12章, 1850年),
  spelled out only where the English is a rhetorical count (十行总结).
- Formulas, variables and the letters of a method or task stay as they are (a, b, c, RT, $S$, $I$, $k$, ki).
- People: the Chinese name in narration and on screen (亥姆霍兹, 唐德斯), in full at first mention
  (赫尔曼·亥姆霍兹). Author-year citations on screen keep the Latin spelling so they can be looked up
  (Roelofs（2018）, Woods 等（2015）), and reference cards stay as they are in English.
- A stage, task or faculty has one Chinese name everywhere; the table below is the register, and a new part adds
  its terms here before it is translated.
- Sensitive topics (Acts VIII to X) follow the wording of the current Chinese clinical classification, not a literal
  rendering of the English.
- Language-dependent demonstrations (Parts 18, 21, 23, 33) use Chinese materials and norms, not translated English
  ones; the syllabus marks them.

## Series terms

| English | 中文 |
|---|---|
| Psychology, Built | 心理学，从零搭建 |
| Psyche (the model subject) | 普赛克 |
| the Pool | 样本池 |
| the Battery | 成套测验 |
| the Replication Ledger, the Ledger | 重复账本，账本 |
| the Archive | 档案 |
| the Homunculus (homunculus) | 小人 |
| On you | 在你身上 |
| In practice | 实践 |
| Frontier | 前沿 |
| payoff: where this comes back | 这些会在哪里再出现 |
| act, part, chapter | 幕，部分，章 |
| device | 装置 |
| faculty | 能力 |
| a mechanism that runs | 能运行的机制 |
| simulated, computed, historical data, published, schematic, illustrative | 模拟，计算，历史数据，已发表，示意图，示意 |

## The Ledger's verdicts

| English | 中文 |
|---|---|
| replicated | 已重复 |
| replicated, smaller | 已重复，效应更小 |
| contested | 有争议 |
| failed | 重复失败 |
| not directly tested | 未直接检验 |
| retracted | 已撤稿 |
| story and record | 故事与记录 |
| replication, direct replication | 重复实验，直接重复 |
| preregistered | 预注册 |
| meta-analysis | 元分析 |
| the replication crisis | 可重复性危机 |

## Scales, levels and the map of faculties

| English | 中文 |
|---|---|
| molecule, neuron, circuit, brain, mind, person, group, culture | 分子，神经元，回路，大脑，心灵，个人，群体，文化 |
| what is computed, by what algorithm, in what tissue | 计算什么，用什么算法，在什么组织里 |
| representation, algorithm, hardware | 表示，算法，硬件 |
| reacts, detects, sees, hears, attends | 反应，探测，看，听，注意 |
| learns, predicts, holds in mind, remembers, knows kinds | 学习，预测，暂存，记忆，分类 |
| speaks, reasons, decides, chooses, is aware | 说话，推理，决定，选择，觉知 |
| wants, feels, grows, reads minds, suffers | 想要，感受，成长，读心，受苦 |

## Part 1: measurement and its history

| English | 中文 |
|---|---|
| reaction time | 反应时 |
| simple reaction, choice reaction, go/no-go | 简单反应，选择反应，做/不做（口语：做或不做） |
| stage | 阶段 |
| sense, tell apart, choose, respond (the stages) | 感知，分辨，选择，执行 |
| program (a response) | 编排（反应） |
| subtraction method | 减法 |
| pure insertion | 纯插入 |
| additive factors method | 加因素法 |
| interaction | 交互作用 |
| distribution, mean, variance, spread | 分布，平均值，方差，离散程度 |
| convolution | 卷积 |
| ex-Gaussian | 指数高斯分布 |
| cascade | 级联 |
| accumulation of evidence, threshold (of a decision) | 证据累积，阈值 |
| threshold (of sensation) | 阈限 |
| just-noticeable difference | 最小可觉差 |
| Weber's law, Weber fraction, Fechner's law | 韦伯定律，韦伯分数，费希纳定律 |
| Hick's law, bit | 希克定律，比特 |
| nonsense syllable, saving (in relearning) | 无意义音节，节省 |
| introspection | 内省 |
| imageless thought | 无意象思维 |
| behaviourism, behaviourist | 行为主义，行为主义者 |
| stimulus, response, reward, punishment | 刺激，反应，奖励，惩罚 |
| cognitive map | 认知地图 |
| the cognitive revolution, cognitive psychology | 认知革命，认知心理学 |
| short-term memory | 短时记忆 |
| subject (of an experiment), experimenter, observer | 被试，实验者，观察者 |
| trial | 试验 |
| false start | 抢跑 |
| human factors | 人因 |
| chronoscope | 计时器 |
| tuning fork, drum | 音叉，鼓 |
| questioner (of Hans) | 提问者 |
| blind; single, double, triple blind | 盲法；单盲，双盲，三盲 |
| "procedure without knowledge" (Pfungst) | “不知情的程序” |
| blinders | 眼罩 |
| ideomotor action | 念动动作 |
| control group; treatment | 对照组；处理 |
| independent, dependent variable; operational definition | 自变量，因变量；操作性定义 |
| threats: testing, history, maturation, regression, selection, attrition | 测验效应，历史，成熟，回归，选择，流失 |
| regression to the mean | 向平均数回归 |
| confound | 混淆因素 |
| the shuffle; to shuffle people into groups | 洗牌；洗牌分组 |
| randomization; randomization test | 随机化；随机化检验 |
| spread (of a set of results) | 离散程度 |
| eagerness (the Pool's unmeasured trait) | 积极程度 |
| the game (Part 2's invented treatment) | 游戏 |
| between-person, within-person design | 两组设计，被试内设计（“每个人做自己的对照”） |
| counterbalancing; counterbalanced | 平衡顺序；顺序平衡 |
| Latin square, Williams square | 拉丁方，威廉姆斯方 |
| experimenter expectancy; demand characteristics | 实验者的期望；要求特征 |
| handler; alert (of a detection dog) | 训导员；示警 |
| placebo; active placebo; balanced placebo design | 安慰剂；活性安慰剂；平衡安慰剂设计 |
| factorial design; interaction | 析因设计；交互作用 |
| parallel, fanning, crossing (lines of an interaction plot) | 平行，张开，交叉 |
| statistical conclusion, internal, construct, external validity | 统计结论效度，内部效度，构念效度，外部效度 |
| WEIRD | WEIRD（西方的、受过教育的、工业化的、富裕的、民主的） |
| natural experiment; cutoff | 自然实验；分数线 |
| intention to treat | 意向治疗分析 |
| informed consent; debriefing; deception | 知情同意；事后说明；欺瞒 |
| ethics board | 伦理委员会 |
| respect for persons, beneficence, justice | 尊重个人，有利，公正 |
| arm (of a trial) | 组 |

## Names

| English | 中文 |
|---|---|
| Immanuel Kant | 伊曼努尔·康德 |
| Gustav Fechner, Ernst Weber | 古斯塔夫·费希纳，恩斯特·韦伯 |
| Hermann Helmholtz, Johannes Müller | 赫尔曼·亥姆霍兹，约翰内斯·缪勒 |
| Franciscus Donders | 弗朗西斯库斯·唐德斯 |
| Wilhelm Wundt, Oswald Külpe, Edward Titchener | 威廉·冯特，屈尔佩，铁钦纳 |
| Hermann Ebbinghaus | 赫尔曼·艾宾浩斯 |
| William James | 威廉·詹姆斯 |
| John B. Watson, B. F. Skinner, Edward Thorndike | 约翰·华生，斯金纳，桑代克 |
| Edward Tolman, Karl Lashley | 爱德华·托尔曼，卡尔·拉什利 |
| George Miller, Allen Newell, Herbert Simon, Noam Chomsky | 乔治·米勒，艾伦·纽厄尔，赫伯特·西蒙，诺姆·乔姆斯基 |
| Claude Shannon, William Hick, Ulric Neisser | 克劳德·香农，威廉·希克，乌尔里克·奈瑟 |
| Saul Sternberg, James McClelland | 索尔·斯滕伯格，詹姆斯·麦克莱兰 |
| David Marr, Daniel Dennett | 大卫·马尔，丹尼尔·丹尼特 |
| Francis Galton, David Woods, Ardi Roelofs | 弗朗西斯·高尔顿，大卫·伍兹，阿尔迪·鲁洛夫斯 |
| Clever Hans | 聪明的汉斯 |
| Wilhelm von Osten, Carl Stumpf, Oskar Pfungst | 威廉·冯·奥斯滕，卡尔·施通普夫，奥斯卡·普丰斯特 |
| Michel Chevreul, William Carpenter | 谢弗勒尔，卡彭特 |
| Charles Peirce, Joseph Jastrow | 查尔斯·皮尔士，约瑟夫·贾斯特罗 |
| Ronald Fisher | 费希尔 |
| Donald Campbell, Julian Stanley | 坎贝尔，斯坦利 |
| Robert Rosenthal, Kermit Fode, Lenore Jacobson | 罗森塔尔，福德，雅各布森 |
| Stephen Raudenbush, Martin Orne, Willem Wagenaar | 劳登布什，马丁·奥恩，瓦赫纳尔 |
| Stanley Milgram | 米尔格拉姆 |
| Tuskegee, Alabama | 亚拉巴马州塔斯基吉 |
| Königsberg, Leipzig, Utrecht, Würzburg, Cornell | 柯尼斯堡，莱比锡，乌得勒支，维尔茨堡，康奈尔 |

## Titles

| English | 中文 |
|---|---|
| *Metaphysical Foundations of Natural Science* | 《自然科学的形而上学基础》 |
| *Elemente der Psychophysik* | 《心理物理学纲要》 |
| *On Memory* (*Über das Gedächtnis*) | 《论记忆》 |
| *The Principles of Psychology* | 《心理学原理》 |
| "Psychology as the Behaviorist Views It" | 《行为主义者眼中的心理学》 |
| *The Behavior of Organisms* | 《有机体的行为》 |
| "The Magical Number Seven" | 《神奇的数字7》 |
| *Cognitive Psychology* | 《认知心理学》 |
| *Vision* | 《视觉》 |
| *Brainstorms* | 《头脑风暴》 |
| *Clever Hans* (*Das Pferd des Herrn von Osten*) | 《聪明的汉斯》 |
| "On Small Differences in Sensation" | 《论感觉的微小差别》 |
| *The Design of Experiments* | 《实验设计》 |
| *Pygmalion in the Classroom* | 《课堂里的皮格马利翁》 |
| *The Belmont Report* | 《贝尔蒙报告》 |

## The parts

The Chinese titles of the sixty-two parts and thirteen acts are the entries of `psychology_text_zh.json` (`N.\ Title`
and the `phrases`); `psychN/zh_lines.py` gives each part's film title in the form
`心理学，从零搭建 · 第N部分：标题`.
