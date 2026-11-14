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
| measurement; to measure | 测量 |
| scale (of measurement); rating scale | 量表；评定量表 |
| nominal, ordinal, interval, ratio scale | 称名量表，顺序量表，等距量表，比率量表 |
| permissible transformation; to respace (a rating scale) | 允许的变换；重排间距 |
| sone | 宋 |
| conjoint measurement; double cancellation | 联合测量；双重消去 |
| true score, error, observed score | 真分数，误差，观察分数 |
| reliability; validity | 信度；效度 |
| standard error of measurement | 测量标准误 |
| parallel form (a second form of a test) | 复本 |
| attenuation; correction for attenuation | 衰减；衰减校正 |
| Spearman-Brown formula | 斯皮尔曼–布朗公式 |
| Cronbach's alpha | α系数（克龙巴赫） |
| test-retest; agreement between sessions | 重测；两次之间的一致性 |
| Cohen's kappa | kappa系数（科恩） |
| content, criterion, construct validity | 内容效度，效标效度，构念效度 |
| nomological network | 法则网络 |
| multitrait-multimethod matrix | 多特质–多方法矩阵 |
| convergent validity; method variance | 聚合效度；方法变异 |
| jingle fallacy; jangle fallacy | 同名异实；异名同实 |
| conscientiousness, neuroticism, extraversion | 尽责性，神经质，外向性 |
| grit | 坚毅 |
| construct; latent variable; network (of symptoms) | 构念；潜变量；网络 |
| factor analysis; loading | 因素分析；载荷 |
| self-report; introspection | 自我报告；内省 |
| choice blindness | 选择盲 |
| the reliability paradox | 信度悖论 |
| conflict task; cost (of conflict); flanker; Stroop | 冲突任务；代价；侧翼；斯特鲁普 |
| generalizability theory | 概化理论 |
| questionable measurement practices | 可疑的测量做法 |
| a reading (of one's character); sketch | 解读；速写 |

## Part 4: evidence

| English | 中文 |
|---|---|
| effect size; Cohen's d | 效应量；d |
| overlap (of two distributions) | 重叠 |
| variation explained | 解释的变异 |
| p-value; significant; not significant | p值；显著；不显著 |
| power (of a study) | 统计功效（简称功效） |
| false positive; false alarm | 假阳性；误报 |
| the garden of forking paths | 小径分岔的花园 |
| the plan (the planned analysis) | 原计划（计划中的分析） |
| outcome; outlier; covariate | 结果指标；极端值；协变量 |
| the file drawer; publication bias | 文件抽屉；发表偏倚 |
| funnel plot | 漏斗图 |
| the winner's curse | 赢家的诅咒 |
| p-curve | p曲线 |
| optional stopping (looking and stopping) | 选择性停止 |
| HARKing | 先知道结果再提假设（HARKing） |
| fabrication; flexibility | 捏造；灵活 |
| fraud | 造假 |
| the Reproducibility Project | 可重复性项目 |
| replication; original (study) | 重复研究；原始研究 |
| replication rate | 重复率 |
| preregistration; registered report | 预注册；注册报告 |
| exploratory; confirmatory | 探索性的；验证性的 |
| Many Labs | “多实验室”项目 |
| equivalence test; Bayes factor | 等价检验；贝叶斯因子 |
| margin of error (confidence interval) | 误差范围（置信区间） |
| prediction (betting) market | 博彩市场（预测市场） |
| precognition | 预知 |
| priming; imagined contact | 启动效应；想象接触 |
| dashboard; metric; primary metric | 仪表盘；指标；主要指标 |
| the false-positive lab | 假阳性实验室 |

## Part 5: the neuron

| English | 中文 |
|---|---|
| neuron; the neuron doctrine | 神经元；神经元学说 |
| dendrite; cell body; axon; terminal | 树突；胞体；轴突；末梢 |
| nerve signal; action potential; spike | 神经信号；动作电位；锋电位 |
| impulse (Adrian's word) | 冲动 |
| to fire; firing rate | 发放；发放频率 |
| membrane; membrane potential | 膜（细胞膜）；膜电位 |
| ion; sodium; potassium; calcium | 离子；钠；钾；钙 |
| channel; gate; door (informal) | 通道；门 |
| conductance; capacitance; resistance | 电导；电容；电阻 |
| battery (an ion's equilibrium potential) | 电池 |
| Nernst potential; Goldman equation | 能斯特电位；戈德曼方程 |
| resting potential; at rest | 静息电位；静息时 |
| time constant; length constant | 时间常数；长度常数 |
| voltage clamp; step (of voltage) | 电压钳；阶跃 |
| threshold; all-or-none | 阈值；全或无 |
| refractory period (dead time); absolute, relative | 不应期；绝对，相对 |
| overshoot | 超射 |
| squid giant axon | 乌贼巨轴突 |
| myelin; gap (node) | 髓鞘；缺口 |
| phase plane; recovery variable | 相平面；恢复变量 |
| integrate-and-fire | 积分发放 |
| rate code; spike train | 频率编码；信号串 |
| Fano factor; Poisson train | 法诺因子；泊松信号串 |
| coincidence detection | 重合检测 |
| compartment (of a model neuron) | 房室 |
| glia | 胶质细胞 |
| cochlear implant; local anaesthetic; deep-brain stimulator; neuromorphic chip | 人工耳蜗；局部麻醉药；脑深部电刺激器；神经形态芯片 |
| perceptron | 感知机 |

## Part 6: synapses and circuits

| English | 中文 |
|---|---|
| synapse; chemical, electrical | 突触；化学突触，电突触 |
| the sparks; the soups | 火花派；汤派 |
| cleft; vesicle; release site | （突触）间隙；囊泡；释放位点 |
| transmitter; neuromodulator (modulator) | 递质；神经调质（调质） |
| packet (quantum) | 一包（量子） |
| receptor; agonist; antagonist | 受体；激动剂；拮抗剂 |
| pump (transporter); enzyme | 泵；酶 |
| glutamate; GABA; acetylcholine | 谷氨酸；GABA；乙酰胆碱 |
| dopamine; serotonin; noradrenaline; the opioids | 多巴胺；血清素；去甲肾上腺素；阿片类 |
| curare; naloxone; botulinum toxin; L-DOPA | 箭毒；纳洛酮；肉毒毒素；左旋多巴 |
| caffeine; adenosine; nicotine; morphine; cocaine | 咖啡因；腺苷；尼古丁；吗啡；可卡因 |
| benzodiazepines; SSRIs; stimulants; antipsychotics; nerve agent | 苯二氮卓类；SSRI；兴奋剂；抗精神病药；神经毒剂 |
| excitation; inhibition; EPSP; IPSP | 兴奋；抑制；兴奋性突触后电位（EPSP）；抑制性突触后电位（IPSP） |
| summation in time, in space | 时间上的总和，空间上的总和 |
| shunting inhibition; a shunt | 分流抑制；分流 |
| depolarized | 去极化 |
| Hebb's rule; local (rule); weight; learning rate | 赫布规则；局部的；权重；学习率 |
| Oja's rule; first principal component | 奥亚规则；第一主成分 |
| long-term potentiation (LTP) | 长时程增强（LTP） |
| hippocampus; dentate gyrus; perforant path | 海马；齿状回；穿通通路 |
| AMPA receptor; NMDA receptor; magnesium plug | AMPA受体；NMDA受体；镁塞子 |
| spike timing | 锋电位时序 |
| sliding threshold (BCM); selective | 滑动的阈值；有选择性 |
| lateral inhibition; receptor unit; compound eye; horseshoe crab | 侧抑制；感受单元；复眼；鲎 |
| Mach bands; ramp; foot, top (of a ramp) | 马赫带；斜坡；坡脚，坡顶 |
| Hermann grid; street; crossing; grey spot | 赫尔曼栅格；街道；交叉口；灰点 |
| receptive field; centre-surround; filter | 感受野；中心-周边；滤波器 |
| winner-take-all; self-excitation; rival | 胜者全得；自兴奋；对手 |
| half-centre; central pattern generator; fatigue | 半中枢；中枢模式发生器；疲劳 |
| flexor; extensor; spinal cord | 屈肌；伸肌；脊髓 |
| population; drive; saturation; to oscillate | 群体；驱动；饱和；振荡 |
| EEG (electroencephalogram) | 脑电图（EEG） |
| gain; three-factor rule | 增益；三因子规则 |
| motif (of a circuit) | 基本样式 |
| dissociation constant; occupancy | 解离常数；占据率 |
| tolerance; dependence; placebo; regulator | 耐受；依赖；安慰剂；监管机构 |
| engram; to tag (cells); optical fibre; to freeze | 记忆痕迹；标记；光纤；僵住 |

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
| the British Association for the Advancement of Science | 英国科学促进会 |
| Norman Campbell (the physicist); Donald Campbell | 诺曼·坎贝尔；唐纳德·坎贝尔 |
| Stanley Smith Stevens | 斯坦利·史蒂文斯 |
| Duncan Luce, John Tukey | 卢斯，图基 |
| Bertram Forer | 伯特伦·福勒 |
| Charles Spearman, William Brown | 查尔斯·斯皮尔曼，威廉·布朗 |
| Lee Cronbach, Paul Meehl, Donald Fiske | 李·克龙巴赫，保罗·米尔，唐纳德·菲斯克 |
| Jacob Cohen, Truman Kelley | 科恩，凯利 |
| Richard Nisbett, Timothy Wilson | 理查德·尼斯贝特，蒂莫西·威尔逊 |
| Craig Hedge | 克雷格·赫奇 |
| Joel Michell | 乔尔·米歇尔 |
| Jessica Flake, Eiko Fried | 杰西卡·弗莱克，艾科·弗里德 |
| Daryl Bem | 达里尔·贝姆 |
| Joseph Simmons, Leif Nelson, Uri Simonsohn | 西蒙斯，纳尔逊，西蒙松 |
| Robert Rosenthal (the file drawer) | 罗森塔尔 |
| Andrew Gelman, Eric Loken | 安德鲁·格尔曼，埃里克·洛肯 |
| Diederik Stapel | 迪德里克·斯塔佩尔 |
| Luigi Galvani | 路易吉·伽伐尼 |
| Luigi Galvani, Alessandro Volta | 路易吉·伽伐尼，亚历山德罗·伏打 |
| Camillo Golgi, Santiago Ramón y Cajal | 卡米洛·高尔基，圣地亚哥·拉蒙-卡哈尔 |
| Walther Nernst, David Goldman | 瓦尔特·能斯特，戈德曼 |
| Alan Hodgkin, Andrew Huxley, Bernard Katz | 艾伦·霍奇金，安德鲁·赫胥黎，伯纳德·卡茨 |
| Kenneth Cole, Howard Curtis, George Marmont | 肯尼思·科尔，霍华德·柯蒂斯，乔治·马蒙特 |
| John Zachary Young | 约翰·扎卡里·扬 |
| Richard FitzHugh, Jinichi Nagumo, Louis Lapicque | 理查德·菲茨休，南云仁一，路易·拉皮克 |
| Edgar Adrian, Yngve Zotterman | 埃德加·阿德里安，英韦·佐特曼 |
| Otto Loewi | 奥托·勒维 |
| Henry Dale, John Eccles | 亨利·戴尔，约翰·埃克尔斯 |
| Donald Hebb, Erkki Oja | 唐纳德·赫布，奥亚 |
| Terje Lømo, Tim Bliss | 泰耶·勒莫，蒂姆·布利斯 |
| Guo-qiang Bi, Mu-ming Poo | 毕国强，蒲慕明 |
| Bienenstock, Cooper, Munro | 比嫩施托克，库珀，芒罗 |
| Keffer Hartline, Floyd Ratliff | 凯弗·哈特兰，弗洛伊德·拉特利夫 |
| Ernst Mach, Ludimar Hermann | 恩斯特·马赫，卢迪马尔·赫尔曼 |
| Günter Baumgartner, János Geier | 京特·鲍姆加特纳，亚诺什·盖尔 |
| Charles Sherrington, Thomas Graham Brown | 查尔斯·谢灵顿，托马斯·格雷厄姆·布朗 |
| Hans Berger | 汉斯·贝格尔 |
| Hugh Wilson, Jack Cowan | 休·威尔逊，杰克·考恩 |
| Xu Liu, Steve Ramirez | 刘旭，史蒂夫·拉米雷斯 |
| Erick Turner | 埃里克·特纳 |
| Phineas Gage | 菲尼亚斯·盖奇 |
| Graz, Oslo, Jena, Vermont | 格拉茨，奥斯陆，耶拿，佛蒙特 |
| Bologna, Plymouth | 博洛尼亚，普利茅斯 |
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
| "On the Theory of Scales of Measurement" | 《论测量量表的理论》 |
| "The Proof and Measurement of Association between Two Things" | 《两事物之间关联的证明与测量》 |
| "Telling More Than We Can Know" | 《说出的比能知道的多》 |
| "Feeling the Future" | 《预感未来》 |
| "False-Positive Psychology" | 《假阳性心理学》 |
| *Science*, *Nature* | 《科学》，《自然》 |
| *The Organization of Behavior* | 《行为的组织》 |

## The parts

The Chinese titles of the sixty-two parts and thirteen acts are the entries of `psychology_text_zh.json` (`N.\ Title`
and the `phrases`); `psychN/zh_lines.py` gives each part's film title in the form
`心理学，从零搭建 · 第N部分：标题`.
