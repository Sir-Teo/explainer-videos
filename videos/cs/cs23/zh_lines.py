"""Chinese narration for cs23: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第23部分：优化"

CHAPTERS = {
    "Hook": "多面体上的最优点",
    "LinearPrograms": "1. 线性规划",
    "Simplex": "2. 单纯形法",
    "Duality": "3. 对偶",
    "KleeMinty": "4. 理论上是指数的，实践中却很快",
    "PolyTime": "5. 多项式时间：椭球与中心路径",
    "Unimodular": "6. 当顶点都是整数时",
    "IntegerPrograms": "7. 整数规划",
    "Approximation": "8. 近似：覆盖问题",
    "Tsp": "9. 旅行商问题",
    "MaxCut": "10. 随机超平面：最大割",
    "Online": "11. 在线：看不见未来的决策",
    "Weights": "12. 乘性权重",
    "Convex": "13. 一页纸讲凸优化",
    "Frontier": "14. 前沿：更快的线性规划、Hirsch 问题与唯一博弈猜想",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "In 1945 the economist George Stigler asked":
        "1945年，经济学家 George Stigler 问：养活一个人一年，最少要花多少钱？他有七十七种食物和九种营养素，一个人每种营养都要摄入足够。"
        "<bookmark mark='a'/>凭着试算和洞察，他找到一份每年三十九美元九十三美分的食谱，按1939年的价格计，主要是小麦粉、卷心菜和炼乳。他写道，"
        "没有直接的办法找到真正的最小值。<bookmark mark='b'/>两年后，George Dantzig 发明了这样的办法。Jack Laderman 的团队用台式计算器，"
        "手工执行他的单纯形法，<bookmark mark='c'/>大约花了一百二十个人日的算术，得到三十九美元六十九美分。而且它带来了 Stigler 不可能有的东西："
        "一个证明，证明没有更便宜的食谱。<bookmark mark='d'/>这个证明，这一部分称之为对偶，才是经久不衰的思想。",
    "This part is about choosing the best":
        "这一部分讲的是如何选出最好的，以及我们能得到的三种答案。<bookmark mark='a'/>对线性规划，也就是多面体上的最优点，有快速的算法，"
        "以及附带证明的精确答案。<bookmark mark='b'/>对带整数选择的问题，比如旅行商问题，求精确答案是 NP 难的；我们退而求其次，用有保证的算法，"
        "以及比保证承诺的做得更好的启发式方法。<bookmark mark='c'/>而对看不见未来就要做出的决定，比如缓存该淘汰哪一页，我们拿自己和一位"
        "什么都看得见的先知比较，并证明自己永远不会落后太多。",
    "Part 23 of Computer Science, Built: Optimization.":
        "计算机科学，从零搭建，第23部分：优化。<bookmark mark='a'/>这一部分包括：线性规划、单纯形法与对偶；为什么单纯形法在理论上是指数的、"
        "在实践中却很快，以及在它之后出现的多项式方法；整数规划，以及它何时是容易的；覆盖问题、旅行商问题、背包问题和最大割的近似算法；在线算法"
        "与乘性权重；以及一页纸讲完的凸优化。",
    # ------------------------------------------------------------------ LinearPrograms
    "Chapter one. Linear programs.": "第1章。线性规划。",
    "A linear program asks for the largest value":
        "线性规划要求在一组线性不等式的约束下，求一个线性函数的最大值。<bookmark mark='a'/>这是一个小例子，Vašek Chvátal 教科书中的第一个"
        "例子：三种产品，利润分别是五、四、三，用三种稀缺资源制成；左边是每种产品所需的资源量，右边是供应量。<bookmark mark='b'/>写成矩阵形式："
        "在 A x 不超过 b、x 非负的条件下，最大化 c 转置 x。<bookmark mark='c'/>Leonid Kantorovich 在1939年为列宁格勒的一家胶合板托拉斯"
        "制定计划时，提出了这类问题。<bookmark mark='d'/>George Dantzig 在1947年为美国空军做调度时遇到了它们，那时“规划”这个词还只是"
        "“计划”的意思。<bookmark mark='e'/>Kantorovich 和 Tjalling Koopmans 因这项工作分享了1975年的诺贝尔经济学奖；众所周知，Dantzig "
        "没有得奖。",
    "Most of the work of linear programming is modelling":
        "线性规划的大部分工作在于建模：决定变量是什么。<bookmark mark='a'/>这是 Kantorovich，以及1941年独立地由 Frank Hitchcock 研究过的"
        "那类问题。两家工厂分别生产三十和四十个单位；三家商店分别需要二十、二十五和二十五；每条道路有每单位的运费。<bookmark mark='b'/>每条"
        "道路一个变量：沿它运送的数量。<bookmark mark='c'/>在每家工厂的产能和每家商店的需求约束下，最小化总费用。<bookmark mark='d'/>让每家"
        "商店都从最便宜的工厂进货，要花三百五十五美元，但这要求工厂 B 供应五十个单位，而 B 只能生产四十个。<bookmark mark='e'/>最优解花费"
        "三百六十五美元：商店三由两家工厂分担，有十个单位走了更贵的那条路。<bookmark mark='f'/>几个小技巧能把多得多的问题化成这种形式。一个等式"
        "就是两个不等式。可以为负的变量，是两个非负变量之差。要最小化几个线性费用中最大的那个，就添一个变量 t，要求每个费用都不超过 t，再最小化 t。"
        "绝对值也是同样的做法。这就是为什么运筹学中有那么多内容就是线性规划。",
    "Each inequality cuts space in half":
        "每个不等式把空间切成两半，满足所有不等式的点构成一个凸多面体。<bookmark mark='a'/>对我们的三种产品，它就是这个三维立体，坐标轴平面是它"
        "的三面墙。<bookmark mark='b'/>它有六个顶点。<bookmark mark='c'/>目标函数的等值集，也就是利润相同的点，是一族平行的平面。<bookmark "
        "mark='d'/>沿利润增加的方向推动这个平面，直到它即将离开多面体。它最后碰到的点是一个顶点：第一种产品两个单位、第三种一个单位，利润为十三。"
        "<bookmark mark='e'/>情况总是如此：多面体上的线性函数在某个顶点取到最大值，所以只有有限个地方需要查看。难处在于，高维的多面体可以有"
        "天文数字般多的顶点。",
    # ------------------------------------------------------------------ Simplex
    "Chapter two. The simplex method.": "第2章。单纯形法。",
    "Dantzig's simplex method walks from corner to corner.":
        "Dantzig 的单纯形法从一个顶点走到另一个顶点。<bookmark mark='a'/>从某个顶点出发；原点，什么都不生产，就是一个顶点。<bookmark "
        "mark='b'/>在当前顶点，查看从它出发的各条边。有没有哪条是上坡的，能增加利润？<bookmark mark='c'/>如果有，就沿它走，直到碰到下一个顶点。"
        "这里，路径从零利润走到十二点五，只生产第一种产品，然后到十三。<bookmark mark='d'/>当没有上坡的边时，就完成了。微妙之处在于：一个局部"
        "检查证明了全局最优，因为在凸区域中，没有改进边的顶点在任何地方都无法被超越。<bookmark mark='e'/>这里走了两步。",
    "In algebra, the walk is a sequence of pivots.":
        "在代数上，这条路径是一连串的转轴。<bookmark mark='a'/>给每个不等式添一个松弛变量，即每种资源未用掉的数量，约束就变成了等式。松弛变量"
        "本身构成第一个基：原点，所有资源都未使用。<bookmark mark='b'/>最下面一行是目标函数。负的元素意味着增加那个变量会提高利润；Dantzig 规则"
        "选最负的那个，这里是第一种产品。<bookmark mark='c'/>它能增加多少？比值检验把每个右端项除以该列的元素，取最小者：第一种资源最先用完，"
        "在二点五处。<bookmark mark='d'/>转轴就是高斯消元的一步，把这一列变成单位向量。<bookmark mark='e'/>再一次转轴引入第三种产品，现在最下面"
        "一行没有负元素了。利润是十三，而松弛变量各列下面的数，一、零、一，是各资源的价格；下一章会说明，它们就是一个证明。",
    "Which edge should the walk take?":
        "路径应该走哪条边？<bookmark mark='a'/>Dantzig 规则取最陡的系数。<bookmark mark='b'/>在退化顶点处，紧约束比维数所需的更多，一次转轴"
        "可能改变了基却没有移动；规则选得不巧，方法会在同样的几个基之间永远循环。<bookmark mark='c'/>Robert Bland 1977年的规则总是选下标最小的"
        "可选变量，可以证明它永不循环。<bookmark mark='d'/>工业级求解器使用更聪明的规则，比如最陡边规则，并且不显式保存单纯形表，而是把它表示为"
        "基的 LU 分解，每次转轴后更新。<bookmark mark='e'/>单纯形法被评为二十世纪最重要的十个算法之一。是否存在某种转轴规则总能在多项式步内"
        "结束，至今仍不知道；第4章会说明为什么这个问题很微妙。",
    # ------------------------------------------------------------------ Duality
    "Chapter three. Duality.": "第3章。对偶。",
    "How could anyone prove that thirteen":
        "怎样才能证明十三就是可能的最大利润？<bookmark mark='a'/>把每个约束乘以一个非负数，再加起来。<bookmark mark='b'/>如果合并后的左边"
        "至少达到目标函数的系数五、四、三，那么对任何可行的计划，利润都不超过合并后的右边。<bookmark mark='c'/>第一个约束乘以三得到六、九、三，"
        "覆盖了五、四、三，所以利润至多为十五。第三个约束乘以三分之五，证明利润至多十三又三分之一。第二个约束乘以四分之五则不行：它覆盖不了第二、"
        "第三种产品的系数。而第一个约束加上第三个约束，恰好证明了十三。<bookmark mark='d'/>寻找最好的界，本身就是一个线性规划，即对偶问题：在"
        "覆盖条件下，最小化五 y 一加十一 y 二加八 y 三。",
    "So every linear program has a twin.":
        "所以每个线性规划都有一个孪生兄弟。<bookmark mark='a'/>原始问题对 x 求最大，对偶问题对 y 求最小，矩阵被转置，b 和 c 的角色互换。"
        "<bookmark mark='b'/>弱对偶就是我们刚才的论证：每个可行计划的收益都不超过每个可行的界。<bookmark mark='c'/>强对偶说得更多：在最优处"
        "两者相等，所以最好的界总是紧的。John von Neumann 在1947年与 Dantzig 的一次谈话中看出了这一点，Gale、Kuhn 和 Tucker 在1951年证明了"
        "它。<bookmark mark='d'/>证明的引擎是1902年的 Farkas 引理：一个线性方程组要么有非负解，要么有一个简短的证书说明它没有，二者绝不同时"
        "成立。<bookmark mark='e'/>从几何上看，凸锥之外的点总能用一个超平面与它分开。<bookmark mark='f'/>它的实际意义是：每个最优解都附带一个"
        "证明，怀疑者只需做一次矩阵乘向量就能检验。",
    "The dual variables mean something.":
        "对偶变量是有含义的。<bookmark mark='a'/>最优的 y i 是资源 i 的影子价格：多一个单位的这种资源，最大利润会增加多少。<bookmark "
        "mark='b'/>这是一个局部的价格。我们给第一种资源加一个单位再重新求解：利润增加了三分之一，而不是一，因为多出的这一单位改变了哪些约束是紧的。"
        "<bookmark mark='c'/>互补松弛把两个规划联系在一起：没有用完的资源价格为零；所耗资源的价值高于其利润的产品不会被生产。<bookmark "
        "mark='d'/>这里第二种资源还剩一个单位，所以它的价格为零；第二种产品所耗资源的价值比它的利润多三，所以最优解不生产它。<bookmark "
        "mark='e'/>每个求解器都会报告这些价格，经济学家把它们解读为竞争市场会定出的价格。",
    # ------------------------------------------------------------------ KleeMinty
    "Chapter four. Exponential in theory, fast in practice.": "第4章。理论上是指数的，实践中却很快。",
    "How many pivots can the simplex method need?":
        "单纯形法最多可能需要多少次转轴？<bookmark mark='a'/>1972年，Victor Klee 和 George Minty 构造了一个坏例子：一个被压扁、不再方正"
        "的立方体。<bookmark mark='b'/>每个坐标的上下界都稍稍依赖于前一个坐标，这使得每个面都略微倾斜。<bookmark mark='c'/>在这个立方体上，"
        "Dantzig 规则在到达顶端之前会访问每一个顶点，每一步都在上升。在 n 维中，那是二的 n 次方个顶点。<bookmark mark='d'/>这里是三维：七次"
        "转轴，经过全部八个顶点。",
    "We ran our simplex on Klee–Minty cubes":
        "我们在最高十二维的 Klee–Minty 立方体上运行了自己的单纯形法。<bookmark mark='a'/>Dantzig 规则每次都恰好需要二的 n 次方减一次转轴："
        "十二维时是四千零九十五次。<bookmark mark='b'/>Bland 规则在这个立方体上表现好一些，但在它自己的变体上同样是指数的，David Avis 和 "
        "Chvátal 证明了这一点。<bookmark mark='c'/>最大改进规则试遍每条边、取增益最大的那条，它一次转轴就解决了这个立方体；Robert Jeroslow "
        "在1973年构造了也能打败它的立方体。<bookmark mark='d'/>这种模式重复了几十年：几乎每一个被提出的转轴规则都有了自己的坏例子，最后一个著名"
        "的是2011年的 Zadeh 规则。<bookmark mark='e'/>还没有任何已知的转轴规则能在多项式时间内运行。",
    "Yet the simplex method is fast on real problems":
        "然而单纯形法在实际问题上很快，通常只需要约束数的一个小倍数。为什么？<bookmark mark='a'/>在随机的稠密规划上，我们的单纯形法用的转轴"
        "次数还不到约束数的一半：一百六十个约束平均三十四次。<bookmark mark='b'/>Daniel Spielman 和滕尚华在2001年用平滑分析解释了这一点："
        "取任何一个线性规划，哪怕是最坏的，给它的数据加上一点高斯噪声。那么转轴次数的期望就是规模以及噪声大小倒数的多项式。<bookmark "
        "mark='c'/>坏实例是刀锋上的构造，摇一摇它们就倒了。在我们的十维立方体上，极小的噪声什么也改变不了，但百分之十的噪声把一千零二十三次转轴"
        "减到大约四百次，百分之三十则减到大约七十五次。<bookmark mark='d'/>他们因此获得了哥德尔奖，平滑分析如今还解释了为什么其他一些最坏情况下"
        "很差的算法在实践中却管用。",
    # ------------------------------------------------------------------ PolyTime
    "Chapter five. Polynomial time: ellipsoids and the central path.": "第5章。多项式时间：椭球与中心路径。",
    "In 1979 Leonid Khachiyan proved":
        "1979年，Leonid Khachiyan 证明了线性规划可以在多项式时间内求解，用的方法根本不沿边行走。<bookmark mark='a'/>换个问法：多面体是不是"
        "空的？从一个大到足以包含它的球开始。<bookmark mark='b'/>看球心。如果它可行，就完成了。如果不可行，那里就有某个约束被违反，而这个约束"
        "说明多面体整个位于过球心的某条直线的一侧。<bookmark mark='c'/>用包含剩下那一半的最小椭球代替它，然后重复。<bookmark mark='d'/>每一步"
        "都把体积缩小一个固定的倍数，e 的负二 n 加二分之一次方，所以经过多项式步之后，椭球会比用这些数据构成的任何非空多面体都小。<bookmark "
        "mark='e'/>这里，九次切割就到达了一个可行点。优化问题可以通过对目标值二分查找，或者把目标函数作为又一个切割加进去，归结为可行性问题。",
    "How many steps? <bookmark mark='a'/> As the feasible region gets thinner":
        "需要多少步？<bookmark mark='a'/>可行域越薄，切割次数就随它宽度倒数的对数增长：在二维中，宽度每缩小十倍，平均多大约十七次。<bookmark "
        "mark='b'/>一般地，界是 n 的平方乘以输入的位数，是多项式的，《纽约时报》把它登上了头版。<bookmark mark='c'/>在实践中，这个方法比单纯形法"
        "慢得多，没有人用它求解线性规划。<bookmark mark='d'/>它留下的遗产是一个定理。Martin Grötschel、László Lovász 和 Alexander Schrijver "
        "证明，这个方法从不需要把约束写出来，只需要一种找出被违反约束的办法。所以，即使一个线性规划有指数多个约束，只要能高效地找到被违反的约束，"
        "它仍然可以在多项式时间内求解。分离和优化一样容易。",
    "The method that made polynomial time practical":
        "让多项式时间变得实用的方法，1984年来自贝尔实验室的 Narendra Karmarkar。<bookmark mark='a'/>不沿着边界走，而是严格地待在内部。"
        "<bookmark mark='b'/>给目标函数加上一个障碍项，即各松弛量的对数之和，它在每面墙上都趋于无穷，并用参数 t 给真正的目标函数加权。<bookmark "
        "mark='c'/>对每个 t 都有一个最优点；随着 t 增大，这些点描出一条光滑的曲线，即中心路径，从多面体的中间通向最优顶点。<bookmark "
        "mark='d'/>沿着它走：把 t 增大一点，用几步牛顿法回到路径上，然后重复。与最优值的差距至多是约束数除以 t。<bookmark mark='e'/>理论上"
        "保证的是 m 的平方根乘以精度倒数的对数；实践中，无论规模多大，都只需要二十到八十步牛顿迭代。<bookmark mark='f'/>这正是 AI 系列中的"
        "牛顿法，每个严肃的求解器都把它和单纯形法一起运行。",
    # ------------------------------------------------------------------ Unimodular
    "Chapter six. When the vertices are integers.": "第6章。当顶点都是整数时。",
    "Most integer programs are hard":
        "大多数整数规划都很难，但有些其实是伪装起来的线性规划。<bookmark mark='a'/>以第18部分的二分图匹配为例。给每条边一个介于零和一之间的变量，"
        "并要求每个顶点处各边之和至多为一。<bookmark mark='b'/>约束矩阵每条边一列，在它的两个端点处各有一个一：这就是关联矩阵。<bookmark "
        "mark='c'/>对二分图，它是全单模的：每个方子矩阵的行列式都是零、一或负一。我们检查了这个矩阵的每一个方子矩阵。<bookmark mark='d'/>于是由"
        "克莱姆法则，多面体的每个顶点都有整数坐标，因为每个坐标都是行列式之比，而分母是正负一。<bookmark mark='e'/>所以终止于顶点的单纯形法，"
        "免费地解决了整数问题。在一百个随机赋权的二分图上，没有一个最优顶点有分数坐标。",
    "Outside bipartite graphs it fails":
        "离开二分图它就失效了，最小的反例是一个三角形。<bookmark mark='a'/>它的关联矩阵行列式为二。<bookmark mark='b'/>线性规划乐于在每条边上"
        "放二分之一，总共一点五，尽管三角形中任何匹配都只有一条边。<bookmark mark='c'/>在一百个随机赋权的非二分图上，四分之一的最优顶点是分数的。"
        "<bookmark mark='d'/>Jack Edmonds 在1965年修补了它：为每个奇数大小的顶点集添一个约束，说它内部至多含有其一半、向下取整那么多条边，"
        "多面体就又是整的了。<bookmark mark='e'/>这样的约束有指数多个，但被违反的约束可以很快找到，所以由第5章的定理，这个规划仍然可以在多项式"
        "时间内求解。",
    "The same miracle explains other results":
        "同样的奇迹解释了我们已经知道的其他结果。<bookmark mark='a'/>最大流是一个线性规划，它的矩阵是有向关联矩阵，是全单模的。<bookmark "
        "mark='b'/>它的对偶是最小割，所以第18部分的最大流最小割定理，就是伪装起来的线性规划对偶。<bookmark mark='c'/>而整数容量总有整数的最大流，"
        "正如 Ford 和 Fulkerson 的增广路径所找到的那样。<bookmark mark='d'/>调度中出现的区间矩阵，以及网络矩阵，也都是全单模的。<bookmark "
        "mark='e'/>Paul Seymour 在1980年证明，每个全单模矩阵都是由网络矩阵和两个小的例外拼装而成的，所以一个矩阵是否具有这种性质，可以在多项式"
        "时间内检验。",
    # ------------------------------------------------------------------ IntegerPrograms
    "Chapter seven. Integer programming.": "第7章。整数规划。",
    "Insist that the answer be made of whole things":
        "坚持答案必须由整个的东西组成，线性规划就变成了 NP 难的。标准的攻法仍以线性规划为向导。<bookmark mark='a'/>这是一个背包问题：八件物品，"
        "各有价值和重量，容量为八十。把它松弛：允许物品按分数取。这个线性规划很容易，按单位重量的价值贪心即可，它的最优值给出任何整数选择所能达到的"
        "上界。<bookmark mark='b'/>根节点的界是一百八十四，有一件物品只取了一部分。在这件物品上分支：一个子问题取它，另一个不取，各有自己的界。"
        "<bookmark mark='c'/>任何一个界不能超过迄今最好整数解的节点，都不经探索就被剪掉。<bookmark mark='d'/>这里，最好的答案一百七十四在"
        "二十四个节点之后被找到并被证明最优，而不是检查全部二百五十六种可能的选择。Ailsa Land 和 Alison Doig 于1960年在伦敦政治经济学院发明了"
        "这个方法。",
    "How well does it scale?":
        "它的扩展性如何？<bookmark mark='a'/>在最多一百六十件物品、有二的一百六十次方种选择的随机背包上，分支定界平均只需要几百个节点，因为线性界"
        "与真值相差不过百分之一二。坏实例是存在的，但界承担了大部分工作。<bookmark mark='b'/>Ralph Gomory 在1958年展示了如何用切割代替分支："
        "推导出一个新的不等式，每个整数解都满足它，而分数最优解违反它；把它加进去，再求解。<bookmark mark='c'/>现代求解器两者都做，即分支切割，"
        "再加上层层的预处理和启发式方法。<bookmark mark='d'/>Robert Bixby 度量过它们的进步：1991年到2007年间，仅算法本身就快了大约三万倍，"
        "这还没算硬件的提升。<bookmark mark='e'/>它们为航空公司排机组，调度电网，匹配肾脏捐献者，在芯片上布置元件。",
    "Knapsack also shows a different kind of compromise.":
        "背包问题还展示了另一种妥协。<bookmark mark='a'/>第19部分用动态规划精确地解决了它，时间与容量成正比，而容量可以大得惊人。<bookmark "
        "mark='b'/>Oscar Ibarra 和 Chul Kim 把每个价值向下取整到 epsilon 乘以最大价值再除以 n 的倍数，然后对价值做动态规划，精确地求解取整后的"
        "问题。<bookmark mark='c'/>每件物品损失不到一个取整单位，所以整个答案至多损失 epsilon 乘以最优值，而表格有 n 的平方除以 epsilon 个元素。"
        "任意你想要的精度，时间是 n 和 epsilon 倒数的多项式：一个完全多项式时间近似方案。<bookmark mark='d'/>在一个困难的强相关实例上，即使 "
        "epsilon 取十分之九，只保证最优值的十分之一，它也找到了百分之九十九点三；从十分之一往下，它找到的就是精确最优解，而工作量只与 epsilon "
        "的倒数成正比地增长。",
    # ------------------------------------------------------------------ Approximation
    "Chapter eight. Approximation: covers.": "第8章。近似：覆盖问题。",
    "When the exact answer is out of reach":
        "当精确答案遥不可及时，就要一个可证明与它接近的答案。<bookmark mark='a'/>顶点覆盖是一组触及每条边的顶点，找出最小的那组是 NP 难的。"
        "<bookmark mark='b'/>这里有一个两行的算法。取任意一条两端都未被覆盖的边，把两端都加进来。重复，直到每条边都被覆盖。<bookmark "
        "mark='c'/>它取的这些边两两没有公共顶点，而任何覆盖都必须至少包含其中每条边的一端，所以最优解至少是我们所取的一半。这就是一个二倍的保证，"
        "而且不需要知道最优解就证明了。<bookmark mark='d'/>这里它取了八个顶点，而最优是六个。<bookmark mark='e'/>第二种办法用线性规划：给每个"
        "顶点一个分数，要求每条边两端的分数之和至少为一，并最小化总和。然后保留分数至少为二分之一的每个顶点。<bookmark mark='f'/>松弛问题的顶点"
        "只取零、二分之一和一这几个值。这里它处处取二分之一，总共四点五，这是最优解的一个下界，而取整保留了全部九个顶点。同样至多是线性规划值的两倍，"
        "所以至多是最优解的两倍。",
    "We ran both on a hundred random graphs":
        "我们在一百个十六个顶点的随机图上运行了这两种算法，并与暴力搜索得到的精确最优解比较。<bookmark mark='a'/>两者都稳稳地落在二倍的保证之内，"
        "尽管在别的图上两者都是紧的。<bookmark mark='b'/>没有人知道如何做得比二减去一个趋于零的量更好；Subhash Khot 和 Oded Regev 证明了，如果"
        "唯一博弈猜想成立，就没有人能做到。<bookmark mark='c'/>线性规划也帮不上更多的忙：在完全图上，它的值是 n 的一半，而最优解是 n 减一，整性"
        "间隙为二。",
    "Set cover is the general form":
        "集合覆盖是一般形式：用尽可能少的给定集合覆盖一个元素全集。<bookmark mark='a'/>贪心算法反复选取覆盖最多尚未覆盖元素的那个集合。<bookmark "
        "mark='b'/>David Johnson 和 László Lovász 在1970年代证明，贪心所用的集合数至多是第 n 个调和数乘以最优值，大约是 n 的自然对数。<bookmark "
        "mark='c'/>证明把每个选中集合的代价分摊到它新覆盖的元素上，并说明任何一个最优集合中的元素总共至多支付 H n。<bookmark mark='d'/>这个界"
        "几乎是紧的。在这个陷阱里，两行就覆盖了一切，但贪心被大小逐次减半的各列引诱，用了七个集合，而两个就够了。<bookmark mark='e'/>在随机实例上，"
        "它平均只差百分之六。Uriel Feige 证明了，做得比对数更好是困难的，所以任何人都会先试的贪心，本质上已经是最好的了。",
    # ------------------------------------------------------------------ Tsp
    "Chapter nine. The travelling salesman.": "第9章。旅行商问题。",
    "The travelling salesman wants the shortest tour":
        "旅行商想要一条经过所有城市的最短回路。<bookmark mark='a'/>一般情况下，任何近似因子都不可能：给图中不存在的道路赋上巨大的长度，那么任何"
        "能做到 c 倍以内的算法，都会告诉你这个图有没有哈密顿回路。<bookmark mark='b'/>所以假定真实的距离，它们满足三角不等式：直走永远不比绕路长。"
        "<bookmark mark='c'/>这样就有了一个二倍的算法。最小生成树不比最优回路长，因为从回路中去掉一条边就剩下一棵生成树。绕着树走一圈，每条边走两次，"
        "跳过已经访问过的城市。<bookmark mark='d'/>Nicos Christofides，以及独立地 Anatoliy Serdyukov，在1976年做得更好。树中奇数度的顶点可以"
        "用一个至多为最优值一半的匹配配成对。把它加进来，每个顶点的度都成了偶数，于是有一条欧拉回路；再走捷径。<bookmark mark='e'/>至多是最优值的"
        "二分之三。<bookmark mark='f'/>而这就是最优回路本身，来自 Held 和 Karp 的动态规划。",
    "How do they do in general?":
        "一般情况下它们表现如何？我们在四十个十二城市的随机实例上运行了它们，与精确最优解比较。<bookmark mark='a'/>双树平均比最优高百分之二十一，"
        "Christofides 高百分之七。但表现最好的方法根本没有保证：最近邻之后再做二交换，不断寻找交换后能缩短回路的两条边，把它们解开，直到没有交换能"
        "改进为止。它平均只比最优高百分之一多一点。<bookmark mark='b'/>保证与实践之间的这种差距贯穿了整整这一章。<bookmark mark='c'/>四十五年里"
        "没有人改进过二分之三，直到2021年，Anna Karlin、Nathan Klein 和 Shayan Oveis Gharan 把它改进了十的负三十六次方，一个极小的数，却是"
        "一大步概念上的进展。<bookmark mark='d'/>对于平面上的城市，Sanjeev Arora 和 Joseph Mitchell 找到了一个近似方案：对你选的任何 epsilon，"
        "都能做到一加 epsilon 倍以内。",
    "And at scale?":
        "规模大了又如何？<bookmark mark='a'/>十五个城市的精确动态规划在 Python 中就已经要零点几秒，每多一个城市时间就翻倍。<bookmark "
        "mark='b'/>对三百个随机城市，最近邻构造出长度十六点二的回路，二交换在十分之一秒内把它缩短到十三点九。<bookmark mark='c'/>随机点的最优"
        "回路长度接近零点七一二四乘以 n 的平方根，这是1959年的一个定理，它在这里预测大约十二点三。二交换比这个估计高百分之十二，而这个估计忽略了"
        "正方形的边界，所以真实的差距要小一些。<bookmark mark='d'/>Lin–Kernighan 移动，以及 Keld Helsgaun 对它们的实现，能做到相差不到百分之一。"
        "<bookmark mark='e'/>而建立在 Gomory 那样的线性规划割平面之上的 Concorde 程序，已经证明了经过八万五千九百个城市的回路是最优的，这些城市"
        "是一块电路板上的点。<bookmark mark='f'/>它的用途从送货车一直延伸到望远镜和基因组图谱。",
    # ------------------------------------------------------------------ MaxCut
    "Chapter ten. A random hyperplane: MAX-CUT.": "第10章。随机超平面：最大割。",
    "Here is one of the most elegant algorithms":
        "这是本课程中最优美的算法之一。<bookmark mark='a'/>最大割问题要求把图的顶点分成两边，使被切断的边尽可能多。它是 NP 难的。<bookmark "
        "mark='b'/>把每个顶点所在的一边写成正一或负一；一条边被切断，当且仅当它两端的乘积是负一。<bookmark mark='c'/>Michel Goemans 和 David "
        "Williamson 把这些符号松弛为单位向量，并按每条边两端向量分开的程度给它奖励。<bookmark mark='d'/>这是一个半定规划，是线性规划的近亲，可以"
        "高效求解。相邻顶点的向量在球面上彼此散开。<bookmark mark='e'/>对这个十二个顶点的图，松弛问题的值是十八点三，比真正的最大值十八略高。"
        "<bookmark mark='f'/>现在用一个过球心的随机平面切开球面，把平面两侧的顶点分别放到割的两边。",
    "Why is that good?":
        "为什么这样做好？<bookmark mark='a'/>夹角为 theta 的两个向量被随机平面分开的概率是 theta 除以 pi：平面的方向必须落在它们之间的楔形里。"
        "<bookmark mark='b'/>把这与松弛问题给这条边的奖励，即一减 cos theta 再除以二，相比较。它们的比值永远不小于大约零点八七八。<bookmark "
        "mark='c'/>最坏的情况是大约一百三十四度的夹角。<bookmark mark='d'/>所以逐条边来看，割的期望至少是松弛值的零点八七八倍，而松弛值至少是"
        "最优值。<bookmark mark='e'/>1995年之前，已知最好的保证是二分之一，来自把每个顶点随机放到一边。",
    "We tried it on thirty random graphs":
        "我们在三十个随机图上试了它，与检查每种划分得到的真正最大值比较。<bookmark mark='a'/>随机分边大约切到最大值的三分之二。一个随机超平面"
        "平均达到百分之九十六，最差的图也有百分之九十四，远在保证之上；两百个超平面中最好的那个在每个图上都找到了最优解。我们用简单的办法求解半定规划："
        "在单位向量上做梯度步。<bookmark mark='b'/>而这个常数并非偶然。Subhash Khot 和同事们在2004年证明，如果唯一博弈猜想成立，就没有人能在"
        "多项式时间内超过零点八七八。<bookmark mark='c'/>不依赖这个猜想，Johan Håstad 证明了超过十七分之十六是 NP 难的。<bookmark "
        "mark='d'/>先松弛为几何，再随机取整：这个模板如今贯穿了整个领域。",
    # ------------------------------------------------------------------ Online
    "Chapter eleven. Online: deciding without the future.": "第11章。在线：看不见未来的决策。",
    "So far every algorithm saw its whole input.":
        "到目前为止，每个算法都看得到完整的输入。而许多真实的决定，是在未来到来之前做出的。<bookmark mark='a'/>雪板买一副要十，租一天要一，而你不知道"
        "会下几天雪。<bookmark mark='b'/>用竞争比来评判一个策略：在最坏情况下，它比一个知道未来的人多付多少；那个人在雪季短时会一直租，在雪季长时"
        "会立刻买。<bookmark mark='c'/>先租九天，再买。如果雪季短，你付的和先知一样；如果雪季长，你付了十九而不是十。永远不超过两倍。<bookmark "
        "mark='d'/>没有确定性规则能做得更好，因为知道你规则的对手可以让雪季恰好在你买下的那天结束。<bookmark mark='e'/>但如果你以合适的概率在随机"
        "的一天买，对手就无从瞄准，期望比值降到 e 除以 e 减一，大约一点五八。我们对这条规则的模拟，在长雪季里付了十五点四，而先知付十。",
    "Caches face the same problem every nanosecond":
        "缓存每一纳秒都面临同样的问题：缓存满了，又来了一个新的行，哪个旧的该走？<bookmark mark='a'/>我们把第9部分 Job 的内存访问轨迹，十五万五千次"
        "访问、九十二个不同的行，在八到九十六行的缓存上，按几种策略重放了一遍。<bookmark mark='b'/>Laszlo Belady 在1966年证明，最优策略是淘汰下一次"
        "使用离现在最远的那一行。它是完美的，却无法在线实现，但它可以用来衡量其他所有策略。<bookmark mark='c'/>最近最少使用在这里与先知相差大约"
        "一点二倍到七倍，先进先出紧随其后。<bookmark mark='d'/>一旦缓存变大，随机化策略就胜出了：标记算法随机淘汰一个自当前阶段开始以来未被使用的页，"
        "甚至纯粹的随机淘汰也胜过 LRU。Job 在循环中扫过它的表，而循环恰恰是 LRU 最薄弱的地方，下一个例子会说明这一点。",
    "How bad can least recently used be?":
        "最近最少使用能有多糟？<bookmark mark='a'/>用一个四页的缓存，循环请求五个页。LRU 淘汰的页总是下一个就要请求的那一页，所以每次请求都缺页。"
        "<bookmark mark='b'/>先知淘汰最远才需要的那一页，大约每四次请求才缺页一次。<bookmark mark='c'/>Daniel Sleator 和 Robert Tarjan 在1985年"
        "用这个例子创立了竞争分析：LRU 和 FIFO 是 k-竞争的，而同样的对手能迫使每个确定性策略在每次请求时都缺页，所以没有哪个做得更好。随机化的标记"
        "算法不会这样落入陷阱，只付出一个对数因子，二倍的 H k。<bookmark mark='d'/>真实的程序比对手仁慈，这就是为什么从第9部分到第32部分，每一个"
        "缓存都运行着 LRU 的近似。",
    # ------------------------------------------------------------------ Weights
    "Chapter twelve. Multiplicative weights.": "第12章。乘性权重。",
    "One algorithm keeps turning up in this part's last chapters":
        "有一个算法在这一部分的最后几章里反复出现，在计算机科学的许多地方也是如此。<bookmark mark='a'/>每天有十位专家各自做出预测，你必须在知道谁对"
        "之前就按他们的建议行动。给每位专家一个权重，按权重的比例随机跟随一位。<bookmark mark='b'/>每天结束后，把每位说错了的专家的权重乘以一个略小于"
        "一的因子。<bookmark mark='c'/>这里有一位专家百分之四十五的时间出错，其他人百分之五十。几百轮之内，权重就找到了它。<bookmark mark='d'/>"
        "用遗憾来衡量：你比事后挑出的那位最好的专家差多少。<bookmark mark='e'/>对任何损失序列，哪怕是对手挑选的，遗憾都至多是 T 除以二乘以 log n "
        "的平方根。<bookmark mark='f'/>我们测得的遗憾始终在这个界之下，每轮的遗憾趋于零：从长远看，你做得和最好的专家一样好，却不需要知道是哪一位。",
    "The proof is four lines, and it is worth seeing once.":
        "证明只有四行，值得看一次。<bookmark mark='a'/>盯住总权重。它从 n 开始，每位专家一。<bookmark mark='b'/>到最后，它至少是最好的那位专家"
        "单独的权重，而那个权重每出一次错就被乘一次 e 的负 eta 次方。<bookmark mark='c'/>而在每一轮中，当我们按权重比例跟随专家时，总权重缩小的"
        "因子大约是 e 的负 eta 乘以这一轮我们的期望损失次方，外加 Hoeffding 不等式给出的一个小修正。<bookmark mark='d'/>把各轮串起来，两个事实"
        "就形成夹击：我们的损失不可能比最好专家的多太多，否则总权重就会跌到最好专家自己的权重之下。<bookmark mark='e'/>取对数，选择 eta 使两项平衡，"
        "遗憾就是 T 除以二乘以 log n 的平方根。<bookmark mark='f'/>这是一个势函数论证，就像第16和第17部分的均摊分析，同样的模式还证明了提升法和"
        "极小极大定理。",
    "The same few lines prove theorems.":
        "同样的几行代码能证明定理。<bookmark mark='a'/>在一个零和博弈中，让一方对自己的策略运行乘性权重，另一方总是给出最佳应对。<bookmark "
        "mark='b'/>双方的平均策略收敛到博弈的值，这里是零点四八四六，双方各自能保证的值之间的差距随之闭合。这就是 von Neumann 的极小极大定理，用运行"
        "一个算法来证明，而它又一次是线性规划的对偶。<bookmark mark='c'/>把权重放在训练样本上而不是专家上，就得到了提升法，AI 系列构造过它。"
        "<bookmark mark='d'/>把权重放在线性规划的约束上，就得到了求解流和装箱类问题的快速近似算法。<bookmark mark='e'/>Sanjeev Arora、Elad Hazan "
        "和 Satyen Kale 以这样的标题综述了它：一个元算法及其应用。",
    # ------------------------------------------------------------------ Convex
    "Chapter thirteen. Convex optimization in a page.": "第13章。一页纸讲凸优化。",
    "Linear programs are the simplest convex problems":
        "线性规划是最简单的凸问题，而第5章的内点法已经用到了一般的工具。<bookmark mark='a'/>这是一个两变量的光滑凸函数，来自 Boyd 和 Vandenberghe "
        "教科书中的对数和指数函数，被拉伸得山谷很窄。<bookmark mark='b'/>梯度下降沿下坡方向前进，用回溯法选择每一步的步长。<bookmark mark='c'/>"
        "在狭窄的山谷里，下坡方向主要横穿山谷，而不是沿着山谷，所以路径呈之字形：要四十步才达到十位精度。<bookmark mark='d'/>牛顿法利用二阶导数，在"
        "当前点用一个二次函数拟合原函数，然后跳到这个二次函数的最小点。<bookmark mark='e'/>四步。在最优点附近，正确的位数每一步都翻倍。<bookmark "
        "mark='f'/>但每一步牛顿法都要解一个以海森矩阵为系数的线性方程组，有十亿个变量时这毫无希望，这就是为什么 AI 系列中训练神经网络用的是梯度方法。",
    "Convex optimization fits on a page.":
        "凸优化可以写在一页纸上。<bookmark mark='a'/>在凸集上最小化凸函数，每个局部最小值都是全局最小值，并有一个对偶证书来证明它。<bookmark "
        "mark='b'/>在最优点，Karush–Kuhn–Tucker 条件成立：目标函数的梯度被紧约束梯度的一个非负组合所平衡。<bookmark mark='c'/>这些乘子就是第3章的"
        "影子价格，推广了而已。<bookmark mark='d'/>问题类形成一个阶梯：线性规划、凸二次规划、二阶锥规划，以及像第10章那样的半定规划。<bookmark "
        "mark='e'/>Yurii Nesterov 和 Arkadi Nemirovski 证明，内点法能在多项式时间内把它们全都求解到任意精度。<bookmark mark='f'/>没有凸性，局部"
        "最小值就到处都是，一般问题是 NP 难的；尽管如此，神经网络照样被训练出来了，这是 AI 系列的谜题之一。<bookmark mark='g'/>正如 Tyrrell "
        "Rockafellar 所说，优化中的分水岭不在线性与非线性之间，而在凸与非凸之间。",
    # ------------------------------------------------------------------ Frontier
    "Chapter fourteen. Frontier":
        "第14章。前沿：更快的线性规划、Hirsch 问题，以及唯一博弈猜想。",
    "The first front is speed.":
        "第一条战线是速度。<bookmark mark='a'/>对 n 个变量的线性规划，Karmarkar 的方法大约需要 n 的三点五次方次运算。Pravin Vaidya 把它降到 n 的"
        "二点五次方：步数更少，并且注意到相继的牛顿步几乎不改变矩阵，所以它的逆可以更新而不必重新计算。<bookmark mark='b'/>2019年，Michael Cohen、"
        "Yin Tat Lee 和 Zhao Song 把这个思路推到了自然的终点：n 的 omega 次方，其中 omega 约为二点三七，是矩阵乘法的指数。一年后，Jan van den Brand 把它变成"
        "了确定性的。如今求解一个线性规划，代价大约和两个矩阵相乘一样，而下限，仅仅读入输入，是 n 的平方。<bookmark mark='c'/>同样的工具催生了这十年"
        "最重要的算法成果。2022年，Li Chen、Rasmus Kyng、Yang Liu、Richard Peng、Maximilian Probst Gutenberg 和 Sushant Sachdeva 在几乎线性的时间内"
        "解决了最大流，m 的一加一个趋于零的指数次方。<bookmark mark='d'/>它是作用在第18部分流规划上的内点法，每一步对流的改变都非常小，巧妙的动态"
        "数据结构就能让它保持最新。",
    "The second front is the simplex method's own question.":
        "第二条战线是单纯形法自己的问题。会不会有一个转轴规则总在多项式步内结束？<bookmark mark='a'/>那样的话，每个多面体的任意两个顶点之间都必须"
        "有一条短路径。这是一个有二十四个随机面、四十四个顶点的多面体；它相距最远的两个顶点相隔八条边。<bookmark mark='b'/>1957年，Warren Hirsch "
        "猜想这个距离永远不超过面数减去维数。<bookmark mark='c'/>在随机多面体上，它轻松成立：直径大致随面数的平方根增长，远低于这个界。<bookmark "
        "mark='d'/>但在2010年，Francisco Santos 构造了一个反例：一个四十三维、八十六个面的多面体，直径至少为四十四。<bookmark mark='e'/>已知最好的"
        "上界甚至不是多项式的：Gil Kalai 和 Daniel Kleitman 的 n 的 log d 加二次方。<bookmark mark='f'/>直径是否以某个多项式为界，即多项式 "
        "Hirsch 猜想，仍未解决；在它解决之前，没有人能指望证明某个单纯形规则是多项式的。",
    "The third front is the other side of approximation":
        "第三条战线是近似的另一面：证明没有什么能做得更好。<bookmark mark='a'/>这是这一部分的问题，列出了已知最好的算法，以及低于它就已知很难近似"
        "的阈值。<bookmark mark='b'/>工具是1992年的 PCP 定理：任何证明都可以改写成这样，只检查随机几位的验证者，就能以很大的概率抓住任何错误。"
        "<bookmark mark='c'/>它把近似变成了判定：近似得比某个阈值更好，就能解决一个 NP 完全问题。Johan Håstad 证明，对 MAX-3SAT，平凡的八分之七"
        "恰恰就是对的。第27部分会构造这个定理。<bookmark mark='d'/>对其他问题还有差距；2002年，Subhash Khot 提出了唯一博弈猜想。如果它成立，"
        "顶点覆盖就无法超过二，最大割无法超过 Goemans 和 Williamson 的零点八七八，所以这一部分的这两个算法都是最优的。2018年，Khot、Dor Minzer "
        "和 Muli Safra 证明了一个较弱的近亲，二对二定理，它已经让顶点覆盖在二的平方根以下变得困难。<bookmark mark='e'/>而 Prasad Raghavendra "
        "证明，如果这个猜想成立，一个半定规划就同时是每一个约束满足问题的最佳可能算法。",
    "Here is where things stand.":
        "现状如下。<bookmark mark='a'/>线性规划有没有强多项式算法，即步数只依赖于变量数和约束数、而不依赖于系数有多少位？最大流有一个；一般的线性"
        "规划没有，Steve Smale 把这个问题列入了他为本世纪提出的问题之中。<bookmark mark='b'/>每个多面体的直径都以一个多项式为界吗？<bookmark "
        "mark='c'/>唯一博弈猜想是真的吗？<bookmark mark='d'/>这一部分的研究题选的是第二个。",
    # ------------------------------------------------------------------ Outro
    "What we built in this part.":
        "这一部分我们构造了什么。线性规划，以及沿着多面体的边行走的单纯形法。对偶，它把每个最优解变成一份怀疑者可以检验的证书。让这条路径变成指数长"
        "的 Klee–Minty 立方体，以及解释它在实践中为何从不如此的平滑分析。椭球与中心路径。让某些整数规划免费可解的全单模性，以及处理其余问题的分支"
        "定界。有证明的近似：覆盖、回路、背包，以及穿过一个向量球面的随机超平面。还有看不见未来的决策：租雪板、页面置换和乘性权重。",
    "Where this comes back.":
        "它们会在哪里再出现。第27部分构造这一部分困难性结果背后的 PCP 定理，以及唯一博弈猜想。第32部分的内核用 CLOCK 置换页面，它是最近最少使用的"
        "一种廉价近似。第45部分的云把虚拟机装到服务器上，这是一个每秒都在用启发式方法求解的整数规划；第48部分在线地做负载均衡。第52部分解释为什么"
        "线性规划求解器要与浮点数搏斗。第57部分则把乘性权重变成一套学习理论。AI 系列自始至终都在使用这一部分的工具：梯度下降和牛顿法、提升法，以及"
        "让训练变得可行的凸损失函数。",
    "In practice. HiGHS":
        "在实践中。HiGHS、Gurobi、CPLEX 和 OR-Tools 在有数百万变量的问题上运行单纯形法、障碍法和分支切割。航空公司排班机组，承运商规划车辆路线，"
        "供应链用整数规划做计划。电网和肾脏交换由优化来出清，并给出对偶价格。每个缓存都在做在线决策，而每个模型都由梯度下降的后代训练出来。",
    "Six problems, with full solutions":
        "六道习题，完整解答在这一部分的笔记里。可以在任何一道上暂停。第五道是构造题：用 Pebble 语言、以精确分数实现单纯形法，在模拟器上运行。最后"
        "一道标有星号，是研究题：它的答案尚不知道，笔记里说明了从哪里入手。",
    "Next time, algorithms in practice.":
        "下一次，实践中的算法。大 O 隐藏了常数，而在生产环境里，决定一切的是常数和机器。真实代码中的日常工具：前缀和、Fenwick 树和线段树、双指针、"
        "单调栈和位运算技巧。然后是算法工程：一个教科书式的哈希表或二分查找，只要尊重第二幕讲过的缓存、分支预测器和向量单元，就能快上许多倍，以及如何"
        "诚实地测量这一点。第24部分，实践中的算法。",
    "The books and papers this part follows":
        "这一部分所依据的书和论文都在屏幕上，也在笔记里。感谢观看。",
}

PHRASES = {}
