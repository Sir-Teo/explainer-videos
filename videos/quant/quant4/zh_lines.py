"""Chinese narration for quant4: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).
Terms follow videos/quant/QUANT_ZH_GUIDE.md."""

TITLE = '量化金融，从零搭建 · 第4部分：鞅与测度'

CHAPTERS = {
    'Research': '写给研究者：公平的游走能走多远？',
    'Hook': '你能战胜公平博弈吗？',
    'Information': '1. 信息：σ代数与过滤',
    'Projection': '2. 条件期望是一种投影',
    'Martingales': '3. 鞅：维尔的公平博弈',
    'System': '4. 你赢不了这个系统',
    'Stopping': '5. 停时，以及永远会赢的随机游走',
    'Optional': '6. 可选停止定理的证明',
    'Doubling': '7. 加倍下注与容许策略',
    'Barings': '8. 加倍下注：巴林银行，1995',
    'Ruin': '9. 赌徒破产与大胆下注',
    'Convergence': '10. 鞅会收敛',
    'Doob': '11. 杜布分解',
    'Measure': '12. 测度变换',
    'Radon': '13. 拉东–尼科迪姆，以及奇异的无穷',
    'Stable': '14. 作为稳定分布的厚尾',
    'Betting': '15. 维尔不等式与以下注来检验',
    'House': '16. 学会下注',
    'Industry': '17. 赌场、庄家与市场',
    'Frontier': '18. 前沿：随时有效的推断，2023–2026',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {
    "Part four. Martingales and measure.":
        "第4部分。鞅与测度。第一幕问的是：价格是不是一场公平博弈。这一幕搭建让这个问题变得精确的数学，而它的第一件工具，是赌博中最古老的想法：公平的赌注"
        "。",

    "Here is a historical betting score using yesterday's sign and transformed American market ":
        "这是一个历史下注分数，用昨天的收益符号和经过变换的美国市场收益来计算。<bookmark mark='a'/>正确校准的非负检验鞅，曾经达到二十"
        '的概率至多为百分之五。这里的分数使用估计的中心、截尾结果和事后初始化的尺度；第十五章会解释这些选择为什么重要。它在一九二九年二月越过二十，后来达'
        "到大约十的一百次方。<bookmark mark='b'/>让同一位下注者从二零零零年开始，分数四处游荡，却从未达到二十。<bookmark m"
        "ark='c'/>这个反差引出以下注来检验。到本部分结束，你会知道随时有效的保证何时成立，以及为什么历史分数本身还不够。",

    'In the House, this part adds a monitor to the data desk':
        '在我们公司，本部分为数据台增加一个监视器：针对明确给出的有界结果模型构建e过程；原假设正确校准时，它能控制长期监测中的误报。<bookmark '
        "mark='a'/>研究台开始同时检验上百个想法时，会继承这件工具。",

    "Probability in finance is about information":
        "金融中的概率，讲的是信息：你知道什么，什么时候知道。把硬币掷三次。有八个可能的世界，X数出每个世界里正面的个数。<bookmark mark='"
        "a'/>掷币之前你无法区分这些世界：它们都在同一块里。你对X最好的猜测是它的平均值，一点五，在每个世界都一样。<bookmark mark='b"
        "'/>第一次掷币后，世界一分为二。如果是正面，最好的猜测是二；如果是反面，是一。<bookmark mark='c'/>第二次掷币后，四块，四个"
        "猜测。<bookmark mark='d'/>第三次之后，你确切知道X。<bookmark mark='e'/>这串不断细分的划分叫作σ代数流，"
        "也叫过滤：每个时刻你能回答的问题。而每一块上最好的猜测，也就是在你还无法区分的那些世界上取平均，就是给定你所知信息下X的条件期望。看着这个猜测："
        "它只在信息到来时变动，而平均来说它根本不动。",

    'A martingale is a process whose best forecast of tomorrow is today.':
        '鞅是一个明天的最佳预测等于今天的过程。它在每个时刻可知，绝对值有有限期望，而且下一步的条件期望等于当前值。这就是公平博弈的数学形式。<bookm'
        "ark mark='a'/>这个名称来自让·维尔一九三九年的博士论文，借自最著名的下注系统：每输一次就把注额加倍。约瑟夫·杜布读了维尔的工作，并"
        "建立了系统理论。<bookmark mark='b'/>例子包括公平博弈中的财富、随机游走的平方减去步数，以及上一章中任何可积变量随着信息到来而"
        '形成的条件期望：杜布鞅。',

    "Here is a Doob martingale you can watch.":
        "这是一个你能看着它走的杜布鞅。两位玩家把一枚公平硬币掷二十一次，正面出现十一次或更多就算正面赢。每掷一次，就根据到目前为止的结果，计算正面获胜的"
        "概率。<bookmark mark='a'/>每条线是一场比赛。每个预测都从50%出发，随每次掷币跳动，越接近终点跳得越猛，最后停在零或一。然而"
        "平均来说它从不移动：今天的预测是明天预测的平均。<bookmark mark='b'/>博彩市场的价格就是这样变动的；在合适的测度下，期权到期时"
        "处于实值的概率也是如此。",

    'Optional stopping solves the oldest problem in probability in one line.':
        '可选停止用一行解决一个古老问题。赌徒在公平的单位步长博弈中从a出发，到b或破产时停止。停止后的财富始终在零到b之间，而且退出几乎必然发生，因此可'
        "选停止适用。<bookmark mark='a'/>结束时财富不是b就是零。<bookmark mark='b'/>所以先到b的概率是a除以b。"
        "<bookmark mark='c'/>如果胜率为p、博弈有偏，棣莫弗的技巧是寻找另一个鞅：q除以p的财富次方。同样的论证给出一般公式。",

    'Here is what that formula means at a casino.':
        "看这个公式在赌场里意味着什么。从五十个单位开始，每次押一，试图达到一百。公平博弈中的成功概率为一半，是一条直线。<bookmark mark='"
        "a'/>欧式轮盘押红，三十七次里平均赢十八次，对你的优势差只有三十七分之一，但翻倍的概率已经降到约百分之六。美式轮盘多一个零，概率只剩大约千分之"
        '五。小额下注让本金反复暴露于劣势；这里失败很可能发生，但并非确定。',

    'Compare ways to reach twice a starting bankroll before ruin, without a deadline or table l':
        '比较没有截止时刻和桌面限额时，在破产之前把本金翻倍的方法。从一百个单位出发，每次押一，成功概率不到百分之零点五；从五百个单位出发，大约只有五千亿'
        "分之一。赌场优势有更多次机会起作用。<bookmark mark='a'/>一次把本金押在红色上，成功概率是三十七分之十八，接近百分之四十九。<"
        "bookmark mark='b'/>杜宾斯与萨维奇在一九六五年证明：在经典的劣势、等额赔率和可自由分割注额的模型中，大胆下注最适合在破产前达到"
        '目标这一目的。最大化期望对数增长是另一个目的，第八部分研究凯利准则。',

    'In February 1995 escalating derivatives exposures and concealed losses broke a bank. Barin':
        '一九九五年二月，不断加大的衍生品敞口和被隐瞒的亏损拖垮了一家银行。成立于一七六二年的巴林银行，因为新加坡的一位交易员尼克·里森亏损约八点三亿英镑'
        '而倒闭，损失超过银行资本的两倍。他把亏损藏在编号八八八八八的错误账户里，持续约两年半。荷兰的ING银行以一英镑买下剩余业务。里森在法兰克福被捕，'
        '在新加坡被判六年半监禁。',

    "Most processes are not martingales: prices drift.":
        "大多数过程不是鞅：价格有漂移。杜布证明，任何均值有限的过程都能以唯一的方式分解为一个可预测部分和一个鞅。可预测部分一步一步地累加在前一步已知信息"
        "下的期望变化。剩下的就是一场公平博弈。<bookmark mark='a'/>取一枚55%落正面的硬币，正面向上走一步，反面向下走一步。<boo"
        "kmark mark='b'/>它的期望步长是十分之一，所以可预测部分是一条斜率为十分之一的直线。<bookmark mark='c'/>游走减"
        "去这条直线就是一个鞅：全部的意外，没有任何漂移。",

    'f"Now the market. Here is the logarithm of a dollar':
        "现在看市场。这是一九二六年把一美元投进美国股市、分红再投资之后的财富对数。<bookmark mark='a'/>用估计的漂移演示分解：前二百五"
        "十天做事后初始化，此后用不断扩大的样本均值预测。把这些预测累加起来。<bookmark mark='b'/>剩下的是预测残差。只有预测等于真实条"
        "件均值时，它才是鞅；这张图并没有建立该条件。<bookmark mark='c'/>到二零二零年，一美元变成约{np.exp(d['X_end'"
        ']):,.0f}美元。约九个对数点的增长中，这个选定的预测方法把七点多分给估计漂移，不到两点分给残差。这是代数归因，并不是已经识别出的技巧与运气'
        '的分界。',

    'For a square-integrable martingale, subtracting the sum of true conditional increment vari':
        "对于平方可积鞅，从其平方中减去真实条件增量方差的累计和，会得到另一个鞅。这里的市场例子使用估计残差。<bookmark mark='a'/>绿线"
        "累加EWMA方差预测，起初六十天采用事后初始化。<bookmark mark='b'/>其总数与实际平方残差接近，都是二点八九。总数相近只是数值"
        "比较，不能证明条件方差预测正确。<bookmark mark='c'/>第五部分建立伊藤微积分时，会区分可预测二次变差与实际二次变差。",

    'The same worlds can carry different probabilities.':
        '同一组世界可以有不同概率。掷三次硬币，在P下硬币公平，八个世界各有八分之一概率；在Q下正面概率为百分之六十，正面较多的世界权重更高。<bookm'
        "ark mark='a'/>逐个世界把Q的概率除以P，得到比值L，也就是Q相对于P的拉东–尼科迪姆导数。<bookmark mark='b'/>"
        'Q下的期望等于P下用L重新加权的期望。Q的概率和为一，所以L在P下的期望为一。第九部分会使用等价定价测度，使贴现后的可交易总收益过程成为鞅，前提'
        '是满足相应市场模型的假设。',

    "Now follow L as the tosses go on, say for three hundred.":
        "现在随着掷币继续，比如掷三百次，跟踪L。在公平硬币下，L是均值为一的鞅：我们构造它时就让它平均为一。<bookmark mark='a'/>可是"
        "看看这些路径。几乎全部都沉向零。三百次之后的中位数约为千分之二，三分之二的路径终点低于百分之一。均值之所以保持为一，只是因为少数几条路径一飞冲天"
        "，罕见到两千条模拟路径的平均都不到一半。非负鞅必然收敛，而这个鞅收敛到零。<bookmark mark='b'/>如果硬币真是那枚60%的硬币，"
        "同一个L会增长：三分之二的路径终点高于一百。<bookmark mark='c'/>把L看作一位赌徒的财富：他一次次押注硬币是Q。如果不是，他就"
        "在玩一场公平博弈，几乎必然破产；如果是，他就发财。这就是第15章以下注来检验背后的想法。",

    'Part one measured how heavy the tails of returns are.':
        '第一部分测量了收益尾部有多重。这里是曼德勃罗提出的分布族。独立同分布增量的标准化和，在方差有限时趋向高斯形状。保罗·列维问，什么形状能在相加后保'
        "留下来：独立副本之和仍是同样形状，只是更宽。<bookmark mark='a'/>答案是稳定分布族，参数alpha在零与二之间。alpha为二"
        "时是高斯；低于二时尾部按幂次衰减，慢到方差无穷大；对称的alpha等于一的成员是柯西分布。<bookmark mark='b'/>一九六三年曼德"
        '勃罗用约一点七拟合棉花价格；一九六五年法马对三十只道琼斯股票也得到低于二的alpha。若这些分布精确成立，方差就不是有限数值，经典的波动率定价设'
        '定也需要调整。',

    "Measure it. The House fits a stable law to daily returns":
        "测量一下。我们的公司用五个分位数为日收益拟合稳定分布，这是J.休斯顿·麦卡洛克1986年发表的方法，它不受最极端的日子影响。<bookmark "
        "mark='a'/>美国市场，逐个十年来看：alpha在一点四到一点六之间，从未接近二。整个样本是一点四。比特币更低：一点二七。<bookmar"
        "k mark='b'/>1995年，罗萨里奥·曼特尼亚和尤金·斯坦利在标普500的逐分钟数据中发现了同样的一点四。按这个指标，收益分布的中心部分"
        "形状像一个稳定分布。",

    "Ville's thesis contained a second idea, ignored for sixty years.":
        "维尔的论文里还有第二个想法，被忽视了六十年。如果一位赌徒的财富是从一开始的非负鞅，那么它在整个无限的未来中曾经达到二十的概率，最多是二十分之一。"
        "<bookmark mark='a'/>把这变成一个检验。把原假设表述为某场博弈是公平的。让一位赌徒对它下注，从不冒超过自己所有的风险。如果原假"
        "设为真，赌徒的财富就是一个非负鞅，一个e过程。<bookmark mark='b'/>当财富达到二十时拒绝原假设。由维尔不等式，无论你多常查看、"
        "无论你决定何时停止，你犯错的概率最多是5%。格伦·谢弗和弗拉基米尔·沃夫克在这个想法上重建了概率论，自2020年以来它已成为一个领域：随时有效的"
        "推断。",

    'f"Why does that matter? Because people look.':
        '这为什么重要？因为人会反复看。模拟两千个完全公平的博弈，每个两千五百步。从第二十步起，每天把已知方差的z统计量与正负一点九六比较，这是正态近似下'
        "名义百分之五的阈值；对硬币数据，有限样本中它只是正态近似。<bookmark mark='a'/>统计量游走并逐渐越界。百分之{100 * p["
        "'t_reject']:.0f}的公平博弈曾被判为不公平，只因为每天都检查。<bookmark mark='b'/>同样的路径上，e过程有百分之"
        "{100 * p['e_reject']:.1f}达到二十，低于百分之五，符合维尔的理论界。每天审查策略的研究员或风险委员会，需要考虑这种反复查"
        '看的性质。',

    'Back to the opening historical scores. The mixture bets on transformed, demeaned returns u':
        '回到开场的历史分数。混合下注者根据昨天的符号，对变换并去均值后的收益下注。估计中心和截尾定义了特定的原假设，起初六十天还用事后信息初始化尺度。因'
        "此，这些图没有证明原始收益鞅检验具有百分之五的误报校准。<bookmark mark='a'/>从一九二六年开始，三年内越过二十；从一九七五年开"
        "始，十五个月内越过。指数收益中的正序列相关，与第一部分的陈旧价格解释一致。<bookmark mark='b'/>从二零零零年开始则从未达到，二"
        "零一八年以来的比特币也没有。<bookmark mark='c'/>没有越界并不证明公平。精确的随时保证要求实际有界结果的条件均值为零，而且校准"
        '只用过去信息。偏斜的零均值收益在截尾后可能不再是零均值，检查这个条件也是有效检验的一部分。',

    "The House has its monitor.":
        "我们的公司有了它的监视器。<bookmark mark='a'/>接下来是第5部分：随机微积分。我们让掷币变得无限快，随机游走就变成了布朗运动，"
        "它有自己的微积分，建立在本部分遇到的二次变差之上。",

    "The question is older than the stock market.":
        "这个问题比股市还古老。1654年，有人问布莱兹·帕斯卡：一局提前中止的赌局，赌注该怎么分？先得三分者赢六十四枚皮斯托尔金币，A以二比一领先。<b"
        "ookmark mark='a'/>倒着推。如果A赢下一分，A拿走六十四。如果B赢，下一分定胜负，所以那个局面值三十二。<bookmark ma"
        "rk='b'/>两者平均，A应得四十八；如果是二比零，则是五十六。<bookmark mark='c'/>一局未完赌局的公平价值，是给定已发生之"
        "事时的期望收益：一个条件期望。一分一分算下来，这些价值构成一个鞅。",

    "From Pascal the idea runs through de Moivre":
        "从帕斯卡开始，这个想法经过棣莫弗的赌徒破产问题和巴舍利耶的公平价格。<bookmark mark='a'/>1933年科尔莫戈罗夫给概率论立下公"
        "理，1939年维尔为鞅命名，沃尔德发明了序贯检验，杜布写成了理论。<bookmark mark='b'/>萨缪尔森、哈里森和普利斯卡让价格成为鞅"
        "。<bookmark mark='c'/>巴林银行展示了加倍下注会对一家银行做什么；沙弗、沃夫克和拉姆达斯则把维尔的下注变成了随时有效的检验。",

    "The plan, in eighteen chapters:":
        "本部分共十八章：信息与投影；鞅，以及为什么没有系统能战胜它；停时、加倍下注与巴林银行；破产与收敛；杜布分解、测度变换与拉东–尼科迪姆；稳定分布；"
        "检验与学会下注；以及业界与前沿。",

    "Chapter one. Information: sigma-algebras and filtrations.":
        "第1章。信息：σ代数与过滤。",

    'Make that precise. A sigma-algebra contains the whole space and is closed under complement':
        '把它说精确。西格玛代数包含整个空间，并且对补集与可数并封闭。在这个有限例子里，问题可以用非、且、或来组合。掷完n次，能回答的事件正是各个分块的并'
        '；每块或者选入、或者不选，所以事件数是二的二的n次方次幂。还没掷时有两个，掷一次有四个，两次十六个，三次二百五十六个。<bookmark mar'
        "k='a'/>随机变量对这些信息可测，就是能根据这些信息算出它；在划分上，这意味着它在每一块内为常数。第一次的结果通过了：两块内部的柱子各自一样"
        "高。<bookmark mark='b'/>正面总数没有通过，因为同一块内部它仍会变化。每个时刻的取值都对当时信息可测的过程叫适应过程。价格适应"
        "市场信息，策略的财富也必须如此；但下一次掷币的注额必须在掷币之前就确定。<bookmark mark='c'/>检查一下：前两次正面数为偶数，是"
        'F一中的事件吗？不是，它需要第二次结果，属于F二。',

    "What about infinitely many tosses?":
        "无穷多次掷币怎么办？有一个技巧让它变得具体：把掷币序列写成零到一之间某个数的二进制数字，正面为一，反面为零。公平掷币就变成了区间上的长度。<bo"
        "okmark mark='a'/>真实世界就在这根条上的某处，那个金色的点，而你不知道在哪里。每次掷币都把包含它的那一块切成两半。<bookma"
        "rk mark='b'/>放大，继续掷：掷六次之后，你知道自己在六十四个细条中的哪一条，仅此而已。那一条就是你的信息，F6。<bookmark "
        "mark='c'/>1933年，安德烈·科尔莫戈罗夫把整个概率论建立在这幅图上：一个世界的集合，一个事件的σ代数，以及一个对可数多块可加的测度。"
        "第13章会再用这张网格来构造拉东–尼科迪姆导数。"
        "有了信息的定义，就可以问：给定这些信息，最佳预测是什么。下一章。",

    "Chapter two. Conditional expectation is a projection.":
        "第2章。条件期望是一种投影。",

    "What is the best forecast of tomorrow's return":
        '已知今天，怎样最好地预测明天收益？科尔莫戈罗夫的定义给出答案。对可积变量，Y是给定G的X的条件期望，当且仅当Y能由G计算，并在G的每个事件上与X'
        "有相同平均。<bookmark mark='a'/>在正概率分块上，就是逐块取加权平均。<bookmark mark='b'/>若变量平方可积，"
        "误差X减Y与每个平方可积、可由G计算的变量正交；由示性函数的等式推广到和与极限即可。<bookmark mark='c'/>把X到任意可计算Z的"
        "平方距离展开，交叉项消失，得到勾股恒等式，所以Y是均方意义下最近的预测。<bookmark mark='d'/>已知量可以提出条件期望，需满足有"
        "界或乘积可积的条件。<bookmark mark='e'/>先按更多信息条件化，再按较少信息条件化，等于直接按较少信息条件化：塔性质。<book"
        "mark mark='f'/>凸函数满足相应可积性时，预测值的凸函数不大于凸函数的预测值，这是詹森不等式；独立的信息不改变均值。",

    'f"Here is that Pythagoras theorem as a picture.':
        "这就是那个勾股定理的图像。三个世界，概率分别是二分之一、十分之三和五分之一；一个变量是一支箭头，每个坐标按其概率的平方根拉伸，于是长度就是均方根"
        "。<bookmark mark='a'/>如果你只能分辨世界是不是c，你能算出的东西构成一个平面。从X向它作垂线：垂足一点八七五、一点八七五、一"
        "，就是条件期望。<bookmark mark='b'/>把图转过来：确实是直角。<bookmark mark='c'/>什么都不知道时，你只能算"
        "出常数，那是一条直线。把垂足投影上去，或者把X直接投影上去：两者都落在{c['toy_mean']:.1f}。这就是塔性质的几何形式。",

    'f"Now the market. Let the information be one bit':
        '现在看市场。信息只用一个比特：昨天涨还是跌？在每个时期内，用事后的组内平均估计两个条件均值；这些并不是样本外预测。<bookmark mark='
        "'a'/>一九二六到七四年，上涨日之后为{e0['up']:.1f}个基点，下跌日之后为{e0['down']:.1f}。平均而言，符号延续。一"
        "九七五到九九年也类似，分别为{e1['up']:.1f}与{e1['down']:.1f}。<bookmark mark='b'/>二零零零年以"
        "来则转向：上涨日之后为{e2['up']:.1f}，下跌日之后为{e2['down']:.1f}。白线表示按二十天一块重抽样时的变化范围，{ve"
        'rdict}这是从投影角度观察开场的历史结构。',

    "the old continuation and the new reversal both":
        "过去的延续和现在的反转，在下跌日之后都明显离开了零。",

    "after down days the bands still reach zero":
        "下跌日之后的区间仍然触及零，所以反转只是迹象，并不确定。",

    'f"In the House this is five lines:':
        "在我们的公司里，这只有五行：在每一块上按概率加权平均X，再把每一块的平均赋给块里的每个世界。<bookmark mark='a'/>在三个世界上"
        "，它返回垂线的垂足；在2000年以来的市场上，以昨天的符号为划分，它返回我们刚才画出的两个数。第6部分的回归就是这同一个函数，配上更细的划分。<"
        "bookmark mark='b'/>那么，2000年以来，下跌日之后，今天收益最好的预测是涨、跌还是零？{('Up' if e2['down'"
        "] > 0 else 'Down')}，幅度为{abs(e2['down']):.1f}个基点。"
        "一个无法用过去改进的预测，正是公平博弈的定义。下一章：鞅。",

    "Chapter three. Martingales: Ville's fair games.":
        "第3章。鞅：维尔的公平博弈。",

    'Fair, unfavourable and favourable games have names.':
        '公平、不利与有利的博弈各有名称。若明天的条件期望至多等于今天，叫上鞅，例如赌场中赌徒的财富；若至少等于今天，叫下鞅。<bookmark mark'
        "='a'/>三个例子，各用一行证明。公平游走下一步的平方展开后，交叉项均值为零，新一步的平方为一，所以游走平方减去步数是鞅。<bookmark "
        "mark='b'/>theta乘游走的指数，每步期望乘以theta的双曲余弦，也就是正负一步的矩母函数；除掉这个因子便得到指数鞅，第五章会用它计"
        "算等待时间。<bookmark mark='c'/>可积变量随着信息细化而形成的预测，由塔性质构成鞅。<bookmark mark='d'/>詹"
        '森不等式把鞅的凸函数变成下鞅，前提是变换后的取值仍然可积。',

    'f"That last fact has a price.':
        "最后一个事实有价格含义。执行价为二的游走看涨收益是凸函数，所以其期望随时间不减。<bookmark mark='a'/>看它在五十步时增长到{c"
        'all[-1]:.2f}，模拟路径落在精确曲线附近。这里比较的是同一个鞅、固定执行价，而且没有贴现。市场看涨期权的期限比较还需要一致的远期价格与'
        "贴现因子。<bookmark mark='b'/>游走的绝对值是鞅吗？不是，是下鞅；其均值按根号二n除以圆周率的速度增长，五十步时为{absm["
        "-1]:.2f}。<bookmark mark='c'/>马尔可夫不等于鞅：前者讲记忆，后者讲条件均值。硬币若公平，巧妙的下注系统能把它变成有利"
        '博弈吗？下一章。',

    "Chapter four. You can't beat the system.":
        "第4章。你赢不了这个系统。",

    "A betting system decides each stake from what has happened":
        "下注系统根据已经发生的事决定每一注的大小。把注额记作H。赌徒的财富是注额乘以每一步之和：鞅变换。规则只有一条：注额必须在看到这一步之前定下。<b"
        "ookmark mark='a'/>于是，把已知的提出来，下一步的期望收益等于注额乘以下一步的期望，而那是零。鞅的变换仍是鞅：没有任何系统能把公"
        "平博弈变成有利的博弈。<bookmark mark='b'/>在轮盘上，押红色的每一单位平均损失三十七分之一，所以每个系统都损失其总注额的三十七"
        "分之一：每单位同样的税。<bookmark mark='c'/>一个能在看到结果后再下注的作弊者每一局都会赢。整个定理就在“之前”这两个字上。",

    "Here is the rule as a machine.":
        "把这条规则做成一台机器。十二次公平掷币扣在幕布后面，每一次之前，加倍下注系统先定下注额。<bookmark mark='a'/>然后才翻开牌，财"
        "富随之上下一步。<bookmark mark='b'/>每一步都是事先知道的注额乘以一枚公平硬币，而公平硬币平均下来会抵消。",

    "Now six famous systems on European roulette":
        "现在看欧式轮盘上六个著名的系统，都押红色。平注。加倍下注。达朗贝尔：输了加一单位，赢了减一单位。拉布歇尔：在一行写好的数字里划掉数字。斐波那契。"
        "还有奥斯卡磨法：每一轮只求赢一单位。<bookmark mark='a'/>每个小图玩一局两百转，下面的数字是两万局累计的损失除以总注额。这些路"
        "径看起来千差万别：稳定的漂移、长时间的攀升、突然的悬崖。<bookmark mark='b'/>而那些数字都落在同一个值上：负的三十七分之一，所"
        "下注额的百分之二点七。",

    'f"The ledger. The systems differ':
        "账本。这些系统的区别在于下注多少，以及结果的形状。加倍下注和斐波那契赢下大多数场次，代价是罕见的巨额亏损：它们的偏度强烈为负。<bookmark"
        " mark='a'/>但把损失除以总注额，{verdict}，{fair}<bookmark mark='b'/>那么，拉布歇尔和平注，哪个按每"
        "单位注额输得更多？都不是。拉布歇尔下注多得多，所以总共输得更多，同时赢的场次也更多：大多数夜晚是愉快的，代价由其余的夜晚支付。",

    "every ratio is within two standard errors":
        "每个比率都在负三十七分之一的两个标准误之内",

    "most ratios sit within two standard errors":
        "大多数比率在负三十七分之一的两个标准误之内；尾部很重的那些需要更多局数",

    "and on a fair coin every mean is within":
        "而在公平硬币上，每个均值都在零的两个标准误之内。",

    "and on a fair coin the means scatter":
        "而在公平硬币上，均值散布在零附近。",

    "In the House the transform is one line":
        "在我们的公司里，鞅变换只有一行，每个系统都是一个从过去结果到下一注额的函数。<bookmark mark='a'/>在那十二次掷币上，它重现了幕"
        "布后的过程。第16章会把这一行变成一个检验。"
        "改变赌注不行。那选择何时停手呢？",

    "Chapter five. Stopping times, and the walk that always wins.":
        "第5章。停时，以及永远会赢的随机游走。",

    "Optional stopping needs a precise notion of when to stop.":
        "可选停止需要一个关于何时停止的精确概念。停时是这样一条规则：只用到目前为止发生的事，决定现在是否停止。<bookmark mark='a'/>一"
        "个公平随机游走朝着一道遮住未来的幕布前进。规则A在游走第一次到达正一时敲钟，就在它发生的那一刻。<bookmark mark='b'/>规则B在"
        "前一百步的最高点敲钟。拉开幕布：要知道这是最高点，它需要整条未来的路径。<bookmark mark='c'/>规则B不是停时。第一次击中目标、"
        "一个固定日期、财富第一次翻倍：允许。最高点、最后一次回到零、崩盘的前一天：禁止，无论多么诱人。",

    "Two facts, with proofs. First, stopping a martingale":
        "两个事实，附证明。第一，停止一个鞅，它仍是鞅：停止后的游走就是第4章的变换，注额在停时之前为一，之后为零。<bookmark mark='a'/"
        ">在第k步是否还在玩，由第k减一步决定，所以注额是可预测的。<bookmark mark='b'/>第二，一个悖论。设τ是公平随机游走第一次到达"
        "正一的时刻。由反射原理，走了n步还没到达的概率，等于游走停在零或一的概率，约为根号下二除以πn。<bookmark mark='c'/>所以它以"
        "概率一到达，但这些概率下降得太慢，期望时间是无穷大。<bookmark mark='d'/>沃尔德恒等式一行就能证明：如果期望时间有限，期望位置"
        "就是零，可τ时刻的位置是一。<bookmark mark='e'/>停止指数鞅，通过母函数得到τ的完整分布，它在一处的斜率，也就是均值，是无穷大"
        "。",

    'f"Here are {k_show} walks':
        "这是{k_show}条随机游走，每条在第一次到达正一的那一刻用一个金点冻结。<bookmark mark='a'/>计数器一开始升得快，后来越来"
        "越慢：有些游走在零以下游荡得很深，要很久才回来。<bookmark mark='b'/>在对数坐标上，仍在等待的概率落在斜率为负二分之一的直线上"
        "：一万条游走，跟踪到十万步，落在精确曲线上。<bookmark mark='c'/>而平均等待时间永远不会稳定。截断在一百步时是{cap['10"
        "0']:.0f}；一千步，{cap['1000']:.0f}；一万步，{cap['10000']:.0f}；十万步，{cap['100000']"
        ":.0f}。它按截断长度的平方根增长，没有上限。<bookmark mark='d'/>那么，公平地走一百步之后，还有多大比例从未领先过一？约{"
        "100 * f['p100_exact']:.0f}%。永远会赢的随机游走，能让你等得比任何本金都久。"
        "那么，停手到底在什么情况下帮不上忙？下一章：定理及其证明。",

    "Chapter six. Optional stopping, proved.":
        "第6章。可选停止定理的证明。",

    "Now the theorem, with its proof.":
        "现在是定理和它的证明。一个鞅在有限停时停止后保持初始均值，条件是：在某个固定日期之前停止；或者停止后的过程有界；或者期望时间有限且每一步有界。<"
        "bookmark mark='a'/>证明只有四行。对每个固定的n，停止后的鞅均值为M0：第5章。<bookmark mark='b'/>n增大"
        "时，停止后的路径冻结在τ时刻的值。<bookmark mark='c'/>每个假设都给出整条停止路径的一个可积上界：一个常数，或者起点加上c乘以"
        "τ。<bookmark mark='d'/>于是控制收敛定理让极限移进期望。<bookmark mark='e'/>没有界就会失败：在正一处停止"
        "的游走，在每个有限的n上均值为零，但在τ时刻总是一。一致可积性说的是没有质量逃逸到无穷远。这里却逃逸了。",

    'Watch the mass escape.':
        '看质量怎样逃走。这是一万条停止游走在第n步的位置。金色尖峰在正一，表示已经赢的路径，红色是仍未获胜的其余路径。支点标出均值。<bookmark '
        "mark='a'/>随着n变大，金色尖峰吸收几乎全部质量，一条稀薄的红色尾巴则向更左边延伸。总体均值始终为零，屏幕上的样本均值会波动。最左侧箱子"
        "保留视野外的尾部，读数使用没有截尾的位置。<bookmark mark='b'/>几乎必然的极限位置为一，其期望也是一；取极限前，每个期望却都为"
        '零。极限与期望不能交换，就是一致可积性失效，也是加倍下注钻的空子。',

    "Optional stopping also computes, by Bob Li's trick":
        '可选停止还能计算，方法来自李硕彦一九八零年的技巧。多久出现两个连续正面？每次掷币前，一个新赌徒拿一美元按公平赔率押正面，赢了就把钱再押一次。<b'
        "ookmark mark='a'/>正正第一次出现时，第四个赌徒有四美元，第五个有两美元。<bookmark mark='b'/>独立的两次掷币"
        '块以四分之一概率出现正正，因此等待时间有几何尾，期望有限。现在才能用有界步长的可选停止，把赌场每次收一美元的总收入与六美元支出相平衡：平均等待六'
        '次。',

    'f"In general, the same argument gives a formula':
        "一般地，同样的论证给出任意图案的公式：对每个使图案的前k个字母等于后k个字母的k，把m的k次方加起来。<bookmark mark='a'/>正"
        "正：二加四，六。正反：只有整个图案与自身重叠，四。正反正：十。三个正面：十四。二十万条模拟序列在抽样误差内吻合。一只猴子在二十六键打字机上打出A"
        "BRACADABRA，平均需要约{abra:.2f}千万亿次击键，这是威廉姆斯书中的一道习题。<bookmark mark='b'/>重叠也决定"
        "了彭尼游戏：如果你选正正反、我选反正正，我有{100 * pt['penney_exact']:.0f}%的时间获胜。<bookmark mar"
        "k='c'/>那么正正和正反，哪个出现得更晚？正正，六对四，尽管在任意两次掷币中两者概率相同：正正与自身重叠，所以它的差一点会浪费时间。"
        "定理需要条件。下一章：打破这些条件的策略——加倍下注。",

    "Chapter seven. Doubling, and admissible strategies.":
        "第7章。加倍下注与容许策略。",

    "The doubling system is the original martingale:":
        "加倍下注系统就是最初的“鞅”：押一单位，每输一次把注额加倍，直到第一次赢。只要信用无限，你会在第一次赢时停下，平均两次掷币，总是恰好领先一单位。"
        "<bookmark mark='a'/>定理并没有被打破。注额一、二、四、八无限增长，赢之前背负的亏损也是，所以三个条件一个都不成立。<book"
        "mark mark='b'/>给赌徒一笔真实的本金，一千零二十三单位，够加倍十次。现在一千零二十四局中有一千零二十三局赢一单位，有一局输光。期望"
        "收益恰好为零。<bookmark mark='c'/>每一局以一千零二十四分之一的概率破产，所以等到第一次破产的局数服从几何分布，均值一千零二十"
        "四局，一路赢来的单位一次全部输掉。",

    'f"Watch a thousand doublers':
        "看一千位加倍下注者，每人本金一千零二十三，输光就补满。画出其中八十位。<bookmark mark='a'/>金色的阶梯每局爬升一单位。然后在随"
        "机的时刻，一条变成红色的悬崖，直落一千零二十三单位。中位数下注者很长时间里都爬得很开心；均值始终在零附近，因为悬崖为每一级台阶买了单。<book"
        "mark mark='b'/>三千局之后，{100 * d['frac_ruined']:.0f}%的人至少破产过一次，与公式一致，平均结果是{"
        "d['mean_end']:+.0f}，在抽样误差内为零。<bookmark mark='c'/>本金一千零二十三，平均要多少局才第一次破产？平"
        "均一千零二十四局；模拟结果为{d['first_ruin_mean']:,.0f}。",

    'In idealized continuous-time models allowing infinitely many bets before a deadline, unlim':
        '在理想化的连续时间模型里，如果允许截止时刻前无限多次下注，无限信用就容许加倍构造。金融限制容许策略：贴现财富不能低于某个固定下界。<bookma'
        "rk mark='a'/>哈里森与普利斯卡在一九八一年说明，在等价鞅测度下，满足相应条件的容许财富过程是上鞅，不能无本获利。<bookmark "
        "mark='b'/>迪布维格与黄在一九八八年研究了这种信用下界如何排除加倍下注，证明放在第九部分。<bookmark mark='c'/>记住阶"
        '梯与悬崖的形状：卖期权经常收小额权利金，偶尔付大额损失。有位交易员用银行的钱不断增加风险，下一章看巴林。',

    "Chapter eight. Doubling down: Barings, 1995.":
        "第8章。加倍下注：巴林银行，1995。",

    'f"Here is the Nikkei through those months.':
        "这是那些月份的日经指数。里森持有日经期货多头，也卖出了在指数平静时带来收入的期权。<bookmark mark='a'/>一月十七日，神户发生地"
        "震。一周内指数下跌百分之{abs(week):.0f}。<bookmark mark='b'/>为了追回亏损，里森继续增加敞口。这与加倍下注相似"
        "，但他的实际期货与期权组合，并不是下面展示的二元下注规则。<bookmark mark='c'/>二月二十六日巴林倒闭，第二天日经又跌了一次。",

    "f\"We do not have Leeson's book":
        "我们没有里森的账簿，所以这里用一个示意代替，并明确标注：在真实指数上运行一条简单的加倍规则。持有一单位日经指数；每个下跌日之后加倍；账户一回到高"
        "点，就回到一单位。对照的是一家资本给定的银行。<bookmark mark='a'/>整个秋天，这条规则一次又一次地赢小钱。<bookmark "
        "mark='b'/>然后是神户。头寸日复一日地加倍，直到{D['max_units']:.0f}单位，并且{crossed}<bookmark "
        "mark='c'/>{story}<bookmark mark='d'/>{capped}",

    "The same rule capped at sixteen units never recovers":
        "同样的规则若上限为十六单位，就再也没能恢复：有界的注额服从可选停止，没有翻本的保证。",

    "The same rule capped at sixteen units also recovered":
        "同样的规则若上限为十六单位，也恢复了：在这个短窗口里，运气站在它这边。",

    "f'the account crosses the capital line":
        "账户在神户地震后{_days_after_kobe(cross)}天越过了资本线。",

    "the account never crosses the capital line.":
        "账户从未越过资本线。",

    'f"A doubler with unlimited credit would':
        "在这次重演中，一个信用无限的加倍下注者会在低点之后{k_back}个交易日回到零以上，这正是没人阻止时加倍下注系统所承诺的。但银行的资本线先被越"
        "过了。",

    "Even with unlimited credit, the doubler had not":
        "即使信用无限，加倍下注者到3月底也没有赢回来。",

    "So the lesson is not that optional stopping failed.":
        "所以教训不是可选停止失效了。银行的控制措施，就是为了让它的假设成立。<bookmark mark='a'/>头寸限额让注额有界。只对已申报的头寸"
        "提供保证金融资，让本金有界。把做交易的人和结算交易的人分开，让亏损看得见。<bookmark mark='b'/>在新加坡，里森同时管着交易和后"
        "台。调查报告的摘要说得很直白：明确的职责分离是任何有效控制体系的根本。"
        "里森的上限是银行的资本。每个赌徒都有上限。下一章：破产的算术。",

    "Chapter nine. Gambler's ruin, and bold play.":
        "第9章。赌徒破产与大胆下注。",

    'f"How long does it take?':
        "要多久？用第3章的另一个鞅，游走的平方减去步数，从零出发，两道边界分别在负a和b减a。它在结束时的期望值为零。<bookmark mark='a"
        "'/>游走最终停在某一道边界上，概率就是我们刚才求出的。<bookmark mark='b'/>所以期望下注次数是a乘以b减a：从五十出发，目标"
        "一百，两千五百次。<bookmark mark='c'/>六十局，到达一百变金色，输光变红色。{verdict}在欧式轮盘上，赌局结束得更早，只"
        "有{100 * R['frac_top']:.1f}%停在一百。"
        "有界的公平博弈总要在某处停下来。下一章：鞅为什么收敛。",

    "f'Four thousand simulated games average {F['mean']:,.0f}, within":
        "四千局模拟平均{F['mean']:,.0f}次，在公式的抽样误差之内。",

    "f'Four thousand simulated games average {F['mean']:,.0f}, a little":
        "四千局模拟平均{F['mean']:,.0f}次，与公式略有偏差：长局很少见，却主导了平均值。",

    "Chapter ten. Martingales converge.":
        "第10章。鞅会收敛。",

    'Can a fair game wander forever without settling?':
        "公平博弈能永远游荡而不稳定吗？杜布用交易策略回答。画出从a到b的带，鞅低于a时买一单位，高于b时卖出。<bookmark mark='a'/>每"
        "次完整上穿至少赚b减a，损失只可能来自最后一笔尚未平仓的交易。<bookmark mark='b'/>注额由过去决定，所以交易者仍在玩公平博弈。"
        '若鞅的平均绝对大小还有统一界，就能约束期望上穿次数；没有这个额外条件，普通公平游走完全可以永远反复穿越。',

    "Written out, this is Doob's upcrossing lemma.":
        "写出来，这就是杜布上穿引理。交易者的财富至少是b减a乘以上穿次数，再减去未平仓交易的亏损。<bookmark mark='a'/>对上鞅，期望财"
        "富至多为零，所以期望上穿次数不超过低于a的期望缺口除以带宽。<bookmark mark='b'/>如果鞅的平均大小保持有界，每条端点为有理数的"
        "带子只被穿过有限次，所以路径不能振荡：它收敛。这就是杜布向前收敛定理。<bookmark mark='c'/>但收敛不等于保持均值：在第12章，"
        "一位公平赌徒的财富趋于零，而均值保持为一。一致可积性恰恰是保持均值的条件。",

    'f"The most famous convergent martingale is an urn.':
        "最著名的收敛鞅是一个罐子。开始时一个红球，一个蓝球。摸出一个，放回，再加一个同色的球。<bookmark mark='a'/>下一次抽取后红球的"
        "期望个数，恰好增加当前的红球比例，所以比例本身是一个鞅，界于零和一之间。它必然收敛。<bookmark mark='b'/>看一百个罐子。一开始"
        "它们上下跳动；然后各自冻结在自己的水平上。富者愈富，罐子永远记得最初的几次抽取。<bookmark mark='c'/>它们停在哪里？收集一万个"
        "罐子的极限，直方图是平的：极限在零和一之间均匀分布，习题里用归纳法证明了这一点。所以红球比例最终超过90%的概率是10%；模拟结果为{100 *"
        " p['p_above_09']:.1f}%。",

    'f"Lévy\'s upward theorem:':
        '列维向上定理说，不断细化信息的预测，会收敛到全部信息给出的预测，这就是学习。用一个工作高斯模型估计市场均值，这里代入EWMA方差，并事后用六十天'
        "数据初始化。它的可信区间不是对真实市场收益校准过的置信序列。<bookmark mark='a'/>模型区间大致按时间平方根的倒数缩窄：十年后约"
        "正负{100 * dp['half_1936']:.0f}个百分点，五十年后为{100 * dp['half_1976']:.1f}。<book"
        "mark mark='b'/>到二零二零年，估计年均收益为百分之{100 * dp['end_mean']:.1f}，区间半宽为{100 * d"
        "p['end_half']:.1f}个百分点。这段历史和模型说明默顿的提醒：估计漂移可能很慢。价格会有漂移，下一章看怎样把过程分成漂移与公平部分"
        '。',

    "Chapter eleven. Doob's decomposition.":
        "第11章。杜布分解。",

    "Why unique? The predictable part adds up":
        "为什么唯一？可预测部分把每一步的预测加起来，所以剩下的部分预测为零。<bookmark mark='a'/>两种分解之差既可预测又是鞅，而一个事"
        "先知道、预测为零的步长就是零。<bookmark mark='b'/>用在鞅的平方上，可预测部分就是条件方差之和，即尖括号过程。<bookmar"
        "k mark='c'/>但可预测部分是一个预测，而预测取决于你知道什么。",

    "A casino learned this in court.":
        "一家赌场在法庭上学到了这一课。2012年8月，菲尔·艾维在伦敦的Crockfords赌场玩百家乐，赢了七百七十多万英镑。押闲家的庄家优势是百分之"
        "一点二四。<bookmark mark='a'/>在赌场看来，一位每手都押闲家的玩家，可预测部分每手向下倾斜这么多。<bookmark mark"
        "='b'/>但艾维的搭档对牌做了分拣，在发牌前就知道了第一张牌的一些信息。根据这个信息选择押哪一边，同一个游戏的可预测部分每手向上倾斜约百分之六"
        "点五，这是高等法院认定的数字。<bookmark mark='c'/>牌没有变；变的是过滤。法院一直到2017年的最高法院都认定这是作弊，艾维没"
        "有拿到钱。<bookmark mark='d'/>所以漂移是你所知信息的属性。"
        "也取决于你使用的概率。下一章：改变概率，漂移就消失了。",

    "Chapter twelve. Change of measure.":
        "第12章。测度变换。",

    'Over time the change of measure is a process:':
        "随时间推进，测度变换成为一个过程：前n次掷币的似然比，是P下的杜布鞅。<bookmark mark='a'/>Q下的条件期望，是P下重新加权的条"
        "件期望，再除以当前的密度：贝叶斯公式。<bookmark mark='b'/>漂移发生改变：游走减去每步二q减一，是Q下的鞅，这是硬币上的吉尔萨"
        "诺夫。<bookmark mark='c'/>埃舍尔的方法按指数重新加权。匹配一项资产的期望总回报，只是单期演示，并不能证明所有可交易资产都满足"
        '所需的条件期望关系。',

    'Here is the picture to keep.':
        "记住这个画面。两百条硬币游走在公平硬币下生成，每条路径起初同样可能。<bookmark mark='a'/>改用正面概率百分之六十的测度，没有一"
        "条路径移动，只按似然比改变线条粗细：正面多的路径变粗，反面多的路径变淡。<bookmark mark='b'/>扇形的可见中心向上移动，终点分布"
        '也随之变化。有限期限内的等价测度只是重新加权路径，并且双向保持零测集。只有单向绝对连续时，不能推出这种双向保持。',

    'f"Build one illustrative Q on historical days. Fit an exponential tilt in sample so expect':
        '在历史交易日上构造一个示意性的Q。用全样本拟合指数倾斜，使市场的期望总回报等于样本中的无风险回报目标。这并没有识别唯一的定价测度，也不是动态定价'
        "模型。<bookmark mark='a'/>theta为{es['theta']:.2f}，Q偏向较差的交易日。平均日对数收益从{es['me"
        "an_p']:.2f}个基点降到{es['mean_q']:.2f}。<bookmark mark='b'/>权重移到了左尾：最差百分之一的交易"
        "日占Q权重的百分之{100 * es['tail_q']:.2f}。<bookmark mark='c'/>坏日子在这个选定的倾斜下获得更多权重"
        '；这既不改变真实崩盘概率，也没有识别市场风险溢价。测度变换能走多远？下一章：拉东–尼科迪姆定理，以及它的边界。',

    "Chapter thirteen. Radon-Nikodym, and the singular infinite.":
        "第13章。拉东–尼科迪姆，以及奇异的无穷。",

    'When can one probability be written as another':
        '何时能把一种概率写成另一种概率的重新加权？拉东–尼科迪姆定理说，只要Q不给P认为不可能的事件赋正概率，就存在相对于P的密度。<bookmark '
        "mark='a'/>鞅可以证明它。在第一章的二进分块上，取Q质量与P质量之比。子块分担父块的Q质量，所以这个比值是P下的鞅。<bookmark "
        "mark='b'/>它非负，因此收敛；绝对连续又使它一致可积，极限就是密度。<bookmark mark='c'/>双向绝对连续叫等价：两者零测"
        "集相同，因此对同一个自融资策略是否构成套利，它们给出相同判断。<bookmark mark='d'/>对独立的硬币乘积测度，若每个坐标的概率都严"
        '格介于零与一之间，角谷二分法适用：亲和度乘积保持正值或趋于零，对应整体等价或相互奇异。',

    "Watch the density appear.":
        "看着密度出现。P把概率均匀地铺在一个正方形上；Q偏向远处的角落。在二乘二的网格上，每根柱子的高度是格子里Q的质量除以P的质量。<bookmark"
        " mark='a'/>把每个格子切成四个：四乘四，八乘八，十六乘十六。每根柱子变成四根，四根的平均等于父柱子：这就是鞅。柱子组成的城市平滑成一张"
        "曲面，拉东–尼科迪姆导数。<bookmark mark='b'/>现在试一个把全部质量放在对角线上的Q。P给对角线的面积为零，所以Q不是绝对连续"
        "的。对角线上的柱子每切一次就翻倍，其余的落到零，永远形不成曲面。Q和P是奇异的：每一个都活在另一个认为不可能的地方。",

    "f\"Kakutani's dichotomy, simulated.":
        "角谷二分法的模拟。在公平硬币下，跟踪60%硬币的似然比，掷一万次。<bookmark mark='a'/>它崩塌了：中位数接近十的{C['med"
        "ian_log10']:.0f}次方，正如每次零点零二的相对熵所预言。在每个有限时刻两枚硬币等价，但在无穷序列上它们是奇异的：强大数定律能确定地"
        "把它们区分开。<bookmark mark='b'/>现在让倾斜逐渐消失：第k次掷币正面概率为二分之一加零点二除以k。倾斜的平方和有限，亲和度的"
        "乘积保持为正，似然比稳定在一个正的极限上，均值为{F['mean_L']:.2f}。这两个测度永远等价。<bookmark mark='c'/>"
        "那么，一枚公平硬币和一枚50.1%的硬币，永远掷下去，是等价的吗？不是。这就是为什么在第5部分，吉尔萨诺夫只能在固定期限内改变布朗运动的漂移，也"
        "是为什么任何测度变换都改变不了它的波动率。"
        "测度变换重新加权了尾部。下一章：真实的尾部有多重。",

    "Chapter fourteen. Heavy tails, as stable laws.":
        "第14章。作为稳定分布的厚尾。",

    'f"For a symmetric, zero-location stable law, the sum of n independent copies is one copy s':
        "对于对称、零位置的稳定分布，n个独立副本之和等于一个副本拉伸n的alpha分之一次方。<bookmark mark='a'/>特征函数把和变成积"
        "；负的ct绝对值的alpha次方的指数，在取n次幂后等价于拉伸t，这就是对称稳定分布。<bookmark mark='b'/>取两次对数，alp"
        "ha就成为直线斜率，是库特鲁韦利斯的方法。<bookmark mark='c'/>先用中位数与四分位距标准化收益，再平均指数项。箭头只显示经验特"
        "征函数的模，不显示相位；这里逐日重抽样的自助法忽略了时间依赖。高斯对照给出{ga['alpha']:.2f}，美国市场给出{us['alpha'"
        ']:.2f}。{verdict}',

    "The two estimators agree, which is what":
        "两个估计量一致，这正是稳定分布应有的表现。",

    "The two estimators disagree:":
        "两个估计量不一致：中心的分位数说一点四，而权衡整个分布主体的特征函数给出更大的α。真正的稳定分布只会给出一个答案。",

    'f"A third estimator: a finite-budget likelihood search, with the stable density computed n':
        '第三个估计量是有限计算预算下的似然搜索，每个候选参数都数值计算稳定密度。看它学习：每次尝试新的alpha、beta、尺度和位置，从接近高斯的al'
        "pha二开始。<bookmark mark='a'/>右边是目前最好的拟合，左边是正在尝试的alpha，对应三个各一千五百天的随机样本。每个样本"
        "最多做一百五十次函数计算，并没有建立全局收敛。<bookmark mark='b'/>最后的alpha平均为{np.mean(a_):.2f}。"
        '{verdict}',

    "Maximum likelihood lands within the spread":
        "最大似然落在麦卡洛克答案的样本间离散范围之内。",

    "Maximum likelihood lands above McCulloch's":
        "最大似然高于麦卡洛克的答案，差距超过样本间的离散：倾听每一天的似然，比分位数更偏好较轻的尾部。",

    'f"A descriptive check: iid stable sums keep their standardized distribution. Below alpha t':
        '做一个描述性检查：独立同分布的稳定变量相加后保持标准化分布，但alpha低于二时，总体方差与四阶矩发散，标准化峰度没有定义。这张样本峰度图是描述'
        "性的，并非经过校准的稳定性检验。<bookmark mark='a'/>高斯对照接近零。市场单日峰度从{ku[0]:.0f}开始。{verdic"
        't}中心看起来像稳定分布，并不意味着尾部也稳定。变化的波动率也影响时间聚合，是第七与第十三部分的主题。厚尾让经典检验更脆弱，下一章介绍由公平博弈'
        '构成的随时有效检验。',

    'The sample kurtosis falls substantially. This suggests changing shape across horizons, but':
        '样本峰度明显下降，提示不同期限下的形状会改变，但不能据此证明总体方差有限。',

    "It falls only a little, which on its own":
        "它只下降了一点，单靠这一点无法下结论。",

    "Chapter fifteen. Ville's inequality, and testing by betting.":
        "第15章。维尔不等式与以下注来检验。",

    "The proof uses only what you have.":
        "证明只用到你已经有的东西。设τ是财富第一次达到c的时刻。<bookmark mark='a'/>在τ和n中较早的那个时刻停止：可选停止使均值至多"
        "为一，而在τ先到的事件上，财富至少是c。<bookmark mark='b'/>让n趋于无穷：维尔不等式。<bookmark mark='c'/"
        ">一次下注的收益，在原假设下均值至多为一，就是一个e值，由马尔可夫不等式成为一个检验。<bookmark mark='d'/>而重对数律说，公平"
        "游走的统计量会永无止境地反复越过一点九六：每天查看，你终将拒绝一个真实的原假设。",

    'Shafer and Vovk rebuilt probability as a game.':
        "沙弗与沃夫克把概率重建为一场游戏。<bookmark mark='a'/>预报者宣布价格，怀疑者在不冒超过自身资本风险的前提下下注，现实给出结果"
        "。<bookmark mark='b'/>资本大幅增长，是反对预报承诺的证据；明确的阈值控制误报。怀疑者仍需选择怎样下注，下一章就让它学习。",

    "Chapter sixteen. Learning to bet.":
        "第16章。学会下注。",

    "The House's monitor bets a fixed menu of stakes.":
        '我们公司的监视器使用固定注额菜单，下注者能否学会自己的注额？财富每步乘以一加注额乘结果，注额只依赖过去。在有界结果的条件均值为零的原假设下，这是'
        "非负鞅，维尔不等式允许这种学习规则。<bookmark mark='a'/>规则决定速度。小注额下的二阶近似把期望对数增长写成抛物线，若注额允许"
        "，峰值在优势除以二阶矩。<bookmark mark='b'/>对平稳的小优势，用ln二十除以近似增长率，日夏普零点零五时约需两千四百天。这是知"
        "道真实优势的预言者的增长率估计，实际首次越界时间是随机的。<bookmark mark='c'/>真实下注者在线学习，这里对对数财富使用在线牛顿"
        "步。<bookmark mark='d'/>置信序列则假设有界观测共享一个条件均值；两个单侧下注者各分得一半误差预算，并保留所有过去的约束。数值"
        '网格的交点向外取整，因此也覆盖网格之间的均值。',

    'f"Watch one learner.':
        "看一个学习者。一个真实日夏普比率为零点零五的策略，模拟一万天。左边，下注者的注额是表盘上的指针，凯利比例用金色标出；右边是它的对数财富，以及二十"
        "那条线。<bookmark mark='a'/>一开始指针剧烈摆动：下注者一无所知。然后它稳定在金色标记附近，财富开始攀升。{crossing}",

    "f'It crosses twenty on day":
        "它在第{cross:,}天越过二十，而一位从一开始就知道优势的下注者大约需要{l['theory_days']:,.0f}天。",

    "It has not reached twenty within ten thousand days.":
        "一万天之内它没有达到二十。",

    'f"Now a fair race.':
        '现在公平竞赛：固定菜单、在线牛顿学习者、用滚动优势估计的aGRAPA，以及知道真实优势的预言者。四种策略，从无优势到日夏普零点一；八个种子各一百'
        "次运行，柱线给出种子间的最小和最大值。<bookmark mark='a'/>没有优势时，每位下注者标记的比例约不超过百分之五，{promise"
        "}<bookmark mark='b'/>在这次模拟中，预言者最快；日夏普零点零五时，各种子首次标记时间中位数的平均为{med['kelly']"
        ':,.0f}天。{verdict}',

    "At a Sharpe of point zero five the learner beats":
        "在日夏普零点零五时，学习者胜过了我们公司的固定菜单。",

    'At a Sharpe of point zero five, the surprise:':
        '日夏普零点零五时，一个意外是固定注额菜单比学习者更快。小优势给学习者的信号很弱，而菜单里已经有接近合适水平的注额。这个实验并没有建立普遍适用的优'
        '劣排序。',

    'f"Back to the hook\'s historical diagnostic, now with a learner on the same transformed out':
        "回到开场的历史诊断，这次让学习者处理同样的变换结果。第十五章关于校准的限制仍然适用。<bookmark mark='a'/>{timing}<b"
        "ookmark mark='b'/>{late_txt}<bookmark mark='c'/>{verdict}",

    "Since 2000, and on Bitcoin since 2018, neither":
        "2000年以来，以及2018年以来的比特币上，两位下注者都从未做到。",

    "Since 2000 or on Bitcoin, at least one":
        "2000年以来或在比特币上，至少有一位下注者越过了。",

    "f'Started in July 1926, the menu crosses":
        "从1926年7月开始，菜单在{y['19260701'][0]:.1f}年后越过二十，学习者在{y['19260701'][1]:.1f}年后。"
        "从1975年开始，分别在{y['19750101'][0]:.1f}年和{y['19750101'][1]:.1f}年后。",

    "The old market's bets do not always reach twenty.":
        "旧市场上的下注并不总能达到二十。",

    'The two historical scores have the same crossing pattern in these windows.':
        '在这些历史窗口中，两种分数的越界模式相同。',

    'The historical crossing pattern depends on the bettor in at least one window.':
        '至少一个窗口中的历史越界模式取决于所选下注者。',

    'f"And the corrected confidence sequence. Clip daily log returns to minus point two through':
        '现在看修正后的置信序列。把日对数收益截在负零点二到正零点二之间，假设这些有界观测共享一个条件均值。在这个模型下，可预测的单侧下注在所有时刻同时给'
        "出百分之九十五覆盖率，数值网格的边界向外取整。这并没有证明比特币符合共同条件均值假设。<bookmark mark='a'/>早期很宽的区间，在"
        "图中裁切到正负一百五十个基点。到二零二零年底，区间从每日{cs['end'][0]:.0f}到{cs['end'][1]:.0f}个基点。{ve"
        'rdict}',

    'It includes zero, so this construction does not reject zero under the stated model.':
        '区间包含零，因此这个构造在所述模型下没有拒绝零均值。',

    'f"In the House the learner is ten lines':
        "我们公司的学习者只有十行代码。误报保证需要有界结果、只用过去信息的注额，以及正确指定的条件均值原假设。<bookmark mark='a'/>在"
        "模拟策略上，注额稳定在{l['lam_end']:.2f}附近。<bookmark mark='b'/>试验计数器为{env['trials']"
        '}，第五条规则增加一句：注额可以学习。修正后的置信序列单独登记，旧记录保留，也没有打开任何封存的留出样本。接下来看看靠这些想法工作的赌场、庄家、'
        '市场与检验平台。',

    "Chapter seventeen. The house, the book, and the market.":
        "第17章。赌场、庄家与市场。",

    'f"A casino is a portfolio of martingales':
        "赌场是带有有利漂移的博弈组合。<bookmark mark='a'/>内华达大学的数据说，二零二四年轮盘桌保留了换筹金额的百分之十七点三四。<b"
        "ookmark mark='b'/>而双零轮盘的单次优势为百分之五点二六。若用这个恒定优势作近似，留存率除以优势，隐含投注额与换筹金额的比值约为"
        "{ca['turnover']:.1f}；这不是实际下注次数的直接统计。<bookmark mark='c'/>桌面限额约束注额，但可选停止还需"
        '要停止期限或可积性条件，只有限额并不够。',

    'f"How sure is the house in this fixed-unit model? Subtract the known drift. The centered o':
        '在这个固定单位下注的模型里，赌场有多稳？减去已知漂移，中心化结果的条件取值范围长度为二，所以适用霍夫丁–东和敬界。<bookmark mark='
        "'a'/>单零轮盘的等额赔率下注，一百次后赌场仍亏的概率约百分之{100 * rows[0]['exact']:.0f}，一万次后约百分之{10"
        "0 * r4['exact']:.2f}，十万次后极小。这个界比独立同分布的二项精确答案宽松；它需要条件范围有界和指定的条件漂移，不能只看注额限"
        "额。<bookmark mark='b'/>实际月留存率仍有约三个百分点的波动。若完全由等额下注运气造成，一个月就只能有大约{ca['need_"
        "even']:,.0f}次这种下注。不同注额、大客户和周转率都可能重要；这个简化计算并没有识别各因素的实际贡献。",

    "The house's enemies change the filtration.":
        "赌场的敌人会改变过滤。爱德华·索普在1962年证明，二十一点的牌靴是有记忆的，算牌者有时面对正的漂移。<bookmark mark='a'/>1"
        "982年，新泽西州最高法院在肯·乌斯顿案中裁定，算牌问题应由赌场管制委员会来规定，所以赌场不能自行把算牌者拒之门外。<bookmark mark"
        "='b'/>在英国，分拣牌边被认定为作弊。",

    'Bookmakers run the same business on sport.':
        '体育博彩庄家经营类似业务。二零一七年，考尼茨、钟与克莱纳用多家庄家的共识赔率估计概率，在某家的报价显得有利时下注。五万六千多笔回测下注获得约百分'
        "之三点五回报，真实资金也获利，直到庄家开始用他们的话说，严重限制账户。<bookmark mark='a'/>Flutter披露，二零二四年美国"
        "体育博彩业务在约五百一十亿美元投注额中获得百分之七点九的净收入比例。<bookmark mark='b'/>比尔·本特的赛马团队把模型与公众赔率"
        '结合，据彭博商业周刊报道，累计赢得接近十亿美元。',

    'f"Prediction markets trade contracts paying a dollar if an event happens. Their prices are':
        '预测市场交易事件发生时支付一美元的合约，价格常被读作概率，但风险溢价与交易摩擦可能使价格不同于信念。二零二四年，贾·科布法官认定，CFTC禁止K'
        'alshi国会控制权合约时超越了授权，上诉法院拒绝暂停该裁决。据The Block报道，Polymarket总统选举市场交易额接近三十七亿美元。'
        "<bookmark mark='a'/>这种价格是鞅吗？奥根布利克与拉宾把第十一章变成一个信念基准检验：一致的贝叶斯预测，其期望平方移动等于已消"
        "除的不确定性。<bookmark mark='b'/>第三章预测的比值为{b['bayes']:.2f}，符合模型；过度反应百分之三十的预测者给"
        "出{b['over']:.2f}。<bookmark mark='c'/>在一千一百万笔Betfair交易中，作者发现持续的过度移动。对于Kal"
        'shi，伯尔吉、邓与惠兰发现价格在临近结束时更精确，也存在偏好冷门的偏差，主动吃单者更明显。',

    'Testing while you watch is old, and now industrial.':
        "边看边检验由来已久，如今已经工业化。沃尔德在战争年代提出的序贯概率比检验，监测第十二章的似然比，证据足够就停止。<bookmark mark='"
        "a'/>Optimizely为不断查看的网站实验提供随时有效的p值；Netflix也用随时有效的检验，在新版本逐步发布时判断风险。<bookma"
        "rk mark='b'/>只要原假设与依赖结构设定合适，这种监测也可以用于策略衰减。实现和校准必须针对具体应用。最后看研究前沿。",

    "Chapter eighteen. The frontier:":
        "第18章。前沿：随时有效的推断，从2023年到2026年。",

    "Ville's idea is now a fast-moving field.":
        '维尔的想法已成为快速发展的领域。基础工作包括王若度与拉姆达斯二零二二年的e-BH，在任意依赖下用e值控制错误发现；二零二三年拉姆达斯、格伦瓦尔德'
        "、沃夫克与沙弗的综述描绘了全貌。<bookmark mark='a'/>鲁夫、拉尔松、库伦与拉姆达斯把维尔的定理推广到复合假设：在定理条件下，原"
        '假设类的零事件可由在其上发散的e过程刻画。沃德比–史密斯与拉姆达斯用下注估计均值，得到第十六章的置信序列；谢卡尔与拉姆达斯用下注检验两个分布是否'
        "相同。<bookmark mark='b'/>格伦瓦尔德、德海德与库伦的安全检验在二零二四年提交英国皇家统计学会讨论。格伦瓦尔德还研究了基于e值"
        "的事后决策保证；数据选择的显著性水平不能直接解释成普通、预先固定的第一类错误界。<bookmark mark='c'/>拉尔松、拉姆达斯与鲁夫把"
        '指定假设类下的对数最优e变量与计价单位组合联系起来；菲舍尔与拉姆达斯使置换检验随时有效，便于回测；二零二五年拉姆达斯与王把相关理论写成专著。',

    'That bridge deserves a picture. On simulated bounded outcomes, choose a fixed linear stake':
        "把这座桥画出来。对模拟的有界结果，在零到二分之一的固定线性注额网格上，最大化备择分布下估计的期望对数增长。<bookmark mark='a'/"
        ">这只是一个受限的凯利例子。<bookmark mark='b'/>在条件均值为零的原假设下，同一条财富路径也是有效检验。一般计价单位理论研究指"
        '定原假设与备择类中的对数最优e值；它并不保证在所有有限样本情形中都具有最高检验功效。',

    'f"Finally the frontier at work on a desk problem.':
        '最后把前沿用在交易台问题上。每天观察两百个策略，持续十年，其中二十个的真实日夏普为零点零八，其余没有优势。各自由学习e过程监测，交易台每二十一个'
        "交易日以百分之十水平审查一次e-BH。<bookmark mark='a'/>规则只需五行：把e值降序排列，找最大的k，使第k个仍达到策略总数除"
        "以alpha与k的乘积的阈值。<bookmark mark='b'/>左图是二十个种子的错误发现比例，右图是发现数。普通BH使用单侧、已知方差的"
        "z检验p值，发现更多、更快。<bookmark mark='c'/>假设每种方法在第一次有十个发现的审查时刻行动。在这二十个种子中，{verdi"
        "ct}到期限仍不行动的运行记错误发现比例为零。<bookmark mark='d'/>共同停时下的保证，要求每个e过程对联合过滤都有效。独立策略"
        '模拟满足这一条件，但数值平均本身并不是证明。',

    "e-BH's false discovery rate stays under":
        "e-BH的错误发现率保持在10%以下；BH的则远远超过。",

    "here both happen to stay near their target.":
        "这里两者恰好都停在目标附近。",

    "here even e-BH overshoots":
        "这里连e-BH也超出了，这是种子样本太少的警告。",

    'Part four in twelve lines.':
        '用十二句话回顾第四部分。西格玛代数是可回答的问题，条件期望是相应的信息投影。鞅对明天的预测等于今天。可预测注额不能把公平博弈变成有利博弈，轮盘对'
        '每种系统收取同样的单位下注劣势。可选停止需要停时与可积性条件，只有注额有界还不够。加倍下注依赖无界信用；金融中的容许性约束排除它，巴林的隐藏账户'
        '说明控制的重要。公平破产概率是a除以b，大胆下注解决经典劣势目标先于破产的模型。有界鞅会收敛。杜布把过程分成漂移与鞅，漂移取决于信息。测度变换移'
        '动权重，不移动路径；鞅也构造拉东–尼科迪姆导数。稳定分布诊断是证据，不是总体矩存在性的证明。正确校准的e过程允许学习注额，也允许反复查看。',

    'Five desk questions.':
        "五个交易台问题。鞅从一出发，到零或三时停止：到三的概率是三分之一，由可选停止得到。<bookmark mark='a'/>公平硬币直到两个连续正"
        "面，期望六次，由赌徒赌场方法算出。<bookmark mark='b'/>经典目标先于破产的模型中，欧式轮盘上一百美元争取二百美元，一次全押红色"
        "比每次押一美元有更高成功概率。<bookmark mark='c'/>彭尼游戏里，你选正正反，我选反正正，赢的概率是四分之三。<bookmark"
        " mark='d'/>公平游走首次领先一时停止，期望等待多久？无穷大：否则沃尔德恒等式会把终点的期望算成零，然而终点始终为一。",

    "And nine problems:":
        "还有九道习题：游走离开一条带子所需的时间，有偏博弈的破产概率，加倍下注系统的真实战绩，似然比为什么会崩塌，维尔不等式的证明，波利亚罐子的极限，"
        "沃尔德恒等式，以及两道资格考试水平的题：重对数律的上半部分，和罗宾斯的随时有效边界。中英文解答都在讲义里。",

    "Where this comes back:":
        "这些内容会在哪里再出现：二次变差在第5和第7部分；风险中性世界在第9、10和23部分；容许性在第9部分；日历价差在第12部分；计价单位组合在第8"
        "部分；厚尾在第7、13和40部分；e过程在第26部分和终章。",

    "The textbook chapters this part covers, and the papers it draws on; the notes":
        "本部分涵盖的教科书章节和所依据的论文；讲义把每个教科书小节对应到各章。每个数字都由本系列自己的代码算出：肯尼斯·弗伦奇1926年以来的日度市场数"
        "据、币安的比特币数据，以及圣路易斯联储的日经指数。",


    # ------------------------------------------------------------------ Research (the PhD layer)
    "For the researcher: Chapter 15 said a test checked forever":
        "写给研究者：第15章说，一个被永远检查下去的检验会拒绝一个真实的原假设。这里是说明公平游走能走多远的定理，以及一个随时有效的检验必须为此付出的代价。",

    "The theorem is Khinchin's, from 1924.":
        "这是辛钦一九二四年的定理。<bookmark mark='a'/>独立、公平、单位方差的增量之和，除以根号二t乘log log t，上极限几乎必"
        "然恰好为一。<bookmark mark='b'/>中心极限定理描述一个固定时刻，重对数律则描述所有时刻：任何略低于该尺度的包络都会被无穷多次越"
        '过，任何略高于该尺度的包络只会被有限多次越过。上极限本身没有决定是否反复越过恰好相等的包络。因为log log t无界增长，游走最终以概率一越过'
        '一点九六个标准差，或任何固定倍数。',

    'For Gaussian or one-sub-Gaussian steps, the upper half has a short martingale proof. The g':
        "对高斯或单位次高斯增量，上半部分有一个简短的鞅证明；一般有限方差结果还需要截断论证。<bookmark mark='a'/>对指数鞅使用杜布最大"
        "不等式，并选择最好的指数参数，得到运行最大值的高斯尾界。<bookmark mark='b'/>在theta的k次方这些几何时刻，使用略高于重对"
        "数尺度的边界。<bookmark mark='c'/>一个时间块内任意越界的概率，被k的一个幂控制。<bookmark mark='d'/>th"
        'eta足够接近一时，这些概率界可求和，由博雷尔–坎泰利，只有有限多个块会越界。匹配的下半部分使用块间独立增量与第二博雷尔–坎泰利引理。',

    'See it happen.':
        "看它发生。<bookmark mark='a'/>一千条高斯公平游走，从第一步起，每一步都和固定样本边界一点九六根号t比较；这里用高斯增量，而第"
        "十五章使用硬币增量。曾越界的比例继续上升。<bookmark mark='b'/>到十万步时，大约四分之三。重对数律说最终趋向一，但非常慢：十万"
        '处的log log t还不到二点五。',

    'How should a test look forever and stay honest?':
        "怎样永远查看而保持有效？赫伯特·罗宾斯在一九七零年给出了答案。<bookmark mark='a'/>对于高斯原假设下的增量，lambda S减"
        "去lambda平方t除以二的指数，是均值为一的鞅；条件单位次高斯增量则给出上鞅，因此仍有相同的概率界。<bookmark mark='b'/>对"
        "lambda按正态分布混合，混合仍保持相应的鞅或上鞅性质，配方即可算出积分。<bookmark mark='c'/>维尔不等式把它曾达到alph"
        "a分之一的概率控制在alpha以内。<bookmark mark='d'/>对游走求解，得到在全部时刻同时有效的边界，按根号t log t增长，"
        '比重对数尺度更快。',

    'Now the same thousand walks against the always-valid boundaries.':
        "现在让同样的一千条游走面对随时有效的边界。<bookmark mark='a'/>一条是罗宾斯混合边界；另一条按几何时间块分配误差预算，再把指数"
        "界拼接起来，来自霍华德、拉姆达斯、麦考利夫与塞孔二零二一年的构造。<bookmark mark='b'/>在十万步内，大约百分之五的路径越过混合"
        '边界，与一千条路径的抽样误差相容；越过拼接边界的不到百分之一。保证针对所有时刻同时构建，所以不取决于你何时读取。',

    'The price of looking forever is width.':
        "永远查看的代价是更宽的边界。<bookmark mark='a'/>固定边界为一点九六个标准差，只适合预先确定的一次查看。罗宾斯边界按根号log"
        " t变宽；拼接边界按根号log log t变宽，与白色重对数尺度同阶。<bookmark mark='b'/>但增长阶是渐近概念。在十万步和这里"
        '的调参下，混合边界约三点六个标准差，拼接边界约四点三。两者排序取决于期限和调参，并不存在这里已经证明的普遍最优。它们都用额外宽度换取同时覆盖。',

    "Three open questions. <bookmark mark='a'/> Which always-valid boundary is best?":
        "三个开放问题。<bookmark mark='a'/>哪个随时有效的边界最好？重对数律确定了速度，但常数，以及边界如何在早期功效和后期功效之间取舍，是没有唯一答案的选择。"
        "<bookmark mark='b'/>对于复合原假设，比如“无论分布如何，均值至多为零”，e值的理论还在书写之中。<bookmark mark='c'/>而收益既不是轻尾的，也不是独立的；"
        "适用于它们的边界是新近的，而且很松。",

    "Pause and predict. With rho of a hundred and alpha of five percent":
        "暂停思考。rho为一百、alpha为百分之五时，罗宾斯的边界在一百步时是多少个标准差，在一万步时呢？与一点九六比较。",

    'consistent with the theoretical bound up to Monte Carlo variation.':
        '在蒙特卡洛波动范围内，与理论界相符。',

    'the small-seed estimates vary around the bound; they do not prove calibration.':
        '少量种子的估计会在理论界附近波动，不能据此证明校准正确。',

    "Reveal the comparison. Divide the boundary by root t. <bookmark mark='a'/> At a hundred st":
        "揭示比较结果。先把边界除以根号t。<bookmark mark='a'/>一百步时，是二乘ln八百的平方根，大约三点六六个标准差。<bookma"
        "rk mark='b'/>一万步时，大约三点二七。两者都高于一点九六，因为它们保护反复查看。在这些早期时刻，标准化宽度不必单调增加；rho决定边"
        '界在哪个时间尺度上更有效率。',
}

PHRASES = {'Up': '向上', 'Down': '向下', "Ville's promise, kept.": '维尔的承诺兑现了。', "close to Ville's promise.": '接近维尔的承诺。', 'It has left zero behind.': '它已经把零甩在后面了。'}
