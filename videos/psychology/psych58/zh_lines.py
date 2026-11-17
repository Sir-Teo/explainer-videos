"""Chinese narration for psych58: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第58部分：高效、预测的大脑'

CHAPTERS = {
    'Hook': '一个长出了感受野的网络',
    'Predict': '1. 在你身上：一种后效，以及四个数字',
    'Efficient': '2. 高效编码',
    'Sparse': '3. 稀疏编码',
    'Bias': '4. 效率解释偏差',
    'Rate': '5. 率失真',
    'Normalize': '6. 归一化',
    'Predictive': '7. 预测编码',
    'Free': '8. 自由能原理',
    'Bayes': '9. 贝叶斯脑及其批评者',
    'Resource': '10. 资源理性',
    'Learning': '11. 学习规则',
    'Unified': '12. 统一理论',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：编解码器与表征',
    'Frontier': '15. 前沿：一个原理？',
    'Outro': '回顾、习题与前方的路',
}

ZH = {
    "In 1959 Hubel and Wiesel found cells in the cat's visual cortex that respond to edges at o":
        "1959年，休伯尔和维泽尔在猫的视觉皮层中发现了一些细胞，它们只对某一位置、某一朝向的边缘作出反应。第13部分讲过这个故事。<bookmark mark='a'/>这里有另一条通向同样细胞的路。Psyche的世界是一幅枯叶图像：大小和明暗随机的圆盘层层堆叠，这是自然场景统计特性的一个标准替身。<bookmark mark='b'/>六十四个单元必须描述它的小块图像，并且要让尽可能少的单元处于活跃状态。<bookmark mark='c'/>没有人告诉它们该变成什么。它们一开始是随机的图块。<bookmark mark='d'/>十步之后，没什么变化。五十步之后，出现了结构。<bookmark mark='e'/>四百步之后，它们变成了小的、有朝向的边缘检测器：第13部分的简单细胞，从一个原理中长了出来。",
    "So this part asks: is there one principle from which the mind's mechanisms follow? <bookma":
        "所以这一部分要问：是否存在一个原理，心智的各种机制都由它推出？<bookmark mark='a'/>1961年，霍勒斯·巴洛提出，感觉神经元的存在是为了去除其输入中的冗余。<bookmark mark='b'/>1996年，布鲁诺·奥尔斯豪森和大卫·菲尔德在自然照片上运行了你刚刚看到的那种优化，得到了同样的结果。一个优化原理产生了生物学。<bookmark mark='c'/>我们会追踪它的后代：高效编码、预测编码，以及自由能原理，一个声称能解释大脑所做的一切的理论。<bookmark mark='d'/>我们还会提出每个宏大理论都必须回答的问题：它必须冒什么风险？",
    "This is Part 58 of Psychology, Built: the efficient, predictive brain. <bookmark mark='a'/":
        "这是《心理学，从零搭建》第58部分：高效、预测的大脑。<bookmark mark='a'/>我们会从效率推导出中心-周边细胞和边缘检测器。我们会从高效编码预测后效和偏差。我们会从率失真理论推导出泛化，并认识归一化的那一个方程。我们会一步一步构建预测编码和自由能。我们会权衡贝叶斯脑、资源理性和学习规则。我们还会追问一个统一理论必须冒什么风险。",
    'Chapter one. On you: an after-effect, and four numbers.':
        '第1章。在你身上：一种后效，以及四个数字。',
    "First, an experiment on you. <bookmark mark='a'/> Look at the small yellow bar between the":
        "首先，一个在你身上做的实验。<bookmark mark='a'/>看着两个圆之间的那根黄色小横条，让你的目光沿着它从一端慢慢移到另一端。继续看。上面的线条向一边倾斜，下面的线条向另一边倾斜。在接下来的半分钟里一直盯着这根横条。你的朝向调谐神经元正在适应，对它们一直看到的朝向调低增益。眼睛继续盯着横条。这和让你看瀑布之后再看岩石时岩石似乎在上升的，是同一种机制。<bookmark mark='b'/>现在。这些线条是竖直的吗？",
    "They are vertical. <bookmark mark='a'/> Most people see the top lines tilted to the left a":
        "它们是竖直的。<bookmark mark='a'/>大多数人会看到上面的线条向左倾斜，下面的线条向右倾斜，与他们适应过的方向相反。<bookmark mark='b'/>这就是倾斜后效。适应过的单元反应变弱了，而一个仍然假定它们没变的读出，被推离了适应刺激。<bookmark mark='c'/>第四章会从高效编码预测出它的大小。",
    "Now four numbers. <bookmark mark='a'/> One: after staring at lines tilted twenty degrees c":
        "现在是四个数字。<bookmark mark='a'/>第一：盯着顺时针倾斜二十度的线条看过之后，一条竖直的线看起来向哪边倾斜，大约倾斜多少？<bookmark mark='b'/>第二：竖直和水平是世界上最常见的朝向。一条接近竖直的线，看起来是被拉向竖直，还是被推离竖直？<bookmark mark='c'/>第三：一个神经元对对比度有二十个反应等级。哪些对比度应该得到最多的等级？<bookmark mark='d'/>第四：你通过从自己的信念中抽取样本来作决定，而每个样本都要花时间。最好的样本数是多少？在这里暂停，把答案写下来。",
    'Chapter two. Efficient coding.':
        '第2章。高效编码。',
    "Why would a neuron care about statistics? <bookmark mark='a'/> In 1954 Fred Attneave point":
        "为什么一个神经元要关心统计规律？<bookmark mark='a'/>1954年，弗雷德·阿特尼夫指出，自然图像是冗余的：一幅图的大部分内容可以从相邻的点和边缘猜出来。<bookmark mark='b'/>1961年，霍勒斯·巴洛认为，感官的容量有限，所以好的编码会把容量花在无法预测的东西上。<bookmark mark='c'/>这就是高效编码假说：神经元被调谐到世界的统计规律上，在其限制允许的范围内携带尽可能多的信息。<bookmark mark='d'/>这是一个规范性理论。它先说明编码应该是什么样子，再检查神经元是否如此。",
    "Here's the first clean test. <bookmark mark='a'/> In 1981 Simon Laughlin studied cells in ":
        "这里是第一个干净的检验。<bookmark mark='a'/>1981年，西蒙·劳克林研究了苍蝇眼中反应范围有限的细胞。<bookmark mark='b'/>为了让每个等级被使用得同样频繁，反应应该是苍蝇所遇到的对比度的累积分布：在对比度常见的地方陡峭，在罕见的地方平缓。<bookmark mark='c'/>他测量了苍蝇栖息地中的对比度，细胞的反应曲线与预测相吻合。<bookmark mark='d'/>在Psyche的世界里，二十个等级在匹配时每次反应携带约四点二比特，在均匀分布时为三点七比特。你的第三个数字：最常见的对比度，接近零的那些，得到最多的等级。",
    "Now take the same idea to space. <bookmark mark='a'/> Natural images have most of their po":
        "现在把同样的想法用到空间上。<bookmark mark='a'/>自然图像的大部分能量在低空间频率，大致按频率平方的倒数下降。这里是Psyche图块每个成分的方差，用对数刻度表示。<bookmark mark='b'/>去除这种冗余，称为白化，会把频谱拉平，让每个成分携带相同的方差。<bookmark mark='c'/>这里是完成它的滤波器，针对一个像素：一个明亮的中心和一个暗的环。这就是第13部分的视网膜神经节细胞。<bookmark mark='d'/>约瑟夫·阿蒂克和诺曼·雷德利克补充说，视网膜应该在噪声占主导的高频处衰减，而它确实如此。",
    'Chapter three. Sparse coding.':
        '第3章。稀疏编码。',
    "Why edges? Here's the objective, written out. <bookmark mark='a'/> Describe each patch x a":
        "为什么是边缘？这里把目标函数写出来。<bookmark mark='a'/>把每个图块x描述为基函数之和：D乘以一个编码a。<bookmark mark='b'/>最小化平方误差加上lambda乘以编码的绝对值之和。拟合得好，同时活跃的单元少。<bookmark mark='c'/>对每个图块，用几步收缩求出编码，这个算法叫ISTA。然后微调基函数让拟合更好，再重复。<bookmark mark='d'/>Lambda设定了活跃的代价。太低，单元会保持分散。太高，拟合就差。<bookmark mark='e'/>奥尔斯豪森和菲尔德在1996年把它用在白化后的照片上，得到了局部化、有朝向、带通的单元，就像V1的简单细胞。",
    'Is it the sparseness that matters? Compare two codes for the same patches. <bookmark mark=':
        "关键是稀疏性吗？比较同一批图块的两种编码。<bookmark mark='a'/>稀疏的单元小而有朝向。只做去相关的主成分是全局的波纹，就像傅里叶基。<bookmark mark='b'/>测量每个单元有多少能量集中在它最强的三乘三区域。稀疏编码：约零点八。主成分和随机模式：约零点二五。<bookmark mark='c'/>只做去相关得到的是波纹。稀疏性要求的是独立的成因，而边缘正是图像的组成部分。",
    "How far does it go? <bookmark mark='a'/> It's replicated. Independent component analysis g":
        "它能走多远？<bookmark mark='a'/>它被重复了。独立成分分析给出了同样的滤波器，正如安东尼·贝尔和特伦斯·谢诺夫斯基在1997年所展示的，许多后来的方法也是如此，包括深度网络的第一层。<bookmark mark='b'/>同样的目标用于声音，得到了像耳蜗那样的滤波器，正如迈克尔·莱维茨基在2002年所展示的。<bookmark mark='c'/>但它并不精确。实测的V1感受野比模型的更圆、更多样，这是达里奥·林加赫发现的。<bookmark mark='d'/>关于Psyche还要说明一点：它的图像是合成的枯叶图，而不是一套有授权的照片。结果在性质上相同，只是感受野更小。",
    'Chapter four. Efficiency explains biases.':
        '第4章。效率解释偏差。',
    "Start with the after-effect you just saw. <bookmark mark='a'/> Psyche's population has sev":
        "从你刚刚看到的后效开始。<bookmark mark='a'/>Psyche的群体有七十二个调谐到不同朝向的单元。适应会降低调谐在适应刺激附近的单元的增益。<bookmark mark='b'/>读出仍然假定旧的增益，所以每个测试刺激都被推离适应刺激。<bookmark mark='c'/>偏移在离适应刺激十到二十五度处最大：二十度时约四度，这是你的第一个数字。人们报告的是几度。<bookmark mark='d'/>为什么要适应呢？把编码重新对准最近的输入，能在世界变化时保持高效。错觉就是代价。",
    "Now a bias that seemed to break the Bayesian story. <bookmark mark='a'/> Vertical and hori":
        "现在来看一个似乎打破了贝叶斯故事的偏差。<bookmark mark='a'/>竖直和水平是最常见的朝向，所以一个简单的贝叶斯观察者应该被拉向它们。<bookmark mark='b'/>但人们会把接近竖直的线条判断为被推离竖直。<bookmark mark='c'/>2015年，魏学昕和艾伦·斯托克说明了原因。如果编码器把精确度花在先验高的地方，似然就会变得不对称，后验就落在了另一侧。结果是排斥。<bookmark mark='d'/>Psyche的高效观察者偏离竖直和水平约二点五度。这是你的第二个数字。<bookmark mark='e'/>他们2017年的规律，即偏差与判别阈值平方的斜率成正比，在许多已发表的数据集中都成立。",
    "What else does efficiency explain? <bookmark mark='a'/> Weber's law: a code whose resource":
        "效率还能解释什么？<bookmark mark='a'/>韦伯定律：一个按强度的重尾分布分配资源的编码，会给出与强度成正比的阈值，正如迪普·甘古利和埃罗·西蒙切利所展示的。这是第11部分。<bookmark mark='b'/>容量限制：工作记忆是一个信息有限的通道，第19部分，项目增加时精确度下降。<bookmark mark='c'/>价值：编码价值的神经元会按可选的选项进行归一化，这会在选择中产生情境效应，第26部分。<bookmark mark='d'/>还有警示：几乎任何偏差都能用某个先验加某种资源限制来拟合。真正的检验是一个独立测量的先验，就像劳克林测量他那只苍蝇的世界那样。",
    'Chapter five. Rate-distortion.':
        '第5章。率失真。',
    "What's the cheapest representation that's good enough? <bookmark mark='a'/> Rate is how ma":
        "足够好的最便宜的表征是什么？<bookmark mark='a'/>率是一个表征携带了多少比特关于刺激的信息。失真是它所允许的错误的期望代价。<bookmark mark='b'/>香农的率失真理论给出，对每一个可容忍的失真，达到它所需的最小率。<bookmark mark='c'/>等价地，最小化率加上beta乘以失真，其中beta是错误的代价有多高。<bookmark mark='d'/>理查德·布拉胡特和有本卓的算法通过交替进行两个简单的更新来找到最佳通道。<bookmark mark='e'/>对大脑来说，知觉和记忆是必须便宜的通道，而它们的错误应该是代价低的错误。",
    "Here's a law it derives. <bookmark mark='a'/> In Part 22, Roger Shepard's universal law of":
        "这里是它推导出的一条定律。<bookmark mark='a'/>在第22部分，罗杰·谢泼德的泛化普遍定律：在不同物种和刺激之间，泛化大致随心理距离指数下降。<bookmark mark='b'/>这里是Psyche在三种错误代价下的最佳通道。便宜的编码，率低，会大范围地混淆相近的刺激。<bookmark mark='c'/>昂贵的编码泛化得很窄，而每一条梯度都是平滑的下降。<bookmark mark='d'/>2018年，克里斯·西姆斯证明，这条定律可以从一个高效通道中推出，无需对心理空间的几何作任何假设。",
    'Chapter six. Normalization.':
        '第6章。归一化。',
    "Is there a canonical computation? Here's a candidate: one equation. <bookmark mark='a'/> A":
        "存在一种典范计算吗？这里有一个候选：一个方程。<bookmark mark='a'/>一个神经元的驱动，除以一群邻近神经元的活动总和再加上一个常数。<bookmark mark='b'/>它的反应在高对比度时饱和，而一个驱动邻近群体却不驱动该细胞的掩蔽刺激会抑制它。<bookmark mark='c'/>在对数轴上，曲线横向平移：改变的是增益，而不是形状。<bookmark mark='d'/>大卫·黑格在1992年为视觉皮层提出了它，2012年马泰奥·卡兰迪尼和黑格认为它是一种典范的神经计算。",
    "The same equation appears everywhere. <bookmark mark='a'/> In the retina, light adaptation":
        "同一个方程到处出现。<bookmark mark='a'/>在视网膜中，光适应把反应除以平均光照水平。<bookmark mark='b'/>在视觉皮层中，它带来对比度饱和以及跨朝向抑制。<bookmark mark='c'/>在注意中：约翰·雷诺兹和大卫·黑格2009年的模型让注意在归一化之前放大驱动，它再现了第18部分的许多发现。<bookmark mark='d'/>在价值中：一个选项的价值除以其他可选的选项，来自第26部分。<bookmark mark='e'/>以及它为什么高效：除掉共享的活动，就去除了邻近单元之间的冗余。这又是巴洛的原理，正如奥德莉娅·施瓦茨和埃罗·西蒙切利在2001年所展示的。",
    'Chapter seven. Predictive coding.':
        '第7章。预测编码。',
    "Does the cortex send its predictions down? <bookmark mark='a'/> In 1999 Rajesh Rao and Dan":
        "皮层会把它的预测向下发送吗？<bookmark mark='a'/>1999年，拉杰什·拉奥和达娜·巴拉德构建了一个层级结构，其中每一层预测下一层的活动。<bookmark mark='b'/>向上传递的只有误差：输入中预测没能解释的那部分。<bookmark mark='c'/>每一层调整自己的成因，以缩小上下两层的误差。这是通过梯度下降进行的推断。<bookmark mark='d'/>它解释了末端抑制：当一条线延伸到感受野之外时，细胞会停止放电，因为长线条是从上层预测出来的。<bookmark mark='e'/>它和高效编码是同一个想法：不要发送接收者已经能预测的东西。",
    "Here's the loop, small enough to watch. <bookmark mark='a'/> Psyche's two-level network ha":
        "这里是这个回路，小到可以看清楚。<bookmark mark='a'/>Psyche的两层网络有十六个输入、四个成因，以及一个关于成因的先验。<bookmark mark='b'/>给它一个预期的输入，误差单元几乎没有反应。<bookmark mark='c'/>给它一个意外的输入，就会有一阵误差爆发，在成因稳定下来的过程中被吸收。<bookmark mark='d'/>剩下的是与先验的分歧。网络学到了一些东西。<bookmark mark='e'/>所以对生理学的预测是：对预期刺激的反应被抑制，对意外刺激的反应被增强。",
    "What does the evidence support? <bookmark mark='a'/> Expected stimuli evoke smaller respon":
        "证据支持什么？<bookmark mark='a'/>预期的刺激诱发的反应更小：重复抑制、第15部分的失匹配负波，以及对被省略刺激的反应。<bookmark mark='b'/>小鼠初级视觉皮层会对奔跑与视觉流之间的不匹配作出反应，这是格奥尔格·凯勒及其同事在2012年发现的。<bookmark mark='c'/>存在争议的是：按这一方案的要求，存在分别位于不同皮层的误差神经元和预测神经元。证据零零散散。<bookmark mark='d'/>还有一个问题：对预期刺激的抑制也可以由适应和注意来预测，所以单靠它无法单独证明预测编码。",
    'Chapter eight. The free-energy principle.':
        '第8章。自由能原理。',
    'Can one quantity explain everything a brain does? First, the mathematics, step by step. <b':
        "一个量能解释大脑所做的一切吗？首先，一步一步来看数学。<bookmark mark='a'/>贝叶斯法则给出了在数据x下成因z的后验，但它需要数据的概率，而这通常无法计算。<bookmark mark='b'/>所以选一个简单的分布族q，并定义自由能F：q的对数的期望减去联合分布的对数。<bookmark mark='c'/>整理之后，它是q与真实后验之间的散度，加上意外程度，即负的log p(x)。<bookmark mark='d'/>散度永远不为负，所以对q最小化F就是在做推断，而它的最小值是意外程度的一个界。这就是《AI，从零搭建》中的变分推断。",
    "Here's the free energy of a small model. <bookmark mark='a'/> A cause z has a standard nor":
        "这里是一个小模型的自由能。<bookmark mark='a'/>一个成因z服从标准正态先验，一个读数为二的观测带着标准差零点五的噪声到来。<bookmark mark='b'/>把F对q的均值作图，它是一个碗。<bookmark mark='c'/>碗底是精确的后验均值，一点六，碗底的高度是意外程度，约二点六奈特。<bookmark mark='d'/>到这里为止，这是一个定理。它对任何模型都成立，只能通过所选择的那个模型来检验。",
    "Now the principle. <bookmark mark='a'/> Karl Friston argues that any system that persists ":
        "现在来看这个原理。<bookmark mark='a'/>卡尔·弗里斯顿认为，任何持续存在的系统都必须让自己的感觉状态不出意外，所以它必须最小化自由能。<bookmark mark='b'/>在知觉中，它改变自己的信念来适应输入，而预测编码是一种实现方式。<bookmark mark='c'/>在行动中，它改变输入来适应自己的信念。这就是主动推断，欲望被重新表述为对偏好状态的预测。<bookmark mark='d'/>批评是：如果模型和先验可以自由选择，任何行为都可以被描述为最小化自由能，而一个不可能失败的原理，并不能被它的成功所检验。<bookmark mark='e'/>回应是：这个原理是一个框架，就像物理学中的哈密顿原理，而用它构建的具体模型确实会作出可检验的预测。",
    'Chapter nine. The Bayesian brain and its critics.':
        '第9章。贝叶斯脑及其批评者。',
    "Optimal against what? First, where the Bayesian account earned its place. <bookmark mark='":
        "相对于什么而言最优？首先，贝叶斯解释在哪里赢得了一席之地。<bookmark mark='a'/>线索整合：视觉和触觉按各自的可靠性加权，正如最优解所要求的。这是马克·恩斯特和马丁·班克斯在2002年的发现，也是第14部分的内容。<bookmark mark='b'/>运动控制：人们学习扰动的分布和自身的噪声，并据此计划，正如康拉德·科丁和丹尼尔·沃尔珀特所展示的。<bookmark mark='c'/>作为最优猜测的错觉：一个偏好慢速运动的先验，解释了为什么在低对比度下东西看起来更慢。<bookmark mark='d'/>它的长处是根据测量的噪声作出定量预测，没有自由的权重。",
    "Now the critics. <bookmark mark='a'/> Jeffrey Bowers and Colin Davis called many Bayesian ":
        "现在来看批评者。<bookmark mark='a'/>杰弗里·鲍尔斯和科林·戴维斯把许多贝叶斯解释称为“想当然的故事”：先验和似然在事后选定，任何行为都可以被称为最优。<bookmark mark='b'/>马特·琼斯和布拉德利·洛夫警告贝叶斯原教旨主义，它拟合数据，却不问计算是如何完成的。<bookmark mark='c'/>多布罗米尔·拉内夫和雷切尔·丹尼森表明，人们在许多任务中稳定地次优，并认为有用的问题是如何次优。<bookmark mark='d'/>辩护是：作为一个先验经过测量的模型来使用，贝叶斯解释能够预测。作为对一切的描述来使用，它就不能。",
    "So how do you keep it honest? <bookmark mark='a'/> Measure the prior independently: from t":
        "那么如何让它保持诚实？<bookmark mark='a'/>独立地测量先验：从环境的统计规律中，像劳克林的苍蝇那样，或者从训练中。<bookmark mark='b'/>从判别阈值中独立地测量噪声。<bookmark mark='c'/>然后在没有剩余参数可拟合的情况下预测一个新任务。<bookmark mark='d'/>并与一个具名的替代模型比较，而不是与没有模型比较。这是第48部分的模型比较。",
    'Chapter ten. Resource rationality.':
        '第10章。资源理性。',
    "Are heuristics optimal after all? <bookmark mark='a'/> In 2014 Edward Vul, Noah Goodman, T":
        "启发式最终是最优的吗？<bookmark mark='a'/>2014年，爱德华·伍尔、诺亚·古德曼、托马斯·格里菲斯和约书亚·特南鲍姆对这样的决策建模：从后验中抽取几个样本，取多数。<bookmark mark='b'/>样本越多，准确率越高：一个样本时为零点六五，五十个样本时为零点九八。<bookmark mark='c'/>但如果每个样本都要花时间，单位时间的回报在只抽一个样本时最高。这是你的第四个数字。<bookmark mark='d'/>概率匹配常被称为非理性的，而它恰恰是只抽一个样本的决策者会做的事。",
    "Resource rationality makes this general. <bookmark mark='a'/> Falk Lieder and Thomas Griff":
        "资源理性把这一点推广开来。<bookmark mark='a'/>福尔克·利德和托马斯·格里菲斯把它定义为考虑到思考成本时的最佳策略，而不是在时间无限时的最佳答案。<bookmark mark='b'/>锚定与调整，或者第26部分的取最佳线索这样的启发式，在思考代价高昂时可以是理性的。<bookmark mark='c'/>一个检验：当成本和利害改变时，人们会朝分析所预测的方向改变策略。<bookmark mark='d'/>风险和以前一样：如果成本可以自由选择，任何行为都是资源理性的，所以成本也必须加以测量。",
    'Chapter eleven. Learning rules.':
        '第11章。学习规则。',
    "How does a brain learn what to predict? <bookmark mark='a'/> Deep networks learn by sendin":
        "大脑如何学会预测什么？<bookmark mark='a'/>深度网络通过把精确的误差梯度反向传过每一个突触来学习，而神经元显然做不到这一点。<bookmark mark='b'/>但随机的反向权重仍然能教会一个网络，蒂莫西·利利克拉普及其同事称之为反馈对齐。<bookmark mark='c'/>而预测编码的误差单元一旦稳定下来，就近似于反向传播的梯度，正如詹姆斯·惠廷顿和拉法尔·博加奇所展示的。<bookmark mark='d'/>在2020年的一篇综述中，利利克拉普及其同事认为大脑可能用局部信号和反馈来近似反向传播。这还没有被详细检验。",
    "There's a second kind of learning. <bookmark mark='a'/> Part 17's dopamine prediction erro":
        "还有第二种学习。<bookmark mark='a'/>第17部分的多巴胺预测误差训练前额叶皮层中慢变的权重。<bookmark mark='b'/>2018年，简·王及其同事表明，以这种方式训练的循环网络，会在其活动中学到一种它自己的快速学习算法。<bookmark mark='c'/>它再现了哈里·哈洛的学习定势：猴子在同一类的每个新问题上都学得更快。<bookmark mark='d'/>同样的想法驱动着今天的语言模型，它们从提示中的例子学习，而不改变任何权重。这是第60部分的内容。",
    'Chapter twelve. Unified theories.':
        '第12章。统一理论。',
    "What would a theory of everything a mind does have to risk? <bookmark mark='a'/> In 1973 A":
        "一个关于心智所做一切的理论必须冒什么风险？<bookmark mark='a'/>1973年，艾伦·纽厄尔抱怨说，心理学研究了一个又一个效应，每个都有自己的小模型，永远加不到一起。你无法和自然玩二十个问题并获胜。<bookmark mark='b'/>他的答案是认知的统一理论：一个能完成所有任务的架构。<bookmark mark='c'/>约翰·安德森的ACT-R，以及由约翰·莱尔德、纽厄尔和保罗·罗森布卢姆构建的Soar，在一个系统中积累了数十年的记忆、技能和问题解决模型。<bookmark mark='d'/>2017年，“认知的通用模型”列出了这些架构达成一致的内容。<bookmark mark='e'/>今天的竞争者是大型脑模拟，以及同时在许多实验上训练的模型，第60部分会讨论它们。",
    "Here's each principle in this part, and what it risked. <bookmark mark='a'/> Efficient cod":
        "这里是这一部分中的每个原理，以及它冒了什么风险。<bookmark mark='a'/>高效编码在测量之前就预测了后效、排斥性偏差和劳克林的曲线，并且站住了。<bookmark mark='b'/>归一化预测了增益变化、抑制和注意效应，并且站住了。<bookmark mark='c'/>预测编码预测了独立的误差神经元和对预期刺激的抑制，结果好坏参半。<bookmark mark='d'/>贝叶斯脑用测量的噪声去冒线索权重的风险，在先验经过测量的地方表现很好。<bookmark mark='e'/>自由能原理本身什么风险都不冒。是它的模型在预测。<bookmark mark='f'/>一个原理不经测量就能解释的越多，它冒的风险就越少。",
    'Chapter thirteen. The Ledger.':
        '第13章。账本。',
    'Four new rows. The first: a sparse code for natural images learns receptive fields like V1':
        "四个新条目。第一条：自然图像的稀疏编码学到了像V1简单细胞那样的感受野。<bookmark mark='a'/>原始研究：奥尔斯豪森与菲尔德，1996年。<bookmark mark='b'/>记录：独立成分分析、与实测细胞的比较，以及对真实感受野的综述。<bookmark mark='c'/>计算可以重现；匹配是定性的。<bookmark mark='d'/>已重复。",
    "The second: an efficient code predicts biases away from common values. <bookmark mark='a'/":
        "第二条：高效编码预测了偏离常见值的偏差。<bookmark mark='a'/>原始研究：魏学昕与斯托克，2015年。<bookmark mark='b'/>记录：他们提出的偏差与阈值之间的规律关系，在许多数据集中成立。<bookmark mark='c'/>在先验经过测量的地方最强。<bookmark mark='d'/>已重复。",
    'The third: cortex has distinct prediction-error neurons, as predictive coding requires. <b':
        "第三条：如预测编码所要求的，皮层中有独立的预测误差神经元。<bookmark mark='a'/>原始研究：拉奥与巴拉德，1999年。<bookmark mark='b'/>记录：小鼠V1中的失匹配神经元，以及一篇证据综述。<bookmark mark='c'/>对意外刺激的反应是稳健的；专门的误差单元尚未确立。<bookmark mark='d'/>存在争议。",
    "And the fourth: everything a brain does minimizes free energy. <bookmark mark='a'/> The or":
        "第四条：大脑所做的一切都是在最小化自由能。<bookmark mark='a'/>原始研究：弗里斯顿，2010年。<bookmark mark='b'/>记录：一篇关于它是哪一类主张的分析。<bookmark mark='c'/>一个框架，它的模型必须逐一检验。<bookmark mark='d'/>未经直接检验，问题在于它能否被检验。",
    "What the four have in common. <bookmark mark='a'/> Principles that predicted measured quan":
        "这四条有什么共同点。<bookmark mark='a'/>预测了可测量的量的原理站住了：高效编码及其偏差。<bookmark mark='b'/>主张越大，检验越弱。误差神经元存在争议，自由能原理未经检验。<bookmark mark='c'/>每个原理都要通过输入经过测量的模型来证明自己的价值。<bookmark mark='d'/>所以这就是这一部分问题的答案。还没有一个原理能解释心智，但有几个原理能解释知觉的很大一部分。",
    'Chapter fourteen. In practice: codecs and representations.':
        '第14章。实践中：编解码器与表征。',
    "Where does efficient coding earn money? <bookmark mark='a'/> In perceptual codecs. JPEG qu":
        "高效编码在哪里赚钱？<bookmark mark='a'/>在感知编解码器中。JPEG对精细细节粗略量化，那里人眼最不敏感；MP3丢弃被第15部分的掩蔽所隐藏的声音。<bookmark mark='b'/>在神经形态传感器中：事件相机只报告每个像素的变化，这是硅片中的预测编码。<bookmark mark='c'/>在表征学习中：稀疏字典和自编码器，如今被用来在AI模型内部寻找可解释的特征。<bookmark mark='d'/>还有在显示和成像中，色调映射和伽马曲线把等级花在人们能看出差别的地方。",
    "Here's a worked example. <bookmark mark='a'/> A sensor has twenty output levels for local ":
        "这里是一个实例。<bookmark mark='a'/>一个传感器对Psyche图像中的局部对比度有二十个输出等级。<bookmark mark='b'/>等级均匀分布时，中间几个被频繁使用，其余的很少用到。<bookmark mark='c'/>等级设在对比度分布的分位数上时，每个等级被使用的频率大致相同。有一个是空的，因为许多图块完全平坦。这样每次读数携带四点二比特，而均匀分布时为三点七比特。<bookmark mark='d'/>按劳克林的规则，同样的硬件多得到了约百分之十四的信息。",
    'Chapter fifteen. Frontier: one principle?':
        '第15章。前沿：一个原理？',
    "What would settle it? First, what's new. <bookmark mark='a'/> Recordings across cortical l":
        "什么能解决这个问题？首先，有哪些新进展。<bookmark mark='a'/>跨皮层层次和区域的记录，公开共享，并为检验预测编码与适应而设计。<bookmark mark='b'/>关于工作记忆以及被遗忘内容的率失真解释。<bookmark mark='c'/>在图像上训练的深度网络能预测视觉皮层的反应，而哪种目标让它们像大脑，是一个开放的检验。<bookmark mark='d'/>奥尔斯豪森和菲尔德的方法也被重新启用，来解读语言模型内部的特征。",
    "And the open problems. <bookmark mark='a'/> A normative account of why working memory and ":
        "还有那些悬而未决的问题。<bookmark mark='a'/>一个关于工作记忆和注意为什么有这样的限制的规范性解释。<bookmark mark='b'/>皮层实际使用的是哪种学习规则。<bookmark mark='c'/>是否有任何统一理论作出了专门理论没有作出的冒险预测。<bookmark mark='d'/>以及大脑在优化什么，如果它在优化什么的话，在每种感官的编码之外。",
    "First, your four numbers. <bookmark mark='a'/> After lines tilted twenty degrees clockwise":
        "先看你的四个数字。<bookmark mark='a'/>看过顺时针倾斜二十度的线条之后，一条竖直的线看起来是逆时针倾斜的，在Psyche中约四度，在人身上是几度。接近竖直的线被推离竖直，约二点五度。最常见的对比度，接近零的那些，得到最多的等级。而当每个样本都要花时间时，最好的样本数是一个。<bookmark mark='b'/>每个答案都来自一个在有限资源下尽力而为的编码。",
    "Part fifty-eight in twelve lines. <bookmark mark='a'/> Sparse codes for images grow edge d":
        "第五十八部分，十二句话。<bookmark mark='a'/>图像的稀疏编码长出了边缘检测器。高效编码与世界的统计规律相匹配，正如劳克林的苍蝇所示。白化推导出中心-周边细胞。适应重新对准编码，后效是代价。高效编码让偏差成为排斥性的。率失真理论推导出泛化梯度。归一化是一个出现在许多地方的方程。预测编码向上发送误差、向下发送预测，存在争议。自由能是一个定理和一个框架，作为原理未经检验。当先验经过测量时，贝叶斯模型能够预测。当思考有代价时，启发式可以是理性的。一个原理要看它冒了什么风险来评判。",
    "Where this comes back. <bookmark mark='a'/> Priors and precision in psychiatry are Part 59":
        "这些内容会在哪里再出现。<bookmark mark='a'/>精神病学中的先验与精确度是第59部分。从情境中的例子学习的机器是第60部分。而第62部分的学位论文可以检验一个原理。",
    "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One applie":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道应用劳克林的规则。一道设计一个白化滤波器。一道计算一个归一化的反应。一道手算变分推断。一道统计样本的多数。一道问什么能构成反对自由能原理的证据。最后带星号的一道，请你把预测编码和适应区分开来。如果想试一试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README. Hyvarinen, Hurri ':
        '这一部分所依据的书籍和论文列在这里，也列在README中。许韦里宁、胡里和霍耶的书是了解自然图像统计的最佳入门；达扬和阿博特的书是理论神经科学的标准教材；帕尔、佩祖洛和弗里斯顿的书从作者的角度阐述了主动推断。',
    "The first part of the frontier is done. <bookmark mark='a'/> It asked whether one principl":
        "前沿的第一部分已经完成。<bookmark mark='a'/>它追问一个原理能否解释心智，发现有几个原理能解释知觉的很大一部分。<bookmark mark='b'/>下一部分把这些模型带进门诊：学习率、先验和精确度，作为疾病可能所在的地方。第59部分：计算精神病学。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
