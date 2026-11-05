"""Chinese narration for philosophy2: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '哲学，从零搭建 · 第2部分：思维的法则'

CHAPTERS = {
    'Hook': '用计算来解决争论',
    'Boole': '1. 布尔的思维代数',
    'Syntax': '2. 公式、树与真值函数',
    'Post': '3. 足够的联结词',
    'Semantics': '4. 用计算判定有效性',
    'Normal': '5. 范式',
    'Deduction': '6. 自然演绎',
    'Soundness': '7. 可靠性：证明从不说谎',
    'Completeness': '8. 完全性：每个有效式都有证明',
    'Resolution': '9. 只用一条规则：归结',
    'DPLL': '10. 搜索一个模型',
    'CDCL': '11. 从冲突中学习',
    'Cost': '12. 计算的代价',
    'Industry': '13. 工作中的SAT',
    'Elenchus': '14. 作为SAT求解器的苏格拉底',
    'Evil': '15. 第一张价目表：恶的问题',
    'Outro': '回顾、习题，以及它们会在哪里再出现',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "In Part 1 we met Leibniz's dream":
        "在第1部分，我们见到了莱布尼茨的梦想：总有一天，两位哲学家意见不合时，他们不必争吵。<bookmark mark='a'/>"
        "他们会拿起笔，坐到石板前，对彼此说：让我们来算一算。<bookmark mark='b'/>这一部分要造出这台计算器的第一个零件："
        "关于“并且”“或者”“并非”和“如果”的逻辑。这是哲学中唯一一个梦想真正成真的角落，只是要付出代价，而这个代价我们会亲手测量。",
    "Here is a dispute to settle.":
        "这里有一个争论要解决。在一座岛上，每个人要么是骑士，只说真话；要么是无赖，只说假话。<bookmark mark='a'/>"
        "你遇到了三个岛民。A说：我们全都是无赖。<bookmark mark='b'/>B说：我们当中恰好有一个骑士。<bookmark mark='c'/>"
        "C什么也没说。谁是什么人？这道题出自雷蒙德·斯穆里安。你可以一步步推理，但也可能推错。",
    "Or you can calculate.":
        "或者，你可以计算。用a表示“A是骑士”这句话。<bookmark mark='a'/>那么A说的话为真，恰好当A是骑士的时候："
        "a，当且仅当，非a并且非b并且非c。<bookmark mark='b'/>B也一样。两个方程，三个未知数，每个未知数只能取真或假。",
    "So there are only eight possibilities.":
        "所以只有八种可能。<bookmark mark='a'/>把每一种都拿去对照两个方程，<bookmark mark='b'/>只要有人说的话和他的身份对不上，"
        "就划掉那一行。<bookmark mark='c'/>只剩下一行。A和C是无赖，B是骑士。不需要任何聪明：一张表，任何人、任何东西都会用同样的方式填写它。",
    'f"Now make the puzzle enormous.':
        "现在把这道题变得巨大。给从1到n的整数涂色，每个数涂蓝色或橙色，使得没有一组勾股数，比如3、4、5，全是同一种颜色。"
        "<bookmark mark='a'/>这里是前{n}个数，由我们在这一部分要造的求解器来涂色。<bookmark mark='b'/>3、4、5；5、12、13；"
        "20、21、29：<bookmark mark='c'/>{n}以内的全部{len(d['triples'])}组勾股数，每一组都用到了两种颜色。",
    "How far can you go?":
        "最多能涂到多少？<bookmark mark='a'/>2016年，马林·赫勒、奥利弗·库尔曼和维克托·马雷克给出了答案：1到7824可以这样分开，"
        "1到7825就不行。这个证明不是人找到的，而是程序找到的。它写出的证书长达200太字节，没有人能读完。检查它的，是另一个简单得多的程序。"
        "这就是莱布尼茨的石板，只是规模远远超出了他的想象。",
    "So this part is about the logic of whole sentences":
        "所以这一部分讲的是整句话的逻辑，也就是命题逻辑，以及用它来计算意味着什么。<bookmark mark='a'/>我们从布尔的思维代数开始，"
        "然后是作为树的公式，以及两个句子可以组合起来的十六种方式。<bookmark mark='b'/>接着是真值表，以及有效性是什么。"
        "<bookmark mark='c'/>然后是自然演绎，它给出机器可以检查的证明；再是可靠性和完全性，这两条定理说明证明与真理是一致的。"
        "<bookmark mark='d'/>最后是求解器：归结、搜索和子句学习；它们的代价；以及它们为工业和哲学做了什么。",
    "Two of the series' devices begin here.":
        "本系列的两个装置从这里开始。<bookmark mark='a'/>第一个是“墙”。每一部分都会砌上一块砖：标出计算在哪里止步的那条定理。"
        "第1部分砌下的是芝诺那一块。<bookmark mark='b'/>这一部分的砖不会说我们无法计算。它会说计算要花多少代价。",
    "The second is the Price List.":
        "第二个是“价目表”。当苏格拉底向一个人表明，他的信念彼此矛盾时，他让对方陷入了困境，希腊人称之为“疑难”：无路可走。"
        "<bookmark mark='a'/>我们要造一台机器，把走出一个矛盾的每一条出路都精确地列出来，并用它来处理最古老的论证之一：恶的问题。",

    # ------------------------------------------------------------------ Boole
    "Chapter one. Boole's algebra of thought.":
        "第1章。布尔的思维代数。",
    "The logic of whole sentences is older than Boole.":
        "整句话的逻辑比布尔古老得多。公元前三世纪，斯多亚派的克吕西波列出了五种他称为“不证自明”的论证："
        "其他一切推理都应当从它们出发。<bookmark mark='a'/>第一种：如果第一，那么第二；第一；所以第二。"
        "<bookmark mark='b'/>第二种：如果第一，那么第二；并非第二；所以并非第一。<bookmark mark='c'/>另外三种关于“并非两者都”、"
        "“要么……要么”和排斥。前两种我们今天每天都在用，用的是它们的拉丁名字：肯定前件式和否定后件式。",
    "The Stoics also argued about what 'if' means.":
        "斯多亚派还争论过“如果”是什么意思。麦加拉的斐洛认为，“如果p那么q”只在一种情况下为假：p真而q假。"
        "狄奥多罗斯·克罗诺斯要求更多：一种在任何时候都成立的联系。<bookmark mark='a'/>这场争论有名到诗人卡利马科斯开玩笑说，"
        "连屋顶上的乌鸦都在呱呱地争论哪些条件句是真的。这一部分采用斐洛的答案；到了第14部分我们会看到，乌鸦们为什么有理由继续争下去。",
    "Two thousand years later, George Boole":
        "两千年后，乔治·布尔，一位来自林肯郡、自学成才的中学教师，后来成了科克的教授，做了一件新的事情。1847年，"
        "然后在1854年的《思维规律的研究》中，他把逻辑写成了代数。<bookmark mark='a'/>让x代表白色事物的类，y代表绵羊的类。"
        "<bookmark mark='b'/>那么x乘以y就是白色绵羊的类。<bookmark mark='c'/>x加y把两者合在一起，前提是它们不重叠。"
        "<bookmark mark='d'/>1是我们所谈论的一切事物构成的全域，1减x是所有不是白色的东西。<bookmark mark='e'/>0是空类。",
    "One of Boole's laws is unlike ordinary algebra.":
        "布尔的定律中有一条和普通代数不一样。白色的白色事物，就是白色事物：x乘x等于x。布尔称之为二元律。"
        "<bookmark mark='a'/>作为一个关于数的方程，它只有两个解：曲线x平方和直线x相交于0和1。<bookmark mark='b'/>"
        "两个真值就是从这里来的。把1读作真，把0读作假，布尔关于类的代数就变成了关于句子的代数。",
    "And from that one law Boole derived":
        "从这一条定律出发，布尔推出了逻辑中最古老的原理：亚里士多德的矛盾律。<bookmark mark='a'/>从x平方等于x开始。"
        "<bookmark mark='b'/>两边同时减去x平方。<bookmark mark='c'/>因式分解。x乘以1减x等于0：既是x又不是x的事物构成的类是空的。"
        "没有什么东西既是白的又不是白的。一条思维规律，用代数推了出来。",
    'f"Boole\'s algebra could be done by a machine':
        "布尔的代数可以由机器来完成。1869年，经济学家威廉·斯坦利·杰文斯造出了一台：逻辑钢琴。它的方法和我们在岛上用的一样。"
        "<bookmark mark='a'/>取两个前提：铁是金属，每种金属都是元素。<bookmark mark='b'/>把这三个词项的所有组合都写出来：共有{len(rows)}种。",
    'f"The first premise strikes out':
        "第一个前提划掉了{len(strikes[0])}种组合，其中有铁却不是金属。<bookmark mark='a'/>第二个前提又划掉剩下的{len(strikes[1])}种，"
        "其中是金属却不是元素。<bookmark mark='b'/>留下了{len(surv)}种组合，而在每一种含有铁的组合里，元素也在。"
        "<bookmark mark='c'/>所以铁是元素。杰文斯的琴键和杠杆做的正是这件事，最多可处理四个词项：列举所有情况，扔掉不可能的那些。"
        "我们岛上的求解器，以及这一部分的每一张真值表，都是这样工作的。",
    "So by 1870 the pieces were on the table":
        "所以到1870年，零件都已经摆在桌上了：取两个值的变量所代表的句子；作为运算的联结词；以及通过穷尽所有情况来检验的有效性。"
        "还缺的，是对“公式是什么”以及“联结词能构造什么、不能构造什么”的精确说明。这就是下一章的内容。",

    # ------------------------------------------------------------------ Syntax
    "Chapter two. Formulas, trees and truth functions.":
        "第2章。公式、树与真值函数。",
    "A formula is built by rules":
        "公式是按规则构造出来的，就像语法构造句子一样。<bookmark mark='a'/>从原子开始：p、q、r，每个都代表一整句话，"
        "比如“正在下雨”。<bookmark mark='b'/>如果A和B是公式，那么非A；A并且B；A或者B；如果A那么B；以及A当且仅当B，"
        "各自加上括号，也都是公式。<bookmark mark='c'/>除此之外，没有别的东西是公式。",
    "Here is one formula, built in seven steps":
        "这是一个公式，分七步构造出来：否定后件式的形状。<bookmark mark='a'/>两个原子；如果p那么q；非q；它们的合取；非p；"
        "以及整个条件句。<bookmark mark='b'/>这是一个归纳定义，这一部分中关于公式的每一个证明都沿用它的形状："
        "先证明某个性质对原子成立，再证明每条规则都保持这个性质。于是它对所有公式都成立。",
    "Every formula has exactly one parse tree.":
        "每个公式都恰好有一棵语法树。<bookmark mark='a'/>原子在叶子上；每个联结词位于它所连接的东西之上；主联结词，"
        "这里是最后那个“如果……那么”，位于树根。<bookmark mark='b'/>这棵树告诉我们如何计算真值：从叶子往上算。给原子赋值，"
        "p为真，q为假。<bookmark mark='c'/>每个联结词读入它的子节点，写出自己的值。如果p那么q为假；非q为真；合取为假；非p为假；"
        "而整个条件句为真。",
    "Brackets are what make the tree unique.":
        "让树唯一的，是括号。<bookmark mark='a'/>没有括号，“p并且q或者r”可以有两种构造方式，<bookmark mark='b'/>"
        "而两棵树可能给出不同的答案：当p为假、q和r为真时，一棵为真，另一棵为假。一种用来解决争论的逻辑，不能让读者去猜。"
        "1879年，弗雷格第一个坚持要对全部推理做到这种精确。",
    "What a connective does is captured by its truth table":
        "一个联结词做什么，由它的真值表刻画：一个从输入的真值到一个真值的函数。两个输入时有四行：都真，真假，假真，都假。"
        "<bookmark mark='a'/>每一行的输出可真可假，所以两个句子的联结词一共有2的4次方，也就是16种。<bookmark mark='b'/>"
        "这里是全部16种，绿色表示真，红色表示假。",
    'f"Some have names everyone knows':
        "有些名字人人都知道：并且，或者，如果……那么，当且仅当。<bookmark mark='a'/>有些名字只有逻辑学家才用：异或，与非，或非。"
        "<bookmark mark='b'/>有些几乎算不上联结词：永远为真，永远为假，或者照抄p。<bookmark mark='c'/>有n个输入时，真值函数共有2的2的n次方个："
        "3个输入时有{cn['3']}个，5个输入时超过40亿个。下一章的问题是：我们到底需要其中多少个。",
    "One of the sixteen deserves a closer look":
        "这16个中有一个值得细看：斯多亚派斐洛的条件句，只在“如果”部分为真、“那么”部分为假时为假。<bookmark mark='a'/>"
        "它让“如果月亮是奶酪做的，那么2加2等于4”成为真的，很多人觉得这不对：这两部分之间没有任何联系。<bookmark mark='b'/>"
        "但是，假如“如果”终究要是一个真值函数，那么三个不高的要求就能把它挑出来。",
    'f"First, modus ponens must be valid':
        "第一，肯定前件式必须有效：如果p为真，“如果p那么q”也为真，那么q为真。16个中有{len(demands[0]['survivors'])}个通过。"
        "<bookmark mark='a'/>第二，“如果p那么p”必须永远为真：剩下{len(demands[1]['survivors'])}个，“如果……那么”和“当且仅当”。"
        "<bookmark mark='b'/>第三，“如果p那么q”不能和“如果q那么p”说同一件事。只剩下一个：斐洛的条件句。所以奶酪条件句的古怪，"
        "是把“如果”当作真值函数所付出的代价。第14部分会追问：“如果”应不应该是一个真值函数。",
    # ------------------------------------------------------------------ Post
    "Chapter three. Enough connectives.":
        "第3章。足够的联结词。",
    "Every one of those truth functions can be written with just three connectives":
        "那些真值函数中的每一个，都可以只用三个联结词写出来：并非、并且、或者。方法是逐行读真值表。<bookmark mark='a'/>"
        "以异或为例。它在两行中为真：p真q假，或者p假q真。<bookmark mark='b'/>用一个“并且”把每个为真的行精确地描述出来："
        "p并且非q；非p并且q。<bookmark mark='c'/>再用“或者”把这些描述连起来。结果恰好在那些为真的行中为真，"
        "<bookmark mark='d'/>它自己的真值表也证实了这一点。",
    "The recipe works for any table with any number of inputs.":
        "这个方法对任何真值表、任何数目的输入都适用。如果没有一行为真，就写p并且非p。<bookmark mark='a'/>"
        "所以并非、并且、或者是函数完全的：它们能表达存在的每一个真值函数。这个方法产生的形式有一个名字，叫析取范式，"
        "它会在第5章再次出现。",
    "Can we use fewer?":
        "能用得更少吗？<bookmark mark='a'/>德摩根律说，p或者q等同于并非（非p并且非q），于是“或者”可以去掉："
        "并非和并且就够了。<bookmark mark='b'/>1913年，亨利·谢弗证明一个联结词就够了：“并非两者都”，通常叫作与非，"
        "写成一个向上的箭头。<bookmark mark='c'/>非p就是p与非p。<bookmark mark='d'/>p并且q，是p与非q再与它自己做与非。"
        "<bookmark mark='e'/>而或者，是两个否定的与非。<bookmark mark='f'/>每个等式在全部四行中都成立。"
        "查尔斯·桑德斯·皮尔士早在1880年就发现了这一点，写在一份五十年无人阅读的手稿里。",
    "This is why a computer can be built from one kind of part.":
        "这就是为什么计算机可以只用一种零件造出来。<bookmark mark='a'/>四个与非门，这样连接，就能计算异或。"
        "<bookmark mark='b'/>把四种输入都送进去，输出恰好在两个输入不同时为真。<bookmark mark='c'/>加法器、存储器和处理器，"
        "都可以只用与非门搭成，而闪存之所以叫NAND闪存，就是因为它的存储单元是这样连接的。谢弗用纸笔找到的这个真值函数，"
        "如今在你的口袋里存在了数十亿次。",
    "But not every set is enough.":
        "但并不是每一组联结词都够用。不管怎么组合，并且和或者永远造不出并非。<bookmark mark='a'/>1941年，埃米尔·波斯特找到了精确的判据。"
        "一个联结词可能具有五种性质：保假，把全假映射为假；保真；自对偶；单调；或者仿射，也就是模2的和。<bookmark mark='b'/>"
        "这里列出了每个联结词，空心圆表示它不具有该性质。",
    "Each property survives composition.":
        "每一种性质在复合下都保持不变。以单调为例：<bookmark mark='a'/>把一个输入从假改为真，绝不会把输出从真改为假。"
        "并且和或者是单调的，用单调的零件连成的任何东西也都是单调的。并非不是单调的，所以永远造不出来。<bookmark mark='b'/>"
        "因此，一组完全的联结词，对这五种性质中的每一种，都需要有某个联结词不具有它。波斯特证明，这也是充分的。"
        "<bookmark mark='c'/>检验几组：并非加并且，完全；单独的与非，完全；并且加或者，困在单调类里；并非加当且仅当，困在仿射类里；"
        "而如果……那么，即使加上并且、或者和当且仅当，也困在保真类里，因为它们在所有输入为真时都为真。"
        "我们还通过生成每一组能构造出的全部函数，交叉检验了每一个结论。",

    # ------------------------------------------------------------------ Semantics
    "Chapter four. Valid by calculation.":
        "第4章。用计算判定有效性。",
    "Now the definitions everything else rests on.":
        "现在来看其他一切所依赖的定义。<bookmark mark='a'/>一个赋值给每个原子指派真或假：就这些句子所能分辨的而言，"
        "世界可能是什么样子的一种方式。<bookmark mark='b'/>一个公式如果在每个赋值下都为真，就是重言式；<bookmark mark='c'/>"
        "如果至少在一个赋值下为真，就是可满足的。<bookmark mark='d'/>而一组前提Γ衍推一个结论，写成这个双十字转门符号，"
        "意思是：每个使所有前提为真的赋值，也都使结论为真。<bookmark mark='e'/>这就是有效性：在所有情况下都保持真。",
    "Is Peirce's law, if 'if p then q' implies p, then p, a tautology?":
        "皮尔士律，也就是：如果“如果p那么q”蕴涵p，那么p，是重言式吗？大多数人对它毫无直觉。<bookmark mark='a'/>"
        "那就计算吧。每个原子一列，<bookmark mark='b'/>然后由内而外，每个子公式一列。<bookmark mark='c'/>"
        "最后一列的每一行都为真。是重言式。不过我们会在第6章看到，它是个奇怪的重言式：有些逻辑学家拒绝接受它。",
    "Arguments are checked the same way.":
        "论证也用同样的方法检验。<bookmark mark='a'/>肯定前件式：在两个前提都为真的每一行，结论也为真。有效。"
        "<bookmark mark='b'/>否定后件式、选言三段论、两个条件句连成的链：有效、有效、有效。",
    "Now a famous mistake, affirming the consequent.":
        "现在来看一个著名的错误：肯定后件。<bookmark mark='a'/>如果下了雨，街道就是湿的；街道是湿的；所以下了雨。"
        "<bookmark mark='b'/>真值表找到了驳倒它的那一行：p假而q真。没下雨，街道却湿了：有人开了洒水器。那一行就是一个反模型，"
        "而一个反模型就足够了。<bookmark mark='c'/>否定前件也在同一行失败。",
    "So propositional logic is decidable.":
        "所以命题逻辑是可判定的。存在一个机械的程序，对每个有效性问题都给出是或否的回答，并且总会停下来。"
        "<bookmark mark='a'/>埃米尔·波斯特在1921年的博士论文中就是这样使用真值表的，维特根斯坦的《逻辑哲学论》也在同一年用到了它。"
        "<bookmark mark='b'/>对推理的这一部分而言，莱布尼茨的梦想是字面意义上的真：任何人都可以计算，而且每个人都得到同样的答案。",
    'f"Literally true, and ruinously expensive.':
        "字面意义上的真，而且贵得惊人。一张真值表，每个赋值需要一行：n个原子就需要2的n次方行。<bookmark mark='a'/>"
        "30个原子，大约十亿行：对一台每秒检查十亿行的机器来说，要一秒。<bookmark mark='b'/>60个原子：{n60['years']:.0f}年。"
        "<bookmark mark='c'/>100个原子：宇宙年龄的{ratio:,.0f}倍。<bookmark mark='d'/>我们自己用纯Python写的填表程序，"
        "每秒大约能填{rate:,.0f}行。真实的问题有数以百万计的原子。蛮力行不通，这一部分剩下的内容，就是讲怎样做得更好。",

    # ------------------------------------------------------------------ Normal
    "Chapter five. Normal forms.":
        "第5章。范式。",
    "Chapter three built a formula from a table's true rows":
        "第3章用真值表中为真的行构造了一个公式：一个由“并且”构成的“或者”，也就是析取范式。把这个方法反过来。"
        "<bookmark mark='a'/>改看为假的行。<bookmark mark='b'/>对每一个为假的行，写一个子句，说“不是这一行”："
        "对于p真q假，写非p或者q。<bookmark mark='c'/>把这些子句用“并且”连起来，它恰好在没有任何假行成立时为真："
        "这就是合取范式，一个由“或者”构成的“并且”。",
    "Each clause is a constraint that any satisfying valuation must meet":
        "每个子句都是任何满足赋值必须遵守的约束，所以这种形式的公式就是一张约束清单。<bookmark mark='a'/>"
        "每个SAT求解器读入的都是这种形式，用一种叫DIMACS的纯文本格式：每行一个子句，原子用数字表示，负号表示并非。"
        "来自芯片设计、排程和数学的问题，都是以这样的清单交给求解器的。",
    'f"But getting into this form by algebra can explode.':
        "但用代数方法化成这种形式，可能会爆炸。<bookmark mark='a'/>取x1并且y1，或者x2并且y2，依此类推，共n对。"
        "要把它写成子句，就要把“或者”对“并且”做分配，就像把括号乘开一样。<bookmark mark='b'/>每个子句从每一对中挑一个字母，"
        "所以一共有2的n次方个子句。<bookmark mark='c'/>10对：{r10['dist_clauses']:,}个子句。40对：大约一万亿个。"
        "一个写得下一行的公式，变成了一张没有计算机能装下的清单。",
    'f"In 1968 Grigori Tseitin showed the way around.':
        "1968年，格里戈里·采廷指出了绕过去的办法。不要分配。<bookmark mark='a'/>给每个子公式起一个新名字，"
        "再写几个子句，说明这个名字的意思。比如t代表x并且y：如果t那么x；如果t那么y；如果x并且y，那么t。"
        "每个联结词三个子句，再加一个子句说整个公式的名字为真。<bookmark mark='b'/>这样，规模只按直线增长："
        "10对时，只需{r10['tseitin_clauses']}个子句，而不是{r10['dist_clauses']:,}个。",
    "The new formula is not equivalent to the old one":
        "新公式和旧公式并不等价：它多了新的字母。但它恰好在旧公式可满足时可满足，而这就是求解器所需要的一切。"
        "<bookmark mark='a'/>所以从现在起，每个问题都是一张子句清单，“这个论证有效吗？”就变成了"
        "“这些子句，加上结论的否定，是不可满足的吗？”第9到11章的求解器回答的正是这个问题。",
    'f"Not every list of clauses is equally hard.':
        "并非每张子句清单都一样难。<bookmark mark='a'/>至多含一个未被否定的原子的子句，叫作霍恩子句，以逻辑学家阿尔弗雷德·霍恩命名，"
        "它其实就是一条规则：非下雨或者湿，说的是“如果下雨，街道就湿”。<bookmark mark='b'/>给定事实，下雨和寒冷，"
        "求解器根本不需要搜索。它触发每一条条件已知的规则，然后继续：{chain}。<bookmark mark='c'/>这就是上一章工具箱里的单元传播，"
        "对霍恩子句来说，它能在线性时间内判定可满足性。它是编程语言Prolog的引擎，也是1980年代基于规则的专家系统的引擎。"
        "每个子句两个文字的情形也很容易。每个子句三个文字时，这个问题就和任何答案可以快速检验的问题一样难，第12章会讲到。",

    # ------------------------------------------------------------------ Deduction
    "Chapter six. Natural deduction.":
        "第6章。自然演绎。",
    "Truth tables tell you whether an argument is valid.":
        "真值表告诉你一个论证是否有效。它不告诉你为什么，而且规模一大就不行了。证明两样都能做到：一串小步骤，每一步都由一条规则许可，"
        "从前提走到结论。<bookmark mark='a'/>1934年和1935年，斯坦尼斯瓦夫·雅希科夫斯基和格哈德·根岑各自独立地设计了一种证明系统，"
        "力求看起来像日常推理，根岑称之为自然演绎。<bookmark mark='b'/>每个联结词都有两类规则：一类引入它，一类消去它。",
    "Some rules simply say what the connective means.":
        "有些规则只是在说联结词的意思。由A和B，推出A并且B；由A并且B，推出A。<bookmark mark='a'/>另一些规则用到临时假设。"
        "要证明“如果A那么B”，就先假设A，在这个假设下推出B，然后撤销假设，得出“如果A那么B”。这就是条件证明。"
        "<bookmark mark='b'/>否定也是同样的方式：如果假设A导致矛盾，也就是写成倒T的那个假常项，就得出非A。而从矛盾出发，什么都能推出来。",
    "Here is modus tollens, proved rather than tabulated":
        "这是否定后件式，这次是证明出来的，而不是列表算出来的，用的是弗雷德里克·菲奇在1952年引入的格式。<bookmark mark='a'/>"
        "前提：如果p那么q；非q。<bookmark mark='b'/>现在为了论证而假设p。竖线标出这个假设的有效范围。<bookmark mark='c'/>"
        "由p和“如果p那么q”，得到q：这是箭头消去。<bookmark mark='d'/>但我们还有非q：矛盾。<bookmark mark='e'/>"
        "所以这个假设必须撤销。关上它的方框，得出非p。六行，每一行都是一条任何人都能检查的规则。",
    'f"Checking a proof is mechanical':
        "检查证明是机械的，所以由推理机来做：它查看每一行、所引用的规则，以及这条规则用到的那些行。<bookmark mark='a'/>"
        "它接受了我们的证明。<bookmark mark='b'/>现在改动最后一行：不撤销假设，而是重复使用在方框里推出的q。"
        "<bookmark mark='c'/>检查器拒绝了：{msg}。那个q只在假设p时成立。绝不使用只是为了论证而假设的东西：这条规则，正是方框存在的全部意义。",
    'f"Not every tautology comes so easily.':
        "不是每个重言式都来得这么容易。这是皮尔士律，用{len(lines)}行证出，带有两层嵌套的假设。<bookmark mark='a'/>"
        "看看真正起作用的那一行。它去掉了双重否定：由非非p，推出p。<bookmark mark='b'/>排中律，p或者非p，也需要这同一条规则，"
        "皮尔士律的每一个证明都需要它。",
    "Remove that one rule and you get intuitionistic logic":
        "去掉这一条规则，你就得到直觉主义逻辑，荷兰数学家布劳威尔的逻辑。<bookmark mark='a'/>布劳威尔认为，要断言“p或者非p”，"
        "你必须能说出是哪一个；而“非非p”的证明还不是p的证明。这一部分的每一张真值表都说排中律是重言式，所以在他看来，"
        "真值表本身就假定得太多了。第9部分会构造他的逻辑，以及它自己的语义。一条看似无害的规则，标出了数学哲学中最深的分歧之一。",
    # ------------------------------------------------------------------ Soundness
    "Chapter seven. Soundness: proofs never lie.":
        "第7章。可靠性：证明从不说谎。",
    "We now have two ways of saying that a conclusion follows from premises.":
        "现在我们有两种方式来说一个结论从前提得出。<bookmark mark='a'/>一种关于证明：存在一个推导，写成单十字转门符号。"
        "<bookmark mark='b'/>另一种关于真：每个使前提为真的赋值也使结论为真，也就是双十字转门。证明是我们做的事情，"
        "用纸上的记号，任何人都能检查。真则关乎世界可能是的每一种样子。<bookmark mark='c'/>两者是一回事吗？"
        "两条定理回答了这个问题，每个方向一条。<bookmark mark='d'/>第一条是可靠性：凡是我们能证明的都是有效的。证明从不说谎。",
    'f"The proof follows the shape of proofs':
        "这个证明沿用证明本身的形状：对证明的长度做归纳。<bookmark mark='a'/>前提在每个使前提为真的赋值中为真，这是显然的。"
        "然后证明每一条规则，作用于在某个赋值中为真的行，都产生在该赋值中为真的行。<bookmark mark='b'/>每条规则的条件本身"
        "就是一个小的衍推或重言式，所以推理机逐一检查它们。<bookmark mark='c'/>全部{len(d)}条都通过了。",
    "The rules that close boxes need a little more care":
        "关闭方框的规则需要多加小心，因为在方框里面，前提变了。<bookmark mark='a'/>箭头引入说：如果前提加上A导出B，"
        "那么单凭前提就导出“如果A那么B”。它的条件就是这个公式，其中G代表前提：它是一个重言式，所以不管G说什么，这一步都是安全的。",
    "Compare a rule we must not add":
        "对比一条我们绝不能加的规则：由“如果A那么B”和B，推出A，也就是把肯定后件当成规则。<bookmark mark='a'/>"
        "推理机立刻找到了它的反模型：A假，B真。有这条规则的系统，会从真的前提证出假的结论。<bookmark mark='b'/>"
        "可靠性有一个推论。没有赋值能使假常项为真，所以不从任何前提出发的证明都到达不了它：这个系统是一致的。"
        "<bookmark mark='c'/>我们能检查的，永远不会超出事实本身。",
    "Soundness also says something about what rules can and cannot do.":
        "可靠性还告诉我们规则能做什么、不能做什么。<bookmark mark='a'/>1960年，阿瑟·普赖尔发明了一个他称为tonk的联结词，"
        "它的引入规则像“或者”：由A，推出A tonk B；消去规则像“并且”：由A tonk B，推出B。<bookmark mark='b'/>"
        "两条看似无害的规则，合在一起，却能从任何东西证出任何东西。由“下雨了”，推出“下雨了tonk月亮是奶酪做的”，再推出“月亮是奶酪做的”。",
    'f"Could some truth table make tonk sound?':
        "有没有哪张真值表能让tonk成为可靠的？它的引入规则要求只要A为真它就为真；消去规则要求只要它为真B就为真。"
        "<bookmark mark='a'/>推理机检查了全部16张表。{len(t['intro_only'])}张使引入规则可靠，{len(t['elim_only'])}张使消去规则可靠，"
        "没有一张两者兼顾：在A真B假的那一行，两个要求发生冲突。<bookmark mark='b'/>努埃尔·贝尔纳普在1962年的回应是："
        "规则只有在与语言其余部分和谐时，才能赋予一个词意义：加入它们，不能对旧的词证出任何新东西。我们的规则通过了这个检验；"
        "tonk的规则没有。规则如何赋予意义这个问题，会在第28部分再次出现。",

    # ------------------------------------------------------------------ Completeness
    "Chapter eight. Completeness: every validity has a proof.":
        "第8章。完全性：每个有效式都有证明。",
    "Soundness says the rules never prove too much.":
        "可靠性说规则从不证明得太多。完全性说它们也从不证明得太少：如果一个结论在每个赋值中都从前提得出，"
        "那么就存在它的一个推导，只用第6章那几条规则。<bookmark mark='a'/>保罗·贝尔奈斯在1918年证明了命题逻辑的情形，"
        "埃米尔·波斯特在1921年用别的方法证明了它，库尔特·哥德尔在1929年证明了第3部分那种丰富得多的逻辑的情形。",
    "The proof turns the question around.":
        "这个证明把问题反过来。<bookmark mark='a'/>假设结论φ不能被证明。<bookmark mark='b'/>那么把非φ加到前提里，"
        "就永远不会导出矛盾：如果会，否定引入和双重否定消去就能证出φ了。这个集合是一致的。<bookmark mark='c'/>"
        "所以，假设我们能证明每个一致的集合都有模型，也就是一个使它全部为真的赋值。<bookmark mark='d'/>"
        "那么就有某个赋值使前提为真而φ为假，这个论证就不是有效的。这就是倒过来读的完全性。",
    "Consistency is a fact about proofs":
        "一致性是关于证明的事实：推不出矛盾。有模型是关于真的事实。整条定理的分量都压在高亮的那一步上，"
        "它从第一类事实架起一座通往第二类事实的桥。",
    'f"The bridge is due to Adolf Lindenbaum.':
        "这座桥要归功于阿道夫·林登鲍姆。<bookmark mark='a'/>把所有公式一个接一个列出来：它们是可数的，就像字典里的词。"
        "从一个一致的集合开始：这里是p或者q，以及非p。<bookmark mark='b'/>现在沿着清单往下走。对每个公式，如果加入后集合仍然一致，"
        "就加入它；否则，加入它的否定。第一个是{first['f'].replace('¬', 'not ')}：{('consistent, so it goes in' if first['chose'] == 'it' else 'that would contradict what we have, so its negation goes in')}。"
        "<bookmark mark='c'/>如此下去，永不停止。这里是计算出的前十四步。",
    "In the limit, the set decides every formula":
        "在极限处，这个集合判定了每一个公式：它包含每个公式或它的否定，而且仍然一致，因为任何矛盾只会用到它有限多个成员，"
        "而每个有限阶段都是一致的。<bookmark mark='a'/>现在读出一个赋值：一个原子为真，当且仅当集合包含它。"
        "一个通过对公式归纳证明的真值引理说，这个赋值使之为真的，恰好是集合中的那些公式。<bookmark mark='b'/>"
        "所以每个一致的集合都有模型，完全性得证。",
    "The construction has a remarkable consequence, called compactness.":
        "这个构造有一个了不起的推论，叫作紧致性。<bookmark mark='a'/>如果一组句子的每个有限子集都能被满足，那么整组句子也能，"
        "即使这组句子是无穷的。<bookmark mark='b'/>例如：一张无穷的地图可以用四种颜色着色，使相邻的国家颜色不同，"
        "只要它的每个有限部分都可以。尼古拉斯·德布鲁因和保罗·埃尔德什在1951年证明了这一点。每个国家一个句子；"
        "每个有限集合都可满足；所以整张地图都可着色。",
    "In propositional logic, then, proof and truth coincide exactly":
        "所以，在命题逻辑中，证明与真完全吻合：有效的都能被证明，能被证明的都是有效的。没有任何真理能逃出这些规则。"
        "<bookmark mark='a'/>紧致性会在第3部分再次出现，在那里它变出比每个自然数都大的数；而证明与真之间的吻合，会在第7部分彻底破裂。",

    # ------------------------------------------------------------------ Resolution
    "Chapter nine. One rule: resolution.":
        "第9章。只用一条规则：归结。",
    "Natural deduction has ten rules":
        "自然演绎有十条规则，需要一个人来选择下一步用哪条。归结只有一条规则，机器可以盲目地使用它。<bookmark mark='a'/>"
        "由一个含有x的子句，和一个含有非x的子句，推出由其余所有部分组成的子句。A或者x；B或者非x；所以A或者B。"
        "<bookmark mark='b'/>它的可靠性按情况证明。如果x为真，第二个子句需要B。<bookmark mark='c'/>如果x为假，第一个子句需要A。"
        "<bookmark mark='d'/>无论哪种情况，都是A或者B。<bookmark mark='e'/>而当两个子句只是x和非x时，什么也不剩：空子句，"
        "画成一个方框，没有任何赋值能满足它。最纯粹的矛盾。",
    "Resolution proves things by refutation.":
        "归结通过反驳来证明。<bookmark mark='a'/>要证明前提衍推结论，就加上结论的否定，<bookmark mark='b'/>把一切都化成子句，"
        "<bookmark mark='c'/>然后不断归结，直到出现空子句。<bookmark mark='d'/>如果出现了，前提和被否定的结论就不可能同时为真："
        "结论成立。<bookmark mark='e'/>马丁·戴维斯和希拉里·普特南在1960年把归结用于命题子句。1965年，约翰·艾伦·罗宾逊"
        "把它变成了一个处理第3部分完整逻辑的证明器的唯一规则，从那以后，它一直是自动推理的引擎。",
    'f"Back to the island.':
        "回到岛上。我们的两个方程变成了{len(base)}个子句。<bookmark mark='a'/>要证明B是骑士，就加上相反的说法，非b，"
        "然后寻找空子句。<bookmark mark='b'/>推理机用{len(proof)}步找到了一个反驳。每一步都归结黑板上已有的两个子句，"
        "被用到的子句会闪一下。",
    "Read it as an argument.":
        "把它当作一个论证来读。A是无赖：谜题的子句直接包含这一点，因为骑士永远不会说“我们全是无赖”。然后，如果B是无赖，"
        "C就必须既是无赖又是骑士。方框闭合了。B是骑士，和真值表说的一样，而现在我们知道了为什么。",
    "Resolution is refutation complete":
        "归结是反驳完全的：如果一组子句不可满足，归结最终会推出空子句。所以它也能判定有效性。<bookmark mark='a'/>"
        "但盲目的归结可能产生大量的子句，下一步归结哪一对，才是全部的技巧所在。我们的归结器先处理最短的子句，"
        "并扔掉任何比已有子句说得更多的子句。即便如此，在第12章会遇到的一族公式上，数量还是爆炸了。"
        "接下来两章改为搜索模型，并且边搜边学。",

    # ------------------------------------------------------------------ DPLL
    "Chapter ten. Searching for a model.":
        "第10章。搜索一个模型。",
    "A truth table tries every valuation.":
        "真值表尝试每一个赋值。更聪明的搜索一步一步地构造一个赋值，遇到麻烦就退回。<bookmark mark='a'/>这是马丁·戴维斯、"
        "乔治·洛格曼和唐纳德·洛夫兰在1962年提出的方法，现在叫DPLL。它有三个动作。<bookmark mark='b'/>传播：如果一个子句"
        "除了一个文字之外都为假，那么那个文字就被强制。如果a为真，子句非a或者c就强制c。<bookmark mark='c'/>分支："
        "没有被强制的东西时，挑一个未定的原子，先试真。<bookmark mark='d'/>退回：如果某个子句的每个文字都为假，"
        "就撤销上一个选择，改试另一个值。",
    'f"Here it is on a formula of':
        "这是它在一个由{len(clauses)}个子句、五个原子组成的公式上的运行，是推理机自己的运行记录。<bookmark mark='a'/>{story}",
    "Try a as true, which forces c, d and e":
        "先试a为真，这强制了c、d和e，然后一个子句失败了：退回。再试a为假，这强制了b。试c为真。试d为真，这强制了e，"
        "然后一个子句失败了：退回。试d为假，每个子句都成立了。",
    'f"The search visited':
        "这次搜索访问了{len(nodes)}个节点，而真值表要填{2 ** 5}行。<bookmark mark='a'/>在真实的问题上，差距是天文数字，"
        "因为一个被强制的值会强制另一个，形成长长的链条，而一次冲突会一下子剪掉整棵子树。<bookmark mark='b'/>"
        "这也是一个细心的人从假设出发推理的方式：先假设，追踪后果，当后果冲突时，就收回假设。DPLL就是系统化的归谬法。",
    'f"How hard is a random formula?':
        "随机公式有多难？<bookmark mark='a'/>在n个原子上生成由三个随机文字组成的子句，然后转动一个旋钮：每个原子对应的子句数。"
        "子句很少时，几乎每个公式都可满足，DPLL立刻就找到一个模型。子句很多时，几乎每个公式都自相矛盾，冲突很快就出现。"
        "<bookmark mark='b'/>在两者之间，大约每个原子4.27个子句处，可满足的概率从几乎为1跌到几乎为0，n越大跌得越陡。"
        "<bookmark mark='c'/>而在它附近，DPLL的工作量达到峰值：对40个原子，是在每个原子{peak['40']}个子句处；"
        "对小公式来说，峰值位于阈值稍右一点。最难的公式，就生活在可满足与不可满足之间的刀锋上，一种相变，就像水结冰一样。"
        "<bookmark mark='d'/>埃胡德·弗里德古特在1999年证明了这种下跌是陡峭的；而它究竟落在哪里，目前只对长子句得到了证明，"
        "由丁剑、艾伦·斯莱和孙妮可在2015年完成。",

    # ------------------------------------------------------------------ CDCL
    "Chapter eleven. Learning from conflict.":
        "第11章。从冲突中学习。",
    "DPLL forgets.":
        "DPLL会遗忘。一个分支失败时，它退回一步再试；如果同样的错误潜伏在树的别处，它就会一遍又一遍地重新发现它。"
        "<bookmark mark='a'/>1996年，若昂·马克斯-席尔瓦和卡里姆·萨卡拉用他们的求解器GRASP，教会了搜索从每一次失败中学习。"
        "<bookmark mark='b'/>五年后，求解器Chaff让这个想法变得飞快。冲突驱动的子句学习，如今存在于每一个严肃的SAT求解器中。",
    'f"Watch it on a formula of':
        "看它在一个由{len(clauses)}个子句、八个原子组成的公式上运行，这是推理机自己的运行。<bookmark mark='a'/>第一个决策：a为真。"
        "<bookmark mark='b'/>传播随之而来。a强制b，也强制c。b和c一起强制d。d强制e。d和e强制f。<bookmark mark='c'/>"
        "把每个被强制的值画出来，再从强制它的那些值画箭头指向它，你就得到了蕴涵图。<bookmark mark='d'/>"
        "然后一个子句失败了：非f或者非a。冲突。",
    "Now ask why.":
        "现在问为什么。顺着蕴涵图，把冲突追溯到造成它的那些决策。<bookmark mark='a'/>每一条路径都指向同一个原因：决定a。"
        "<bookmark mark='b'/>所以学习一个禁止这个原因的子句：非a。它可以通过沿着图做归结从公式推出，所以加入它不会排除任何满足赋值；"
        "但求解器再也不会在搜索的任何地方犯这个错误了。",
    "Then jump back: not one step":
        "然后跳回去：不是退一步，而是退到学到的子句第一次派上用场的那一层，这里是最顶层，在任何决策之前。"
        "<bookmark mark='a'/>学到的子句立刻强制了非a。然后传播强制了g、h和b。决定d强制了e和f，最后一个决策c，"
        "使每个子句都得到满足。一次冲突，一个教训，搜索再也没有回到那条死路。",
    'f"Does learning pay?':
        "学习划算吗？这里是在子句与原子之比最难的地方生成的随机公式，每个规模{seeds}个，由推理机的DPLL和CDCL分别求解。"
        "<bookmark mark='a'/>随着公式变大，CDCL需要的决策少得多：在50个原子时，中位数是{r50['cdcl_decisions_median']:.0f}，"
        "而DPLL是{r50['dpll_decisions_median']:.0f}。工业级求解器做得更多，能处理有数百万个原子的公式。<bookmark mark='b'/>"
        "这背后有一个深刻的事实：CDCL学到的都是归结式，所以它是伪装起来的归结。加上重启，它可以模拟任何归结证明，"
        "这是诺特·皮帕特斯里萨瓦和阿德南·达尔维希在2011年证明的。这意味着，凡是让归结变慢的东西，也会让CDCL变慢。这就是下一章。",
    # ------------------------------------------------------------------ Cost
    "Chapter twelve. The price of calculation.":
        "第12章。计算的代价。",
    "Every solver we have built works on small examples.":
        "我们造的每一个求解器，在小例子上都能工作。真正的问题是，工作量如何随着问题的规模增长。<bookmark mark='a'/>"
        "有些问题可以在随规模按多项式增长的时间内解决：给一张清单排序，找一条最短路径。这一类叫作P。<bookmark mark='b'/>"
        "另一些问题的答案，一旦有人递给你，检查起来很快。一个满足赋值，逐个子句一查，转眼就查完了。这一类叫作NP。"
        "<bookmark mark='c'/>是否每个答案能被快速检查的问题，其答案也都能被快速找到，也就是P是否等于NP，"
        "是计算机科学中最著名的未解问题，也是克雷研究所悬赏百万美元的千禧年大奖难题之一。",
    "In 1971 Stephen Cook, and independently Leonid Levin":
        "1971年，斯蒂芬·库克，以及在莫斯科独立工作的列昂尼德·列文，证明了SAT是NP完全的。<bookmark mark='a'/>"
        "取任何一个答案可以被某台机器快速检查的问题。把这台机器的整个运行过程写成一张网格：每个时刻一行，纸带的每个格子一列。"
        "<bookmark mark='b'/>为每一个形如“在时刻t，第i格写着符号s”的事实设一个原子。<bookmark mark='c'/>"
        "然后写出子句，说明每一行都按机器的规则从上一行得来，并且最后一行写着“接受”。<bookmark mark='d'/>"
        "这些子句可满足，恰好当问题有答案的时候。所以，一个快速的SAT方法，就会是所有答案可以被检查的问题的快速方法："
        "排课表、设计蛋白质，以及破解今天大部分的加密。大多数研究者相信，这样的方法并不存在。",
    "Even a formula that is obviously false can be expensive to refute.":
        "即使一个显然为假的公式，反驳起来也可能代价高昂。<bookmark mark='a'/>把n加1只鸽子放进n个洞里，每个洞至多一只。"
        "谁都看得出这办不到。<bookmark mark='b'/>写成子句：每只鸽子都在某个洞里；没有两只鸽子共用一个洞。<bookmark mark='c'/>"
        "1985年，阿明·哈肯证明，这些公式的每一个归结反驳都是指数长的，不管找得多么巧妙。",
    'f"Here is what our own solvers did.':
        "这是我们自己的求解器做的事。<bookmark mark='a'/>随着洞的数目从1增加到{res[-1]['n']}，归结生成了{res_txt}个子句。"
        "<bookmark mark='b'/>对{php[-1]['n']}个洞，CDCL需要{php[-1]['cdcl_conflicts']:,}次冲突，每多一个洞大约多{np.mean(growth[-3:]):.1f}倍。"
        "<bookmark mark='c'/>而真值表，对{last['n']}个洞，需要2的{last['vars']}次方行。",
    "Is that a limit of proof itself, or only of resolution?":
        "这是证明本身的极限，还是只是归结的极限？<bookmark mark='a'/>更强的证明系统做得更好。扩展归结可以像采廷编码给子公式命名那样"
        "给新的想法命名，它对鸽巢原理有简短的证明，这是库克在1976年证明的。<bookmark mark='b'/>是否有某个证明系统对每个重言式"
        "都有简短的证明，结果和NP是否等于它的镜像coNP是同一个问题，这是斯蒂芬·库克和罗伯特·雷克豪在1979年提出的。它仍然悬而未决。",
    "So here is the second brick of the Wall.":
        "所以这就是墙上的第二块砖。<bookmark mark='a'/>莱布尼茨的计算是存在的：命题有效性的每一个问题，都可以被任何人机械地解决，"
        "每次都得到同样的答案。<bookmark mark='b'/>但除非P等于NP，有些问题解决起来的代价，比整个宇宙付得起的还多。"
        "梦想还在，只是标上了价格。",

    # ------------------------------------------------------------------ Industry
    "Chapter thirteen. SAT at work.":
        "第13章。工作中的SAT。",
    "In 1994 the mathematician Thomas Nicely noticed":
        "1994年，数学家托马斯·奈斯利注意到，英特尔新的奔腾处理器在某些除法上会算错。英特尔估计，大约每90亿次随机除法出错一次。"
        "它更换了这些芯片，花费了4.75亿美元。<bookmark mark='a'/>从那以后，芯片制造商转向了证明：把芯片的逻辑写成公式，"
        "对每一个输入，而不是一个样本，去对照它的规格进行检查。<bookmark mark='b'/>有一种方法叫有界模型检测，诞生于1999年，"
        "它把一个电路展开成k个时钟周期：每一步一份它的状态转移逻辑，一端是初始状态，另一端是某个性质的失效。"
        "<bookmark mark='c'/>是否存在一个能到达失效的输入序列？一个SAT问题。如果答案是否，那么在k步之内，没有任何输入能弄坏这块芯片。",
    "In the cloud, the same idea guards data.":
        "在云端，同样的想法守护着数据。亚马逊的工具Zelkova把客户编写的访问策略翻译成逻辑，<bookmark mark='a'/>"
        "然后问一个求解器：是否可能有某个请求被允许，从而把数据暴露给公众。<bookmark mark='b'/>这里用的是SMT求解器："
        "加上了算术、字符串和其他理论的SAT求解器。<bookmark mark='c'/>2022年，亚马逊的妮哈·伦格塔报告说，这样的检查每天大约运行十亿次。",
    "Installing software is a logic problem too.":
        "安装软件也是一个逻辑问题。<bookmark mark='a'/>每个软件包都要求其他软件包的某些版本，又和另一些冲突：这些就是子句。"
        "这里，A1需要B的第2版或第3版，C1不能和B3共存，而B只能装一个版本。<bookmark mark='b'/>推理机的求解器选了B2。"
        "<bookmark mark='c'/>有成千上万个软件包时，这就是一场真正的搜索：判定一个软件包到底能不能装上是NP完全的，"
        "而从Linux发行版到科学计算用的Python安装器conda，软件包管理器都把它交给SAT式的求解器。",
    "And in mathematics.":
        "还有数学。<bookmark mark='a'/>开场时的勾股数问题，2016年。第五个舒尔数160，紧接着第二年，证明长达2拍字节。"
        "关于用立方体铺砌的凯勒猜想，在第7维，2020年。每一个都是没有人逐行检查过的定理，而是由一个小到可以单独验证的证明检查器来认证的。",
    "Is a two-hundred-terabyte certificate a proof?":
        "一张200太字节的证书是证明吗？这个问题比这些求解器更古老。<bookmark mark='a'/>1976年，肯尼斯·阿佩尔和沃尔夫冈·哈肯"
        "借助计算机证明了四色定理；三年后，哲学家托马斯·季莫奇科论证说，接受它就意味着改变我们所说的“证明”的含义："
        "<bookmark mark='b'/>数学接纳了实验。今天的标准回答是形式化的：如果一个小的、可信的程序检查过它，一张证书就是一个证明。"
        "第9部分会追问，这样的检查说明了什么，又遗漏了什么。",

    # ------------------------------------------------------------------ Elenchus
    "Chapter fourteen. Socrates as a SAT solver.":
        "第14章。作为SAT求解器的苏格拉底。",
    "Socrates' method was a kind of calculation.":
        "苏格拉底的方法是一种计算。在柏拉图《理想国》第一卷中，老人克法洛斯提出，正义就是说真话、偿还所欠。<bookmark mark='a'/>"
        "苏格拉底问：假设一位朋友在神志清醒时把武器寄放在你这里，后来疯了，向你索回。你应该还给他吗？<bookmark mark='b'/>"
        "三个主张。正义就是偿还所欠。归还武器就是偿还所欠。而把武器还给一个疯子，是不正义的。<bookmark mark='c'/>"
        "每一个都说得通；合在一起却不一致。",
    "Cephalus leaves to see to a sacrifice":
        "克法洛斯离开去照看祭祀，他的儿子玻勒马霍斯接过了论证，给出一个新的定义：<bookmark mark='a'/>正义就是帮助朋友、伤害敌人。"
        "<bookmark mark='b'/>所以正义的人有时会伤害敌人。<bookmark mark='c'/>苏格拉底追问。伤害一个人会使他在人的德性上变坏，"
        "而正义是一种人的德性：伤害使人变得不那么正义。<bookmark mark='d'/>但使任何人变得不那么正义，不可能是正义的作为。"
        "又是四个主张，第二个矛盾。",
    'f"Feed all {len(keys)} claims to the Reasoner':
        "把全部{len(keys)}个主张交给推理机，每个都写成一个公式：o代表“归还武器就是偿还所欠”，j代表“这是正义的”，依此类推。"
        "<bookmark mark='a'/>它检查全部{d['subsets_checked']}个主张子集的一致性，返回其中极小的不一致集合：这些集合是矛盾的，"
        "但只要去掉其中任何一个主张，就不再矛盾。<bookmark mark='b'/>恰好有{len(mus)}个：苏格拉底找到的那两个矛盾，再没有别的藏在其中。",
    'f"Now the question an interlocutor actually faces':
        "现在来看对话者实际面对的问题：该放弃哪些主张？<bookmark mark='a'/>一个极小修正集，是去掉之后就能恢复一致的最小主张集合。"
        "<bookmark mark='b'/>这里有{len(mcs)}个：从第一个矛盾中取一个主张，从第二个矛盾中取一个，所有的组合。<bookmark mark='c'/>"
        "这不是巧合。雷蒙德·赖特在1987年证明的一条定理说，极小修正集恰好就是那些极小不一致集合的极小碰集："
        "一次打破所有矛盾的最小方式。",
    "Socrates' own choice was one of these":
        "苏格拉底自己的选择就是其中之一：放弃两个定义。<bookmark mark='a'/>逻辑并没有替他选择。它精确地指出了选择在哪里。"
        "<bookmark mark='b'/>这就是本系列“价目表”的引擎。对每一个重大的难题，我们都会陈述那些可信的主张，让机器找出每一条出路，"
        "并给每条出路标上走这条路的哲学家；在2020年PhilPapers调查问过的地方，还标上有多少哲学家走这条路。",

    # ------------------------------------------------------------------ Evil
    "Chapter fifteen. The first Price List: the problem of evil.":
        "第15章。第一张价目表：恶的问题。",
    "The argument is very old.":
        "这个论证非常古老。大约公元300年，拉克坦修斯把它归于伊壁鸠鲁。<bookmark mark='a'/>大卫·休谟在《自然宗教对话录》中"
        "借斐洛之口说：他愿意阻止恶，却做不到吗？那他就是无能的。他做得到，却不愿意吗？那他就是恶意的。他既做得到又愿意吗？"
        "那恶从何而来？<bookmark mark='b'/>1955年，J. L. 麦基把它磨砺成一项不一致的指控。他说，有神论者的信念不只是缺乏支持，"
        "而是根本不理性：它们彼此矛盾。",
    "State it as six claims.":
        "把它写成六个主张。<bookmark mark='a'/>上帝存在。上帝是全能的。上帝是全知的。上帝是全善的。一个善良、全知、全能的存在者"
        "会阻止一切恶。而恶是存在的。<bookmark mark='b'/>推理机证实了麦基的说法：这六个主张不一致。而且唯一的极小不一致集合"
        "就是这六个全体。所以立场恰好有六种：放弃其中任何一个主张，一致性就恢复了。",
    "Give up the first: there is no God.":
        "放弃第一个：上帝不存在。这是麦基自己的结论；在2020年的PhilPapers调查中，大约三分之二的哲学家接受或倾向于无神论。",
    "Give up omnipotence: God's power is limited.":
        "放弃全能：上帝的力量是有限的。追随怀特海和哈茨霍恩的过程神学家认为，上帝是劝导，而不是强制。",
    "Limit what God knows:":
        "限制上帝所知：一些开放有神论者认为，受造物未来的自由选择，还不存在可以被知道的东西。",
    "Give up perfect goodness:":
        "放弃完全的善：很少有哲学家走这条出路。",
    "Deny that evil is real:":
        "否认恶是真实的：一些传统称它为幻象。奥古斯丁的观点，即恶是一种缺失，是善的不在场，很接近这条出路，但并没有真正走上去。",
    "Or give up the bridge premise:":
        "或者放弃那个桥接前提：一个善良而全能的存在者，可能为了更大的善而容许恶。阿尔文·普兰丁格在1974年提出的自由意志辩护论证说，"
        "一个由有时会做错事的自由受造物组成的世界，可能比上帝能够创造的任何一个没有恶的世界都更好。今天大多数哲学家，"
        "无论是不是有神论者，都同意这条出路至少在逻辑上是开放的，纯粹逻辑形式的恶的问题并不成立。",
    "Notice what the calculation did, and what it did not.":
        "注意这次计算做了什么，没做什么。<bookmark mark='a'/>它精确地找到了每一条出路，没有遗漏任何一条。<bookmark mark='b'/>"
        "它没有说哪些出路是通的。自由意志值不值得它所容许的恶，这不是命题逻辑的问题。第23部分会回到这里，到那时，"
        "这个论证会变成一个关于概率的论证。",
    "And notice one more thing.":
        "还要注意一件事。我们把“一切恶”和“每一个存在者”写在了原子里面，逻辑看不到它们。<bookmark mark='a'/>"
        "命题逻辑无法看进一个句子的内部。“凡人皆有一死；苏格拉底是人；所以苏格拉底会死”，在它看来，就是p和q，所以r："
        "<bookmark mark='b'/>无效，有一个反模型。要看进句子内部，我们需要“所有”和“有些”，也就是量词。这就是第3部分。",

    # ------------------------------------------------------------------ Outro
    "Let's gather what we built.":
        "我们来汇总一下造出了什么。<bookmark mark='a'/>布尔把逻辑写成了代数，他的定律x平方等于x给了逻辑两个值。公式是树；"
        "连接两个句子有十六种方式，其中一种，与非，就足以表达全部，这由波斯特判据给出。<bookmark mark='b'/>"
        "有效性就是在每个赋值中都保持真，可以用真值表判定，代价是2的n次方行。范式把每个问题都变成一张子句清单。"
        "<bookmark mark='c'/>自然演绎给出机器可以检查的证明，可靠性与完全性说明证明与真完全一致。<bookmark mark='d'/>"
        "归结、DPLL和子句学习，是工业中运行的求解器。SAT是NP完全的，有些显而易见的真理只有极其庞大的证明。"
        "而苏格拉底的方法，作为SAT来运行，列出了走出矛盾的每一条出路。",
    "The Reasoner now has its first module":
        "推理机现在有了第一个模块：公式、真值表、范式、一个证明检查器、三个求解器，以及价目表的引擎，每一个都用蛮力检验过。"
        "<bookmark mark='a'/>之后的每一部分都会往里添加，第39部分会用这个SAT求解器来检验关于投票的阿罗定理的一个情形。"
        "<bookmark mark='b'/>墙也有了第二块砖：计算的代价。",
    "Six problems, with full solutions in this part's notes.":
        "六道习题，完整的解答在这一部分的笔记里。<bookmark mark='a'/>两道关于联结词和证明，一道关于编码，又一座岛，"
        "赖特定理的一半，还有一道题请你和苏格拉底争论。在这里暂停，试着做一做。",
    "Where this comes back.":
        "这些内容会在哪里再出现。<bookmark mark='a'/>SAT求解器和价目表会在连锁悖论、恶的问题、心身问题、自由意志和阿罗定理中再次出现。"
        "完全性和紧致性在第3和第7部分再次出现。双重否定规则，是第9部分的直觉主义者下车的地方。斐洛的条件句会在第14部分受到盘问。"
        "<bookmark mark='b'/>接下来，在第3部分，我们要打开原子：“所有”“有些”、关系与模型、哥德尔的完全性定理，"
        "以及第一个任何计算都绕不过去的结果。",
    "The books and papers this part follows":
        "这一部分所依据的书和论文都列在屏幕上，也写在笔记里。感谢观看。",
}

PHRASES = {
    "line 6: cites a line that is not accessible": "第6行引用了一行不可访问的内容",
    "consistent, so it goes in": "一致，所以把它加进去",
    "that would contradict what we have, so its negation goes in": "那会与已有的内容矛盾，所以加入它的否定",
    "p": "p",
    "wet, then ice, then slippery": "路面湿了，然后结冰，然后打滑",
}
