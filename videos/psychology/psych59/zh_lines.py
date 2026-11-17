"""Chinese narration for psych59: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第59部分：计算精神病学'

CHAPTERS = {
    'Hook': '稳健的效应，不可靠的个人',
    'Predict': '1. 在你身上：设计一个任务，以及四个数字',
    'Programme': '2. 研究纲领',
    'Compulsivity': '3. 强迫性与基于模型的控制',
    'Volatility': '4. 不确定性下的学习',
    'Mood': '5. 作为计算的心境',
    'Measure': '6. 修正测量',
    'Biotypes': '7. 生物型',
    'Travel': '8. 无法迁移的预测',
    'Selection': '9. 选择一种治疗',
    'Stimulation': '10. 新的干预',
    'Phones': '11. 数字表型',
    'Targets': '12. 什么才算一个计算靶点',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：评估一项生物标志物主张',
    'Frontier': '15. 前沿：临床级的测验组',
    'Outro': '回顾、习题与前方的路',
}

ZH = {
    'Before we start. This part is about psychiatry and mental illness, including depression, a':
        "开始之前。这一部分讲精神病学与精神疾病，包括抑郁、焦虑和强迫相关障碍。<bookmark mark='a'/>它是教育，不是诊断或治疗。如果其中有任何内容触及你自己的生活，请和医生、心理咨询师或你信任的人谈一谈。<bookmark mark='b'/>如果你现在处于危险之中，请拨打当地的紧急电话。在美国，你可以拨打或发短信到988。在英国和爱尔兰，撒玛利亚会的电话是116 123。在其他国家，findahelpline.com 列出了免费、保密的求助热线。",
    "Here's the plan of computational psychiatry. <bookmark mark='a'/> Give a patient a task fr":
        "这是计算精神病学的计划。<bookmark mark='a'/>给患者一个来自第四幕和第五幕的任务，拟合模型，读出出了问题的那个参数，然后选择治疗。<bookmark mark='b'/>但这里有第一个障碍。Psyche的四百人做了两次类似斯特鲁普的任务。群体效应巨大，t统计量接近五十。<bookmark mark='c'/>但每个人的效应几乎无法重复：重测相关约为零点三。<bookmark mark='d'/>克雷格·赫奇、加文·鲍威尔和佩特罗克·萨姆纳在2018年把它称为信度悖论。这些任务之所以被信任，是因为每个人都表现出这个效应，而这恰恰是它们无法区分不同个人的原因。<bookmark mark='e'/>这一部分讲的是一个年轻领域的承诺，以及它不得不重新学习的第3部分的测量规范。",
    "So this part asks: can a model of the mind tell a clinician something a conversation can't":
        "所以这一部分要问：一个心智模型能告诉临床医生一些谈话无法告诉的东西吗？<bookmark mark='a'/>研究纲领，以及两个实例。<bookmark mark='b'/>测量：信度、生物型，以及能够迁移的预测。<bookmark mark='c'/>选择治疗，以及新的干预。<bookmark mark='d'/>还有手机，以及什么才算一个靶点。",
    "This is Part 59 of Psychology, Built: computational psychiatry. <bookmark mark='a'/> We'll":
        "这是《心理学，从零搭建》第59部分：计算精神病学。<bookmark mark='a'/>我们会认识信度悖论，并计算它要付出多少试次。我们会区分理论驱动和数据驱动的研究纲领。我们会把强迫性、波动性和心境看作计算。我们会在没有类型的数据中找到生物型，并学会如何分辨。我们会看着预测在一项新试验中失败，并为选择治疗的试验确定样本量。我们还会用第2部分的标准来评判刺激疗法、迷幻剂和手机。",
    'Chapter one. On you: design a task, and four numbers.':
        '第1章。在你身上：设计一个任务，以及四个数字。',
    "First, a slider. <bookmark mark='a'/> On the course site, you move a task's effect between":
        "首先，一个滑块。<bookmark mark='a'/>在课程网站上，你可以把一个任务的效应在统一和多变之间移动：统一时每个人都表现出这个效应，多变时人与人之间有差异。<bookmark mark='b'/>统一会带来巨大的群体效应和毫无用处的信度。多变则相反。<bookmark mark='c'/>这里的每条曲线对应一个试次数，只有更多的试次才能两者兼得。<bookmark mark='d'/>代价是与患者相处的时间，这是门诊真正的货币。",
    "Now four numbers. <bookmark mark='a'/> One: a task's effect with two hundred trials per co":
        "现在是四个数字。<bookmark mark='a'/>第一：一个任务的效应在每种条件两百个试次时信度为零点五。要达到零点九需要多少试次？<bookmark mark='b'/>第二：对两百二十名患者完全没有亚组的脑数据进行聚类。各聚类在症状上出现差异的频率有多高？<bookmark mark='c'/>第三：一个模型在它自己的试验中预测治疗结果的AUC为零点七二。在一项新试验中会怎样？<bookmark mark='d'/>第四：一项证明某种治疗有效的试验需要三百五十名患者。要证明一条选择治疗的规则有效，需要多少人？在这里暂停，把答案写下来。",
    'Chapter two. The programme.':
        '第2章。研究纲领。',
    "What is computational psychiatry trying to do? <bookmark mark='a'/> The theory-driven rout":
        "计算精神病学想要做什么？<bookmark mark='a'/>理论驱动的路线把一个机制的模型，学习、推断或选择的模型，拟合到一个任务上，并把参数看作障碍所在之处。昆廷·休斯、蒂亚戈·马亚和迈克尔·弗兰克在2016年阐述了这一路线。<bookmark mark='b'/>数据驱动的路线对许多测量使用机器学习，预测诊断、病程或治疗反应，可以有机制，也可以没有。<bookmark mark='c'/>二者之间的桥梁是先拟合机制模型，再把它们的参数作为预测的特征。<bookmark mark='d'/>两条路线都需要在个体身上可靠的测量，以及在新样本中依然成立的预测。",
    "What has it delivered so far? <bookmark mark='a'/> Robust group findings: altered learning":
        "到目前为止它交付了什么？<bookmark mark='a'/>稳健的群体发现：抑郁中从惩罚中学习的改变，强迫性维度上基于模型的控制的减弱，以及精神病中的异常显著性。<bookmark mark='b'/>新的任务和模型，以及让个体差异研究成为可能的大型在线样本。<bookmark mark='c'/>但还没有经过验证的临床测试。在常规照护中，没有哪个参数被用来诊断或选择治疗。<bookmark mark='d'/>原因就是这一部分的各章：信度、重复与推广。",
    'Chapter three. Compulsivity and model-based control.':
        '第3章。强迫性与基于模型的控制。',
    "Is compulsion a habit that planning can't override? <bookmark mark='a'/> Part 17's two-ste":
        "强迫是一种计划无法压倒的习惯吗？<bookmark mark='a'/>第17部分的两步任务，把无模型学习，即重复得到奖励的行为，与基于模型的计划，即利用任务结构，区分开来。<bookmark mark='b'/>2016年，克莱尔·吉兰及其同事让约一千四百名在线参与者完成这项任务和许多症状问卷。<bookmark mark='c'/>对问卷的因素分析发现了三个跨诊断维度。其中一个，强迫行为与侵入性思维，与较少的基于模型的控制相关联。<bookmark mark='d'/>这种关联存在于一个跨越诊断的维度上，就像第39部分那样，而不是与任何一个诊断相关联。",
    "What limits it? <bookmark mark='a'/> Size: the association is small. It describes a popula":
        "它受到什么限制？<bookmark mark='a'/>大小：这种关联很小。它描述的是总体，而不是一位患者，这是第47部分的观点。<bookmark mark='b'/>信度：任务的基于模型指数的重测信度不高。真实相关为零点五，用信度分别为零点四和零点八的测量来测，看起来约为零点二八。<bookmark mark='c'/>重复：这一在线发现已在更多的在线和临床样本中得到重复。<bookmark mark='d'/>下一步是证明改变基于模型的控制能改变强迫。这需要一项干预，而不是一个相关。",
    'Chapter four. Learning under uncertainty.':
        '第4章。不确定性下的学习。',
    "Does anxiety change how fast people learn? <bookmark mark='a'/> In 2007 Timothy Behrens an":
        "焦虑会改变人们学习的速度吗？<bookmark mark='a'/>2007年，蒂莫西·贝伦斯及其同事发现，当世界多变时，人们会提高学习率，正如第17部分的贝叶斯学习者应该做的那样。<bookmark mark='b'/>2015年，迈克尔·布朗宁及其同事发现，在一个稳定区块与多变区块交替的任务中，特质焦虑高的人对学习率的调整更少。<bookmark mark='c'/>这种解释是：焦虑是一种难以利用世界的统计规律来决定学多少的困难。<bookmark mark='d'/>后来样本更大的研究对这一缺陷的发现并不一致。",
    'A model built for this is the hierarchical Gaussian filter, here in outline. <bookmark mar':
        "为此构建的一个模型是层次高斯滤波器，这里是它的轮廓。<bookmark mark='a'/>第一层是每个试次发生的事情，有奖励或没有。<bookmark mark='b'/>第二层是结果所来自的倾向，它随时间漂移。<bookmark mark='c'/>第三层是这个倾向漂移得有多快：波动性。<bookmark mark='d'/>学习率从模型中自然得出，当认为波动性高时就更高，就像卡尔曼滤波器的增益。<bookmark mark='e'/>而参数，一个人认为世界变化有多大，以及他们多快更新这一信念，都是候选的计算靶点。",
    'Chapter five. Mood as computation.':
        '第5章。作为计算的心境。',
    "What is a mood, computationally? <bookmark mark='a'/> In 2014 Robb Rutledge and colleagues":
        "从计算上说，心境是什么？<bookmark mark='a'/>2014年，罗布·拉特利奇及其同事发现，在一个赌博任务中，片刻的幸福感由近期的期望奖励和奖励预测误差预测，即第17部分的信号，而不是由总赢利预测。<bookmark mark='b'/>同一个模型拟合了约一万八千名智能手机应用用户的评分。<bookmark mark='c'/>埃兰·埃尔达尔和雅埃尔·尼夫提出心境是一种动量：近期预测误差的积分，它会使人们感知新结果的方式产生偏差。这是一个可能滑向躁狂或抑郁的回路。<bookmark mark='d'/>其前景是把心境障碍看作设置错误的积分器。迄今的证据来自健康样本和模型，而不是患者。",
    "How would a computational account of mood be tested? <bookmark mark='a'/> Prediction: does":
        "如何检验关于心境的计算解释？<bookmark mark='a'/>预测：从一周的评分中拟合出的积分器时间常数，能否预测下一个月的病程？<bookmark mark='b'/>信度：在同一个人身上，它在几周之间是否稳定？<bookmark mark='c'/>干预：改善心境的治疗是否会改变这个参数，而且这种改变是否先发生？<bookmark mark='d'/>每一步都是一项独立的研究，而做过的很少。",
    "Here's the idea run forward. <bookmark mark='a'/> Forty gambles, with a run of losses in t":
        "这里把这个想法向前运行。<bookmark mark='a'/>四十次赌博，中间有一连串的输。柱子是预测误差。<bookmark mark='b'/>两个模拟的人权重相同，区别只在于过去的误差消退得有多慢。<bookmark mark='c'/>慢的积分器在顺利时摆得更高，在连输时则低得多：约零点一五对零点三一。<bookmark mark='d'/>一个参数，一个时间常数，区分出了有韧性的心境和黏滞的心境。这正是这个研究纲领想要的靶点，前提是它能被可靠地测量，而那是第六章的问题。",
    'Chapter six. Fixing measurement.':
        '第6章。修正测量。',
    "How many trials does a person need? <bookmark mark='a'/> Spearman and Brown's formula, fro":
        "一个人需要多少试次？<bookmark mark='a'/>第3部分的斯皮尔曼-布朗公式说，试次噪声按试次数的倒数缩小，而真实差异不会。<bookmark mark='b'/>Psyche的任务在六十个试次时信度约为零点三。<bookmark mark='c'/>要达到零点九，每种条件大约需要一千一百五十个试次。这在一个任务上要花去大半个小时。<bookmark mark='d'/>还有你的第一个数字：在两百个试次时信度为零点五，要达到零点九需要九倍的试次。也就是一千八百个。",
    "What does unreliability do to a correlation? <bookmark mark='a'/> Part 3's attenuation for":
        "不可靠性对相关有什么影响？<bookmark mark='a'/>第3部分的衰减公式：观测到的相关等于真实相关乘以两个信度乘积的平方根。<bookmark mark='b'/>一个参数与一种症状之间零点五的真实关联，在任务信度为零点二时，看起来只有零点二。<bookmark mark='c'/>把小样本和低信度放在一起，关联就会被漏掉，而被发现的那些则被夸大：第4部分的赢家诅咒。<bookmark mark='d'/>许多已发表的参数与症状之间的相关，都在零点一到零点三之间。",
    "What fixes it? <bookmark mark='a'/> Model the trials. Hierarchical models estimate each pe":
        "什么能修正它？<bookmark mark='a'/>对试次建模。层次模型估计每个人的效应及其噪声，而不是取两个均值之差。这是杰弗里·劳德和朱莉娅·哈夫的观点，也是第48部分的工具。<bookmark mark='b'/>跳过差值。使用模型的参数，或者原始的速度和准确率，它们往往比差异分数更可靠。<bookmark mark='c'/>分散试次。在许多天里、在家用手机进行的简短测试，能平均掉状态不好的日子。<bookmark mark='d'/>报告信度。每一项个体差异研究都应该报告其测量在自己样本中的信度。<bookmark mark='e'/>以及为个人而设计：选择人与人之间有差异的条件，而不是每个人都表现出效应的条件。",
    'Chapter seven. Biotypes.':
        '第7章。生物型。',
    "Are there kinds of depression in the brain? <bookmark mark='a'/> In 2017 Andrew Drysdale a":
        "大脑中存在不同种类的抑郁症吗？<bookmark mark='a'/>2017年，安德鲁·德赖斯代尔及其同事分析了约一千二百人的静息态扫描。<bookmark mark='b'/>他们选出与症状最相关的连接特征，然后据此对患者进行聚类。<bookmark mark='c'/>他们找到了四个聚类，症状特征不同，在一个子集中对磁刺激的反应也不同。<bookmark mark='d'/>这是一个承诺：一次扫描就能告诉你一个人患的是哪种抑郁症，以及该给哪种治疗。",
    "Now run the same pipeline on data with no types. <bookmark mark='a'/> Psyche's two hundred":
        "现在，在没有类型的数据上运行同样的流程。<bookmark mark='a'/>Psyche的两百二十名患者有二十个连接特征，完全没有亚组。症状与其中三个特征弱相关。<bookmark mark='b'/>这个流程保留与症状最相关的六个特征，把患者聚成四类，再检验各聚类在症状上是否有差异。<bookmark mark='c'/>在十项模拟研究中有九项，它们确实有差异，p小于零点零五。这就是你的第二个数字。<bookmark mark='d'/>特征是因为与症状有关联才被选出来的，所以无论怎么切分，得到的组都会不同。这是循环分析：第8部分的重复使用数据。",
    'How do you tell real types from fake ones? Split the sample and see if the clusters come b':
        "如何区分真实的类型和虚假的类型？把样本分开，看聚类是否会再次出现。<bookmark mark='a'/>分别对两个随机的一半进行聚类，按每一半的中心给所有人分配类别，然后比较标签。<bookmark mark='b'/>没有类型时，一致性约为零点一六。每次的聚类都不一样。<bookmark mark='c'/>当Psyche中植入了真实的类型时，一致性约为零点七四。聚类会再次出现。<bookmark mark='d'/>2019年，理查德·丁加及其同事在一百八十七人身上重新进行了生物型分析。聚类并不稳定，而且没有聚类的数据也给出了类似的结果。",
    'Chapter eight. Prediction that does not travel.':
        '第8章。无法迁移的预测。',
    "Will a model that predicts response work in the next clinic? <bookmark mark='a'/> In 2016 ":
        "一个能预测疗效的模型，在下一个诊所也能用吗？<bookmark mark='a'/>2016年，亚当·切克劳德及其同事从一项大型抗抑郁药试验的约一千九百名患者中提取了二十五个基线问题，训练了一个预测谁会缓解的机器学习模型。<bookmark mark='b'/>在另一项试验中检验时，它在相似药物组中准确率约为百分之六十，在另一种药物组中仅略好于随机。<bookmark mark='c'/>2024年，同一团队取五项抗精神病药试验，在其中一项上训练，在其他几项上检验。<bookmark mark='d'/>模型在构建它们的那项试验中表现很好，在其他试验中则接近随机。",
    "Here are three accuracies for one model. <bookmark mark='a'/> Psyche's trials have three h":
        "这里是一个模型的三种准确率。<bookmark mark='a'/>Psyche的试验有三百名患者和四十个基线特征，其中三个有微弱的预测力。模型保留十个最好的特征，拟合一个逻辑回归。<bookmark mark='b'/>在构建它的数据上评分，AUC为零点七二。<bookmark mark='c'/>诚实的交叉验证，即在每一折内部进行特征选择，给出零点五九。<bookmark mark='d'/>在另一个地点的一项新试验中，关系略有漂移，结果是零点五七。这就是你的第三个数字。",
    "Why doesn't prediction travel? <bookmark mark='a'/> Selection on all the data: choosing fe":
        "为什么预测无法迁移？<bookmark mark='a'/>在全部数据上做选择：在交叉验证之前选择特征，会把答案泄漏到估计中。<bookmark mark='b'/>不同的患者：纳入标准、地点和严重程度会改变特征的分布。<bookmark mark='c'/>不同的关系：方案、剂量和评定者会改变特征与结果之间的关系。<bookmark mark='d'/>微弱的信号：当真实信号很弱时，模型学到的噪声在它所知道的东西中占了很大一部分。<bookmark mark='e'/>应当要求的标准是：在一个独立样本中进行外部验证，并在运行之前注册，正如TRIPOD报告指南所规定的。",
    'Chapter nine. Choosing a treatment.':
        '第9章。选择一种治疗。',
    "Can data say which treatment suits which person? <bookmark mark='a'/> In 2014 Robert DeRub":
        "数据能说出哪种治疗适合哪个人吗？<bookmark mark='a'/>2014年，罗伯特·德鲁贝斯及其同事取一项认知疗法对比抗抑郁药的试验，为每位患者在每种治疗下的结果拟合了一个模型。<bookmark mark='b'/>这个指数是一种治疗下的预测结果减去另一种治疗下的预测结果：一位患者的预测优势。<bookmark mark='c'/>大多数患者的预测优势很小。对少数人来说，预测的差异在临床上是有意义的。<bookmark mark='d'/>真正重要的检验是：把患者随机分配到按指数选择治疗或按常规选择治疗，然后比较。",
    "What does it cost to show that a choice rule works? <bookmark mark='a'/> A rule helps only":
        "证明一条选择规则有效需要付出什么？<bookmark mark='a'/>只有当治疗对不同的人效果不同时，规则才有帮助。在统计上，这是治疗与调节变量之间的交互作用。<bookmark mark='b'/>要以百分之八十的功效证明一个大小为零点三的主效应，大约需要三百五十名患者。<bookmark mark='c'/>同样大小的交互作用需要四倍的人数，约一千四百人。这就是你的第四个数字。<bookmark mark='d'/>而真实的交互作用通常比主效应小，所以很少有试验足够大。",
    "What works while we wait? <bookmark mark='a'/> Measurement-based care: measure symptoms ev":
        "在等待的同时，什么是有效的？<bookmark mark='a'/>基于测量的照护：每次就诊都测量症状，在进展停滞时改变治疗。这是第57部分的反馈。<bookmark mark='b'/>阶梯式照护：从可能有效的最低强度治疗开始，再让无反应者升级。<bookmark mark='c'/>共同决策：患者的偏好和副作用，是模型所没有的信息。<bookmark mark='d'/>还有序贯试验，在每一步都重新随机分配，这种设计称为SMART，用来了解下一步怎么做最好。",
    'Chapter ten. New interventions.':
        '第10章。新的干预。',
    "What do new interventions show? First, stimulating the brain. <bookmark mark='a'/> Transcr":
        "新的干预说明了什么？首先是刺激大脑。<bookmark mark='a'/>经颅磁刺激在前额叶皮层上方发送磁脉冲。它于2008年在美国获准用于治疗抑郁症，元分析发现它比假刺激有温和的益处。<bookmark mark='b'/>加速方案每天进行多次治疗，按每个人的连接图谱定位。2022年，埃莉诺·科尔及其同事在一项二十九人的试验中报告了相对于假刺激的巨大益处。<bookmark mark='c'/>深部脑刺激把电极植入膝下扣带回。2005年它在少数患者身上取得了惊人的开放性结果，随后一项更大的假刺激对照试验因无效而被叫停。<bookmark mark='d'/>教训是：关于设备的小型开放性研究会高估效果。决定性的是假刺激对照和样本量。",
    "Second, fast-acting drugs. <bookmark mark='a'/> A single infusion of ketamine lifts depres":
        "其次是速效药物。<bookmark mark='a'/>单次输注氯胺酮能在数小时内缓解部分患者的抑郁症状。艾司氯胺酮鼻喷雾剂于2019年获批。效果会在几天内消退。<bookmark mark='b'/>赛洛西宾：2022年，盖伊·古德温及其同事给两百三十三名患者服用了二十五毫克或一毫克的剂量。三周时症状下降更多，到十二周时差异较小且不确定。<bookmark mark='c'/>问题在于盲法。人们通常知道自己是否服用了迷幻剂，所以期待，也就是第57部分的主题，是每个结果的一部分。<bookmark mark='d'/>所提出的机制，放松的先验和可塑性，都是计算性的，还有待检验。",
    "So judge them by Part 2's standards. <bookmark mark='a'/> Randomization and a credible con":
        "所以要用第2部分的标准来评判它们。<bookmark mark='a'/>随机化和可信的对照：假线圈、活性安慰剂或低剂量。<bookmark mark='b'/>检查盲法，而不是假定盲法有效：问患者和评定者他们认为给的是什么。<bookmark mark='c'/>持续数月而不是数天的结果。<bookmark mark='d'/>足够多的患者，让估计值不只是一个幸运的样本，就像第4部分那样。<bookmark mark='e'/>以及由与该治疗没有利害关系的团队进行的重复。",
    'Chapter eleven. Digital phenotyping.':
        '第11章。数字表型。',
    "Can a phone measure a mood? <bookmark mark='a'/> In 2017 Thomas Insel argued that phones r":
        "一部手机能测量心境吗？<bookmark mark='a'/>2017年，托马斯·因塞尔提出，手机持续记录着运动、睡眠、打字和通话，所以数字表型可以在两次就诊之间追踪病情。<bookmark mark='b'/>主动数据是每天几次的简短问卷，即第47部分的经验取样。<bookmark mark='c'/>被动数据来自GPS、加速度计、屏幕使用和通话，不需要当事人付出任何努力。<bookmark mark='d'/>早期对几十人的研究发现，GPS特征与抑郁分数之间有很强的关联。更大规模的研究发现的关联则弱得多。",
    "Here's why. <bookmark mark='a'/> Four hundred simulated studies of a phone feature whose t":
        "原因在这里。<bookmark mark='a'/>四百项模拟研究，研究一个与心境的真实相关为零点二的手机特征。<bookmark mark='b'/>只有三十人时，相关的范围很宽，有百分之几超过零点五。<bookmark mark='c'/>有三百人时，它们聚集在真值附近。<bookmark mark='d'/>早期的强结果是小样本中幸运的尾部，被选中发表了，就像第4部分那样。",
    "What can a phone do, and what can't it? <bookmark mark='a'/> Within a person, changes from":
        "手机能做什么，不能做什么？<bookmark mark='a'/>在个人内部，相对于自己基线的变化，即第47部分的想法，可能比人与人之间的比较更有用。<bookmark mark='b'/>缺失数据：人们会停止使用应用，而没有数据的日子可能正是最糟糕的日子。<bookmark mark='c'/>隐私：位置和消息是私密的，所以知情同意、存储以及谁能看到数据，都是设计的一部分。<bookmark mark='d'/>还有行动：只有当有人能及时据此采取行动，而且有人参与其中时，一个信号才有用。",
    'Chapter twelve. What would count as a computational target.':
        '第12章。什么才算一个计算靶点。',
    "When is a parameter ready for the clinic? Here are five tests. <bookmark mark='a'/> It's r":
        "一个参数什么时候可以进入门诊？这里有五项检验。<bookmark mark='a'/>它是可靠的：重测信度高到足以定位一个人，约为零点八或以上。<bookmark mark='b'/>它与症状的关联在样本之外成立，在一个新样本中，而不只是在发现它的那个样本中。<bookmark mark='c'/>有效的治疗会改变它。<bookmark mark='d'/>它的变化在前：参数在症状之前发生变化，并承载了效应。<bookmark mark='e'/>同样的结果在新的地点也成立：其他诊所、国家和设备。",
    'Here are four candidates from this part, scored against the five tests, as the published r':
        "这里是这一部分的四个候选者，按已发表的记录，对照五项检验打分。<bookmark mark='a'/>基于模型的控制：它与强迫性的关联已在样本外和跨地点得到重复；信度好坏参半，用层次模型更好。治疗能否改变它，证据不一，它的变化是否在前，尚未检验。<bookmark mark='b'/>波动性下的学习率：信度和重复都好坏参半，其余尚未检验。<bookmark mark='c'/>心境积分器：有前景，大多尚未检验。<bookmark mark='d'/>连接生物型则没能通过稳定性和重复检验。<bookmark mark='e'/>还没有哪个参数通过全部五项。这就是一个年轻领域的诚实现状。",
    'Chapter thirteen. The Ledger.':
        '第13章。账本。',
    'Four new rows. The first: tasks with robust group effects measure individual differences p':
        "四个新条目。第一条：具有稳健群体效应的任务，对个体差异的测量很差。<bookmark mark='a'/>原始研究：赫奇、鲍威尔与萨姆纳，2018年。<bookmark mark='b'/>记录：一项关于自我调节任务的大型重测研究，以及对噪声的层次解释。<bookmark mark='c'/>这个悖论是算术。<bookmark mark='d'/>已重复。",
    'The second: weaker model-based control goes with a compulsive dimension that cuts across d':
        "第二条：较弱的基于模型的控制，与一个跨越诊断的强迫维度相关联。<bookmark mark='a'/>原始研究：吉兰及其同事，2016年。<bookmark mark='b'/>记录：一项激励研究，以及有和没有强迫症诊断的患者。<bookmark mark='c'/>一个小的总体层面的关联，受信度所限。<bookmark mark='d'/>已重复。",
    "The third: brain connectivity divides depression into four biotypes. <bookmark mark='a'/> ":
        "第三条：大脑连接把抑郁症分为四种生物型。<bookmark mark='a'/>原始研究：德赖斯代尔及其同事，2017年。<bookmark mark='b'/>记录：一项方法学重复，发现聚类不稳定。<bookmark mark='c'/>循环选择保证了聚类之间会有差异。<bookmark mark='d'/>存在争议。",
    'And the fourth: a model trained in one trial predicts who responds in others. <bookmark ma':
        "第四条：在一项试验中训练的模型，能预测其他试验中谁会有反应。<bookmark mark='a'/>原始研究：切克劳德及其同事，2016年。<bookmark mark='b'/>记录：五项抗精神病药试验，模型在各项之间接近随机。<bookmark mark='c'/>在本地的准确率夸大了在外地的准确率。<bookmark mark='d'/>失败。",
    "What the four have in common. <bookmark mark='a'/> The group findings are real. Measuring ":
        "这四条有什么共同点。<bookmark mark='a'/>群体发现是真实的。测量个体才是瓶颈。<bookmark mark='b'/>失败有一个共同的原因：分析看到了自己的答案，无论是循环的聚类还是样本内的准确率。<bookmark mark='c'/>解决办法都是老办法：信度、留出的数据和独立的样本。<bookmark mark='d'/>所以这就是这一部分问题的答案。一个心智模型只有在个体层面通过第3部分和第4部分的检验之后，才能告诉临床医生一些新东西，而目前还没有一个做到。",
    'Chapter fourteen. In practice: evaluating a biomarker claim.':
        '第14章。实践中：评估一项生物标志物主张。',
    "Where is this a job? <bookmark mark='a'/> In computational psychiatry labs: tasks, models,":
        "这在哪里是一份工作？<bookmark mark='a'/>在计算精神病学实验室中：任务、模型，以及大型在线样本和临床样本。<bookmark mark='b'/>在数字健康公司中：卖给卫生系统的应用、传感和预测模型。<bookmark mark='c'/>在卫生技术评估中，它决定一项测试或设备是否值得付费。<bookmark mark='d'/>还有在监管机构中，它们批准设备以及作为医疗器械的软件。",
    "Here's a claim of the kind you'll meet. It's invented for this exercise, and describes no ":
        "这里是一个你会遇到的那类主张。它是为这个练习编造的，不描述任何真实的公司。<bookmark mark='a'/>“我们二十分钟的游戏加上一个AI模型，能以百分之八十五的准确率预测两种抗抑郁药中哪一种对你有效，研究涉及一百二十名患者。”<bookmark mark='b'/>你会问什么？",
    "Six questions. <bookmark mark='a'/> Was the eighty-five percent measured on patients the m":
        "六个问题。<bookmark mark='a'/>这百分之八十五是在模型从未见过的、来自另一个地点的患者身上测得的吗？这是第八章。<bookmark mark='b'/>特征是用全部一百二十名患者选出来的吗？这是第八章的泄漏。<bookmark mark='c'/>这个游戏的重测信度是多少？这是第六章。<bookmark mark='d'/>每位患者都服用了两种药，还是对的那种药是推断出来的？一条选择规则需要交互作用，而要证明一个交互作用需要约一千四百名患者。这是第九章。<bookmark mark='e'/>与什么相比：给每个人用更好的那种药，还是临床医生的选择？<bookmark mark='f'/>以及，按测试结果选择治疗对比常规照护的随机试验，注册了吗？",
    'Chapter fifteen. Frontier: a clinical-grade battery.':
        '第15章。前沿：临床级的测验组。',
    "What would a reliable computational assessment look like? <bookmark mark='a'/> Reliability":
        "一个可靠的计算评估会是什么样子？<bookmark mark='a'/>信度优先：按重测信度重新设计和挑选任务，并使用试次层面的层次模型。<bookmark mark='b'/>许多次简短的测试：在家中数周内玩的游戏，平均掉状态不好的日子。<bookmark mark='c'/>大型队列：数万名在线参与者，以及包含任务、症状和随访的人群队列。<bookmark mark='d'/>还有注册的验证：模型被冻结，并在其构建者从未见过的样本中检验。",
    "And the open problems. <bookmark mark='a'/> Mechanism or marker: is a parameter a cause of":
        "还有那些悬而未决的问题。<bookmark mark='a'/>机制还是标志：一个参数是疾病的原因，还是只是疾病的迹象？<bookmark mark='b'/>状态与特质：参数会随心境和睡眠变化，那么哪一部分才是这个人？<bookmark mark='c'/>按参数治疗：一项按计算测量分配治疗、并且胜出的试验。<bookmark mark='d'/>还有亲历经验：把患者认为的好转纳入模型。",
    "First, your four numbers. <bookmark mark='a'/> To go from a reliability of zero point five":
        "先看你的四个数字。<bookmark mark='a'/>要从两百个试次时零点五的信度提高到零点九，需要一千八百个试次。在没有类型的数据中，十项研究里有九项的聚类在症状上有差异。在Psyche中，一个在本地AUC为零点七二的模型，在新试验中得分零点五七。而证明一条选择规则有效需要约一千四百名患者，是证明治疗本身所需试验的四倍。<bookmark mark='b'/>群体效应是真实的。测量个体和推广，是剩下的工作。",
    "Part fifty-nine in twelve lines. <bookmark mark='a'/> Robust group effects can be unreliab":
        "第五十九部分，十二句话。<bookmark mark='a'/>稳健的群体效应可能是对个体不可靠的测量。理论驱动和数据驱动的路线需要同样的规范。强迫性与较少的基于模型的控制相关联。焦虑与波动性是一个证据好坏参半的想法。心境可能是预测误差的积分。更多的试次、层次模型和多次测试能修正测量。循环的聚类总会在症状上有差异，所以要检查它们的稳定性。样本内的准确率无法迁移。选择规则需要四倍的样本。刺激疗法和迷幻剂要用假刺激、盲法和样本量来评判。手机在小样本中的强相关会缩水。一个靶点有五项检验，目前还没有一个通过。",
    "Where this comes back. <bookmark mark='a'/> Models of minds, artificial and human, are Par":
        "这些内容会在哪里再出现。<bookmark mark='a'/>人工的和人类的心智模型，是第60部分。由大团队和注册模型构成的下一个心理学，是第61部分。而第62部分的学位论文可以研究个体的测量。",
    "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One buys r":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道用试次换取信度。一道衰减一个相关。一道修复一个有泄漏的流程。一道解读一次稳定性检查。一道为一条选择规则的试验确定样本量。一道给一项小研究的相关加上区间。最后带星号的一道，请你设计一项对计算治疗靶点的检验。如果想试一试，就在这里暂停。",
    "The books and papers behind this part are listed here and in the README. Peggy Series's pr":
        '这一部分所依据的书籍和论文列在这里，也列在README中。佩姬·塞里斯的入门书是了解这些模型的最佳读物；雷迪什和戈登编的文集概览了这个领域；而休斯、马亚和弗兰克的综述阐述了两条路线。',
    "Two parts of the frontier are done. <bookmark mark='a'/> This one asked whether models of ":
        "前沿的两部分已经完成。<bookmark mark='a'/>这一部分追问心智模型能否走进门诊，发现这条路要经过测量。<bookmark mark='b'/>下一部分问的是另一种模型：会说话的机器。大型语言模型能告诉心理学什么，心理学又能告诉我们关于它们的什么？第60部分：心智与机器。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
