"""Chinese narration for cs52: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第52部分：用实数计算"

CHAPTERS = {
    "Hook": "世纪十大算法",
    "Conditioning": "1. 条件与稳定性",
    "Backward": "2. 向后误差分析",
    "Lu": "3. 高斯消去法",
    "Qr": "4. 最小二乘与 QR",
    "Svd": "5. 奇异值分解",
    "Eigen": "6. 特征值：QR 算法",
    "Krylov": "7. 共轭梯度法",
    "Sparse": "8. 稀疏矩阵",
    "Multigrid": "9. 多重网格",
    "Roots": "10. 求根与牛顿分形",
    "Approx": "11. 逼近",
    "Quadrature": "12. 数值求积",
    "Odes": "13. 微分方程",
    "Speed": "14. 速度：BLAS、LAPACK 与混合精度",
    "Frontier": "15. 前沿：随机化与低精度的数值计算",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    "In the year 2000 a journal asked two numerical analysts to":
        "2000年，一家期刊请两位数值分析学家，评选出二十世纪对科学和工程影响最大的十个算法。<bookmark mark='a'/>他们的名单从1946年诞生于洛斯阿拉莫斯的蒙特卡洛方法开始，"
        "经过单纯形法、Krylov 迭代、矩阵分解、第一个优化编译器、QR 算法、快速排序、快速傅里叶变换、整数关系探测，一直到快速多极子方法。<bookmark mark='b'/>这十个算法中，"
        "有八个是用实数计算的。这一部分讲的就是它们，以及笼罩在每一个算法之上的那个问题：每一次运算都有舍入，哪些答案可以信任？",
    "Here is the question in miniature. <bookmark mark='a'/> Two":
        "这是这个问题的一个缩影。<bookmark mark='a'/>两个方程，两个未知数。答案几乎恰好是1和1。<bookmark mark='b'/>按学校里教的方式做高斯消去，用双精度，"
        "得到的答案是第一个未知数等于0。每一位数字都是错的。<bookmark mark='c'/>在消去之前把两个方程交换一下，同样的算术就能算对。"
        "<bookmark mark='d'/>这个问题本身没有任何困难。数据的微小变化，只让答案改变一点点。出问题的是算法。把问题的难度与算法的好坏区分开来，是数值分析的第一个思想，这一部分其余的内容都建立在它之上。",
    "This is Part 52 of Computer Science, Built, and it opens":
        "这是计算机科学，从零搭建，第52部分，它从第4部分停下的地方开始，也就是会舍入的数。<bookmark mark='a'/>我们将把问题的条件与算法的稳定性区分开来；"
        "用消去法、QR 和 SVD 求解线性方程组；用一种三次收敛的迭代求特征值；用共轭梯度法和多重网格求解一百万个方程；跟着牛顿法走进它的分形；做插值、做积分，并一步一步地求解刚性方程；"
        "还要看看为什么在每一台机器上，最快的代码都是矩阵乘法。",
    # ------------------------------------------------------------------ s02_conditioning
    "Chapter one. Conditioning and stability.":
        "第一章：条件与稳定性。",
    "Before asking whether an algorithm is good, ask whether the":
        "在问一个算法好不好之前，先问这个问题难不难。<bookmark mark='a'/>把数据 x 推动一个小的相对量。答案也会移动，这两个相对变化之比，就是这个问题的条件数 κ。"
        "<bookmark mark='b'/>把 f 的变化写成 f 在 x 加 δx 处的值减去 f 在 x 处的值，再重新组合：一个差商，乘以 x 除以 f(x)。"
        "<bookmark mark='c'/>当推动越来越小，这个差商就变成导数。κ 等于 x 乘以 f 撇 x 的大小，除以 f(x)。<bookmark mark='d'/>注意少了什么：没有算法，"
        "也没有舍入。κ 只属于问题本身，而 κ 很大的问题叫作病态的。",
    "Four small problems show the range. <bookmark mark='a'/>":
        "四个小问题展示了它的范围。<bookmark mark='a'/>从一个非常接近1的数里减去1：κ 等于 x 除以 x 减1，大约100万。这就是第4部分的抵消，而现在我们看到，这是问题的错，"
        "不是计算机的错。<bookmark mark='b'/>平方根的 κ 处处都是二分之一：它把相对误差减半。<bookmark mark='c'/>指数函数的 κ 等于 x，所以在 x 等于100处，"
        "κ 就是100。<bookmark mark='d'/>正切函数在接近直角的地方，κ 大约是16000。<bookmark mark='e'/>经验法则是：数据有16位精确数字，"
        "就大约能得到16减去 κ 的常用对数那么多位。",
    "For a linear system A x equals b, perturb the right-hand":
        "对线性方程组 A x 等于 b，扰动它的右端项。<bookmark mark='a'/>两个方程相减：A 乘 δx 等于 δb。"
        "<bookmark mark='b'/>所以 δx 等于 A 的逆乘以 δb，它的大小至多是 A 的逆的范数乘以 δb 的大小。<bookmark mark='c'/>因为 b 等于 A x，"
        "所以 x 至少有 b 除以 A 的范数那么大。两式相除：x 的相对变化，至多是 A 的范数，乘以 A 的逆的范数，再乘以 b 的相对变化。"
        "<bookmark mark='d'/>这个乘积就是矩阵的条件数，这个名字是阿兰·图灵在1948年取的。<bookmark mark='e'/>从几何上看，A 把单位圆变成一个椭圆，"
        "而 κ 就是它的最长轴与最短轴之比。",
    "Some problems are ill conditioned through and through.":
        "有些问题从里到外都是病态的。<bookmark mark='a'/>大卫·希尔伯特的矩阵，元素是 i 加 j 减1分之一。用最小二乘拟合多项式时就会出现它，它相邻的列几乎平行，"
        "以至于这个方程组几乎确定不了 x。<bookmark mark='b'/>我们的仪器测量了它的条件数：4阶时约为16000，8阶时为150亿，"
        "<bookmark mark='c'/>而12阶时是1.6乘以10的16次方，超过了机器精度的倒数。<bookmark mark='d'/>按照经验法则，无论用什么算法，4阶时剩下12位数字，"
        "8阶时剩下6位，12阶时一位也不剩。",
    "Conditioning is the problem's share of the error. Stability":
        "条件是误差中属于问题的那一份，稳定性是属于算法的那一份。<bookmark mark='a'/>精确映射 f 把数据 x 送到答案 f(x)。算法 f 波浪在每一步都舍入，落到了别的地方。"
        "<bookmark mark='b'/>詹姆斯·威尔金森的问题是：是否存在邻近的数据 x 波浪，使得那个错误的答案恰好是对的？如果总是存在，而且相差在机器精度的一个小倍数之内，"
        "这个算法就叫作向后稳定的。<bookmark mark='c'/>向后稳定的算法所犯的误差，不超过把数据舍入一次所带来的误差，而条件数把它转化为答案的误差。开场的那两个方程是良态的；"
        "不做行交换的消去法，只不过是不稳定而已。",
    # ------------------------------------------------------------------ s03_backward
    "Chapter two. Backward error analysis.":
        "第二章：向后误差分析。",
    "James Wilkinson learned his trade beside Turing at the":
        "詹姆斯·威尔金森是在英国国家物理实验室，在图灵身边学会这门手艺的，他用一个简单的模型来分析舍入。<bookmark mark='a'/>每一次浮点运算返回的，都是精确结果乘以一加 δ，"
        "其中 δ 至多是单位舍入误差，在双精度下大约是10的负16次方。<bookmark mark='b'/>把三个数加起来。每一次加法舍入一次。<bookmark mark='c'/>把它乘开，"
        "每个输入都得到它自己的一个小因子。<bookmark mark='d'/>所以计算出的和，是几个略有不同的数的精确和，每个数大约被改变了两次舍入。这就是向后误差：不是答案错了多少，"
        "而是数据必须移动多远，才能让答案恰好正确。",
    "Why ask the question backwards? Because the two errors are":
        "为什么要倒过来问这个问题？因为这两种误差由条件数联系在一起。<bookmark mark='a'/>假设计算出的答案 y 帽，是数据 x 加 δx 的精确答案。"
        "<bookmark mark='b'/>在一阶近似下，答案移动了 f 撇 x 乘以 δx。<bookmark mark='c'/>除以 y，再同乘同除以 x：相对向前误差等于 κ 乘以相对向后误差。"
        "<bookmark mark='d'/>向前误差至多是条件数乘以向后误差。算法控制其中一个因子，问题控制另一个，而每一个都可以单独研究。",
    "For linear systems the rule is exact, and the backward error":
        "对线性方程组，这条规则是精确的，而且向后误差可以测量。<bookmark mark='a'/>给定一个计算出的解 x 帽，构造残差：b 减 A x 帽。"
        "<bookmark mark='b'/>给 A 加上一个秩一矩阵，r 乘以 x 帽的转置，再除以 x 帽大小的平方，这样 x 帽就恰好是改变后的方程组的解。"
        "<bookmark mark='c'/>这个改变相对于 A 的大小，是 r 的范数除以 A 的范数与 x 帽的范数之积。把它叫作 η：它是事后算出来的，用的都是我们手头已有的东西。"
        "<bookmark mark='d'/>与此同时，真正的误差，x 减 x 帽，等于 A 的逆乘以 r。<bookmark mark='e'/>取范数，相对误差就至多是 κ 乘以 η，完全没有近似。",
    "Our instrument tests the rule on Hilbert systems. It picks":
        "我们的仪器在希尔伯特方程组上检验这条规则。它选定 x，令 b 等于 H 乘 x，再通过 NumPy，用 LAPACK 的选主元消去法求解。"
        "<bookmark mark='a'/>向后误差在每个阶数上都保持在10的负17次方附近：这个算法稳定到了舍入所允许的极限。"
        "<bookmark mark='b'/>向前误差则从4阶时的2乘以10的负13次方，攀升到12阶时的约百分之五。<bookmark mark='c'/>而且在每个阶数上，它都低于 κ 乘以 η，"
        "也就是我们推导出的界。算法内部没有出任何错；是问题放大了它自己数据的舍入。",
    "In digits, the picture is simple. <bookmark mark='a'/> At":
        "用位数来说，图景很简单。<bookmark mark='a'/>4阶时，16位数字里有12位是对的。<bookmark mark='b'/>8阶时，7位。"
        "<bookmark mark='c'/>12阶时，1位。<bookmark mark='d'/>每一次，丢掉的位数大约就是 κ 的对数：向后稳定的算法，只丢掉问题本身毁掉的那些。"
        "<bookmark mark='e'/>这是威尔金森伟大的澄清，写在他1963年的书《代数过程中的舍入误差》（Rounding Errors in Algebraic Processes）里，"
        "并让他在1970年获得了图灵奖。下一章把它用在所有算法中用得最多的那一个上：高斯消去法。",
    # ------------------------------------------------------------------ s04_lu
    "Chapter three. Gaussian elimination.":
        "第三章：高斯消去法。",
    "Elimination is the oldest algorithm in this part: the":
        "消去法是这一部分里最古老的算法：中国的《九章算术》就已经用到了它。<bookmark mark='a'/>为了把主元下方的第一列清零，从第二行减去第一行的2倍，从第三行减去第一行的4倍。"
        "<bookmark mark='b'/>再从第三行减去新的第二行的3倍。剩下的是上三角的：把它叫作 U。<bookmark mark='c'/>把乘数2、4和3保存在一个对角线全是1的下三角矩阵里："
        "把它叫作 L。<bookmark mark='d'/>于是 A 等于 L 乘 U，这是图灵在1948年指出的。这样，求解 A x 等于 b 就成了两次三角求解：L 从上往下，然后 U 从下往上。",
    "How much work is it? <bookmark mark='a'/> Step k updates the":
        "工作量有多大？<bookmark mark='a'/>第 k 步更新主元右下方的块：n 减 k 的平方个元素，每个做一次乘法和一次减法。<bookmark mark='b'/>把各步加起来，"
        "并从末尾开始数。<bookmark mark='c'/>前若干个平方数之和是一个三次式，<bookmark mark='d'/>它的首项给出 n 的立方的三分之二次运算。"
        "<bookmark mark='e'/>每次三角求解只花大约 n 的平方，所以分解只做一次，就能对每一个右端项重复使用。改为计算逆矩阵，要花三倍的工作量，于是有了这条规则：要求解，永远不要求逆。",
    "Here is the hook's failure. <bookmark mark='a'/> Eliminating":
        "这就是开场里的那次失败。<bookmark mark='a'/>用很小的主元 ε 做消去，需要乘数 ε 分之一，并在角上留下1减 ε 分之一。"
        "<bookmark mark='b'/>当 ε 是10的负20次方时，它舍入成负10的20次方。那个1没了。<bookmark mark='c'/>计算出的因子，是另一个矩阵的精确因子，"
        "那个矩阵在原来是1的地方是0。<bookmark mark='d'/>解药是部分选主元：每一步之前，把这一列中元素最大的那一行换上来，这样每个乘数都至多为1。"
        "<bookmark mark='e'/>在我们仪器的运行中，不选主元时，误差随着 ε 变小而增大，直到没有一位数字是对的；选主元时，误差始终保持在舍入的水平。",
    "With pivoting, how large can the entries of U become?":
        "选主元之后，U 的元素能变得多大？<bookmark mark='a'/>每一步把一个元素替换成它自身减去一个至多为1的乘数乘以另一个元素，"
        "<bookmark mark='b'/>所以最大的元素至多翻一倍。<bookmark mark='c'/>经过 n 减1步，增长因子 ρ 至多是2的 n 减1次方，这是威尔金森证明的，"
        "而消去法的向后误差随 ρ 增长。<bookmark mark='d'/>这个界是能达到的：这里最后一列每一步都翻倍。<bookmark mark='e'/>实测下来，"
        "在威尔金森的矩阵上它恰好是2的 n 减1次方，64阶时是9乘以10的18次方，<bookmark mark='f'/>但对同样大小的随机矩阵，只有大约4。"
        "Lloyd Trefethen 和 Robert Schreiber 在1990年研究过这个问题：实践中增长很小，而没有人证明过这是为什么。",
    "When A is symmetric and positive definite, as covariance":
        "当 A 是对称正定的，就像协方差矩阵那样，消去法的工作量可以减半。<bookmark mark='a'/>把 A 写成 L 乘 L 的转置。<bookmark mark='b'/>对应元素："
        "l 一一的平方等于 a，l 一一乘 l 二一等于 b，而角上给出 c。<bookmark mark='c'/>依次求解：几个平方根和一次除法。正定性恰好就是每个平方根下都是正数的条件。"
        "L 的每个元素都以 A 的某个对角元的平方根为界，所以什么都不会增长，也不需要选主元。"
        "<bookmark mark='d'/>André-Louis Cholesky 的方法需要 n 的立方的三分之一次运算，是 LU 的一半。",
    # ------------------------------------------------------------------ s05_qr
    "Chapter four. Least squares and QR.":
        "第四章：最小二乘与 QR。",
    "Least squares, published by Adrien-Marie Legendre in 1805":
        "最小二乘法由 Adrien-Marie Legendre 在1805年发表，高斯也宣称是自己的发现；它用方程比未知数多的方程组来拟合一个模型。<bookmark mark='a'/>我们想要的 x，"
        "要让 A x 尽可能接近 b。<bookmark mark='b'/>最接近的 A x，是从 b 向 A 的各列张成的平面所作垂线的垂足，所以残差与每一列都正交：A 的转置乘以残差等于零。"
        "<bookmark mark='c'/>整理一下，这就是正规方程，一个小的方阵方程组。<bookmark mark='d'/>但 A 转置 A 的奇异值是 A 的奇异值的平方，"
        "所以它的条件数是 κ 的平方。一个 κ 为一百万的问题，变成了 κ 为一万亿的问题。",
    "Gene Golub's answer, in 1965, was never to form A transposed":
        "Gene Golub 在1965年给出的答案是：根本不要构造 A 转置 A。<bookmark mark='a'/>把 A 分解成一个正交矩阵 Q 乘以一个上三角矩阵 R。"
        "<bookmark mark='b'/>乘以 Q 的转置不改变任何长度，所以残差的大小不变，而问题一分为二。<bookmark mark='c'/>下面几行是任何 x 都修正不了的部分；"
        "上面几行是一个三角方程组，它的条件数是 κ，而不是 κ 的平方。<bookmark mark='d'/>我们的仪器在四个条件数下拟合一个高瘦的方程组。正规方程的误差像 κ 的平方那样增长，"
        "在 κ 为10的8次方时达到百分之三十七。<bookmark mark='e'/>QR 解的误差只像 κ 那样增长。",
    "How do we find Q and R stably? Alston Householder's answer,":
        "怎样稳定地求出 Q 和 R？Alston Householder 在1958年给出的答案是：镜子。<bookmark mark='a'/>取第一列 x，这里是3和4。我们想要一个反射，"
        "把它放倒到第一个坐标轴上。反射保持长度，所以它必须落在正5或负5。<bookmark mark='b'/>镜面垂直于 v，而 v 沿着 x 加5倍 e1 的方向。反射就是减去沿 v 方向分量的两倍，"
        "<bookmark mark='c'/>于是 x 恰好落在负5、0。这样选符号，是把两个正数相加，而不是把两个几乎相等的数相减：第一章的抵消，就这样避免了。"
        "<bookmark mark='d'/>同一面镜子把第二列送到负3、1，矩阵就成了三角的。<bookmark mark='e'/>更大的矩阵每一列需要一面镜子，每面镜子都把对角线以下的一切清零，"
        "而 Q 就是它们的乘积。",
    "Wallace Givens used rotations instead of mirrors. <bookmark":
        "Wallace Givens 用旋转代替了镜子。<bookmark mark='a'/>把数对 a、b，这里是3和4，旋转一个角度，让它落到坐标轴上。"
        "<bookmark mark='b'/>余弦是 a 除以 r，正弦是 b 除以 r，其中 r 是长度。<bookmark mark='c'/>验算一下：第二个元素变成负 a b 加 a b，也就是零，"
        "第一个元素变成 r，这里是5。<bookmark mark='d'/>每次旋转只涉及两行，并把一个元素清零。我们的三乘三例子只需要两次旋转，因为有一个元素一开始就是零。"
        "<bookmark mark='e'/>正是这种节省，让第六章的特征值算法在它那些近乎三角的矩阵上使用旋转。",
    "The textbook way to get Q is Gram–Schmidt: take each column":
        "求 Q 的教科书方法是 Gram–Schmidt 正交化：取每一列，减去它沿前面各列的分量。<bookmark mark='a'/>经典 Gram–Schmidt 用原始的列来度量每个分量。"
        "<bookmark mark='b'/>修正 Gram–Schmidt 用到目前为止已经更新过的列来度量。在精确算术下，它们是同一个算法。<bookmark mark='c'/>在浮点数下，"
        "对希尔伯特矩阵，经典版本得到的 Q 到8阶时已经完全不正交了。<bookmark mark='d'/>修正版本丧失的正交性与 κ 成正比，这是 Åke Björck 在1967年证明的。"
        "<bookmark mark='e'/>Householder 的镜子在每个阶数上都保持正交到机器精度，因为每面镜子在构造上就是精确正交的。",
    # ------------------------------------------------------------------ s06_svd
    "Chapter five. The singular value decomposition.":
        "第五章：奇异值分解。",
    "Every matrix, of any shape, has a singular value":
        "每个矩阵，无论什么形状，都有奇异值分解。<bookmark mark='a'/>看这个二乘二矩阵作用在单位圆上。先是一个旋转 V 转置，把两个特殊的、互相垂直的方向转到坐标轴上。"
        "<bookmark mark='b'/>然后一个对角矩阵 Σ，把每个坐标轴按一个奇异值拉伸。<bookmark mark='c'/>再是第二个旋转 U，圆就成了一个椭圆。"
        "<bookmark mark='d'/>用符号来写，A 把每个右奇异向量 v i 送到 σ i 乘以 u i。把它们作为列并排放在一起，又因为 V 是正交的，A 就等于 U Σ V 转置。"
        "<bookmark mark='e'/>最长的拉伸除以最短的拉伸，就是第一章的条件数。",
    'f"Multiply the decomposition out and a matrix':
        "把这个分解乘开，一个矩阵就变成若干个秩一部分之和，最大的在前。<bookmark mark='a'/>保留前 k 个，就得到了所有秩 k 近似中最好的那一个："
        "Carl Eckart 和 Gale Young 在1936年证明，它的误差就是下一个奇异值，这一事实正是《人工智能，从零搭建》第3部分里那些嵌入背后的道理。"
        "<bookmark mark='b'/>这里是一个模糊信号的矩阵的80个奇异值。<bookmark mark='c'/>低于舍入水平的那些，是算术中的噪声，所以数值秩是{r_num}，而不是80。"
        "<bookmark mark='d'/>而以我们数据中的噪声，也就是千分之一来衡量，只有{r_noise}个携带信息。在浮点数中，秩取决于一个容差。",
    "Here is the experiment. <bookmark mark='a'/> A signal of two":
        "这是那个实验。<bookmark mark='a'/>一个由两个方块组成的信号，绿色的，被那个矩阵模糊，再加上千分之一的噪声：就是这条黄色曲线。我们能撤销这次模糊吗？"
        "<bookmark mark='b'/>把分解的每个因子求逆，解就成了一个和，每个奇异值对应一项，每个系数都除以它的 σ。<bookmark mark='c'/>但噪声也被奇异值除，"
        "而最小的奇异值是10的负16次方。<bookmark mark='d'/>条件数大约是10的16次方，朴素解的误差是信号的10的13次方倍。错不在算术：这个问题，照它提出的样子，是解不了的。",
    'f"The cure is to stop dividing by tiny numbers.':
        "解药是不再除以极小的数。<bookmark mark='a'/>只保留前 k 项：截断 SVD。每丢掉一项，就丢失一点信号；每保留一项，就加入被它的 σ 除过的噪声。"
        "<bookmark mark='b'/>我们的仪器尝试了每一个 k。误差从只有一项时的百分之{100 * first:.0f}，"
        "降到 k 等于{kb}时的百分之{100 * best['error']:.0f}，然后爆炸，到全部80项时又回到10的13次方。<bookmark mark='c'/>在最好的 k 处，"
        "两个方块回来了，只是稍微圆了一点。<bookmark mark='d'/>Andrey Tikhonov 1963年的正则化，平滑地衰减每一项，而不是把它截掉。无论哪种方式，我们都是有意去解一个邻近的、良态的问题。",
    "How is it computed? Not from A transposed A, which would":
        "它是怎么计算的？不是通过 A 转置 A，那样又会把条件数平方。<bookmark mark='a'/>Gene Golub 和威廉·卡亨在1965年，"
        "交替地从左边和右边施加 Householder 镜子，清掉一列，再清掉一行。<bookmark mark='b'/>剩下的是一个双对角矩阵，奇异值不变，再由下一章 QR 算法的一个变体把它们求出来。"
        "<bookmark mark='c'/>回报是伪逆：只对高于某个容差的奇异值求逆，即使矩阵是秩亏损的，也能得到最短的最小二乘解。"
        "<bookmark mark='d'/>SVD 的代价是 QR 的好几倍，所以它是最后的手段：当其他方法都失败时，它能确切地告诉你，数据能告诉你多少。",
    # ------------------------------------------------------------------ s07_eigen
    "Chapter six. Eigenvalues, and the QR algorithm.":
        "第六章：特征值，以及 QR 算法。",
    "An eigenvector is a direction that a matrix only stretches:":
        "特征向量是矩阵只拉伸、不转动的方向：A v 等于 λ v。<bookmark mark='a'/>把所有项移到一边。A 减 λI 把 v 送到零，所以它是奇异的，它的行列式为零。"
        "<bookmark mark='b'/>这个行列式是一个 n 次多项式，特征值就是它的根：这里是一个随机的八乘八对称矩阵的八个根。"
        "<bookmark mark='c'/>Niels Henrik Abel 在1824年证明，一般的五次多项式没有根式求解公式。"
        "<bookmark mark='d'/>而每个多项式都是某个矩阵的特征多项式，也就是它的友矩阵。所以一般来说，没有任何有限的步骤能求出特征值：每一个特征值算法都必须迭代。",
    'f"The simplest iteration is the power method.':
        "最简单的迭代是幂法。<bookmark mark='a'/>把一个起始向量用特征向量表示出来。<bookmark mark='b'/>乘以 A 共 k 次，就把每个分量乘以它的特征值的 k 次方。"
        "<bookmark mark='c'/>把最大的那个提出来：其他每个分量都像一个比值的 k 次方那样缩小。这里的比值大约是三分之二，误差在{kp}步之后达到10的负13次方。"
        "<bookmark mark='d'/>逆迭代用的是 A 减去一个位移 μ 之后的逆，它的特征值是 λ 减 μ 分之一，所以离位移最近的那个特征值压倒性地占主导。位移相差0.3时，{ki}步就够了，"
        "每一步都是用第三章的因子做一次线性求解。",
    'f"In 1961 John Francis in England and,':
        "1961年，英格兰的 John Francis，以及苏联的 Vera Kublanovskaya，各自独立地找到了今天仍在使用的算法。<bookmark mark='a'/>把矩阵分解成 Q 乘 R。"
        "<bookmark mark='b'/>因为 Q 是正交的，R 就等于 Q 转置乘 A。<bookmark mark='c'/>现在把两个因子按相反的次序相乘。"
        "<bookmark mark='d'/>结果是 Q 转置 A Q，一个相似变换，所以特征值不变：这就是把幂法一次作用在一整组基上。<bookmark mark='e'/>重复下去，"
        "矩阵就慢慢趋向对角形式，特征值出现在它的对角线上。按大小在对数刻度上着色，我们这个矩阵最后一个非对角元在40次迭代中淡到了10的负15次方。把全部八个都求出来，需要{un['iterations']}次。",
    'f"Three refinements make it fast. <bookmark':
        "三项改进让它变快。<bookmark mark='a'/>第一，用两侧的 Householder 镜子，把矩阵一次性约化为 Hessenberg 形式，也就是第一条次对角线以下全为零；"
        "对称矩阵则变成三对角的。QR 算法保持这种形状，于是每一步用 Givens 旋转只花 n 的平方，而不是 n 的立方。<bookmark mark='b'/>第二，位移："
        "分解之前减去对某个特征值的猜测，分解之后再加回来。詹姆斯·威尔金森的位移，是右下角那个二乘二块的一个特征值。<bookmark mark='c'/>第三，收缩：当最后一个次对角元小到可以忽略时，"
        "最下面的特征值就求出来了，迭代在一个更小的矩阵上继续。<bookmark mark='d'/>三项都用上，我们的八个特征值只需要{sh['iterations']}次迭代，"
        "而不是{q['unshifted']['iterations']}次。",
    "Here is why the shift matters. <bookmark mark='a'/> Without":
        "这就是位移之所以重要的原因。<bookmark mark='a'/>没有位移时，最后一个次对角元每一步按一个常数因子缩小：在对数刻度上是一条直线，也就是线性收敛。"
        "<bookmark mark='b'/>用了威尔金森的位移，它从8乘以10的负4次方，变成4乘以10的负12次方，再变成3乘以10的负35次方。"
        "<bookmark mark='c'/>正确的位数每次大约变成三倍；测得的阶大约是3.7和3。这就是三次收敛，而威尔金森在1968年证明，用他的位移，对称情形的迭代总是收敛的。"
        "<bookmark mark='d'/>这些答案与 LAPACK 的结果吻合到大约10的负14次方。你见过的几乎每一个特征值，都是这样算出来的。",
    # ------------------------------------------------------------------ s08_krylov
    "Chapter seven. Conjugate gradients.":
        "第七章：共轭梯度法。",
    "For a symmetric positive definite matrix, solving A x equals":
        "对一个对称正定矩阵来说，求解 A x 等于 b，就等同于走下坡路。<bookmark mark='a'/>定义 φ(x) 为二分之一 x 转置 A x，减去 b 转置 x。它是一只碗，"
        "这些椭圆是它的等高线。<bookmark mark='b'/>它的梯度是 A x 减 b：<bookmark mark='c'/>恰好在解处为零，在其他各处都是负的残差。"
        "<bookmark mark='d'/>所以第23部分的梯度下降就派上了用场。沿着残差走，只要碗还在往下降就一直走，然后重复。在一只又长又窄的碗里，它会走之字形，每一步都抵消掉上一步的一部分。"
        "<bookmark mark='e'/>共轭梯度法在同一只碗上，两步就到了。",
    "Why two steps? The conjugate gradient method of Magnus":
        "为什么是两步？Magnus Hestenes 和 Eduard Stiefel 1952年的共轭梯度法，做的不只是走下坡路。<bookmark mark='a'/>走了 k 步之后，"
        "它能从 b 构造出来的向量，只有 b、A b、A 的平方乘 b 等等的组合：这就是 Krylov 子空间。<bookmark mark='b'/>共轭梯度法在整个子空间里挑出最好的点，"
        "用的是碗自己的范数，而不只是沿一条直线上最好的点。<bookmark mark='c'/>它之所以做得到，是因为它的搜索方向是共轭的，也就是在 A 的内积下正交，所以新的一步永远不会破坏旧的几步。"
        "<bookmark mark='d'/>这个循环很短：一次与 A 的乘积，两次内积，四个向量的内存。在精确算术下，它在 n 步之内结束；在实践中，要早得多。",
    '''f"How fast is it? <bookmark mark='a'/> The error''':
        "它有多快？<bookmark mark='a'/>误差下降得至少和一个比值的 k 次方的两倍一样快：根号 κ 减1，除以根号 κ 加1。<bookmark mark='b'/>当 κ 很大时，"
        "这个比值大约是1减去根号 κ 分之二，<bookmark mark='c'/>所以步数像条件数的平方根那样增长。<bookmark mark='d'/>在共轭梯度法是 κ 的平方根的地方，"
        "最速下降法是 κ 本身。<bookmark mark='e'/>我们的仪器在三个网格上求解泊松问题，也就是第八章的矩阵；κ 随未知数的个数增长。"
        "最速下降法在最小的网格上需要{rows_[0]['steepest']}步，在下一个网格上需要{rows_[1]['steepest']:,}步，而在最大的网格上，八千步之后还没有收敛。"
        "共轭梯度法需要{rows_[0]['cg']}步、{rows_[1]['cg']}步和{rows_[2]['cg']}步，大约是那个界所允许的一半。",
    'f"Since the cost depends on kappa, change kappa.':
        "既然代价取决于 κ，那就改变 κ。<bookmark mark='a'/>把方程组乘以一个矩阵 M 的逆，M 很像 A，但用它来求解很便宜。解不变，而如果 M 模仿得好，"
        "M 的逆乘 A 的条件数就会小得多。<bookmark mark='b'/>最简单的选择，A 自己的对角线，在这里毫无作用：泊松矩阵的对角线上全是4，步数完全相同。"
        "<bookmark mark='c'/>对称逐次超松弛，也就是两次三角扫描，把{mid['cg']}步减到{mid['ssor_cg']}步，"
        "把{rows_[2]['cg']}步减到{rows_[2]['ssor_cg']}步。<bookmark mark='d'/>不完全 Cholesky 分解效果还要更好，而第九章的多重网格能让步数与网格无关。",
    'f"Conjugate gradients needs a symmetric matrix. Add':
        "共轭梯度法需要对称矩阵。加上一股流动，也就是在扩散之外再加上对流，对称性就失去了。"
        "<bookmark mark='a'/>Yousef Saad 和 Martin Schultz 1986年提出的 GMRES，用 Arnoldi 过程构造 Krylov 子空间的一组标准正交基，"
        "而 Arnoldi 过程就是第四章的修正 Gram–Schmidt。A 乘以这组基，等于下一组基乘以一个小的 Hessenberg 矩阵，也就是第六章的那种形状。"
        "<bookmark mark='b'/>它在这个子空间里寻找 x，<bookmark mark='c'/>并通过一个小的最小二乘问题让残差最小，这个问题用 Givens 旋转求解。"
        "<bookmark mark='d'/>在我们那个有1024个未知数的非对称问题上，它在{g['iterations']}步内达到10的负8次方。<bookmark mark='e'/>代价是内存："
        "每一个基向量都要保存，所以长时间的运行要重新启动。",
    # ------------------------------------------------------------------ s09_sparse
    "Chapter eight. Sparse matrices.":
        "第八章：稀疏矩阵。",
    "The matrices of chapters seven and nine come from equations":
        "第七章和第九章的矩阵，来自泊松方程这样的方程，它支配着稳态的热、电势和压强。<bookmark mark='a'/>我们要在一个正方形上求 u，已知 f，并且 u 在边界上为零。"
        "在一个间距为 h 的网格上对 u 采样。<bookmark mark='b'/>把 u 在 x 加 h 和 x 减 h 处的泰勒级数相加，奇数次项就抵消了，"
        "<bookmark mark='c'/>于是二阶导数变成二阶差分，再除以 h 的平方。<bookmark mark='d'/>在 y 方向做同样的事再相加：每个网格点与它的四个邻居耦合，"
        "自身的4倍减去每个邻居各一次。这就是每个网格点一个方程，每个方程至多五个未知数。",
    'f"Number the grid points row by row, and almost':
        "把网格点一行一行地编号，矩阵几乎每个元素都是零。<bookmark mark='a'/>压缩稀疏行格式只存储非零元：它们的值，一行接一行，<bookmark mark='b'/>它们的列号，"
        "<bookmark mark='c'/>以及每一行从哪里开始。<bookmark mark='d'/>乘以一个向量，就是把这些数组走一遍，每个非零元两次运算。按列号每读取一次 x，"
        "都会落到一个无法预测的地方，所以这个乘积受内存带宽限制，就像第9部分那样。<bookmark mark='e'/>对一个64乘64的网格，也就是4096个未知数，"
        "这个矩阵有{big['nnz_A']:,}个非零元：用这种格式大约是260千字节，而稠密存储要134兆字节。",
    'f"Direct solvers factor the matrix, and there':
        "直接求解器要分解矩阵，而在那里，稀疏性很脆弱。<bookmark mark='a'/>在这个箭形矩阵里，一个未知数，也就是中心，与其他所有未知数耦合。"
        "Seymour Parter 1961年对消去法的看法是一张图：消去一个未知数，会让它的所有邻居彼此耦合起来。<bookmark mark='b'/>先消去中心，其他未知数两两之间就都耦合了："
        "因子被完全填满。<bookmark mark='c'/>最后消去它，就什么都不会填充。同一个矩阵，同一个答案；不同的只是次序。<bookmark mark='d'/>在64乘64的网格上，"
        "一行一行地编号，Cholesky 因子有26万2000个非零元，是矩阵的{big['natural'] / big['nnz_A']:.0f}倍。",
    "So the order of elimination is the whole game. <bookmark":
        "所以，消去的次序就是全部的关键。<bookmark mark='a'/>一行一行地编号，网格就像扫帚扫地那样被消去，部分消去的未知数构成的前沿，把它身后的一切与它前方的一切耦合起来："
        "宽度为 m 的带被完全填满。<bookmark mark='b'/>最小度排序是一条贪心规则，可以追溯到1957年的 Harry Markowitz，它总是接下来消去邻居最少的那个未知数。"
        "<bookmark mark='c'/>嵌套剖分是 Alan George 1973年的想法，它用一条由未知数组成的线把网格一分为二，把这条线最后编号，再对每一半做同样的事。"
        "<bookmark mark='d'/>在二维网格上，它的填充像 n log n 那样增长，工作量像 n 的二分之三次方那样增长，这是可能达到的最好的增长阶。",
    "Here is what the orderings buy on our grid of four thousand":
        "这就是各种排序在我们那个有4096个未知数的网格上换来的东西。<bookmark mark='a'/>一行一行地编号，因子有26万2000个非零元。逆 Cuthill–McKee 排序只把带变窄，"
        "是18万1000个。<bookmark mark='b'/>最小度排序，6万3000个，大约是矩阵本身的3倍；我们那个简单的嵌套剖分，8万9000个。"
        "<bookmark mark='c'/>嵌套剖分的优势在于增长和并行性：它的两半彼此独立，这就是为什么 METIS 这样的库在大型网格上使用它。当网格的边长翻倍时，逐行编号的填充增长到8倍，"
        "好的排序则不到6倍。<bookmark mark='d'/>在三维中，分隔集是平面，填充像 n 的三分之四次方那样增长，于是迭代方法接管了一切。",
    # ------------------------------------------------------------------ s10_multigrid
    "Chapter nine. Multigrid.":
        "第九章：多重网格。",
    "Go back to Poisson's equation, in one dimension to start:":
        "回到泊松方程，先从一维开始：63个未知数，对角线上是2，旁边是负1。<bookmark mark='a'/>最简单的迭代，加权 Jacobi 迭代，把每个未知数朝它自己的方程想要的值移动一段距离。"
        "<bookmark mark='b'/>减去真解，b 就抵消了：每次扫描，误差都乘以同一个矩阵。<bookmark mark='c'/>这个矩阵与 A 有相同的特征向量，它们都是正弦波："
        "第1个模态是一个平滑的单峰，第63个模态是一条锯齿。<bookmark mark='d'/>所以每次扫描只是把每个模态缩放一下，缩放因子我们可以写出来。"
        "<bookmark mark='e'/>每次移动三分之二的距离，模态中粗糙的上半部分，每次扫描至少缩小到三分之一。最平滑的模态则保留了自身的0.999。",
    "Watch it happen. <bookmark mark='a'/> These bars are a":
        "看它是怎么发生的。<bookmark mark='a'/>这些柱条是一个随机误差，沿着63个正弦波中的每一个来度量：平滑的模态在左边，粗糙的在右边。<bookmark mark='b'/>扫描一次，"
        "右半边就降下去了。<bookmark mark='c'/>扫描三次。<bookmark mark='d'/>十次之后，粗糙的那一半几乎完全消失，而最平滑的模态损失还不到百分之一。"
        "<bookmark mark='e'/>所以单靠松弛是没有希望的：剩下的误差是平滑的，而平滑的误差几乎不动。但松弛有一件事做得极好。它会把误差变平滑。",
    "Here is the trick. <bookmark mark='a'/> A smooth wave on a":
        "诀窍是这样的。<bookmark mark='a'/>在一个15个点的细网格上，一个平滑的波，第6个模态，位于频谱的下半部分，那里松弛很慢。<bookmark mark='b'/>每隔一个点保留一个。"
        "在7个点的粗网格上，同一个波是7个模态中的第6个：位于上半部分，那里松弛很快。<bookmark mark='c'/>所以先松弛几次，算出残差，把它传到粗网格上。在那里解出修正量，把它插值回来，"
        "加上去，再松弛一次。Radii Fedorenko 在1964年发表了这种两重网格方案，而 Achi Brandt 在1970年代让它变得实用。"
        "<bookmark mark='d'/>粗网格上的问题是同一类问题，所以用同样的方法对待它。",
    "Recursing gives the V-cycle. <bookmark mark='a'/> Relax and":
        "递归下去，就得到 V 循环。<bookmark mark='a'/>松弛并限制，穿过越来越粗的网格，一直到只有几个点的网格；在那里精确求解；然后在回来的路上插值并松弛。"
        "<bookmark mark='b'/>我们的仪器在二维泊松问题上运行它。在一个有225个未知数的网格上，每个循环把残差缩小到大约五分之一。<bookmark mark='c'/>在961个未知数上，"
        "一样。在16000个未知数上，还是一样。这些曲线彼此重叠，在每个网格上，十个循环都能达到亿分之几。循环的次数不随问题增长。",
    "And each cycle is cheap. <bookmark mark='a'/> It relaxes on":
        "而且每个循环都很便宜。<bookmark mark='a'/>它在最细的网格上松弛，工作量与 n 成正比，然后在一个点数只有四分之一的网格上做同样的事。"
        "<bookmark mark='b'/>把它展开：n 乘以一加四分之一加十六分之一，依此类推，<bookmark mark='c'/>也就是单在最细网格上的工作量的三分之四。"
        "<bookmark mark='d'/>现在比较一下求解同一个泊松问题的各种方法。稠密消去像 n 的立方那样增长；逐行编号的带状消去，像 n 的平方；嵌套剖分和共轭梯度法，像 n 的二分之三次方。"
        "多重网格像 n 那样增长。<bookmark mark='e'/>这就是读一遍右端项的代价，所以没有任何方法能做得更好。对于非结构化的问题，代数多重网格从矩阵本身构造它的粗层级，"
        "它常常就是共轭梯度法里面的那个预条件子。",
    # ------------------------------------------------------------------ s11_roots
    "Chapter ten. Roots, and Newton's fractal.":
        "第十章：求根，以及牛顿分形。",
    "Every method in this chapter hunts for a zero, and our test":
        "这一章里的每一种方法都在寻找一个零点，而我们的测试例子是2的平方根，也就是 x 的平方减2的正根。<bookmark mark='a'/>二分法只需要一次变号。f 在1处为负，在2处为正，"
        "所以有一个根位于两者之间。<bookmark mark='b'/>计算中点的值，保留仍然变号的那一半，然后重复。区间每次都减半，<bookmark mark='c'/>所以每一步得到一个比特，"
        "大约是十分之三位十进制数字。二分法不会失败，但它很慢：四十步之后，12位数字。",
    "Newton's method uses the slope as well. <bookmark mark='a'/>":
        "牛顿法还利用了斜率。<bookmark mark='a'/>在 x 附近，f 在 x 加 h 处的值，大约等于 f(x) 加上 f 撇 x 乘以 h：这就是切线。"
        "<bookmark mark='b'/>令它等于零，解出 h，<bookmark mark='c'/>然后迈出一步。从2出发，切线落在1.5，下一次落在1.4167。"
        "<bookmark mark='d'/>在泰勒级数中再多保留一项，新的误差就是一个常数乘以旧误差的平方。千分之一的误差变成大约百万分之一：正确的位数每一步都翻倍。"
        "<bookmark mark='e'/>割线法把导数换成经过最近两个点的斜率。它的阶是黄金比，1.618。",
    "Here is the race, computed. <bookmark mark='a'/> Bisection":
        "这就是这场比赛，实际算出来的。<bookmark mark='a'/>二分法沿着它的直线往上爬，每步十分之三位数字。<bookmark mark='b'/>割线法的正确位数是1、2、3、6、9.5，"
        "然后接近16，这是双精度的极限。<bookmark mark='c'/>牛顿法的是1、2.5、5.5、12、16：翻倍。<bookmark mark='d'/>但牛顿法的每一步，既要计算 f，"
        "又要计算它的导数。按每次函数求值来算，牛顿法的阶是2的平方根，而割线法的1.618，是两者中更快的那一个。",
    "Newton's method works for complex numbers too, and in 1879":
        "牛顿法对复数也适用，1879年，Arthur Cayley 问：从一个给定的起点出发，它会找到哪个根？对 z 的平方减1，答案很简单：较近的那个根。"
        "<bookmark mark='a'/>对 z 的立方减1，按照每个起点最终到达的根给它着色，花的时间越长，颜色越深。"
        "<bookmark mark='b'/>每个根都坐落在一片属于自己颜色的、平静的吸引域里。<bookmark mark='c'/>但吸引域之间的边界不是一条线。只要两种颜色相遇，"
        "第三种颜色就会出现在它们之间，形成越来越小的副本。",
    "Zoom in. <bookmark mark='a'/> A window fifteen times":
        "放大来看。<bookmark mark='a'/>在边界上取一个小15倍的窗口：同样的结构，花蕾上长着花蕾。在精确的图景中，它永无止境，因为一个吸引域边界上的每一个点，"
        "都同时位于所有三个吸引域的边界上。<bookmark mark='b'/>再放大20倍，但这次是放大到一个吸引域的内部，图景就变平了：那里的每个起点都在6步内到达同一个根。"
        "<bookmark mark='c'/>在根附近很快，离根远时无法预测：这就是为什么函数库里的求根程序都带有保护措施。Brent 方法来自1973年，它保持一个二分区间，只在快速的插值步留在区间之内时才采用它们。",
    # ------------------------------------------------------------------ s12_approx
    "Chapter eleven. Approximation.":
        "第十一章：逼近。",
    "To stand in for a function, the obvious idea is to sample it":
        "要替代一个函数，显而易见的想法是对它采样，再让一个多项式穿过这些样本点。<bookmark mark='a'/>1901年，Carl Runge 在一个完全光滑的函数上试了这个方法："
        "1加25 x 平方分之一。<bookmark mark='b'/>穿过11个等距点，多项式在中间跟得上它，但在两端附近摆动。<bookmark mark='c'/>穿过21个点，情况糟得多："
        "在两端附近，误差大约是60。<bookmark mark='d'/>用81个点，误差是6乘以10的14次方。数据越多，答案越差。函数是无辜的：该怪的是那些点。",
    "The cure is to choose the points. <bookmark mark='a'/> Space":
        "解药是选择这些点。<bookmark mark='a'/>在一个半圆上均匀地取点，再把它们投到直径上。这些就是切比雪夫点，它们朝两端聚集。<bookmark mark='b'/>为什么在那里？"
        "插值误差是 f 的某阶导数，这个我们改变不了，<bookmark mark='c'/>乘以节点多项式，也就是 x 减去每个采样点的乘积，这个我们可以改变。"
        "<bookmark mark='d'/>对等距点，它在中间很小，在两端附近要大将近100倍。对切比雪夫点，它均匀地起伏，永远不超过2的1减 n 次方，与任何一种选点方式所能达到的最小最大值相比，相差不到两倍。",
    "Here is the difference, computed. <bookmark mark='a'/>":
        "这就是两者的差别，实际算出来的。<bookmark mark='a'/>穿过21个切比雪夫点，多项式就已经处处与 Runge 函数相差不到百分之二。"
        "<bookmark mark='b'/>随着次数增长，等距点的误差爆炸，而切比雪夫点的误差按几何级数下降，到80次时降到大约一千万分之一。"
        "<bookmark mark='c'/>这个速率由 f 在哪里不再光滑决定：在正负 i 除以5处的极点，它们不在实轴上。"
        "<bookmark mark='d'/>围绕这个区间、穿过这两个极点的椭圆有一个参数 ρ，等于1加根号26，再除以5，大约是1.22，"
        "<bookmark mark='e'/>而误差像 ρ 的负 n 次方那样下降：就是那条虚线。",
    "How should a computer evaluate the interpolating polynomial?":
        "计算机应该怎样计算插值多项式？<bookmark mark='a'/>拉格朗日公式在每个点上都要花 n 的平方阶次运算，而且素有不稳定的名声。"
        "<bookmark mark='b'/>把节点多项式从每个拉格朗日基函数中提出来：剩下的是一个权重除以 x 减 x j。<bookmark mark='c'/>这就给出了第一种重心形式。"
        "<bookmark mark='d'/>现在对常数函数1做插值，任何插值都能精确地重现它。<bookmark mark='e'/>把第一个等式除以这一个，节点多项式就消掉了。"
        "剩下的每个点只花 n 阶次运算。<bookmark mark='f'/>对切比雪夫点，权重就是正负1，两端减半，而 Nicholas Higham 在2004年证明了这个公式是稳定的。"
        "这一章里的每一条曲线，都是这样计算出来的。",
    "Zachary Battles and Lloyd Trefethen took this to its":
        "Zachary Battles 和 Lloyd Trefethen 在2004年用 Chebfun 把这个思路推向了它的结论。"
        "<bookmark mark='a'/>用一个函数在切比雪夫点上的值来表示它，点要足够多，使它的切比雪夫系数降到舍入水平：先试17个点，然后33个、65个，依此类推，直到尾部成了噪声，就在那里截断。"
        "<bookmark mark='b'/>对 Runge 函数，我们刚才得到的速率预测大约需要185个。<bookmark mark='c'/>然后直接用这个函数本身来计算，精确到大约15位数字："
        "对它积分、求导、求它的最大值，并一次求出它的所有根，作为由它的系数构造的一个矩阵的特征值，又是第六章。<bookmark mark='d'/>用函数做数值计算，而不只是用数。",
    # ------------------------------------------------------------------ s13_quadrature
    "Chapter twelve. Quadrature.":
        "第十二章：数值求积。",
    "To integrate, sample the function and add up. Our test":
        "要做积分，就对函数采样，再加起来。我们的测试积分是 e 的 x 次方乘以余弦3x，从0到2。它的精确值大约是负百分之一：是几块大面积之间的一个小差。"
        "<bookmark mark='a'/>梯形法则用直线把样本点连起来。<bookmark mark='b'/>它的误差像 h 的平方那样缩小：间距减半，误差就降到四分之一。"
        "<bookmark mark='c'/>把两个梯形和组合起来，较细的那个的4倍减去较粗的那个，再除以3，h 的平方项就抵消了。这就是 Simpson 法则，"
        "<bookmark mark='d'/>它的误差像 h 的四次方那样下降。",
    "Both rules fix the sample points and choose only the":
        "这两种法则都固定了采样点，只选择权重。1814年，卡尔·弗里德里希·高斯把采样点也一起选了。<bookmark mark='a'/>用两个点，就有四个未知数，两个节点和两个权重，"
        "<bookmark mark='b'/>所以我们可以要求它对1、x、x 的平方和 x 的立方都给出正确答案。<bookmark mark='c'/>解出来，是在正负根号3分之一处、权重都为1："
        "两个样本，对每一个三次多项式都精确。<bookmark mark='d'/>用 n 个点，这个法则直到2n 减1次都是精确的。节点是 Legendre 多项式的根，"
        "像第十一章的切比雪夫点一样朝两端聚集。<bookmark mark='e'/>Gene Golub 和 John Welsch 在1969年证明，它们是一个对称三对角矩阵的特征值，"
        "所以第六章的 QR 算法就能把它们算出来。",
    "Here are four rules on our integral, computed. <bookmark":
        "这是四种法则在我们这个积分上的表现，实际算出来的。<bookmark mark='a'/>点数每翻一倍，梯形法则的误差就降到四分之一，到64个区间时大约是千分之一。"
        "<bookmark mark='b'/>Simpson 法则的误差每次降到十六分之一，降到大约百万分之一。<bookmark mark='c'/>高斯求积只用16个点就达到了4乘以10的负15次方，"
        "然后就再也下不去了：那是舍入。对光滑的被积函数，它的误差按几何级数下降，就像切比雪夫插值那样。<bookmark mark='d'/>蒙特卡洛方法，也就是 f 在随机点上的平均值，是迄今最差的："
        "用65个样本，它的典型误差仍然超过一半。",
    "A smooth stretch deserves few points and a wild one many.":
        "平坦的一段只值得用几个点，剧烈变化的一段则需要很多。自适应求积自己决定把点放在哪里。<bookmark mark='a'/>对一个区间用一次 Simpson 法则，再对它的两半各用一次。"
        "<bookmark mark='b'/>Simpson 法则的误差像宽度的五次方那样增长，所以两半合起来的误差，只有前者的十六分之一。<bookmark mark='c'/>两者相减，"
        "就免费得到了一个误差估计。<bookmark mark='d'/>如果它足够小，就接受，并把这个估计加回去作为修正；如果不够小，就分割并递归，每一半用一半的容差。"
        "<bookmark mark='e'/>在一个带尖点的被积函数上，区间在尖点处堆积起来，在别处则保持宽阔。在我们那个光滑的测试积分上，要求精度为10的负10次方时，我们的仪器用了985次函数求值，"
        "而高斯求积只需要16次：问题集中在局部时，自适应才划算。",
    "Monte Carlo loses in one dimension, and wins in many.":
        "蒙特卡洛方法在一维中输了，在多维中赢了。<bookmark mark='a'/>积分就是一个平均值，所以就用 f 在 N 个随机点上的平均值来估计它：这是这一部分那份十大算法名单上的第一个，"
        "来自洛斯阿拉莫斯。<bookmark mark='b'/>N 个独立样本的平均值的方差，是单个样本的方差除以 N，<bookmark mark='c'/>所以无论维数是多少，"
        "误差都像根号 N 分之一那样下降。<bookmark mark='d'/>在 d 维中有 N 个点的网格，间距是 N 的负 d 分之一次方，而梯形法则的误差像 N 的负 d 分之二次方那样下降。"
        "<bookmark mark='e'/>超过四维，蒙特卡洛方法就赢了，而在金融和物理中那种成百上千的维数里，别的方法都不可行。",
    # ------------------------------------------------------------------ s14_odes
    "Chapter thirteen. Differential equations.":
        "第十三章：微分方程。",
    "A differential equation gives the slope of its solution":
        "一个微分方程给出它的解在每一处的斜率，而求解器就沿着它走。<bookmark mark='a'/>根据泰勒级数，一步 h 之后的值，等于现在的值，加上 h 乘以斜率，再加上一个 h 平方阶的项。"
        "<bookmark mark='b'/>把其余部分丢掉，就是欧拉法：对 y 撇等于 y，步长为二分之一走四步，到达的是5，而不是7.39。"
        "<bookmark mark='c'/>Carl Runge 和 Wilhelm Kutta 在每一步中对斜率采样四次，让误差一直抵消到 h 的四次方。"
        "<bookmark mark='d'/>同样的四步，到达7.38。",
    "How large a step? Let the method decide. <bookmark":
        "步长该取多大？让方法自己决定。<bookmark mark='a'/>John Dormand 和 Peter Prince 1980年的公式，用同样的七个斜率给出两个答案，一个五阶，一个四阶。"
        "它们的差估计了误差，而误差像 h 的五次方那样增长。<bookmark mark='b'/>要求下一步的误差等于容差。<bookmark mark='c'/>两式相除，常数就消掉了："
        "把 h 乘以容差除以误差的五次方根。<bookmark mark='d'/>再加上一个安全系数，并重做任何失败的一步。<bookmark mark='e'/>这就是我们仪器的循环，"
        "也是 SciPy 的默认求解器和 MATLAB 的 ode45 背后的方法。",
    "Now a harder kind of equation. <bookmark mark='a'/> Its":
        "现在来看一类更难的方程。<bookmark mark='a'/>它的解是余弦 t 减去 e 的 λt 次方：当 λ 是很大的负数时，是一段短暂的瞬态，然后就只剩下平滑的余弦。"
        "<bookmark mark='b'/>λ 为负1时，自适应方法走了11步；为负100时，走了132步。<bookmark mark='c'/>为负10000时，走了6067步，尽管在最初的一瞬之后，"
        "答案还是那条平缓的余弦。<bookmark mark='d'/>向后欧拉法每次都走200步，而且它的误差甚至还缩小了。这就是刚性：一个早已结束的衰减，仍然支配着显式方法的步长。",
    "Why? Test each method on y prime equals lambda y, with z":
        "为什么？在 y 撇等于 λy 上测试每一种方法，令 z 等于 h 乘以 λ：每一步都把 y 乘以某个 R(z)。<bookmark mark='a'/>欧拉法的因子是1加 z："
        "只在以负1为圆心的一个圆盘内稳定。<bookmark mark='b'/>四阶 Runge–Kutta 的因子是它的泰勒多项式：区域更大，但仍然有界。"
        "<bookmark mark='c'/>向后欧拉法取新点处的斜率，得到的是1减 z 分之一，<bookmark mark='d'/>它在整个左半平面上都小于1。"
        "Germund Dahlquist 在1963年把这称为 A 稳定性。显式方法的因子是一个多项式，是无界的，所以没有任何显式方法是 A 稳定的。",
    "Some problems care less about one moment than about what is":
        "有些问题关心的不是某一时刻，而是在几百万步中守恒的东西：行星、分子、粒子束。<bookmark mark='a'/>蛙跳法，Loup Verlet 在1967年把它用于分子，先给动量半次冲击，"
        "让位置漂移整整一步，再完成那次冲击。<bookmark mark='b'/>每一部分都是相空间的一次剪切，它精确地保持面积：这一步是辛的。"
        "<bookmark mark='c'/>我们让一个偏心率为二分之一的轨道运行了一千圈，每圈一百步。<bookmark mark='d'/>四阶 Runge–Kutta 的轨道缩小了。"
        "蛙跳法的轨道大小正确，但转了一个角度。",
    "Here is the energy after every orbit. <bookmark mark='a'/>":
        "这是每一圈之后的能量。<bookmark mark='a'/>四阶 Runge–Kutta 一开始更精确，但它的误差稳步增长，一千圈后达到百分之三。"
        "<bookmark mark='b'/>蛙跳法的误差大约是百分之一，而且从不增长。<bookmark mark='c'/>大约370圈之后，蛙跳法领先，而且差距只会越来越大。"
        "<bookmark mark='d'/>原因是一条定理：辛方法几乎精确地守恒一个稍有不同的能量，也就是修正哈密顿量，所以真正的能量只能围绕它摆动。"
        "<bookmark mark='e'/>这又是第二章的向后误差分析：方法几乎精确地求解了一个邻近的问题。",
    # ------------------------------------------------------------------ s15_speed
    "Chapter fourteen. Speed: BLAS, LAPACK, and mixed precision.":
        "第十四章：速度：BLAS、LAPACK 与混合精度。",
    "Almost every algorithm in this part spends its time in a few":
        "这一部分里几乎每一个算法，都把时间花在少数几个内核上，它们被标准化为基本线性代数子程序，也就是 BLAS。<bookmark mark='a'/>第一级来自1979年，作用于向量：a 乘 x 加 y，"
        "每个元素做两次运算，搬动24个字节，也就是每字节十二分之一次运算。<bookmark mark='b'/>第二级来自1988年，做矩阵乘以向量，每个矩阵元素只用一次：每字节四分之一次。"
        "<bookmark mark='c'/>第三级来自1990年，做矩阵乘矩阵：对3n 平方个数做2n 立方次运算，强度是 n 除以12，随 n 增长。"
        "<bookmark mark='d'/>这就是一行字写下的第9部分的屋顶线模型：只有第三级在每个字节上做了足够多的算术，能让处理器一直忙碌。",
    'f"Here are the three levels timed on this machine,':
        "这是三个级别在这台机器上的计时，通过 NumPy，它调用的是一个优化过的 BLAS。<bookmark mark='a'/>矩阵乘法随着 n 增大而攀升，"
        "在2048阶时达到大约每秒{big['gemm_gflops']:.0f}吉次运算。<bookmark mark='b'/>另外两个在这个规模上，"
        "只能达到每秒{big['axpy_gflops']:.1f}吉次和{big['gemv_gflops']:.0f}吉次：做的是同一类算术，"
        "却慢了{big['gemm_gflops'] / big['axpy_gflops']:.0f}倍和{big['gemm_gflops'] / big['gemv_gflops']:.0f}倍。"
        "<bookmark mark='c'/>小的向量加法能放进缓存，比大的跑得更快，这是第9部分的存储层次，而不是算术。<bookmark mark='d'/>所以，1990年以来，"
        "数值线性代数的手艺就是改写每一个算法，让它的大部分工作都落在第三级上。",
    "LAPACK, released in 1992, does exactly that. <bookmark":
        "1992年发布的 LAPACK 做的正是这件事。<bookmark mark='a'/>拿来第三章的消去法，但不再一次处理一列，而是分解一个由 b 列组成的窄面板，"
        "<bookmark mark='b'/>然后一次性更新它右下方的全部内容：尾随矩阵减去两个瘦块的乘积，也就是一次矩阵乘法。<bookmark mark='c'/>移到下一个面板。"
        "只有面板在第二级上运行，在三分之二 n 立方次运算中，大约占 n 平方乘 b 除以2次，<bookmark mark='d'/>比例是4n 分之3b。对一万个未知数、宽度64的面板，是百分之零点五。"
        "NumPy 求解线性方程组时，调用的正是这个例程。",
    "Speed also comes from fewer bits: single precision moves":
        "速度也来自更少的位数：单精度搬动的字节数减半，通常至少快一倍。<bookmark mark='a'/>所以用单精度把矩阵分解一次：这是 n 立方的工作量。"
        "<bookmark mark='b'/>用双精度计算残差，它只花 n 的平方，<bookmark mark='c'/>用便宜的因子解出一个修正量，把它加上去。"
        "<bookmark mark='d'/>每一轮都把误差乘以大约 κ 乘以单精度的单位舍入误差，所以当这个乘积小于1时，它就收敛。<bookmark mark='e'/>当 κ 为10的5次方时，"
        "我们的仪器每一轮获得将近三位数字，四轮之后，就和一次完整的双精度求解差不多一样精确。第十五章会一直降到16位。",
    '''f"Since 1993 the world's fastest computers have been''':
        "自1993年起，世界上最快的计算机每年排名两次，登上 Top500 榜单，所用的是一个程序：High-Performance Linpack，"
        "它源自 Jack Dongarra 在1979年参与编写的 LINPACK 库。<bookmark mark='a'/>它用部分选主元的消去法求解一个稠密的随机方程组，"
        "再把三分之二 n 立方次运算除以所用的时间。其中几乎全部是矩阵乘法，所以它衡量的是一台机器的最佳状态。<bookmark mark='b'/>在这个刻度上，我们机器的第一级速度在这里，"
        "它的矩阵乘法在这里。<bookmark mark='c'/>2022年6月，橡树岭的 Frontier 成为第一台每秒运算超过10的18次方次的计算机："
        "大约是我们矩阵乘法的{ratio / 1000000.0:.0f}百万倍。<bookmark mark='d'/>一个共轭梯度基准测试，像大多数真实的模拟一样稀疏、受内存限制，在同样的机器上只能达到峰值的百分之几。",
    # ------------------------------------------------------------------ s16_frontier
    "Chapter fifteen, the frontier. Can randomness, and fewer":
        "第十五章，前沿。随机性和更少的位数，能不能让线性代数更快，同时依然正确？",
    'f"The first frontier is randomness. <bookmark':
        "第一个前沿是随机性。<bookmark mark='a'/>要用一个秩为{r['k']}的矩阵来近似一个大矩阵，就把它乘以一个瘦长的随机矩阵。乘积的各列是这个矩阵自身各列的随机混合，"
        "它们以很高的概率几乎恰好张成它最重要的那些方向。<bookmark mark='b'/>把它们标准正交化，做投影，再对一个小矩阵做 SVD。"
        "Nathan Halko、Per-Gunnar Martinsson 和 Joel Tropp 在2011年分析了这个方法。"
        "<bookmark mark='c'/>在我们那个{r['m']:,}乘{r['n']:,}的矩阵上，多加几个随机列，再做一两次幂迭代，"
        "误差就能达到任何秩{r['k']}矩阵所能做到的最好结果的百分之{max(1, round(100 * (best['ratio'] - 1)))}以内，"
        "所用的时间只是完整 SVD 所需{r['full_seconds']:.1f}秒的一小部分。",
    "The second frontier is precision. Graphics processors do":
        "第二个前沿是精度。图形处理器用16位做算术，比用64位快很多倍，因为机器学习需要它们这样。数值线性代数能不能利用这些位数，而不损失精度？<bookmark mark='a'/>迭代改进，"
        "这是威尔金森的一个想法，它的回答是：能，有时候能。用低精度便宜地分解矩阵，用高精度计算残差，再用便宜的因子解出一个修正量。<bookmark mark='b'/>对一个良态矩阵，"
        "误差在两三步内就降到双精度的水平。<bookmark mark='c'/>当条件数为10的8次方时，乘以单精度大约10的负7次方的机器精度，乘积超过了1，迭代改进就发散了。自2019年起，"
        "一个基于这个想法的基准测试，与经典的 Linpack 超级计算机排名并列发布。",
    "The third frontier is a theorem we do not have. Partial":
        "第三个前沿是一条我们还没有的定理。部分选主元可能让元素增长到2的 n 减1次方倍，所以在最坏情况下，消去法是不稳定的，然而在实践中，它从来不会这样。"
        "<bookmark mark='a'/>拿来威尔金森的最坏情况矩阵，加上一亿分之一的噪声。增长就从20亿降到了2。最坏情况需要每一列都恰好打平，而任何扰动都会打破它们。"
        "<bookmark mark='b'/>Daniel Spielman 和滕尚华发明了平滑分析，来解释为什么单纯形法在实践中很快：最坏情况被容易的情况包围着。对部分选主元的消去法，类似的定理，"
        "也就是在小的随机扰动下增长是多项式的，还没有被证明。",
    "Open problems. <bookmark mark='a'/> Whether matrices can be":
        "未解问题。<bookmark mark='a'/>矩阵乘法能否在接近 n 平方的时间内完成，这是第19部分提出的问题。<bookmark mark='b'/>线性方程组能否也这么快地求解，"
        "同时依然稳定，在实践中而不只是在理论上。<bookmark mark='c'/>哪些算法能在16位算术中幸存下来，又需要什么样的修正。<bookmark mark='d'/>还有那些搬动数据的代价，"
        "如今已占主导，达到其下界的算法。<bookmark mark='e'/>这一部分的研究题就是那条缺失的定理：证明对任何加上一点高斯噪声扰动的矩阵，部分选主元的消去法以很高的概率具有多项式有界的增长。",
    # ------------------------------------------------------------------ s17_outro
    "What we built in this part. The condition number, which says":
        "这一部分我们搭建了什么。条件数，它说明一个问题有多难，与向后稳定性分开，后者说明一个算法有多好，以及把两者连起来的规则：向前误差至多是条件数乘以向后误差。靠选主元变得稳定的消去法；"
        "Householder 的镜子和 SVD；三次收敛的 QR 算法；用于有几百万个未知数的方程组的共轭梯度法、多重网格和稀疏排序；牛顿法和它的分形；切比雪夫点、高斯求积、刚性求解器和辛积分器。"
        "一个思想贯穿其中：既然舍入无处不在，正确的问题就不是一个答案是否精确，而是它是不是一个邻近问题的精确答案。",
    "Where this comes back. Part 51's renderer is linear algebra":
        "这些内容会在哪里再出现。第51部分的渲染器就是线性代数和积分，每秒做几十亿次。第53部分的量子计算机，是一个作用在向量上的酉矩阵。第54部分证明程序是正确的，浮点数也包括在内。"
        "第56部分通过一个图的矩阵的特征值来解读这个图。而第57部分的学习理论，依赖的是同样的优化。",
    "In practice. Never invert a matrix to solve a system: factor":
        "实践中。永远不要为了求解方程组而对矩阵求逆：要分解它，并且选主元。用 QR 或 SVD 做最小二乘拟合，而不是用正规方程。估计条件数，并报告残差，而不只是答案。对大型方程组，使用稀疏方法和迭代方法，"
        "配上一个好的预条件子。还有，调用 BLAS 和 LAPACK：只有在想学习它的原理时，才自己写矩阵乘法。",
    "Six problems, with full solutions in the part's notes. Pause":
        "六道习题，完整解答在这一部分的笔记里。可以在任何一道上暂停。第五道是构建题：为一维泊松问题写一个两重网格求解器，它的收敛因子不应依赖于网格的大小。最后一道标有星号，是研究题："
        "证明只要矩阵受到一点噪声的扰动，部分选主元的增长就是多项式的。",
    "Next time, Part 53: quantum computation. A qubit is a unit":
        "下一次，第53部分：量子计算。一个量子比特是二维复空间中的一个单位向量，一个门是一个酉矩阵，而一次计算就是它们的乘积，又是线性代数。干涉让错误的答案相互抵消，而建立在它之上的一个算法，Shor 算法，"
        "将终结第30部分的公钥密码学。",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书和论文都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
