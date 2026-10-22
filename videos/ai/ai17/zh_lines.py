"""Chinese narration for ai17: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第17部分：硅'

CHAPTERS = {
    'Hook': '八千万倍的算术',
    'PowerWall': '1. 功耗墙',
    'Throughput': '2. 从像素到GPU通用计算',
    'SIMT': '3. 线程束、分支发散与延迟',
    'AlexNet': '4. AlexNet：那一刻',
    'Matmul': '5. 矩阵乘法就是工作负载',
    'Hierarchy': '6. 存储层次',
    'Roofline': '7. 屋顶线',
    'Systolic': '8. 张量核心与脉动阵列',
    'Formats': '9. 硬件里的数字格式',
    'Interconnect': '10. 互连与集合通信',
    'Kernel': '11. 写一个内核',
    'Trends': '12. 算力、美元与瓦特',
    'Accelerators': '13. GPU之外',
    'Frontier': '14. 2026年底的前沿',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'f"In 2012, the neural network that started the deep learning boom, AlexNet':
        "2012年，掀起深度学习热潮的那个神经网络AlexNet，是在两块为电子游戏设计的显卡上，训练了五到六天。<bookmark mark='a'/>十二年后，Meta在16384块英伟达H100 GPU上训练了Llama 3.1，一个4050亿参数的语言模型：它们都在这里，一块GPU一个小方格。<bookmark mark='b'/>按Epoch AI的统计，这次训练用掉的浮点运算，大约是AlexNet的{ratio / 1000000.0:.0f}00万倍。其中几乎全部，都是矩阵的乘法和加法。",

    'f"The computer making this video reports its processor as {machine_spoken()}.':
        "制作这个视频的计算机，报告它的处理器是{machine_spoken()}。<bookmark mark='a'/>我们测了它的一个核心做矩阵乘法有多快：最快大约每秒{r1 / 1000000000.0:.0f}0亿次运算。<bookmark mark='b'/>照这个速度，AlexNet的训练要花大约{d_alex:.0f}天。<bookmark mark='c'/>Llama 3.1的训练，要花大约{y_llama / 1000000.0:.0f}00万年。",

    'That gap is the subject of this part.':
        "这道鸿沟，就是本部分的主题。为什么人工智能跑在图形处理器上？为它专门造的芯片，又会是什么样子？<bookmark mark='a'/>我们会沿着硬件的历史走下去：从时钟频率不再上涨的那一刻，经过GPU、CUDA和AlexNet，到矩阵乘法的算术，以及给它的速度设上限的屋顶线；再到谷歌的TPU、只有四位宽的数字，以及一整间屋子那么大、却像一台计算机一样工作的机器。<bookmark mark='b'/>只要能做到，我们就在制作这个视频的这台计算机上亲手测量。",

    'This is Part 17 of AI, Built, in the third act':
        "这是《人工智能，从零搭建》的第17部分，属于第三幕：Transformer时代。<bookmark mark='a'/>本部分要讲：时钟为什么不再变快；图形芯片怎样变成了人工智能的发动机；为什么矩阵乘法就是工作负载，又是什么限制了它的速度，从存储层次一直讲到屋顶线；脉动阵列，以及硬件里的数字格式；芯片之间怎样通信；快速的内核是怎样写出来的；以及今天的硬件走到了哪一步。",

    # ------------------------------------------------------------------ PowerWall
    'Chapter one. The power wall.':
        '第1章。功耗墙。',

    'f"In 1965 Gordon Moore, then at Fairchild Semiconductor':
        "1965年，当时在仙童半导体的戈登·摩尔注意到，一块芯片上的元件数一直在逐年翻倍，他猜这会继续下去。<bookmark mark='a'/>这是五十年来的微处理器，画在对数刻度上：从1971年英特尔的4004，大约{round(first, -2):,.0f}个晶体管，到拥有{last / 1000000000.0:.0f}0亿个晶体管的芯片。<bookmark mark='b'/>对数刻度上的一条直线，就是指数增长。拟合出来是每{dbl:.1f}年翻一倍，正是摩尔在1975年修正后的速度。在三十年里，每一次翻倍也让每个程序免费变快。",

    'Why did shrinking make computers faster?':
        "为什么把晶体管做小，计算机就变快？答案在1974年来自IBM的罗伯特·登纳德和同事，他也是单晶体管存储单元的发明者。<bookmark mark='a'/>把晶体管的每个尺寸都缩小κ倍，电压也降低同样的倍数。<bookmark mark='b'/>它要充电的电容降为κ分之一，<bookmark mark='c'/>开关速度快κ倍。<bookmark mark='d'/>开关一次的功耗是C乘V的平方乘f，降为κ平方分之一。<bookmark mark='e'/>但同样的面积现在能放下κ平方倍的晶体管。于是每平方毫米的功耗保持不变，而时钟更快、数量更多。这就是登纳德缩放，三十年里，它就是那顿免费的午餐。",

    'Then, in the early two thousands, the voltage stopped falling.':
        "后来，到了2000年代初，电压降不下去了。<bookmark mark='a'/>晶体管是个开关，电压低于某个值，它就关不干净：在室温下，电压每降60毫伏，电流最多只能降到十分之一，所以电压越低，漏电越多。<bookmark mark='b'/>电压卡住了，每个更小的晶体管，用的功率就和原来一样多，<bookmark mark='c'/>而在同样面积里塞进κ平方倍的晶体管，发热也就乘上了κ平方。<bookmark mark='d'/>2004年，英特尔取消了奔腾4的后继型号，转向每块芯片两个核心。一年后，程序员赫布·萨特写道：免费的午餐结束了。",

    'f"You can see the wall in the data.':
        "这堵墙在数据里看得见。<bookmark mark='a'/>从1985年到2003年，时钟频率每{e:.1f}年翻一倍，然后停在了{f04:.1f}吉赫兹左右；{rate}。<bookmark mark='b'/>功耗一直跟着上涨，最后停在一个风扇加散热片能带走的水平，大约一百瓦。<bookmark mark='c'/>单线程性能，也就是一个程序能拿到的速度，在那之前每{se:.1f}年翻一倍；2010年以后，要{sl:.1f}年。<bookmark mark='d'/>一直在增长的，是核心的数量。晶体管还在不断增加；剩下唯一能用上它们的办法，就是并行。",

    "f'and since 2006 it has drifted down by about":
        "从2006年起，它每年还下降了大约{100 * (1 - late):.0f}%",

    "f'and since 2006 it has crept up by only":
        "从2006年起，它每年只上涨了{100 * (late - 1):.0f}%",

    'Why does parallel win?':
        "为什么并行能赢？<bookmark mark='a'/>开关功耗是C乘V的平方乘f，而要让时钟跑得更快，电压大致要成比例地提高。所以功耗随时钟频率的三次方增长。<bookmark mark='b'/>要做两倍的工作，一个核心把时钟提高一倍，功耗大约是八倍；两个核心保持原来的时钟，功耗只是两倍。<bookmark mark='c'/>代价是1967年的阿姆达尔定律：程序里不能拆开的那部分，限制了加速比，不管你加多少核心。<bookmark mark='d'/>所以，对一个能拆成几百万个相同小块的问题，最好的芯片，是成千上万条又慢又简单的通道。这样的芯片已经存在了。它是用来画电子游戏的。",

    # ------------------------------------------------------------------ Throughput
    'Chapter two. From pixels to GPGPU.':
        '第2章。从像素到GPU通用计算。',

    'Think about what a graphics card does.':
        "想想显卡是做什么的。<bookmark mark='a'/>屏幕上每个像素，都在自己的坐标上运行同一个小程序，叫着色器，而且没有哪个像素需要知道别的像素。<bookmark mark='b'/>一块1080p的屏幕大约有两百万个像素，每秒六十次：每秒超过一亿次运行同一个程序，彼此完全独立。<bookmark mark='c'/>1999年，英伟达把GeForce 256作为世界上第一块GPU，也就是图形处理器来卖；2001年，它的着色器变得可以编程。这是一块为“把一件事做极多次”而造的芯片。",

    'f"A CPU and a GPU spend their transistors differently.':
        "CPU和GPU，把晶体管花在了不同的地方。<bookmark mark='a'/>CPU把它们花在让一条指令流跑得快上：大缓存，让数据离得近；分支预测器，猜程序会往哪边走；还有让指令乱序执行的机制。<bookmark mark='b'/>GPU把它们花在算术上：许多小处理器，英伟达叫它们流式多处理器，每个都是一组简单的通道。<bookmark mark='c'/>制作这个视频的计算机有{m['cores']}个核心，每个核心的向量单元是{lanes}个数宽。一块H100有132个流式多处理器，每个有128条通道：差不多一万七千条。<bookmark mark='d'/>每条通道都又慢又简单。只是数量极多。",

    'f"Simple lanes are the easy part.':
        "简单的通道是容易的部分。难的是喂饱它们，因为内存离得很远。<bookmark mark='a'/>排队论里有一条定律，是约翰·利特尔1961年提出的：系统里的东西的数量，等于它们到达的速率，乘以每个停留的时间。<bookmark mark='b'/>用在内存上，它说的是：要让内存一直忙着，已经请求、还没收到的字节数，必须等于带宽乘以延迟。<bookmark mark='c'/>研究人员测得，Hopper GPU的内存大约在{round(lat_s * 1000000000.0, -1):.0f}纳秒之外。每秒两太字节，就需要每时每刻大约有{round(inflight / 1000.0, -1):.0f}千字节在路上：成千上万个请求。<bookmark mark='d'/>这台计算机的一个核心，实测只需要大约{ours / 64:.0f}个缓存行在路上，它靠预取器来做到：预取器会猜一段长而规则的读取接下来的地址。GPU用另一种办法凑出那成千上万个请求：成千上万个线程，每个都在等自己的那次读取。",

    'Researchers noticed.':
        "研究人员注意到了。<bookmark mark='a'/>在2000年代初，他们把算术伪装成图形：把数组存成纹理，把计算写成像素着色器，再从屏幕上把答案读回来。2004年，伊恩·巴克在斯坦福做的Brook语言，让这件事变得可以忍受。<bookmark mark='b'/>同一年，吴京洙和郑基哲在显卡上跑了一个神经网络，比在CPU上快二十倍。<bookmark mark='c'/>巴克去了英伟达，和约翰·尼科尔斯一起做出了CUDA：就是C语言，外加一种一次在成千上万个线程上启动同一个函数的办法。它在2006年11月随GeForce 8800发布，2007年正式推出。<bookmark mark='d'/>到了2009年，斯坦福的拉贾特·雷纳、阿南德·马达万和吴恩达，在GPU上训练深度网络，比在CPU上快多达七十倍。下一个十年的拼图，已经摆在了桌上。",

    # ------------------------------------------------------------------ SIMT
    'Chapter three. Warps, divergence and latency.':
        '第3章。线程束、分支发散与延迟。',

    'Here is a CUDA program.':
        "这是一个CUDA程序。<bookmark mark='a'/>这个函数叫内核，它说的是一个线程要做什么：根据我的块编号和线程编号，算出哪个元素归我，然后更新这个元素。<bookmark mark='b'/>启动时，要求足够多的、每块256个线程的线程块，来覆盖整个数组：一百万个元素，大约四千个块。<bookmark mark='c'/>硬件把线程块分给流式多处理器，再把每个块切成32个线程一组的线程束。<bookmark mark='d'/>一个线程束的32个线程，在同一时刻执行同一条指令，各自处理自己的数据。英伟达把这叫作SIMT，单指令多线程：一台向量机器，你却是一次一个线程地给它编程。",

    '"Lockstep has a price.':
        "步调一致是有代价的。<bookmark mark='a'/>假设一个线程束里的线程遇到一个if，有的进去，有的不进去。<bookmark mark='b'/>线程束一次只能发一条指令，所以它先执行if分支，把其他线程屏蔽掉，<bookmark mark='c'/>再执行else分支，把第一组屏蔽掉。两条路径都要花掉整个线程束的时间。这就是分支发散。<bookmark mark='d'/>我们在四千个线程束上，模拟了一个依赖数据的分支。{verdict}",

    "f'Random data diverges in almost every warp":
        "随机数据几乎在每个线程束里都会发散，线程束只有大约{100 * mid:.0f}%的有用功。先把数据排好序，让相邻的线程意见一致，就只有处在边界上的那几个线程束会分叉。",

    'f"Now the reason for all those threads.':
        "现在说说为什么要那么多线程。从内存读一次要几百个周期；一个线程束在等的时候，调度器就去发另一个已经就绪的线程束的指令。<bookmark mark='a'/>我们模拟了一个调度器，内存在{lat}个周期之外，这是在一块Hopper GPU上测得的延迟。<bookmark mark='b'/>如果每个线程束每次读取只做四次运算，即使有十六个线程束，调度器也只有{100 * u_lo:.0f}%的时间在忙。<bookmark mark='c'/>如果每次读取做六十四次运算，{k_hi}个线程束就够了。<bookmark mark='d'/>那几条线就是利特尔定律：需要在路上的线程束数，等于延迟加上工作量，再除以工作量。H100的一个多处理器有四个调度器，能容纳六十四个线程束。超过这个数，隐藏延迟的唯一办法，就是每个字节做更多的算术，这个想法在第5章还会出现。",

    'One more rule of the road.':
        "还有一条交通规则。<bookmark mark='a'/>内存是按128字节一段来读的。当一个线程束的32个线程读32个相邻的数，硬件会把它们合成一次传输：这叫访存合并。<bookmark mark='b'/>如果它们读的是分散的地址，同样32个数要花很多次传输，取回来的每一段，大部分都被扔掉了。这和CPU缓存行的道理一样，对矩阵也很重要：要沿着行去走。",

    # ------------------------------------------------------------------ AlexNet
    'Chapter four. AlexNet: the moment.':
        '第4章。AlexNet：那一刻。',

    'By 2012 the ingredients were in place.':
        "到2012年，各样原料都备齐了。<bookmark mark='a'/>2009年，李飞飞的团队发布了ImageNet，几百万张标注好的照片；从2010年起，每年有一场比赛：模型看一张图，从一千个类别里说出它是什么，可以猜五次。<bookmark mark='b'/>2012年，多伦多杰弗里·辛顿实验室的一个网络，由亚历克斯·克里热夫斯基和伊利亚·苏茨克维搭建，<bookmark mark='c'/>在15.3%的测试图片上答错。第二名答错了26.2%。谁也没见过这么大的差距。",

    'What made it possible was two gaming graphics cards.':
        "让这件事成为可能的，是两块游戏显卡。<bookmark mark='a'/>这个网络有六千万个参数，一块3GB显存的GeForce GTX 580，训练时装不下它。于是克里热夫斯基把它一分为二：每一层的卷积核，一半放在一块卡上，一半放在另一块上。<bookmark mark='b'/>两半只在少数几层交换结果，好让两块卡之间的通信量小一些。<bookmark mark='c'/>卷积是他自己用CUDA写的，写在一个叫cuda-convnet的库里。训练花了五到六天，把120万张图片过了九十遍。",

    'f"How much arithmetic was that?':
        "那是多少算术？<bookmark mark='a'/>大约120万张图片，乘以九十遍，乘以每张图四分之三个十亿次乘加，每次乘加算两次运算，再乘以三，算上反向传播：<bookmark mark='b'/>大约{prod / 1e+17:.1f}乘以10的17次方次浮点运算；公开的估计是4.7。<bookmark mark='c'/>两块卡在五天半里能做大约{avail / 1e+18:.1f}乘以10的18次方次，所以这个网络让它们大约{100 * use:.0f}%的时间在忙。<bookmark mark='d'/>在渲染这个视频的计算机上，按我们测到的最快速度，一个核心要大约{d1:.0f}天{tail}",

    "f', and all {int(mt['threads'])} cores together about {dN:.0f}":
        "，全部{int(mt['threads'])}个核心一起要大约{dN:.0f}天：比2010年的两块显卡{faster}，前提还是每个核心只做矩阵乘法。",

    "f'. All {int(mt['threads'])} cores together should do better":
        "。全部{int(mt['threads'])}个核心一起本该更快，但我们测量时别的任务正在用它们，结果一起算也不比一个核心快。",

    'After 2012 the field moved onto GPUs.':
        "2012年以后，整个领域搬到了GPU上。<bookmark mark='a'/>2014年，英伟达发布了cuDNN，一个深度学习内核库，研究人员不用再自己写了。<bookmark mark='b'/>2016年，它围绕八块GPU造了一台服务器，DGX-1，黄仁勋亲手把第一台送到了OpenAI。<bookmark mark='c'/>2018年，达里奥·阿莫代伊和丹尼·埃尔南德斯测量了这个趋势：从AlexNet开始，最大规模训练所用的算力每3.4个月翻一倍，六年里增长了三十万倍。<bookmark mark='d'/>2020年，萨拉·胡克给这段历史起了个名字：硬件彩票。一个想法能不能成功，要看它适不适合当时的硬件；神经网络全是乘加，抽中了一张为电子游戏印的中奖彩票。",

    # ------------------------------------------------------------------ Matmul
    'Chapter five. Matrix multiply is the workload.':
        '第5章。矩阵乘法就是工作负载。',

    'f"Why are GPUs so good for neural networks in particular?':
        "为什么GPU特别适合神经网络？因为一个网络几乎所有的算术，都是同一种运算。<bookmark mark='a'/>以GPT-3为例。每处理一个词元，它的1750亿个权重，每个都参与一次乘法和一次加法：每个权重两次运算，全部在矩阵乘法里。<bookmark mark='b'/>注意力自己的乘积，也就是查询对键，再加上{100 * parts[1][0]:.1f}%。<bookmark mark='c'/>其余的一切，归一化、激活函数、softmax，即使往宽里算，也只是个零头。<bookmark mark='d'/>训练要做一次前向，再做一次代价是它两倍的反向：每个词元每个权重六次运算。6乘以1750亿参数，再乘以3000亿个词元，就得到GPT-3公开的算力，误差不到百分之一。要让人工智能更快，就让矩阵乘法更快。",

    'So let\'s count.':
        "那就来数一数。<bookmark mark='a'/>C的每个元素，是A的一行和B的一列的点积。<bookmark mark='b'/>有K项，就是K次乘法和K减1次加法：大约2K次运算。<bookmark mark='c'/>一共有M乘N个元素，所以整个乘积要2MNK次浮点运算。对于大小为n的方阵：2n的立方。尺寸翻倍，工作量变成八倍。",

    'The arithmetic is only half the cost.':
        "算术只是一半的代价。数字还得从内存里来。<bookmark mark='a'/>运算次数和搬运字节数之比，叫作算术强度。<bookmark mark='b'/>如果天真地做，每次乘加都去取它的两个数，单精度下每个四字节：八个字节做两次运算，每字节四分之一次运算。<bookmark mark='c'/>可整个乘积只需要把A和B各读一次、C写一次：3n平方个数，做2n立方次运算。算术强度像n除以6那样增长。<bookmark mark='d'/>n等于1024时，大约是每字节170次运算。每个数被用了上千次。整个游戏的关键，就是趁它就在手边，把它用上一千次，而不是去取它一千次。",

    "That's what tiling does.":
        "这就是分块要做的事。<bookmark mark='a'/>把C切成b乘b的块。要算其中一块，就沿着A的一条和B的一条走，每次各取一个b乘b的块。<bookmark mark='b'/>把这两块搬进快速存储，相乘，加到C的那一块上，然后往下走。<bookmark mark='c'/>每个搬进来的数被用了b次，所以算术强度是b除以4字节。<bookmark mark='d'/>上限在于快速存储：三个块必须放得下。快速存储越大，块越大，复用越多。<bookmark mark='e'/>1981年，洪加威和孔祥重证明，没有哪种顺序能好得多：任何计算这个乘积的方法，搬运的数据量至少是n立方除以快速存储大小的平方根这个量级。",

    "'We measured this on one core of this computer, multiplying two matrices of size 1,024 ' + how":
        "我们在这台计算机的一个核心上，把两个1024阶的矩阵相乘，测了一下{how}<bookmark mark='a'/>教科书上的三重循环：每秒{gflops(r['naive'])}千兆次运算。它沿着B的列往下走，每取一个数就要一条缓存行。<bookmark mark='b'/>同样的算术，换一下循环的顺序，让每个内层循环都沿着行走：{gflops(r['ikj'])}。<bookmark mark='c'/>分块之后：{gflops(blk[kb])}，是教科书循环的{speed_tile:.0f}倍。<bookmark mark='d'/>最好的块大小是{best_b}：{where}。{past}<bookmark mark='e'/>numpy调用的BLAS库，由专家调优，块里套块，还有手写的向量代码：{gflops(r['blas'])}，是教科书循环的{speed_blas:.0f}倍，算术一模一样。",

    'in Python, with numpy doing the innermost loop':
        '，用的是Python，最内层循环交给numpy：这台计算机没有C编译器。',

    'Past that, the tiles spill out and the speed falls.':
        '再大，块就装不下了，速度随之下降。',

    "f'three {best_b} by {best_b} tiles take {ws / 1024:.0f} kilobytes, which fits":
        "三个{best_b}乘{best_b}的块占{ws / 1024:.0f}千字节，正好放得进{l2 / 1024:.0f}千字节的二级缓存",

    "f'three {best_b} by {best_b} tiles take {ws / 1024:.0f} kilobytes'":
        "三个{best_b}乘{best_b}的块占{ws / 1024:.0f}千字节",

    # ------------------------------------------------------------------ Hierarchy
    'Chapter six. The memory hierarchy.':
        '第6章。存储层次。',

    'f"A GPU\'s memory is not one thing.':
        "GPU的内存不是一样东西。我们放大来看一块H100。<bookmark mark='a'/>芯片周围是一叠叠高带宽内存，DRAM裸片一层层摞起来：{h['mem'] / 1000000000.0:.0f}GB，每秒能读{h['bw'] / 1000000000000.0:.2f}太字节，但远在几百个周期之外。<bookmark mark='b'/>芯片本身上，有五十兆字节的二级缓存，由全部132个流式多处理器共用，距离大约是一半。<bookmark mark='c'/>每个多处理器里面：256千字节的共享内存，由程序员有意地去填，大约四十个周期远；<bookmark mark='d'/>还有寄存器，又是256千字节，紧挨着运算单元，每个周期都能读。每往下一层，就更小、更近，读起来也快得多。",

    'f"That memory is a feat of its own.':
        "那种内存本身就是一项壮举。<bookmark mark='a'/>高带宽内存把DRAM裸片一层层叠起来，用直接穿过硅片的导线连通，再把整叠内存放在GPU旁边的一块硅片上，用成千上万根短导线相连：比电路板能承载的多得多。AMD在2015年第一次把它用在显卡上。<bookmark mark='b'/>从P100开始，每块GPU的内存从{cap[0]:.0f}GB增长到Rubin的{cap[-1]:.0f}GB，带宽从每秒{bw[0]:.2f}太字节增长到{bw[-1]:.1f}：十年里大约{bw[-1] / bw[0]:.0f}倍。它是整个封装里最贵的部分，而且我们会看到，也是最稀缺的资源。",

    'On the right, the same core follows a chain of pointers in random order, so every read':
        '右边，同一个核心按随机顺序追着一串指针走，所以每次读都要等上一次读完。',

    'On the right, the same core follows a chain of pointers in random order, from Python':
        '右边，同一个核心在Python里按随机顺序追着一串指针走：这台计算机没有C编译器，所以每次读还要付出解释器的开销。',

    'f"We can see the same hierarchy on this computer':
        "在这台计算机自己的处理器上，计个时，也能看到同样的层次。<bookmark mark='a'/>左边，一个核心反复读一个数组，把它加起来；数组从四千字节增大到256兆字节。它还放得进一级缓存时，大约每秒{b1 / 1000000000.0:.0f}GB。超出以后，从二级缓存读，大约{b2 / 1000000000.0:.0f}。从主存读，大约{bd / 1000000000.0:.0f}。<bookmark mark='b'/>{chase}在一级缓存里，一次读大约{t1 * 1000000000.0:.1f}纳秒；在二级缓存里，大约{t2 * 1000000000.0:.0f}；在主存里，大约{td * 1000000000.0:.0f}。<bookmark mark='c'/>虚线是处理器报告的各级缓存大小。{tail}",

    'f"The last level is nominally {L3k / 1024:.0f} megabytes':
        "最后一级缓存名义上有{L3k / 1024:.0f}兆字节，但它由芯片上所有核心共用，在这里我们的随机读取大约到{last_mib:.0f}兆字节就离开了它。",

    'f\'The last level holds up to about its':
        "最后一级缓存差不多能用满它的{L3k / 1024:.0f}兆字节。",

    'The last level is shared by every core on the chip.':
        '最后一级缓存由芯片上所有核心共用。',

    'f"Why build it this way? Distance costs energy.':
        "为什么要这样造？因为距离要耗能。<bookmark mark='a'/>马克·霍洛维茨列出了在45纳米芯片上，每种操作的代价。两个32位整数相加：十分之一皮焦。两个浮点数相乘：3.7。<bookmark mark='b'/>从一小块片上存储读32位：大约5。<bookmark mark='c'/>从DRAM读：640，相当于大约{ratio:.0f}次乘法。算术很便宜；搬运数字才是贵的。新的芯片改变了这些数字，却没改变这个比值的教训：每个从远处取来的字节，都必须用上很多次。",

    # ------------------------------------------------------------------ Roofline
    'Chapter seven. The roofline.':
        '第7章。屋顶线。',

    'Chapters two to six give a program two ways to be slow.':
        "第2到第6章，给了一个程序两种慢下来的方式。<bookmark mark='a'/>如果它要做W次运算，机器的峰值是每秒P次，那至少要W除以P的时间。<bookmark mark='b'/>如果它要通过带宽为β的内存搬运Q个字节，那至少要Q除以β的时间。<bookmark mark='c'/>两个都快不过，所以它的速度，W除以T，至多是P和β乘以W除以Q中较小的那个。<bookmark mark='d'/>W除以Q就是算术强度I：每字节的运算次数。所以速度至多是P和β乘以I的最小值。2009年，伯克利的塞缪尔·威廉斯、安德鲁·沃特曼和大卫·帕特森把它画成了一张图，叫作屋顶线。",

    'f"Here is the roofline of one core of this computer, measured.':
        "这是这台计算机一个核心的屋顶线，是实测出来的。<bookmark mark='a'/>斜的那段：内存带宽，每秒{gbs(B)}GB，是我们测到的一个核心流式读写主存的最快速度。落在斜坡上的程序，是在等内存；经典的STREAM三元组测试，就落在斜坡上或斜坡下方。<bookmark mark='b'/>平的那段：我们测到的最快算术，每秒{gflops(P)}千兆次运算。两段在拐点相遇，每字节{P / B:.1f}次运算。<bookmark mark='c'/>矩阵乘向量，每个四字节的权重做两次运算，而且每个权重只用一次：它离不开斜坡。我们测到的最多是每秒{gflops(gv_best)}千兆次。<bookmark mark='d'/>矩阵乘矩阵的算术强度是n除以6。看它随着n增大往上爬：n等于{int(n_small)}时，开销占了主导，它只有{gflops(small)}；到了{int(n_big)}，它达到{gflops(big)}，碰到了屋顶。",

    'f"Intensity is a property of the algorithm':
        "算术强度是算法的性质，但只有代码真正挣到它才算数。<bookmark mark='a'/>第5章的四种矩阵乘法，纸面上的算术强度都一样，n除以6，大约每字节{n / 6:.0f}次运算。<bookmark mark='b'/>教科书循环远远落在屋顶下面，因为它一遍又一遍地取同样的数：它真正的算术强度要低得多。<bookmark mark='c'/>换序和分块往屋顶爬，<bookmark mark='d'/>而那个库碰到了屋顶：高了{gap:.0f}倍，在同一条竖线上。屋顶线说的是可能达到什么；屋顶下面的那段差距，是写内核的人的活儿。{many}",

    "f'With all {int(mt['threads'])} cores the roof rises":
        "用上全部{int(mt['threads'])}个核心，屋顶升到{gflops(Pn)}，是一个核心的{ratio:.1f}倍；内存是共用的，所以斜坡升得少一些。",

    'f"We also tried all {int(mt[\'threads\'])} cores at once':
        "我们也试了同时用全部{int(mt['threads'])}个核心，但别的任务正在用它们，我们看到的最好成绩是{gflops(Pn)}：在一台共享的机器上，你能拿到的屋顶，就是别人留给你的屋顶。",

    'f"Now put a GPU on the same axes.':
        "现在把一块GPU放到同样的坐标轴上。<bookmark mark='a'/>我们那个核心的屋顶线，缩在左下角。<bookmark mark='b'/>H100的张量核心，在16位算术下每秒大约做{H['tensor'] / 1000000000000.0:.0f}万亿次运算，它的内存每秒搬运{H['bw'] / 1000000000000.0:.2f}太字节。它的拐点在每字节大约{ridge:.0f}次运算。用16位数字，方阵乘法要在n大约到{round(n_star, -1):.0f}时才能碰到它。<bookmark mark='c'/>现在说说第19部分要讲的问题。语言模型一次写一个词元，每个权重只乘一次：大约每字节一次运算。那是在斜坡的底部，只有峰值的{100 * H['bw'] / H['tensor']:.1f}%。<bookmark mark='d'/>谷歌2017年的TPU论文，用的正是这张图。他们芯片的拐点在每字节1350次运算，K80 GPU的在9。一块芯片快不快，要看你的程序落在哪里。",

    # ------------------------------------------------------------------ Systolic
    'Chapter eight. Tensor cores and systolic arrays.':
        '第8章。张量核心与脉动阵列。',

    "There's an older idea that suits matrix products":
        "有一个更老的想法，比GPU的通道还要适合矩阵乘法。<bookmark mark='a'/>1978年，卡内基梅隆大学的孔祥重和查尔斯·雷瑟尔森提出了脉动阵列：由简单单元组成的网格，每个单元只和邻居相连，数据有节奏地脉动着穿过它，就像血液穿过心脏。<bookmark mark='b'/>从内存读出的一个数，从边缘进入，被它经过的每个单元使用，所以内存只读一次，算术却做了很多次。<bookmark mark='c'/>1982年，孔祥重解释了为什么这很重要：对矩阵乘法这样的问题，每次访存的运算次数可以不断增长，而不需要更多带宽。这就是屋顶线里的算术强度，直接做进了连线里。",

    'f"Here\'s one computing a product, cycle by cycle, simulated.':
        "这是一个正在计算乘积的阵列，一个周期一个周期地模拟出来。<bookmark mark='a'/>一个四乘四的单元网格，每个单元保存一个累加和。A的各行从左边进来，B的各列从上边进来，每一行、每一列都比前一个晚一个周期。<bookmark mark='b'/>每个周期，每个单元把穿过它的两个数相乘，加到自己的和上，再把A的数交给右边，把B的数交给下边。<bookmark mark='c'/>看那些正在工作的单元：一道斜的波前扫过整个网格。<bookmark mark='d'/>{T}个周期之后，每个单元都存着C的一个元素。{end}",

    'The result matches the product computed by numpy, exactly.':
        '结果和numpy算出的乘积完全一致。',

    "The result is checked against numpy's product.":
        '结果用numpy的乘积做了核对。',

    'Why does it work?':
        "为什么这样行得通？<bookmark mark='a'/>因为错开了时间，单元i、j在第i加j加k个周期遇到a_ik和b_kj：正好是它那个元素的各项，每项一次。<bookmark mark='b'/>最后一项在第2n减2再加K减1个周期到达最远的角，<bookmark mark='c'/>所以整个乘积要K加2n减2个周期：我们的例子是十个。<bookmark mark='d'/>每个数从内存读一次，被n个单元使用，所以每次运算的访存量像n分之一那样下降。更大的阵列就是更大的块，而且不需要缓存：复用就在导线里。",

    'f"In 2013 Google projected that if people used voice search':
        "2013年，谷歌估算，如果人们每天用三分钟语音搜索，光是语音识别网络，就需要把它的数据中心翻一倍。它转而造了一块芯片，只用了十五个月。<bookmark mark='a'/>张量处理器TPU，是一个256乘256的8位乘加器组成的脉动阵列，跑在700兆赫兹：每秒大约{tops / 1000000000000.0:.0f}万亿次运算。它从2015年起就在谷歌的数据中心里运行，还在和李世石的对局中运行了AlphaGo。<bookmark mark='b'/>在谷歌自己的工作负载上，它比旁边的CPU和GPU快十五到三十倍，每瓦性能好三十到八十倍。<bookmark mark='c'/>一块大而固定的网格，代价是：工作要按整块来做。一层257乘257的权重，要占四块，只用上四分之一的单元。尺寸是阵列大小整数倍的形状，才能全速运行，在TPU上和GPU上都一样。",

    'f"GPUs took the hint in 2017.':
        "2017年，GPU领会了这个意思。<bookmark mark='a'/>英伟达的Volta加入了张量核心：一种单元，在一个时钟里把两个四乘四矩阵相乘，再把乘积加到第三个上。每条指令六十四次乘加，而不是一次。<bookmark mark='b'/>一块V100有640个张量核心，由此得到半精度下每秒{V['tensor'] / 1000000000000.0:.0f}万亿次运算，是它普通通道的八倍。<bookmark mark='c'/>此后的每一代，都让张量核心更大、用的数字更小：A100加入了TF32和bfloat16，H100是8位浮点，Blackwell和Rubin是4位。GPU还是GPU，但它的大部分算术，如今都发生在它内部那些小小的脉动引擎里。",

    # ------------------------------------------------------------------ Formats
    'Chapter nine. Number formats in hardware.':
        '第9章。硬件里的数字格式。',

    'A floating-point number is a sign, an exponent and a mantissa':
        "一个浮点数由符号、指数和尾数组成：二进制的科学计数法。<bookmark mark='a'/>这是π，被舍入到本部分的硬件所支持的每种格式里。<bookmark mark='b'/>FP32，1985年的IEEE标准：8个指数位，23个尾数位，大约七位十进制有效数字。<bookmark mark='c'/>TF32和bfloat16保留了FP32的8位指数，所以范围一样，但把尾数砍到了10位和7位。FP16反过来取舍：5个指数位，10个尾数位。<bookmark mark='d'/>然后是两种8位格式：4个指数位加3个尾数位，或者5个加2个。<bookmark mark='e'/>还有4位：2个指数位，1个尾数位。π变成了3。",

    'Two numbers describe a format.':
        "两个数就能描述一种格式。<bookmark mark='a'/>有M个尾数位，每个2的幂之间就被切成2的M次方个相等的台阶。<bookmark mark='b'/>就近舍入，最多偏差半个台阶，所以相对误差至多是2的负M加1次方，叫作单位舍入误差。这就是精度。<bookmark mark='c'/>指数位决定范围：最大的数比2乘以2的最大指数次方略小一点。<bookmark mark='d'/>对E4M3来说是448，因为有一个位模式留着表示“非数”。FP16最大到65504，所以用FP16训练要小心，而有着FP32指数的bfloat16就不用。",

    'f"Let\'s measure it.':
        "我们来测一测。把一百万个高斯样本舍入到每种格式，再做比较。<bookmark mark='a'/>尾数每少一位，误差就成倍增加。FP32的误差只有一亿分之几，bfloat16大约{100 * r['BF16']['gauss']:.2f}%，8位的E4M3大约{100 * r['E4M3']['gauss']:.1f}%，4位是{100 * e4:.0f}%。<bookmark mark='b'/>白点是预测值：如果舍入误差在一个台阶里均匀分布，数值在对数上均匀分布，那么相对误差的均方根，就是2的负M次方乘以一个常数，即2的自然对数除以18再开平方，大约五分之一。这个预测忽略了极小和极大的数，{agree}。4位偏离得最多：在那里，很多样本落在了最小的台阶之下。",

    '"Four bits have so little range':
        "4位的范围太小，整个矩阵用一个缩放因子是不行的：少数几个大值，会把其余的数全都挤到最底下那一级台阶里。<bookmark mark='a'/>解决办法在2023年由开放计算项目标准化，叫作微缩放：给每32个数一组，配一个共享的指数。<bookmark mark='b'/>我们把{what}用每种方式都舍入了一遍。{verdict}<bookmark mark='c'/>第19部分会用这些格式，以4位来运行一个真实的模型。",

    'f"Sharing a scale per block of thirty-two cuts':
        "每32个数共享一个缩放因子，把4位的误差从{100 * t4:.0f}%降到了{100 * mx4:.0f}%；英伟达更细的块，配上8位的缩放因子，又降到了{100 * nv:.0f}%。",

    "f'Here the block scales give":
        "在这里，分块缩放得到{100 * mx4:.0f}%和{100 * nv:.0f}%，而整个张量只用一个缩放因子时是{100 * t4:.0f}%。",

    'f"Why go small at all?':
        "到底为什么要用小格式？因为乘法器的大小，大致随尾数宽度的平方增长，而每少搬一位，就省下一份带宽。<bookmark mark='a'/>位数减半，张量核心就做两倍的工作：一块H100在bfloat16下每秒做{H['tensor'] / 1000000000000.0:.0f}万亿次运算，在FP8下做{H['fp8'] / 1000000000000.0:,.0f}万亿次；Blackwell GPU在4位下又翻一倍。<bookmark mark='b'/>但前提是硬件为它而造。{cpu_says}<bookmark mark='c'/>历史是这样的：1985年卡亨主导的IEEE标准；谷歌大脑为TPU设计的bfloat16；2022年英伟达、Arm和英特尔提出的8位浮点；2023年的微缩放。第18部分用8位训练；第19部分用4位来推理。",

    "f\"This computer's processor has no bfloat16 units":
        "这台计算机的处理器没有bfloat16单元，PyTorch的bfloat16矩阵乘法，比它的FP32慢{slow:.1f}倍。",

    "f\"This computer's processor has bfloat16 instructions, yet":
        "这台计算机的处理器有bfloat16指令，但在这里，PyTorch的bfloat16矩阵乘法仍比它的FP32慢{slow:.1f}倍。",

    "f\"This computer's processor has bfloat16 instructions, and":
        "这台计算机的处理器有bfloat16指令，PyTorch的bfloat16矩阵乘法，速度是它的FP32的{1 / slow:.1f}倍。",

    # ------------------------------------------------------------------ Interconnect
    'Chapter ten. Interconnect and collectives.':
        '第10章。互连与集合通信。',

    'f"A frontier model doesn\'t fit on one chip.':
        "一个前沿模型，一块芯片是装不下的。<bookmark mark='a'/>Llama 3.1的4050亿个参数，用16位数存要810GB；训练时，加上梯度和优化器状态，每个参数大约要16个字节，总共约{train / 1000000000000.0:.1f}太字节。一块H100装80GB，光是装下它，就至少要{need}块，而Meta是在16384块上训练的。<bookmark mark='b'/>所以芯片之间必须通信，而且每远一步就更慢。GPU内部，它自己的内存：每秒3.35太字节。同一台服务器里的GPU之间，NVLink：每秒900GB。服务器之间，InfiniBand网络：大约一百。每一步大约差十倍。",

    'NVIDIA built its own links.':
        "英伟达造了自己的链路。<bookmark mark='a'/>NVLink随P100在2016年问世，每块GPU每秒160GB；此后每一代大致翻一倍，到2026年的Rubin，是每秒三太字节。<bookmark mark='b'/>链路还需要一种拓扑形状。交换机把所有东西和所有东西连起来：英伟达的NVL72机柜，把72块GPU放在同一张NVLink网络上，总共每秒130太字节，Rubin这一代是216。<bookmark mark='c'/>机柜之间，用胖树，这是查尔斯·雷瑟尔森1985年的设计：越往上链路越多，顶层才不会成为瓶颈。<bookmark mark='d'/>谷歌把它的TPU连成三维环面，每块芯片连着六个邻居；从TPU v4起，还用光路交换机重新配置它，一次4096块芯片。",

    'f"To reason about communication, use the simplest model that works.':
        "要推理通信，就用最简单而管用的模型。<bookmark mark='a'/>发一条n字节的消息，花一个固定的α，也就是延迟，再加上n除以β，β是带宽。<bookmark mark='b'/>我们在这台计算机的两个进程之间测了它，消息从8字节到32兆字节。<bookmark mark='c'/>拟合结果：α大约{a * 1000000.0:.0f}微秒，β大约每秒{B / 1000000000.0:.1f}GB。<bookmark mark='d'/>小于α乘β，在这里大约{round(knee / 1000.0, -1):.0f}千字节，消息不管多大，代价都差不多；大于它，带宽就决定一切。在GPU集群上，数字会变，是微秒和每秒几百GB，但形状不变。",

    "Training on many GPUs means, every step":
        "在许多块GPU上训练，意味着每一步都要把所有人的梯度加起来，让每块GPU都拿到总和：这叫全规约。<bookmark mark='a'/>环形算法把每块GPU的数据切成p块。<bookmark mark='b'/>每一步，每块GPU把一块发给邻居，再把收到的那块加到自己的上面。p减1步之后，每块GPU都持有完整总和的一块。<bookmark mark='c'/>然后再用p减1步，把算完的块传一圈，直到每块GPU都拿到全部。<bookmark mark='d'/>每一步发送n除以p个字节，所以总时间是2乘以p减1个α，加上2乘以p分之p减1，再乘以n除以β。不管有多少块GPU，带宽项都不超过2n除以β，而且在这一项上，没有哪种算法能做得更好。第18部分的数据并行，就建立在这上面。",

    'f"There\'s another way: a tree.':
        "还有另一种办法：树。<bookmark mark='a'/>先两两相加，再把两对相加，一直加到一块GPU上，再把总和发回去。这是2乘log p步，而不是2p步，但每一步都要发送整条消息。<bookmark mark='b'/>这里是两种算法，以延迟为单位，分别对8块、64块和512块GPU。消息小的时候，树赢：步数少。消息大的时候，环赢：每一步的数据少。<bookmark mark='c'/>512块GPU时，交叉点在大约{cross[str(ps[-1])]:.0f}倍的α乘β。延迟几微秒、带宽是NVLink那么大时，α乘β是几兆字节，而梯度是吉字节量级：大块数据用环，看重延迟用树，像英伟达NCCL这样的库会替你选。<bookmark mark='d'/>{meas}",

    'f"On this computer\'s four processes, the measured times follow the model':
        "在这台计算机的四个进程上，大消息的实测时间和模型相差在两倍以内，而且环在模型预言的地方超过了树。",

    'We also timed both on four processes of this computer':
        "我们也在这台计算机的四个进程上给两种算法计了时，但每个核心都和别的任务共用，测出来的时间比模型慢好几倍，噪声也太大，没法用来检验它：这个模型描述的是网络，而不是一个忙碌的操作系统。",

    # ------------------------------------------------------------------ Kernel
    'Chapter eleven. Writing a kernel.':
        '第11章。写一个内核。',

    "Here is chapter five's tiling, written for a GPU":
        "这是第5章的分块，照教科书的教法，写成GPU代码。<bookmark mark='a'/>每个线程块计算C的一个T乘T的块，每个线程负责一个元素。<bookmark mark='b'/>线程块声明两个共享内存块，也就是第6章里由程序员管理的SRAM。<bookmark mark='c'/>每一轮，每个线程从全局内存里拷贝A的一个数和B的一个数到共享块里：相邻的线程，相邻的地址，访存合并。<bookmark mark='d'/>线程们互相等待，然后每个线程从共享内存里做T次乘加，再等一次，然后这些块才会被覆盖。<bookmark mark='e'/>每个从全局内存取来的数被用了T次：算术强度是T除以4。块大小取32，就是每字节8次运算，仍然低于H100的拐点。真正的内核会更进一步：每个线程在寄存器里再保留一小块自己的数据，乘加交给张量核心去做。",

    'f"How many threads can share a multiprocessor?':
        "一个多处理器能容纳多少线程？第3章说：要多少，就要多到足以隐藏内存延迟。但它们共用多处理器的寄存器和共享内存。<bookmark mark='a'/>H100的一个多处理器有65536个寄存器。如果一个内核的每个线程要R个寄存器，那最多只能驻留65536除以32R个线程束，而且永远不超过64个。这个比例叫占用率。<bookmark mark='b'/>每个线程越大，它就一级一级地往下掉。<bookmark mark='c'/>我们那个小而简单的分块内核，占用率是{100 * ex1:.0f}%。一个用大寄存器块、专门喂张量核心的内核，只有{100 * ex2:.0f}%。<bookmark mark='d'/>而后者可能更快：2010年，瓦西里·沃尔科夫证明，更少的线程、每个线程用寄存器做更多的事，常常胜过满占用率。这又是第3章的那个权衡：用线程来隐藏延迟，还是用每次读取做更多算术来隐藏。",

    'Writing kernels like that by hand is hard':
        "这样手写内核很难，挤出最后那两倍性能就更难。<bookmark mark='a'/>2019年，哈佛的研究生菲利普·蒂莱，和孔祥重，也就是做脉动阵列的那位孔祥重，以及大卫·考克斯一起发表了Triton。你写的是Python，编程的对象是输出的一个块，而不是一个线程。<bookmark mark='b'/>取A的一块、B的一块，用一个点积把它们相乘，累加，往下走：第5章的分块，十一行代码。编译器决定线程怎样分工，把块经由共享内存中转，合并访存，并用上张量核心。<bookmark mark='c'/>OpenAI在2021年发布了它，如今PyTorch的编译器自己就会写Triton内核。英伟达的CUTLASS库和JAX的Pallas，在C加加和JAX里扮演同样的角色。",

    'The model example of thinking this way is FlashAttention.':
        "这种思路的典范，是FlashAttention。<bookmark mark='a'/>注意力要给每一对位置算一个分数：一张T乘T的表。标准实现把这张表写到高带宽内存里，再读回来做softmax，然后再读一次去给值加权。输入一长，这些搬运就占了主导，张量核心只能干等。<bookmark mark='b'/>2022年，斯坦福的道三（Tri Dao）和同事改成一块一块地计算注意力，每一块都留在片上SRAM里，用一个滚动的最大值和滚动的和，让softmax的结果精确无误。<bookmark mark='c'/>这张表根本不写出去。他们证明，它的访存量是T平方乘d平方除以M，M是SRAM的大小：只要d平方小于M，就比标准版本少，而实践中正是如此。同样的算术，更快，因为它搬的字节更少。第19部分会推导它。",

    # ------------------------------------------------------------------ Trends
    'Chapter twelve. FLOPs, dollars and watts.':
        '第12章。算力、美元与瓦特。',

    'f"How fast is all this improving?':
        "这一切进步得有多快？<bookmark mark='a'/>这是英伟达、谷歌、AMD和亚马逊从2017年以来的旗舰加速器，来自Epoch AI的数据库。它们的16位张量算力，每{Tt:.1f}年翻一倍。<bookmark mark='b'/>内存带宽，每{Tb:.1f}年翻一倍。<bookmark mark='c'/>算术跑得比内存快。Epoch自己对47款加速器的研究也发现了同样的事，2.3年对4年；阿米尔·戈拉米和同事回顾了二十年，把它叫作内存墙。<bookmark mark='d'/>所以屋顶线的拐点一直往右移：在这组数据里，一块芯片每读一个字节能做的运算次数，每{Tr:.1f}年翻一倍。每一代都需要更多的复用，才能保持忙碌。",

    'f"Here\'s the ridge, generation by generation':
        "这是一代一代的拐点，来自各家的数据手册。<bookmark mark='a'/>用16位数字，它从V100的每字节大约{b16[0]:.0f}次运算，移到了Blackwell GPU的大约{b16[3]:.0f}次。<bookmark mark='b'/>但每一代也加入了更小的格式，用各自最小的格式算，Rubin的拐点已经爬到了大约{vals[-1]:,.0f}。更小的数字身兼两职：每个周期两倍的算术，每个数一半的字节，正是后者把工作负载拉回到拐点上。",

    'f"What about energy?':
        "那能量呢？<bookmark mark='a'/>用每块芯片的峰值除以它的功耗：在这组数据里，每瓦每秒的16位运算次数，每{Te:.1f}年翻一倍；Epoch算出来是三年。<bookmark mark='b'/>训练AlexNet的那块显卡，每次浮点运算大约花{pj_x:.0f}皮焦。一块H100大约花{pj_h:.1f}：少了大约{round(pj_x / pj_h, -1):.0f}倍，部分是因为用了更少的位。不过第6章的教训仍然成立：把操作数从内存里取出来，比算术本身更费能。按Epoch的统计，性价比大约每两年翻一倍。",

    'f"And then there\'s the electricity.':
        "然后还有电力。<bookmark mark='a'/>国际能源署估计，2024年数据中心用了大约{IEA['twh_2024']}太瓦时，约占全世界电力的百分之一点五，并预计到2030年约为{IEA['twh_2030']}，人工智能是主要推动力。<bookmark mark='b'/>训练Llama 3.1的集群，估计要二十多兆瓦。<bookmark mark='c'/>英伟达现在用一百兆瓦的“AI工厂”来描述它的Rubin系统：四万块GPU，算上冷却和网络，每块大约{per_gpu / 1000.0:.1f}千瓦。建设人工智能的瓶颈，越来越是那根电线。",

    # ------------------------------------------------------------------ Accelerators
    'Chapter thirteen. Beyond the GPU.':
        '第13章。GPU之外。',

    'f"The TPU was the first of many chips built only for neural networks.':
        "TPU是众多只为神经网络而造的芯片里的第一款。<bookmark mark='a'/>谷歌这条产品线，从2015年的一块8位推理芯片，走向了训练：2017年的TPU v2加入了高带宽内存、bfloat16，以及由许多芯片连成的集群；v4用光路交换机把4096块连在一起。<bookmark mark='b'/>第七代Ironwood，2025年：每块芯片每秒{IRONWOOD['fp8'] / 1000000000000.0:,.0f}万亿次8位运算，集群规模{IRONWOOD['pod']:,}块。<bookmark mark='c'/>2026年4月，谷歌发布了两款第八代芯片，一款用于训练，一款用于推理服务，训练超级集群有{TPU8T['pod']:,}块芯片。谷歌就在自己的TPU上训练Gemini模型。<bookmark mark='d'/>亚马逊造Trainium，微软造Maia，Meta造MTIA。它们大多是某种规模的脉动阵列，由高带宽内存喂数据：正是第6到第8章的配方。",

    'Others changed the shape of the chip itself.':
        "还有人改变了芯片本身的形状。<bookmark mark='a'/>芯片是从直径三十厘米的硅晶圆上切下来的。Cerebras不切：整片晶圆就是一块芯片。<bookmark mark='b'/>它的第三代产品是2024年的，有四万亿个晶体管、九十万个核心，以及分布在它们之间的44GB SRAM，所以模型的权重可以就挨着运算单元，而不是放在旁边的内存芯片里。<bookmark mark='c'/>它的面积大约是H100裸片的五十七倍。难点正是大家都说不可能的那些：这么大一片晶圆上的缺陷，它要绕开走；还有给它散热和供电。",

    'f"Groq took the opposite bet from the GPU.':
        "Groq押了和GPU相反的注。<bookmark mark='a'/>它的创始人乔纳森·罗斯，曾在谷歌参与发起TPU项目。Groq的LPU根本没有高带宽内存：权重住在片上SRAM里，编译器预先安排好每一个周期，所以没有什么要等缓存。<bookmark mark='b'/>对一次写一个词元来说，屋顶线的斜坡就是一切，而SRAM很快。2025年12月，英伟达获得了Groq技术的授权，并聘请了它的创始人；2026年3月，它介绍了成果：一个装有256块Groq 3 LPU的机柜，每块的SRAM带宽大约每秒{per_lpu / 1000000000000.0:.0f}太字节，而Rubin GPU的内存是{R['bw'] / 1000000000000.0:.1f}。<bookmark mark='c'/>代价是容量：每块芯片500兆字节。一个一万亿参数的模型，用4位存，大约需要{chips_1t:,.0f}块。所以英伟达把它们搭配起来用：GPU读长长的提示，负责注意力；LPU运行每个新词元的其余部分。",

    'Two older dreams are still being chased.':
        "还有两个更老的梦想，人们仍在追逐。<bookmark mark='a'/>一个是模拟存内计算：把每个权重存成网格里一个单元的电导，把输入作为电压加在各行上，按欧姆定律，每个单元的电流就是一个乘积；按基尔霍夫定律，一列上的电流自动相加。<bookmark mark='b'/>一整个矩阵乘向量，一步完成，一个权重都不用搬。2023年，IBM在一块有三千五百万个这种单元的芯片上运行了语音识别；难点在于噪声和精度。<bookmark mark='c'/>另一个是类脑芯片，它们像神经元一样用脉冲计算，而且只在有变化时才计算：2014年IBM的TrueNorth，英特尔的Loihi，以及2024年的Hala Point，有超过十亿个人工神经元。两者都还跑不了今天的前沿模型。它们押的都是第6章的那个教训：最便宜的数据搬运，就是不搬。",

    # ------------------------------------------------------------------ Frontier
    'Chapter fourteen. The frontier, late 2026.':
        '第14章。2026年底的前沿。',

    'Where does all this stand at the end of 2026?':
        "到2026年底，这一切走到了哪里？<bookmark mark='a'/>英伟达2024年3月发布的Blackwell，碰到了芯片制造的极限：一块裸片不能比光刻机一次曝光的面积更大。所以Blackwell是两块达到这个极限的裸片，以每秒十太字节连在一起，像一块GPU一样工作：2080亿个晶体管，张量核心支持4位数字。<bookmark mark='b'/>销售的单位变成了机柜。一台GB200 NVL72把72块这样的GPU放在同一张NVLink网络上，用液体冷却，让整个机柜表现得像一块巨大的GPU；2025年的Blackwell Ultra又把每块GPU的内存提高到288GB。",

    'f"Its successor is in production now.':
        "它的后继者现在已经投产。<bookmark mark='a'/>一台Vera Rubin NVL72机柜里，有72块Rubin GPU，和36块英伟达自己的Arm CPU。<bookmark mark='b'/>每块GPU有288GB的第四代高带宽内存，每秒读{R['bw'] / 1000000000000.0:.1f}太字节，训练时每秒做{R['fp4'] / 1000000000000000.0:.0f}千万亿次4位运算。第六代NVLink每块GPU每秒搬运{R['link'] / 1000000000000.0:.0f}太字节，整个机柜{rack['nvlink'] / 1000000000000.0:.0f}太字节。<bookmark mark='c'/>英伟达现在按一百兆瓦来卖这些东西：一栋楼里四万块GPU。<bookmark mark='d'/>再注意一下拐点：用4位算术，大约每字节{ridge:,.0f}次运算。只有复用极多的工作，才能把它全部用上。",

    'f"The unit of computing keeps growing.':
        "计算的单位还在不断变大。<bookmark mark='a'/>2022年，共享同一张高速网络的GPU，是一台服务器里的八块。<bookmark mark='b'/>到了Blackwell，是一个机柜里的七十二块。<bookmark mark='c'/>谷歌的环面集群还要更大：4096块TPU v4芯片，2025年9216块Ironwood芯片，以及今年发布的TPU 8t超级集群里的{TPU8T['pod']:,}块。<bookmark mark='d'/>谷歌说，它新的数据中心网络，能让一百万块这样的芯片像一个集群那样工作。第18部分要讲的，就是怎样用这样的机器完成一次训练。",

    'The newest trend is to split the work by where it sits on the roofline.':
        "最新的趋势，是按工作落在屋顶线上的位置来拆分它。<bookmark mark='a'/>读一个提示，是矩阵乘矩阵：算术强度高，受算力限制。一次一个词元地写答案，是矩阵乘向量：算术强度低，受内存限制。<bookmark mark='b'/>所以英伟达把Rubin GPU，以及一款专为超长提示设计的变体，和Groq的SRAM芯片搭配起来做解码；<bookmark mark='c'/>谷歌的第八代是两块芯片，一块用于训练，一块用于推理服务，片上内存是前一代的三倍，用来存注意力缓存。<bookmark mark='d'/>如今的限制是功耗、内存带宽，以及芯片之间的链路，正是本部分的三条主线。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock. When the voltage stopped falling":
        "我们来总结一下。电压降不下去以后，时钟就不再上涨，用上更多晶体管的唯一办法，就是并行。GPU以线程束为单位运行成千上万个线程，并为分支发散付出代价。矩阵乘法几乎就是一个网络全部的算术，分块让每个取来的数被用上很多次。内存是一个层次，从小而近到大而远，屋顶线告诉你，一个程序受限于算术还是受限于字节。脉动阵列把复用做进了连线里。更少的位数换来了吞吐量，误差的代价可以测量。一块芯片不够时，环形全规约以接近带宽极限的效率分担工作。",

    'All of this comes back. Part 18 trains a model across many GPUs':
        "这些都会再出现。第18部分在许多GPU上训练模型，用到α–β模型、环形全规约，以及8位算术。第19部分把推理放到屋顶线上：读提示受算力限制，写答案受内存限制，FlashAttention和4位格式随之而来。第15部分的记忆方法，是按高带宽内存的大小设计、为了用上张量核心而写的；第16部分的专家在NVLink域里交换词元，而张量核心的四选二稀疏，能让它们的算术翻倍。",

    'Here are six problems to try, from arithmetic intensity':
        '这里有六道习题，从算术强度，一直到GPU要隐藏的延迟。请在这里暂停，动手做一做；完整的解答在本部分的笔记里。',

    'Next time: pretraining at scale.':
        "下一次：大规模预训练。上万亿个词元从哪里来，又怎样清洗；一个模型怎样被切开，分到成千上万块GPU上，按数据、按张量、按流水线阶段、按专家，而本部分的全规约就在正中央；8位训练怎样保持稳定；以及在一万六千块GPU上训练时，会出什么问题。",

    "Hennessy and Patterson's book is the place to go deeper":
        "想深入了解这一切，就去读亨尼西和帕特森的书；GPU编程，就读柯克和胡文美的书。感谢观看，第18部分再见。",
}

PHRASES = {
    'in C.': '，用的是C语言。',
    'It was the largest size we tried.': '这也是我们试过的最大的块。',
    'faster': '更快',
    'slower': '更慢',
    'and the measurements land on it': '测量值正好落在预测上',
    'and the measurements land close to it': '测量值落在预测附近',
    "the weights of this series' own small language model": '本系列自己那个小语言模型的权重',
    'a weight matrix of the voice model narrating this video': '为这个视频配音的语音模型里的一个权重矩阵',
    'Gaussian samples': '高斯样本',
}
