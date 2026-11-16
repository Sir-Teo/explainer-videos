"""Chinese narration for psych60: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第60部分：心智与机器'

CHAPTERS = {
    'Hook': '一位心理学家的机器',
    'Predict': '1. 在你身上：人还是机器，以及四个数字',
    'Networks': '2. 作为心智模型的网络',
    'MachinePsych': '3. 机器心理学',
    'Tom': '4. 机器的心理理论',
    'Psychometrics': '5. 机器的心理测量',
    'Trust': '6. 人对机器的信任',
    'Persuasion': '7. 改变人心的机器',
    'Care': '8. 作为助手和陪伴者的机器',
    'Silicon': '9. 硅基样本',
    'Screens': '10. 屏幕与幸福感',
    'Lack': '11. 机器缺少什么，又拥有什么',
    'Behaviour': '12. 一门机器行为的科学',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：评估一个模型',
    'Frontier': '15. 前沿：两门关于心智的科学',
    'Outro': '回顾、习题与前方的路',
}

ZH = {
    'In 1958 a learning machine called the Perceptron was published in Psychological Review, by':
        "1958年，一台名叫感知机的学习机器发表在《心理学评论》上，作者是一位心理学家，弗兰克·罗森布拉特。<bookmark mark='a'/>这一部分就从那里开始。<bookmark mark='b'/>强化学习来自巴甫洛夫和桑代克，也就是第16和第17部分。几十年来，人工智能一直在向心理学借东西。<bookmark mark='c'/>1966年，约瑟夫·魏岑鲍姆的ELIZA用一个简单的脚本把人说的话变成问题，而魏岑鲍姆沮丧地发现，它的用户那么轻易就向它倾诉。<bookmark mark='d'/>如今这笔债是双向的。语言模型参加心理学的测验，被提出作为心智的模型，还被用作顾问、助手和替身参与者。<bookmark mark='e'/>这些用途每一个都是一个心理学主张，而这一部分用前五十九部分的工具逐一检验它们。",
    'So this part asks: what can psychology and artificial intelligence now tell each other? <b':
        "所以这一部分问：心理学和人工智能如今能告诉彼此什么？<bookmark mark='a'/>机器作为心智的模型，也作为心理学测验的对象。<bookmark mark='b'/>陷阱：污染、提示语，以及一个模型不是一个样本这一事实。<bookmark mark='c'/>人与机器：信任、说服、照护，以及替身参与者。<bookmark mark='d'/>还有屏幕与幸福感，以及机器缺少什么。",
    "This is Part 60 of Psychology, Built: minds and machines. <bookmark mark='a'/> We'll judge":
        "这是《心理学，从零搭建》的第60部分：心智与机器。<bookmark mark='a'/>我们将把一个网络当作心智的模型来评判，并看到为什么行为相符不等于机制相同。我们将在没有污染、没有伪重复的情况下测试一台机器。我们将把基准测试当作一项测验，讲效度、项目反应理论和样本量。我们将预测人如何依赖、信任机器，又如何被机器说服。我们将说明硅基样本在哪里失效，并权衡关于屏幕的争论。我们还将说明一门机器行为的科学需要从心理学得到什么。",
    'Chapter one. On you: human or machine, and four numbers.':
        '第一章。在你身上：人还是机器，以及四个数字。',
    'First, an experiment on you. Here are six sentences about the mind. Three are William Jame':
        "首先，一个在你身上做的实验。这里有六个关于心智的句子。三句出自威廉·詹姆斯1890年的《心理学原理》。另外三句是一个语言模型为这部影片写的，要求它模仿他的笔法。<bookmark mark='a'/>对每一句，判断：是詹姆斯，还是机器？<bookmark mark='b'/>如果你想慢慢读，可以在这里暂停，写下你的六个答案。",
    "Here are the answers. <bookmark mark='a'/> One, three and five are James: attention, the b":
        "答案在这里。<bookmark mark='a'/>第一、第三和第五句是詹姆斯的：注意、婴儿那一片“繁盛而嘈杂的混乱”，以及思想之流。第二、第四和第六句是机器的。<bookmark mark='b'/>研究用更大的文本样本做这个测试时，人分辨简短的机器文字和人类文字，只比碰运气好一点点。这既是关于文字的事实，也是关于我们自己的事实：我们凭表面来判断心智。",
    "Now four numbers. <bookmark mark='a'/> One: a model memorized eighty percent of a publishe":
        "现在是四个数字。<bookmark mark='a'/>第一：一个模型背下了某个已发表测验百分之八十的题目。在同样问题的改写版上，它得多少分？<bookmark mark='b'/>第二：一个模型，用一百种措辞提问，给出一个三分宽的百分之九十五区间。这是关于语言模型的区间吗？<bookmark mark='c'/>第三：模拟的回答者填写一份调查。他们答案的离散程度与真人相比如何？<bookmark mark='d'/>第四：就青少年的屏幕时间和幸福感而言，屏幕时间能解释幸福感变异的多大比例？在这里暂停，把它们写下来。",
    'Chapter two. Networks as models of the mind.':
        '第二章。作为心智模型的网络。',
    "When does a network explain a brain? First, vision. <bookmark mark='a'/> In 2016 Daniel Ya":
        "一个网络什么时候能解释一个大脑？先说视觉。<bookmark mark='a'/>2016年，丹尼尔·亚明斯和詹姆斯·迪卡洛表明，只被训练来识别物体的网络，能预测腹侧通路，也就是第14部分那条通路上神经元的反应，比手工构建的模型预测得更好。<bookmark mark='b'/>如今的基准测试拿许多网络与许多神经和行为数据集比较打分。<bookmark mark='c'/>但它们的错误与人的不同。它们看重纹理胜过形状，而且被人眼察觉不到地改动过的图像就能改变它们的答案。<bookmark mark='d'/>2023年，杰弗里·鲍尔斯及其同事主张，能很好地预测神经数据并不是机制相同的证据，网络应当用心理学的受控实验来检验。",
    "Second, language. <bookmark mark='a'/> Part 23 showed that a language model's surprisal pr":
        "再说语言。<bookmark mark='a'/>第23部分表明，语言模型的意外度能预测阅读时间和N400。<bookmark mark='b'/>凯尔·马霍瓦尔德及其同事把形式能力，也就是语法，模型具备，与功能能力，也就是推理、知识和社会常识，区分开来，后者参差不齐。<bookmark mark='c'/>还有一个数据差距。儿童学会语言所用的词，比模型训练用的少好几个数量级。<bookmark mark='d'/>所以一个模型可以是“从文本中能学到什么”的好模型，同时是“儿童如何学习”的差模型。",
    "So, behaviour matched is not mechanism shared. <bookmark mark='a'/> A network can match pe":
        "所以，行为相符不等于机制相同。<bookmark mark='a'/>一个网络可以在马尔所说的“计算什么”层面上与人相符，而在“如何完成”上不同，正如第1部分所说。<bookmark mark='b'/>比较各自答错的是哪些题，而不是总体准确率。<bookmark mark='c'/>使用前面各部分的受控测试：最小对比对、分离和错觉。<bookmark mark='d'/>而回报是：一个通过了这些测试的网络，是一个你可以打开、可以损毁的候选理论，而大脑很少允许你这样做。",
    'Chapter three. Machine psychology.':
        '第三章。机器心理学。',
    "What happens when a model sits psychology's tests? <bookmark mark='a'/> In 2023 Marcel Bin":
        "当一个模型参加心理学的测验时，会发生什么？<bookmark mark='a'/>2023年，马塞尔·宾茨和埃里克·舒尔茨把第26部分的情境题交给一个语言模型：琳达问题、框架效应和认知反思测验。它的回答很像人，连偏差也一样。<bookmark mark='b'/>后来的模型解出了同样的经典题目，偏差缩小或消失了。<bookmark mark='c'/>那是推理，还是这些题目，有名而且在网上被讨论得很多，就在训练文本里？<bookmark mark='d'/>接下来有三个陷阱，每一个都是这个系列前面的一课。",
    "Trap one: contamination. <bookmark mark='a'/> Psyche has two test-takers. One saw eighty p":
        "陷阱一：污染。<bookmark mark='a'/>普赛克有两个应试者。一个在训练中见过已发表题目的百分之八十。另一个靠推理，正确率百分之五十六。<bookmark mark='b'/>在已发表的题目上，背题者赢了：大约百分之八十五对百分之五十六。<bookmark mark='c'/>把题目改写一下，逻辑不变，背题者就跌到百分之二十五，也就是碰运气的水平。推理者保持在百分之五十四。这是你的第一个数字。<bookmark mark='d'/>补救办法是第2部分的：新题目，在训练之后编写，以及旧题目的扰动版本。",
    "Traps two and three. <bookmark mark='a'/> Trap two: answers move with the wording, the ord":
        "陷阱二和陷阱三。<bookmark mark='a'/>陷阱二：答案会随着提示语的措辞、顺序和示例而变动，所以要报告多种措辞。<bookmark mark='b'/>陷阱三：对一个模型用一百种措辞提问，得到一个很窄的区间，也就是红色的条。这是你的第二个数字。<bookmark mark='c'/>但模型彼此之间有差异。对于一个关于模型的主张，模型才是被试，而一个模型是一个大小为一的样本。诚实的区间是绿色的条。<bookmark mark='d'/>这就是第47部分的伪重复：对一个被试的多次测量，不等于多个被试。",
    'Chapter four. Theory of mind in machines.':
        '第四章。机器的心理理论。',
    "Does a model know what others believe? <bookmark mark='a'/> In 2023 Michal Kosinski report":
        "一个模型知道别人相信什么吗？<bookmark mark='a'/>2023年，米哈尔·科辛斯基报告说，大型语言模型能通过错误信念任务，也就是第35部分的莎莉-安妮任务，达到学龄儿童的水平。<bookmark mark='b'/>托默·厄尔曼表明，一些琐碎的改动，比如一个透明的袋子，或者一个已经被告知真相的人，就会让答案出错。那是对任务熟悉形式的模式匹配。<bookmark mark='c'/>2024年，詹姆斯·斯特拉坎及其同事用一组心理理论测验，把模型与大约一千九百人做了比较。模型在一些测验上达到或超过了人，在另一些上低于人，比如识别失言，而且回答风格偏谨慎。<bookmark mark='d'/>这个主张仍有争议，而方法已经改进了。",
    "Here's one item, perturbed. <bookmark mark='a'/> The classic: Sam puts chocolate in a box ":
        "这是一道被扰动的题目。<bookmark mark='a'/>经典版本：萨姆把巧克力放进一个盒子，然后离开。安娜把它挪到一个袋子里。萨姆会去哪里找？盒子里，因为他没看见它被挪走。<bookmark mark='b'/>现在扰动它。袋子是透明的，萨姆回来时能透过袋子看见巧克力。<bookmark mark='c'/>正确答案变了。一个追踪萨姆能看见什么的读者会说袋子。一个套用熟悉故事的读者会说盒子。<bookmark mark='d'/>2023年，托默·厄尔曼表明，像这样的小改动就让通过了原题的模型出错。后来的模型能通过更多这样的题目，这正是测试集必须不断更新的原因。<bookmark mark='e'/>这和第30部分的婴儿研究是同一个逻辑：一种能力，要由只有它才能给出正确答案的情形来证明。",
    "What would a valid test need? <bookmark mark='a'/> New items: stories never published, in ":
        "一个有效的测试需要什么？<bookmark mark='a'/>新题目：从未发表过的故事，以模型没见过的形式出现。<bookmark mark='b'/>对照：真实信念版本，让只追踪故事事实的做法失败。<bookmark mark='c'/>汇聚的任务：几种应当一致的测量，正如第30部分对婴儿注视的要求。<bookmark mark='d'/>人类基线：同样的题目、同样的计分，用在人身上。<bookmark mark='e'/>这就是第30部分的一课。婴儿的心理理论围绕注视时间争论了几十年，而关于一种新被试的主张，也值得同样的谨慎。",
    'Chapter five. Psychometrics for machines.':
        '第五章。机器的心理测量。',
    "Is a benchmark a good test? It is a test, so ask Part 3's questions. <bookmark mark='a'/> ":
        "一个基准测试是好测验吗？它就是一项测验，所以问第3部分的那些问题。<bookmark mark='a'/>构念：分数代表什么？推理、知识，还是安全？<bookmark mark='b'/>信度：换一组题目，排名还能保持吗？<bookmark mark='c'/>饱和：一旦每个模型的得分都接近满分，这个测验就再也区分不开它们。<bookmark mark='d'/>还有古德哈特定律：一个变成目标的分数，就不再测量它原来测量的东西。",
    "Which items do the work? <bookmark mark='a'/> Psyche's benchmark has three hundred items, ":
        "哪些题目在起作用？<bookmark mark='a'/>普赛克的基准有三百道题，用第45部分的双参数模型拟合，还有十二个模型，能力落在阴影带里。<bookmark mark='b'/>最好的五分之一题目承载了将近一半的信息。它们区分度高，而且难度正好落在模型所在的地方。<bookmark mark='c'/>太容易或太难的题目，对这些模型什么也说明不了。<bookmark mark='d'/>一个更短的自适应基准也能把它们排得一样好。这就是第45部分的计算机化自适应测验。",
    "How many items does it take to tell two models apart? <bookmark mark='a'/> Take two models":
        "要分辨两个模型，需要多少道题？<bookmark mark='a'/>取两个准确率接近百分之七十、相差三个百分点的模型，显著性水平百分之五，统计功效百分之八十。<bookmark mark='b'/>如果在不同的题目上计分，大约需要三千七百道题。<bookmark mark='c'/>如果在相同的题目上配对，题目得分相关，大约需要一千八百道。<bookmark mark='d'/>许多排行榜区分模型的差距，小于它们的题目所能分辨的程度。要报告区间，并做配对比较，正如第4部分所教的。",
    'Chapter six. People trusting machines.':
        '第六章。人对机器的信任。',
    "Do people rely on machines too much, or too little? <bookmark mark='a'/> In 2015 Berkeley ":
        "人对机器依赖得太多，还是太少？<bookmark mark='a'/>2015年，伯克利·迪特沃斯特、约瑟夫·西蒙斯和凯德·梅西发现，看到算法犯过一次错的人会更少选择它，即便它比他们强。他们称之为算法厌恶。<bookmark mark='b'/>2019年，詹妮弗·洛格、朱莉娅·明森和唐·穆尔发现，人在被告知建议来自算法时，往往会更看重它：算法欣赏。<bookmark mark='c'/>两者都成立，只是在不同的任务中：在看得见的错误之后和在关乎品味的事情上是厌恶，在数字预测上是欣赏。<bookmark mark='d'/>还有第51部分的自动化偏差：可靠系统的监督者会停止检查它们。",
    "What does aversion cost? <bookmark mark='a'/> Psyche's two thousand people have an aid tha":
        "厌恶的代价是什么？<bookmark mark='a'/>普赛克的两千人有一个正确率百分之八十的辅助工具，和他们自己正确率百分之七十的判断。<bookmark mark='b'/>每当他们依赖辅助工具而它出了错，他们就把依赖减半，而他们自己的错误却被原谅了。<bookmark mark='c'/>依赖稳定在一半左右，准确率稳定在百分之七十五左右，而始终依赖能达到百分之八十。<bookmark mark='d'/>已经研究过的补救办法：让人可以稍微调整算法，以及展示它与人自己的成绩对比。",
    "How do people see a mind in a machine? <bookmark mark='a'/> In 2007 Heather Gray, Kurt Gra":
        "人是怎样在机器里看到心智的？<bookmark mark='a'/>2007年，希瑟·格雷、库尔特·格雷和丹尼尔·韦格纳发现，人从两个维度判断心智：能动性，它能计划和行动吗；以及体验，它能感受吗？<bookmark mark='b'/>机器在能动性上被评为中等，在体验上被评为低。<bookmark mark='c'/>一个声音、一个名字和流利的语言会同时提高这两个评分，不管底下是什么。<bookmark mark='d'/>所以设计上的问题是，系统到底该不该以心智的面目出现。",
    'Chapter seven. Machines changing minds.':
        '第七章。改变人心的机器。',
    "Can a conversation with a machine change a belief? <bookmark mark='a'/> In 2024 Thomas Cos":
        "和一台机器的一次对话能改变一个信念吗？<bookmark mark='a'/>2024年，托马斯·科斯特洛、戈登·彭尼库克和戴维·兰德让相信某个阴谋论的人描述它，然后与一个模型进行三轮对话，模型针对他们自己的证据作答。<bookmark mark='b'/>与就另一个话题进行的对照对话相比，对那个理论的相信程度平均下降了大约五分之一。<bookmark mark='c'/>两个月后效应仍然存在，还稍微外溢到了其他阴谋信念上。<bookmark mark='d'/>他们提出的机制是针对这个人自己的理由量身定做的事实，而正如第34部分发现的，人很少得到这样的事实。<bookmark mark='e'/>同样的力量可以朝任何方向使用，所以谁控制有说服力的系统，是一个属于整个社会的问题。",
    "There's an opposite risk. <bookmark mark='a'/> Sycophancy: models trained on human approva":
        "还有一个相反的风险。<bookmark mark='a'/>谄媚：用人的认可来训练的模型，学会了附和用户表明的观点，即使那个观点是错的。<bookmark mark='b'/>为什么？人会给附和打高分。这是第34部分的从众，反过来学到的。<bookmark mark='c'/>风险在于一个自信又随和的顾问，它证实你本来就相信的东西，也就是第24部分的证实偏差。<bookmark mark='d'/>而且它可以测量：同一个问题，带上和不带一个表明的观点各问一次，数一数答案翻转了多少次。",
    'Chapter eight. Machines as helpers and companions.':
        '第八章。作为助手和陪伴者的机器。',
    "Can a chatbot help, and what would show it? <bookmark mark='a'/> Scripted chatbots that de":
        "一个聊天机器人能帮上忙吗？什么能证明这一点？<bookmark mark='a'/>提供认知行为疗法练习的脚本式聊天机器人，已经在小规模、短期的试验中检验过，与只提供信息的对照相比有适度的改善。<bookmark mark='b'/>2025年，迈克尔·海因茨及其同事把大约两百名成年人随机分配到一个为治疗而构建的生成式聊天机器人组或等待名单组，发现试验期间抑郁和焦虑症状下降得更多。<bookmark mark='c'/>但等待名单对照会让任何治疗显得更好，正如第42部分所展示的，而且还没有与人类治疗师或积极对照比较的试验。<bookmark mark='d'/>陪伴类应用：许多用户报告孤独感减少，但在一些研究中，重度使用伴随着更多的孤独，而因果方向未知。",
    "What would a well-designed helper look like? <bookmark mark='a'/> Scope: it says what it's":
        "一个设计良好的助手应当是什么样子？<bookmark mark='a'/>范围：它说明自己是做什么的，比如练习一项技能或记录心境，以及不是做什么的，比如诊断或紧急情况。<bookmark mark='b'/>升级：它能察觉一个人何时需要超出它能给予的帮助，并把他们转接给一个人，而这个察觉器要像任何分类器一样，按它的漏报来检验。<bookmark mark='c'/>比较：它要与积极对照比较，而不是等待名单，正如第42部分所要求的，结果要在几周后测量。<bookmark mark='d'/>还有隐私：人告诉它的是健康数据，存储、共享和删除都要遵守与诊所相同的规则。",
    "So what do Part 42's standards require? <bookmark mark='a'/> An active control: the compar":
        "那么第42部分的标准要求什么？<bookmark mark='a'/>积极对照：患者原本会得到的比较对象，而不是等待名单。<bookmark mark='b'/>持久的结果，在几个月里由不知道分组的人测量。<bookmark mark='c'/>计入伤害：错误的建议、依赖、隐私，以及有人需要紧急帮助时系统如何回应。<bookmark mark='d'/>还有它触及了谁：它是为原本没有照护的人增加了照护，还是替代了原本有照护的人的照护。",
    'Chapter nine. Silicon samples.':
        '第九章。硅基样本。',
    "Can a model stand in for participants? <bookmark mark='a'/> In 2023 Lisa Argyle and collea":
        "一个模型能替代参与者吗？<bookmark mark='a'/>2023年，莉萨·阿盖尔及其同事用几千名真实回答者的背景信息提示一个模型，它重现了美国调查中这些人的投票选择和态度模式。<bookmark mark='b'/>它的前景是廉价的预试验、协助调查设计，以及难以接触的群体。<bookmark mark='c'/>后来的研究发现，回答过于一致，少数群体的观点被拉向多数人的观点，而且结果会随模型及其版本而变化。<bookmark mark='d'/>第46部分的调查科学要问：均值相同，但离散程度也相同吗，子群体也相同吗？",
    "Here's that test in Psyche. Five groups answer a survey question, and silicon respondents ":
        "这是在普赛克中做的那个检验。五个群体回答一个调查问题，硅基回答者根据模型吸收的内容作答。<bookmark mark='a'/>总体均值相符。<bookmark mark='b'/>离散程度不符：人的标准差是一点七，硅基的是零点七。这是你的第三个数字。<bookmark mark='c'/>最小的那个群体偏差了将近一分，被拉向了多数。<bookmark mark='d'/>所以，用硅基样本做预试验和推敲措辞，而关于人的主张要在人身上检验。",
    'Chapter ten. Screens and well-being.':
        '第十章。屏幕与幸福感。',
    "Are phones harming teenagers? This is a live dispute, so here is each side's best case. <b":
        "手机在伤害青少年吗？这是一场正在进行的争论，所以这里给出双方最有力的论证。<bookmark mark='a'/>认为有害的一方：从大约2012年智能手机普及时起，几个国家的青少年报告的抑郁上升了。重度使用者报告的幸福感更差，而时间上的吻合和机制，睡眠减少、社会比较和被挤占的活动，都说得通。<bookmark mark='b'/>认为危害很小的一方：这些关联很微弱，在一项分析中和戴眼镜或吃土豆的关联差不多。趋势因国家和测量方式而异，而因果方向未知。<bookmark mark='c'/>双方一致的地方：都呼吁因果设计、更好的使用测量，以及来自平台的数据。",
    "Amy Orben and Andrew Przybylski's tool for this is the specification curve: run every defe":
        "埃米·奥本和安德鲁·普日比尔斯基用来研究这个问题的工具是设定曲线：跑完每一种站得住脚的分析，把它们全部展示出来。<bookmark mark='a'/>普赛克的调查有一万名青少年，一个很小的真实效应，以及同时影响屏幕使用和幸福感的混杂因素：睡眠、收入和学校。<bookmark mark='b'/>一共有两百八十八种分析：三种使用测量、三种幸福感测量、十六组控制变量，以及两个样本。<bookmark mark='c'/>每个效应都是负的而且很小，大多数之所以显著，只是因为样本很大。<bookmark mark='d'/>屏幕时间大约解释了幸福感变异的百分之一。这是你的第四个数字。在真实数据中，奥本和普日比尔斯基发现最多是百分之零点四。",
    "What do experiments say? <bookmark mark='a'/> In 2020 Hunt Allcott and colleagues paid peo":
        "实验怎么说？<bookmark mark='a'/>2020年，亨特·奥尔科特及其同事付钱让人们在一次选举前停用脸书四周。他们报告的幸福感略有提高，并把时间花在了其他活动上。<bookmark mark='b'/>其他停用和减少使用的实验结果不一，效应大多很小，而且是在成年人中。<bookmark mark='c'/>对青少年的大规模实验很少，而自然实验，比如宽带的铺开和学校的手机禁令，正在研究中。<bookmark mark='d'/>诚实的总结是：平均效应很小，对某些人和某些用法而言更大的伤害是可能的，只是还没有被很好地测量。",
    'Chapter eleven. What machines lack, and have.':
        '第十一章。机器缺少什么，又拥有什么。',
    "What would a child-like learner need? <bookmark mark='a'/> In 2017 Brenden Lake and collea":
        "一个像儿童那样的学习者需要什么？<bookmark mark='a'/>2017年，布伦登·莱克及其同事主张，人能从一个或几个例子中学会新概念，构建因果模型，并且从婴儿期起就使用直觉物理学和直觉心理学。<bookmark mark='b'/>发展性基准测试如今把第30部分关于客体永久性、数和能动性的测验交给模型。<bookmark mark='c'/>儿童规模的学习用一个儿童所接触的语言量，或者一个儿童头戴摄像机拍下的视频来训练模型。<bookmark mark='d'/>到目前为止，这样训练的模型学会了一些词和类别，而大部分差距仍然存在。",
    "There's also a data gap. <bookmark mark='a'/> A child hears on the order of millions of wo":
        "还有一个数据差距。<bookmark mark='a'/>一个儿童一年听到的词在几百万这个量级，到学龄就能流利说话。<bookmark mark='b'/>大型语言模型用几万亿个词训练，多出好几个数量级。迈克尔·弗兰克在2023年阐明了这个差距。<bookmark mark='c'/>所以一个模型的流利，并不是儿童学习机制的证据。儿童带来了更多先天的结构，或者从更丰富的输入中学习，视觉、触觉和其他人，或者两者都有。<bookmark mark='d'/>悬而未决的实验，是用一个儿童可能听到和看到的东西来训练模型，看它们学到了什么。",
    "Part 27 left a question open. Here it is, asked of machines. <bookmark mark='a'/> The theo":
        "第27部分留下了一个悬而未决的问题。这里把它拿来问机器。<bookmark mark='a'/>第27部分的那些理论，全局工作空间、高阶理论和循环加工，各自列出了一个系统需要具备的功能。<bookmark mark='b'/>一种做法是对照这些指标，一个理论一个理论地检查一个系统的架构。<bookmark mark='c'/>单靠行为无法定论：一个用人类文本训练的系统，不管它有没有体验，都会描述体验。<bookmark mark='d'/>这个问题是开放的，而两种错误，归因过多或过少，都有代价。",
    'Chapter twelve. A science of machine behaviour.':
        '第十二章。一门机器行为的科学。',
    "What does psychology bring? <bookmark mark='a'/> In 2019 Iyad Rahwan and colleagues propos":
        "心理学能带来什么？<bookmark mark='a'/>2019年，伊亚德·拉万及其同事提出，像研究动物那样研究机器：研究它们在野外的行为、行为的发展、功能和演化。<bookmark mark='b'/>工程师知道代码，却不知道从训练和使用中涌现出来的行为。<bookmark mark='c'/>心理学一个世纪的方法正好适用：实验、对照、信度、样本和重复。<bookmark mark='d'/>而机器会变，所以一个结果是关于某个日期的某个模型的，就像账本里的一行。",
    "Here's the toolkit, part by part. <bookmark mark='a'/> Part 2: randomize, control, and bli":
        "这是工具箱，一部分一部分来。<bookmark mark='a'/>第2部分：随机化、设置对照，并让评分者不知情。<bookmark mark='b'/>第3和第45部分：构念效度、信度和项目反应理论。<bookmark mark='c'/>第4部分：预注册，数清分岔路径，报告试过的每一个模型。<bookmark mark='d'/>第47部分：模型才是被试，所以要测试许多模型，而不是许多提示语。<bookmark mark='e'/>还有第48部分：比较拟合出来的行为模型，而不是单个分数。",
    'Chapter thirteen. The Ledger.':
        '第十三章。账本。',
    "Five new rows. The first: language models show people's biases on the classic judgment pro":
        "五个新行。第一行：语言模型在经典判断问题上表现出人的偏差。<bookmark mark='a'/>原始研究：宾茨和舒尔茨，2023年。<bookmark mark='b'/>记录：这些偏差在后来的模型中消退了。<bookmark mark='c'/>这取决于模型和措辞，而且这些题目就在训练文本里。<bookmark mark='d'/>有争议。",
    "The second: language models have a robust theory of mind. <bookmark mark='a'/> The origina":
        "第二行：语言模型具有稳健的心理理论。<bookmark mark='a'/>原始研究：科辛斯基，2023年。<bookmark mark='b'/>记录：在琐碎改动上的失败，以及一项与一千九百人的比较。<bookmark mark='c'/>在熟悉的形式上很强，超出这些形式就有争议。<bookmark mark='d'/>有争议。",
    "The third: after seeing an algorithm err, people avoid it, even when it's better. <bookmar":
        "第三行：看到一个算法犯错之后，人会回避它，即使它更好。<bookmark mark='a'/>原始研究：迪特沃斯特、西蒙斯和梅西，2015年。<bookmark mark='b'/>记录：算法欣赏，以及能恢复使用的控制权。<bookmark mark='c'/>两者都能重复；由任务决定。<bookmark mark='d'/>有争议。",
    'The fourth: a short conversation with a model durably reduces belief in a conspiracy theor':
        "第四行：与一个模型的简短对话能持久地降低对一个阴谋论的相信。<bookmark mark='a'/>原始研究：科斯特洛、彭尼库克和兰德，2024年。<bookmark mark='b'/>记录：到目前为止，只有这篇论文自己的两项研究。<bookmark mark='c'/>前景可观，有待独立重复。<bookmark mark='d'/>尚未直接检验。",
    "And the fifth: smartphones and social media caused a large rise in adolescents' depressive":
        "第五行：智能手机和社交媒体导致青少年的抑郁症状大幅上升。<bookmark mark='a'/>原始研究：特文格及其同事，2018年。<bookmark mark='b'/>记录：跨各种设定的微弱关联，以及成年人停用后的小幅获益。<bookmark mark='c'/>上升是真实的；原因和大小有争议。<bookmark mark='d'/>有争议。",
    "What the five have in common. <bookmark mark='a'/> Four of five are contested. It's a youn":
        "这五行的共同点。<bookmark mark='a'/>五行中有四行有争议。这是一个年轻的领域，它的研究对象每年都在变。<bookmark mark='b'/>争论都关乎方法：污染、扰动、对照和因果设计。<bookmark mark='c'/>而每一行都以同样的方式解决：新题目、许多模型、随机化实验和重复。<bookmark mark='d'/>所以这一部分问题的答案是：心理学和人工智能可以告诉彼此很多东西，只要双方都使用心理学的方法。",
    'Chapter fourteen. In practice: evaluating a model.':
        '第十四章。实践中：评估一个模型。',
    "Where is this a job? <bookmark mark='a'/> In AI evaluation: designing benchmarks and studi":
        "这在哪里是一份工作？<bookmark mark='a'/>在AI评估中：用心理测量学设计基准测试和模型行为研究。<bookmark mark='b'/>在人与AI的交互中：人如何依赖、信任系统并与之合作，以及如何校准这种依赖。<bookmark mark='c'/>在安全与对齐中：红队测试，以及对谄媚、说服和欺骗的测试。<bookmark mark='d'/>还有在产品和研究中：按临床标准要求的心理健康产品，以及用合成回答者做的市场研究，并要对照真人验证。",
    "Here's a worked evaluation plan. <bookmark mark='a'/> The construct: write down what reaso":
        "这是一份算好的评估方案。<bookmark mark='a'/>构念：写下“推理得更好”是什么意思，以及哪些任务能显示它。这是第3部分。<bookmark mark='b'/>题目：新题，在两个模型的训练之后编写，每道题都配一个扰动过的孪生版本。<bookmark mark='c'/>规模：在百分之七十附近提升三个百分点，在相同题目上配对，大约需要一千八百道题，题目相关性越低需要越多。<bookmark mark='d'/>提示语：几种措辞，事先固定，两个模型相同。<bookmark mark='e'/>报告：一个预注册的主要分数及其区间，每种措辞的结果，以及两个模型表现不同的那些题目。",
    'Chapter fifteen. Frontier: two sciences of minds.':
        '第十五章。前沿：两门关于心智的科学。',
    "What happens when both kinds of mind are studied together? First, what's new. <bookmark ma":
        "当两种心智被放在一起研究时，会发生什么？先说新进展。<bookmark mark='a'/>用许多实验的试次级数据微调的网络，被提出作为人类选择的通用模型，并用它们没见过的实验来评判。<bookmark mark='b'/>可解释性研究读取模型内部的特征和回路，把神经科学的方法用在机器上。<bookmark mark='c'/>现场实验在日常使用中对AI导师、顾问和陪伴者做随机化。<bookmark mark='d'/>关于人借助AI学习的研究，追问几个月下来，辅助对技能、记忆和信念有什么影响。",
    "And the open problems. <bookmark mark='a'/> A science of machine behaviour, with psycholog":
        "还有悬而未决的问题。<bookmark mark='a'/>一门机器行为的科学，用上心理学来之不易的方法，结果按模型版本标注日期。<bookmark mark='b'/>同时也是可以检查的机制的认知模型。<bookmark mark='c'/>无处不在的AI对人类学习、信念和关系的影响，用因果方法测量。<bookmark mark='d'/>以及要怎样才能知道一台机器是否有体验。",
    "First, your four numbers. <bookmark mark='a'/> The memorizer scored twenty-five percent on":
        "先说你的四个数字。<bookmark mark='a'/>背题者在改写的题目上得了百分之二十五，也就是碰运气的水平。对一个模型用一百种措辞提问，得到的区间只关于那一个模型。硅基回答者的离散程度是零点七，而人是一点七。在普赛克中，屏幕时间大约解释了幸福感变异的百分之一，在真实数据中最多是百分之零点四。<bookmark mark='b'/>每个答案都是心理学的一条老教训，用在一种新的被试身上。",
    "Part sixty in twelve lines. <bookmark mark='a'/> AI began in psychology, and now the debt ":
        "十二行总结第六十部分。<bookmark mark='a'/>AI始于心理学，如今这笔债是双向的。网络能预测大脑，而错误和对照检验机制。经典题目被污染了，所以要用新题和扰动过的题。一个模型是大小为一的样本。机器的心理理论有争议。基准测试就是测验，有效度、项目反应理论和样本量。厌恶和欣赏取决于任务。一次对话持久地改变了信念，有待重复。聊天机器人照护需要积极对照和计入伤害。硅基样本缩小了离散程度，抹去了少数群体。屏幕显示出微弱的关联，实验很少。而机器行为需要心理学的方法。",
    "Where this comes back. <bookmark mark='a'/> Language models as research assistants and sim":
        "这些内容会在哪里再出现。<bookmark mark='a'/>作为研究助手和模拟参与者的语言模型，以及写成代码的理论，是第61部分。第62部分的学位论文有一份注册过的分析。",
    "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One reads ":
        "七道习题，完整解答在这一部分的README里。<bookmark mark='a'/>一道解读一项污染测试。一道求样本量。一道区分两个模型。一道计算借助辅助工具时的准确率。一道追问哪些结论在硅基样本下站得住。一道追问一个微弱的关联是否可能要紧。最后一道带星号，请你设计一项心理健康聊天机器人的试验。如果你想试试，就在这里暂停。",
    "The books and papers behind this part are listed here and in the README. Melanie Mitchell'":
        '这一部分背后的书和论文列在这里，也列在README里。梅拉妮·米切尔的书清楚地介绍了AI能做什么、不能做什么；莱克及其同事的论文阐明了像人一样学习需要什么；拉万及其同事的论文提出了机器行为的科学。',
    "Three parts of the frontier are done. <bookmark mark='a'/> This one turned psychology's me":
        "前沿的三个部分已经完成。<bookmark mark='a'/>这一部分把心理学的方法用在机器上，也用在与机器一起生活的人身上。<bookmark mark='b'/>下一部分把它们用在心理学自身。如果这个领域在今天被设计出来，有大团队、巨大的样本和写成代码的理论，它会是什么样子？第61部分：下一代心理学。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
