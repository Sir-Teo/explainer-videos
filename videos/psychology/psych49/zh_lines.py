"""Chinese narration for psych49: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '心理学，从零搭建 · 第49部分：为大脑数据建模'

CHAPTERS = {
    'Hook': '七十个团队，一个数据集',
    'Predict': '1. 在你身上：数一数岔路，四个数字',
    'Preprocess': '2. 预处理',
    'Glm': '3. 两个层次上的线性模型',
    'Thresholds': '4. 深入阈值',
    'Decoding': '5. 模式',
    'Rsa': '6. 几何',
    'Encoding': '7. 编码模型',
    'Connect': '8. 连接性',
    'Eeg': '9. 脑电与脑磁',
    'Neurons': '10. 神经元群体',
    'Bci': '11. 读出',
    'Samples': '12. 样本量的清算',
    'Ledger': '13. 账本',
    'Practice': '14. 实践中：诊所、设备与主张',
    'Frontier': '15. 前沿：基础模型与精准映射',
    'Outro': '回顾、习题与前路',
}

ZH = {
    'In 2020, one brain-imaging dataset':
        "2020年，一个来自一百多名做赌博任务者的脑成像数据集，被交给了七十个研究团队。<bookmark mark='a'/>每个团队都拿到同样九个是或否的问题。这个脑区对收益有反应吗？对损失呢？<bookmark mark='b'/>没有两个团队选择了相同的分析流程。<bookmark mark='c'/>对其中几个问题，有的团队说是，有的说否，用的是同样的数据。<bookmark mark='d'/>差异来自分析，而不是来自大脑。",
    'Psyche can do the same where the truth is known.':
        "Psyche可以在已知真相的地方做同样的事。<bookmark mark='a'/>一个合成大脑，三十个人，五个脑区，植入的效应从无到大。<bookmark mark='b'/>七十二条说得过去的流程：三种平滑程度、六种阈值、两种排除规则，以及加或不加一个协变量。每一列是一条流程，每一行是一个问题，金色表示是。<bookmark mark='c'/>在没有植入任何东西的地方，每条流程都说否。对最大的效应，大约四分之三说是。在两者之间，流程意见分裂。<bookmark mark='d'/>七十二条流程给出了四十四张不同的图。",
    'So this part asks what must be true for a brain map to be evidence.':
        "所以这一部分要问：一张脑图要成为证据，必须满足什么条件。<bookmark mark='a'/>流程：预处理、两个层次上的模型，以及阈值。<bookmark mark='b'/>模式：解码、几何和编码模型。<bookmark mark='c'/>连接、脑波和神经元群体。<bookmark mark='d'/>还有从大脑中读出信息，以及一个主张需要多少人。",
    "This is Part 49 of Psychology, Built: modelling the brain's data.":
        "这是《心理学，从零搭建》第49部分：为大脑数据建模。<bookmark mark='a'/>我们将走完分析链条，数一数它的岔路。我们将在两个层次上拟合模型，看看为什么被试必须是一个样本。我们将用置换检验团块，并控制错误发现。我们将解码模式、比较几何结构，并对照噪声上限拟合编码模型。我们将看到头动对连接性做了什么，选择时间窗口对ERP做了什么，以及一群神经元如何编码一个动作。我们还将从大脑中读出信息，并问一个大脑与行为的主张需要多少人。",
    'Chapter one. On you: count the forks, and four numbers.': "第1章。在你身上：数一数岔路，四个数字。",
    'First, count the forks yourself.':
        "首先，自己数一数岔路。<bookmark mark='a'/>这里是分析一次脑扫描时十个普通的选择，每个都有两到四个说得过去的选项：层间时间校正、头动校正、头动回归量、剔除坏帧、模板、平滑、反应模型、滤波、阈值和软件。<bookmark mark='b'/>把它们乘起来。<bookmark mark='c'/>六千九百一十二条流程。2012年，约书亚·卡普在一个数据集上运行了数千条这样的流程，得到的图在效应出现的位置、甚至是否出现上都各不相同。在课程网站上，你可以自己做每一个选择，看着图如何变化。",
    'Now four numbers.':
        "现在写下四个数字。<bookmark mark='a'/>第一：在一个数据集上运行七十二条说得过去的流程。会得到多少张不同的图？<bookmark mark='b'/>第二：纯噪声，一千个体素。用全部数据挑出最好的五十个体素，再对解码器做交叉验证。它报告的准确率是多少？<bookmark mark='c'/>第三：真实的大脑与行为相关为零点一，用二十五个人来研究。在显著的结果中，报告的平均相关是多少？<bookmark mark='d'/>第四：要对零点一的相关有百分之八十的功效，需要多少人？在这里暂停，把它们写下来。",
    'Chapter two. Preprocessing.': "第2章。预处理。",
    'Before any statistics, four steps.':
        "在任何统计之前，有四个步骤。<bookmark mark='a'/>层间时间校正。一个体积是一层一层采集的，要花一两秒，所以每一层的时间序列都要移到一个共同的时间。<bookmark mark='b'/>头动校正。每个体积都与第一个对齐，头动的估计值要保留下来，因为对齐无法消除头动造成的一切。<bookmark mark='c'/>配准。每个大脑都被映射到一个模板上，使一个体素在每个人身上指的是同一个位置。<bookmark mark='d'/>还有平滑：几毫米宽的模糊，它降低噪声、帮助不同的人对齐，代价是图更粗糙。每一步都有选项，每个选项都是一条岔路。",
    'Motion matters most where people differ.':
        "在人与人不同的地方，头动最要紧。<bookmark mark='a'/>Psyche造出八十个大脑完全相同的人。其中一半头动更多，表现为短暂的抽动。<bookmark mark='b'/>一次抽动会同时改变邻近脑区的信号，所以在头动多的人身上，相近的脑区对看起来连接更强，相距远的则稍弱。<bookmark mark='c'/>任何头动更多的群体，比如儿童、患者或老年人，都会显示出一个其实只是头动的“发现”。<bookmark mark='d'/>去掉有头动的扫描，差异就消失了。2012年，乔纳森·鲍尔及其同事在真实数据中发现的正是这种模式，一些已发表的连接性差异不得不重新审视。",
    'How wide should the blur be?':
        "模糊应该多宽？<bookmark mark='a'/>把同样的七十二条流程按平滑程度分开。植入的脑区是八个体素宽的圆盘，模糊也以体素为单位。<bookmark mark='b'/>在这里，不平滑最常找到中等大小的效应。<bookmark mark='c'/>比脑区更宽的模糊会把它的信号散到周围安静的组织里，连最大的效应，在模糊最宽的流程中也只有不到三分之一找到了它。<bookmark mark='d'/>合适的核取决于你要找的东西有多大。这就是信号处理中的匹配滤波规则。",
    'Chapter three. The linear model, at two levels.': "第3章。两个层次上的线性模型。",
    "The model has two levels, like Part 47's.":
        "这个模型有两个层次，就像第47部分的那样。<bookmark mark='a'/>第8部分拟合了第一层：每个体素的时间序列，对照与血流动力学反应卷积后的任务。<bookmark mark='b'/>然后每个人在每个体素上给出一个对比，比如面孔减房子。<bookmark mark='c'/>第二层把人当作一个样本。检验的误差，是这个对比在人与人之间变化多少。<bookmark mark='d'/>这就是第47部分的多层模型，只是用体素代替了试次。",
    "Here it is on Psyche's brain.":
        "这是它在Psyche大脑上的样子。<bookmark mark='a'/>左边是植入的东西：五个圆盘，效应从无到大。中间是一个人的图，主要是这个人自己的特点和噪声。<bookmark mark='b'/>右边是三十个人的群体t图。大的效应清楚地显现，中等的隐约可见，最小的完全看不到。三十个人对某些问题够了，对另一些问题不够，这就是流程在那些地方分裂的原因。",
    'Why must the second level use the spread across people?':
        "为什么第二层必须使用人与人之间的离散？<bookmark mark='a'/>取二十个人，完全没有群体效应。但每个人真实的效应不同，而且每个人的效应都带着一些测量误差。<bookmark mark='b'/>固定效应检验只使用测量误差，好像扫描就是样本。百分之十四的零假设体素在千分之一的水平上通过。<bookmark mark='c'/>随机效应检验使用人与人之间的离散，得到千分之一，正如承诺的那样。<bookmark mark='d'/>固定效应描述的是这二十个人。只有随机效应能代表他们所来自的总体。早期的脑成像研究常常使用固定效应。",
    'Chapter four. Thresholds at depth.': "第4章。深入阈值。",
    'Part 8 met the thresholding rules.':
        "第8部分已经介绍过阈值规则。这里是其中四种，用在同一张群体图上：对的地方是金色，错的地方是红色。<bookmark mark='a'/>逐体素阈值控制的是每一次检验，而不是整张图。错误发现率控制的是被宣布的体素中错误的比例。<bookmark mark='b'/>团块规则问的是：一个斑块是否比噪声造出的斑块更大。置换则问：如果什么都没有，最大的t会是多少。同样的数据，四张图，没有一张找到了全部植入的体素。",
    'Permutation lets the data make its own null.':
        "置换让数据自己构造零分布。<bookmark mark='a'/>如果没有效应，每个人的对比图朝上和朝下的可能性一样。<bookmark mark='b'/>所以随机翻转一部分人的符号，重新计算整张t图。<bookmark mark='c'/>记录全脑任何地方最大的t，或最大的团块。<bookmark mark='d'/>重复数千次，这些最大值的第九十五百分位数就是阈值。不需要假设噪声在空间上如何相关。大脑自己的噪声定下了门槛。",
    'Now the failure that shook the field.':
        "现在是那次震动整个领域的失败。<bookmark mark='a'/>Psyche造出两百项纯噪声的群体研究，它们的空间相关有一条长尾，就像真实的噪声那样。<bookmark mark='b'/>用高斯噪声校准团块大小，并在百分之一的水平上形成团块，大约每八项研究就有一项出现团块，而承诺的是二十分之一。<bookmark mark='c'/>在千分之一的水平上，它接近承诺，而置换在两种情况下都保持在百分之五左右。<bookmark mark='d'/>2016年，安德斯·埃克伦德、托马斯·尼科尔斯和汉斯·克努特松用常见软件对真实的静息态数据做了零假设分析，在宽松阈值下发现了大得多的超出。这记在账本里。",
    'And the threshold is a fork.':
        "阈值也是一条岔路。<bookmark mark='a'/>这里是按阈值规则分开、对五个问题说是的流程所占的比例。<bookmark mark='b'/>对空的脑区和最小的效应，每条规则都同意：否。<bookmark mark='c'/>对中等的效应，单单是规则就能改变答案：一个从没有流程到三分之一的流程，另一个从五分之二到三分之二。<bookmark mark='d'/>阈值是关于冒哪种错误风险的决定。在数据之前选定它，并说明选了哪一个。",
    'Chapter five. Patterns.': "第5章。模式。",
    'Mass-univariate maps test each voxel alone.':
        "大规模单变量图逐个检验体素。模式问的是许多体素合起来说了什么。<bookmark mark='a'/>2001年，詹姆斯·哈克斯比及其同事给人们看面孔、房子、椅子、鞋子以及另外四类物体。<bookmark mark='b'/>他们把每个人的数据分成两半，问一个类别在一半数据中的模式，是否与另一半中同一类别的模式比其他类别更匹配。<bookmark mark='c'/>是的，遍及腹侧颞叶皮层，即使去掉选择性最强的体素也依然如此。<bookmark mark='d'/>信息是分散的，是一种模式，而不仅仅是一个斑块。<bookmark mark='e'/>现代解码器在一些试次上训练分类器，在另一些试次上测试。这就是交叉验证，麻烦也从这里开始。",
    "Here's how a decoder can read noise.":
        "这就是解码器读出噪声的方式。<bookmark mark='a'/>两个类别，每类四十个试次，一千个体素，一个简单的解码器，用五折交叉验证检验。<bookmark mark='b'/>在纯噪声上，用全部体素，它的得分大约是百分之五十：机会水平。<bookmark mark='c'/>现在用全部试次挑出两个类别之间差异最大的五十个体素，然后才做交叉验证。百分之九十四，凭空而来。测试试次帮助挑选了体素。<bookmark mark='d'/>只在每个训练折内部挑选，结果就回到机会水平。如果有一个真实但微弱的信号，诚实的解码器大约找到三分之二。任何看到测试数据的步骤，无论是挑选、缩放还是调参，都必须放在循环之内。",
    'So what does decoding show?':
        "那么解码说明了什么？<bookmark mark='a'/>说明这个信息存在于该脑区的活动中，并且是以线性读出可以使用的形式存在的；还说明它能推广多远：跨运行、跨人，或从看到推广到想象。<bookmark mark='b'/>它不能说明大脑使用了这个信息。像眼动或反应时这样的混杂因素也可能携带标签。它不能说明这个脑区计算了它，因为信息可能是从别处继承来的。它也不能说明表征是什么。那是下一章的问题。",
    'Chapter six. Geometry.': "第6章。几何。",
    'Geometry asks a different question: not where, but what shape.':
        "几何问的是另一个问题：不是在哪里，而是什么形状。<bookmark mark='a'/>2008年，尼古拉斯·克里格斯科特、玛丽克·穆尔和彼得·班德蒂尼提出了表征相似性分析。<bookmark mark='b'/>对每一对刺激，这个脑区的模式差异有多大？这些距离构成的表就是表征相异矩阵。<bookmark mark='c'/>同样的表可以从模型得到，从行为得到，比如第22部分的相似性判断，从猴子的神经元得到，或从神经网络的某一层得到。<bookmark mark='d'/>比较这些表，非常不同的测量就相遇了。不需要把任何体素与神经元对应起来。",
    'Psyche makes a region where the answer is known.':
        "Psyche造出一个答案已知的脑区。<bookmark mark='a'/>二十四个刺激，分成四类，每类六个，每类内部的大小各不相同。每张表都是二十四乘二十四，深色表示相似。<bookmark mark='b'/>这个脑区的表，十二个人的平均，显示出四个深色的块，也就是类别；每个块内部还有一个渐变，也就是大小。两张模型表说明了每种想法的预测。",
    'So how good is each model, and how good could any model be?':
        "那么每个模型有多好，任何模型又最多能有多好？<bookmark mark='a'/>类别模型与每个人的表相关大约零点六四，大小模型大约零点四五。<bookmark mark='b'/>灰色带是噪声上限：群体自己的表能多好地预测每个人，这里大约是零点九。<bookmark mark='c'/>没有模型能超过它。一个接近它的模型，解释了数据所能显示的一切。<bookmark mark='d'/>这里两个模型都没有达到，因为这个脑区两者兼有。一个同时包含类别和大小的模型会更好。",
    'Chapter seven. Encoding models.': "第7章。编码模型。",
    'Encoding models turn the arrow around.':
        "编码模型把箭头反过来。<bookmark mark='a'/>解码从大脑走向标签。编码从刺激的特征走向每个体素。<bookmark mark='b'/>特征就是一种理论：边缘和朝向、词语的意义，或神经网络的某一层。<bookmark mark='c'/>权重带着惩罚项拟合，也就是岭回归，用的是一部分刺激，模型只在它从未见过的刺激上接受评判。<bookmark mark='d'/>托马斯·纳塞拉里斯及其同事在2011年阐述了这个框架。一个模型靠预测证明自己的价值。",
    'Psyche builds a case where the true features are known.':
        "Psyche构建了一个真实特征已知的例子。<bookmark mark='a'/>三百个体素，四十个刺激特征，在三百个刺激上训练，在六十个新刺激上测试，每个测试刺激呈现两次。<bookmark mark='b'/>每个体素的噪声上限，是测试刺激的一次呈现能多好地预测另一次。没有模型能比数据与自身的一致程度更好。<bookmark mark='c'/>对有反应的体素，模型达到的相关中位数大约是零点七八，接近它们的上限。<bookmark mark='d'/>灰色的体素对任何特征都没有反应：上限很低，没有什么可预测。真实的模型远低于它们的上限，这个差距就是理论所缺的东西。",
    'Encoding models made a striking map.':
        "编码模型画出了一张引人注目的图。<bookmark mark='a'/>2016年，亚历山大·胡思及其同事在扫描仪里给少数几个人播放了数小时的故事。<bookmark mark='b'/>每个词都用它的意义来描述，表示为一串数字，每个体素都有自己的权重。<bookmark mark='c'/>这些权重用调谐于各类意义的斑块铺满了大部分皮层：人物、地点、数字等等，在两个半球都是如此。<bookmark mark='d'/>这些图来自少数几个人，每人扫描了数小时：对他们来说很精确，对其他所有人来说则是一个开放的问题。<bookmark mark='e'/>同样的方法也用来绘制第23部分的语言网络，如今的语言模型也是这样与大脑比较的。",
    'Chapter eight. Connectivity.': "第8章。连接性。",
    'Some of the most reproducible findings come from people doing nothing.':
        "一些最可重复的发现，来自什么都不做的人。<bookmark mark='a'/>2001年，马库斯·赖希勒及其同事注意到，有些脑区的活动在几乎任何目标导向的任务中都会下降，其中包括内侧前额叶和后扣带皮层。<bookmark mark='b'/>他们称之为大脑功能的默认模式。<bookmark mark='c'/>2003年，迈克尔·格雷修斯及其同事发现，这些脑区缓慢的波动在静息时是相关的，完全不需要任务。<bookmark mark='d'/>数千次静息扫描之后，皮层可以可重复地分成少数几个大网络，默认网络就是其中之一。<bookmark mark='e'/>它做什么，是记忆、想象，还是思考自己和他人，仍有争论。",
    'Connectivity has its own forks.':
        "连接性也有自己的岔路。<bookmark mark='a'/>Psyche造出两个网络，各有自己的信号，再加上每个脑区共享的一个全局信号。没有任何东西与任何东西负相关。<bookmark mark='b'/>原始数据中，网络内的脑区相关大约零点四七，网络之间大约零点一四。<bookmark mark='c'/>现在回归掉大脑的平均信号，这是一个常见的清理步骤。网络之间的相关变成了大约负零点二七。<bookmark mark='d'/>去掉平均值会迫使相关的平均接近零，所以有些相关必然变成负的。凯文·墨菲及其同事在2009年表明了这一点，于是默认网络是否与注意网络负相关，就成了取决于这一个选择的问题。",
    'So what can a correlation between two regions mean?':
        "那么两个脑区之间的相关能意味着什么？<bookmark mark='a'/>直接的连接：有可能，但不是必需的。<bookmark mark='b'/>共同的输入：两个脑区都受第三个脑区、任务、呼吸或心跳的驱动。<bookmark mark='c'/>共享的伪影：头动、全局信号或扫描仪。<bookmark mark='d'/>还有方向：相关没有方向，而在缓慢的功能磁共振信号上用滞后方法判断方向是不可靠的。连接性图是一张共同波动的图。因果主张需要第8部分的干预。",
    'Chapter nine. EEG and MEG.': "第9章。脑电与脑磁。",
    'EEG and MEG trade space for time.':
        "脑电和脑磁用空间换时间。<bookmark mark='a'/>ERP把许多锁定在一个事件上的试次平均起来。噪声随次数的平方根下降，正如第8部分所示，一个成分用它在某个时间窗口内的幅度或潜伏期来测量。<bookmark mark='b'/>时频分析给出每个频率上随时间变化的功率。阿尔法波，大约每秒十次，在注意力投入时下降。<bookmark mark='c'/>源估计从头皮电压反推回源。这是一个不适定问题，正如第8部分的沉默源所示，所以要由一个先验在众多答案中选出一个。<bookmark mark='d'/>脑磁记录同样这些电流的磁场，受颅骨的模糊更少。每一种方法都有自己的岔路，最常见的就是窗口。",
    "Here's the most common fork in ERP research.":
        "这是ERP研究中最常见的岔路。<bookmark mark='a'/>二十四个人，两个完全没有差异的条件，两千项模拟研究。<bookmark mark='b'/>在一个事先确定的窗口上检验，百分之五是假阳性，正如承诺的那样。<bookmark mark='c'/>现在看总平均的差异，把窗口放在它的峰值上，再在那里检验。百分之四十五。这是第8部分的循环分析，发生在时间上。<bookmark mark='d'/>从两个条件的平均中选择窗口，它对两者的差异一无所知，结果就回到百分之五。窗口要从以往的研究、从独立的定位任务，或从合并的平均中选择。",
    'Chapter ten. Populations of neurons.': "第10章。神经元群体。",
    'Below the voxel are the neurons.':
        "体素之下是神经元。<bookmark mark='a'/>1982年，阿波斯托洛斯·乔治波洛斯及其同事发现，运动皮层的神经元对手臂运动的方向有宽泛的调谐。每个神经元对一个方向放电最多，对其他方向较少。<bookmark mark='b'/>让每个神经元为自己偏好的方向投票，按它放电的多少加权，所有票的总和就指向手臂运动的方向。<bookmark mark='c'/>用Psyche的有噪声的神经元，四个细胞平均偏差四十多度，两百五十六个细胞大约六度。<bookmark mark='d'/>没有哪个单独的细胞是精确的。群体是精确的。",
    'Populations also have shapes.':
        "群体也有形状。<bookmark mark='a'/>一百个神经元，在缓慢、游移的伸手动作中记录：每个时刻一百个数字。<bookmark mark='b'/>主成分显示，两个维度就包含了百分之九十以上的方差。其余的是噪声。<bookmark mark='c'/>画在这两个维度上，活动位于一个环上，也就是运动的方向。这叫作神经流形。<bookmark mark='d'/>在真实的记录中，流形也是低维的，如今运动皮层的模型试图解释的，正是它们的动力学，而不是单个细胞。",
    'Chapter eleven. Reading out.': "第11章。读出。",
    'Decoding becomes a device when it runs live.':
        "当解码实时运行时，它就变成了一个设备。<bookmark mark='a'/>脑机接口进行记录、解码和行动，使用者看到结果并加以适应。<bookmark mark='b'/>用头皮脑电，拼写器闪烁字母，检测大脑对被注意的那个字母的反应：很慢，但不需要手术。<bookmark mark='c'/>用植入运动皮层的电极阵列，瘫痪的人通过意图运动来移动光标和机械臂。<bookmark mark='d'/>最近的研究从一位再也不能说话的人的皮层中解码尝试说出的话，转换为文字，并借助语言模型。<bookmark mark='e'/>每一步都是群体向量思想的成长：许多有噪声的通道，一个意图中的动作。",
    'How good is a decoder? Engineers count bits.':
        "一个解码器有多好？工程师计算比特。<bookmark mark='a'/>乔纳森·沃尔波的公式给出在N个目标中做一次选择所包含的信息，选择正确的概率为P。再除以每次选择的时间。<bookmark mark='b'/>两个目标，正确率百分之九十，每次四秒：每分钟大约八比特。<bookmark mark='c'/>四个目标，正确率百分之八十，每次三秒：大约十九比特。<bookmark mark='d'/>二十六个字母，正确率百分之九十五，每次一秒半：大约一百六十七比特。打字是几百比特。<bookmark mark='e'/>接近机会水平的准确率几乎毫无价值。曲线在顶端很陡，所以最后几个百分点最重要。",
    'So what can be read out?':
        "那么能读出什么？<bookmark mark='a'/>意图中的动作，包括说话的动作。一个人在系统提供的选项中注意的是哪一个。还有所看到或想象之物的粗略类别，用在这个人身上训练、并在其配合下得到的模型。<bookmark mark='b'/>读不出不请自来的、陌生人的随意思想。用在别人身上训练的模型，没有长时间的校准，读不出多少东西。也读不出一个人拒绝提供的东西：到目前为止，一个抗拒的参与者能挫败这些解码器。超出这些的主张，值得做第十四章的审查。",
    'Chapter twelve. The sample-size reckoning.': "第12章。样本量的清算。",
    'Now the question that reorganized the field.':
        "现在是那个重组了整个领域的问题。<bookmark mark='a'/>取一个大脑测量与一种行为之间零点一的真实相关。这大约就是大多数全脑关联最终的大小。<bookmark mark='b'/>用二十五个人，一项研究可能得到从负零点三到将近零点五的任何值。<bookmark mark='c'/>用四千人，它落在真相附近。<bookmark mark='d'/>2022年，斯科特·马雷克及其同事考察了多达数万人的样本。全脑关联大多就是这么小，需要数千人才能估计它们。",
    "And here's what gets reported.":
        "再看看什么会被报告出来。<bookmark mark='a'/>用二十五个人，大约百分之八的研究显著，而这些研究报告的平均相关接近零点四七：将近真相的五倍。<bookmark mark='b'/>一个显著的结果，在同样大小的新样本中，大约只有百分之六的时候能重复。<bookmark mark='c'/>对零点一的相关达到百分之八十的功效，需要大约七百八十人。<bookmark mark='d'/>小型研究的文献，是一部赢家的诅咒的文献：第4部分的算术，发生在大脑里。",
    'Small samples are half the problem.':
        "小样本是问题的一半。另一半是尺子。<bookmark mark='a'/>斯皮尔曼的衰减，来自第3部分：两个测量的信度共同限制了相关。<bookmark mark='b'/>2020年，马克斯韦尔·埃利奥特及其同事发现，常见任务态功能磁共振测量的重测信度平均大约是零点四。<bookmark mark='c'/>所以，零点二的真实相关，大脑测量的信度为零点四，行为的信度为零点八，观测到的大约只有零点一一。<bookmark mark='d'/>补救办法是：每人扫描更长时间，选择信度高的测量，以及数千人的样本。",
    'One more test of the methods themselves.':
        "再对方法本身做一次检验。<bookmark mark='a'/>2017年，埃里克·乔纳斯和康拉德·科尔丁拿来一块工作原理完全已知的芯片，运行着三款经典电子游戏，并像神经科学家研究大脑那样研究它。<bookmark mark='b'/>损毁：去掉一些晶体管会让一款游戏停止，而其他游戏不受影响，好像那些晶体管是专门负责那款游戏的。<bookmark mark='c'/>调谐曲线、部件之间的相关和降维，都得出了看似合理的发现。<bookmark mark='d'/>没有一种揭示了芯片实际上是如何计算的。<bookmark mark='e'/>教训是：方法必须在答案已知的系统上检验。这正是这一部分的合成大脑的用途。",
    'Chapter thirteen. The Ledger.': "第13章。账本。",
    'Five new rows.':
        "五条新记录。第一条：对同一份大脑数据使用不同的、说得过去的流程，可能得出不同的结论。<bookmark mark='a'/>原始研究：约书亚·卡普，2012年。<bookmark mark='b'/>记录：2020年的七十个团队，以及神经科学之外的多分析者研究。<bookmark mark='c'/>差异在于分析，所以要报告岔路并注册流程。<bookmark mark='d'/>已重复。",
    'The second: the default mode network.':
        "第二条：默认模式网络。<bookmark mark='a'/>原始研究：赖希勒及其同事，2001年。<bookmark mark='b'/>记录：静息时相关，并在数千次扫描中再次发现。<bookmark mark='c'/>它的功能仍有争论，它的负相关取决于分析方法。<bookmark mark='d'/>已重复。",
    'The third: brain-behaviour correlations from a few dozen people':
        "第三条：来自几十个人的大脑与行为相关既大又可重复。<bookmark mark='a'/>原始研究：卡奈和里斯在2011年综述的那些研究。<bookmark mark='b'/>记录：一项对十七个这类相关的预注册重复，几乎没有找到任何证据；而数千人的样本发现真实的相关很小。<bookmark mark='c'/>这些关联是真实的，但很小，正如第十二章所计算的。<bookmark mark='d'/>失败。",
    'The fourth: cluster inference at a lenient threshold':
        "第四条：宽松阈值下的团块推断能把假阳性控制在百分之五。<bookmark mark='a'/>原始研究：弗里斯顿及其同事的随机场理论，1994年。<bookmark mark='b'/>记录：吴、克里希南和韦杰的警告，以及埃克伦德、尼科尔斯和克努特松对真实数据所做的零假设分析。<bookmark mark='c'/>更严格的初始阈值或置换检验可以解决它。<bookmark mark='d'/>失败。",
    'And the fifth: object categories can be decoded':
        "第五条：物体类别可以从腹侧颞叶皮层的模式中解码出来。<bookmark mark='a'/>原始研究：哈克斯比及其同事，2001年。<bookmark mark='b'/>记录：猴子和人类身上同样的结构，以及跨人的解码。<bookmark mark='c'/>可解码意味着信息存在，不一定意味着被使用。<bookmark mark='d'/>已重复。",
    'What the five have in common.':
        "这五条的共同点。<bookmark mark='a'/>三条已重复：一个在每个大样本中都能找到的网络，一个在每个实验室都能找到的模式，以及分析本身的变异性。<bookmark mark='b'/>两条失败了，而且都是方法的失败：样本太小，以及一个不成立的近似。<bookmark mark='c'/>两者都是通过在已知真相的地方检验方法，或用大到足以知道真相的数据，才被发现的。<bookmark mark='d'/>所以，这就是这一部分问题的答案。一张脑图成为证据，需要流程事先确定，阈值与噪声相符，样本与效应的大小相符。",
    'Chapter fourteen. In practice: clinics, devices and claims.': "第14章。实践中：诊所、设备与主张。",
    'Where do these analyses run?':
        "这些分析在哪里运行？<bookmark mark='a'/>在诊所里：脑部手术前绘制语言和运动区域，一次一位患者，使用经过验证并固定的流程，在那里漏报是有代价的。<bookmark mark='b'/>在设备工程中：脑机接口像医疗设备一样接受检验，看准确率、比特率、几个月里的稳定性，以及使用者自己的目标。<bookmark mark='c'/>在消费级神经技术中：声称能测量专注或平静的头带，来自几个干电极，其信号主要被肌肉和眼动所主导。<bookmark mark='d'/>在数据科学中：数千人的大型共享数据集，有固定的流程和留出的样本，如今是大脑与行为主张的标准。",
    "And here's a checklist for auditing any claim about the brain.":
        "这里有一份审查任何关于大脑的主张的清单。<bookmark mark='a'/>流程是在数据之前确定的吗，试了多少条路径？<bookmark mark='b'/>检验是在人的层次上进行的吗，阈值与噪声相符吗？<bookmark mark='c'/>对解码器：每个选择都是在交叉验证循环内部做的吗，会不会有混杂因素携带了标签？<bookmark mark='d'/>对大脑与行为的主张：多少人，测量的信度如何，是否在留出的样本中检验过？<bookmark mark='e'/>对设备：与机会水平相比的准确率，每分钟多少比特，在谁身上，持续多久？<bookmark mark='f'/>这个主张是关于方法能显示什么，还是关于一个人在想什么？",
    'Chapter fifteen. Frontier: foundation models and precision mapping.': "第15章。前沿：基础模型与精准映射。",
    'Three frontiers.':
        "三个前沿。<bookmark mark='a'/>大脑活动的基础模型：在来自许多人的数千小时记录上训练的网络，再适配到新的人和新的任务。它们很有前景，但仍需证明能胜过简单的基线。<bookmark mark='b'/>自然刺激：用电影和故事代替闪烁的棋盘格，为编码模型提供更丰富的数据，代价是失去控制。<bookmark mark='c'/>还有精准映射：每人扫描许多小时，得到的个人图在网络所在的位置上与群体平均不同。这是第47部分的教训，发生在大脑里。",
    'Open questions.':
        "开放的问题。<bookmark mark='a'/>哪些分析选择最重要，一个领域能否在不冻结方法的前提下就默认设置达成一致？<bookmark mark='b'/>对于一个心灵理论来说，正确的对象是群体图，还是一个人自己的图？<bookmark mark='c'/>一个大脑测量要预测一个人的行为到可以使用的程度，需要什么？<bookmark mark='d'/>当一个网络预测了大脑活动时，解释了什么？",
    'First, your four numbers.':
        "首先，你的四个数字。<bookmark mark='a'/>七十二条流程给出了四十四张不同的图。一个用全部数据挑选体素的解码器，以百分之九十四的准确率读出了纯噪声。用二十五个人，显著的相关平均大约零点四七，而真相是零点一。对这个真相达到百分之八十的功效，需要大约七百八十人。<bookmark mark='b'/>一张脑图是由一条流程做出的测量。固定流程，让阈值与噪声相符，让样本与效应相符。",
    'Part forty-nine in twelve lines.':
        "用十二行总结第49部分。<bookmark mark='a'/>一个数据集，许多流程，不同的答案。预处理的选择是岔路，头动会制造连接。第二层把人当作样本。宽松的团块会失败，置换让噪声来定门槛。阈值是关于错误的决定。只要有任何选择看到了测试数据，解码器就会泄漏。几何比较距离表，最多到噪声上限。编码模型由预测来评判。全局信号回归会制造负相关。从答案中选出的窗口会带来假阳性。群体能编码单个细胞编码不了的东西。大脑与行为的主张需要数千人和可靠的测量。",
    "Kant's wager.":
        "康德的赌注。<bookmark mark='a'/>第一个反驳遇到了群体模型、置换检验、解码器和编码模型，全都在一个真相已知的大脑上运行。绿色。<bookmark mark='b'/>第二个反驳遇到了对大脑的设计实验，以及按解码出的意图行动的设备。绿色。<bookmark mark='c'/>第三个，关于内省。大脑数据不是报告，尽管一个脑区表征什么，仍然要通过一个模型来解读。绿色。",
    'Where this comes back.':
        "这些内容会在哪里再次出现。<bookmark mark='a'/>跨研究的证据分量就在下一部分，第50部分。预测的大脑是第58部分。计算精神病学及其对生物标志物的寻找是第59部分。大脑与机器的比较是第60部分。",
    "Seven problems, with full solutions in this part's README.":
        "七道习题，完整的解答在这一部分的README里。<bookmark mark='a'/>一道数流程。一道计算群体t值。一道求邦费罗尼阈值。一道计算每分钟比特数。一道衰减一个相关。一道解释一次泄漏。最后一道带星号，请你规划一项值得被相信的大脑与行为研究。如果你想试试，就在这里暂停。",
    'The books and papers behind this part are listed here and in the README.':
        "这一部分背后的书和论文列在这里，也列在README里。波尔德拉克、芒福德和尼科尔斯讲授功能磁共振的分析流程；史蒂文·勒克的书是ERP的标准著作；而那篇七十个团队的论文，是支持注册分析的最好的单篇论证。",
    'Six parts of the graduate toolkit done.':
        "研究生工具箱完成了六个部分。<bookmark mark='a'/>这一部分跟随大脑的数据，从扫描仪一直走到主张。<bookmark mark='b'/>接下来是整个文献。一个监管机构掌握着七十四项抗抑郁药试验的注册结果，而期刊讲的是另一个故事。一个文献说了什么，它说的话能被信任吗？第50部分：证据的分量。",
}

PHRASES = {f"{n} percent": f"{n}%" for n in range(101)}
