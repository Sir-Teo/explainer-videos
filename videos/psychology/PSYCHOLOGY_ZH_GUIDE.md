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

## Part 7: the brain

| English | 中文 |
|---|---|
| the brain (the organ); the mind | 大脑；心灵 |
| lobe; frontal, parietal, temporal, occipital | 叶；额叶，顶叶，颞叶，枕叶 |
| cerebral cortex; hemisphere; cerebellum; brainstem | 大脑皮层；半球；小脑；脑干 |
| corpus callosum; thalamus; basal ganglia | 胼胝体；丘脑；基底神经节 |
| hippocampus; amygdala; hypothalamus | 海马；杏仁核；下丘脑 |
| grey matter; white matter; fibre tract | 灰质；白质；纤维束 |
| lesion; damage; to remove (tissue) | 损伤；损伤；切除 |
| faculty (of the mind) | 能力 |
| phrenology; bump (on the skull) | 颅相学；包 |
| mass action; memory trace | 整体作用；记忆的痕迹 |
| aphasia; conduction aphasia | 失语症；传导性失语 |
| Broca's area; Wernicke's area | 布罗卡区；韦尼克区 |
| to understand, to speak, to repeat | 理解，说话，复述 |
| box-and-arrow diagram; module; pathway | 方框和箭头的图；模块；通路 |
| single dissociation; double dissociation | 单一分离；双重分离 |
| resource; impaired; normal; cutoff | 资源；受损；正常；分界线 |
| necessity (of tissue for a task) | 必要性 |
| a screen (of patients) | 筛查 |
| map (on the cortex); cortical magnification | 地图；皮层放大 |
| eccentricity; centre of gaze; field of view | 离心度；视线中心；视野 |
| blind spot; optic nerve; receptors; filling in | 盲点；视神经；感受器；填补 |
| epilepsy; seizure; stroke | 癫痫；发作；中风 |
| mirror tracing; skill; recollection | 镜画；技能；回忆 |
| split brain; the interpreter | 裂脑；解释器 |
| left-brained, right-brained; a (whole-brain) type | 左脑型，右脑型；（全脑）类型 |
| lateralization; to lean (left, right) | 偏侧化；偏向 |
| neglect; visual agnosia; prosopagnosia; blindsight | 忽视症；视觉失认症；面孔失认症；盲视 |
| plasticity; critical period; to rewire; remapping | 可塑性；关键期；重新接线；重新映射 |
| lazy eye (amblyopia) | 弱视 |
| network; specialized; connected; redundant | 网络；有分工的；相连的；有冗余的 |
| the ten-percent myth | 10%的迷思 |
| clinical neuropsychologist; battery (of tests) | 临床神经心理学家；成套测验 |
| control sample; z-score; single-case t test; degrees of freedom | 对照样本；z分数；单病例t检验；自由度 |
| percentile; base rate | 百分位；基础率 |
| lesion-symptom mapping; voxel; overlap | 损伤—症状映射；体素；重叠 |
| artery; trunk; branch; territory (of an artery) | 动脉；主干；分支；供血区 |
| disconnection | 断连 |
| the tamping iron; stagecoach | 铁棍；驿站马车 |

## Part 8: reading the brain

| English | 中文 |
|---|---|
| to read the brain; brain scan; scanner | 读脑；脑扫描；扫描仪 |
| salmon | 三文鱼 |
| voxel; map (of activity); slice | 体素；图；切片 |
| active, activation; to light up | 激活；亮起来 |
| single cell recording; fine wire (electrode) | 单细胞记录；细金属丝 |
| tuning curve; preferred angle; firing rate | 调谐曲线；最喜欢的角度；发放率 |
| electroencephalogram (EEG); electrode; scalp | 脑电图（EEG）；电极；头皮 |
| brain wave; rhythm | 脑电波；节律 |
| source; aligned, in step | 源；对齐，同步 |
| forward problem; inverse problem | 正问题；逆问题 |
| trial; to average; locked to (the word) | 试次；平均；锁定在……上 |
| event-related potential; N400; P300 | 事件相关电位；N400；P300 |
| microvolt | 微伏 |
| magnetic resonance imaging (MRI); functional MRI | 磁共振成像；功能磁共振成像 |
| proton; magnetic field; tesla; to wobble (precess) | 质子；磁场；特斯拉；摆动 |
| radio pulse; to recover (relax); out of step | 无线电脉冲；摆回原位；错开步调 |
| contrast (of an image) | 对比度 |
| gradient; stripe pattern; Fourier transform | 梯度；条纹图案；傅里叶变换 |
| blood-oxygen-level-dependent signal (BOLD) | 血氧水平依赖信号（BOLD） |
| the echo (haemodynamic response) | 回声 |
| convolution; regressor; weight; t statistic | 卷积；回归量；权重；t统计量 |
| least squares; the linear model | 最小二乘法；线性模型 |
| contrast (task minus control); control task; rest | 差；对照任务；休息 |
| pure insertion; subtraction | 纯插入；减法 |
| threshold; to pass; correction (for the number of tests) | 阈值；通过；校正 |
| false alarm; miss | 误报；漏报 |
| Bonferroni; false discovery rate; cluster | 邦费罗尼；错误发现率；簇 |
| empty (null) brain; smooth noise; long tail | 空的大脑；平滑的噪声；长尾巴 |
| permutation test; to shuffle the labels | 置换检验；打乱标签 |
| circular analysis; "voodoo correlations" | 循环分析；“巫毒相关” |
| reliability; the ceiling (on a correlation) | 信度；上限 |
| reverse inference; forward, backward | 逆向推断；正着走，倒着走 |
| odds; base rate; Bayes' rule | 赔率；基础率；贝叶斯法则 |
| decoding; decoder; the gist | 解码；解码器；大意 |
| to intervene; necessary; sufficient | 干预；必要的；充分的 |
| magnetic pulse (TMS); coil | 磁脉冲；线圈 |
| light-sensitive cells (optogenetics) | 对光敏感的细胞 |
| lie detection; countermeasure | 测谎；小动作（反制手段） |
| brain training; transfer | 大脑训练；迁移 |
| brain-wide association; sample size | 全脑关联；样本量 |
| brain privacy | 大脑隐私 |

## Part 9: genes and evolution

| English | 中文 |
|---|---|
| gene; version (allele); copy; position (variant) | 基因；版本；份（拷贝）；位置（变异） |
| to inherit; heritable; heritability | 遗传；可遗传的；遗传率 |
| nature and nurture | 天性与教养 |
| identical twins; fraternal twins | 同卵双胞胎；异卵双胞胎 |
| twins raised apart; raised together | 分开抚养的双胞胎；一起长大 |
| adoption; adoptive brothers and sisters; birth parents; adoptive parents | 收养；收养家庭里的兄弟姐妹；生父母；养父母 |
| the home a family shares (C); everything else (E) | 共同的家庭；其余的一切 |
| share (of the variance) | 份额 |
| the Pool's twin registry; planted (shares) | 样本池的双胞胎登记册；埋进去的 |
| Falconer's formula; "on a napkin" | 福尔克纳公式；在一张餐巾纸上 |
| path diagram; square, circle, arrow, curved line | 路径图；方框，圆圈，箭头，弯线 |
| maximum likelihood; interval | 最大似然法；区间 |
| equal environments; random mating; like marries like | 环境相等；随机婚配；相似的人结婚 |
| genes that simply add (additive); in combination | 简单相加（加性）；组合起来 |
| regression (to the mean); slope | 回归；斜率 |
| eugenics; forced sterilization | 优生学；强制绝育 |
| seed, field, rich soil, poor soil | 种子，田，肥田，瘦田 |
| phenylketonuria | 苯丙酮尿症 |
| the three laws of behaviour genetics | 行为遗传学的三条定律 |
| candidate gene; serotonin transporter; short and long version | 候选基因；血清素转运体；短版本和长版本 |
| interaction (gene by environment) | 交互作用 |
| genome; genome-wide association; genome-wide significance | 基因组；全基因组关联；全基因组显著 |
| chip; hit | 芯片；命中 |
| polygenic score; discovery study | 多基因分数；用来发现的研究 |
| genetic nurture; transmitted, not transmitted | 遗传养育；传下去的，没有传下去的 |
| missing heritability; rare variants | 缺失的遗传率；罕见变异 |
| epigenetics; chemical tag | 表观遗传学；化学标记 |
| natural selection; adaptive; just-so story | 自然选择；适应性的；“原来如此的故事” |
| mate preferences; financial prospects | 择偶偏好；经济前景 |
| genetic counselling; Huntington's disease, cystic fibrosis, Down syndrome | 遗传咨询；亨廷顿病，囊性纤维化，唐氏综合征 |
| embryo selection; IVF | 胚胎选择；试管婴儿 |
| ancestry; stratification (two strata) | 祖源（血统）；群体分层（两层人群） |
| Mendel's lottery | 孟德尔的彩票 |
| siblings; within families, between families | 兄弟姐妹；家庭内部，家庭之间 |

## Part 10: chemistry and clocks

| English | 中文 |
|---|---|
| the body's clock; daily rhythm; period | 身体里的钟（生物钟）；一天的节律；周期 |
| to set the clock; to lock on (entrain) | 给钟对表；锁上（同步） |
| the low point (of body temperature) | 最低点 |
| suprachiasmatic nucleus; optic nerves; the crossing | 视交叉上核；视神经；交叉 |
| clock genes; pineal gland; melatonin | 钟基因；松果体；褪黑素 |
| rods and cones; light-sensitive cell; pigment | 视杆和视锥；感光细胞；色素 |
| phase response curve; moves later, earlier | 相位响应曲线；往后拨，往前拨 |
| time zone; jet lag; night shift | 时区；时差；夜班 |
| stages of sleep; light sleep; deep (slow-wave) sleep | 睡眠阶段；浅睡眠；深睡眠（慢波睡眠） |
| REM sleep (rapid eye movement); paradoxical sleep | REM睡眠（快速眼动睡眠）；异相睡眠 |
| spindle; slow wave; cycle | 纺锤波；慢波；周期 |
| the two-process model; process S, process C | 双过程模型；过程S，过程C |
| sleep pressure; threshold; the gate | 睡眠压力；阈值；门 |
| recovery sleep; the second wind; alertness | 恢复性睡眠；第二股劲；清醒程度 |
| chronotype; midpoint of sleep; social jetlag | 时型；睡眠中点；社会时差 |
| work days; free days | 工作日；休息日 |
| lapse (of attention); vigilance task | 失误；警觉任务 |
| to consolidate (a memory); to cue; replay | 巩固；提示；重放 |
| activation-synthesis; forebrain; brainstem | 激活—合成假说；前脑；脑干 |
| hormone; cortisol; the stress loop; stressor | 激素；皮质醇；应激回路；应激源 |
| hypothalamus; pituitary; adrenal glands | 下丘脑；垂体；肾上腺 |
| brake (feedback); a worn brake | 刹车；磨损的刹车 |
| to organize; to activate (of hormones) | 组织作用；激活作用 |
| the Yerkes-Dodson law; arousal | 耶基斯—多德森定律；唤醒 |
| to mimic, block, hold, amplify (a transmitter) | 模仿，阻断，留住，放大 |
| pump (reuptake); the gap | 泵；缝隙 |
| nicotine; acetylcholine; morphine; naloxone | 尼古丁；乙酰胆碱；吗啡；纳洛酮 |
| caffeine; adenosine; cocaine; alcohol | 咖啡因；腺苷；可卡因；酒精 |
| antidepressant; benzodiazepines; GABA | 抗抑郁药；苯二氮䓬类；GABA |
| dose; dose and response; occupancy | 剂量；剂量与反应；占有率 |
| blocker (antagonist); antidote; overdose | 阻断剂；解毒剂；过量 |
| half-life; a constant fraction, a constant amount | 半衰期；固定的比例，固定的量 |
| tolerance; withdrawal; the opponent process | 耐受；戒断；对立过程 |
| heroin; the usual room, a new room | 海洛因；平常的房间，新房间 |
| insomnia; behavioural therapy; sleep efficiency | 失眠；行为治疗；睡眠效率 |
| roster; fatigue risk | 排班；疲劳风险 |
| clearance (of waste); anaesthesia | 清除；麻醉 |
| a drawing, not a recording / not the data | 示意图，不是记录／不是数据 |

## Part 11: the threshold

| English | 中文 |
|---|---|
| threshold (of sensation); absolute threshold | 阈限；绝对阈限 |
| just noticeable difference (JND); standard; comparison; increment | 最小可觉差；标准刺激；比较刺激；增量 |
| Weber's fraction; Weber's law; the near miss (to Weber's law) | 韦伯分数；韦伯定律；（韦伯定律的）“近失” |
| Fechner's law; Fechner's step; psychophysics | 费希纳定律；费希纳的一步；心理物理学 |
| method of limits; method of adjustment (of average error); method of constant stimuli (of right and wrong cases) | 极限法；调整法（平均误差法）；恒定刺激法（正误法） |
| ascending, descending series; changeover | 上升序列，下降序列；转折点 |
| point of subjective equality | 主观相等点 |
| two-interval forced choice; yes-no | 二间隔迫选；是否（判断） |
| psychometric function; guess rate; lapse rate; spread; slope | 心理测量函数；猜测率；失误率；离散度；斜率 |
| cumulative Gaussian, logistic, Weibull | 累积高斯，逻辑斯谛，韦布尔 |
| binomial count; likelihood; log-likelihood; deviance | 二项计数；似然；对数似然；偏差 |
| parametric bootstrap; goodness of fit; drift | 参数自助法；拟合优度；漂移 |
| staircase; 2-down 1-up; reversal (turning point); step size | 阶梯法；二下一上；转折点；步长 |
| QUEST; belief (posterior); placement | QUEST；信念（后验）；放置 |
| magnitude estimation; power law; exponent; continuum | 量值估计；幂律；指数；维度 |
| cross-modality matching; range effect | 跨通道匹配；范围效应 |
| bisection; middle grey; lightness; grey card | 二等分；中灰；明度；灰卡 |
| photon noise; dark light; the square-root law (de Vries-Rose) | 光子噪声；暗光；平方根定律（德弗里斯-罗斯定律） |
| compressed code; growing noise | 被压缩的编码；增长的噪声 |
| number sense; scalar timing (the scalar property) | 数感；标量计时（标量性质） |
| utility; the St Petersburg paradox; ducat | 效用；圣彼得堡悖论；金币（达克特） |
| audiometer; decibel; eye chart; codec | 听力计；分贝；视力表；编码器 |
| triangle test; taster; power | 三角检验；品尝者；检验力 |
| paired comparison; law of comparative judgment; Case V | 配对比较；比较判断律；情形V |
| contrast sensitivity function (CSF); the quick CSF | 对比敏感度函数（CSF）；快速CSF |

## Part 12: signal and noise

| English | 中文 |
|---|---|
| signal detection theory; signal; noise | 信号检测论；信号；噪声 |
| hit; miss; false alarm; correct rejection | 击中；漏报；虚报；正确拒斥 |
| hit rate; false-alarm rate | 击中率；虚报率 |
| sensitivity, d′ (read "d prime"); criterion, c; β | 敏感度，d′（读作“d撇”）；判断标准，c值；β |
| the evidence; blank trial; signal trial | 证据；空白试验；信号试验 |
| ROC (receiver operating characteristic); area under the curve (AUC); zROC | ROC（接收者操作特征曲线）；曲线下面积（AUC）；zROC |
| confidence rating; rating scale | 信心评分；评分量表 |
| likelihood ratio; ideal observer; Neyman–Pearson lemma | 似然比；理想观察者；奈曼–皮尔逊引理 |
| payoff; base rate; prevalence | 报酬；基础比率；流行率（出现频率） |
| equal and unequal variance; slope; intercept | 等方差与不等方差；斜率；截距 |
| forced choice; m alternatives | 迫选；m个选项 |
| high-threshold model; correction for guessing | 高阈限模型；猜测校正 |
| recollection; familiarity; dual-process model | 回想；熟悉感；双加工模型 |
| natural frequencies; positive predictive value; odds | 自然频数；阳性预测值；几率 |
| prevalence effect; threat-image projection | 流行率效应；威胁图像投放 |
| vigilance decrement; watch; Clock Test | 警觉衰减；值守；时钟测试 |
| double reading; line-up (simultaneous, sequential); diagnosticity ratio | 双人读片；列队辨认（同时式、顺序式）；诊断性比率 |
| precision; recall | 精确率；召回率 |
| metacognition; type 2 ROC; meta-d′ | 元认知；第二类ROC；元d′ |

## Part 13: the eye and the code

| English | 中文 |
|---|---|
| quantum (of light); photon; frequency of seeing | 光量子；光子；看见频率 |
| rod; cone (L, M, S); photoreceptor; dark adaptation | 视杆细胞；视锥细胞（长波、中波、短波）；光感受器；暗适应 |
| Poisson distribution; quantum efficiency | 泊松分布；量子效率 |
| modulation transfer function (MTF); diffraction; aberration; pupil | 调制传递函数（MTF）；衍射；像差；瞳孔 |
| cone mosaic; Nyquist limit; aliasing; cycles per degree | 视锥镶嵌；奈奎斯特极限；混叠；每度周数 |
| gain control; Naka-Rushton function; log unit | 增益控制；纳卡-拉什顿函数；对数单位 |
| ganglion cell; receptive field; on-centre, off-centre; surround | 神经节细胞；感受野；给光中心、撤光中心；周边 |
| difference of Gaussians (DoG); band-pass filter; Mach bands | 高斯差（DoG）；带通滤波器；马赫带 |
| redundancy; efficient coding | 冗余；高效编码 |
| orientation tuning; simple cell; complex cell; Gabor function; energy model | 朝向调谐；简单细胞；复杂细胞；加博函数；能量模型 |
| contrast sensitivity function (CSF); grating; acuity; Campbell-Robson chart | 对比敏感度函数（CSF）；光栅；视敏度；坎贝尔-罗布森图 |
| channels; adaptation; divisive normalization; cross-orientation masking | 通道；适应；除法归一化；交叉朝向掩蔽 |
| spectrum; cone fundamentals; univariance | 光谱；视锥基本函数；单变量原理 |
| colour matching; primaries; colour-matching functions; standard observer | 颜色匹配；原色；颜色匹配函数；标准观察者 |
| metamer; null space; chromaticity diagram; gamut | 同色异谱；零空间；色度图；色域 |
| opponent colours; unique yellow; hue cancellation | 拮抗色；纯黄（单一黄）；色调抵消 |
| colour vision deficiency; dichromat; tetrachromat | 色觉缺陷（色盲）；二色视者；四色视者 |
| colour constancy; illuminant; von Kries scaling | 颜色恒常性；光源；冯·克里斯缩放 |
| ventral stream (what); dorsal stream (where, how); visual form agnosia | 腹侧通路（是什么）；背侧通路（在哪里、怎么做）；视觉形状失认 |
| chroma subsampling (4:2:0) | 色度二次采样（4:2:0） |

## Part 14: seeing as inference

| English | 中文 |
|---|---|
| seeing as inference; unconscious inference; the inverse problem | 看见即推断；无意识推断；逆问题 |
| prior; likelihood; posterior; precision; shrinkage | 先验；似然；后验；精度；收缩 |
| completing the square; precision-weighted average; bias and variance | 配方；按精度加权的平均；偏差与方差 |
| Gestalt laws: proximity, similarity, good continuation, closure | 格式塔定律：接近性、相似性、良好连续、闭合 |
| illusory contour; figure and ground; border ownership | 错觉轮廓；图形与背景；边界归属 |
| binocular disparity; stereoscope; random-dot stereogram; free fusion | 双眼视差；立体镜；随机点立体图；自由融合 |
| stereoacuity; hyperacuity; motion parallax; texture gradient | 立体视敏度；超视敏；运动视差；纹理梯度 |
| vergence; accommodation; vergence-accommodation conflict | 辐辏；调节；辐辏与调节的冲突 |
| size constancy; lightness; reflectance; illumination; retinex | 大小恒常性；明度；反射率；照度；retinex |
| the Ames room; the Ponzo illusion; the Müller-Lyer illusion; carpentered world | 艾姆斯房间；庞佐错觉；米勒-莱尔错觉；横平竖直的人造环境 |
| cue combination; reliability; cue conflict; point of subjective equality | 线索整合；可靠性；线索冲突；主观相等点 |
| ventriloquist effect | 腹语效应 |
| light-from-above prior; slow-speed prior | 光从上方来的先验；慢速先验 |
| the aperture problem; intersection of constraints; vector average; MAP | 孔径问题；约束交点；向量平均；最大后验 |
| invariance; primal sketch; 2½-D sketch; 3-D model; geons; view-based | 不变性；初始草图；二点五维草图；三维模型；几何离子；基于视角的 |
| face inversion; composite face; the Thatcher illusion | 面孔倒置；合成面孔；撒切尔错觉 |
| fusiform face area; face patches; prosopagnosia; super-recognizer; greebles | 梭状回面孔区；面孔斑块；面孔失认症；超级识别者；格里布尔 |
| convolutional network; texture bias; cue-conflict image; adversarial example | 卷积网络；纹理偏好；线索冲突图像；对抗样本 |
| disruptive colouring; countershading | 破坏性斑纹；反荫蔽 |
| Molyneux's question; affordance; optic array | 莫利纽克斯问题；可供性；光学阵列 |

## Part 15: the other senses

| English | 中文 |
|---|---|
| decibel (dB SPL); sound pressure; threshold in quiet; audiogram | 分贝（声压级）；声压；静息阈；听力图 |
| harmonic; fundamental; missing fundamental; residue pitch | 谐波；基频；缺失基频；残余音高 |
| cochlea; basilar membrane; travelling wave; base, apex | 耳蜗；基底膜；行波；底部、顶部 |
| inner, outer hair cells; cochlear amplifier; otoacoustic emission | 内、外毛细胞；耳蜗放大器；耳声发射 |
| tonotopy; place map (Greenwood) | 音调拓扑；位置图谱（格林伍德） |
| gammatone filter; ERB; critical band; masking; upward spread | 伽马通滤波器；等效矩形带宽（ERB）；临界带；掩蔽；向上扩散 |
| resolved, unresolved harmonics; phase locking; summary autocorrelation | 可分辨、不可分辨的谐波；锁相；汇总自相关 |
| interaural time, level difference (ITD, ILD); duplex theory; coincidence detector | 两耳时间差、强度差（ITD、ILD）；双重理论；重合检测器 |
| auditory scene analysis; streaming; cocktail party problem; harmonicity; common onset | 听觉场景分析；流分离；鸡尾酒会问题；谐和性；共同起始 |
| formant; lack of invariance; categorical perception; ABX; the McGurk effect; causal inference | 共振峰；缺乏不变性；范畴知觉；ABX；麦格克效应；因果推断 |
| roughness; consonance, dissonance; fifth; tritone | 粗糙感；协和、不协和；纯五度；三全音 |
| Meissner, Merkel, Pacinian, Ruffini endings; two-point threshold; proprioception | 迈斯纳小体、默克尔盘、帕西尼小体、鲁菲尼小体；两点阈；本体感觉 |
| the rubber hand illusion; phenomenological control | 橡胶手错觉；现象控制 |
| gate control; large, small fibres; dorsal horn; substantia gelatinosa; TENS | 闸门控制；大、小纤维；背角；胶状质；经皮神经电刺激 |
| phantom limb; mirror box; naloxone; placebo analgesia | 幻肢；镜盒；纳洛酮；安慰剂镇痛 |
| odorant receptor; combinatorial code; flavour; umami; the tongue map | 气味受体；组合编码；风味；鲜味；舌头地图 |
| semicircular canals; otolith organs; vestibulo-ocular reflex; sensory conflict | 半规管；耳石器官；前庭眼反射；感觉冲突 |
| hearing aid; compression; cochlear implant; perceptual coding; codec | 助听器；压缩；人工耳蜗；感知编码；编解码器 |
| hidden hearing loss; synaptopathy; sensitization; mismatch negativity | 隐性听力损失；突触病变；敏化；失匹配负波 |


## Part 16: conditioning

| English | 中文 |
|---|---|
| conditioning (classical, Pavlovian; operant, instrumental) | 条件作用（经典、巴甫洛夫式；操作性、工具性） |
| unconditioned stimulus, response (US, UR); conditioned stimulus, response (CS, CR) | 无条件刺激、反应；条件刺激、反应 |
| acquisition; extinction; spontaneous recovery; generalization; discrimination | 习得；消退；自发恢复；泛化；分化 |
| law of effect; reinforcement; shaping by successive approximation; cumulative record | 效果律；强化；逐步逼近的塑造；累积记录 |
| fixed ratio, variable ratio, fixed interval, variable interval (schedules) | 固定比率、可变比率、固定间隔、可变间隔（强化程序） |
| partial reinforcement extinction effect | 部分强化消退效应 |
| contingency (ΔP); outcome-density effect; truly random control | 关联性（德尔塔P）；结果密度效应；真随机对照 |
| blocking, unblocking; overshadowing; conditioned inhibition; overexpectation | 阻断、解除阻断；遮蔽；条件抑制；过度预期 |
| prediction error; associative strength; associability; the Rescorla–Wagner rule; delta rule | 预测误差；联结强度；可联结性；雷斯科拉-瓦格纳规则；德尔塔规则 |
| latent inhibition; renewal (ABA, ABC, AAB); reinstatement | 潜伏抑制；复燃（ABA、ABC、AAB）；重建 |
| peak procedure; scalar property; rate estimation; autoshaping | 峰值程序；标量性质；速率估计；自动塑造 |
| matching law; undermatching; melioration; concurrent schedules | 匹配律；匹配不足；改善；并发程序 |
| taste aversion; preparedness; instinctive drift; observational learning | 味觉厌恶；准备性；本能漂移；观察学习 |
| exposure therapy; contingency management; token economy; clicker; loot box | 暴露疗法；权变管理；代币制；响片；战利品箱 |
| conditioned tolerance; reconsolidation; latent cause; propositional learning | 条件性耐受；再巩固；潜在原因；命题学习 |

## Part 17: reward and prediction

| English | 中文 |
|---|---|
| reward (the part's title: reward and prediction) | 奖励（本部分标题：奖赏与预测） |
| reinforcement learning; credit assignment; value; discount (γ) | 强化学习；功劳分配；价值；折扣（γ） |
| temporal-difference (TD) learning; TD error; the Bellman equation | 时间差分学习；时间差分误差；贝尔曼方程 |
| reward prediction error; burst; dip; ramp | 奖励预测误差；爆发；下陷；斜坡 |
| tapped delay line; complete serial compound; second-order conditioning | 抽头延迟线；完全序列复合刺激；二级条件作用 |
| optogenetics; unblocking | 光遗传学；解除阻断 |
| actor-critic; Q-learning; softmax; inverse temperature (β); learning rate (α) | 演员-评论家；Q学习；软最大化；逆温度（β）；学习率（α） |
| basal ganglia; striatum (ventral, dorsal); direct and indirect pathways; Go, NoGo | 基底神经节；纹状体（腹侧、背侧）；直接与间接通路；“去”，“不去” |
| levodopa; dopamine agonist; impulse-control disorder | 左旋多巴；多巴胺激动剂；冲动控制障碍 |
| bandit (multi-armed, contextual); win-stay, lose-shift; parameter recovery | 老虎机（多臂、情境）；赢则留，输则换；参数恢复 |
| explore, exploit; regret; ε-greedy; UCB; Thompson sampling; directed and random exploration | 探索，利用；遗憾值；ε贪心；置信上界；汤普森抽样；定向探索与随机探索 |
| latent learning; cognitive map; place cell; grid cell; entorhinal cortex | 潜伏学习；认知地图；位置细胞；网格细胞；内嗅皮层 |
| model-free, model-based; habit, goal-directed action; devaluation; the two-step task | 无模型，基于模型；习惯，目标导向行动；贬值；两步任务 |
| successor representation; reward and transition revaluation; replay (forward, backward) | 后继表征；奖励与转移再评估；重放（正向、反向） |
| distributional reinforcement learning; expectile; salience | 分布式强化学习；期望分位数；显著性 |
| learning sets; meta-learning; recommender system; A/B test | 学习定势；元学习；推荐系统；A/B测试 |

## Part 18: attention

| English | 中文 |
|---|---|
| selective attention; dichotic listening; shadowing; the cocktail party effect | 选择性注意；双耳分听；追随；鸡尾酒会效应 |
| filter; attenuation; early and late selection; perceptual load; flanker | 过滤器；衰减；早期与晚期选择；知觉负荷；侧翼刺激 |
| spatial cueing; valid, invalid, neutral; benefit, cost; endogenous, exogenous; inhibition of return | 空间提示；有效、无效、中性；收益、代价；内源性、外源性；返回抑制 |
| visual search; feature search, conjunction search; set-size function; pop-out | 视觉搜索；特征搜索、联合搜索；集合大小函数；跳出 |
| feature integration theory; binding; illusory conjunction; guided search; priority map; quitting threshold | 特征整合理论；捆绑；错觉性结合；引导搜索；优先级图；退出阈限 |
| saliency map; centre-surround; winner-take-all; scan path; selection history; value-driven capture | 显著性图；中心-周边；赢者通吃；扫视路径；选择历史；价值驱动的捕获 |
| change blindness; the flicker paradigm; inattentional blindness; attentional set | 变化盲视；闪烁范式；非注意盲视；注意定势 |
| attentional blink; lag-1 sparing; RSVP; psychological refractory period; central bottleneck; SOA | 注意瞬脱；滞后一豁免；快速序列视觉呈现；心理不应期；中央瓶颈；刺激起始间隔 |
| Stroop effect; interference, facilitation; delta plot; conflict monitoring; congruency sequence effect; task switching; switch cost | 斯特鲁普效应；干扰、促进；差值图；冲突监测；一致性序列效应；任务切换；切换代价 |
| biased competition; normalization; attention field; contrast gain; response gain | 偏向竞争；归一化；注意场；对比度增益；反应增益 |
| theory of visual attention (TVA); whole report; capacity; vigilance decrement; prevalence effect; satisfaction of search | 视觉注意理论；全部报告；容量；警觉衰减；流行率效应；搜索满足 |
| alarm fatigue; viewability; media multitasking; rhythmic sampling | 警报疲劳；可见度；媒体多任务；节律采样 |

## Part 19: working memory

| English | 中文 |
|---|---|
| working memory; short-term memory; memory span; digit span; chunk; recoding | 工作记忆；短时记忆；记忆广度；数字广度；组块；重新编码 |
| absolute judgment; channel capacity; bits; mutual information | 绝对判断；通道容量；比特；互信息 |
| iconic memory; whole report; partial report; masking | 图像记忆；全部报告；部分报告；掩蔽 |
| the Brown-Peterson task; decay; interference; proactive interference; release from proactive interference | 布朗-彼得森任务；衰退；干扰；前摄干扰；前摄干扰的释放 |
| temporal distinctiveness; SIMPLE; Luce's choice rule | 时间独特性；SIMPLE 模型；卢斯选择规则 |
| the modal model; rehearsal; double dissociation | 多重存储模型；复述；双重分离 |
| the multicomponent model; central executive; phonological loop; visuospatial sketchpad; episodic buffer | 多成分模型；中央执行系统；语音环路；视觉空间画板；情景缓冲器 |
| word-length effect; phonological similarity effect; articulatory suppression; dual-task | 词长效应；语音相似性效应；发音抑制；双任务 |
| memory scanning; serial exhaustive search; self-terminating search; limited-capacity parallel model; mimicry | 记忆扫描；系列穷尽搜索；自我终止搜索；有限容量平行模型；模仿 |
| change detection; capacity K; hits, false alarms; Cowan's K; Pashler's K; subitizing | 变化检测；容量 K；击中、虚报；考恩 K；帕什勒 K；感数 |
| continuous report; delayed estimation; colour wheel; von Mises distribution; concentration; precision; Fisher information | 连续报告；延迟估计；色轮；冯·米塞斯分布；集中度；精度；费希尔信息 |
| mixture model; guess rate; swap errors; misbinding | 混合模型；猜测率；交换错误；错误捆绑 |
| slots; slots plus averaging; resources; equal precision; variable precision; AIC | 槽位；槽位加平均；资源；等精度；变精度；赤池信息准则 |
| delay activity; memory field; ring attractor; bump; diffusion; activity-silent; short-term facilitation | 延迟期活动；记忆野；环形吸引子；活动峰；扩散；静默活动；短时易化 |
| complex span; reading span; operation span; fluid intelligence; latent correlation | 复杂广度；阅读广度；运算广度；流体智力；潜变量相关 |
| dual n-back; near transfer; far transfer; active control; no-contact control | 双重 n-back；近迁移；远迁移；主动控制组；无接触控制组 |
| read-back; hear-back; cognitive load; rate-distortion; resource-rational | 复诵；听复核；认知负荷；率失真；资源理性 |

## Part 20: memory, storing and finding

| English | 中文 |
|---|---|
| savings; relearning; nonsense syllable; forgetting curve; power law; exponential | 节省量；重学；无意义音节；遗忘曲线；幂律；指数函数 |
| base-level activation (ACT-R); rational analysis; need probability | 基础激活（ACT-R）；理性分析；需要概率 |
| free recall; serial-position curve; primacy; recency; probability of first recall | 自由回忆；系列位置曲线；首因；近因；首次回忆概率 |
| lag; lag-conditional response probability (lag-CRP); temporal contiguity; forward asymmetry | 滞后；滞后条件反应概率（滞后CRP）；时间邻近效应；向前不对称 |
| continual-distractor free recall; long-term recency; the ratio rule | 持续干扰自由回忆；长时近因；比例规则 |
| levels of processing; transfer-appropriate processing; generation effect; method of loci | 加工水平；迁移适当加工；生成效应；位置记忆法 |
| encoding specificity; recognition failure; context-dependent memory; state-dependent memory | 编码特异性；再认失败；情境依存记忆；状态依存记忆 |
| search of associative memory (SAM); rehearsal buffer; sampling; recovery | 联想记忆搜索（SAM）；复述缓冲区；抽取；恢复 |
| temporal context model (TCM); context maintenance and retrieval (CMR); drift; context reinstatement | 时间情境模型（TCM）；情境维持与提取模型（CMR）；漂移；情境恢复 |
| likelihood; held out; bits per recall; serial-position baseline | 似然；留出；每次回忆的比特数；系列位置基线 |
| Hopfield network; energy; attractor; content-addressable memory; crosstalk; capacity | 霍普菲尔德网络；能量；吸引子；按内容寻址的记忆；串扰；容量 |
| declarative; non-declarative; episodic; semantic; priming; stem completion | 陈述性；非陈述性；情景；语义；启动；词干补全 |
| familiarity; recollection; remember/know; dual-process model; unequal-variance model | 熟悉感；回想；记得/知道；双加工模型；不等方差模型 |
| hippocampal indexing theory; pattern separation; pattern completion; dentate gyrus; CA3; time cells | 海马索引理论；模式分离；模式补全；齿状回；CA3；时间细胞 |
| cognitive interview; telescoping; landmark; word-list learning test | 认知访谈；伸缩效应；地标；词表学习测验 |
| induction head | 归纳头 |

## Part 21: memory, forgetting and inventing

| English | 中文 |
|---|---|
| decay; interference; proactive interference; retroactive interference; retrieval-induced forgetting | 衰退；干扰；前摄干扰；倒摄干扰；提取诱发遗忘 |
| Jost's law; hazard; averaging artefact; Wickelgren's law; AIC | 约斯特定律；风险率；平均伪影；威克尔格伦定律；赤池信息准则 |
| linear associator; A-B, A-C design | 线性联想器；A-B、A-C设计 |
| consolidation; systems consolidation; Ribot's gradient; retrograde amnesia; multiple trace theory | 巩固；系统巩固；里博梯度；逆行性遗忘；多重痕迹理论 |
| replay; slow-wave sleep; targeted memory reactivation; reconsolidation | 重放；慢波睡眠；目标记忆再激活；再巩固 |
| catastrophic interference (forgetting); complementary learning systems; interleaved learning | 灾难性干扰（遗忘）；互补学习系统；交错学习 |
| spacing effect; massed and distributed practice; retention interval; temporal ridgeline | 间隔效应；集中与分散练习；保持间隔；时间脊线 |
| testing effect; retrieval practice; bifurcation model; metacognitive illusion; fluency | 测验效应；提取练习；分岔模型；元认知错觉；流畅性 |
| schema; reconstruction; category adjustment model; prototype | 图式；重建；类别调整模型；原型 |
| DRM paradigm; critical lure; global matching; activation-monitoring; fuzzy-trace theory; gist; verbatim | DRM范式；关键诱饵词；整体匹配；激活-监控；模糊痕迹理论；要义；逐字 |
| misinformation effect; source monitoring; implanted memory; imagination inflation | 误导信息效应；来源监控；植入记忆；想象膨胀 |
| verbal overshadowing; Registered Replication Report | 言语遮蔽；注册重复报告 |
| flashbulb memory; line-up; confidence-accuracy characteristic (CAC); double-blind administration | 闪光灯记忆；列队辨认；信心-准确性特征（CAC）；双盲施测 |
| highly superior autobiographical memory (HSAM); mnemonist | 高度超常自传记忆（HSAM）；记忆术家 |
| Leitner boxes; spaced repetition; half-life regression | 莱特纳盒子；间隔重复；半衰期回归 |
| elastic weight consolidation; Fisher information; machine unlearning; silent engram | 弹性权重巩固；费希尔信息；机器遗忘学习；沉默记忆痕迹 |

## Part 22: concepts and categories

| English | 中文 |
|---|---|
| concept; category; classical view; necessary and sufficient features | 概念；类别；经典观点；必要且充分的特征 |
| typicality; family resemblance; graded membership; fuzzy boundary | 典型性；家族相似性；有程度的成员资格；模糊边界 |
| prototype; exemplar; context model; generalized context model (GCM) | 原型；范例；情境模型；广义情境模型（GCM） |
| attention weight; Luce's choice rule; the 5-4 structure; linear separability | 注意权重；卢斯选择法则；五四结构；线性可分 |
| the six problems (Types I to VI); ALCOVE; delta rule | 六个问题（第一型至第六型）；ALCOVE；德尔塔法则 |
| multidimensional scaling (classical, non-metric); double centring; stress | 多维尺度法（经典、非度量）；双重中心化；应力 |
| psychological space; generalization gradient; universal law of generalization; consequential region | 心理空间；泛化梯度；泛化的普遍定律；后果区域 |
| metric axioms: minimality, symmetry, triangle inequality | 度量公理：极小性、对称性、三角不等式 |
| contrast model; prominence; focusing; subject and referent | 对比模型；突出性；聚焦；主语与参照 |
| semantic network; cognitive economy; spreading activation; fan effect | 语义网络；认知经济性；扩散激活；扇效应 |
| semantic priming; lexical decision; naming; associate | 语义启动；词汇判断；命名；联想词 |
| basic level; superordinate; subordinate; category utility | 基本水平；上位水平；下位水平；类别效用 |
| theory theory; ad hoc category; psychological essentialism; natural kind; artefact | 理论观；临时类别；心理本质主义；自然种类；人造物 |
| number game; hypothesis space; size principle; suspicious coincidence | 数字游戏；假设空间；规模原则；可疑的巧合 |
| distributional hypothesis; co-occurrence; PPMI; singular value decomposition; word vector; cosine | 分布假说；共现；正点互信息；奇异值分解；词向量；余弦 |
| latent semantic analysis (LSA); analogy; symbol grounding | 潜在语义分析（LSA）；类比；符号接地 |
| polythetic category; HiTOP; card sorting; taxonomy | 多元类别；HiTOP；卡片分类；分类体系 |
| representational similarity analysis (RSA); hue angle | 表征相似性分析（RSA）；色调角 |
| Rosch, Mervis; McCloskey, Glucksberg; Wittgenstein | 罗施，默维斯；麦克洛斯基，格吕克斯伯格；维特根斯坦 |
| Posner, Keele; Homa, Vosburgh; Medin, Schaffer; Nosofsky; Kruschke | 波斯纳，基尔；霍马，沃斯堡；梅丁，谢弗；诺索夫斯基；克鲁施克 |
| Shepard, Hovland, Jenkins; Torgerson; Kruskal; Ekman (Gösta); Rothkopf | 谢泼德，霍夫兰，詹金斯；托格森；克鲁斯卡尔；埃克曼（约斯塔）；罗特科普夫 |
| Tversky, Gati; Collins, Quillian, Loftus; Meyer, Schvaneveldt; Hutchison | 特沃斯基，加蒂；柯林斯，奎利恩，洛夫特斯；迈耶，施瓦内维尔特；哈奇森 |
| Corter, Gluck; Tanaka, Taylor; Rips; Barsalou; Murphy; Keil; Gelman, Markman | 科特，格鲁克；田中，泰勒；里普斯；巴萨卢；墨菲；凯尔；格尔曼，马克曼 |
| Tenenbaum, Griffiths; Fei Xu; Harris; Firth; Landauer, Dumais; Harnad | 特南鲍姆，格里菲斯；Fei Xu（保留原名）；哈里斯；弗斯；兰道尔，杜迈斯；哈纳德 |

## Part 23: language

| English | 中文 |
|---|---|
| productivity; phoneme; morpheme; syntax; semantics; pragmatics | 能产性；音位；语素；句法；语义；语用 |
| the wug test; over-regularization; the U-shaped curve; words and rules | wug 测验；过度规则化；U 形曲线；词与规则 |
| Zipf's law; rank; power law; the typing monkey | 齐普夫定律；名次；幂律；敲打字机的猴子 |
| mental lexicon; lexical decision; word frequency; cohort; uniqueness point; TRACE | 心理词典；词汇判断；词频；同类群；唯一性点；TRACE |
| word superiority effect; interactive activation model; feature, letter and word levels; mask | 词优效应；交互激活模型；特征层、字母层与词层；掩蔽 |
| garden-path sentence; reanalysis; fixation; regression (of the eyes); eye tracker | 花园路径句；重新分析；注视；（眼动的）回视；眼动仪 |
| surprisal; bits; trigram model; Kneser-Ney smoothing; perplexity; spillover | 意外度；比特；三元语法模型；Kneser-Ney 平滑；困惑度；溢出效应 |
| self-paced reading; the Natural Stories corpus | 自定步速阅读；自然故事语料库 |
| statistical learning; transitional probability; word segmentation; part-word | 统计学习；转移概率；词切分；部分词 |
| poverty of the stimulus; identification in the limit; negative evidence; universal grammar; fast mapping | 刺激贫乏；极限识别；负面证据；普遍语法；快速映射 |
| critical period; age of arrival; age of starting; late first-language learners | 关键期；到达年龄；开始年龄；晚学第一语言者 |
| Broca's area; Wernicke's area; aphasia; the language network; N400; P600 | 布洛卡区；韦尼克区；失语症；语言网络；N400；P600 |
| linguistic relativity; basic colour terms; cognitive technology; executive control; bilingual advantage | 语言相对论；基本颜色词；认知技术；执行控制；双语优势 |
| readability; Flesch reading ease; phonics; minimal pairs; BabyLM | 可读性；弗莱施易读度；自然拼读法；最小对立句对；BabyLM |
| Skinner; Chomsky; Berko; Zipf; Miller (George A.) | 斯金纳；乔姆斯基；让·伯科；齐普夫；乔治·米勒 |
| Marslen-Wilson; Reicher; Wheeler; McClelland; Rumelhart | 马斯伦-威尔逊；赖歇尔；惠勒；麦克莱兰；鲁梅尔哈特 |
| Bever; Frazier; Rayner; Hale; Levy; Smith (Nathaniel) | 贝弗；弗雷泽；雷纳；黑尔；利维；纳撒尼尔·史密斯 |
| Saffran, Aslin, Newport; Black, Bergmann; Gold; Carey, Bartlett; Hart, Risley | 萨弗兰，阿斯林，纽波特；布莱克，伯格曼；戈尔德；凯里，巴特利特；哈特，里斯利 |
| Marcus; Pinker, Prince; Genie; Mayberry; Johnson; Hartshorne | 马库斯；平克，普林斯；吉妮；梅伯里；约翰逊；哈茨霍恩 |
| Broca; Wernicke; Fedorenko; Kutas, Hillyard; Osterhout, Holcomb | 布洛卡；韦尼克；费多连科；库塔斯，希利亚德；奥斯特豪特，霍尔科姆 |
| Whorf; Berlin, Kay; Winawer; Frank (Michael); the Pirahã | 沃尔夫；柏林，凯；威纳沃；迈克尔·弗兰克；皮拉罕人 |
| Bialystok; Paap, Greenberg; Lehtonen; Flesch; Breitenstein | 比亚韦斯托克；帕普，格林伯格；莱赫托宁；弗莱施；布赖滕施泰因 |
| Wai Keen Vong; Byung-Doh Oh; Schuler; Christiansen; Chater | Wai Keen Vong（保留原名）；Byung-Doh Oh（保留原名）；舒勒；克里斯蒂安森；查特 |

## Part 24: reasoning and problem solving

| English | 中文 |
|---|---|
| selection task; permission; social contract; cheater detection; pragmatic reasoning schema | 选择任务；许可；社会契约；骗子识别；实用推理图式 |
| syllogism; premise; mood; figure; valid; no valid conclusion; existential import | 三段论；前提；语气；格；有效；没有有效结论；存在含义 |
| mental model; counterexample; atmosphere effect; matching; probability heuristics | 心理模型；反例；气氛效应；匹配说；概率启发式 |
| belief bias; optimal data selection; rarity; expected information gain | 信念偏差；最优数据选择；稀有性；期望信息增益 |
| problem space; state; operator; means-ends analysis; hill climbing; subgoal; goal stack | 问题空间；状态；算子；手段-目的分析；爬山法；子目标；目标栈 |
| production system; working memory; ACT-R; think-aloud protocol | 产生式系统；工作记忆；ACT-R；口语报告 |
| insight; functional fixedness; the nine-dot problem; feeling of warmth | 顿悟；功能固着；九点问题；温暖感 |
| expertise; chunk; deliberate practice; the 10,000-hour rule | 专长；组块；刻意练习；一万小时定律 |
| analogy; structure mapping; systematicity; the radiation problem | 类比；结构映射；系统性；射线问题 |
| mental imagery; mental rotation; depictive; descriptive; tacit knowledge; aphantasia | 心理表象；心理旋转；图画式；描述式；默会知识；心盲症 |
| contingency; delta P; causal power; noisy-OR; intervention | 相倚性；delta P；因果力；噪声或模型；干预 |
| bounded rationality; satisficing; posterior median; power law; Erlang prior | 有限理性；满意即止；后验中位数；幂律；埃尔朗先验 |
| Wason; Griggs, Cox; Cheng, Holyoak; Cosmides; Johnson-Laird; Khemlani; Ragni | 沃森；格里格斯，考克斯；程，霍利约克；科斯米德斯；约翰逊-莱尔德；赫姆拉尼；拉格尼 |
| Evans, Barston, Pollard; Oaksford, Chater; Woodworth, Sells; Wetherick, Gilhooly | 埃文斯，巴斯顿，波拉德；奥克斯福德，查特；伍德沃思，塞尔斯；韦瑟里克，吉尔胡利 |
| Newell, Shaw, Simon; Anderson, Douglass; Ericsson; Duncker; Adamson; Metcalfe, Wiebe | 纽厄尔，肖，西蒙；安德森，道格拉斯；埃里克森；东克尔；亚当森；梅特卡夫，维布 |
| de Groot; Chase; Gobet; Macnamara; Gick; Gentner; Shepard, Metzler; Ganis, Kievit | 德格罗特；蔡斯；戈贝；麦克纳马拉；吉克；根特纳；谢泼德，梅茨勒；加尼斯，基维特 |
| Kosslyn; Pylyshyn; Zeman; Waldmann, Hagmayer; Griffiths, Tenenbaum; Mozer; Chollet; Webb | 科斯林；派利夏恩；泽曼；瓦尔德曼，哈格迈尔；格里菲斯，特南鲍姆；莫泽；肖莱；韦布 |
## Part 25: deciding in time

| English | 中文 |
|---|---|
| random-dot motion; coherence; speed-accuracy trade-off; speed and accuracy instructions | 随机点运动；一致性；速度–准确性权衡；速度指令与准确指令 |
| Hick's law; Fitts's law; index of difficulty; submovement; bits | 希克定律；菲茨定律；难度指数；子动作；比特 |
| response-time distribution; quantile; ex-Gaussian; skew; tail | 反应时间分布；分位数；离散高斯；偏度；尾巴 |
| sequential probability ratio test; log-likelihood ratio; operating characteristic; average sample number; overshoot | 序贯概率比检验；对数似然比；操作特征；平均样本数；冲过界线 |
| diffusion model; drift rate; bound; starting point; non-decision time; first-passage time | 扩散模型；漂移率；界线；起点；非决策时间；首次通过时间 |
| selective influence; EZ diffusion; across-trial variability; fast errors; slow errors | 选择性影响；EZ 扩散；试验间变异；快的错误；慢的错误 |
| accumulator; ramp; step; lateral intraparietal area (LIP) | 累积器；渐升；跳变；外侧顶内区（LIP） |
| linear ballistic accumulator; leaky competing accumulator; inhibition; leak; urgency; collapsing bound | 线性弹道累积器；泄漏竞争累积器；抑制；泄漏；紧迫；塌缩的界线 |
| stop-signal task; stop-signal delay; stop-signal reaction time (SSRT); inhibition function; integration method | 停止信号任务；停止信号延迟；停止信号反应时（SSRT）；抑制函数；积分法 |
| confidence; balance of evidence; folded X; attentional drift diffusion model | 信心；证据之差；折叠的 X；注意漂移扩散模型 |
| Wald, Wolfowitz; Stone; Laming; Ratcliff; McKoon; Rouder; Tuerlinckx; Navarro, Fuss | 瓦尔德，沃尔福威茨；斯通；拉明；拉特克利夫；麦昆；劳德；图尔林克斯；纳瓦罗，富斯 |
| Wagenmakers; Gomez; Voss; Rae; Heathcote; Brown; Dutilh; Usher; McClelland; Bogacz | 瓦根马克斯；戈麦斯；福斯；雷伊；希思科特；布朗；迪蒂伊；乌舍尔；麦克莱兰；博加奇 |
| Shadlen; Newsome; Roitman; Latimer; Pillow; Steinemann; Logan, Cowan; Verbruggen; Bissett | 沙德伦；纽瑟姆；罗伊特曼；拉蒂默；皮洛；施泰内曼；洛根，考恩；弗吕格根；比塞特 |
| Vickers; Kiani; Pleskac, Busemeyer; Sanders; Cisek; Drugowitsch; Hawkins; Krajbich, Armel, Rangel | 维克斯；基亚尼；普莱斯卡克，布斯迈耶；桑德斯；西塞克；德鲁戈维奇；霍金斯；克拉伊比赫，阿梅尔，兰热尔 |
| Hyman; Fitts; Crossman, Goodeve; Pachella; Wickelgren; Hedge; Lerche; Green; Thapar | 海曼；菲茨；克罗斯曼，古德伊夫；帕切拉；维克尔格伦；赫奇；勒尔歇；格林；塔帕尔 |

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
| John Harlow, Malcolm Macmillan | 约翰·哈洛，马尔科姆·麦克米伦 |
| Franz Joseph Gall, Pierre Flourens | 弗朗茨·约瑟夫·加尔，皮埃尔·弗卢朗 |
| Paul Broca, Leborgne ("Tan") | 保罗·布罗卡，勒博涅（“Tan”，保留原文） |
| Carl Wernicke, Ludwig Lichtheim, Nina Dronkers | 卡尔·韦尼克，路德维希·利希特海姆，尼娜·德隆克斯 |
| Wilder Penfield, Edwin Boldrey | 怀尔德·彭菲尔德，埃德温·博尔德里 |
| Henry Molaison (H.M.), William Scoville, Brenda Milner | 亨利·莫莱森（H.M.），威廉·斯科维尔，布伦达·米尔纳 |
| Roger Sperry, Michael Gazzaniga | 罗杰·斯佩里，迈克尔·加扎尼加 |
| Torsten Wiesel, David Hubel, Michael Merzenich | 托斯坦·维泽尔，大卫·休伯尔，迈克尔·梅策尼希 |
| Eleanor Maguire, Katherine Woollett, Jared Nielsen | 埃莉诺·马奎尔，凯瑟琳·伍利特，贾里德·尼尔森 |
| Cavendish, Bicêtre, Montreal, Hartford, Caltech, Utah | 卡文迪什，比塞特，蒙特利尔，哈特福德，加州理工学院，犹他 |
| Graz, Oslo, Jena, Vermont | 格拉茨，奥斯陆，耶拿，佛蒙特 |
| Bologna, Plymouth | 博洛尼亚，普利茅斯 |
| Königsberg, Leipzig, Utrecht, Würzburg, Cornell | 柯尼斯堡，莱比锡，乌得勒支，维尔茨堡，康奈尔 |
| Marta Kutas, Steven Hillyard, Kara Federmeier | 玛尔塔·库塔斯，史蒂文·希利亚德，费德迈尔 |
| Seiji Ogawa, Nikos Logothetis | 小川诚二，尼科斯·洛戈塞蒂斯 |
| Anders Eklund, Edward Vul, Russell Poldrack | 安德斯·埃克伦德，爱德华·武尔，拉塞尔·波尔德拉克 |
| Anthony Barker, Adrian Owen | 安东尼·巴克，阿德里安·欧文 |
| Jaeggi, Kozel, Ganis (in the Ledger) | 耶吉，科泽尔，加尼斯 |
| Charles Darwin, Gregor Mendel | 查尔斯·达尔文，格雷戈尔·孟德尔 |
| Thomas Bouchard, Matt McGue | 托马斯·布沙尔，麦格 |
| Eric Turkheimer, Richard Lewontin, Stephen Jay Gould | 埃里克·特克海默，理查德·列万廷，斯蒂芬·杰伊·古尔德 |
| Falconer; David Buss | 福尔克纳；戴维·巴斯 |
| Caspi, Risch, Chabris, Border, Rietveld, Lee, Okbay, Polderman (in the Ledger) | 卡斯皮，里施，查布里斯，博德，里特费尔德，李，奥克贝，波尔德曼 |
| Jim, Linda, Betty, James Alan, Toy (the dog) | 吉姆，琳达，贝蒂，詹姆斯·艾伦，托伊 |
| Ohio, Minnesota, Dunedin, Iceland, Kentucky | 俄亥俄，明尼苏达，达尼丁，冰岛，肯塔基 |
| *Hereditary Genius* | 《遗传的天才》 |
| Nathaniel Kleitman, Bruce Richardson | 纳撒尼尔·克莱特曼，布鲁斯·理查森 |
| Charles Czeisler, Eugene Aserinsky | 查尔斯·蔡斯勒，尤金·阿瑟林斯基 |
| Alexander Borbély; Hans Van Dongen, David Dinges | 亚历山大·博尔贝伊；汉斯·范东恩，戴维·丁格斯 |
| Björn Rasch, Jan Born; Allan Hobson, Robert McCarley, Mark Solms | 比约恩·拉施，扬·博恩；艾伦·霍布森，罗伯特·麦卡利，马克·索姆斯 |
| Richard Solomon, John Corbit; Shepard Siegel | 理查德·所罗门，约翰·科比特；谢泼德·西格尔 |
| Yerkes, Dodson; Gustav Fechner | 耶基斯，多德森；古斯塔夫·费希纳 |
| Mammoth Cave; Seattle, Rochester, Philadelphia, Kansas, Leipzig | 猛犸洞；西雅图，罗切斯特，费城，堪萨斯，莱比锡 |
| Hessel de Vries, Albert Rose; Joseph Plateau, Joseph Delboeuf | 赫塞尔·德弗里斯，阿尔伯特·罗斯；约瑟夫·普拉托，约瑟夫·德尔伯夫 |
| S. S. Stevens, Gösta Ekman, E. C. Poulton | 史蒂文斯，约斯塔·埃克曼，普尔顿 |
| Harry Levitt; Andrew Watson, Denis Pelli; Felix Wichmann, Jeremy Hill | 哈里·莱维特；安德鲁·沃森，丹尼斯·佩利；费利克斯·维希曼，杰里米·希尔 |
| Daniel Bernoulli; Louis Thurstone; John Gibbon; Kingdom and Prins | 丹尼尔·伯努利；路易斯·瑟斯顿；约翰·吉本；金登和普林斯 |
| Norman Mackworth; Wilson Tanner, John Swets, Theodore Birdsall; Peterson, Fox | 诺曼·麦克沃思；威尔逊·坦纳，约翰·斯韦茨，西奥多·伯索尔；彼得森，福克斯 |
| David Green; Roger Ratcliff; Andrew Yonelinas | 戴维·格林；罗杰·拉特克利夫；安德鲁·约内利纳斯 |
| Gerd Gigerenzer, Ulrich Hoffrage; David Eddy | 格尔德·吉仁泽，乌尔里希·霍夫拉格；戴维·埃迪 |
| Jeremy Wolfe, Todd Horowitz, Naomi Kenner; Fleck, Mitroff; See, Howe, Warm, Dember | 杰里米·沃尔夫，托德·霍罗威茨，娜奥米·肯纳；弗莱克，米特罗夫；西，豪，沃姆，登伯 |
| Robyn Dawes, John Monahan; Laura Mickes, Heather Flowe, John Wixted | 罗宾·道斯，约翰·莫纳汉；劳拉·米克斯，希瑟·弗洛，约翰·维克斯特德 |
| Brian Maniscalco, Hakwan Lau; Macmillan and Creelman | 布赖恩·马尼斯卡尔科，刘克顽；麦克米伦和克里尔曼 |
| Selig Hecht, Simon Shlaer, Maurice Pirenne; Hessel de Vries, Albert Rose | 塞利格·赫克特，西蒙·施拉尔，莫里斯·皮雷纳；赫塞尔·德弗里斯，阿尔伯特·罗斯 |
| Denis Baylor, Trevor Lamb, King-Wai Yau; Alipasha Vaziri (Tinsley et al.) | 丹尼斯·贝勒，特雷弗·兰姆，游景威；瓦齐里（廷斯利等） |
| Stephen Kuffler, Robert Rodieck, Ernst Mach; Clay Reid, José-Manuel Alonso | 斯蒂芬·库夫勒，罗伯特·罗迪克，恩斯特·马赫；克莱·里德，何塞-曼努埃尔·阿隆索 |
| Dennis Gabor; Fergus Campbell, John Robson, Colin Blakemore; David Heeger, Matteo Carandini | 丹尼斯·加博；弗格斯·坎贝尔，约翰·罗布森，科林·布莱克莫尔；大卫·黑格，马泰奥·卡兰迪尼 |
| Isaac Newton, Thomas Young, James Clerk Maxwell; Andrew Stockman, Lindsay Sharpe | 艾萨克·牛顿，托马斯·杨，詹姆斯·克拉克·麦克斯韦；安德鲁·斯托克曼，琳赛·夏普 |
| W. S. Stiles, J. M. Burch; William Wright, John Guild | 斯泰尔斯，伯奇；威廉·赖特，约翰·吉尔德 |
| Ewald Hering; Leo Hurvich, Dorothea Jameson; John Dalton; Masataka Okabe, Kei Ito | 埃瓦尔德·赫林；利奥·赫维奇，多萝西娅·詹姆森；约翰·道尔顿；冈部正隆，伊藤启 |
| Johannes von Kries; Rosa Lafer-Sousa, Katherine Hermann, Bevil Conway; Pascal Wallisch; Witzel, Racey, O'Regan | 约翰内斯·冯·克里斯；罗莎·拉弗-索萨，凯瑟琳·赫尔曼，贝维尔·康韦；帕斯卡·瓦利施；维策尔，雷西，奥里根 |
| Leslie Ungerleider, Mortimer Mishkin; Melvyn Goodale, David Milner; D.F. | 莱斯莉·昂格莱德，莫蒂默·米什金；梅尔文·古德尔，大卫·米尔纳；D.F. |
| Bruno Olshausen, David Field; Gabriele Jordan; Brian Wandell | 布鲁诺·奥尔斯豪森，大卫·菲尔德；加布里埃莱·乔丹；布赖恩·万德尔 |
| Edward Adelson; Hermann von Helmholtz; Adelbert Ames; Max Wertheimer; Gaetano Kanizsa; Edgar Rubin | 爱德华·阿德尔森；赫尔曼·冯·亥姆霍兹；阿德尔伯特·艾姆斯；马克斯·韦特海默；加埃塔诺·卡尼萨；埃德加·鲁宾 |
| Rüdiger von der Heydt; Charles Wheatstone; Bela Julesz; Mario Ponzo; Franz Müller-Lyer; Richard Gregory | 吕迪格·冯·德·海特；查尔斯·惠斯通；贝拉·尤勒斯；马里奥·庞佐；弗朗茨·米勒-莱尔；理查德·格雷戈里 |
| Marshall Segall, Donald Campbell, Melville Herskovits; Dorsa Amir, Chaz Firestone | 马歇尔·西格尔，唐纳德·坎贝尔，梅尔维尔·赫斯科维茨；多尔萨·阿米尔，查兹·费尔斯通 |
| Marc Ernst, Martin Banks; David Alais, David Burr; Monica Gori; Dobromir Rahnev, Rachel Denison | 马克·恩斯特，马丁·班克斯；大卫·阿莱，大卫·伯尔；莫妮卡·戈里；多布罗米尔·拉内夫，雷切尔·丹尼森 |
| Vilayanur Ramachandran; Wendy Adams, Erich Graf; Peter Thompson; Yair Weiss, Eero Simoncelli | 维拉亚努尔·拉马钱德兰；温迪·亚当斯，埃里希·格拉夫；彼得·汤普森；雅伊尔·韦斯，伊罗·西蒙切利 |
| Robert Snowden, Nicola Stimpson, Roy Ruddle; Paolo Pretto | 罗伯特·斯诺登，尼古拉·斯廷普森，罗伊·拉德尔；保罗·普雷托 |
| Edwin Land, John McCann; Alan Gilchrist; David Knill, Daniel Kersten | 埃德温·兰德，约翰·麦肯；艾伦·吉尔克里斯特；戴维·尼尔，丹尼尔·克斯滕 |
| David Marr; Irving Biederman; Heinrich Bülthoff, Shimon Edelman; Simon Thorpe | 戴维·马尔；欧文·比德曼；海因里希·比尔托夫，希蒙·埃德尔曼；西蒙·索普 |
| Robert Yin; Andrew Young; Nancy Kanwisher; Doris Tsao; Isabel Gauthier | 罗伯特·殷；安德鲁·扬；南希·坎维舍；曹颖；伊莎贝尔·高蒂尔 |
| Daniel Yamins, James DiCarlo; Robert Geirhos; Christian Szegedy | 丹尼尔·亚明斯，詹姆斯·迪卡洛；罗伯特·盖尔霍斯；克里斯蒂安·塞格迪 |
| David Hoffman, Martin Banks; Innes Cuthill; Karla Evans; Trafton Drew, Melissa Võ, Jeremy Wolfe; Kevin Eykholt | 戴维·霍夫曼，马丁·班克斯；因尼斯·卡思希尔；卡拉·埃文斯；特拉夫顿·德鲁，梅丽莎·沃，杰里米·沃尔夫；凯文·艾克霍尔特 |
| William Molyneux, John Locke; Richard Held, Pawan Sinha; Wai Keen Vong, Brenden Lake; James Gibson | 威廉·莫利纽克斯，约翰·洛克；理查德·赫尔德，帕万·辛哈；Wai Keen Vong，布伦登·莱克；詹姆斯·吉布森 |
| Alan Stocker; Jeffrey Bowers, Colin Davis | 艾伦·斯托克；杰弗里·鲍尔斯，科林·戴维斯 |
| Georg von Békésy; Donald Greenwood; David Kemp; William Brownell; Harvey Fletcher; Eberhard Terhardt | 格奥尔格·冯·贝凯西；唐纳德·格林伍德；戴维·肯普；威廉·布朗内尔；哈维·弗莱彻；埃伯哈德·特哈特 |
| August Seebeck; Georg Ohm; Jan Schouten; J. C. R. Licklider; Ray Meddis, Michael Hewitt | 奥古斯特·泽贝克；格奥尔格·欧姆；扬·斯豪滕；J. C. R. 利克莱德；雷·梅迪斯，迈克尔·休伊特 |
| Lord Rayleigh; Lloyd Jeffress; Antje Brand, Benedikt Grothe; Colin Cherry; Albert Bregman; Leon van Noorden | 瑞利勋爵；劳埃德·杰弗里斯；安特耶·布兰德，贝内迪克特·格罗特；科林·彻里；阿尔伯特·布雷格曼；莱昂·范诺登 |
| Alvin Liberman; Bob McMurray, Michael Tanenhaus, Richard Aslin; Harry McGurk, John MacDonald | 阿尔文·利伯曼；鲍勃·麦克默里，迈克尔·塔南豪斯，理查德·阿斯林；哈里·麦格克，约翰·麦克唐纳 |
| Debshila Mallick, John Magnotti, Michael Beauchamp; Reinier Plomp, Willem Levelt; Josh McDermott | 德布希拉·马利克，约翰·马格诺蒂，迈克尔·比彻姆；赖尼尔·普隆普，威廉·莱韦尔特；乔希·麦克德莫特 |
| Roland Johansson, Åke Vallbo; Guy Goodwin, Ian McCloskey, Peter Matthews; Matthew Botvinick, Jonathan Cohen; Peter Lush | 罗兰·约翰松，奥克·瓦尔博；盖伊·古德温，伊恩·麦克洛斯基，彼得·马修斯；马修·博特维尼克，乔纳森·科恩；彼得·拉什 |
| René Descartes; Henry Beecher; Ronald Melzack, Patrick Wall; Jon Levine, Newton Gordon, Howard Fields | 勒内·笛卡尔；亨利·比彻；罗纳德·梅尔扎克，帕特里克·沃尔；乔恩·莱文，牛顿·戈登，霍华德·菲尔兹 |
| Linda Buck, Richard Axel; David Hänig; Edwin Boring; Virginia Collings | 琳达·巴克，理查德·阿克塞尔；戴维·黑尼希；埃德温·波林；弗吉尼亚·柯林斯 |
| Caroline Bushdid; Richard Gerkin, Jason Castro; Markus Meister; James Reason, Joseph Brand | 卡罗琳·布什迪德；理查德·格金，贾森·卡斯特罗；马库斯·迈斯特；詹姆斯·里森，约瑟夫·布兰德 |
| Sharon Kujawa, Charles Liberman; Risto Näätänen; Brian Moore | 莎伦·库亚瓦，查尔斯·利伯曼；里斯托·纳塔宁；布赖恩·穆尔 |
| François-Emmanuel Roux; Evan Gordon | 弗朗索瓦-埃马纽埃尔·鲁；埃文·戈登 |
| Ivan Pavlov; Daniel Todes; Edward Thorndike; Rosalie Rayner; Ben Harris | 伊万·巴甫洛夫；丹尼尔·托德斯；爱德华·桑代克；罗莎莉·雷纳；本·哈里斯 |
| B. F. Skinner, Charles Ferster; Robert Rescorla, Allan Wagner; Leon Kamin; Bernard Widrow, Ted Hoff | 斯金纳，查尔斯·弗斯特；罗伯特·雷斯科拉，艾伦·瓦格纳；利昂·卡明；伯纳德·威德罗，特德·霍夫 |
| Edward Kremer; Gretchen Chapman, Steven Robbins; Edward Wasserman; Robert Lubow, Ulrich Moore | 爱德华·克雷默；格雷琴·查普曼，史蒂文·罗宾斯；爱德华·瓦瑟曼；罗伯特·卢博，乌尔里希·穆尔 |
| Mark Bouton, Robert Bolles; Nicholas Mackintosh; John Pearce, Geoffrey Hall; Randy Gallistel, John Gibbon | 马克·布顿，罗伯特·博尔斯；尼古拉斯·麦金托什；约翰·皮尔斯，杰弗里·霍尔；兰迪·加利斯特尔，约翰·吉本 |
| Richard Herrnstein, William Baum, Drazen Prelec; John Garcia, Robert Koelling; Keller and Marian Breland | 理查德·赫恩斯坦，威廉·鲍姆，德拉赞·普雷莱茨；约翰·加西亚，罗伯特·克林；凯勒和玛丽安·布里兰 |
| Martin Seligman; Albert Bandura, Dorothea Ross, Sheila Ross; Tom Beckers; David Zendle, Paul Cairns | 马丁·塞利格曼；阿尔伯特·班杜拉，多萝西娅·罗斯，希拉·罗斯；汤姆·贝克斯；戴维·曾德尔，保罗·凯恩斯 |
| Chris Mitchell, Jan De Houwer, Peter Lovibond; Sam Gershman, David Blei, Yael Niv; Daniela Schiller | 克里斯·米切尔，扬·德豪尔，彼得·洛维邦德；萨姆·格什曼，戴维·布莱，亚埃尔·尼夫；达妮埃拉·席勒 |
| Wolfram Schultz, Peter Dayan, Read Montague; Richard Bellman, Richard Sutton, Andrew Barto; Arthur Samuel | 沃尔夫拉姆·舒尔茨，彼得·达扬，里德·蒙塔古；理查德·贝尔曼，理查德·萨顿，安德鲁·巴托；亚瑟·塞缪尔 |
| Elizabeth Steinberg, Patricia Janak; Chris Watkins; Michael Frank, Lauren Seeberger, Randall O'Reilly | 伊丽莎白·斯坦伯格，帕特里夏·贾纳克；克里斯·沃特金斯；迈克尔·弗兰克，劳伦·西伯格，兰德尔·奥赖利 |
| Herbert Robbins; William Thompson; Robert Wilson; Charles Honzik; John O'Keefe; May-Britt and Edvard Moser | 赫伯特·罗宾斯；威廉·汤普森；罗伯特·威尔逊；查尔斯·洪齐克；约翰·奥基夫；梅-布里特和爱德华·莫泽 |
| Christopher Adams, Tony Dickinson; Nathaniel Daw; Carolina Feher da Silva, Todd Hare; Ida Momennejad | 克里斯托弗·亚当斯，托尼·迪金森；纳撒尼尔·道；卡罗琳娜·费赫尔·达席尔瓦，托德·黑尔；伊达·莫梅内贾德 |
| Matthew Wilson, Bruce McNaughton; Mark Howe, Ann Graybiel; Will Dabney; David Redish; Lihong Li; Daniel Weintraub | 马修·威尔逊，布鲁斯·麦克诺顿；马克·豪，安·格雷比尔；威尔·达布尼；戴维·雷迪什；李力鸿；丹尼尔·温特劳布 |
| Harry Harlow; Jane Wang | 哈里·哈洛；简·王 |
| Daniel Simons, Christopher Chabris; Ronald Rensink, Kevin O'Regan, James Clark; Colin Cherry; Donald Broadbent | 丹尼尔·西蒙斯，克里斯托弗·查布里斯；罗纳德·伦辛克，凯文·奥里根，詹姆斯·克拉克；科林·彻里；唐纳德·布罗德本特 |
| Neville Moray; Noelle Wood, Nelson Cowan; Anne Treisman, Garry Gelade, Hilary Schmidt; J. Anthony Deutsch, Diana Deutsch | 内维尔·莫雷；诺埃尔·伍德，纳尔逊·考恩；安妮·特瑞斯曼，加里·格拉德，希拉里·施密特；J. 安东尼·多伊奇，戴安娜·多伊奇 |
| Nilli Lavie; Michael Posner, Yoav Cohen; Jeremy Wolfe; Laurent Itti, Christof Koch, Ernst Niebur | 尼丽·拉维；迈克尔·波斯纳，约阿夫·科恩；杰里米·沃尔夫；劳伦特·伊蒂，克里斯托夫·科赫，恩斯特·尼布尔 |
| Brian Anderson, Patryk Laurent, Steven Yantis; Edward Awh, Artem Belopolsky, Jan Theeuwes; Steven Most | 布赖恩·安德森，帕特里克·洛朗，史蒂文·扬蒂斯；爱德华·奥，阿尔乔姆·别洛波利斯基，扬·西韦斯；史蒂文·莫斯特 |
| Trafton Drew, Melissa Võ; Jane Raymond, Kimron Shapiro, Karen Arnell; Harold Pashler; John Ridley Stroop, Colin MacLeod | 特拉夫顿·德鲁，梅利莎·沃；简·雷蒙德，金伦·夏皮罗，卡伦·阿内尔；哈罗德·帕什勒；约翰·里德利·斯特鲁普，科林·麦克劳德 |
| Barbara and Charles Eriksen; Matthew Botvinick, Jonathan Cohen; Gabriele Gratton; Robert Rogers, Stephen Monsell | 芭芭拉·埃里克森和查尔斯·埃里克森；马修·博特维尼克，乔纳森·科恩；加布里埃莱·格拉顿；罗伯特·罗杰斯，斯蒂芬·蒙塞尔 |
| Jeffrey Moran, Robert Desimone, John Duncan; David Heeger, John Reynolds; Katrin Herrmann, Marisa Carrasco | 杰弗里·莫兰，罗伯特·德西蒙，约翰·邓肯；大卫·希格，约翰·雷诺兹；卡特琳·赫尔曼，玛丽莎·卡拉斯科 |
| Claus Bundesen; George Sperling; Norman Mackworth; Mathias Fleck, Stephen Mitroff; David Strayer, William Johnston | 克劳斯·邦德森；乔治·斯珀林；诺曼·麦克沃思；马蒂亚斯·弗莱克，斯蒂芬·米特罗夫；戴维·斯特雷耶，威廉·约翰斯顿 |
| Eyal Ophir, Clifford Nass, Anthony Wagner; Reza Wiradhany, Mark Nieuwenstein; Robert Lubow; Paul Dux, René Marois | 埃亚勒·奥菲尔，克利福德·纳斯，安东尼·瓦格纳；雷扎·维拉德哈尼，马克·纽文斯坦；罗伯特·卢博；保罗·达克斯，勒内·马鲁瓦 |
| Ayelet Landau, Pascal Fries; Ashish Vaswani | 阿耶莱特·兰道，帕斯卡尔·弗里斯；阿希什·瓦斯瓦尼 |

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
