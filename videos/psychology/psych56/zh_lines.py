"""Chinese narration for psych56: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第56部分：心理学与法律'

CHAPTERS = {
    'Hook': '一位确信的证人',
    'Predict': '1. 在你身上：一次列队辨认，以及四个数字',
    'Sdt': '2. 作为信号检测的列队辨认',
    'Sequential': '3. 同时列队与顺序列队',
    'Confidence': '4. 信心',
    'Reforms': '5. 系统变量与改革',
    'Confessions': '6. 虚假供述',
    'Lies': '7. 识别谎言',
    'Experts': '8. 专家也是人',
    'Children': '9. 儿童、暗示与植入的记忆',
    'Juries': '10. 陪审团与法官',
    'Risk': '11. 风险评估',
    'Numbers': '12. 法庭上的数字',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：权衡一次辨认',
    'Frontier': '15. 前沿：机器、询问与工具',
    'Outro': '回顾、习题与前方的路',
}

ZH = {
    "A witness picks a man from a line-up, and she's certain. <bookmark mark='a'/> The jury bel":
        "一位证人从列队中指认了一个男人，而且她很确定。<bookmark mark='a'/>陪审团相信了她，他进了监狱。<bookmark mark='b'/>多年以后，DNA检测表明罪行是另一个人犯下的。<bookmark mark='c'/>布兰登·加勒特研究美国最早的两百五十起DNA平反案件时发现，约四分之三涉及目击证人的错误辨认。<bookmark mark='d'/>法庭心理学就是第12部分的信号检测和第21部分的记忆，再系上一个人的自由。<bookmark mark='e'/>这一次，研究改变了实践。然后，它又改变了自己对其中一项改革的看法。",
    'So this part asks: how much should a court trust a memory, a confession or an expert? <boo':
        "所以这一部分要问：法庭应该在多大程度上信任一段记忆、一份供述或一位专家？<bookmark mark='a'/>列队辨认：检测、程序与信心。<bookmark mark='b'/>供述与谎言识别。<bookmark mark='c'/>专家、儿童与陪审团。<bookmark mark='d'/>还有风险工具与法庭上的数字。",
    "This is Part 56 of Psychology, Built: psychology and law. <bookmark mark='a'/> We'll treat":
        "这是《心理学，从零搭建》第56部分：心理学与法律。<bookmark mark='a'/>我们会把列队辨认当作信号检测，用ROC曲线来分析。我们会看到顺序列队为什么被采用，又为什么被放弃。我们会追问证人的信心什么时候可以信任。我们会看看虚假供述和谎言识别的局限。我们会看到法庭科学专家的情境偏差，以及暗示能够制造的记忆。我们还会认识风险工具、关于公平的不可能性结果，以及一个IQ分数周围的误差如何成了宪法。",
    'Chapter one. On you: a line-up, and four numbers.':
        '第1章。在你身上：一次列队辨认，以及四个数字。',
    "First, a line-up. <bookmark mark='a'/> On the course site there's a short staged event, th":
        "首先，一次列队辨认。<bookmark mark='a'/>课程网站上有一段简短的模拟事件，然后是一个六人列队，你要给出自己的信心。<bookmark mark='b'/>在Psyche的证人中，当罪犯在列队中时，约百分之五十六指认了他，百分之三十一指认了陪衬者，百分之十三谁也没指认。<bookmark mark='c'/>当罪犯不在列队中时，仍有百分之六十四的人指认了某个人，而如果嫌疑人是无辜的，百分之十一的人指认了他。<bookmark mark='d'/>公平的列队会把错误的指认分散到陪衬者身上，陪衬者是已知无辜的人，选中他们反而能洗清嫌疑人。",
    "Now four numbers. <bookmark mark='a'/> One: in a line-up where the culprit is absent, how ":
        "现在是四个数字。<bookmark mark='a'/>第一：在罪犯不在场的列队中，证人仍然指认某个人的频率有多高？<bookmark mark='b'/>第二：当人们判断别人是否在说谎时，判断正确的比例是多少？<bookmark mark='c'/>第三：在实验室里，被诬告弄坏了电脑的学生被要求签署一份供述。有多大比例签了？<bookmark mark='d'/>第四：一个IQ分数为七十一，测验信度为零点九七。它的百分之九十五区间是多少？在这里暂停，把答案写下来。",
    'Chapter two. The line-up as signal detection.':
        '第2章。作为信号检测的列队辨认。',
    "What is a witness deciding? <bookmark mark='a'/> Each face gives a memory-match signal. In":
        "证人在决定什么？<bookmark mark='a'/>每张面孔都会给出一个记忆匹配信号。无辜者的面孔集中在零附近，罪犯的面孔更高，这里高出一点五个标准差。<bookmark mark='b'/>如果最佳匹配超过某个标准，证人就选它。这是史蒂文·克拉克的模型，也是约翰·威克斯泰德和劳拉·米克斯的模型。<bookmark mark='c'/>宽松的标准会指认出更多罪犯，也会指认出更多无辜的嫌疑人。严格的标准两者都更少。<bookmark mark='d'/>所以评判一种程序必须看整个权衡，即第12部分那样的ROC曲线，而不是只看一对比率。",
    'Gary Wells divided the factors into two kinds. Estimator variables lower d prime, and the ':
        "加里·韦尔斯把因素分为两类。估计变量会降低d'，司法系统无法控制它们。<bookmark mark='a'/>观察条件：距离、光线和持续时间。在三十米外瞥一眼，不同于在三米处看一看。<bookmark mark='b'/>压力与武器：注意力被武器吸引，留给面孔的就少了。这就是武器聚焦效应，即第18部分的注意。<bookmark mark='c'/>跨种族效应：对其他群体面孔的辨认准确性更低，错误辨认更多。<bookmark mark='d'/>还有延迟：从犯罪到列队辨认之间的几周里，第21部分的遗忘在起作用。",
    'Chapter three. Simultaneous against sequential.':
        '第3章。同时列队与顺序列队。',
    "In 1985 a reform was proposed. <bookmark mark='a'/> Rod Lindsay and Gary Wells introduced ":
        "1985年，有人提出了一项改革。<bookmark mark='a'/>罗德·林赛和加里·韦尔斯引入了顺序列队：一次只看一张面孔，对每张面孔作出是或否的判断，而且不能回头。<bookmark mark='b'/>研究发现，对无辜嫌疑人的错误辨认更少了，正确辨认也更少了，但正确与错误之比更高，这个比值被称为诊断比。<bookmark mark='c'/>许多美国警察局采用了顺序列队。<bookmark mark='d'/>但这个比值取决于证人的标准设在哪里，而不只取决于一种程序区分有罪者和无辜者的能力。",
    "The ROC curve reversed it. <bookmark mark='a'/> Here are two typical operating points. Sim":
        "ROC曲线推翻了这个结论。<bookmark mark='a'/>这里是两个典型的工作点。同时列队，诊断比约为五。顺序列队，更加谨慎，约为七点五。按这个比值，顺序列队看起来更好。<bookmark mark='b'/>现在看整条曲线。在每一种错误辨认率下，同时列队都给出更多的正确辨认。<bookmark mark='c'/>约翰·威克斯泰德和劳拉·米克斯在2014年提出了这一论证，此后的实验室和现场数据都与之一致：顺序程序主要是移动了标准，还损失了一点区分能力。<bookmark mark='d'/>2020年的建议不再偏好顺序列队。一项该领域曾经大力倡导的改革，被它自己更好的测量推翻了。",
    'Chapter four. Confidence.':
        '第4章。信心。',
    "Can a witness's certainty be trusted? <bookmark mark='a'/> The old view said confidence is":
        "证人的确信可以信任吗？<bookmark mark='a'/>旧观点认为信心几乎毫无用处，因为总体而言，信心与准确性的相关很低。<bookmark mark='b'/>更好的问题是：在高信心作出的辨认中，有多大比例是正确的？这就是信心-准确性特征。<bookmark mark='c'/>在Psyche中，最低信心时约一半正确，最高信心时百分之九十六正确。<bookmark mark='d'/>约翰·威克斯泰德和加里·韦尔斯在2017年得出结论：在干净的程序下作出的高信心初次辨认具有很高的诊断性，而低信心的辨认是一个警示。",
    "But confidence grows after the fact. <bookmark mark='a'/> In 1998 Gary Wells and Amy Bradf":
        "但信心会在事后增长。<bookmark mark='a'/>1998年，加里·韦尔斯和埃米·布拉德菲尔德发现，被告知“很好，你认出了嫌疑人”的证人变得更有信心，并且记得自己当时看得更清楚。<bookmark mark='b'/>在Psyche中，同样的反馈让每一个指认嫌疑人的人提高约一个等级。在最高等级上，准确率从百分之九十六降到百分之九十三，而最高等级现在容纳了两倍的辨认。<bookmark mark='c'/>到了几个月后的审判，一个当初说“可能是三号”的证人会说“我永远忘不了那张脸”。<bookmark mark='d'/>所以算数的信心是第一次的信心，在列队辨认时，用证人自己的话记录下来。",
    'Chapter five. System variables and the reforms.':
        '第5章。系统变量与改革。',
    'System variables are the ones the justice system controls, and the reforms target them. <b':
        "系统变量是司法系统能够控制的变量，改革针对的正是它们。<bookmark mark='a'/>双盲施测：主持列队辨认的警官不知道谁是嫌疑人。这是去掉了第2部分的聪明汉斯。<bookmark mark='b'/>说明此人可能在也可能不在列队中，给证人谁也不指认的许可。<bookmark mark='c'/>公平的陪衬者：嫌疑人不应显得突出，陪衬者应符合证人的描述。<bookmark mark='d'/>在任何反馈之前，用证人自己的话记录第一次的信心陈述。<bookmark mark='e'/>以及只做一次列队辨认。一个证人如果两次看到同一个嫌疑人，就已经见过他了，所以第二次检验是被污染的。加里·韦尔斯及其同事2020年的建议列出了这些做法。",
    "What about real line-ups? <bookmark mark='a'/> In the field the truth is usually unknown, ":
        "那么真实的列队辨认呢？<bookmark mark='a'/>在现场，真相通常是未知的，但有一种错误是看得见的：选中陪衬者总是错误。<bookmark mark='b'/>在约翰·威克斯泰德及其同事对休斯敦一家警察局列队辨认的研究中，低信心时选中陪衬者很常见，高信心时则很少。<bookmark mark='c'/>这正是实验室所预测的模式。一次干净的、高信心的首次辨认，通常指认的就是证人看到的那个人。<bookmark mark='d'/>而在平反案件中出错的，大多涉及低信心或未记录的初始信心、有暗示性的程序，或者重复辨认。",
    'Chapter six. False confessions.':
        '第6章。虚假供述。',
    "Why would an innocent person confess? <bookmark mark='a'/> In 1996 Saul Kassin and Katheri":
        "为什么一个无辜的人会供认？<bookmark mark='a'/>1996年，索尔·卡辛和凯瑟琳·基切尔让学生打字，并警告他们按下ALT键会让电脑崩溃。电脑崩溃了，他们被指控。<bookmark mark='b'/>其实没有人按过那个键。当被要求签署供述时，约三分之二的人签了。<bookmark mark='c'/>当一名同谋说她看见他们按了那个键，也就是虚假证据，而且节奏很快时，几乎所有人都签了，有些人还开始相信这是真的。<bookmark mark='d'/>实验室里的供述没有代价。重点在于机制：虚假证据和压力会改变人们说什么，有时还会改变他们记得什么。",
    "How does interrogation produce false confessions? <bookmark mark='a'/> Isolation and time:":
        "审讯是如何制造虚假供述的？<bookmark mark='a'/>隔离与时间：平反案件中的供述都发生在漫长的审讯之后。<bookmark mark='b'/>虚假证据策略：在一些国家，包括美国，就证据撒谎是合法的，它会改变嫌疑人对何为无望的判断。<bookmark mark='c'/>淡化：暗示宽大处理但不作承诺，比如“换了谁都会这么做”。<bookmark mark='d'/>年轻人和智力障碍者更常作出虚假供述。<bookmark mark='e'/>然后是陪审团：对陪审员来说，一份供述的分量几乎超过其他任何证据，即使他们被告知供述是被迫的。",
    "What's the alternative? <bookmark mark='a'/> After false confessions in the nineteen seven":
        "替代方案是什么？<bookmark mark='a'/>在20世纪70年代和80年代出现虚假供述之后，英格兰和威尔士的警方在20世纪90年代初采用了PEACE模式，并对询问进行录像录音。<bookmark mark='b'/>PEACE代表准备与计划、接触与解释、陈述、结束和评估。目的是获取信息，而不是获得供述。<bookmark mark='c'/>2014年，克里斯蒂安·迈斯纳及其同事回顾了相关实验：与指控式方法相比，信息收集式询问保留了真实供述，减少了虚假供述。<bookmark mark='d'/>完整的录音录像能让法庭看到对嫌疑人说了什么，而不只是嫌疑人说了什么。",
    'Chapter seven. Detecting lies.':
        '第7章。识别谎言。',
    "Can anyone tell when someone is lying? <bookmark mark='a'/> In 2006 Charles Bond and Bella":
        "有人能分辨出别人什么时候在说谎吗？<bookmark mark='a'/>2006年，查尔斯·邦德和贝拉·德保罗汇总了两百零六项研究，涉及约两万四千名判断者。他们的正确率为百分之五十四，而随机水平是百分之五十。<bookmark mark='b'/>人们判断真话比判断谎言更准：一种真实偏差，也就是第12部分的标准偏向相信。<bookmark mark='c'/>警察和其他专业人员也好不了多少，而且他们更有信心。<bookmark mark='d'/>人们使用的线索，回避目光和坐立不安，与说谎几乎没有关系。信号很弱，所以任何标准都无济于事。",
    "And machines? <bookmark mark='a'/> The polygraph records arousal: breathing, sweating and ":
        "那么机器呢？<bookmark mark='a'/>测谎仪记录的是唤醒：呼吸、出汗和心率。但唤醒不等于欺骗。<bookmark mark='b'/>2003年，美国国家研究委员会的综述发现，在针对具体事件的测试中，它优于随机，但远非完美，而用它来从许多人中筛查少数间谍则是不可靠的。<bookmark mark='c'/>筛查问题就是第51部分的警报：在基础比率很低时，大多数警报都是虚警。<bookmark mark='d'/>脑成像测谎，也就是第8部分的那一条，在实验室之外并没有做得更好。最有前景的方法问的是嫌疑人知道什么，而不是他们是否紧张。",
    'Chapter eight. Experts are people.':
        '第8章。专家也是人。',
    "Does an expert see what the context leads them to see? <bookmark mark='a'/> In 2004 the FB":
        "专家看到的，是情境引导他们看到的东西吗？<bookmark mark='a'/>2004年，联邦调查局把俄勒冈州的一名律师错误地认定为马德里火车爆炸案中一枚指纹的来源，三名检验员都表示同意。<bookmark mark='b'/>2006年，伊蒂尔·德罗尔、戴维·查尔顿和艾尔莎·佩伦给五名经验丰富的检验员看了他们自己多年前比对过的指纹，而他们并不知情，同时告诉他们这些就是马德里错误认定案中的指纹。<bookmark mark='c'/>五人中有四人改变了结论。<bookmark mark='d'/>后来的研究发现，这种效应主要出现在难以判断的指纹上。在数据模糊的地方，情境会来填补，就像第14部分的先验那样。",
    "Forensic science has been reviewed. <bookmark mark='a'/> In 2009 the US National Research ":
        "法庭科学已经接受了审查。<bookmark mark='a'/>2009年，美国国家研究委员会得出结论：除了DNA之外，几乎没有哪种法庭科学方法被证明能可靠地识别单一来源。<bookmark mark='b'/>2016年，总统科学顾问委员会要求在黑箱研究中逐个检验员地测量错误率。<bookmark mark='c'/>2017年接受调查的检验员大多同意偏差会影响法庭科学的判断，却大多否认偏差影响了他们自己。这就是偏差盲点，也是为什么仅靠培训是不够的。<bookmark mark='d'/>黑箱研究发现，指纹的假阳性率很低但确实存在，其他一些方法则更高。",
    "The remedy is the one psychology gave medicine: blinding. <bookmark mark='a'/> Itiel Dror ":
        "解决办法是心理学给医学的那一个：盲法。<bookmark mark='a'/>伊蒂尔·德罗尔及其同事提出了线性顺序揭示：先检验并记录犯罪现场的痕迹，然后才看嫌疑人的样本。<bookmark mark='b'/>然后再比较，并记录任何改变主意之处及其理由。这个顺序能防止嫌疑人的指纹引导人们在模糊的痕迹中看到什么。<bookmark mark='c'/>一名案件管理员过滤送到检验员手中的信息：没有供述，没有侦探的直觉，只有比对所需要的东西。<bookmark mark='d'/>还有混入日常案件中的盲法能力测试，测量出法庭应该听到的错误率。",
    'Chapter nine. Children, suggestion and implanted memories.':
        '第9章。儿童、暗示与植入的记忆。',
    "Can questioning create a memory? <bookmark mark='a'/> In the nineteen eighties a series of":
        "询问能制造出一段记忆吗？<bookmark mark='a'/>在20世纪80年代，美国一系列托儿所虐待案的起诉依据的是儿童的陈述，而这些陈述是通过反复的诱导性询问得来的。<bookmark mark='b'/>在斯蒂芬·切奇和玛吉·布鲁克的实验中，被反复问到从未发生过的事件的幼儿，开始报告这些事件，而且带有细节。<bookmark mark='c'/>这些案件中的询问使用的正是实验表明危险的那些技巧：重复、对回答给予奖励，以及“其他孩子已经告诉我们了”。<bookmark mark='d'/>大多数定罪后来都被推翻了。<bookmark mark='e'/>学龄前儿童最容易受暗示。年龄较大的儿童和成年人不那么容易，但也并非免疫。",
    "So how should a child be interviewed? <bookmark mark='a'/> The NICHD protocol, developed b":
        "那么应该如何询问儿童？<bookmark mark='a'/>由迈克尔·兰姆及其同事开发的NICHD规程，先建立融洽关系，练习详细讲述一件中性的事情，然后邀请自由回忆：告诉我发生的所有事情。<bookmark mark='b'/>开放式提示，比如“再多告诉我一些”，比是非题和选择题能引出更长、更准确的陈述。<bookmark mark='c'/>不重复提问，不对回答给予奖励，也不说“其他孩子已经告诉我们了”。托儿所案件中的错误，通过设计被消除了。<bookmark mark='d'/>对受过训练的询问者的现场研究发现，开放式提示能获得更多信息，而以这种方式询问时，幼儿也能给出可靠的陈述。",
    "This led to the memory wars. <bookmark mark='a'/> Part 21 entered the rows: the misinforma":
        "这引发了记忆之战。<bookmark mark='a'/>第21部分记下了这些条目：误导信息效应，以及对整个事件的虚假记忆，比如小时候在商场里走失。<bookmark mark='b'/>在20世纪90年代，寻找被压抑的受虐记忆的治疗导致了一些指控，其中有些后来被撤回。<bookmark mark='c'/>研究并没有表明真实的虐待很少被遗忘，或者常常被错误地记起。它表明的是，暗示性技巧能够制造出详细、自信而虚假的记忆。<bookmark mark='d'/>对法庭来说，一段记忆是如何获得的，与它有多自信同样重要。这又是第四章的教训。",
    'Chapter ten. Juries and judges.':
        '第10章。陪审团与法官。',
    "How are verdicts and sentences reached? <bookmark mark='a'/> Nancy Pennington and Reid Has":
        "裁决和量刑是如何作出的？<bookmark mark='a'/>南希·彭宁顿和里德·黑斯蒂的故事模型：陪审员根据证据构建一个故事，并选择最符合这个故事的裁决。按故事顺序呈现的证据更有说服力。<bookmark mark='b'/>锚定：比尔特·恩格利希、托马斯·穆斯魏勒和弗里茨·施特拉克发现，经验丰富的法官的量刑会向他们自己掷出的骰子点数靠拢。这是第26部分的内容。<bookmark mark='c'/>评议：群体会纠正一些个人错误，也会放大另一些，就像第34部分的群体极化。<bookmark mark='d'/>而被告知要忽略某项证据的陪审员，常常做不到。",
    "Then there are the hungry judges. <bookmark mark='a'/> In 2011 Shai Danziger, Jonathan Lev":
        "然后是饥饿的法官。<bookmark mark='a'/>2011年，沙伊·丹齐格、乔纳森·列瓦夫和利奥拉·阿夫奈姆-佩索报告说，以色列假释委员会在用餐休息后批准约百分之六十五的申请，在下一次休息前降到接近零。<bookmark mark='b'/>被解读为精神疲劳或饥饿后，它成了心理学中被引用最多的发现之一。<bookmark mark='c'/>但凯伦·魏因沙尔-马格尔和约翰·沙帕德指出，案件的顺序不是随机的。没有律师的囚犯通常会被拒绝，而他们总是在每一轮审理的最后。<bookmark mark='d'/>安德烈亚斯·格洛克纳的模拟表明，委员会在预计会很长的案件之前结束一轮审理的做法，本身就能产生这种模式的大部分。<bookmark mark='e'/>账本记作存在争议。数据中的下降是真实的，其原因尚无定论。",
    'Chapter eleven. Risk assessment.':
        '第11章。风险评估。',
    "Can a formula predict who'll reoffend, and fairly? <bookmark mark='a'/> Part 39's Meehl fo":
        "一个公式能预测谁会再犯吗，能公平吗？<bookmark mark='a'/>第39部分的米尔发现，把少数因素组合起来的公式，通常至少和临床判断预测得一样好。<bookmark mark='b'/>用于保释、量刑和假释的风险工具，会对年龄、犯罪史和其他因素打分。它们的准确性中等，ROC曲线下面积约为零点七。<bookmark mark='c'/>2018年，朱莉娅·德雷塞尔和哈尼·法里德发现，未经训练的网民预测再犯的准确率与一款商业工具相当，约为百分之六十五。<bookmark mark='d'/>所以问题不在于机器对人，而在于工具会犯什么错误，以及谁来承担这些错误。",
    "Here's why fairness is hard. <bookmark mark='a'/> Take one risk score, calibrated in both ":
        "这就是公平之所以困难的原因。<bookmark mark='a'/>设想一个风险分数，在两组中都经过校准，因此相同的分数意味着相同的再犯概率。基础比率分别为百分之三十和百分之五十，工具会标记风险超过百分之五十的任何人。<bookmark mark='b'/>假阳性率在A组为百分之十，在B组为百分之二十八，而假阴性率则反过来。<bookmark mark='c'/>亚历山德拉·乔尔德乔娃，以及乔恩·克莱因伯格及其同事，在2016年和2017年证明：当基础比率不相等时，没有任何分数能既经过校准、又在两组中错误率相等。<bookmark mark='d'/>ProPublica 2016年的分析和工具的开发者各自都是对的，只是采用了不同的定义。选择哪个定义，是一个关于价值观的决定。《统计学，从零搭建》第63部分详细推导了这一点。",
    'Chapter twelve. Numbers in court.':
        '第12章。法庭上的数字。',
    "Can a standard error decide a life? <bookmark mark='a'/> In 2002 the US Supreme Court rule":
        "一个标准误能决定一条命吗？<bookmark mark='a'/>2002年，美国最高法院裁定不得处决智力障碍者，并把检验标准交给各州制定。<bookmark mark='b'/>佛罗里达州把高于七十的IQ分数视为决定性的，所以一个得了七十一分的人无法证明自己有智力障碍。<bookmark mark='c'/>第3部分的标准误给出了不同的答案。信度为零点九七时，标准误约为二点五分，七十一分的百分之九十五区间是从六十六到七十六。<bookmark mark='d'/>2014年，最高法院裁定，当分数接近界线时，州政府必须考虑标准误和其他证据。心理测量学成了宪法。",
    "There's a second number in these cases. <bookmark mark='a'/> Part 32's Flynn effect: score":
        "这些案件中还有第二个数字。<bookmark mark='a'/>第32部分的弗林效应：在一个测验的常模制定之后，分数会逐年上升，在20世纪的许多测验中约为每年三分之一分。<bookmark mark='b'/>所以一个人用旧常模测出的分数，会比用新常模高。在一个十五年前制定常模的测验上得七十二分，按现行常模大约是六十七点五分。<bookmark mark='c'/>法院在是否调整的问题上意见分歧。算术很简单。一个平均趋势是否适用于一个人，就不简单了，这是第47部分的问题。<bookmark mark='d'/>普遍的教训是：法庭上的分数是一个估计值，带有误差和日期，而不是关于一个人的事实。",
    'Chapter thirteen. The Ledger.':
        '第13章。账本。',
    'Six new rows. The first: sequential line-ups separate guilty from innocent suspects better':
        "六个新条目。第一条：顺序列队比同时列队更能区分有罪和无辜的嫌疑人。<bookmark mark='a'/>原始研究：林赛与韦尔斯，1985年。<bookmark mark='b'/>记录：ROC分析、一项现场测试，以及放弃了这一偏好的2020年建议。<bookmark mark='c'/>这个比值奖励的是谨慎，而不是区分能力。<bookmark mark='d'/>失败。",
    'The second: under fair, double-blind procedures, an initial high-confidence identification':
        "第二条：在公平、双盲的程序下，高信心的初次辨认通常是准确的。<bookmark mark='a'/>原始研究：尤斯林、奥尔松与温曼的校准分析，1996年。<bookmark mark='b'/>记录：说明为什么只有第一次陈述才算数的反馈研究、一家警察局的列队辨认，以及威克斯泰德和韦尔斯的综述。<bookmark mark='c'/>审判时的信心所含的信息要少得多。<bookmark mark='d'/>已重复。",
    'The third: innocent people accused of a minor offence in a laboratory often sign a confess':
        "第三条：在实验室中被指控犯了轻微过错的无辜者，常常会签署供述。<bookmark mark='a'/>原始研究：卡辛与基切尔，1996年。<bookmark mark='b'/>记录：一个包含有罪和无辜参与者的第二种范式，以及一篇科学综述。<bookmark mark='c'/>其机制与有记录的虚假供述中发现的机制相同。<bookmark mark='d'/>已重复。",
    "The fourth: people judging lies are only slightly better than chance. <bookmark mark='a'/>":
        "第四条：人们判断谎言只比随机略好。<bookmark mark='a'/>原始研究：邦德与德保罗的元分析，2006年。<bookmark mark='b'/>记录：判断者之间几乎没有可靠的差异，原因是线索很弱。<bookmark mark='c'/>信号很弱。<bookmark mark='d'/>已重复。",
    "The fifth: forensic examiners' conclusions can be changed by irrelevant context. <bookmark":
        "第五条：法庭科学检验员的结论可能被无关的情境改变。<bookmark mark='a'/>原始研究：德罗尔、查尔顿与佩伦，2006年。<bookmark mark='b'/>记录：专家与自己早先的判断不一致，以及得知供述后对笔迹作出不同判断。<bookmark mark='c'/>对模糊证据的影响最强。<bookmark mark='d'/>已重复。",
    "And the sixth: judges grant parole far more often after a food break. <bookmark mark='a'/>":
        "第六条：法官在用餐休息后批准假释的频率要高得多。<bookmark mark='a'/>原始研究：丹齐格、列瓦夫与阿夫奈姆-佩索，2011年。<bookmark mark='b'/>记录：案件的顺序，以及不需要疲劳也能产生这种模式的模拟。<bookmark mark='c'/>下降是真实的；其原因尚无定论。<bookmark mark='d'/>存在争议。",
    "What the six have in common. <bookmark mark='a'/> The reliable findings are about procedur":
        "这六条有什么共同点。<bookmark mark='a'/>可靠的发现都关乎程序：一次列队辨认、一次审讯或一次检验对证据做了什么。<bookmark mark='b'/>失败来自用单一数字衡量一种程序，或者脱离设计去解读一种模式。<bookmark mark='c'/>法律采纳了这些研究，然后又采纳了对它们的修正。<bookmark mark='d'/>所以这就是这一部分问题的答案。法庭对一段记忆、一份供述或一位专家的信任，应当与产生它的程序所值得的信任相称。",
    'Chapter fourteen. In practice: weighing an identification.':
        '第14章。实践中：权衡一次辨认。',
    "Where is this a job? <bookmark mark='a'/> In police procedure: line-up protocols, intervie":
        "这在哪里是一份工作？<bookmark mark='a'/>在警务程序中：列队辨认规程、询问培训和录音录像。<bookmark mark='b'/>在专家证词中：心理学家向法庭解释关于记忆、供述和风险的研究。<bookmark mark='c'/>在法庭科学实验室中：盲法、能力测试和错误率研究。<bookmark mark='d'/>还有在司法评估中：说明了误差的测验所支持的能力、风险和行为能力评估。",
    "Here's a worked case: the weight of one identification. <bookmark mark='a'/> Bayes's rule,":
        "这里是一个实例：一次辨认的分量。<bookmark mark='a'/>贝叶斯法则，来自第14部分：有罪的后验几率等于先验几率乘以证据的似然比。<bookmark mark='b'/>以在Psyche的中等标准下对嫌疑人的一次辨认为例。正确辨认率约为零点五六，指认无辜嫌疑人的比率约为零点一一，所以似然比约为五。<bookmark mark='c'/>一比十的先验几率变成大约一比二。这是重要的证据，但不是证明。<bookmark mark='d'/>如果初始信心很高，这个比值要大得多。如果信心低、列队有偏，或者重复看过，这个比值就小得多。<bookmark mark='e'/>专家的工作是把程序的错误率和最初记录的信心告诉法庭，而不是给出一个裁决。",
    "The same pick means different things in different investigations. <bookmark mark='a'/> The":
        "同样的指认，在不同的侦查中意味着不同的东西。<bookmark mark='a'/>横轴是列队辨认之前对嫌疑人的证据有多强。那是侦查，而不是证人。<bookmark mark='b'/>对于中等标准的证人，一个原本有百分之五十可能是罪犯的嫌疑人，变成了百分之八十四。一个原本只有百分之十可能的人，只变成了百分之三十七。<bookmark mark='c'/>围绕一个证据薄弱的嫌疑人组织的列队辨认，会把一位好证人变成薄弱的证据。辨认的大部分意义，来自它之前的警方工作。<bookmark mark='d'/>一位严格的证人，即在第一次辨认时就有高信心的证人，能把同样的先验推得更远。所以要立即用证人自己的话记录下那份信心。",
    'Chapter fifteen. Frontier: machines, interviews and tools.':
        '第15章。前沿：机器、询问与工具。',
    "What will change in the courtroom? <bookmark mark='a'/> Machine face recognition is far be":
        "法庭上会发生什么变化？<bookmark mark='a'/>机器人脸识别在图像质量好时远胜于人，在质量差时则不如人，而且不同群体的错误率不同。一次匹配是一条线索，而不是一次辨认。<bookmark mark='b'/>在一些人脸比对研究中，检验员和算法结合起来比任何一方单独都做得更好。<bookmark mark='c'/>认知询问和PEACE这样的询问方法能获得更多正确细节，而不增加错误。<bookmark mark='d'/>而风险工具正在受到要求效度验证和偏差审计的法律约束，就像招聘工具一样。",
    "And the open problems. <bookmark mark='a'/> Field ground truth: how accurate are real iden":
        "还有那些悬而未决的问题。<bookmark mark='a'/>现场的基本真相：真实的辨认有多准确？平反案件是一个有偏的样本。<bookmark mark='b'/>数月之间的记忆：一年的反复讲述会对证人的陈述产生什么影响。<bookmark mark='c'/>陪审团与统计：如何呈现似然比，才能让陪审员正确地使用它。<bookmark mark='d'/>还有哪一种公平：当基础比率不同时，风险工具对每个群体负有什么责任。",
    "First, your four numbers. <bookmark mark='a'/> When the culprit was absent, sixty-four per":
        "先看你的四个数字。<bookmark mark='a'/>当罪犯不在场时，Psyche的证人中仍有百分之六十四指认了某个人。谎言判断的正确率为百分之五十四。被诬告的学生中约三分之二签署了供述。而一个来自信度为零点九七的测验的七十一分IQ，其区间是从六十六到七十六。<bookmark mark='b'/>证据的好坏，取决于产生它的程序。",
    "Part fifty-six in twelve lines. <bookmark mark='a'/> Most early DNA exonerations involved ":
        "第五十六部分，十二句话。<bookmark mark='a'/>早期的DNA平反案件大多涉及错误的证人。列队辨认是信号检测，所以要用ROC来评判。顺序列队移动的是标准。初次的高信心具有诊断性，后来的信心则不然。以双盲方式进行列队辨认，使用公平的陪衬者，并记录信心。虚假证据会产生虚假供述。谎言识别的正确率是百分之五十四。情境会在模糊证据上扭曲专家的判断。暗示能制造出详细的虚假记忆。饥饿的法官可能只是案件的顺序。校准和错误率相等不能同时成立。法庭上的分数带有误差和日期。",
    "Where this comes back. <bookmark mark='a'/> Assessment and care in health are Part 57. Pre":
        "这些内容会在哪里再出现。<bookmark mark='a'/>健康领域的评估与照护是第57部分。精神病学中的预测与风险是第59部分。机器中的公平是第60部分。而塑造科学本身的激励是第61部分。",
    "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One weighs":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道用贝叶斯法则权衡一次辨认。一道求公平的列队辨认多常抓住一个无辜的嫌疑人。一道解释为什么更好的比值可能意味着更差的曲线。一道计算谎言识别的准确率。一道给一个IQ分数加上区间。一道解释不可能性结果。最后带星号的一道，请你为一支警队编写一份列队辨认规程。如果想试一试，就在这里暂停。",
    "The books and papers behind this part are listed here and in the README. Garrett's book te":
        '这一部分所依据的书籍和论文列在这里，也列在README中。加勒特的书讲述了这些平反案件；威克斯泰德和韦尔斯的综述是关于信心的现代论述；而2020年的建议就是程序本身。',
    "Six parts of Act Twelve are done. <bookmark mark='a'/> This one weighed memories, confessi":
        "第十二幕的六部分已经完成。<bookmark mark='a'/>这一部分用产生记忆、供述和专家意见的程序来衡量它们。<bookmark mark='b'/>这一幕的最后一部分走向健康与照护。心理学如何才能惠及每一个需要帮助的人？第57部分：健康与照护。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
