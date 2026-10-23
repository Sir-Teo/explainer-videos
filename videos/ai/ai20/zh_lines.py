"""Chinese narration for ai20: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第20部分：生成的四种方法'

CHAPTERS = {
    'Hook': '没有人写过的数字',
    'Problem': '1. 生成问题',
    'Autoregressive': '2. 一次一个像素',
    'Latent': '3. 从亥姆霍兹机到VAE',
    'VAE': '4. 训练VAE：码率、失真与坍缩',
    'Game': '5. 对抗博弈',
    'Dynamics': '6. GAN为什么会绕圈',
    'Wasserstein': '7. 瓦瑟斯坦GAN',
    'Scale': '8. 规模化的GAN：BigGAN、StyleGAN与反演',
    'Flows': '9. 归一化流',
    'NeuralODE': '10. 神经ODE与连续流',
    'Hopfield': '11. 霍普菲尔德与玻尔兹曼',
    'RBM': '12. 对比散度',
    'Langevin': '13. 朗之万动力学与分数函数',
    'Judging': '14. 怎样评判一个生成模型',
    'Budget': '15. 五个模型，同一份预算',
    'Meet': '16. 几个家族的交汇',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'f"None of these sixty-four digits was written by a person.':
        "这64个数字，没有一个是人写的。<bookmark mark='a'/>每一块都出自一台不同的机器，它们都在制作这个视频的电脑上训练，"
        "每台大约{mins:.0f}分钟，学的是同样的6万个手写数字。<bookmark mark='b'/>第一台一次写一个像素。"
        "<bookmark mark='c'/>第二台把每个数字压缩成16个数，再学会把它们展开。<bookmark mark='d'/>第三台是通过和一个评论者"
        "对弈学会的。<bookmark mark='e'/>第四台把随机噪声平滑地、可逆地，弯成了墨迹。",

    'Real handwriting looks like this: samples from some distribution':
        "真正的手写数字是这样的：它们是某个分布p(x)的样本，而这个分布没有人写得出来。<bookmark mark='a'/>本部分的问题是："
        "只凭样本，怎样学到一个能从中抽出新样本的分布？<bookmark mark='b'/>这个领域找到了四个行得通的答案，还有一个更古老的、"
        "总是被重新拾起的答案。一块一块地把样本搭出来。把它压缩成一个编码，再学会把编码展开。让两个网络互相对抗。"
        "用一个可逆映射把简单的噪声弯过来。<bookmark mark='c'/>或者，雕出一片能量地形，让数据躺在谷底。下一次要讲的扩散模型，"
        "就是用这些零件搭起来的。",

    'This is Part 20 of AI, Built, and the start of its fourth act':
        "这是《人工智能，从零搭建》的第20部分，也是第四幕“生成与感知”的开始。<bookmark mark='a'/>本部分的内容：生成问题及其历史；"
        "自回归模型；隐变量，从亥姆霍兹机到变分自编码器；对抗博弈，它为什么会绕圈，以及瓦瑟斯坦距离和StyleGAN怎样驯服了它；"
        "可逆映射，从耦合层到神经ODE；能量，从霍普菲尔德和玻尔兹曼，到朗之万动力学和分数函数；最后是怎样评判一个生成模型，"
        "每个家族都在这里训练，并在同一份预算下比较。",

    # ------------------------------------------------------------------ Problem
    'Chapter one. The generative problem.':
        '第1章。生成问题。',

    'Here is the problem at its smallest.':
        "先看这个问题最小的样子。平面上有2万个点，来自一个形状像两弯月亮的分布p。<bookmark mark='a'/>在这里，因为分布是我们造的，"
        "所以我们确切地知道p。可在现实中，面对图像或文本，没有人知道：我们手里只有样本。<bookmark mark='b'/>生成模型，"
        "就是一个带参数θ、从这些样本里学出来的分布q，我们可以从它里面抽样；<bookmark mark='c'/>最好还能计算它，"
        "说出一个新的x有多大可能；<bookmark mark='d'/>最好还能给每个x一个编码，一个说明它是什么的简短描述。",

    'f"How do we fit q to samples?':
        "怎样让q去拟合样本？主力方法是第1部分讲过的最大似然：让样本尽可能地可能，也就是让平均意外度，负log q，尽可能小。"
        "<bookmark mark='a'/>把这个平均值拆成两部分。<bookmark mark='b'/>第一部分是数据自身的熵，任何模型都打不破它；"
        "第二部分是从p到q的KL散度，也就是犯错的代价。<bookmark mark='c'/>所以，最大似然就是最小化KL散度。<bookmark mark='d'/>"
        "对我们的三个测试分布，这个下限是已知的：双月是{hm:.2f}奈特，八个高斯组成的环是{hr:.2f}，棋盘格是{hc:.2f}。"
        "每个模型在留出点上的意外度，都要和这些下限比。",

    'How we got here. In 1948 Claude Shannon':
        "我们是怎么走到这里的。1948年，克劳德·香农用统计出来的频率，一个字母一个字母地生成英文：这是第一个自回归模型。"
        "<bookmark mark='a'/>20世纪80年代，物理学家和心理学家把记忆描述成一片能量地形里的山谷，这就是霍普菲尔德的网络，"
        "以及辛顿和谢诺夫斯基的玻尔兹曼机；<bookmark mark='b'/>到了90年代，Dayan和辛顿又加了第二个网络，去猜测所见之物背后的隐藏原因，"
        "这就是亥姆霍兹机。<bookmark mark='c'/>2006年，堆叠起来的玻尔兹曼机让深度学习重新起步。<bookmark mark='d'/>"
        "接着，短短三年里，出现了变分自编码器、生成对抗网络、可逆的流，以及PixelCNN。<bookmark mark='e'/>大约六年里，"
        "GAN画出的图像最清晰，直到2021年，第21部分的主角扩散模型超过了它们。<bookmark mark='f'/>今天的图像和视频系统，"
        "把这些想法全都结合了起来。",

    'Here are the families we will build, and what each one offers.':
        "这些就是我们要搭建的家族，以及每个家族各自能提供什么。<bookmark mark='a'/>自回归模型给出精确的似然，训练也稳定，"
        "但只能一块一块地采样。<bookmark mark='b'/>VAE一次就能采样，还能给出编码，但只有似然的一个下界。<bookmark mark='c'/>"
        "GAN一次就能采样，完全没有似然，而且出了名地难训练。<bookmark mark='d'/>流在纸面上什么都有，代价是对网络结构的限制。"
        "<bookmark mark='e'/>能量模型只知道差一个常数的密度，这个常数它算不出来，而且采样要走很长一串步子。<bookmark mark='f'/>"
        "Zhisheng Xiao、Karsten Kreis和Arash Vahdat把它叫作一个三难困境：清晰的样本，覆盖全部数据，以及快速的采样。"
        "多年来，大多数家族只能做到其中两样。",

    'Our test bench.':
        "我们的试验台。平面上的三个分布：双月，八个窄高斯组成的环，还有一个边缘锐利的棋盘格。它们小到可以看清模型做的每一件事，"
        "而且每一个都有自己的难处。<bookmark mark='a'/>还有图像：MNIST手写数字，6万个用来训练，1万个用来测试。"
        "为了让每个家族在这台电脑上都训练得起，每个数字都被平均缩小到14乘14个像素，<bookmark mark='b'/>每个像素再切成16个灰度级，"
        "也就是4比特。<bookmark mark='c'/>本部分的每个图像模型，都得到同样的算力预算，一次运算一次运算地数出来，"
        "而且都从几个不同的随机起点训练，好让我们看到结果的波动范围。",

    # ------------------------------------------------------------------ Autoregressive
    'Chapter two. One pixel at a time.':
        '第2章。一次一个像素。',

    'The first answer needs no new mathematics at all.':
        "第一个答案完全不需要新的数学。任何多个变量上的分布，都可以按概率的链式法则分解：<bookmark mark='a'/>第一个变量的概率，"
        "乘以给定第一个时第二个的概率，再乘以给定前两个时第三个的概率，依此类推。<bookmark mark='b'/>每个因子都是一次预测："
        "给定之前的一切，预测下一个变量。把每个因子都学会，你就精确地得到了整个分布；按顺序逐个采样，你就得到一个样本。"
        "<bookmark mark='c'/>1948年香农就是这样生成英文的，本系列的每个语言模型也是这样写字的，而今天，我们也将这样画出一个数字。",

    'f"Start in the plane, with two variables.':
        "先从平面上的两个变量开始。第一个因子，p(x1)，是沿着底边的一条曲线：双月从左到右是怎样铺开的。<bookmark mark='a'/>"
        "第二个因子，给定x1时x2的概率，在每一个切片上都是一条不同的曲线：这里画出了其中三条。每一条都是10个高斯的混合，"
        "它们的权重、中心和宽度，都由一个输入x1的小网络给出。<bookmark mark='b'/>把两个因子乘起来，就是模型学到的密度，"
        "这里回放了整个训练过程，旁边是它在留出点上的意外度。<bookmark mark='c'/>{verdict}",

    "f'It ends {gap:.2f} nats above the floor: close to the best":
        '最后它比下限高{gap:.2f}奈特：已经接近任何模型所能做到的最好。',

    "f'It ends {gap:.2f} nats above the floor: the shape is right":
        '最后它比下限高{gap:.2f}奈特：形状是对的，边缘还有点软。',

    'An image is the same story with more variables.':
        "图像也是同一个故事，只是变量更多。把一个数字的196个像素按阅读顺序排好，从左到右，从上到下。<bookmark mark='a'/>"
        "预测这个像素时，模型可以看它之前的每一个像素，但之后的一个也不能看。它的输出是16个概率，每个灰度级一个，是一个softmax，"
        "和语言模型预测下一个词元一模一样。<bookmark mark='b'/>让它训练起来很快的诀窍，是一个掩码。卷积网络的每个滤波器，"
        "都把属于未来的那一半设为零，这样网络跑一遍，就能同时预测全部196个像素，每个像素只用它自己的过去。<bookmark mark='c'/>"
        "这个想法从NADE和MADE这两种针对二值图像的自回归网络开始，发展成了DeepMind的Aaron van den Oord和同事在2016年提出的"
        "PixelRNN和PixelCNN，同一年又发展成了WaveNet，一次一个采样点地生成语音。",

    "There's a catch, and we can see it by asking the network itself":
        "这里有个问题。我们可以直接问网络本身，它的预测依赖于哪些输入像素：求一个像素的预测对每个输入的梯度。<bookmark mark='a'/>"
        "如果简单地把带掩码的滤波器一层层叠起来，右上方会有一块楔形的像素永远看不见，尽管它们在阅读顺序里排在前面。"
        "每一层的掩码，都会把那个角再多切掉一点。<bookmark mark='b'/>第二篇PixelCNN论文给出的修正，是把网络一分为二："
        "一个竖直的栈，看得到上面所有的整行；一个水平的栈，看得到这一行已经写好的部分；前者把信息送给后者。盲区消失了。"
        "我们训练的就是这种结构。",

    'f"Here is ours learning, on the fourteen-pixel digits.':
        "这是我们的模型在14像素数字上的学习过程。左边是它在留出数字上的意外度，单位是每像素比特数；右边是它在每个检查点画出的东西，"
        "每次用的都是同一组随机数。<bookmark mark='a'/>没训练时，它每个像素要付{cv[0, 2]:.2f}比特，大约就是在16个灰度级里均匀乱猜的代价，"
        "画出来的是一片雪花。<bookmark mark='b'/>随着读到的数字越来越多，它先学会大多数像素是黑的，再学会墨迹是一笔一笔的，"
        "然后学会笔画的形状。<bookmark mark='c'/>最后它停在每像素{finals[0]:.2f}比特。从不同随机起点出发的三次训练，"
        "最后落在{lo:.2f}到{hi:.2f}之间：这些数字反映的是模型本身，不是运气。",

    'f"And here is one digit being drawn.':
        "这是一个数字正在被画出来。右边是模型对下一个像素给出的16个概率。<bookmark mark='a'/>在空白的边缘，它很确定：黑色。"
        "<bookmark mark='b'/>到了笔画的边上，它在深浅之间犹豫，它掷出的那枚硬币决定了数字的形状；一笔一旦开始，"
        "它就很有把握这一笔会继续下去。<bookmark mark='c'/>代价在于顺序：画一个数字要过196遍网络，每一遍都要等上一遍。"
        "在这台电脑上，就是每个数字{ms_ar:.1f}毫秒，大约是第5章那个GAN所需时间的{ratio:,.0f}倍。语言模型一个词元一个词元地写，"
        "付的是同样的代价，而第19部分讲的，就是怎样付得更快。",

    # ------------------------------------------------------------------ Latent
    'Chapter three. From Helmholtz machines':
        '第3章。从亥姆霍兹机到变分自编码器。',

    'The second answer adds something hidden.':
        "第二个答案加进了一些隐藏的东西。假设每个数字都来自一个编码z：几个数，从普通的高斯分布里抽出来。<bookmark mark='a'/>"
        "一个解码器，也就是一个参数为θ的网络，把每个编码变成图像上的一个分布。这是一个真的解码器，在我们的数字上训练，"
        "编码只有两个数：左边平面上的每一个点，都被解码成右边的一个数字，而这些数字平滑地过渡成彼此。<bookmark mark='b'/>"
        "于是，一张图像的概率，就是对所有可能产生它的编码求平均。麻烦就出在这个积分上：我们算不出它，所以也没法直接最大化它。"
        "<bookmark mark='c'/>反过来，从图像求出它的编码，要用贝叶斯法则，而分母里还是同一个积分。",

    'In 1995 Peter Dayan, Geoffrey Hinton, Radford Neal and Richard Zemel':
        "1995年，Peter Dayan、杰弗里·辛顿、Radford Neal和Richard Zemel提出了一个绕开贝叶斯法则的办法：把它学出来。"
        "给模型再配一个网络，一个识别模型q，它看着一张图像，猜出图像背后的隐藏原因。<bookmark mark='a'/>他们把它叫作亥姆霍兹机，"
        "以纪念赫尔曼·冯·亥姆霍兹，他把知觉描述为一种无意识的推断。<bookmark mark='b'/>它分两个阶段训练。醒着的时候，"
        "它看真实的图像，用q猜出原因，再训练生成网络从这些原因重现图像。<bookmark mark='c'/>睡着的时候，它做梦："
        "从自己的生成模型里抽出原因和图像，再训练q把原因找回来。<bookmark mark='d'/>它管用，但很别扭。识别网络是从梦里学的，"
        "而不是从数据里学的；两个阶段优化的也不是同一个目标。18年后，修正它的是一个下界。",

    'Here is the bound. Start from the log-probability of an image':
        "这就是那个下界。从一张图像的对数概率出发，也就是那个算不出来的、对编码的平均。<bookmark mark='a'/>在里面同时乘以和除以识别网络的猜测，"
        "给定x时z的q，这样积分就变成了对从q里抽出的编码求平均。<bookmark mark='b'/>平均值的对数，至少是对数的平均值："
        "这是詹森不等式，因为对数是凹函数。<bookmark mark='c'/>整理一下，就剩两项。第一项把从q里抽出的编码解码，再给图像打分："
        "这是重建。第二项是从q到先验的KL散度：编码偏离普通噪声有多远，也就是编码关于x携带了多少奈特的信息，即它的码率。"
        "两项合起来，就是证据下界，ELBO。<bookmark mark='d'/>而差距，恰好是从q到真实后验的KL散度。抬高这个下界，"
        "就同时做了两件事：改进了模型，也让q成了更好的猜测者。一个目标，取代了亥姆霍兹机的两个。",

    'One problem remains: the reconstruction term averages over random codes':
        "还剩一个问题：重建项是对随机编码求平均，而你没法对掷硬币求梯度。<bookmark mark='a'/>出路是把随机性挪个地方。"
        "编码器输出一个均值和一个幅度；编码等于均值，加上幅度乘以一份新抽的高斯噪声。<bookmark mark='b'/>现在噪声只是另一个输入，"
        "重建项的梯度可以穿过均值和幅度，流回编码器。这就是重参数化技巧。<bookmark mark='c'/>而对高斯分布来说，KL项有闭式解，"
        "是对编码各个维度的一个求和。<bookmark mark='d'/>2013年12月，Diederik Kingma和Max Welling发表了这个方法；"
        "几周之后，Danilo Rezende、Shakir Mohamed和Daan Wierstra独立地发表了同样的方法：这就是变分自编码器。"
        "叫自编码器，是因为编码器和解码器把每张图像都挤过一个编码；叫变分，是因为编码是一个分布，而损失是一个变分下界。",

    'f"Ours is small.':
        "我们的模型很小。一个两层的编码器，为16个编码数中的每一个给出均值和幅度；一个两层的解码器，为每个像素给出一个平滑的钟形分布，"
        "切成16个灰度级，这是从PixelCNN++借来的技巧。总共{p:,}个参数。<bookmark mark='a'/>因为解码器给每个灰度级都分配了真正的概率，"
        "ELBO就是一个和PixelCNN的精确似然单位相同的下界，都是每像素比特数，两者可以直接比较。",

    # ------------------------------------------------------------------ VAE
    'Chapter four. Training a VAE':
        '第4章。训练VAE：码率、失真与坍缩。',

    'f"Here is our VAE learning.':
        "这是我们的VAE的学习过程。下界的两项，单位是留出数字上的每个数字多少奈特：重建，以及码率。<bookmark mark='a'/>一开始，"
        "解码器什么都不知道，重建要花掉每个数字{r0:.0f}奈特，而码率是{k0:.1f}：编码还什么都没说。<bookmark mark='b'/>"
        "然后编码器开始说点什么，码率上升，重建变清晰：模型用信息换来了准确。<bookmark mark='c'/>到最后，"
        "编码关于每个数字携带{k1:.1f}奈特，解码器还需要{r1:.0f}奈特来描述其余部分。换成每像素比特数，下界是{e_b[0]:.2f}；"
        "一个更紧的估计，对每个数字平均64个编码，给出{iw[0]:.2f}。<bookmark mark='d'/>从普通噪声经过解码器抽出的样本，是数字，"
        "只是带着柔和的模糊。而且16个编码数里，最后只有{act}个携带信息；其余的都关掉了，这是本章后面要讲的现象的第一个苗头。",

    'What does the code learn? Give the VAE only two numbers per digit':
        "编码学到了什么？让VAE每个数字只用两个数，我们就能看见。每个点是一个留出的数字，放在它编码的均值处，按它是哪个数字上色。"
        "<bookmark mark='a'/>一开始，每个数字都待在原点。随着训练进行，编码器把它们铺开，同一种数字聚到了一起，尽管没有人告诉它标签。"
        "KL项让整团点挤在原点周围，大致是个高斯。<bookmark mark='b'/>把一个均匀的编码网格解码出来，就得到模型的数字地图："
        "1在一块区域，0在另一块，中间是平滑的过渡，比如一个7慢慢变成9。",

    'f"The two terms pull against each other':
        "这两项互相拉扯，而一个数决定了它们之间的汇率。给KL项乘上一个权重β：DeepMind的Irina Higgins和同事把它叫作β-VAE。"
        "<bookmark mark='a'/>我们在6个β值上训练了它，从{betas[lo]:g}到{betas[hi]:g}，每个两个种子，用的是四分之一的预算。"
        "每个点是一次训练：编码携带多少奈特，对比解码器还需要多少奈特。<bookmark mark='b'/>{trend}β为{betas[lo]:g}时，"
        "编码携带{R[lo].mean():.0f}奈特，有{int(round(A[lo].mean()))}个编码数是活跃的；β为{betas[hi]:g}时，"
        "是{R[hi].mean():.0f}奈特和{int(round(A[hi].mean()))}个。<bookmark mark='c'/>样本显示了这种取舍：β大时，"
        "画出的是平滑、千篇一律的数字，因为编码说的已经不足以确定细节了。Higgins还发现，大的β会促使每个编码数去控制图像的一个因素，"
        "比如物体的位置，或者一张脸的角度。",

    'Every step up in beta lowers the rate':
        'β每升高一级，码率就降低、失真就升高：这些训练连成了一条曲线，也就是信息论里的码率-失真权衡。',

    'Overall, raising beta lowers the rate':
        '总体上，升高β会降低码率、升高失真，虽然不是每一级都如此：这些训练散布在一条曲线周围，也就是信息论里的码率-失真权衡。',

    'f"Those switched-off code numbers have a name':
        "那些被关掉的编码数有个名字：后验坍缩，而我们可以故意让它发生。拿双月，配一个编码只有两个数的VAE。给其中一个版本的解码器，"
        "让它分别从编码预测x1和x2。<bookmark mark='a'/>双月的形状里，x2依赖于x1，所以要得到这个形状，它就必须用上编码，"
        "它也确实用了：它的码率稳定在每个点{fk:.2f}奈特，三个种子都是如此。<bookmark mark='b'/>现在把第2章的本事交给解码器："
        "用编码和x1一起来预测x2。<bookmark mark='c'/>{verdict}",

    'f"The autoregressive decoder\'s rate falls to {ak:.3f} nats, in every seed':
        '自回归解码器的码率降到了{ak:.3f}奈特，每个种子都是：编码坍缩了。每个点都被编码成原点上同一团东西，解码器独自建模了双月。',

    'f"The autoregressive decoder\'s rate falls to {ak:.2f} nats, against {fk:.2f}':
        '自回归解码器的码率降到了{ak:.2f}奈特，对比{fk:.2f}：编码几乎没被用上。',

    'f"Why would a model give up its code?':
        "模型为什么会放弃它的编码？因为编码要花码率，而如果解码器自己就能建模数据，就没有什么来为它买单。2016年，Samuel Bowman和同事"
        "在一个句子VAE上就撞上了这个问题：语言模型解码器学会了完全忽略编码。<bookmark mark='a'/>{first}<bookmark mark='b'/>"
        "{second}<bookmark mark='c'/>{third}解决办法是让编码物有所值：用一个更弱的解码器，给码率设一个下限，"
        "或者把KL的权重慢慢调上去。",

    'f"With a PixelCNN as its decoder, the VAE\'s rate climbs briefly':
        '用PixelCNN做解码器，VAE的码率短暂上升，然后沉到了每个数字{kp:.1f}奈特，而普通VAE是{kv:.1f}。解码器自己就能画出数字，所以编码大多被忽略了。',

    'f"With a PixelCNN as its decoder, the VAE\'s rate ends at':
        '用PixelCNN做解码器，VAE的码率最后是每个数字{kp:.1f}奈特，而普通VAE是{kv:.1f}：强大的解码器对编码的依赖少得多。',

    "f'Decode four digits from one code, and only":
        '从同一个编码解码出四个数字，只有{pa:.0f}%和被编码的那张图像是同一个数字。',

    "f'Decode four digits from one code, and {pa:.0f} percent":
        '从同一个编码解码出四个数字，仍有{pa:.0f}%和被编码的那张图像是同一个数字。',

    "f'Free bits, a floor of":
        '自由比特，也就是每个编码数{fbits:g}奈特的下限，低于它的KL不计代价，能让编码里留住{kf:.1f}奈特，解码出的数字有{pf:.0f}%和来源相符。',

    'f"One more thing to see.':
        "还有一件事要看。在八个窄高斯组成的环上，VAE把样本撒进了各个峰之间的空隙：三个种子平均下来，只有{100 * q:.0f}%"
        "落在某个峰的三倍标准差以内。<bookmark mark='a'/>高斯解码器加上平滑的编码，会把一切锐利的东西都抹模糊；在图像上，"
        "这就是VAE出了名的柔和。<bookmark mark='b'/>修正这一点的办法，各自成了一个研究方向：更深的多层编码，"
        "本部分最后会讲到的离散编码，以及每个潜扩散模型前面的那个自编码器。",
}

PHRASES = {}

ZH.update({
    # ------------------------------------------------------------------ Game
    'Chapter five. The adversarial game.':
        '第5章。对抗博弈。',

    'The third answer throws the likelihood away.':
        "第三个答案把似然扔掉了。2014年，伊恩·古德费洛和蒙特利尔约书亚·本吉奥实验室的同事，让两个网络互相对抗。<bookmark mark='a'/>"
        "生成器把随机噪声变成一个样本；它从来看不到数据。<bookmark mark='b'/>判别器看一个样本，真的或者生成的，"
        "输出它是真的的概率。<bookmark mark='c'/>判别器被训练去分辨两者，生成器被训练去骗过它；论文里打的比方，"
        "是一伙造假币的人对抗警察。写成一个值：判别器最大化它在两种样本上判断正确的对数概率，生成器则最小化它。",

    'What does the discriminator learn, if it wins?':
        "如果判别器赢了，它学到的是什么？把这个值写成对x的积分，用q表示生成器的分布。<bookmark mark='a'/>在每个x上分别来看，"
        "判别器选一个数D(x)，去最大化a乘log D加上b乘log(1减D)。令导数为零。<bookmark mark='b'/>最好的判别器是p除以p加q："
        "x处的概率里属于数据的那一份。<bookmark mark='c'/>数据占主导的地方，它说真；生成器占主导的地方，它说假；两者相当的地方，它说一半。",

    'Now put the best discriminator back into the value.':
        "现在把最好的判别器代回这个值。<bookmark mark='a'/>在每个对数里，把p加q除以2，就出现了两个KL散度，分别从p和从q到它们的平均m，"
        "再减去log 4。<bookmark mark='b'/>两者合起来，就是詹森-香农散度：对称，最大不超过log 2，并且恰好在q等于p时为零。"
        "<bookmark mark='c'/>所以，面对一个完美的评判者，生成器是在最小化自己的分布和数据分布之间的一个散度，"
        "却从来不需要写下一个密度。这就是2014年那篇论文的定理。至于训练是否真能找到这个最小值，是另一个问题，"
        "也就是本章余下部分和下一章的内容。",

    'f"The first practical problem appears on day one.':
        "第一个实际问题，在第一天就出现了。训练初期，假样本很差，判别器很有把握地拒绝它们，D(G(z))停在零附近。<bookmark mark='a'/>"
        "在那里，极小极大损失log(1减D)是平的：生成器在最需要梯度的时候，几乎得不到梯度。<bookmark mark='b'/>"
        "古德费洛在同一篇论文里的修正，是翻转生成器的目标：不再最小化被抓住的概率，而是最大化骗过对方的概率，也就是负log D。"
        "不动点不变，而在原来平的地方，它很陡。<bookmark mark='c'/>{meas}<bookmark mark='d'/>但这个修正有代价，"
        "2017年由Martin Arjovsky和Léon Bottou发现：它的梯度，是一个反向KL散度减去詹森-香农项的梯度。反向KL几乎不惩罚漏掉一个峰，"
        "却重罚把概率放到数据没有的地方。",

    'f"Measured on the ring, in the first steps of training':
        '在环上测量，训练的最初几步里，非饱和生成器的梯度是极小极大生成器的{ratio:.1f}倍。',

    "f'Measured on the ring, in the first steps, the two gradients":
        '在环上测量，最初几步里，两者的梯度相差不到{fac:.1f}倍：我们的判别器在早期从来没有自信到让这个差别显现出来。',

    '"Here is that cost on the ring of eight.':
        "这就是那个代价在八峰环上的样子。背景是判别器对平面的判决，它说真的地方亮；点是生成器的样本，"
        "每个检查点都用同样的300个噪声向量。{pick}<bookmark mark='a'/>看它训练。{hop}<bookmark mark='b'/>"
        "这就是模式坍缩：一个生成器只会做几种东西。<bookmark mark='c'/>{cmp_}",

    "f'Here is the run, of five, that ended with the fewest modes":
        '这是五次训练里，最后覆盖的峰最少的那一次：种子{seed}。五次里有{n_col}次在不同程度上坍缩了。',

    'It covers a few modes at a time':
        '它一次只覆盖几个峰，而覆盖的是哪几个，一直在变：生成器追着判别器最薄弱的地方跑，判别器跟着追过去。',

    'At times it reaches all eight, then loses some again':
        '它有时会覆盖全部八个峰，然后又丢掉几个：生成器追着判别器最薄弱的地方跑，判别器跟着追过去。',

    "f'Over five seeds, the non-saturating GAN ends with {mean_ns:.1f} of the eight modes on average, and covers":
        '五个种子里，非饱和GAN最后平均覆盖八个峰中的{mean_ns:.1f}个，其中{full_ns}次覆盖了全部八个；极小极大损失有梯度问题，'
        '但没有反向KL，最后平均覆盖{mean_mm:.1f}个，全部八个的有{full_mm}次。Adam会放大小的梯度，在这里救了极小极大损失，'
        '于是反向KL的效果就显露出来了。',

    "f'Over five seeds, the non-saturating GAN ends with {mean_ns:.1f} of the eight modes on average, all eight":
        '五个种子里，非饱和GAN最后平均覆盖八个峰中的{mean_ns:.1f}个，全部八个的有{full_ns}次；极小极大损失平均{mean_mm:.1f}个，'
        '全部八个的有{full_mm}次。',

    # ------------------------------------------------------------------ Dynamics
    'Chapter six. Why GANs spiral.':
        '第6章。GAN为什么会绕圈。',

    'Here is the smallest game there is.':
        "这是能有的最小的博弈。一个玩家选x，希望x乘y小；另一个玩家选y，希望它大。均衡点是原点。<bookmark mark='a'/>"
        "每个玩家都沿着自己的梯度走：x按负y变化，y按正x变化。<bookmark mark='b'/>把这些速度画出来，哪里都没有下坡。"
        "这个场绕着均衡点旋转，就像水绕着一个没有洞的排水口打转。<bookmark mark='c'/>它的雅可比矩阵的特征值是正负i："
        "纯粹的旋转。梯度下降是为山谷设计的。而一个博弈，在均衡点附近，可能是一个漩涡。",

    'f"Now take actual steps, both players at once':
        "现在真正走几步，两个玩家同时走，步长为η。每一步都把这个点乘以这个矩阵。<bookmark mark='a'/>它的特征值的大小是1加η平方的平方根："
        "大于1，所以每一步都往外走。<bookmark mark='b'/>同时的梯度步，盘旋着离开均衡点；走了{T}步之后，半径变成了原来的{rs[-1]:.1f}倍。"
        "<bookmark mark='c'/>让两个玩家轮流走，螺旋就闭合成一条轨道：既不逃走，也不到达；它的半径最后是{ra:.2f}。<bookmark mark='d'/>"
        "要真正收敛，就得往前看。外梯度法先试走一步，再用那里的梯度；乐观梯度下降则根据上一步的梯度做外推。两者都盘旋着向内收，"
        "半径分别缩到{re_:.2f}和{ro:.2f}。",

    'Real GANs do this. Lars Mescheder':
        "真实的GAN也会这样。Lars Mescheder、Andreas Geiger和Sebastian Nowozin把一个GAN简化成两个数：数据是零处的一个点，"
        "生成器是θ处的一个点，判别器是一条过原点、斜率为ψ的直线。<bookmark mark='a'/>均衡点是θ和ψ都为零，在它周围，"
        "场还是同样的旋转。<bookmark mark='b'/>同时走的步子盘旋向外；<bookmark mark='c'/>轮流走的步子永远绕圈。<bookmark mark='d'/>"
        "他们的修正是：惩罚判别器在真实数据上的梯度，在这里就是γ的一半乘ψ平方。这个惩罚就是摩擦。螺旋现在向内收，"
        "收到了均衡点。StyleGAN训练时用的正是这个惩罚，R1。",

    'f"Back to the ring. Each row is one of its eight modes':
        "回到环上。每一行是它的八个峰之一，每一列是一个检查点，亮度表示有多少生成器的样本落在那个峰上。<bookmark mark='a'/>"
        "{tour}亮带从一个峰游荡到另一个峰：和那个玩具博弈是同样的旋转，只是现在发生在分布构成的空间里。<bookmark mark='b'/>"
        "多年来，实践者用梯度惩罚、往前看的步子、两个玩家各自的学习率，以及判别器各层的谱归一化，来对付这个问题。",

    "f'Over training the generator visits {visited} of the modes":
        '训练过程中，生成器到过{visited}个峰，但同时最多只覆盖{best}个；最后它覆盖了{last}个。',

    "f'Over training the generator visits all eight modes":
        '训练过程中，生成器到过全部八个峰，有时还同时覆盖了全部，但都不长久；最后它覆盖了{last}个。',

    # ------------------------------------------------------------------ Wasserstein
    'Chapter seven. Wasserstein GANs.':
        '第7章。瓦瑟斯坦GAN。',

    'f"Martin Arjovsky, Soumith Chintala and Léon Bottou asked':
        "Martin Arjovsky、Soumith Chintala和Léon Bottou问了这样一个问题：当两个分布不重叠时，詹森-香农散度会怎样？"
        "对图像来说，它们都躺在一个巨大空间里的薄片上，这正是常态。他们的例子是：数据是x等于零处的一条竖直线段，"
        "模型是平移到θ处的同一条线段。<bookmark mark='a'/>只要θ不为零，两者就不重叠，JS散度就是log 2，不管θ是多少。"
        "一条平线没有梯度：它没法告诉你θ正在靠近。<bookmark mark='b'/>我们在17个θ值上训练判别器来检验：它的估计值都在log 2的"
        "{js_err:.2f}以内。<bookmark mark='c'/>一个衡量概率质量要搬多远的距离，恰好补上了缺的东西：一个V字形，斜率总是指向家。"
        "训练出来的评判器在θ等于{th[k]:.2f}处，把它估计为{w[k]:.2f}。",

    "That distance is the earth mover's distance.":
        "这个距离就是推土机距离。把p想成一堆沙子，把q想成一个同样体积的坑。<bookmark mark='a'/>一个运输方案规定从每个地方运多少沙子到"
        "每个别的地方；它的代价是运的量乘以运的距离。<bookmark mark='b'/>瓦瑟斯坦-1距离，就是最便宜的方案的代价。加斯帕尔·蒙日在1781年"
        "为搬运土方提出了这个问题；列昂尼德·康托罗维奇在1942年给出了它的现代形式，后来还因资源配置理论分享了诺贝尔经济学奖。",

    'Computing a cheapest plan between distributions of images is hopeless':
        "在图像的分布之间求最便宜的方案是没有希望的，但这个距离还有第二种描述。根据康托罗维奇和鲁宾斯坦的对偶，"
        "它等于任何一个处处斜率不超过1的函数，在p和q之间所能拉开的最大期望差距。<bookmark mark='a'/>所以，把判别器换成一个评判器f，"
        "它的输出可以是任意数而不是概率，训练它去拉开这个差距，再训练生成器去缩小它。<bookmark mark='b'/>难处在于让评判器的斜率不超过1。"
        "第一版瓦瑟斯坦GAN干脆把每个权重都截断到一个小方框里。<bookmark mark='c'/>Ishaan Gulrajani和同事注意到，最优的评判器沿着真假点之间的"
        "连线，斜率恰好是1，于是就在那里惩罚斜率偏离1的程度：这就是WGAN-GP。",

    'f"Back to the ring, with the same two networks':
        "回到环上，用同样的两个网络，同样多的生成器步数。背景现在是评判器：不是概率，而是一片地形，数据所在的地方高。"
        "<bookmark mark='a'/>看生成器的样本沿着评判器的地形往上爬，爬向各个峰。<bookmark mark='b'/>{verdict}<bookmark mark='c'/>{sharp}",

    "f'Its samples are less tightly placed, though":
        '不过，它的样本落得没那么准：{qw:.0f}%落在某个峰的三倍标准差以内，而非饱和GAN是{qn:.0f}%。',

    "f'And {qw:.0f} percent of its samples":
        '它的样本里有{qw:.0f}%落在某个峰的三倍标准差以内。',

    "f'Over five seeds, WGAN-GP ends with {mw:.1f} of the eight modes on average, all eight":
        '五个种子里，WGAN-GP最后平均覆盖八个峰中的{mw:.1f}个，有{full_w}次覆盖了全部八个；相比之下，非饱和GAN是{mn:.1f}个，'
        '极小极大GAN是{mm:.1f}个。一个衡量距离的评判器，会一直把生成器拉向它还缺的每一个峰。',

    'f"Over five seeds, WGAN-GP ends with {mw:.1f} of the eight modes on average, against':
        '五个种子里，WGAN-GP最后平均覆盖八个峰中的{mw:.1f}个，相比之下，非饱和GAN是{mn:.1f}个，极小极大GAN是{mm:.1f}个：'
        '在这个环上，评判器的距离并没有换来更好的覆盖。',

    'f"The cure has a price.':
        "这个疗法有代价。WGAN-GP每走一步生成器，都要训练评判器五次，而它的惩罚项还需要对评判器再做一次反向传播。<bookmark mark='a'/>"
        "在我们的数字模型上一次运算一次运算地数，WGAN-GP的一步，相当于GAN一步的{ratio:.1f}倍，<bookmark mark='b'/>"
        "所以在同样的预算下，GAN走了{sg:,}步生成器，WGAN-GP只走了{sw:,}步。第15章我们会看到，这在数字上换来了什么。",
})

ZH.update({
    # ------------------------------------------------------------------ Scale
    'Chapter eight. GANs at scale':
        '第8章。规模化的GAN：BigGAN、StyleGAN与反演。',

    'f"First, ours. A generator and a discriminator':
        "先看我们自己的。一个生成器和一个判别器，各是一个两层网络，在数字上训练。右边是生成器在每个检查点，用同样16个噪声向量画出的东西。"
        "<bookmark mark='a'/>先是一团团的，然后有了笔画，然后是数字。<bookmark mark='b'/>左边是两个损失。它们不像学习曲线那样下降："
        "它们彼此平衡，一方的进步抵消了另一方的。{bal}这些曲线里，没有任何东西告诉你生成器什么时候变好了。这正是GAN需要第14章那些"
        "量尺的原因之一。",

    "The discriminator's loss settles close to two log two":
        '判别器的损失稳定在2 log 2附近，这是它只能像抛硬币一样乱猜时的值。',

    'f"The discriminator\'s loss ends at {dfin:.2f}':
        '判别器的损失最后是{dfin:.2f}，低于2 log 2：它仍然能把大多数假样本和真数字分开。',

    'From two-layer networks to photographs took four years.':
        "从两层网络到照片，用了四年。<bookmark mark='a'/>2015年，Alec Radford、Luke Metz和Soumith Chintala找到了能稳定训练的卷积结构，"
        "还发现噪声向量可以做算术：一个微笑的女人，减去一个女人，加上一个男人，得到一个微笑的男人。<bookmark mark='b'/>2017年，"
        "英伟达的Tero Karras和同事在训练过程中让网络逐渐长大，从4个像素一直长到1024个。<bookmark mark='c'/>2018年，Andrew Brock、"
        "Jeff Donahue和Karen Simonyan把一个按类别生成的GAN扩展到了ImageNet，用的是很大的批量和精心的正则化：在128像素上，"
        "Inception分数达到166.5，FID达到7.4，而此前的最好成绩是52.5和18.6。<bookmark mark='d'/>Karras的团队则把生成器本身重新做了一遍："
        "这就是StyleGAN。",

    "StyleGAN's generator doesn't start from the noise.":
        "StyleGAN的生成器不从噪声出发。它从一个学出来的常数出发，4个像素见方，然后一块一块地上采样。<bookmark mark='a'/>噪声先经过一个"
        "8层的映射网络，变成一个中间编码w。<bookmark mark='b'/>然后w为每一块设定一种风格：给每个通道一个缩放和一个平移。"
        "在每个分辨率上加入的新随机噪声，负责那些没人在意去控制的细节，比如头发和雀斑的确切位置。<bookmark mark='c'/>"
        "因为每个分辨率都有自己的风格，风格就可以混合：粗的那几层取自一张脸，决定姿态和脸型；细的那几层取自另一张脸，决定颜色和质感。"
        "而且w所在的空间，结果比z的空间有条理得多：在它里面走直线，就成了有意义的编辑，这让下一个想法得以实现。",

    '"BigGAN brought one more trick, the truncation trick':
        "BigGAN还带来了一个技巧，截断技巧：采样时，从一个更窄的分布里抽噪声，任何大于t的坐标都重新抽。这样生成器就待在它所学内容的中间地带。"
        "<bookmark mark='a'/>这是它在我们的GAN上的效果，用第14章的精确率和召回率来衡量。<bookmark mark='b'/>{verdict}"
        "<bookmark mark='c'/>{fid_s}",

    "f'The FID, which mixes both, is best at t of":
        '把两者混在一起的FID，在t等于{best[\'t\']:g}时最好。',

    'The FID, which mixes both, is best with no truncation at all.':
        '把两者混在一起的FID，在完全不截断时最好。',

    "f'At t of {t0['t']:g}, precision is {t0['precision']:.2f} and recall {t0['recall']:.2f}; untruncated, {t1['precision']:.2f} and {t1['recall']:.2f}. Fewer":
        "t等于{t0['t']:g}时，精确率是{t0['precision']:.2f}，召回率是{t0['recall']:.2f}；不截断时，是{t1['precision']:.2f}和"
        "{t1['recall']:.2f}。数字更少样、更典型：用多样性换来了逼真度。",

    'f"At t of {t0[\'t\']:g}, precision is':
        "t等于{t0['t']:g}时，精确率是{t0['precision']:.2f}，召回率是{t0['recall']:.2f}；不截断时，是{t1['precision']:.2f}和"
        "{t1['recall']:.2f}：在我们的小GAN上，这种取舍比BigGAN上的弱。",

    'f"A GAN has no encoder.':
        "GAN没有编码器。要用它来编辑一张真实的照片，你得先找到能产生这张照片的噪声向量。这就是GAN反演，最简单的做法是搜索："
        "从一个随机的z出发，对G(z)和图像之间的差做梯度下降。<bookmark mark='a'/>这是生成器从没见过的8个测试数字，以及搜索的过程，"
        "每个数字从4个随机起点出发，保留最好的，走了{steps[-1]}步。<bookmark mark='b'/>{cmp_}<bookmark mark='c'/>"
        "找到之后，这些编码就可以移动：在其中两个之间走一条直线，就能把一个数字渐变成另一个。在StyleGAN的w空间里，"
        "这成了编辑真实照片的工具，从2016年朱俊彦的iGAN，到2023年的DragGAN，后者只要拖动图像上的点，就能把它们挪走。",

    'f"Their average squared error per pixel is {ge:.3f}, against {ve:.3f} for the VAE\'s encoder, which':
        '它们每个像素的平均平方误差是{ge:.3f}，而VAE的编码器是{ve:.3f}；编码器一遍就给出答案，但它是另一个模型。',

    'f"Their average squared error per pixel is {ge:.3f}, against {ve:.3f} for the VAE\'s encoder in one pass':
        '它们每个像素的平均平方误差是{ge:.3f}，而VAE的编码器一遍就是{ve:.3f}：GAN能生成的范围，并不完全包含这些数字。',

    # ------------------------------------------------------------------ Flows
    'Chapter nine. Normalizing flows.':
        '第9章。归一化流。',

    'The fourth answer keeps the likelihood exact':
        "第四个答案既保留精确的似然，又只需一遍就能采样。从简单的噪声z出发，把它推过一个可逆函数g。<bookmark mark='a'/>g把直线拉长的地方，"
        "概率就摊薄；g把直线压缩的地方，概率就堆积起来。<bookmark mark='b'/>概率是守恒的：z的一小段区间里的概率质量，等于它的像里的质量。"
        "<bookmark mark='c'/>所以x的密度，等于产生它的那个z的密度，乘以逆映射把一小段区间缩小了多少。<bookmark mark='d'/>"
        "在多维情形下，这个因子是逆映射雅可比矩阵行列式的绝对值。对数似然是精确的；我们可以像训练自回归模型那样，用最大似然来训练。"
        "2010年Esteban Tabak和Eric Vanden-Eijnden描述了这样的流；2015年Danilo Rezende和Shakir Mohamed把它带进了深度学习。",

    'f"The catch is the determinant':
        "麻烦在于行列式：对一般的d乘d雅可比矩阵，它要花d的三次方次运算，而对一张图像，d有好几千。Laurent Dinh和约书亚·本吉奥"
        "找到了一条绕过去的路。把变量分成两半。<bookmark mark='a'/>前一半原样复制；<bookmark mark='b'/>后一半做缩放和平移，"
        "缩放量s和平移量t可以由任意网络从前一半算出来。<bookmark mark='c'/>这样雅可比矩阵就是三角形的：前一半不依赖于后一半。"
        "三角矩阵的行列式等于对角线的乘积，所以对数行列式就是所有s的和，不花任何代价。<bookmark mark='d'/>逆变换同样便宜："
        "减去t，再除以e的s次方。里面的网络从来不需要求逆。<bookmark mark='e'/>我们把自己的结果和自动微分算出的完整行列式对比过："
        "两者相差不到{sci(gap, 1)}奈特。把这样的层叠起来，轮流换哪一半被复制，流就能把任何东西弯过来。",

    'Here is that bending, for our flow on the two moons':
        "这就是那种弯曲，来自我们在双月上训练的流：8个耦合层。这些线是噪声平面上的一个方格网，这些点是噪声的样本。<bookmark mark='a'/>"
        "一层一层地看：每一层都沿一个坐标轴滑动这些点，滑动的量取决于它们在另一个坐标轴上的位置。<bookmark mark='b'/>网格被剪切、"
        "拉伸、折叠，却从不撕裂，也从不自相交叉，因为每一层都是可逆的。<bookmark mark='c'/>第8层之后，噪声变成了双月："
        "从噪声到样本只要一遍，而把同一个映射倒过来读，就给出每个点的精确概率。<bookmark mark='d'/>如果改在棋盘格上训练，"
        "同样的这些层就得用平滑的映射，把平面切成一个个方块。",

    'f"Training, replayed on the checkerboard':
        "在棋盘格上回放训练：流在每个检查点的密度。<bookmark mark='a'/>概率质量从空的格子里流出，流进有数据的格子，边缘慢慢变锐利。"
        "<bookmark mark='b'/>在留出点上，和每个分布的下限相比，流的意外度最后在双月上高出{gaps['moons']:.2f}奈特，在环上高出"
        "{gaps['ring']:.2f}，在棋盘格上高出{gaps['checker']:.2f}。{why_hard}",

    'The ring is the hardest: an invertible map':
        '环是最难的：一个可逆映射没法把一团噪声撕成八个分开的小岛，所以它在小岛之间拉出了一道道细细的概率之桥。',

    'The checkerboard is the hardest: a stack':
        '棋盘格是最难的：一串平滑的可逆映射，只能近似它的悬崖。',

    'The moons are the hardest of the three for it.':
        '对它来说，双月是三者中最难的。',

    'f"On digits, our flow is eight coupling layers':
        "在数字上，我们的流是作用在像素logit上的8个耦合层，这是它画出来的东西。<bookmark mark='a'/>有笔画，但带着噪声。"
        "把噪声调小，这是OpenAI的Glow用过的技巧，笔画就更干净，也更彼此相像：这是流的截断技巧。<bookmark mark='b'/>{verdict}"
        "<bookmark mark='c'/>2018年，Glow做出了能画人脸的流；此后多年，流一直落在其他家族后面。2024年，苹果的Shuangfei Zhai和同事"
        "用作用在图像块上的Transformer模块搭出了一个流，报告的样本质量可以和扩散模型相比：这是流第一次独自做到这一点。"
        "而流的连续版本，也就是下一章的内容，正是第21部分的流匹配所训练的东西。",

    "f'In bits per pixel the flow gets {mf:.2f} on held-out digits, against {mp:.2f} for the PixelCNN on the same budget: an exact":
        '在留出数字上，流的每像素比特数是{mf:.2f}，而在同样预算下，PixelCNN是{mp:.2f}：似然是精确的，但更差；耦合层把容量花在了保持可逆上。',

    "f'In bits per pixel the flow gets {mf:.2f} on held-out digits, against {mp:.2f} for the PixelCNN on the same budget: a better":
        '在留出数字上，流的每像素比特数是{mf:.2f}，而在同样预算下，PixelCNN是{mp:.2f}：似然比自回归模型还好。',

    # ------------------------------------------------------------------ NeuralODE
    'Chapter ten. Neural ODEs and continuous flows.':
        '第10章。神经ODE与连续流。',

    'A residual network, from Part 9, updates its state':
        "第9部分的残差网络，每一层都把它的状态更新一点点：h加上f(h)。<bookmark mark='a'/>把它读成常微分方程欧拉法的一步，"
        "步长为1。<bookmark mark='b'/>让步长缩到零，层就变成连续的了：状态沿着一个由网络定义的速度场流动。<bookmark mark='c'/>"
        "Ricky Chen、Yulia Rubanova、Jesse Bettencourt和David Duvenaud把它们叫作神经ODE，这篇论文获得了2018年NeurIPS的最佳论文奖。"
        "深度变成了时间，任何求解器都能对它积分，而让求解器倒着跑，就能求逆：这是一个流，不需要任何耦合层。",

    'How does the density change along the flow?':
        "密度沿着流是怎样变化的？走一小步，用上一章的变量替换：减去这一步雅可比矩阵的对数行列式，而这个雅可比矩阵是单位阵加上Δt乘以"
        "场的雅可比矩阵。<bookmark mark='a'/>对很小的一步，单位阵加一个小矩阵的行列式，在一阶近似下等于1加上它的迹。<bookmark mark='b'/>"
        "取极限：对数密度的变化率，等于负的场的雅可比矩阵的迹，也就是它的散度。流散开的地方，密度就下降。<bookmark mark='c'/>"
        "沿着路径积分，就得到连续流的精确对数似然，对网络完全没有任何限制。<bookmark mark='d'/>行列式变成了迹，而迹只需要雅可比矩阵的"
        "对角线。但即使是对角线，每个维度也要花一次反向传播。",

    'f"The way out is a trick from 1989':
        "出路是1989年的一个技巧，用来估计一个巨大矩阵的迹，而这个矩阵你只能拿来做乘法。抽一个随机向量ε，它的各个分量均值为0、方差为1，"
        "然后计算ε转置乘A乘ε。<bookmark mark='a'/>它的平均值，等于A的各个元素乘以ε i乘ε j的平均值，而后者在对角线上是1，"
        "在别处是0：这就是迹。一个随机探针，一次反向传播，一个无偏估计。这就是哈钦森估计量。<bookmark mark='b'/>它的方差取决于探针。"
        "用随机正负号时，方差比用高斯时小，因为对角线上的项从不变化。我们在一个训练好的流的400个点上测了两者，再和公式对比："
        "两者吻合，误差在{100 * rel_err:.0f}%以内，随机正负号的方差是高斯的{ratio:.2f}倍。<bookmark mark='c'/>2019年，"
        "Will Grathwohl和同事在它之上建立了FFJORD。维数越高，省下的越多：在{d_}维里，一个探针比精确的迹快{tr_ratio:.0f}倍，在这台电脑上。",

    'f"Here is a continuous flow trained on the two moons':
        "这是在双月上训练的连续流，两种方法，各三个种子：一种用精确的迹，一种每条路径只用一个随机正负号探针。两者都用同样的方式评判，"
        "也就是在留出点上用精确的迹。<bookmark mark='a'/>{verdict}在二维里，精确的迹反正很便宜：用它训练一次花了{te:.0f}秒，"
        "用估计花了{th:.0f}秒。到了一千维，就只有估计用得起了。",

    "f'The two end within {ag:.2f} nats":
        '两者最后相差不到{ag:.2f}奈特：带噪声的估计和精确的迹训练出的流一样好。',

    "f'The noisy estimate costs {ag:.2f} nats by the end.'":
        '到最后，带噪声的估计损失了{ag:.2f}奈特。',

    "f'The noisy estimate even ends {ag:.2f} nats ahead.'":
        '带噪声的估计最后甚至领先了{ag:.2f}奈特。',

    'And here is the flow itself.':
        "这就是流本身。时刻0时的700个高斯噪声点，被学到的场带到时刻1；下面是每个时刻的密度，用迹的积分算出来的。<bookmark mark='a'/>"
        "这团点被拉伸、分开、卷成两弯月亮，密度一路跟着它，始终守恒。<bookmark mark='b'/>还剩一个代价：训练时每一步都要正向、反向"
        "求解这个ODE。第21部分会展示怎样不付这个代价、用回归的方法学到同一种场：流匹配。",
})

ZH.update({
    # ------------------------------------------------------------------ Hopfield
    'Chapter eleven. Hopfield and Boltzmann.':
        '第11章。霍普菲尔德与玻尔兹曼。',

    'The fifth answer is the oldest.':
        "第五个答案是最古老的。1982年，物理学家约翰·霍普菲尔德描述了一个由二值神经元组成的网络，每个神经元取正1或负1，连接是对称的，"
        "他还给了它一个能量。<bookmark mark='a'/>每次一个神经元看看自己的输入，取它的符号。<bookmark mark='b'/>如果它翻转了，"
        "能量的变化就是负的翻转量乘以输入，而翻转的方向总是和输入的符号一致，所以能量只会下降。网络必然会落进一个山谷。"
        "<bookmark mark='c'/>要让选定的图案成为山谷，就用第9部分讲过的赫布规则来设置权重：在一个图案里同时亮着的神经元之间，"
        "得到一个正的连接。一段记忆，就存成了能量地形的谷底。",

    'f"Here is one, with 196 neurons':
        "这是一个这样的网络，有196个神经元，对应我们14乘14的像素，存了三个数字。<bookmark mark='a'/>从中间那个数字出发，"
        "把它四分之一的像素翻转过来。<bookmark mark='b'/>一个神经元接一个神经元，状态往下坡滑，右边的能量每变一次都在下降。"
        "<bookmark mark='c'/>{res}这种记忆是按内容寻址的：一份受损的副本就足以把它找回来。",

    "f'It settles on the stored digit exactly.'":
        '它恰好停在了存储的那个数字上。',

    "f'It settles on a state that matches":
        '它停在了一个状态上，和存储的数字有{100 * (1 + ov) / 2:.0f}%的像素相同。',

    'f"How much can it hold?':
        "它能存多少？存进随机图案，再用一份稍有损坏的副本去测试每一个。<bookmark mark='a'/>用{N}个神经元，回忆起初是完美的，"
        "然后崩溃：在我们的实验里，当每个神经元摊到{half:.2f}个图案时，能回来的已经不到一半。Daniel Amit、Hanoch Gutfreund和"
        "Haim Sompolinsky用自旋玻璃的物理算出了这个极限：大约每个神经元0.138个图案。<bookmark mark='b'/>数字的情况更糟，"
        "因为数字长得都很像：我们的数字两两之间的平均重叠是{mean_ov:.2f}，而随机图案之间几乎不重叠。{hebb_s}",

    'f"With Hebb\'s rule, recall already fails at':
        '用赫布规则，存到{n_fail}个数字时，回忆就已经失败了；再往后，山谷彼此合并，一个提示会滑进几段记忆的混合。',

    "Even so, with Hebb's rule all ten come back here":
        '即便如此，用赫布规则，这里10个数字都能回来；但再多一些，山谷就会合并，一个提示会滑进几段记忆的混合。',

    'f"The fix came more than thirty years later.':
        "修正来自三十多年以后。Dmitry Krotov和霍普菲尔德让能量变得更陡，Hubert Ramsauer和同事则把更新写成了一种你见过的形式："
        "把状态和每个存储的图案比较，对相似度取softmax，再返回这些图案的加权平均。<bookmark mark='a'/>用这个更新，我们的网络{res}。"
        "<bookmark mark='b'/>而这个更新，就是第13部分的注意力：状态是查询，存储的图案是键和值。在这个精确的意义上，"
        "Transformer的一个注意力层，就是一个只走一步的霍普菲尔德网络。",

    'recalls all ten digits from the same damaged cues':
        '从同样受损的提示里，回忆出了全部10个数字',

    "f'recalls {100 * hm[-1]:.0f} percent":
        '在存了全部10个数字时，回忆出了其中{100 * hm[-1]:.0f}%',

    "Hopfield's network is deterministic and has no hidden parts.":
        "霍普菲尔德的网络是确定性的，也没有隐藏的部分。1985年，David Ackley、杰弗里·辛顿和特伦斯·谢诺夫斯基让神经元变得随机，"
        "以一个由输入决定的概率打开，这样网络就按物理学里的玻尔兹曼分布对状态采样：概率等于e的负能量除以温度次方，再除以归一化常数Z。"
        "<bookmark mark='a'/>他们还加入了隐藏单元，数据从来不直接设定它们：这是机器自己的特征。<bookmark mark='b'/>它的学习规则很美。"
        "把可见单元钳在数据上，测量每一对单元同时打开的频率；再让机器自由运行，重新测一次；每个连接按两者之差加强。"
        "机器一直学，直到它的梦和这个世界有同样的统计。<bookmark mark='c'/>麻烦在于做梦：每次测量都需要网络达到平衡，"
        "而这可能要等到天荒地老。<bookmark mark='d'/>2024年，霍普菲尔德和辛顿分享了诺贝尔物理学奖，"
        "获奖理由是“为利用人工神经网络实现机器学习的基础性发现和发明”。",

    # ------------------------------------------------------------------ RBM
    'Chapter twelve. Contrastive divergence.':
        '第12章。对比散度。',

    'The way out of the dreaming problem was to restrict the machine.':
        "走出做梦难题的办法，是给机器加限制。把单元分成两层，可见层和隐藏层，每个可见单元都和每个隐藏单元相连，但同一层内不相连。"
        "保罗·斯莫伦斯基在1986年提出了它，叫它harmonium；今天它叫受限玻尔兹曼机。<bookmark mark='a'/>它的能量通过一个权重矩阵W"
        "把两层耦合起来。<bookmark mark='b'/>又因为隐藏单元彼此不相连，给定可见层，所有隐藏单元都是独立的：每一个都以它输入的sigmoid"
        "为概率打开。反过来也一样。<bookmark mark='c'/>我们的这台有196个可见单元，对应数字的每个像素，现在切成了黑白两色，"
        "只有16个隐藏单元，原因马上就会看到。",

    'To train it, sum the hidden units out.':
        "要训练它，先把隐藏单元求和消掉。一张图像的对数概率，等于负的自由能，再减去归一化常数Z的对数。<bookmark mark='a'/>"
        "自由能很好算：每个隐藏单元各自求和消掉，变成一个softplus。<bookmark mark='b'/>归一化常数是对每一张可能图像的求和，"
        "但它的梯度是模型下的一个平均。<bookmark mark='c'/>所以权重的梯度，又是玻尔兹曼机的那条规则：钳住数据时的相关性，"
        "减去模型自己产生的相关性。<bookmark mark='d'/>第一项是对批量求和。第二项需要从模型里采样，而要得到这些样本，"
        "仍然意味着要把一条马尔可夫链跑到平衡。",

    "Geoffrey Hinton's shortcut, in 2002, was to stop early.":
        "2002年，杰弗里·辛顿的捷径是：早点停。链不从噪声出发，而从一个训练数字出发。<bookmark mark='a'/>对隐藏单元采样，"
        "再从它们采出一张新图像，然后重复：k步吉布斯采样，受限的结构让它很快，一次就能处理一整层。<bookmark mark='b'/>"
        "把链走到的地方当作模型的样本。k等于1时它是有偏的，因为链几乎没动，但它能学，而且学得快。他把它叫作对比散度。"
        "<bookmark mark='c'/>2008年，Tijmen Tieleman做了改进：不要每次都把链重新放回数据上；保留一组链持续地跑，"
        "让它们随着模型的变化四处游走。",

    'f"Is contrastive divergence maximizing the likelihood?':
        "对比散度是在最大化似然吗？通常没人能检验，因为Z是对2的196次方张图像的求和。但Z也可以对隐藏状态求和，而只有16个隐藏单元时，"
        "隐藏状态只有6万5千多个。<bookmark mark='a'/>所以，这是训练过程中留出数字的精确对数似然，三种方法，各三个种子，"
        "更新次数相同。<bookmark mark='b'/>{verdict}<bookmark mark='c'/>{why_}",

    "f'Ranked by where they end:":
        '按最后的位置排名：{first}是每个数字{fin[order[0]]:.1f}奈特，接着是{second}，{fin[order[1]]:.1f}，然后是{third}，'
        '{fin[order[2]]:.1f}。',

    'One step of the chain is the cheapest estimate of the dreams':
        '链只走一步，是对梦最便宜、也最有偏的估计：它能学，但学到的不完全是对的东西。',

    'With only sixteen hidden units the model is simple enough':
        '只有16个隐藏单元时，模型足够简单，链哪怕只走一步，也是一个还算公允的估计。',

    'What does a Boltzmann machine learn?':
        "玻尔兹曼机学到了什么？把每个隐藏单元的权重画成一张图，就能看出让它打开的图案：这里是一台100单元机器中的40个，"
        "它想要墨迹的地方为正，想要白纸的地方为负；很多看起来像是笔画的片段。<bookmark mark='a'/>要做梦，就从随机像素出发，"
        "让链跑起来：这是它走了1步、10步、100步和1000步之后的样子，逐渐漂向机器认为可能的图像。<bookmark mark='b'/>"
        "只有16个单元时，我们可以做得比做梦更好：把全部6万5千多个隐藏状态精确地加权，一次就从真正的模型里采样。"
        "<bookmark mark='c'/>2006年，辛顿、Simon Osindero和Yee-Whye Teh把这样的机器堆叠起来，每一台都用下面那台的隐藏单元训练，"
        "做成了深度信念网络；深度学习的复兴就是从这里开始的，见第9部分。六年后，在GPU上直接做反向传播，让这种预训练变得不再必要，"
        "玻尔兹曼机也就淡出了。但它们的想法没有：一个能量，以及由一条链抽出的样本。",

    # ------------------------------------------------------------------ Langevin
    'Chapter thirteen. Langevin dynamics and the score.':
        '第13章。朗之万动力学与分数函数。',

    'f"Restricted Boltzmann machines are one case of a general idea.':
        "受限玻尔兹曼机，是一个更一般的想法的特例。任何输出单个数的网络，都可以当作能量，e的负能量次方除以它的积分Z，就是一个密度。"
        "对网络没有任何特殊要求：不用掩码，不用可逆，也不用编码。<bookmark mark='a'/>对数似然的梯度，还是那两个阶段："
        "降低数据的能量，抬高模型自己的样本所在之处的能量。<bookmark mark='b'/>在平面上，我们甚至可以在网格上把Z加出来，"
        "所以我们的环模型的似然是精确的：在留出点上是{nll:.2f}奈特，而下限是{h:.2f}。到了196维，任何网格都不管用，"
        "所以Z和样本都得另想办法。",

    "Sampling comes from physics.":
        "采样的办法来自物理。保罗·朗之万1908年的方程，描述了一个粒子在势场里往下坡漂移，同时被随机碰撞踢来踢去。写成算法就是："
        "沿着对数密度往上坡走一步，加一点高斯噪声，再重复。第5部分的福克-普朗克方程告诉我们，这样一个随机游走的分布最终停在哪里："
        "恰好就是p。<bookmark mark='a'/>这一步需要log p对x的梯度。对e的负E次方除以Z取对数：<bookmark mark='b'/>"
        "Z是一个常数，对每个x都一样，所以它的梯度是零。让训练变得困难的那个归一化常数，在采样里消失了。<bookmark mark='c'/>"
        "这个梯度有个名字，分数函数：密度上升最快的方向。这是我们的环模型的分数函数，箭头指向能量的八个山谷。",

    'f"So an energy model can be trained with its own Langevin chains.':
        "所以，一个能量模型可以用它自己的朗之万链来训练。维护一池子链；每一步取出一批，往下坡走{k_}步朗之万，降低真实点的能量，"
        "抬高链停下的地方的能量，再把它们放回池子。2019年，Yilun Du和Igor Mordatch让这种方法在图像上管用了。<bookmark mark='a'/>"
        "这是它在环上的样子。一开始能量是平的，链到处乱逛。然后在数据所在的地方出现了山谷，链掉了进去，而在链扎堆但没有数据的地方，"
        "能量升了起来。<bookmark mark='b'/>在留出点上，它最后比下限高出{gap:.2f}奈特。",

    'f"And sampling. Three hundred points of uniform noise':
        "然后是采样。在每个分布上放300个均匀噪声点，再在学到的能量上走朗之万步，一共{steps}步。<bookmark mark='a'/>点滑进山谷，"
        "在那里抖动，成了模型的一个样本。<bookmark mark='b'/>在环上，从噪声出发的长链，在三个种子里分别落在八个峰中的{modes[0]}个、"
        "{modes[1]}个和{modes[2]}个上。注意采样器从来不需要的东西：Z，或者对任何东西求逆。只需要分数函数。",

    'f"There is a catch, and it is the bridge to the next part.':
        "这里有一个陷阱，它也正是通向下一部分的桥。这是两个高斯，一个占20%的概率，一个占80%，它们的分数函数是精确已知的。"
        "<bookmark mark='a'/>均匀地撒下点，运行朗之万。<bookmark mark='b'/>每个点都掉进离它近的那个山谷，然后待在那里："
        "越过两者之间的空隙可能性太小，根本不会发生。所以重的那个峰里的样本比例是{100 * ph:.0f}%，这是由它们的起点决定的，"
        "起点里的比例是{100 * sh:.0f}%，而不是密度所说的80%。对于分开的几个峰，分数函数看不到它们的权重。<bookmark mark='c'/>"
        "2019年，宋飏和Stefano Ermon的修正是：先用大量噪声把密度模糊掉，山谷在那里合在一起，点可以自由移动；然后一级一级地调小噪声，"
        "一路跟着分数函数走。{verdict}<bookmark mark='d'/>要在图像上这样做，你需要数据在每个噪声水平上的分数函数，"
        "而它可以通过去噪学出来，这是Aapo Hyvärinen和Pascal Vincent证明的。这就是扩散，第21部分。能量本身也回来了："
        "2025年，均衡匹配学到了一个隐式的能量地形，沿着它往下走，生成了ImageNet图像。",

    "f'Annealing fixes it:":
        '退火修好了它：{100 * ah:.0f}%，接近真实值。',

    "f'Annealing moves it to":
        '退火把它变成了{100 * ah:.0f}%。',
})

ZH.update({
    # ------------------------------------------------------------------ Judging
    'Chapter fourteen. Judging a generator.':
        '第14章。怎样评判一个生成模型。',

    'How good is a generative model?':
        "一个生成模型有多好？显而易见的答案，是它在留出数据上的似然。2016年，Lucas Theis、Aaron van den Oord和Matthias Bethge"
        "说明了为什么这还不够。拿一个好模型，把它稀释：每一百个样本里只有一个来自好模型，其余全是噪声。<bookmark mark='a'/>"
        "它的对数似然最多下降log 100，也就是4.6奈特，对一张有几千个像素的图像来说，这只是个舍入误差。<bookmark mark='b'/>"
        "它的似然几乎一样好；它的样本却99%都是垃圾。似然和样本质量可以不一致。<bookmark mark='c'/>而GAN根本给不出似然。"
        "于是这个领域学会了直接评判样本。",

    'f"The standard measure since 2017':
        "自2017年以来的标准度量，是弗雷歇Inception距离，FID。它的核心是两个高斯之间的距离。在一维里，把一个高斯搬到另一个上最便宜的办法，"
        "是分位数对分位数地映射，而瓦瑟斯坦距离的平方，就等于均值之差的平方，加上幅度之差的平方。<bookmark mark='a'/>在多维里，"
        "幅度变成了协方差矩阵，幅度之差变成了这个带矩阵平方根的迹，这是Dowson和Landau在1982年给出的公式。<bookmark mark='b'/>"
        "Sepp Hochreiter团队的Martin Heusel和同事，不是把它用在像素上，而是用在一个训练好的分类器看到的特征上："
        "给真实图像的特征拟合一个高斯，给生成图像的特征拟合另一个，再算两者的距离。<bookmark mark='c'/>他们用的是谷歌的Inception网络，"
        "在ImageNet上训练。对数字，我们用同样的思路，换成一个在数字上训练的分类器，报告MNIST上FID的论文也是这么做的："
        "取它最后一个隐藏层，128个数；它读测试数字的准确率是{acc:.2f}%。",

    'f"First, a check that the measure measures something.':
        "首先，检查一下这个度量确实在量东西。{rise}一个3乘3的模糊得到{blur:.1f}。<bookmark mark='a'/>其次，一个警告。"
        "FID比较的是估计出来的均值和协方差，而用很少的样本做的估计有噪声，会让距离偏大。真实数字对测试集，用{n0}个样本时FID是{f0:.2f}，"
        "用{n2k:,}个时是{f2k:.2f}，用{nN:,}个时是{fN:.2f}。<bookmark mark='b'/>所以FID只能在样本数相同时比较。我们一律用{n2k:,}个，"
        "这把下限，也就是一个完美模型的得分，放在大约{f2k:.2f}。",

    "f'Add noise to real digits, and our FID rises with every step":
        '给真实数字加噪声，我们的FID随着噪声每升一级而上升，从{nf0:.2f}升到{nfN:.1f}。',

    "f'Add noise to real digits, and our FID rises, overall":
        '给真实数字加噪声，我们的FID总体上随噪声上升，从{nf0:.2f}升到{nfN:.1f}。',

    'f"One number can\'t say whether a model\'s samples are good':
        "一个数说不清，一个模型的样本是好，还是覆盖了数据，而这是两种不同的失败。Mehdi Sajjadi和同事，以及后来英伟达的"
        "Tuomas Kynkäänniemi和同事，把它拆成了两个。<bookmark mark='a'/>在每个真实点周围画一个球，半径到它第三近的真实邻居："
        "这些球合起来，估计出数据所在的地方。<bookmark mark='b'/>精确率，是落进真实球里的生成样本所占的比例：有多少假样本看起来是真的。"
        "<bookmark mark='c'/>召回率反过来：在生成样本周围画球，数一数它们盖住了多少真实点。<bookmark mark='d'/>"
        "这是第5章那个非饱和GAN在环上的结果：精确率{r0['precision']:.2f}，召回率{r0['recall']:.2f}。{verdict}",

    'High precision, low recall:':
        '精确率高，召回率低：它做出来的东西看起来是真的，但只覆盖了数据的一部分。',

    'The two numbers say different things':
        '两个数说的是不同的事，这正是要有两个数的原因。',

    'f"Now every family, on the ring':
        "现在是每个家族，在环上，各三个种子，对比两千个新抽的数据点。<bookmark mark='a'/>精确率最高的是{n_bp}，平均{v_bp:.2f}；"
        "召回率最高的是{n_br}，{v_br:.2f}；精确率最低的是{n_wp}，{v_wp:.2f}。<bookmark mark='b'/>这就是为什么只看FID很危险。"
        "给环拟合一个高斯团，均值和协方差都一样，再从它里面采样。它和环之间的弗雷歇距离是{bfd:.3f}，和环自己两份样本之间的距离差不多小，"
        "因为弗雷歇距离只看均值和协方差。它的精确率是{bprec:.2f}。在图像上，足够丰富的特征会让这种失败少见一些，但永远不会不可能。",

    'f"One failure no sample metric catches is memorization.':
        "有一种失败，任何样本指标都抓不到：死记硬背。一个只是重放训练数字的模型，得分会和真实数据一模一样：FID是{floor:.2f}，"
        "就在下限，精确率{rp:.2f}，召回率{rr:.2f}。<bookmark mark='a'/>所以我们直接检查：对每个样本，在6万个训练数字里找最近的一个。"
        "<bookmark mark='b'/>真实的测试数字，离它最近的训练数字的中位距离是{real_d:.3f}。{verdict}这类度量，以及来自比Inception"
        "更强的网络的特征，比如DINOv2，就是此后评估研究的方向。",

    'None of our models is copying:':
        '我们的模型都没有在抄：它们的样本离训练集的距离，和真实测试数字差不多。',

    'One of them sits suspiciously close to the training set:':
        '其中一个离训练集近得可疑：它可能在抄。',

    # ------------------------------------------------------------------ Budget
    'Chapter fifteen. Five models, one budget.':
        '第15章。五个模型，同一份预算。',

    'f"Now the five image models, side by side, on equal terms.':
        "现在，五个图像模型并排放在一起，条件对等。每一个都得到同样的算力预算，6万亿次浮点运算的训练，一次一次地数出来；"
        "每一个都从三个随机起点训练。<bookmark mark='a'/>算力对等，不等于其他一切都对等。卷积在每个像素上重复使用它的权重，"
        "所以PixelCNN的参数最少，而每个数字上的运算最多：它只看了{pex:.0f}千个训练数字，而{most_s}看了{mex:.1f}百万个。"
        "<bookmark mark='b'/>最后一列是抽一个样本的代价：除了PixelCNN需要196遍，每个模型都只要一遍。",

    'Here is what each one draws, seed zero':
        "这是每个模型画出的东西，都是种子0，前16个样本，没有挑选，旁边是真实数字。<bookmark mark='a'/>先看，再读数字："
        "哪个看起来最清晰，哪个最多样，哪个最像真正的手写？测量结果在后面。",

    'f"First, FID: the distance between our classifier\'s view':
        "第一，FID：我们的分类器眼中生成数字和真实数字之间的距离，各两千个。一个完美的模型大约会得{floor:.2f}，就是真实数字那条线。"
        "<bookmark mark='a'/>{lead}<bookmark mark='b'/>{pr}每个点是一个种子：种子之间的波动，也是结果的一部分。",

    "f'The lowest FID belongs to {n1}, {f1:.1f}, clearly ahead":
        'FID最低的是{n1}，{f1:.1f}，明显领先第二名{n2}的{f2:.1f}；最后一名是{nl}，{fl_:.1f}。',

    "f'The lowest FID belongs to {n1}, {f1:.1f}, though":
        'FID最低的是{n1}，{f1:.1f}，不过它的种子和第二名{n2}的{f2:.1f}有重叠；最后一名是{nl}，{fl_:.1f}。',

    "f'Split in two, the highest precision belongs to":
        '拆成两个数来看，精确率最高的是{nbp}，{vbp:.2f}；召回率最高的是{nbr}，{vbr:.2f}。',

    "f'Split in two, one model leads on both:":
        '拆成两个数来看，一个模型两项都领先：{nbp}，精确率{vbp:.2f}，召回率{R[bp]:.2f}。',

    'f"Second, likelihood, for the three families that have one':
        "第二，似然，只看有似然的那三个家族，单位是留出数字上的每像素比特数：PixelCNN是精确值，VAE和流是上界。<bookmark mark='a'/>"
        "最好的是{b1}，每像素{v1:.2f}比特，然后是{b2}，{v2:.2f}，再然后是{b3}，{v3:.2f}。<bookmark mark='b'/>{cmp_}",

    'Compare the FID ranking: it is not the same.':
        '对比一下FID的排名：它们不一样。正如Theis和同事所警告的，一个模型可以概率算得好，图却画得差，或者反过来。',

    'Here the likelihood ranking and the FID ranking agree':
        '在这里，对这三个模型，似然的排名和FID的排名一致；但它们并不一定一致。',

    'f"Third, a coarse but telling check:':
        "第三，一个粗略但很说明问题的检查：每个模型画的是哪些数字？分类器给每个模型的两千个样本打上标签，而真实数据里，"
        "每个数字大约占十分之一。<bookmark mark='a'/>{msg}在整个类别这个尺度上的模式丢失，是最容易看出来的失败。<bookmark mark='b'/>"
        "所以，在这个小尺度、同一份预算下：每个家族都有所长，没有一个样样都赢。似然模型对数据描述得最好；对抗模型画得怎样和它得分怎样，"
        "是两回事；而哪个最好，取决于模型是拿来做什么的。",

    "f'The most uneven is {nw}:":
        '最不均匀的是{nw}：它最少见的数字是{wk}，只占它样本的{mw:.1f}%，而真实数据里大约是10%。最均匀的是{nf_}，'
        '它最少见的数字也还有{mf:.1f}%。',

    # ------------------------------------------------------------------ Meet
    'Chapter sixteen. Where the families meet.':
        '第16章。几个家族的交汇。',

    'For six years GANs drew the sharpest images.':
        "六年里，GAN画出的图像最清晰。2021年，OpenAI的Prafulla Dhariwal和Alex Nichol发表了一篇论文，标题就说明了发生的事："
        "扩散模型在图像合成上打败了GAN。<bookmark mark='a'/>在256像素的ImageNet上，最好的GAN，BigGAN-deep，FID是6.95；"
        "他们带引导的扩散模型，是4.59。<bookmark mark='b'/>精确率和召回率说明了原因：GAN的精确率最高，但召回率只有0.28。"
        "它画出的是世界里一个狭窄切片的逼真图像。扩散模型覆盖的范围几乎是它的两倍。<bookmark mark='c'/>原因正是本部分遇到过的那些："
        "一个似然式的目标，漏掉每个峰都要付代价；一个稳定的回归，而不是一场博弈；以及一个随着规模变大不断改进的配方。",

    'Meanwhile the families had started to combine.':
        "与此同时，几个家族已经开始结合。2017年，Aaron van den Oord、Oriol Vinyals和Koray Kavukcuoglu给VAE配了一个离散编码。"
        "<bookmark mark='a'/>编码器输出的每个向量，都被吸附到一个学出来的码本里最近的那一项上，于是一张图像变成了一个整数网格：词元。"
        "梯度直接跳过这个吸附步骤，直通过去。<bookmark mark='b'/>没有后验坍缩，因为编码的大小是固定的；而在这些词元之上，"
        "一个自回归模型，一个PixelCNN，学出先验。<bookmark mark='c'/>2021年，VQGAN加了一个GAN损失让解码器更清晰，"
        "并在词元之上用了一个Transformer；同一年，DALL-E用一个Transformer同时写文本词元和图像词元。用VAE做出词元，用GAN让它们好看，"
        "再用自回归模型把它们写出来：这就是今天图像和视频系统的前端，第22部分和第23部分会把它打开来看。",

    'f"We built a small one.':
        "我们做了一个小的。编码器把我们的每个数字变成一个7乘7的词元网格，每个词元是{K}个码本项之一，解码器再把网格变回一个数字。"
        "<bookmark mark='a'/>重建保留了每个数字的身份和大部分形状。码本的困惑度是{perp:.1f}：实际上，它的{K}项里大约有这么多在被使用。"
        "<bookmark mark='b'/>直接写下来，一个网格是{rawb:.0f}比特；一个在训练数字的词元上训练的小Transformer，只用{prb:.0f}比特"
        "就能预测它们。<bookmark mark='c'/>从Transformer里采样词元，再解码，就画出了新的数字。{verdict}",

    "f'Its samples score an FID of {vfid:.1f}, better":
        '它的样本FID是{vfid:.1f}，比上一章五个单一模型都好，不过它是在那份预算之外训练的。',

    "f'Its samples score an FID of {vfid:.1f}; the best":
        '它的样本FID是{vfid:.1f}；上一章最好的单一模型是{bfid:.1f}，而这一个是在那份预算之外训练的。',

    'Autoregressive image models had one more trick to learn.':
        "自回归图像模型还要再学一个技巧。像PixelCNN那样按阅读顺序写词元，很慢，而且对图像来说是个奇怪的顺序。2024年，"
        "字节跳动和北京大学的Keyu Tian和同事改变了“下一个”指的是什么：不是下一个词元，而是下一个尺度。<bookmark mark='a'/>"
        "先是整张图像的一个词元；然后是一个2乘2的图；然后是越来越大的图，每一张都一次性地预测出来，条件是之前所有更粗的图。"
        "<bookmark mark='b'/>在256像素的ImageNet上，他们的模型达到了1.73的FID，而同样的词元按光栅顺序写时是18.65，快了大约20倍，"
        "这篇论文获得了NeurIPS 2024的杰出论文奖。第22部分会在它的基础上继续讲。",

    "And the GAN didn't die.":
        "而GAN并没有死。扩散模型的弱点是速度：每张图像要过几十遍网络，而生成器只要一遍。为了找回一步生成，人们把扩散模型蒸馏成生成器，"
        "而最好的蒸馏方法都用了判别器。<bookmark mark='a'/>Stability AI的Axel Sauer和同事，用GAN损失加一个扩散教师，训练出了"
        "一到四步就能出图的SDXL-Turbo，后来又做了SD3-Turbo，它的判别器本身就是用扩散模型搭的。<bookmark mark='b'/>"
        "Tianwei Yin和同事的DMD2加了一个作用在真实图像上的GAN损失，在小尺寸的ImageNet图像上一步就达到了1.28的FID。"
        "<bookmark mark='c'/>GAN本身也被重建了：R3GAN，一个现代的基线，有原则性的损失和收敛保证。家族之间的界线越来越模糊："
        "一致性模型两步就达到扩散模型的质量；2026年，何恺明的团队训练出一步生成器，方法是在训练中让它们的样本漂移到数据上，"
        "在ImageNet上的FID是1.54。",

    'So this is where the four answers, and the fifth, ended up.':
        "这就是那四个答案，以及第五个，最后的归宿。<bookmark mark='a'/>VAE和GAN变成了分词器和潜空间，每个图像和视频模型都从它们出发。"
        "自回归模型写出那些词元，一次一个尺度，或者一次一个词元。能量模型的分数函数，在每个噪声水平上学出来，就成了扩散，"
        "而VAE的下界就在它里面。神经ODE成了流匹配。GAN的判别器又回来，让扩散变快。<bookmark mark='b'/>所以，下一部分的扩散模型，"
        "是用你现在已经见过的零件搭起来的。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock.":
        "我们来盘点一下。自回归模型一块一块地写出一张图像，似然精确，采样慢。VAE用一个下界同时学出编码和解码器，在码率和失真之间权衡。"
        "GAN从一个评判者那里学习，而这场博弈可能坍缩到少数几个峰上，并绕着均衡点盘旋；瓦瑟斯坦评判器和梯度惩罚驯服了它。"
        "流把噪声可逆地弯成数据，似然精确，神经ODE则连续地做这件事，用迹代替了行列式。玻尔兹曼机是一个能量，"
        "通过把数据和它自己的梦相对比来训练；而朗之万动力学只用分数函数就能从任何能量里采样，只要有足够的噪声让它在峰之间穿行。",

    'All of this comes back.':
        "这些都会再回来。在每个噪声水平上学到的分数函数，就是下一次的扩散，而流匹配用回归来训练连续流。自编码器和它们的词元，"
        "是第22和第23部分图像、视频和音频模型的前端，下一尺度预测会在第22部分回来。对比的思想，把数据往上推、把其他一切往下压，"
        "驱动着第24部分的自监督学习。而怎样评判一个模型，以及它的指标怎样失效，会为整个系列收尾。",

    'Here are six problems to try':
        '这里有六道题可以试一试，从最优判别器到弗雷歇距离。在这里暂停，把它们做一做；完整的解答在这一部分的笔记里。',

    'Next time: diffusion.':
        "下一次：扩散。在每个水平上给数据加噪声，从耳语到咆哮；通过学会去掉噪声，学出每个水平上的分数函数；然后从纯噪声出发，"
        "一级一级地往回走，也就是第13章退火朗之万的成长版。第21部分：扩散与流。",

    'To go deeper, Simon Prince':
        '想深入学习的话，西蒙·普林斯的《理解深度学习》把GAN、流和VAE讲得很清楚，而且可以免费阅读；凯文·墨菲的第二卷则深入地覆盖了'
        '本部分的每一个家族。感谢收看，我们第21部分再见。',
})

PHRASES.update({
    # family names spliced into the comparisons
    'the PixelCNN': 'PixelCNN',
    'the VAE': 'VAE',
    'the GAN': 'GAN',
    'WGAN-GP': 'WGAN-GP',
    'the flow': '流',
    'the autoregressive model': '自回归模型',
    'the energy model': '能量模型',
    # the contrastive-divergence variants
    'CD-1': 'CD-1',
    'CD-10': 'CD-10',
    'persistent CD': '持续对比散度',
})
