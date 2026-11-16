"""Chinese narration for psych39: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第39部分：什么是障碍？'

CHAPTERS = {
    'Hook': '1973年：在疯狂之地保持清醒',
    'Predict': '1. 关于你：一次阳性筛查，和四个数字',
    'History': '2. 疯狂简史',
    'Define': '3. 什么使它成为一种障碍？',
    'Kappa': '4. 两位临床医生，一位病人',
    'Valid': '5. 可靠不等于有效',
    'Dimensions': '6. 类别还是维度？',
    'Structure': '7. 共病是常态',
    'Networks': '8. 相互引起的症状',
    'Epi': '9. 有多常见？',
    'Meehl': '10. 临床预测与统计预测',
    'Culture': '11. 文化、污名与痛苦的表达方式',
    'Ledger': '12. 账本',
    'Practice': '13. 实践：诊断、筛查与风险工具',
    'Frontier': '14. 前沿：网络、个人与生物学',
    'Outro': '回顾、习题与前路',
}

ZH = {
    'Before we start.':
        "开始之前。这一部分和接下来的三部分都是关于痛苦的：焦虑、抑郁、精神病性障碍、成瘾。<bookmark mark='a'/>它们是教育，不是诊断或治疗。如果其中有任何内容触及你自己的生活，请和医生、心理咨询师或你信任的人谈一谈。<bookmark mark='b'/>如果你现在处于危险之中，请拨打当地的紧急电话。在美国，你可以拨打或发短信到988。在英国和爱尔兰，撒玛利亚会的电话是116 123。在其他国家，findahelpline.com 列出了免费、保密的求助热线。",
    'In 1973 the journal Science published a study that shook psychiatry.':
        "1973年，《科学》杂志发表了一项震动精神病学界的研究。<bookmark mark='a'/>戴维·罗森汉报告说，八个没有任何精神病史的人分别去精神病院要求住院，声称听到一个声音。那个声音说：“空的”、“空洞的”、“砰”。<bookmark mark='b'/>一旦住院，他们就不再假装，表现得完全正常。<bookmark mark='c'/>据论文所说，没有一名工作人员识破他们，大多数人出院时的诊断是“精神分裂症，缓解期”。<bookmark mark='d'/>结论是：精神病学诊断无法区分清醒的人和疯狂的人。",
    'It changed the field.':
        "它改变了这个领域。<bookmark mark='a'/>1980年，诊断手册第三版，DSM-III，用明确的标准取代了宽泛的描述，并检验临床医生之间是否一致。<bookmark mark='b'/>几十年后，记者苏珊娜·卡哈兰去寻找那八个人。除了罗森汉本人，她只能确认另外两个。<bookmark mark='c'/>其中一个在医院里有过不错的经历，却被排除在论文之外。罗森汉笔记中的细节，也与他发表的内容对不上。<bookmark mark='d'/>这项研究的数据如今受到严重怀疑。但它指出的问题，诊断不可靠，是真实存在的，而这一部分就要测量它。",
    'So this part asks what a disorder is.':
        "所以这一部分要问：什么是障碍。<bookmark mark='a'/>痛苦与疾病之间的界线是怎样划出来的，又是由谁来划的。<bookmark mark='b'/>两位临床医生的意见有多一致，以及为什么一致还不够。<bookmark mark='c'/>障碍是类别还是维度，是一个因素还是多个因素，以及症状怎样把彼此锁定在原地。<bookmark mark='d'/>还有障碍有多常见，一次阳性筛查意味着什么，以及为什么简单的公式能胜过专家。",
    'This is Part 39 of Psychology, Built':
        "这是《心理学，从零搭建》的第39部分：什么是障碍？这是第十幕“当心灵受苦”的第一部分。<bookmark mark='a'/>我们会简要回顾疯狂及其手册的历史。我们会追问什么使一种状态成为障碍。我们会推导科恩的卡帕系数，并看到为什么一个可靠的诊断仍然可能无效。我们会比较类别与维度，认识p因子，并搭建一个症状网络。我们会统计障碍有多常见，并算出一次阳性筛查意味着什么。最后是临床预测与统计预测的较量，以及文化。",
    'Chapter one. On you: a positive screen, and four numbers.':
        '第一章。关于你：一次阳性筛查，和四个数字。',
    "First, a puzzle you've met before, in Part 12.":
        "首先，一个你在第12部分见过的谜题。<bookmark mark='a'/>某种疾病影响百分之一的人。<bookmark mark='b'/>一份筛查问卷能识别出百分之九十的患者。<bookmark mark='c'/>它也会错误地标记百分之九的非患者。<bookmark mark='d'/>某人筛查结果为阳性。他真的患病的概率是多少？现在给出一个数字。",
    'Here it is in natural frequencies.':
        "用自然频数来看。<bookmark mark='a'/>取一万人。一百人患病，九千九百人没有。<bookmark mark='b'/>这一百人中，九十人检测阳性。<bookmark mark='c'/>九千九百人中，百分之九，也就是八百九十一人，同样检测阳性。<bookmark mark='d'/>所以在九百八十一个阳性中，九十人患病：约百分之九。大多数人猜得高得多。像这样数出来，答案一目了然，这也是为什么筛查永远不等于诊断。",
    'Now four numbers to write down before the part answers them.':
        "现在请写下四个数字，本部分随后会给出答案。<bookmark mark='a'/>第一：在一项大型美国调查中，有多大比例的成年人一生中曾在某个时候符合某种精神障碍的标准？<bookmark mark='b'/>第二：两位临床医生为同一批病人做重性抑郁的诊断。他们超出随机水平的一致性，也就是科恩的卡帕系数，在零到一之间是多少？<bookmark mark='c'/>第三：在三千七百名被诊断为抑郁的人中，有多少种不同的症状组合？<bookmark mark='d'/>第四：在比较临床医生与简单公式的研究中，临床医生明显胜出的研究占多大比例？在这里暂停，把它们写下来。",
    'Chapter two. A short history of madness.':
        '第二章。疯狂简史。',
    'Madness is old.':
        "疯狂古已有之，对它的分类却很年轻。<bookmark mark='a'/>大约1800年，道德治疗：巴黎的菲利普·皮内尔和约克的威廉·图克解开了病人的锁链，给他们工作、规律的生活和善意。<bookmark mark='b'/>整个十九世纪，公立精神病院不断增多、人满为患，看管取代了治愈。<bookmark mark='c'/>大约1900年，埃米尔·克雷佩林按照多年间的病程，把重大精神病分为早发性痴呆，后来称为精神分裂症，以及躁狂抑郁症。<bookmark mark='d'/>与此同时，西格蒙德·弗洛伊德把神经症，焦虑和癔症，描述为心灵中的冲突，以谈话作为治疗。<bookmark mark='e'/>1952年，美国第一部诊断手册DSM-I给出了简短的文字描述。<bookmark mark='f'/>1961年，托马斯·萨斯称精神疾病是一个神话，诊断是一种社会控制。<bookmark mark='g'/>1980年，DSM-III用明确的标准回应了批评者：数症状，并检验临床医生是否一致。",
    'Chapter three. What makes it a disorder?':
        '第三章。什么使它成为一种障碍？',
    'What makes something a disorder rather than a hard life?':
        "是什么让某种状态成为障碍，而不只是艰难的生活？有四个候选标准，每一个单独都站不住。<bookmark mark='a'/>统计上的罕见：远离平均值。但天才也罕见，而焦虑很常见。<bookmark mark='b'/>痛苦：这个人在受苦。但悲伤是没有障碍的痛苦，而躁狂可能让人感觉美妙。<bookmark mark='c'/>功能失调：有什么东西没有按应有的方式运作。但“应有”需要一个标准。<bookmark mark='d'/>伤害，对本人或对他人。但什么算伤害，取决于社会的判断。",
    'The most influential definition combines two of them.':
        "最有影响的定义结合了其中两个。<bookmark mark='a'/>1992年，杰尔姆·韦克菲尔德提出，障碍是一种有害的功能失调。<bookmark mark='b'/>功能失调是一个事实判断：某种心理机制没能完成自然选择让它完成的事。<bookmark mark='c'/>有害是一个价值判断，由这个人所在的社会做出。<bookmark mark='d'/>批评者指出，我们很少知道一种心理机制是为了什么而被选择的，所以事实的那一半常常只是猜测。",
    'The definition has been tested on a real case.':
        "这个定义曾在一个真实案例上接受检验。<bookmark mark='a'/>直到1973年，同性恋在美国的手册中被列为一种精神障碍。<bookmark mark='b'/>1973年12月，美国精神医学学会理事会将它删除。它本身并不导致痛苦或功能损害，证据也不支持把它称为障碍。<bookmark mark='c'/>反对者迫使会员进行公投，1974年，投票者中百分之五十八支持这一改变。<bookmark mark='d'/>一个定义得到了应用，一个类别被删除了。而一个科学类别，最终是由投票决定的。",
    'Chapter four. Two clinicians, one patient.':
        '第四章。两位临床医生，一位病人。',
    'How do you measure whether two clinicians agree?':
        "怎样衡量两位临床医生是否一致？<bookmark mark='a'/>取一百名病人。两人在二十个“是”和六十五个“否”上一致：百分之八十五的一致率。<bookmark mark='b'/>但医生A有四分之一的时候说“是”，医生B是百分之三十。按这样的比率随便猜，他们单凭运气就会有百分之六十的时候一致。<bookmark mark='c'/>雅各布·科恩的卡帕系数，取超出随机的一致，再除以可能达到的最大值。零点八五减零点六，除以一减零点六：零点六二五。<bookmark mark='d'/>零是随机水平，一是完全一致。原始一致率会美化结果，对罕见疾病尤其如此：两个人对谁都说“否”，几乎总是一致的。",
    'How reliable are diagnoses now?':
        "如今的诊断有多可靠？<bookmark mark='a'/>为了第五版，达雷尔·里吉尔和同事在美国和加拿大让成对的临床医生独立访谈同一批病人。<bookmark mark='b'/>有些诊断的一致性很好：重度神经认知障碍约为零点七八，孤独症约为零点七。<bookmark mark='c'/>两种最常见的诊断则不然：重性抑郁接近零点三，广泛性焦虑接近零点二。<bookmark mark='d'/>这次试验的设计与以往不同，以往在更容易的条件下报告过更高的卡帕值。尽管如此，两位临床医生常常对一个人是否抑郁意见不一。",
    'f"Why does agreement matter so much?':
        "为什么一致性如此重要？<bookmark mark='a'/>在普赛克中，两千名病人，其中五分之一的严重程度确实超过阈值。两位临床医生各自透过自己的噪声看到严重程度。<bookmark mark='b'/>随着噪声增大，两位医生之间越来越不一致，每个人与真相的一致性也越来越低。当他们之间的卡帕接近零点三时，每个人与真相的卡帕只有{d['validity'][i3]:.2f}。<bookmark mark='c'/>两位临床医生无法取得一致的诊断，也无法与其他任何东西取得良好的一致。信度限制了效度。<bookmark mark='d'/>但反过来不成立。两位临床医生可以在错误的东西上完全一致。",
    'Chapter five. Reliable is not valid.':
        '第五章。可靠不等于有效。',
    'Agreement shows clinicians are measuring the same thing.':
        "一致性表明临床医生在测量同一个东西，却不能表明这个东西是真实的。<bookmark mark='a'/>1970年，伊莱·罗宾斯和塞缪尔·古兹列出了一个诊断应当积累的证据。可辨认的描述。<bookmark mark='b'/>能识别它的实验室检测。<bookmark mark='c'/>与其他障碍之间的界线。<bookmark mark='d'/>随时间相似的病程，也就是克雷佩林的检验。<bookmark mark='e'/>以及在家族中聚集的倾向。半个世纪过去了，大多数诊断满足其中一些，很少有满足全部的。",
    'f"Validity has a second problem':
        "效度还有第二个问题：一个类别里装的是什么。<bookmark mark='a'/>重性抑郁需要在两周内出现九种症状中的五种或更多，其中一种必须是情绪低落或兴趣丧失。<bookmark mark='b'/>数一数符合条件的组合，共有{d['n']}种。<bookmark mark='c'/>两个人可以有同一个诊断，却只有{d['min_overlap']}种症状相同，就像这里的A和B。<bookmark mark='d'/>这是给一个多样化群体贴上的可靠标签，这也是为什么关于抑郁的研究，最终可能是在对非常不同的人取平均。",
    'And in real patients?':
        "那么在真实的病人身上呢？<bookmark mark='a'/>2015年，艾科·弗里德和伦道夫·内斯分析了一项大型试验中三千七百名抑郁门诊病人，每人的十二种症状都记录为有或无。<bookmark mark='b'/>他们发现了一千零三十种不同的症状模式，其中五百零一种只属于一个人。<bookmark mark='c'/>百分之八十四的模式最多只有五个人共有。<bookmark mark='d'/>弗里德的结论是：要研究症状本身，而不只是它们的总和。",
    'Chapter six. Categories or dimensions?':
        '第六章。类别还是维度？',
    'Is a disorder a kind of person, or a degree?':
        "障碍是一种人，还是一种程度？<bookmark mark='a'/>类别主张的是一种类型：两个群体，中间有一个缺口或第二个峰。<bookmark mark='b'/>维度主张的是一种程度：一个连续体，诊断是横跨其上的一条线。<bookmark mark='c'/>高血压是一个带有临床切分点的维度。多出一条染色体则是一种类型。<bookmark mark='d'/>一种障碍属于哪一种，是一个实证问题。分类测量法要问：数据看起来像两个群体的混合，还是一个连续体。",
    'What do the data say?':
        "数据怎么说？<bookmark mark='a'/>2012年，尼克·哈斯拉姆和同事回顾了一百七十七篇文章：三百一十一项分类测量结果，五十多万人。<bookmark mark='b'/>其中百分之三十九被报告为类别型。但在使用更严格的、基于模拟的方法的研究中，只有百分之十六是。综述者估计真实比例接近百分之十四。<bookmark mark='c'/>他们2020年的更新得出结论：人与人之间的绝大多数差异是连续的，精神病理也不例外。<bookmark mark='d'/>所以大多数诊断，是按惯例横跨在连续体上的线。在哪里划线，是一个关于代价的决定，而不是一项发现。",
    'Chapter seven. Comorbidity is the rule.':
        '第七章。共病是常态。',
    'f"Categories have a third problem':
        "类别还有第三个问题：人们很少只符合一个。<bookmark mark='a'/>在调查中，有一种诊断的人常常也符合其他诊断的标准。共病是常态，而不是例外。<bookmark mark='b'/>普赛克用一个总体因素和三个领域，在两万人中构建了九种诊断。在有任何诊断的人中，{spct(d['share_comorbid'])}有两种或更多。<bookmark mark='c'/>每一个相关都是正的：一个正向流形，就像第32部分的智力测验。明亮的方块是各个领域：内化、外化和思维。<bookmark mark='d'/>第一主成分承载了{spct(d['pc1'])}的方差。",
    'In people, the same structure appears.':
        "在真实的人身上，也出现了同样的结构。<bookmark mark='a'/>2014年，阿夫沙洛姆·卡斯皮和同事分析了从十八岁追踪到三十八岁的达尼丁队列，发现一个总体维度比三个分开的领域拟合得更好。他们仿照智力的g，把它称为p。<bookmark mark='b'/>p越高，功能损害越多，家族史越多，童年也越艰难。<bookmark mark='c'/>精神病理层级分类系统HiTOP，从数据而不是委员会出发，搭建了一个从症状到综合征、到谱系、再到p的阶梯；研究领域标准则按照跨越各种障碍的功能来组织研究。<bookmark mark='d'/>第32部分的问题又回来了：一个总体因素，是一个原因，还是对一同出现之物的概括？",
    'Chapter eight. Symptoms that cause each other.':
        '第八章。相互引起的症状。',
    'The deepest alternative to categories':
        "对类别最深刻的替代方案，重新思考了障碍是什么。<bookmark mark='a'/>通常的图景是，一个隐藏的障碍引起了症状，就像病毒引起发烧。<bookmark mark='b'/>网络的图景则说，症状相互引起。睡眠不好带来疲劳。疲劳损害注意力。做事失败使情绪低落。而情绪低落又扰乱睡眠。<bookmark mark='c'/>障碍是整个网络稳定下来的状态，而不是藏在背后的某个东西。<bookmark mark='d'/>丹尼·博尔斯伯姆阐述了这个理论，安热莉克·克拉默和同事则用这种方式，把抑郁建模为一个动力系统。",
    'Psyche builds such a network.':
        "普赛克搭建了这样一个网络。<bookmark mark='a'/>九种症状，每一种开启的概率，都随压力以及开启的邻居数目而上升。然后把压力调高，再调低。<bookmark mark='b'/>连接强时，随着压力上升，症状会突然一起开启。压力下降时，它们仍然保持开启，直到压力低得多时才关闭。<bookmark mark='c'/>这就是滞后。在同样的压力水平下，网络可以是健康的，也可以是患病的，取决于它从哪里来。<bookmark mark='d'/>连接弱时，症状随压力平滑地升降。在这个模型中，易感性就是连接的强度。",
    'f"Here\'s an episode in time.':
        "这是一次发作的时间过程。<bookmark mark='a'/>日常压力，然后是一段高压时期，然后又回到日常压力。<bookmark mark='b'/>强连接的网络很快就陷入一次发作，压力结束后需要{d['strong_recover']}步才恢复。弱连接的网络只需要{d['weak_recover']}步。<bookmark mark='c'/>这是一个模型，说明为什么发作可以突然开始、缓慢结束，以及为什么同样的压力会让一个人患病、另一个人安然无恙。<bookmark mark='d'/>它是一个模型，不是一项发现。网络的观点会在第40和第47部分接受数据的检验。",
    'Chapter nine. How common?':
        '第九章。有多常见？',
    'How common are disorders?':
        "障碍有多常见？<bookmark mark='a'/>2005年，罗纳德·凯斯勒和同事报告了美国共病调查的复测研究，这是对美国成年人具有代表性的样本所做的面对面访谈。<bookmark mark='b'/>百分之四十六的人一生中曾在某个时候符合至少一种障碍的标准。<bookmark mark='c'/>所有终生病例中，一半在十四岁之前开始，四分之三在二十四岁之前。焦虑通常始于童年，心境障碍在三十岁左右。<bookmark mark='d'/>终生患病率取决于第六章的阈值，也取决于回忆。追踪人们并反复询问的研究，发现的比例还要更高。",
    'Most people with a disorder are never treated.':
        "大多数有障碍的人从未得到治疗。<bookmark mark='a'/>2004年，罗伯特·科恩和同事汇总了世界各地的研究。百分之五十六的重性抑郁患者，以及百分之七十八的酒精使用障碍患者，没有接受过任何治疗。<bookmark mark='b'/>这个缺口在中低收入国家最大。<bookmark mark='c'/>但这里有一个悖论。2017年，安东尼·约姆和同事考察了澳大利亚、加拿大、英格兰和美国。治疗大幅增加，尤其是抗抑郁药，但焦虑和抑郁的患病率并没有下降。<bookmark mark='d'/>可能的原因：治疗没有到达需要的人，或者在实践中的效果不如在试验中。第42部分会权衡这些证据。",
    'Chapter ten. Clinical against statistical prediction.':
        '第十章。临床预测与统计预测。',
    'If diagnosis is hard, maybe expert judgment can rescue it.':
        "如果诊断很难，也许专家判断能挽救它。<bookmark mark='a'/>1954年，保罗·米尔出版了《临床预测与统计预测》。<bookmark mark='b'/>它比较了组合同一批信息的两种方式，这些信息关于一位病人、一名假释犯或一个学生：专家的判断，或者一个固定的公式。<bookmark mark='c'/>在他能找到的研究中，公式几乎每次都做得一样好或更好。<bookmark mark='d'/>他后来称它为“我那本令人不安的小书”。临床医生并不欢迎它。",
    'The question was asked again and again.':
        "这个问题被一再提出。<bookmark mark='a'/>2000年，威廉·格罗夫和同事对比较临床预测与机械预测健康和行为的研究做了元分析。<bookmark mark='b'/>根据分析方法的不同，公式在三分之一到一半的研究中明显更好。临床医生在百分之六到十六的研究中明显更好。其余的不相上下。<bookmark mark='c'/>这种优势在不同任务、不同类型的判断者和不同经验水平中都成立。而当临床医生拥有访谈资料时，他们的表现相对更差。<bookmark mark='d'/>更多的信息可能让判断变得更糟，当这些信息生动却无关时。",
    'Why do formulas win?':
        "公式为什么会赢？<bookmark mark='a'/>在普赛克中，一个结果取决于五条线索，每种方法看到的都是同样的线索。<bookmark mark='b'/>临床医生知道正确的线索和大致正确的权重，却对每个案例的运用略有不同。<bookmark mark='c'/>1979年，罗宾·道斯证明，即使是等权重，一个“不恰当”的模型，也能胜过这样的判断，因为公式是一致的，而人不是。<bookmark mark='d'/>教训不是临床医生毫无用处，而是他们的判断应该按规则来组合。",
    'Chapter eleven. Culture, stigma and idioms of distress.':
        '第十一章。文化、污名与痛苦的表达方式。',
    "Suffering doesn't speak one language.":
        "痛苦并不只说一种语言。<bookmark mark='a'/>1981年，人类学家马克·尼克特在南印度与哈维克婆罗门女性一起工作，他把受文化塑造的表达痛苦的方式称为“痛苦的表达方式”。<bookmark mark='b'/>2015年，邦妮·凯泽和同事系统回顾了其中一种：“想得太多”，许多国家都有这种说法。<bookmark mark='c'/>它与抑郁和焦虑有重叠，但它既不是它们的翻译，也不是单一的综合征。<bookmark mark='d'/>手册第五版现在列出了痛苦的文化概念，以及一份文化概念化访谈。第38部分关于测量的教训，同样适用于诊断。<bookmark mark='e'/>还有污名：标签本身就可能造成伤害，通过羞耻、失去工作和回避治疗。这就是为什么本系列说“有障碍的人”，而不是把障碍当作这个人本身。",
    'One frame holds the next three parts together.':
        "一个框架把接下来的三部分联系在一起。<bookmark mark='a'/>当一种易感性，也就是素质，遇到足够的压力时，障碍就会出现。<bookmark mark='b'/>同样的事件可以让一个人安然无恙、让另一个人患病，第八章的网络就是其中一种机制。<bookmark mark='c'/>易感性来自基因、来自发展、也来自学习，这些在本系列前面都已经见过。<bookmark mark='d'/>接下来是恐惧与悲伤，然后是精神病性障碍、成瘾与发育，然后是心理治疗是否有效的问题。",
    'Chapter twelve. The Ledger.':
        '第十二章。账本。',
    'Five new rows today.':
        "今天新增五行。第一行：伪装一个症状的健康人被精神病院收治，却从未被识破。<bookmark mark='a'/>最初的研究：罗森汉，1973年。<bookmark mark='b'/>记录：卡哈兰对他的文件所做的调查。<bookmark mark='c'/>从未被重复，数据受到严重怀疑。<bookmark mark='d'/>有争议。",
    'The second: formulas predict health and behaviour':
        "第二行：公式对健康和行为的预测至少和专家判断一样好，而且常常更好。<bookmark mark='a'/>最初的研究：米尔，1954年。<bookmark mark='b'/>记录：道斯的不恰当模型，以及对这些比较的一项元分析。<bookmark mark='c'/>应用心理学中最一致的发现之一。<bookmark mark='d'/>重复成功。",
    'The third: most disorders are continua':
        "第三行：大多数障碍是带有惯例切分点的连续体。<bookmark mark='a'/>最初的研究：哈斯拉姆和同事的综述，2012年。<bookmark mark='b'/>记录：他们2020年的元分析。<bookmark mark='c'/>少数可能是类别；对大多数而言，那条线是一个决定。<bookmark mark='d'/>重复成功。",
    'The fourth: one general factor, p':
        "第四行：一个总体因素p，解释了障碍之间的大部分重叠，并代表一种共同的易感性。<bookmark mark='a'/>最初的研究：卡斯皮和同事，2014年。<bookmark mark='b'/>记录：HiTOP联盟的层级模型。<bookmark mark='c'/>这个模式一再被发现；它意味着什么则有争论。<bookmark mark='d'/>有争议。",
    'And the fifth: a laboratory test can diagnose':
        "第五行：实验室检测可以诊断一种精神障碍，就像地塞米松抑制试验曾被声称可以诊断忧郁型抑郁症。<bookmark mark='a'/>最初的研究：卡罗尔和同事，1981年。<bookmark mark='b'/>记录：一篇关于为什么没有这样的检测进入临床的综述。<bookmark mark='c'/>没有任何实验室检测被用于诊断常见的精神障碍。<bookmark mark='d'/>失败。",
    'The tally.':
        "汇总。<bookmark mark='a'/>成立的：公式胜过临床判断，大多数障碍是维度。<bookmark mark='b'/>失败的：用于诊断的实验室检测，至今如此。<bookmark mark='c'/>有争议的：罗森汉的研究，以及p因子意味着什么。<bookmark mark='d'/>诊断通过一致性变得可靠，却还没有通过解释变得有效。",
    'Chapter thirteen. In practice: diagnosis, screening and risk tools.':
        '第十三章。实践：诊断、筛查与风险工具。',
    'A diagnosis does many jobs':
        "一个诊断承担着许多工作，它们朝着不同的方向拉扯。<bookmark mark='a'/>治疗：一个共同的名称，指向关于什么有帮助的证据。<bookmark mark='b'/>支付：医疗服务和保险公司按编码付费，所以阈值决定了谁能得到覆盖。<bookmark mark='c'/>研究：一种为试验给人分组的方式，带着第五章所说的全部多样性。<bookmark mark='d'/>权利：学校里的支持、工作中的调整、残疾福利。<bookmark mark='e'/>还有身份：有些人觉得一个名称是一种解脱，另一些人觉得它是一种负担。",
    'And a warning that applies to every app and questionnaire.':
        "还有一个适用于每一个应用和每一份问卷的警告。<bookmark mark='a'/>筛查工具的设计是为了抓住大多数病例，所以它们会标记许多并非病例的人，就像第一章里的百分之九。<bookmark mark='b'/>阳性筛查应该引向临床医生的评估，而不是一个标签。<bookmark mark='c'/>实践中的风险工具，从自杀风险量表到暴力风险评估工具，在结果罕见时都有同样的问题。大多数被标记的人并不会出现那个结果。<bookmark mark='d'/>第十章的公式胜过判断，却仍然胜不过基础比率。<bookmark mark='e'/>好的做法：用自然频数说明一个分数意味着什么，并在筛查之前就决定阳性之后要做什么。",
    'Chapter fourteen. Frontier: networks, persons and biology.':
        '第十四章。前沿：网络、个人与生物学。',
    'At the frontier, three questions.':
        "前沿有三个问题。<bookmark mark='a'/>2016年，约斯特·克鲁伊斯和贡特尔·马里斯证明，第八章的网络模型、一个潜变量模型和一个共同原因模型，可以给出完全相同的症状分布。<bookmark mark='b'/>所以单靠拟合数据，无法判定一种障碍是一个原因还是一个系统。那需要干预，也需要时间。<bookmark mark='c'/>第二，个体网络：在一个人身上每天多次追踪症状，以估计这个人自己的网络。第47部分会讨论这一点。<bookmark mark='d'/>第三，一种生物学的分类需要这样的标记：能重复，能预测病程或治疗效果，并且胜过访谈。目前还没有一个能做到。",
    'So, open questions.':
        "那么，有哪些悬而未决的问题。常见的精神障碍中，有没有哪一种是自然类别，还是全都是连续体上的惯例？<bookmark mark='b'/>p因子代表什么：一个原因、一种严重程度，还是一个统计概括？<bookmark mark='c'/>在一个人身上估计出的网络，能否预测这个人的下一次发作？<bookmark mark='d'/>为什么更多的治疗没有降低患病率？<bookmark mark='e'/>又该由谁、依据什么证据，来决定诊断的阈值在哪里？",
    'First, your four numbers.':
        "首先，你的四个数字。<bookmark mark='a'/>曾经符合某种障碍标准的美国成年人比例：百分之四十六。现场试验中重性抑郁的卡帕值：约零点三。三千七百名抑郁者中的症状模式：一千零三十种。临床医生明显胜过公式的研究：百分之六到十六。<bookmark mark='b'/>障碍很常见，诊断并不完美，而类别掩盖了大量的多样性。",
    'Part thirty-nine in eleven lines.':
        "用十一句话概括第三十九部分。<bookmark mark='a'/>罗森汉的研究改变了诊断，而它的数据受到严重怀疑。罕见、痛苦、功能失调和伤害，每一个单独都站不住，有害的功能失调结合了其中两个。卡帕是超出随机的一致性，抑郁的卡帕约为零点三。信度限制效度，却不能创造效度。两百二十七种症状组合构成同一个诊断。大多数障碍是带有惯例切分点的维度。共病是常态，p因子概括了它。症状网络可以突然倾覆、缓慢恢复。近一半的成年人一生中曾符合某种标准，而大多数人没有得到治疗。公式胜过临床判断，而谁也胜不过基础比率。痛苦以文化的方式表达，而标签可能造成伤害。",
    "Kant's wager.":
        "康德的赌注。<bookmark mark='a'/>第一个反对意见，数学无法应用于心灵，遇到了卡帕、基础比率、分类测量法，以及一个带滞后的症状网络。<bookmark mark='b'/>第二个反对意见，心灵无法被实验，遇到了成对临床医生的现场试验，以及数十年来公式与判断的较量。<bookmark mark='c'/>第三个反对意见，关于内省：诊断依赖于人们报告的内容，而两位临床医生听到的并不相同。琥珀色。",
    'Where this comes back.':
        "这些内容会在哪里再次出现。<bookmark mark='a'/>焦虑和抑郁，从条件作用到神经回路，就在下一部分，第40部分。精神病性障碍、成瘾和发育是第41部分。心理治疗是否有效是第42部分。潜变量和网络会在第44和第47部分得到完整的讨论。",
    'Seven problems, with full solutions':
        "七道习题，完整解答在本部分的README里。<bookmark mark='a'/>一道手算卡帕。一道说明卡帕何时为零，以及最大能有多大。一道数症状组合。一道在三种患病率下计算筛查。一道证明信度限制效度。一道求症状网络的两个稳定状态。最后一道带星号，请你设计一项能区分网络与共同原因的研究。如果想试试，就在这里暂停。",
    'The books and papers behind this part':
        '本部分依据的书籍和论文列在这里，也列在README中。卡哈兰的《伟大的伪装者》是对罗森汉的调查；米尔的书很短，至今仍令人不安；肖特的《精神病学史》讲述了从精神病院开始的更长的故事。',
    'Act Ten has begun.':
        "第十幕已经开始。<bookmark mark='a'/>这一部分追问什么是障碍，发现答案在一定程度上是一种惯例。<bookmark mark='b'/>下一部分讨论两种最常见的障碍：普通的恐惧和悲伤怎样变成焦虑和抑郁，从条件作用到神经回路。第40部分：恐惧与悲伤。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
