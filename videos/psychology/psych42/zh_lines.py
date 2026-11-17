"""Chinese narration for psych42: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第42部分：治疗有效吗？'

CHAPTERS = {
    'Hook': '1952年：三分之二的人反正会好',
    'Predict': '1. 关于你：两张图，和四个数字',
    'Trial': '2. 试验，以及对照问题',
    'Meta': '3. 元分析的诞生',
    'Dodo': '4. 渡渡鸟',
    'Therapies': '5. 各种疗法',
    'Meds': '6. 药物、谈话，还是两者都要',
    'Bias': '7. 它到底有多大？',
    'Change': '8. 临床意义',
    'Harm': '9. 有害的治疗',
    'Body': '10. 躯体治疗',
    'Dose': '11. 多少治疗才够？',
    'Ledger': '12. 账本',
    'Practice': '13. 实践：指南、选择与监测',
    'Frontier': '14. 前沿：机制、匹配与迷幻药',
    'Outro': '回顾、习题与前路',
}

ZH = {
    'Before we start. This part is about whether therapy works':
        "开始之前。这一部分讲治疗是否有效，也会谈到创伤和自我伤害。<bookmark mark='a'/>它是教育，不是诊断或治疗。如果其中有任何内容触及你自己的生活，请和医生、心理咨询师或你信任的人谈一谈。<bookmark mark='b'/>如果你现在处于危险之中，请拨打当地的紧急电话。在美国，你可以拨打或发短信到988。在英国和爱尔兰，撒玛利亚会的电话是116 123。在其他国家，findahelpline.com 列出了免费、保密的求助热线。",
    'In 1952 the psychologist Hans Eysenck threw down a challenge.':
        "1952年，心理学家汉斯·艾森克抛出了一个挑战。<bookmark mark='a'/>他收集了当时关于神经症患者，也就是焦虑和抑郁患者的疗效报告。<bookmark mark='b'/>接受折中疗法的人中，大约三分之二在两年内有所好转。而在完全没有心理治疗、只有看护照料的人中，好转的人差不多一样多。<bookmark mark='c'/>他的结论是：这些研究未能表明心理治疗有帮助。<bookmark mark='d'/>这个挑战存在了二十五年。回答它需要恰当的对照组，以及一种把许多研究加总起来的方法。",
    'The answer came in 1977.':
        "答案在1977年到来。<bookmark mark='a'/>玛丽·李·史密斯和吉恩·格拉斯用一种新方法，元分析，汇总了三百七十五项有对照的研究，发现接受治疗的一般来访者，比大约四分之三未接受治疗的人状况更好。<bookmark mark='b'/>接着出现了更难的问题。比什么更好？通过哪种成分？已发表的效应有多少是真的？<bookmark mark='c'/>艾森克更深层的观点依然成立。人们反正会好转，只有对照组才能说明，好转中有多少是治疗带来的。",
    'So this part asks how you would know that talking to someone helped.':
        "所以这一部分要问：你怎么才能知道和某人谈话起了作用。<bookmark mark='a'/>它从试验开始：随机化，以及对照的选择。<bookmark mark='b'/>然后是元分析、渡渡鸟，以及来访者与治疗师之间的联盟。<bookmark mark='c'/>然后是各种疗法、药物，以及已发表的效应与真实效应的对比。<bookmark mark='d'/>最后是临床意义、有害的治疗，以及多少治疗才够。",
    'This is Part 42 of Psychology, Built: does therapy work?':
        "这是《心理学，从零搭建》的第42部分：治疗有效吗？<bookmark mark='a'/>我们会看到为什么每个人都会好转，原因是向均值回归和自然恢复。我们会看到对照条件如何决定效应的大小。我们会亲手做一次元分析，认识渡渡鸟和治疗联盟。我们会掂量各种疗法，以及治疗与药物的对比。我们会测量发表偏倚，并推导临床意义。最后我们以有害的治疗、躯体治疗，以及治疗的剂量作结。",
    'Chapter one. On you: two graphs, and four numbers.':
        "第1章。关于你：两张图，和四个数字。",
    'First, two graphs.':
        "首先，两张图。<bookmark mark='a'/>在图A中，来访者开始治疗时症状得分很高，结束时低了很多。<bookmark mark='b'/>在图B中，是同样的来访者，还有一组等待了同样长时间的人。两组都好转了；接受治疗的来访者好转得更多。<bookmark mark='c'/>哪张图表明治疗起了作用？<bookmark mark='d'/>只有B。即使治疗毫无作用，图A看起来也会一模一样，因为人们是在最糟糕的时候前来求助的，反正会好转。等待组显示了好转了多少。",
    'Now four numbers to write down before the part answers them.':
        "现在写下四个数字，这一部分稍后会给出答案。<bookmark mark='a'/>第一：史密斯和格拉斯汇总了三百七十五项心理治疗研究。平均效应量是多少？<bookmark mark='b'/>第二：在美国监管机构掌握的抗抑郁药试验中，大约一半是阳性的。已发表的试验中，阳性的占多大比例？<bookmark mark='c'/>第三：在将近三百项研究中，来访者与治疗师的联盟和疗效之间的相关是多少？<bookmark mark='d'/>第四：到第几次会谈时，一半的来访者已经好转？在这里暂停，把它们写下来。",
    'Chapter two. The trial, and the control problem.':
        "第2章。试验，以及对照问题。",
    'Why does everyone improve?':
        "为什么每个人都会好转？<bookmark mark='a'/>在普赛克中，每个人的得分都围绕自己的平均值波动，当得分达到二十或更高时，也就是在他们最糟糕的时候，他们前来求助。<bookmark mark='b'/>在完全不治疗的情况下，这一组的平均分下降了五分多。<bookmark mark='c'/>这就是向均值回归。一个因为偏高而被挑中的得分，平均而言，后面会跟着一个较低的得分。而且真实的发作也会自行结束。<bookmark mark='d'/>所以接受治疗的人好转了，并不是治疗有效的证据。只有比较才是。",
    'So compare. But with what?':
        "那就比较吧。但和什么比？<bookmark mark='a'/>普赛克让同一种有效的疗法对比三种对照，每组两千人。<bookmark mark='b'/>与等待名单相比，效应最大，部分原因是等待本身可能有害，它让人们不去别处寻求帮助。<bookmark mark='c'/>与不治疗相比，效应小一些。而与一种可信的安慰剂疗法相比，有一位温暖的倾听者但没有特定技术，效应还不到一半。<bookmark mark='d'/>来访者无法对谈话治疗保持盲态，研究者又常常偏爱自己的疗法。效应是比较的属性，而不只是疗法本身的属性。",
    'One more bias.':
        "还有一种偏倚。<bookmark mark='a'/>普赛克进行六十项试验，比较两种同样好的疗法。每项试验都由一个忠于其中一种疗法的团队来做，而这份忠诚会给自己一方的结果加上一点点，通过更好的培训、更多的热情，或者更宽厚的分析。<bookmark mark='b'/>把所有试验汇总起来，优势几乎正好是零，也就是真相。<bookmark mark='c'/>但一方的拥护者所做的试验发现自己的疗法领先，另一方的拥护者也是如此。<bookmark mark='d'/>在真实的元分析中，研究者的忠诚同样能预测疗法比较的结果。",
    'Chapter three. Meta-analysis is born.':
        "第3章。元分析的诞生。",
    'To answer Eysenck, the studies had to be put on one scale.':
        "要回答艾森克，就必须把各项研究放到同一个尺度上。<bookmark mark='a'/>1976年，吉恩·格拉斯把这种方法命名为元分析，也就是对分析的分析。<bookmark mark='b'/>每个结果，无论用什么量表，都变成一个标准化差异：两组之间的差距，以离散程度为单位。<bookmark mark='c'/>史密斯和格拉斯把它应用于三百七十五项有对照的研究。平均效应是零点六八。接受治疗的一般来访者，最终比四分之三未接受治疗的人状况更好。<bookmark mark='d'/>艾森克称之为“超级愚蠢”：好研究和坏研究混在一起，把苹果和橘子相比。对此的回答，将是按照研究的质量和规模来加权。",
    "Here's a meta-analysis by hand.":
        "这是一次亲手做的元分析。<bookmark mark='a'/>十二项模拟试验，每一项画成一个按其权重确定大小的方块，带着它的百分之九十五区间。小试验的区间很宽。<bookmark mark='b'/>德西蒙尼安和莱尔德的随机效应模型允许每项试验有自己的真实效应，以标准差tau散布开来。每项试验的权重是一除以它的方差加上tau的平方。<bookmark mark='c'/>汇总的效应，也就是那个绿色菱形，落在接近真实值二分之一的地方。<bookmark mark='d'/>其中的数学，以及如何解读异质性，是第50部分的内容。",
    'Chapter four. The dodo bird.':
        "第4章。渡渡鸟。",
    'Which therapy works best?':
        "哪种疗法最好？<bookmark mark='a'/>在《爱丽丝梦游仙境》里，渡渡鸟裁判一场赛跑，宣布人人都赢了，人人都该得奖。<bookmark mark='b'/>1936年，索尔·罗森茨威格提出，不同的疗法可能通过它们共有的因素而同样有效。<bookmark mark='c'/>1975年，莱斯特·卢博斯基和同事们综述了这些比较，发现差异很少，于是借用了渡渡鸟的判决。<bookmark mark='d'/>1997年，布鲁斯·万波尔德和同事们对真正意在帮助人的疗法之间的直接比较作了元分析，发现平均差异大约为零。<bookmark mark='e'/>账本把它标为有争议：平均而言近乎相等，但有例外。",
    'The boldest answer to what therapies share came from a therapist who thought it was the whole of therapy.':
        "关于各种疗法共有什么，最大胆的回答来自一位治疗师，他认为这就是治疗的全部。<bookmark mark='a'/>卡尔·罗杰斯，第1部分里“第三势力”的人本主义心理学家，"
        "把他的方法称为来访者中心：主导工作的是来访者，而不是治疗师。他也是最早把治疗会谈录下来以便研究的人之一。"
        "<bookmark mark='b'/>1957年，他提出了治疗师身上的三个条件：共情，即像来访者那样理解来访者的世界；无条件积极关注，即不取决于来访者说什么、做什么的温暖；"
        "以及一致性，即真诚而不是扮演一个角色。他主张，这些是改变的必要且充分条件。<bookmark mark='c'/>六十年后，罗伯特·埃利奥特领衔的元分析发现，"
        "治疗师的共情与疗效的相关约为零点二八。<bookmark mark='d'/>积极关注和真诚显示出较小的正相关。<bookmark mark='e'/>“充分”就是另一回事了："
        "正如接下来几屏所示，对某些障碍来说，特定的治疗会在任何良好关系所能给予的之上再添一些。后来的研究者把罗杰斯的三个条件扩展成了一个概念。",
    'What could the shared factors be?':
        "共同因素可能是什么？<bookmark mark='a'/>一位温暖而可信的治疗师，一个共同认可的对问题的解释，希望，以及对目标和任务的一致看法：合在一起，就是工作联盟。<bookmark mark='b'/>2018年，克里斯托夫·弗吕基格和同事们汇总了二百九十五项研究。联盟与疗效的相关大约是零点二八。<bookmark mark='c'/>这并不大。它解释了疗效变异的大约百分之八。<bookmark mark='d'/>而且方向存在争论。也许是早期的好转建立了联盟，而不是反过来。",
    "But the dodo isn't always right.":
        "但渡渡鸟并不总是对的。<bookmark mark='a'/>对于有些问题，特定的技术显然很重要：暴露，用于恐惧症、惊恐和强迫障碍，正如第40部分所示。<bookmark mark='b'/>2010年，戴维·托林发现，对于焦虑和抑郁，认知行为治疗比其他疗法略好一点。<bookmark mark='c'/>争论之所以继续，是因为双方都部分正确。共同因素承担了效应的很大一部分，而在机制已知的地方，特定因素会再增加一些。<bookmark mark='d'/>最好的检验是拆解研究：去掉一种成分，看看失去了什么。",
    'Chapter five. The therapies.':
        "第5章。各种疗法。",
    'The therapies come in four families.':
        "疗法分为四个家族。<bookmark mark='a'/>行为疗法改变人们所做的事：暴露、激活、强化，来自第16和第40部分。<bookmark mark='b'/>阿伦·贝克的认知治疗，让人们觉察、检验并修正那些让痛苦持续的想法。<bookmark mark='c'/>第三浪潮，接纳与承诺疗法和正念认知疗法，改变的是一个人与自己想法的关系，而不是想法的内容。<bookmark mark='d'/>心理动力学治疗处理的是过去在人际关系中反复出现的模式，包括与治疗师的关系。它的试验较少，其中一些是阳性的。<bookmark mark='e'/>大多数试验检验的是认知行为治疗，所以它的证据最多。证据更多，并不等于效应更大。",
    'One therapy was built for a problem other therapies struggled with.':
        "有一种疗法是为其他疗法难以应对的问题而建立的。<bookmark mark='a'/>1991年，玛莎·莱恩汉描述了辩证行为治疗，用于患有边缘型人格障碍并反复自我伤害的女性。它把接纳与改变结合起来，加上技能小组，以及会谈之间的指导。<bookmark mark='b'/>与一年的常规治疗相比，它带来了更少、更轻的自我伤害行为，以及更少的住院天数。<bookmark mark='c'/>2006年，与经验丰富的社区治疗师的治疗相比，自杀尝试的比率大约减半。<bookmark mark='d'/>后来的元分析发现效应较小，账本把它标为得到重复。",
    'Chapter six. Pills, talk, or both.':
        "第6章。药物、谈话，还是两者都要。",
    'How does therapy compare with medication?':
        "心理治疗与药物相比如何？<bookmark mark='a'/>对于抑郁，在直接比较两者的试验中，认知治疗和抗抑郁药在短期内效果差不多。<bookmark mark='b'/>两者结合比单用任何一种都好一些。<bookmark mark='c'/>人与人不同。有些人偏好其中一种；有些人对一种有反应而对另一种没有；而偏好本身也会影响谁能坚持治疗。<bookmark mark='d'/>选择哪一种是一个共同的决定，而不是一场比赛。",
    'The difference shows when treatment stops.':
        "差别在治疗停止时显现出来。<bookmark mark='a'/>2005年，史蒂文·霍伦和同事们对那些对认知治疗或抗抑郁药有反应的人追踪了一年。<bookmark mark='b'/>心理治疗结束后，大约百分之三十的人复发。药物换成安慰剂后，大约四分之三复发。继续服药的，不到一半复发。<bookmark mark='c'/>心理治疗的效果似乎比治疗本身更持久，仿佛学会了一项技能。药物的效果只在服用期间持续。<bookmark mark='d'/>这是一项试验，人数不多，而后来的研究大体上都同意，心理治疗能降低复发。",
    'Chapter seven. How big is it really?':
        "第7章。它到底有多大？",
    'How big is the effect really?':
        "效应到底有多大？药物试验最清楚地显示了这个问题。<bookmark mark='a'/>2008年，埃里克·特纳和同事们把十二种抗抑郁药在美国监管机构登记的七十四项试验，与已发表的内容作了比较。<bookmark mark='b'/>按照监管机构自己的判读，大约一半是阳性的。在期刊上，百分之九十四看起来是阳性的。<bookmark mark='c'/>阴性试验没有发表，或者被写得像是阳性的，表面上的效应扩大了大约三分之一。<bookmark mark='d'/>这是第4部分的文件抽屉，发生在一个产业里。同样的问题也适用于心理治疗。",
    'Psyche shows what a filter does.':
        "普赛克展示了过滤会造成什么。<bookmark mark='a'/>四百项试验，检验一种真实效应为零点三的疗法，有的小有的大。<bookmark mark='b'/>显著的被发表，其余的发表五分之一。<bookmark mark='c'/>对已发表试验的随机效应元分析，发现效应接近零点四三。对所有试验的分析，则接近真相。<bookmark mark='d'/>缺失的试验是那些小而运气不好的试验，于是在漏斗图上留下一个缺口。第50部分会建立能看到它的工具。",
    'And for psychotherapy?':
        "那么心理治疗呢？<bookmark mark='a'/>2015年，埃伦·德里森和同事们追踪了由美国国立卫生研究院资助的抑郁心理治疗试验。大约四分之一从未发表，把它们加进来后，效应缩小了。<bookmark mark='b'/>2019年，皮姆·奎珀斯和同事们在论文标题中问道，艾森克最终是不是对的。所有成人抑郁心理治疗试验的平均效应接近零点七。限定在低偏倚风险、不用等待名单对照、并校正了发表偏倚的试验后，效应要小得多。<bookmark mark='c'/>他们对自己问题的回答是：不。心理治疗有效。但效应比文献所显示的要小。<bookmark mark='d'/>账本：心理治疗对比不治疗，得到重复。已发表的效应大小，得到重复，但更小。",
    'Chapter eight. Clinical significance.':
        "第8章。临床意义。",
    "A group's average says little about one person.":
        "一个群体的平均值，对一个人几乎说明不了什么。<bookmark mark='a'/>1991年，尼尔·雅各布森和葆拉·特鲁阿克斯为每位来访者提出了两个问题。<bookmark mark='b'/>第一，变化是否大于测量误差？这是第3部分的测量标准误，应用于两个得分之差。用它去除变化，如果比值超过一点九六，就称为可靠的变化。<bookmark mark='c'/>对于一个标准差为七、信度为零点八五的量表，变化必须超过大约七点五分。<bookmark mark='d'/>第二，这个人最终是更接近健康者还是患病者？分界点位于两个分布之间，按各自的离散程度加权。这里大约是十六点五。",
    'Here are four clients.':
        "这里有四位来访者。<bookmark mark='a'/>第一位从三十分降到十四分：可靠的变化，而且越过了分界点。康复了。<bookmark mark='b'/>第二位，从三十分到二十五分：没有可靠的变化。<bookmark mark='c'/>第三位，从二十二分到十五分：越过了分界点，但变化小于测量误差。<bookmark mark='d'/>第四位，从三十四分到二十分：可靠的变化，但仍在患病的一侧。好转了，但没有康复。<bookmark mark='e'/>用这两条规则进行疗效监测，能让临床工作者和来访者一次会谈接一次会谈地看到，谁在正轨上。",
    "Now apply both rules to everyone in chapter two's trial.":
        "现在把这两条规则应用到第2章试验中的每一个人身上。<bookmark mark='a'/>普赛克把每组两千人分为康复、好转、未变和恶化。<bookmark mark='b'/>在完全不治疗的情况下，大约三分之一的人算作康复。向均值回归也会愚弄针对个人的规则。<bookmark mark='c'/>安慰剂疗法组，不到一半；有效疗法组，超过一半。<bookmark mark='d'/>所以一家诊所的康复率本身说明不了多少。能显示疗法贡献的，仍然是与对照组的比较。",
    'Could a clinic see the harm for itself?':
        "一家诊所自己能看到伤害吗？<bookmark mark='a'/>普赛克设定一种疗法，让人们比完全不治疗还差三分。<bookmark mark='b'/>可靠的恶化从大约百分之二上升到大约百分之六：在繁忙的个案负荷中只是寥寥几位来访者。<bookmark mark='c'/>而它的来访者中，大约六分之一仍然算作康复，因为人们是在最糟糕的时候来的。<bookmark mark='d'/>一位治疗师一次只看一位来访者，看到的大多是好转。伤害只有在与对照组比较时才会显现。",
    'Chapter nine. Treatments that harm.':
        "第9章。有害的治疗。",
    'Therapy can also harm.':
        "治疗也可能造成伤害。<bookmark mark='a'/>心理晤谈：在创伤后不久进行一次会谈，详细地复述创伤经过。试验发现它并不能预防创伤后应激，而在一项对交通事故受害者的三年追踪中，接受过晤谈的人状况更差。<bookmark mark='b'/>“恐吓从善”：把青少年违法者带进监狱，让他们直面囚犯。随机试验发现，之后的违法行为更多，而不是更少。<bookmark mark='c'/>恢复记忆的技术：用催眠和引导想象来恢复受虐待的记忆。正如第21部分所示，它们可能制造出虚假的记忆。<bookmark mark='d'/>还有扭转治疗，试图改变性取向。没有证据表明它有效，却有证据表明它有害，各专业团体都反对它。斯科特·利林费尔德在2007年收集了这样的案例。",
    'Why does harm go unseen?':
        "伤害为什么会被忽视？<bookmark mark='a'/>因为每个人反正都会好转，正如第2章所示，没有对照组时，一种有害的治疗也可能看起来有帮助。<bookmark mark='b'/>在任何疗法中，都有少数来访者变得更糟，通常估计为百分之五到十，而治疗师往往察觉不到。<bookmark mark='c'/>而且试验很少像衡量益处那样仔细地衡量伤害。<bookmark mark='d'/>所以，检验益处的同样工具，对照和监测，也是发现伤害所需要的。",
    'Chapter ten. The body treatments.':
        "第10章。躯体治疗。",
    'The body treatments have a darker history.':
        "躯体治疗有一段更黑暗的历史。<bookmark mark='a'/>1935年，里斯本的神经科医生埃加斯·莫尼斯开始切断精神病患者额叶的连接。<bookmark mark='b'/>1949年，他因此获得了诺贝尔医学奖。<bookmark mark='c'/>在美国，沃尔特·弗里曼推广了一种经眼眶进行的快速做法，有时就在诊室里做，随后进行了数以万计的手术。<bookmark mark='d'/>第41部分的氯丙嗪，以及越来越多的伤害证据，终结了它。<bookmark mark='e'/>它是凭临床医生的印象来评判的，没有对照。一种让人变得迟钝的治疗，被算作让他们平静下来。",
    'Electroconvulsive therapy went the other way.':
        "电休克治疗走了另一条路。<bookmark mark='a'/>1938年，罗马的乌戈·切莱蒂和卢乔·比尼用电流诱发癫痫发作来治疗精神病。<bookmark mark='b'/>早期的电休克治疗不用麻醉，有时被当作惩罚，它的形象再也没有恢复过来。<bookmark mark='c'/>现代的电休克治疗在全身麻醉下进行，并使用肌肉松弛剂。对于严重抑郁，它比只给麻醉药的模拟电休克效果更好。<bookmark mark='d'/>它的代价是记忆丧失，主要集中在治疗期间前后。它是对其他治疗无效的严重疾病的一种选择。",
    'Chapter eleven. How much therapy?':
        "第11章。多少治疗才够？",
    'How much therapy is enough?':
        "多少治疗才够？<bookmark mark='a'/>1986年，肯尼思·霍华德和同事们汇总了许多样本。大约一半的来访者到第八次会谈时已经好转，四分之三到第二十六次时好转。<bookmark mark='b'/>普赛克把它画成一条穿过这两个点的对数正态曲线。每多一次会谈，增加的就更少。<bookmark mark='c'/>后来的研究表明，来访者常常在感觉足够好的时候就停止了，所以这条曲线部分反映的是谁留了下来。<bookmark mark='d'/>还有一些人根本没有反应，这正是监测和改变计划发挥作用的地方。",
    'And most people get none.':
        "而大多数人什么治疗也得不到。<bookmark mark='a'/>第39部分的治疗缺口：大多数患有常见精神障碍的人没有接受任何治疗，很少有人接受到与试验所检验的相符的心理治疗。<bookmark mark='b'/>受过训练的治疗师稀缺而昂贵，等待时间很长。<bookmark mark='c'/>应对的办法包括有指导的自助、团体和数字化项目，以及经过培训、提供简单疗法的非专业咨询员，每一种都在各自的试验中接受检验。<bookmark mark='d'/>这些办法能推广到多大规模、对谁有效，是第57部分的问题。",
    'Chapter twelve. The Ledger.':
        "第12章。账本。",
    'Seven new rows today. The first: people who receive psychotherapy':
        "今天新增七行。第一行：接受心理治疗的人，最终比没有接受任何治疗的人状况更好。<bookmark mark='a'/>原始研究：史密斯和格拉斯的元分析，1977年。<bookmark mark='b'/>记录：几十年后来的试验，在2019年再次汇总。<bookmark mark='c'/>对艾森克的回答，其大小取决于对照。<bookmark mark='d'/>得到重复。",
    'The second: therapy for adult depression has an effect near':
        "第二行：成人抑郁的心理治疗效应接近零点七。<bookmark mark='a'/>原始研究：全部文献，按2019年的汇总。<bookmark mark='b'/>记录：未发表的试验，以及低偏倚风险的试验。<bookmark mark='c'/>是真的，但更小。<bookmark mark='d'/>得到重复，但效应较小。",
    'The third: all bona fide therapies are about equally effective.':
        "第三行：所有真正的疗法效果大致相同。<bookmark mark='a'/>原始研究：卢博斯基和同事们，1975年。<bookmark mark='b'/>记录：一项关于直接比较的元分析，以及一项发现认知行为治疗略占优势的元分析。<bookmark mark='c'/>近乎相等，但有例外。<bookmark mark='d'/>有争议。",
    'The fourth: the alliance between client and therapist correlates':
        "第四行：来访者与治疗师之间的联盟与疗效相关。<bookmark mark='a'/>原始研究：霍瓦特和西蒙兹，1991年。<bookmark mark='b'/>记录：二百九十五项研究。<bookmark mark='c'/>相关成立；方向有争论。<bookmark mark='d'/>得到重复。",
    'The fifth: dialectical behaviour therapy reduces self-harm.':
        "第五行：辩证行为治疗能减少自我伤害。<bookmark mark='a'/>原始研究：莱恩汉和同事们，1991年。<bookmark mark='b'/>记录：一项更大的试验，以及一项元分析。<bookmark mark='c'/>后来效应较小，但依然存在。<bookmark mark='d'/>得到重复。",
    'The sixth: a session of debriefing after a trauma':
        "第六行：创伤后的一次晤谈能预防创伤后应激。<bookmark mark='a'/>原始研究：米切尔的方法，1983年。<bookmark mark='b'/>记录：一篇考克兰综述，以及一项三年追踪。<bookmark mark='c'/>没有预防作用，而且可能有害。<bookmark mark='d'/>失败。",
    'And the seventh: confronting young offenders in prisons deters crime.':
        "第七行：让青少年违法者在监狱里直面囚犯能阻止犯罪。<bookmark mark='a'/>原始研究：这个项目及其纪录片，1978年。<bookmark mark='b'/>记录：一篇关于随机试验的综述。<bookmark mark='c'/>它增加了违法行为。<bookmark mark='d'/>失败。",
    'The tally.':
        "清点一下。<bookmark mark='a'/>站得住的：心理治疗胜过不治疗，联盟与疗效相伴，辩证行为治疗减少自我伤害。<bookmark mark='b'/>缩小了或有争议的：已发表的效应大小，以及渡渡鸟。<bookmark mark='c'/>失败的：心理晤谈和“恐吓从善”，两者都造成了伤害。",
    'Chapter thirteen. In practice: guidelines, choices and monitoring.':
        "第13章。实践：指南、选择与监测。",
    'In practice, evidence reaches a person in steps.':
        "在实践中，证据一步步到达一个人。<bookmark mark='a'/>指南：专家小组对试验分级并提出建议。在阶梯式照护中，先用可能有帮助的强度最低的治疗。<bookmark mark='b'/>选择：针对这个问题的证据、本人的偏好，以及能获得什么。一位可信的治疗师和疗法的品牌同样重要。<bookmark mark='c'/>监测：每次会谈填一份简短的问卷，用第8章的可靠变化规则来解读。向治疗师反馈偏离正轨的来访者，能减少病情恶化。<bookmark mark='d'/>改变方向：几次会谈后仍没有可靠的变化，就是改变计划的理由，而不是坚持下去的理由。<bookmark mark='e'/>对来访者来说：问一问这是什么疗法、它是为了什么、如何判断进展，以及如果没有效果会怎么办。",
    'Chapter fourteen. Frontier: mechanisms, matching and psychedelics.':
        "第14章。前沿：机制、匹配与迷幻药。",
    'At the frontier, three ideas.':
        "在前沿，有三个想法。<bookmark mark='a'/>机制：各种疗法声称是通过改变想法、技能或关系而起作用的。但要表明这种改变先发生、并导致了好转，却很少见。<bookmark mark='b'/>匹配：根据一个人的特征，预测两种治疗中哪一种更适合他的模型。它们很有前景，但仍有待前瞻性的检验。那是第59部分。<bookmark mark='c'/>迷幻药：裸盖菇素和MDMA，配合心理治疗使用。参与者几乎总是知道自己有没有服药，所以盲法失效了，而在2024年，美国监管机构拒绝批准MDMA辅助治疗创伤后应激障碍。<bookmark mark='d'/>每一个前沿都需要这一部分用到的东西：一个好的对照，一份未经过滤的记录，以及对本人真正重要的结果。",
    'So, open questions.':
        "那么，悬而未决的问题。心理治疗的效应有多少来自共同因素，又有多少来自特定技术？<bookmark mark='b'/>谈话治疗合适的安慰剂是什么？<bookmark mark='c'/>为什么有些来访者会变得更糟，这能预测吗？<bookmark mark='d'/>更简单、更便宜的疗法能否在不损失效应的情况下缩小治疗缺口？<bookmark mark='e'/>以及，迷幻药治疗的试验能否做到盲法，还是应该用不同的方式来评判？",
    'First, your four numbers.':
        "首先，你的四个数字。<bookmark mark='a'/>史密斯和格拉斯的平均效应量：零点六八。看起来是阳性的已发表抗抑郁药试验：百分之九十四，而在监管机构那里大约是一半。联盟与疗效的相关：大约零点二八。一半来访者好转时的会谈次数：大约八次。<bookmark mark='b'/>心理治疗有效。已发表的效应太大。而对照决定了大小。",
    'Part forty-two in eleven lines.':
        "用十一行总结第42部分。<bookmark mark='a'/>艾森克，1952年：人们反正会好转，只有对照才能说明治疗增加了多少。向均值回归：人们在最糟糕的时候入组，所以每一组都会好转。对照决定效应：等待名单、不治疗、安慰剂疗法。元分析把研究放到同一个尺度上并加权；史密斯和格拉斯发现了零点六八。渡渡鸟：真正的疗法平均而言近乎相等，但有例外。联盟与疗效的相关大约是零点二八，方向有争论。心理治疗和药物效果差不多，而心理治疗的效果比治疗本身更持久。发表偏倚夸大了效应；真实的效应更小，但是真的。可靠变化和分界点能说明一个人是否好转了。有些治疗有害：心理晤谈、“恐吓从善”、恢复记忆。一半的来访者大约在八次会谈内好转，而大多数人根本得不到任何心理治疗。",
    "Kant's wager.":
        "康德的赌注。<bookmark mark='a'/>第一个反驳，即数学无法应用于心灵，遇到了向均值回归、随机效应、可靠变化和发表过滤，全都经过计算。<bookmark mark='b'/>第二个反驳，即心灵无法被实验，遇到了谈话治疗的随机试验，用不同的对照来回答不同的问题。<bookmark mark='c'/>第三个，关于内省：结果大多是自我报告，而且来访者无法对治疗保持盲态。琥珀色。",
    'Where this comes back.':
        "这些内容会在哪里再次出现。<bookmark mark='a'/>从头到尾重复一项研究，是下一部分，第43部分，也就是毕业项目。元分析及其偏倚，正式地讲，是第50部分。缩小治疗缺口是第57部分。把治疗与人相匹配是第59部分。",
    "Seven problems, with full solutions in this part's README.":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道计算向均值回归。一道把结束时的得分换算成相对于三种对照的效应量。一道亲手做一次小型元分析。一道判断可靠的变化。一道求分界点。一道算出显著性过滤对已发表效应的影响。最后一道带星号，请你设计一项试验，把特定成分与共同因素区分开。如果你想试试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README.':
        "这一部分背后的书和论文列在这里，也列在README里。万波尔德和伊梅尔的《伟大的心理治疗之争》为共同因素立论；瓦伦斯坦的《伟大而绝望的疗法》讲述了脑叶切除术的历史；而史密斯、格拉斯和米勒的书是回答了艾森克的完整元分析。",
    'Act Ten is complete.':
        "第十幕完成了。<bookmark mark='a'/>它问了什么是障碍，用本系列自己的模型搭建了恐惧与悲伤、精神病性障碍与成瘾，并掂量了心理治疗的证据。<bookmark mark='b'/>下一部分是整个学位的毕业项目。从账本中选出一个经典效应，在屏幕上恰当地重复它，从选择目标到撰写报告，观众也作为参与者。第43部分：重复。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
