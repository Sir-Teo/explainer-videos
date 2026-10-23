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
        "<bookmark mark='c'/>第二台把每个数字压缩成16个数，再学会把它们展开。<bookmark mark='d'/>第三台是通过和一个评论家"
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

    # ------------------------------------------------------------------ Autoregressive
    'Chapter two. One pixel at a time.':
        '第2章。一次一个像素。',

    "f'It ends {gap:.2f} nats above the floor: close to the best":
        '最后它比下限高{gap:.2f}奈特：已经接近任何模型所能做到的最好。',

    "f'It ends {gap:.2f} nats above the floor: the shape is right":
        '最后它比下限高{gap:.2f}奈特：形状是对的，边缘还有点软。',

    # ------------------------------------------------------------------ Latent
    'Chapter three. From Helmholtz machines':
        '第3章。从亥姆霍兹机到变分自编码器。',

    # ------------------------------------------------------------------ VAE
    'Chapter four. Training a VAE':
        '第4章。训练VAE：码率、失真与坍缩。',

    'Every step up in beta lowers the rate':
        'β每升高一级，码率就降低、失真就升高：这些训练连成了一条曲线，也就是信息论里的码率-失真权衡。',

    'Overall, raising beta lowers the rate':
        '总体上，升高β会降低码率、升高失真，虽然不是每一级都如此：这些训练散布在一条曲线周围，也就是信息论里的码率-失真权衡。',

    "f'Free bits, a floor of {fbits:g} nats per code number, keep {kf:.1f} nats in the code, and":
        '自由比特，也就是每个编码数{fbits:g}奈特的下限，能让编码里留住{kf:.1f}奈特，解码出的数字有{pf:.0f}%和来源相符。',

    "f'Free bits, a floor of {fbits:g} nats per code number, keep {kf:.1f} nats in the code, yet only":
        '自由比特，也就是每个编码数{fbits:g}奈特的下限，能让编码里留住{kf:.1f}奈特，可解码出的数字只有{pf:.0f}%和来源相符：'
        '给码率设一个下限，并不等于用上了编码。',

}

PHRASES = {}

ZH.update({
    # ------------------------------------------------------------------ Game
    'Chapter five. The adversarial game.':
        '第5章。对抗博弈。',

    'f"Measured on the ring, in the first steps of training':
        '在环上测量，训练的最初几步里，非饱和生成器的梯度是极小极大生成器的{ratio:.1f}倍。',

    "f'Measured on the ring, in the first steps, the two gradients":
        '在环上测量，最初几步里，两者的梯度相差不到{fac:.1f}倍：我们的判别器在早期从来没有自信到让这个差别显现出来。',

    'Its samples bunch into one clump':
        '它的样本挤成一团，有时落在一个峰上，有时落在峰与峰之间，而这一团从一个峰跳到另一个峰：生成器追着判别器最薄弱的地方跑，'
        '判别器跟着追过去。',

    'It covers a few modes at a time':
        '它一次只覆盖几个峰，而覆盖的是哪几个，一直在变：生成器追着判别器最薄弱的地方跑，判别器跟着追过去。',

    'At times it reaches all eight, then loses some again':
        '它有时会覆盖全部八个峰，然后又丢掉几个：生成器追着判别器最薄弱的地方跑，判别器跟着追过去。',

    # ------------------------------------------------------------------ Dynamics
    'Chapter six. Why GANs spiral.':
        '第6章。GAN为什么会绕圈。',

    "f'Over training the generator visits {visited} of the modes":
        '训练过程中，生成器到过{visited}个峰，但同时最多只覆盖{best}个；最后它覆盖了{last}个。',

    "f'Over training the generator visits all eight modes":
        '训练过程中，生成器到过全部八个峰，有时还同时覆盖了全部，但都不长久；最后它覆盖了{last}个。',

    # ------------------------------------------------------------------ Wasserstein
    'Chapter seven. Wasserstein GANs.':
        '第7章。瓦瑟斯坦GAN。',

    "f'And {qw:.0f} percent of its samples":
        '它的样本里有{qw:.0f}%落在某个峰的三倍标准差以内。',

})

ZH.update({
    # ------------------------------------------------------------------ Scale
    'Chapter eight. GANs at scale':
        '第8章。规模化的GAN：BigGAN、StyleGAN与反演。',

    "The discriminator's loss settles close to two log two":
        '判别器的损失稳定在2 log 2附近，这是它只能像抛硬币一样乱猜时的值。',

    'f"The discriminator\'s loss ends at {dfin:.2f}':
        '判别器的损失最后是{dfin:.2f}，低于2 log 2：它仍然能把大多数假样本和真数字分开。',

    'The FID, which mixes both, is best with no truncation at all.':
        '把两者混在一起的FID，在完全不截断时最好。',

    'f"Their average squared error per pixel is {ge:.3f}, against {ve:.3f} for the VAE\'s encoder, which':
        '它们每个像素的平均平方误差是{ge:.3f}，而VAE的编码器是{ve:.3f}；编码器一遍就给出答案，但它是另一个模型。',

    'f"Their average squared error per pixel is {ge:.3f}, against {ve:.3f} for the VAE\'s encoder in one pass':
        '它们每个像素的平均平方误差是{ge:.3f}，而VAE的编码器一遍就是{ve:.3f}：GAN能生成的范围，并不完全包含这些数字。',

    # ------------------------------------------------------------------ Flows
    'Chapter nine. Normalizing flows.':
        '第9章。归一化流。',

    'The ring is the hardest: an invertible map':
        '环是最难的：一个可逆映射没法把一团噪声撕成八个分开的小岛，所以它在小岛之间拉出了一道道细细的概率之桥。',

    'The checkerboard is the hardest: a stack':
        '棋盘格是最难的：一串平滑的可逆映射，只能近似它的悬崖。',

    'The moons are the hardest of the three for it.':
        '对它来说，双月是三者中最难的。',

    "f'In bits per pixel the flow gets {mf:.2f} on held-out digits, against {mp:.2f} for the PixelCNN on the same budget: an exact":
        '在留出数字上，流的每像素比特数是{mf:.2f}，而在同样预算下，PixelCNN是{mp:.2f}：似然是精确的，但更差；耦合层把容量花在了保持可逆上。',

    "f'In bits per pixel the flow gets {mf:.2f} on held-out digits, against {mp:.2f} for the PixelCNN on the same budget: a better":
        '在留出数字上，流的每像素比特数是{mf:.2f}，而在同样预算下，PixelCNN是{mp:.2f}：似然比自回归模型还好。',

    # ------------------------------------------------------------------ NeuralODE
    'Chapter ten. Neural ODEs and continuous flows.':
        '第10章。神经ODE与连续流。',

    "f'The two end within {ag:.2f} nats":
        '两者最后相差不到{ag:.2f}奈特：带噪声的估计和精确的迹训练出的流一样好。',

    "f'The noisy estimate costs {ag:.2f} nats by the end.'":
        '到最后，带噪声的估计损失了{ag:.2f}奈特。',

    "f'The noisy estimate even ends {ag:.2f} nats ahead.'":
        '带噪声的估计最后甚至领先了{ag:.2f}奈特。',

})

ZH.update({
    # ------------------------------------------------------------------ Hopfield
    'Chapter eleven. Hopfield and Boltzmann.':
        '第11章。霍普菲尔德与玻尔兹曼。',

    "f'It settles on the stored digit exactly.'":
        '它恰好停在了存储的那个数字上。',

    "f'It settles on a state that matches":
        '它停在了一个状态上，和存储的数字有{100 * (1 + ov) / 2:.0f}%的像素相同。',

    'recalls all ten digits from the same damaged cues':
        '从同样受损的提示里，回忆出了全部10个数字',

    "f'recalls {100 * hm[-1]:.0f} percent":
        '在存了全部10个数字时，回忆出了其中{100 * hm[-1]:.0f}%',

    # ------------------------------------------------------------------ RBM
    'Chapter twelve. Contrastive divergence.':
        '第12章。对比散度。',

    "f'Ranked by where they end:":
        '按最后的位置排名：{first}是每个数字{fin[order[0]]:.1f}奈特，接着是{second}，{fin[order[1]]:.1f}，然后是{third}，'
        '{fin[order[2]]:.1f}。',

    'One step of the chain is the cheapest estimate of the dreams':
        '链只走一步，是对梦最便宜、也最有偏的估计：它能学，但学到的不完全是对的东西。',

    # ------------------------------------------------------------------ Langevin
    'Chapter thirteen. Langevin dynamics and the score.':
        '第13章。朗之万动力学与分数函数。',

})

ZH.update({
    # ------------------------------------------------------------------ Judging
    'Chapter fourteen. Judging a generator.':
        '第14章。怎样评判一个生成模型。',

    'High precision, low recall:':
        '精确率高，召回率低：它做出来的东西看起来是真的，但只覆盖了数据的一部分。',

    'The two numbers say different things':
        '两个数说的是不同的事，这正是要有两个数的原因。',

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
        "每个数字大约占十分之一。<bookmark mark='a'/>{msg}在整个类别这个尺度上的模式丢失，是最容易看出来的失败。",

    'f"So, at this small scale and on one budget, who won what?':
        "那么，在这个小尺度、同一份预算下，谁赢了什么？<bookmark mark='a'/>{close}<bookmark mark='b'/>哪个最好，取决于模型是"
        "拿来做什么的，也取决于规模：GAN曾经多年画出最清晰的图像，用的规模远远超过我们的。",

    "every model wins something, and none wins everything.":
        "每个模型都赢下了一些东西，没有哪个赢下一切。",

    "f'every model but one wins something;":
        "除了一个模型，每个模型都赢下了一些东西；{l0}在这里什么也没赢。",

    "f'{nl} of the five win nothing at all":
        "五个里有{nl}个什么也没赢，{l0}就是其中之一。",

    "f'The most uneven is {nw}:":
        '最不均匀的是{nw}：它最少见的数字是{wk}，只占它样本的{mw:.1f}%，而真实数据里大约是10%。最均匀的是{nf_}，'
        '它最少见的数字也还有{mf:.1f}%。',

    # ------------------------------------------------------------------ Meet
    'Chapter sixteen. Where the families meet.':
        '第16章。几个家族的交汇。',

    "f'Its samples score an FID of {vfid:.1f}, better":
        '它的样本FID是{vfid:.1f}，比上一章五个单一模型都好，不过它是在那份预算之外训练的。',

    "f'Its samples score an FID of {vfid:.1f}; the best":
        '它的样本FID是{vfid:.1f}；上一章最好的单一模型是{bfid:.1f}，而这一个是在那份预算之外训练的。',

    'So this is where the four answers, and the fifth, ended up.':
        "这就是那四个答案，以及第五个，最后的归宿。<bookmark mark='a'/>VAE和GAN变成了分词器和潜空间，每个图像和视频模型都从它们出发。"
        "自回归模型写出那些词元，一次一个尺度，或者一次一个词元。能量模型的分数函数，在每个噪声水平上学出来，就成了扩散，"
        "而VAE的下界就在它里面。神经ODE成了流匹配。GAN的判别器又回来，让扩散变快。<bookmark mark='b'/>所以，下一部分的扩散模型，"
        "是用你现在已经见过的零件搭起来的。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock.":
        "我们来盘点一下。自回归模型一块一块地写出一张图像，似然精确，采样慢。VAE用一个下界同时学出编码和解码器，在码率和失真之间权衡。"
        "GAN从一个评论家那里学习，而这场博弈可能坍缩到少数几个峰上，并绕着均衡点盘旋；瓦瑟斯坦评论家和梯度惩罚驯服了它。"
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

# Narration as tightened for length (replaces the first drafts of these lines).
ZH.update({
    'Here is the problem at its smallest:':
        "先看这个问题最小的样子：平面上的2万个点，抽自一个形状像两弯月亮的分布p。<bookmark mark='a'/>"
        "因为分布是我们造的，我们确切地知道p；面对图像或文本，没有人知道。<bookmark mark='b'/>生成模型，"
        "就是一个从样本里学出来、能从中抽样的分布q；<bookmark mark='c'/>最好还能计算它，"
        "<bookmark mark='d'/>还能给每个x一个编码，一个说明它是什么的简短描述。",

    'f"The workhorse for fitting q':
        '拟合q的主力方法，是第1部分讲过的最大似然：让平均意外度，也就是负log q，尽可能小。'
        "<bookmark mark='a'/>把这个平均值拆成两部分。<bookmark mark='b'/>数据自身的熵"
        "，任何模型都打不破它；加上从p到q的KL散度，也就是犯错的代价。<bookmark mark='c'/>所以，"
        "最大似然就是最小KL。<bookmark mark='d'/>对我们的三个测试密度，这个下限是已知的："
        '双月是{hm:.2f}奈特，八个高斯组成的环是{hr:.2f}，棋盘格是{hc:.2f}。',

    'What each family offers.':
        "每个家族能给出什么。<bookmark mark='a'/>自回归模型：精确的似然，稳定的训练，"
        "但样本只能一块一块地出来。<bookmark mark='b'/>VAE：一遍就能采样，还有一个编码，"
        "但似然只有一个下界。<bookmark mark='c'/>GAN：一遍采样，完全没有似然，而且出了名地难训练。"
        "<bookmark mark='d'/>流：纸面上什么都有，代价付在结构上。<bookmark mark='e'/>"
        "能量模型：密度只知道到差一个常数，采样很慢。<bookmark mark='f'/>Xiao、"
        'Kreis和Vahdat把它叫作三难困境：清晰的样本、对数据的覆盖、快速的采样。大多数家族只做到其中两样。',

    'Our test bench: three densities':
        "我们的试验台：平面上的三个密度，小到能看清模型做的每一件事，各有各的难处。<bookmark mark='a'/>"
        '还有图像：MNIST手写数字，6万个用来训练，1万个用来测试，平均缩小到14乘14像素，'
        "<bookmark mark='b'/>16个灰度级。<bookmark mark='c'/>"
        '每个图像模型都得到同样的算力预算，一次运算一次运算地数，并且从几个随机起点分别训练。',

    'How we got here. In 1948':
        '我们是怎么走到这里的。1948年，克劳德·香农一个字母一个字母地生成英文：这是第一个自回归模型。'
        "<bookmark mark='a'/>20世纪80年代，在霍普菲尔德的网络和玻尔兹曼机里，"
        "记忆成了一片能量地形里的山谷；<bookmark mark='b'/>1995年，亥姆霍兹机又加了第二个网络，"
        "去猜测隐藏的原因。<bookmark mark='c'/>2006年，堆叠起来的玻尔兹曼机让深度学习重新起步。"
        "<bookmark mark='d'/>接着，短短三年里，出现了变分自编码器、生成对抗网络、可逆的流，"
        "以及PixelCNN。<bookmark mark='e'/>GAN画出的图像一直最清晰，"
        "直到2021年被扩散模型超过。<bookmark mark='f'/>今天的系统，把这些想法全都结合了起来。",

    'The first answer needs no new mathematics. Any':
        "第一个答案不需要新的数学。任何分布都可以按链式法则分解：<bookmark mark='a'/>第一个变量，"
        "乘以给定第一个时的第二个，再乘以给定前两个时的第三个，依此类推。<bookmark mark='b'/>"
        '每个因子都是一次预测：给定之前的一切，预测下一个变量。把每个因子都学会，你就精确地得到了这个分布；按顺序逐个采样，'
        "你就得到一个样本。<bookmark mark='c'/>香农的英文，本系列的每个语言模型，以及现在的一个数字，"
        '都是这样来的。',

    'f"In the plane, the first factor':
        "在平面上，第一个因子p(x1)是沿着底边的一条曲线。<bookmark mark='a'/>第二个因子，"
        '给定x1时x2的概率，在每一个切片上都是一条不同的曲线：10个高斯的混合，由一个输入x1的小网络设定。'
        "<bookmark mark='b'/>把两者相乘，就是模型学到的密度，这里回放了整个训练过程，"
        "旁边是它在留出点上的意外度。<bookmark mark='c'/>{verdict}",

    'An image is the same story with more variables: the 196':
        "图像也是同一个故事，只是变量更多：一个数字的196个像素，按阅读顺序排好。<bookmark mark='a'/>"
        '预测这个像素时，模型可以看它之前的每一个像素，之后的一个也不能看；它输出16个概率，每个灰度级一个，'
        "就像语言模型预测下一个词元。<bookmark mark='b'/>让训练变快的诀窍是一个掩码："
        '每个滤波器都把属于未来的那一半设为零，于是跑一遍就能同时预测全部196个像素，每个只用它自己的过去。'
        "<bookmark mark='c'/>从NADE和MADE，"
        '发展出了DeepMind的Aaron van den Oord和同事在2016年提出的PixelRNN和PixelCNN'
        '，以及生成语音的WaveNet。',

    "There's a catch. Ask the network":
        '这里有个问题。问问网络，它的预测依赖于哪些输入：求一个像素的预测对每个输入的梯度。'
        "<bookmark mark='a'/>如果简单地把带掩码的滤波器叠起来，右上方有一块楔形永远看不见，尽管它排在前面"
        "。<bookmark mark='b'/>第二篇PixelCNN论文把网络一分为二：一个竖直的栈，看得到上面的各行，"
        '把信息送给一个水平的栈，它看得到这一行已经写好的部分。盲区消失了。我们训练的就是这种结构。',

    'f"Here is ours learning: on the left':
        '这是我们的模型在学习：左边是它在留出数字上的意外度，单位是每像素比特数；右边是它在每个检查点画出的东西。'
        "<bookmark mark='a'/>没训练时，它每个像素要付{c0:.2f}比特，大约就是均匀乱猜，"
        "画出来的是一片雪花。<bookmark mark='b'/>然后它学会大多数像素是黑的，墨迹是一笔一笔的，"
        "还有笔画的形状。<bookmark mark='c'/>最后它停在每像素{f0:.2f}比特；"
        '三个种子最后落在{lo:.2f}到{hi:.2f}之间。',

    'f"And here is one digit being drawn, with':
        "这是一个数字正在被画出来，旁边是模型对下一个像素给出的16个概率。<bookmark mark='a'/>"
        "在空白的边缘，它很确定：黑色。<bookmark mark='b'/>到了笔画的边上，它会犹豫，"
        "而它掷出的那枚硬币决定了数字的形状。<bookmark mark='c'/>代价在于顺序：一个数字要过196遍网络，"
        '每一遍都要等上一遍，在这里是{ms_ar:.1f}毫秒，大约是GAN一遍所需时间的{ratio:,.0f}倍。',

    'The second answer adds something hidden: every':
        '第二个答案加进了一些隐藏的东西：每个数字都来自一个编码z，几个从普通高斯分布里抽出来的数。'
        "<bookmark mark='a'/>一个解码器把每个编码变成图像上的一个分布。这是一个真的解码器，编码只有两个数"
        "：平面上的每一个点都被解码成一个数字，而这些数字平滑地过渡成彼此。<bookmark mark='b'/>于是，"
        "一张图像的概率，就是对所有可能产生它的编码求平均，而这个积分我们算不出来。<bookmark mark='c'/>"
        '反过来，从图像求编码，要用贝叶斯法则，分母里还是同一个积分。',

    'In 1995 Peter Dayan':
        '1995年，Peter Dayan、杰弗里·辛顿、Radford Neal和Richard Zemel提出，'
        '把贝叶斯法则学出来：用第二个网络，一个识别模型q，去猜一张图像背后的隐藏原因。'
        "<bookmark mark='a'/>这就是亥姆霍兹机，以赫尔曼·冯·亥姆霍兹命名，他把知觉称为无意识的推断。"
        "<bookmark mark='b'/>醒着的时候，它用q猜出真实图像的原因，再训练生成网络把图像重现出来。"
        "<bookmark mark='c'/>睡着的时候，它梦出原因和图像，再训练q把原因找回来。"
        "<bookmark mark='d'/>它管用，但很别扭：q是从梦里学的，两个阶段也没有共同的目标。18年后，"
        '修正它的是一个下界。',

    'Here is the bound. Start':
        "这就是那个下界。从一张图像的对数概率出发。<bookmark mark='a'/>同时乘以和除以给定x时z的q，"
        "积分就变成了对从q里抽出的编码求平均。<bookmark mark='b'/>平均值的对数，至少是对数的平均值："
        "这是詹森不等式。<bookmark mark='c'/>剩下两项：一项是重建，把从q里抽出的编码解码；"
        '另一项是从q到先验的KL散度，也就是编码关于x携带的奈特数，即它的码率。两项合起来，就是证据下界，ELBO。'
        "<bookmark mark='d'/>差距是从q到真实后验的KL散度，所以抬高下界，就同时改进了模型和猜测者："
        '一个目标，取代了亥姆霍兹机的两个。',

    "One problem remains: you can't take":
        "还剩一个问题：你没法对掷硬币求梯度。<bookmark mark='a'/>所以把随机性挪个地方："
        "编码器输出一个均值和一个幅度，编码等于均值加上幅度乘以一份新抽的噪声。<bookmark mark='b'/>"
        "现在噪声只是一个输入，梯度可以流回编码器：这就是重参数化技巧。<bookmark mark='c'/>对高斯分布来说"
        "，KL项有闭式解。<bookmark mark='d'/>2013年12月，"
        'Diederik Kingma和Max Welling发表了这个方法；几周之后，Danilo Rezende、'
        'Shakir Mohamed和Daan Wierstra独立地发表了同样的方法：这就是变分自编码器。',

    'f"Ours has a sixteen-number code':
        '我们的VAE有一个16个数的编码，它的解码器给每个像素一个钟形分布，切成16个灰度级：一共{p:,}个参数。'
        "<bookmark mark='a'/>所以它的下界和PixelCNN用的是同一个单位，每像素比特数。",

    'f"Here is our VAE learning: the bound':
        "这是我们的VAE在学习：下界的两项，单位是每个留出数字的奈特数。<bookmark mark='a'/>一开始，"
        "重建要花{r0:.0f}奈特，码率是{k0:.1f}：编码什么也没说。<bookmark mark='b'/>"
        "然后码率上升，重建变得清晰：准确是用信息换来的。<bookmark mark='c'/>到最后，"
        '编码携带{k1:.1f}奈特，解码器还需要{r1:.0f}；下界是每像素{eb0:.2f}比特，'
        "而每个数字用64个编码得到的更紧的下界是{iw0:.2f}。<bookmark mark='d'/>样本是认得出的数字，"
        '而16个编码数里只有{act}个携带信息。记住这一点。',

    'What does the code learn? With two numbers':
        '编码学到了什么？每个数字只用两个数，我们就能看见：每个点是一个留出数字，放在它的编码处，按它的标签上色。'
        "<bookmark mark='a'/>编码器把它们铺开，同一种数字聚到了一起，尽管没有人告诉它标签；"
        "KL项则让整团点留在原点附近。<bookmark mark='b'/>把一个均匀的编码网格解码出来，"
        '就得到模型的数字地图，各个区域之间是平滑的过渡。',

    'f"Switched-off code numbers have a name':
        '被关掉的编码数有个名字，叫后验坍缩，而我们可以让它发生。在双月上训练一个VAE，它的解码器分别从编码预测x1和x2：'
        "<bookmark mark='a'/>要得到双月的形状，它就必须用上编码，它的码率稳定在每个点{fk:.2f}奈特"
        "。<bookmark mark='b'/>现在把第2章的本事交给解码器：用编码和x1来预测x2。"
        "<bookmark mark='c'/>{verdict}",

    "f'The rate falls to {ak:.3f} nats, in every seed":
        '码率降到了{ak:.3f}奈特，每个种子都是：编码坍缩了，每个点都被编码成同一团东西，解码器独自建模了双月。',

    "f'The rate falls to {ak:.2f} nats, against":
        '码率降到了{ak:.2f}奈特，对比{fk:.2f}：编码几乎没被用上。',

    'f"The code costs rate':
        '编码要付码率，而一个能独自建模数据的解码器，从编码里什么也得不到。2016年，'
        "Samuel Bowman和同事在一个生成句子的VAE上撞上了这个问题。<bookmark mark='a'/>"
        "{first}<bookmark mark='b'/>{second}<bookmark mark='c'/>"
        '{third}疗法是：让编码值得上它的代价。',

    "f'With a PixelCNN decoder, the rate sinks":
        '用PixelCNN做解码器，码率沉到了每个数字{kp:.1f}奈特，而普通VAE是{kv:.1f}：'
        '解码器自己就能画出一个数字。',

    "f'With a PixelCNN decoder, the rate ends":
        '用PixelCNN做解码器，码率最后是每个数字{kp:.1f}奈特，而普通VAE是{kv:.1f}：'
        '强大的解码器对编码的依赖少得多。',

    'f"Decode a hundred test digits\' codes four times each: only':
        '把一百个测试数字的编码各解码四次：结果里只有{pa:.0f}%和被编码的数字相同。',

    'f"Decode a hundred test digits\' codes four times each: {pa:.0f} percent still':
        '把一百个测试数字的编码各解码四次：仍有{pa:.0f}%和被编码的数字相同。',

    'f"One more thing: on the ring':
        '还有一点：在环上，VAE把样本撒进了空隙里；只有{100 * q:.0f}%落在某个峰的三倍标准差以内。'
        "<bookmark mark='a'/>一个平滑的编码，会把一切锐利的东西都模糊掉：这就是VAE出了名的柔和。"
        "<bookmark mark='b'/>修正它的办法，各自成了一整条研究路线：更深的编码、离散的编码，"
        '以及每个潜在扩散模型前端的那个自编码器。',

    'f"The two terms pull against each other; weight':
        '这两项互相拉扯；给KL项乘上一个权重β，就得到Irina Higgins的β-VAE。'
        "<bookmark mark='a'/>我们训练了6个β值，从{b_lo:g}到{b_hi:g}，每个两个种子："
        "每个点是一次训练，它的码率对比它的失真。<bookmark mark='b'/>{trend}β为{b_lo:g}时"
        '，编码携带{r_lo:.0f}奈特，有{a_lo}个活跃的编码数；β为{b_hi:g}时，'
        "是{r_hi:.0f}奈特和{a_hi}个。<bookmark mark='c'/>大的β给出平滑、千篇一律的数字："
        '编码已经不再确定细节了。',

    'The third answer throws the likelihood away.':
        '第三个答案把似然扔掉了。2014年，伊恩·古德费洛和约书亚·本吉奥实验室的同事，让两个网络互相对抗。'
        "<bookmark mark='a'/>生成器把噪声变成一个样本，从来看不到数据。"
        "<bookmark mark='b'/>判别器输出一个样本是真的的概率。<bookmark mark='c'/>"
        '一个学着分辨两者，另一个学着骗过它：用论文里的话说，是造假币的人对抗警察。写成一个值：'
        '判别器最大化它判断正确的对数概率，生成器则最小化它。',

    'What does a winning discriminator learn?':
        "一个获胜的判别器学到的是什么？把这个值写成一个积分，用q表示生成器的分布。<bookmark mark='a'/>"
        '在每个x上，它选一个数D(x)，去最大化a乘log D加上b乘log(1减D)：令导数为零。'
        "<bookmark mark='b'/>最好的判别器是p除以p加q，也就是x处的概率里属于数据的那一份。"
        "<bookmark mark='c'/>数据占主导的地方说真，生成器占主导的地方说假，两者相当的地方说一半。",

    'Put the best discriminator back.':
        "把最好的判别器代回去。<bookmark mark='a'/>在每个对数里把p加q减半，"
        "就出现了两个到平均m的KL散度，再减去log 4。<bookmark mark='b'/>合起来，就是詹森-香农散度"
        "：对称，最大为log 2，并且恰好在q等于p时为零。<bookmark mark='c'/>面对一个完美的评论家，"
        '生成器在最小化一个散度，却从来不需要写下一个密度：这就是2014年那篇论文的定理。训练能不能找到这个最小值，'
        '是本章余下部分和下一章的内容。',

    'f"The first practical problem appears on day one:':
        "第一个实际问题，在第一天就出现了：假样本很差，D(G(z))停在零附近。<bookmark mark='a'/>"
        "在那里，极小极大损失是平的，生成器几乎得不到梯度。<bookmark mark='b'/>"
        '古德费洛在同一篇论文里的修正是：最大化骗过对方的概率，也就是负log D，它在另一个平的地方很陡。'
        "<bookmark mark='c'/>{meas}<bookmark mark='d'/>这个修正有代价，"
        '2017年由Martin Arjovsky和Léon Bottou发现：它的梯度，'
        '是一个反向KL散度减去詹森-香农项的梯度，而反向KL几乎不惩罚漏掉一个峰。',

    '"Here is that cost on the ring:':
        '这就是那个代价在环上的样子：背景是判别器的判决，说真的地方亮；点是生成器从300个固定噪声向量画出的样本。'
        "{pick}<bookmark mark='a'/>{hop}<bookmark mark='b'/>这就是模式坍缩"
        "：一个生成器只会做几种东西。<bookmark mark='c'/>{cmp_}",

    "f'Over five seeds, the non-saturating GAN covers {mean_ns:.1f} of the eight modes on average, all eight in {full_ns}; the minimax loss covers {mean_mm:.1f}, all eight in {full_mm}. Adam":
        '五个种子里，非饱和GAN平均覆盖八个峰中的{mean_ns:.1f}个，有{full_ns}次覆盖了全部八个；'
        '极小极大损失平均覆盖{mean_mm:.1f}个，全部八个的有{full_mm}次。'
        'Adam会把极小极大损失那些小的梯度重新放大，于是反向KL的影响就显露出来了。',

    "f'Over five seeds, the non-saturating GAN covers {mean_ns:.1f} of the eight modes on average, all eight in {full_ns}; the minimax loss covers {mean_mm:.1f}, all eight in {full_mm}.'":
        '五个种子里，非饱和GAN平均覆盖八个峰中的{mean_ns:.1f}个，有{full_ns}次覆盖了全部八个；'
        '极小极大损失平均覆盖{mean_mm:.1f}个，全部八个的有{full_mm}次。',

    "f'This is seed {seed}, the run of five":
        '这是种子{seed}，五次训练里最后覆盖的峰最少的那一次；五次里有{n_col}次在不同程度上坍缩了。',

    'The smallest game: one player':
        "最小的博弈：一个玩家选x，想让x乘y小；另一个选y，想让它大。<bookmark mark='a'/>"
        "各自沿着自己的梯度走：x按负y移动，y按正x移动。<bookmark mark='b'/>把这些速度画出来："
        "哪里都没有下坡，只有转动。<bookmark mark='c'/>雅可比矩阵的特征值是正负i，纯粹的旋转。"
        '梯度下降是为山谷造的；而一场博弈可以是一个漩涡。',

    'f"Take real steps, both players at once':
        "真正走几步，两个玩家同时走，步长为η：每一步都乘以这个矩阵。<bookmark mark='a'/>"
        "它的特征值大小是1加η平方的平方根，大于1。<bookmark mark='b'/>所以同时的步子盘旋向外："
        "走了{T}步之后，半径变成了原来的{rs_end:.1f}倍。<bookmark mark='c'/>轮流走，"
        "螺旋就闭合成一条轨道；它的半径最后是{ra:.2f}。<bookmark mark='d'/>要收敛，就得往前看："
        '外梯度法用一个试探点上的梯度走步，乐观梯度下降则根据上一步做外推。两者都盘旋着向内收，'
        '分别收到{re_:.2f}和{ro:.2f}。',

    'Real GANs do this.':
        '真实的GAN也会这样。Lars Mescheder、'
        'Andreas Geiger和Sebastian Nowozin把一个GAN简化成两个数：数据在零处，生成器在θ处，'
        "判别器是一条斜率为ψ的直线。<bookmark mark='a'/>在均衡点周围，是同样的旋转。"
        "<bookmark mark='b'/>同时走的步子盘旋向外；<bookmark mark='c'/>"
        "轮流走的步子绕圈。<bookmark mark='d'/>他们的修正是惩罚判别器在真实数据上的梯度，"
        '在这里就是γ的一半乘ψ平方：这是摩擦，螺旋于是向内收。StyleGAN训练时用的正是这个惩罚，R1。',

    'f"Back to the ring: each row a mode':
        "回到环上：每一行是一个峰，每一列是一个检查点，亮度表示生成器落在那里的样本。<bookmark mark='a'/>"
        '{tour}亮带从一个峰游荡到另一个峰：这是那个玩具博弈的旋转，发生在由分布构成的空间里。'
        "<bookmark mark='b'/>这个领域用惩罚项、往前看的步子、不同的学习率和谱归一化来对付它。",

    'f"Martin Arjovsky, Soumith Chintala':
        'Martin Arjovsky、Soumith Chintala和Léon Bottou问：当两个分布不重叠时，'
        '詹森-香农散度会怎样？这对图像来说是常态。他们的例子：数据是x等于零处的一条线段，模型是θ处的同一条线段。'
        "<bookmark mark='a'/>只要θ不为零，JS就是log 2：平的，没有梯度，看不出θ正在靠近。"
        "<bookmark mark='b'/>在17个θ值上训练的判别器，"
        "估计值都在log 2的{js_err:.2f}以内。<bookmark mark='c'/>"
        '一个衡量质量要搬多远的距离，给出一个V字形，斜率指向家；训练出来的评论家在θ等于{tk:.2f}处，'
        '把它估计为{wk:.2f}。',

    "That is the earth mover's distance:":
        "这就是推土机距离：把p想成一堆沙子，q想成一个同样体积的坑。<bookmark mark='a'/>"
        "一个运输方案规定多少沙子运到哪里；它的代价是质量乘以距离。<bookmark mark='b'/>瓦瑟斯坦-1距离，"
        '就是最便宜的方案的代价。加斯帕尔·蒙日在1781年提出了这个问题；列昂尼德·康托罗维奇在1942年给出了它的现代形式'
        '。',

    'Cheapest plans between image distributions':
        '在图像的分布之间求最便宜的方案，是没有希望算出来的；但根据康托罗维奇和鲁宾斯坦的对偶，'
        "这个距离也等于一个斜率不超过1的函数在p和q之间所能拉开的最大期望差距。<bookmark mark='a'/>所以"
        "，一个输出可以是任意实数的评论家f，学着拉开这个差距，而生成器学着缩小它。<bookmark mark='b'/>"
        "难处在于斜率的限制；第一版瓦瑟斯坦GAN把每个权重都截断了。<bookmark mark='c'/>"
        'Ishaan Gulrajani和同事注意到，最优评论家在真假点之间的斜率恰好是1，于是就在那里惩罚斜率的偏离：'
        '这就是WGAN-GP。',

    'f"Back to the ring, same networks':
        '回到环上，同样的网络，同样多的生成器步数。背景现在是评论家，一片在数据所在处高起的地形。'
        "<bookmark mark='a'/>样本沿着它往上爬，爬向各个峰。<bookmark mark='b'/>"
        "{verdict}<bookmark mark='c'/>{sharp}",

    "f'Its samples sit less tightly":
        '不过，它的样本落得没那么紧：{qw:.0f}%落在某个峰的三倍标准差以内，而非饱和GAN是{qn:.0f}%。',

    "f'Over five seeds, WGAN-GP covers":
        '五个种子里，WGAN-GP平均覆盖八个峰中的{mw:.1f}个，有{full_w}次覆盖了全部八个，'
        '而非饱和GAN是{mn:.1f}个，极小极大GAN是{mm:.1f}个：一个距离会一直把生成器拉向每一个缺失的峰。',

    'f"Over five seeds, WGAN-GP covers':
        '五个种子里，WGAN-GP平均覆盖八个峰中的{mw:.1f}个，而非饱和GAN是{mn:.1f}个，'
        '极小极大GAN是{mm:.1f}个：在这里，距离并没有换来覆盖。',

    'f"The cure has a price:':
        '这个疗法有代价：每走一步生成器，评论家要更新五次，而每个惩罚项都要多做一次反向传播。'
        "<bookmark mark='a'/>在我们的数字模型上数下来，"
        "WGAN-GP的一步相当于GAN的{ratio:.1f}步，<bookmark mark='b'/>"
        '所以在同一份预算下，GAN走了{sg:,}步生成器，WGAN-GP走了{sw:,}步。第15章会看到这换来了什么。',

    'f"First, ours: two-layer networks':
        "先看我们的：数字上的两层网络，以及生成器从16个固定噪声向量画出的东西。<bookmark mark='a'/>"
        "先是团块，然后是笔画，然后是数字。<bookmark mark='b'/>两个损失不像学习曲线那样下降；"
        '它们在相互平衡。{bal}这里没有任何东西能说明生成器什么时候变好了，这也是GAN需要第14章那些量尺的一个原因。',

    'From there to photographs took four years.':
        "从这里到照片，用了四年。<bookmark mark='a'/>2015年，Alec Radford、"
        'Luke Metz和Soumith Chintala找到了能稳定训练的卷积GAN，它们的噪声向量还能做算术：'
        "一个微笑的女人，减去一个女人，加上一个男人，得到一个微笑的男人。<bookmark mark='b'/>2017年，"
        '英伟达的Tero Karras和同事在训练中让网络逐渐长大，一直长到1024像素。'
        "<bookmark mark='c'/>2018年，Andrew Brock、"
        'Jeff Donahue和Karen Simonyan把GAN扩展到了ImageNet：在128像素上，'
        'Inception分数达到166.5，FID达到7.4，而此前的最好成绩是52.5和18.6。'
        "<bookmark mark='d'/>Karras的团队则把生成器本身重新做了一遍：这就是StyleGAN。",

    "StyleGAN's generator starts not from the noise":
        'StyleGAN的生成器不从噪声出发，而是从一个学出来的4像素常数出发，一块一块地上采样。'
        "<bookmark mark='a'/>噪声先经过一个8层的映射网络，变成一个编码w，"
        "<bookmark mark='b'/>再由w设定每一块的风格，也就是每个通道的一个缩放和一个平移；"
        "新加入的噪声则添上雀斑之类的细节。<bookmark mark='c'/>风格可以混合，粗的层取自一张脸，"
        '细的层取自另一张；而在w的空间里走直线，成了有意义的编辑。',

    '"BigGAN\'s truncation trick:':
        'BigGAN的截断技巧：采样时，任何大于t的噪声坐标都重新抽取，让生成器待在它所学内容的中间地带。'
        "<bookmark mark='a'/>在我们的GAN上，用第14章的精确率和召回率来看："
        "<bookmark mark='b'/>{verdict}<bookmark mark='c'/>{fid_s}",

    "f'at t of {tt:g}, precision {p0:.2f} and recall {r0:.2f}; untruncated, {p1:.2f} and {r1:.2f}. Fidelity":
        't等于{tt:g}时，精确率{p0:.2f}，召回率{r0:.2f}；不截断时，是{p1:.2f}和{r1:.2f}'
        '。用多样性换来了逼真度。',

    'f"at t of {tt:g}, precision':
        't等于{tt:g}时，精确率{p0:.2f}，召回率{r0:.2f}；不截断时，是{p1:.2f}和{r1:.2f}'
        '：这笔交换不如BigGAN的划算。',

    "f'The FID, which mixes both, is best at t of {bt:g}":
        '把两者混在一起的FID，在t等于{bt:g}时最好。',

    'f"A GAN has no encoder:':
        'GAN没有编码器：要编辑一张真实照片，得先找到能产生它的噪声，方法是对G(z)和这张图像之间的差做梯度下降。'
        "这就是GAN反演。<bookmark mark='a'/>八个没见过的测试数字，每个从四个随机起点出发，保留最好的，"
        "走{n_st}步。<bookmark mark='b'/>{cmp_}<bookmark mark='c'/>"
        '在两个找到的编码之间连一条线，一个数字就会渐变成另一个；在StyleGAN的w空间里，这成了照片编辑，'
        '从2016年的iGAN到2023年的DragGAN。',

    'The fourth answer keeps the likelihood exact and sampling one pass':
        '第四个答案既保留精确的似然，又只需一遍就能采样：把简单的噪声z推过一个可逆函数g。'
        "<bookmark mark='a'/>g拉伸的地方，概率就摊薄；g压缩的地方，概率就堆积起来。"
        "<bookmark mark='b'/>概率是守恒的，一段区间一段区间地守恒。"
        "<bookmark mark='c'/>所以x的密度，等于它的z的密度，乘以逆映射把一小段区间缩小了多少；"
        "<bookmark mark='d'/>在多维里，就是逆映射的雅可比行列式。似然是精确的。"
        '2010年Esteban Tabak和Eric Vanden-Eijnden描述了这样的流；'
        '2015年Danilo Rezende和Shakir Mohamed把它带进了深度学习。',

    'f"The catch is the determinant, d cubed':
        '麻烦在于行列式：一个d乘d的雅可比矩阵要花d的三次方次运算。'
        'Laurent Dinh和约书亚·本吉奥找到了一条绕过去的路。把变量分成两半；'
        "<bookmark mark='a'/>前一半原样复制；<bookmark mark='b'/>后一半做缩放和平移，"
        "缩放量s和平移量t可以由任意网络从前一半算出来。<bookmark mark='c'/>雅可比矩阵是三角形的，"
        "所以对数行列式就是所有s的和。<bookmark mark='d'/>逆变换同样便宜：减去t，再除以e的s次方。"
        "<bookmark mark='e'/>我们的结果和自动微分算出的完整行列式相差不到10的负{k_exp}次方奈特。"
        '把这样的层叠起来，轮流换哪一半，流就能把任何东西弯过来。',

    'Here is that bending, our eight coupling layers':
        '这就是那种弯曲，来自我们在双月上的8个耦合层：噪声平面上的一个方格网，以及噪声的样本。'
        "<bookmark mark='a'/>每一层都沿一个坐标轴滑动这些点，滑动的量由另一个坐标决定。"
        "<bookmark mark='b'/>网格被剪切、折叠，却从不撕裂，也从不自相交叉。"
        "<bookmark mark='c'/>第8层之后，噪声变成了双月，而把这个映射倒过来读，就给出每个点的精确概率。"
        "<bookmark mark='d'/>在棋盘格上，同样的这些层把平面切成了一个个方块。",

    'f"Training, replayed on the checkerboard.':
        "在棋盘格上回放训练。<bookmark mark='a'/>概率质量从空的格子里流出，流进有数据的格子。"
        "<bookmark mark='b'/>和每个下限相比，流最后在双月上高出{g_m:.2f}奈特，"
        '在环上高出{g_r:.2f}，在棋盘格上高出{g_c:.2f}。{why_hard}',

    'f"On digits, here is what our flow draws:':
        "在数字上，这是我们的流画出的东西：<bookmark mark='a'/>带噪声的笔画；把噪声调小，"
        "这是Glow的技巧，笔画就更干净，也更彼此相像。<bookmark mark='b'/>{verdict}"
        "<bookmark mark='c'/>2018年Glow画出人脸之后，流多年落在后面，直到2024年，"
        '苹果的Shuangfei Zhai和同事用Transformer模块搭出了一个流，报告的样本可以和扩散模型相比。',

    'A residual network updates its state a little':
        "残差网络每一层都把它的状态更新一点点：h加上f(h)。<bookmark mark='a'/>"
        "这是常微分方程欧拉法的一步。<bookmark mark='b'/>让步长缩到零，"
        "状态就沿着一个由网络定义的速度场流动。<bookmark mark='c'/>Ricky Chen、"
        'Yulia Rubanova、Jesse Bettencourt和David Duvenaud把它们叫作神经ODE，'
        '获得了2018年NeurIPS的最佳论文奖。让求解器倒着跑就能求逆：这是一个不需要耦合层的流。',

    'How does density change along the flow?':
        "密度沿着流是怎样变化的？走一小步，用上一章的变量替换。<bookmark mark='a'/>在一阶近似下，"
        "单位阵加一个小矩阵的行列式，等于1加上它的迹。<bookmark mark='b'/>取极限，对数密度下降的速率，"
        "就是场的散度，也就是它的雅可比矩阵的迹。<bookmark mark='c'/>沿着路径积分：一个精确的似然，"
        "对网络没有任何限制。<bookmark mark='d'/>但即使只是迹，每个维度也要花一次反向传播。",

    'f"The way out is Hutchinson\'s trick':
        '出路是1989年的哈钦森技巧：抽一个均值为0、方差为1的随机向量ε，计算ε转置乘A乘ε。'
        "<bookmark mark='a'/>平均下来，只有对角线留了下来：这就是迹，只用一个探针、一次反向传播。"
        "<bookmark mark='b'/>随机正负号的方差比高斯小，因为对角线上的项从不变化；"
        '在一个训练好的流的400个点上测量，公式在{rel:.0f}%以内成立，正负号的方差是高斯的{ratio:.2f}倍'
        "。<bookmark mark='c'/>2019年的FFJORD就建立在它之上：在{d_}维里，在这台电脑上，"
        '一个探针比精确的迹快{tr_ratio:.0f}倍。',

    'f"A continuous flow on the moons':
        '在双月上训练连续流，两种方法各三个种子：精确的迹，或每条路径一个随机正负号探针，评判时都用精确的迹。'
        "<bookmark mark='a'/>{verdict}用精确的迹训练一次花了{te:.0f}秒，"
        '用估计花了{th:.0f}秒。',

    'And the flow itself: seven hundred':
        '再看流本身：700个噪声点，被学到的场从时刻0带到时刻1，背景是每个时刻的密度。'
        "<bookmark mark='a'/>这团点被拉长、分开，卷成了两弯月亮。<bookmark mark='b'/>"
        '训练时每一步仍要解一次ODE；第21部分的流匹配则改用回归来学这样的场。',

    'The fifth answer is the oldest. In 1982':
        '第五个答案是最古老的。1982年，物理学家约翰·霍普菲尔德给一个由正负1神经元组成、连接对称的网络定义了一个能量。'
        "<bookmark mark='a'/>每次一个神经元取它输入的符号。<bookmark mark='b'/>"
        '一次翻转让能量改变负的翻转量乘以输入，而两者符号一致，所以能量只会下降：网络会落进一个山谷。'
        "<bookmark mark='c'/>第9部分讲过的赫布规则，让选定的图案成为山谷：一段记忆，存成了一片地形的谷底"
        '。',

    'f"Here is one: 196 neurons':
        "这是一个：196个神经元，每个像素一个，存了三个数字。<bookmark mark='a'/>从中间那个数字出发，"
        "翻转它四分之一的像素。<bookmark mark='b'/>一个神经元接一个神经元，状态往下坡滑，每变一次，"
        "能量就降一次。<bookmark mark='c'/>{res}一份损坏的副本，就足以找回这段记忆。",

    'f"How much can it hold? Store random':
        "它能存多少？存进随机图案，再从一份损坏的副本回忆每一个。<bookmark mark='a'/>用{N}个神经元，"
        '当每个神经元摊到{half:.2f}个图案时，能回来的已经不到一半；Amit、'
        'Gutfreund和Sompolinsky的自旋玻璃理论把极限放在大约0.138。'
        "<bookmark mark='b'/>数字彼此相像，平均重叠{mean_ov:.2f}，情况更糟。{hebb_s}",

    'f"Hebb\'s rule already fails at':
        '用赫布规则，存到{n_fail}个数字时就已经失败了，提示会滑进几段记忆的混合。',

    'Even so, all ten come back here':
        '即便如此，在这里十个都回来了；再多一些，山谷就会合并成混合。',

    'f"The fix came over thirty years later:':
        '修正来自三十多年以后：Dmitry Krotov和霍普菲尔德让能量变得更陡，'
        "Hubert Ramsauer和同事把更新写成了比较、softmax、平均。<bookmark mark='a'/>"
        "用它，我们的网络{res}。<bookmark mark='b'/>这个更新就是第13部分的注意力：状态是查询，"
        '记忆是键和值。一个注意力层，就是一个只走一步的霍普菲尔德网络。',

    'In 1985 David Ackley':
        '1985年，David Ackley、杰弗里·辛顿和特伦斯·谢诺夫斯基让神经元变得随机，'
        '于是网络按物理学里的玻尔兹曼分布采样：e的负能量除以温度次方，再除以归一化常数Z。'
        "<bookmark mark='a'/>他们加入了隐藏单元：机器自己的特征。<bookmark mark='b'/>"
        '学习规则是：测量每一对单元在数据钳住时同时打开的频率，再在自由运行时测一次，每个连接按两者之差加强，'
        "直到机器的梦和这个世界相符。<bookmark mark='c'/>麻烦在于：每次测量都要达到平衡，"
        "而这可能要等到天荒地老。<bookmark mark='d'/>2024年，霍普菲尔德和辛顿分享了诺贝尔物理学奖，"
        '获奖理由是“为利用人工神经网络实现机器学习的基础性发现和发明”。',

    'The way out was to restrict the machine:':
        '出路是给机器加限制：两层，可见层和隐藏层，层间相连，层内不连；这是保罗·斯莫伦斯基1986年的harmonium，'
        "今天的受限玻尔兹曼机。<bookmark mark='a'/>一个权重矩阵把两层耦合起来。"
        "<bookmark mark='b'/>给定一层，另一层的单元彼此独立，每个都是它输入的sigmoid。"
        "<bookmark mark='c'/>我们的这台：196个可见单元，也就是黑白两色的数字，以及16个隐藏单元，"
        '原因你马上会看到。',

    'Sum the hidden units out:':
        "把隐藏单元求和消掉：一张图像的对数概率，等于负的自由能，再减去log Z。<bookmark mark='a'/>"
        "自由能是一串softplus项的和。<bookmark mark='b'/>log Z的梯度，是模型下的一个平均。"
        "<bookmark mark='c'/>所以权重的梯度就是玻尔兹曼规则：数据的相关性，减去模型的相关性。"
        "<bookmark mark='d'/>第二项仍然需要从模型里采样。",

    "Geoffrey Hinton's shortcut, in 2002: start":
        "2002年，杰弗里·辛顿的捷径是：让链从一个训练数字出发，<bookmark mark='a'/>跑k步吉布斯采样，"
        "一次处理一整层，<bookmark mark='b'/>然后就用它走到的地方。k等于1时它是有偏的，但它能学，"
        "而且学得快：这就是对比散度。<bookmark mark='c'/>2008年，"
        'Tijmen Tieleman让链在两次更新之间一直跑下去：这就是持续对比散度。',

    'f"Does contrastive divergence maximize':
        '对比散度是在最大化似然吗？Z是对2的196次方张图像求和，但也可以对隐藏状态求和，'
        "而16个隐藏单元只有6万5千多个状态。<bookmark mark='a'/>所以这是留出数字的精确对数似然："
        "三种方法，各三个种子，更新次数相同。<bookmark mark='b'/>{verdict}"
        "<bookmark mark='c'/>{why_}",

    'With sixteen hidden units, even one step':
        '只有16个隐藏单元时，链哪怕只走一步，也是一个公允的估计。',

    "What does it learn? Each hidden unit's weights":
        '它学到了什么？把每个隐藏单元的权重画成一张图，就能看出什么会让它打开：这是一台100个单元的机器里的40个，'
        "正的对应墨迹，负的对应纸面。<bookmark mark='a'/>要做梦，就从随机像素出发运行链：一步、十步、"
        "一百步、一千步。<bookmark mark='b'/>只有16个单元时，我们可以给每个隐藏状态加权，"
        "精确地从真实的模型采样。<bookmark mark='c'/>2006年，辛顿、"
        'Simon Osindero和Yee-Whye Teh把受限玻尔兹曼机堆成了深度信念网络，深度学习的复兴由此开始；'
        '六年后，GPU上的反向传播让这一步变得不再必要。但这些想法留了下来：一个能量，以及由一条链抽出的样本。',

    'f"The general idea: any network':
        '一般的想法是：任何只有一个输出的网络都是一个能量，e的负能量次方除以它的积分Z就是一个密度，不需要掩码，不需要可逆，'
        "也不需要编码。<bookmark mark='a'/>它的梯度有同样的两个阶段：降低数据的能量，抬高模型样本的能量。"
        "<bookmark mark='b'/>在平面上，Z可以在网格上求和，所以我们的环模型的似然是精确的："
        '{nll:.2f}奈特，而下限是{h:.2f}。在196维里，任何网格都不管用。',

    "Sampling comes from physics: Paul Langevin's":
        '采样的办法来自物理：保罗·朗之万1908年的粒子，往下坡漂移，同时被随机地踢来踢去。写成算法：'
        '沿着对数密度往上坡走一步，加一点噪声，再重复；根据第5部分的福克-普朗克方程，这个随机游走最终会停在p上。'
        "<bookmark mark='a'/>这一步需要log p的梯度。<bookmark mark='b'/>Z是常数"
        "，所以它的梯度为零：让训练变难的那个归一化常数，从采样里消失了。<bookmark mark='c'/>"
        '这个梯度就是分数函数，上升最快的方向；在我们的环模型上，就是指向八个山谷的箭头。',

    'f"So train an energy with its own Langevin chains':
        '所以，用能量模型自己的朗之万链来训练它：把一池子链各走{k_}步，降低真实点的能量，抬高链停下处的能量。2019年，'
        "Yilun Du和Igor Mordatch让这种方法在图像上管用了。<bookmark mark='a'/>在环上"
        '：数据所在处出现了山谷，链掉了进去，而在链扎堆却没有数据的地方，能量升了起来。'
        "<bookmark mark='b'/>它最后比下限高出{gap:.2f}奈特。",

    'f"And sampling: uniform noise':
        "再看采样：先撒均匀噪声，然后在每个学到的能量上走{steps}步朗之万。<bookmark mark='a'/>"
        "点滑进山谷，在那里抖动。<bookmark mark='b'/>在环上，三个种子里，长链分别落在八个峰中的{m0}个"
        '、{m1}个和{m2}个上，既不需要Z，也不需要逆映射：只需要分数函数。',

    'f"The catch is the bridge to the next part.':
        '这个陷阱正是通向下一部分的桥。两个高斯，分别占20%和80%，分数函数精确已知。'
        "<bookmark mark='a'/>均匀地撒下点，运行朗之万。<bookmark mark='b'/>"
        '每个点都掉进离它近的那个山谷，然后待在那里，所以重的那个峰得到{p_h:.0f}%，这是由起点决定的，'
        '起点里是{s_h:.0f}%，而不是密度所说的80%：对于分开的几个峰，分数函数看不到它们的权重。'
        "<bookmark mark='c'/>2019年，宋飏和Stefano Ermon的修正是："
        '先用大量噪声把密度模糊掉，让山谷合在一起，然后一级一级地调小噪声。{verdict}'
        "<bookmark mark='d'/>在图像上，这需要每个噪声水平上的分数函数，而它可以通过去噪学出来，"
        '这是Hyvärinen和Vincent证明的：这就是扩散，第21部分。2025年，'
        '均衡匹配则通过沿一个学到的能量往下走来生成图像。',

    "f'Annealing fixes it: {a_h":
        '退火修好了它：{a_h:.0f}%，接近真实值。',

    "f'Annealing moves it to {a_h":
        '退火把它变成了{a_h:.0f}%。',

    'How good is a generative model? Its held-out':
        '一个生成模型有多好？它在留出数据上的似然并不够，2016年Lucas Theis、'
        'Aaron van den Oord和Matthias Bethge说明了这一点：把一个好模型稀释，'
        "每一百个样本里只有一个来自它，其余都是噪声。<bookmark mark='a'/>对数似然最多下降log 100，"
        "对一张图像来说只是个舍入误差。<bookmark mark='b'/>而样本99%都是垃圾。"
        "<bookmark mark='c'/>GAN则根本没有似然。所以这个领域直接评判样本。",

    'f"The standard since 2017 is the Fréchet':
        '自2017年以来的标准，是弗雷歇Inception距离，FID，一个高斯之间的距离。在一维里，'
        '最便宜的搬法是分位数对分位数，瓦瑟斯坦距离的平方等于均值之差的平方加上幅度之差的平方。'
        "<bookmark mark='a'/>在多维里，换成协方差和一个带矩阵平方根的迹：Dowson和Landau，"
        "1982年。<bookmark mark='b'/>"
        'Martin Heusel和同事把这些高斯拟合到一个训练好的分类器看到的特征上，真实的对比生成的。'
        "<bookmark mark='c'/>他们用的是在ImageNet上训练的Inception；对数字，"
        '我们用一个数字分类器的最后一个隐藏层，128个数，它在测试数字上的准确率是{acc:.2f}%。',

    'f"A check: {rise}':
        "先检查一下：{rise}一个3乘3的模糊得到{blur:.1f}。<bookmark mark='a'/>"
        '再提一个警告：样本少会让FID偏大。真实数字对测试集，用{n0}个样本时是{f0:.2f}，'
        '用{n2k:,}个时是{f2k:.2f}，用{nN:,}个时是{fN:.2f}。'
        "<bookmark mark='b'/>所以只能在样本数相同时比较：我们一律用{n2k:,}个，"
        '这让一个完美模型的得分大约是{f2k:.2f}。',

    "f'noise added to real digits raises our FID at every step":
        '给真实数字加噪声，我们的FID随着噪声每升一级而上升，从{nf0:.2f}升到{nfN:.1f}。',

    "f'noise added to real digits raises our FID overall":
        '给真实数字加噪声，我们的FID总体上随之上升，从{nf0:.2f}升到{nfN:.1f}。',

    'f"One number can\'t separate':
        '一个数分不开样本好不好和覆盖全不全。Mehdi Sajjadi和同事，'
        '以及后来英伟达的Tuomas Kynkäänniemi和同事，把它拆成了两个。'
        "<bookmark mark='a'/>在每个真实点周围画一个球，半径到它第三近的真实邻居：这就是数据所在的地方。"
        "<bookmark mark='b'/>精确率：落进真实球里的生成样本所占的比例。"
        "<bookmark mark='c'/>召回率：落进生成球里的真实点所占的比例。"
        "<bookmark mark='d'/>第5章的非饱和GAN，种子0：精确率{pr0:.2f}，"
        '召回率{rc0:.2f}。{verdict}',

    'f"Every family on the ring, three seeds each.':
        "每个家族在环上的结果，各三个种子。<bookmark mark='a'/>精确率最高：{n_bp}，"
        '{v_bp:.2f}；召回率最高：{n_br}，{v_br:.2f}；精确率最低：{n_wp}，{v_wp:.2f}'
        "。<bookmark mark='b'/>再看为什么只看FID很危险：一个均值和协方差都和环一样的高斯团，"
        '弗雷歇距离是{bfd:.3f}，和环自己的两份样本之间差不多，而它的精确率是{bprec:.2f}。',

    'f"No sample metric catches memorization:':
        '没有哪个样本指标能抓住死记硬背：重放训练数字，得分和真实数据一模一样，FID是{floor:.2f}，'
        "精确率{rp:.2f}，召回率{rr:.2f}。<bookmark mark='a'/>所以我们直接检查："
        "每个样本最近的训练数字。<bookmark mark='b'/>"
        '真实的测试数字离它们最近的训练数字的中位距离是{real_d:.3f}。{verdict}',

    'For six years GANs drew the sharpest images. In 2021':
        '六年里，GAN画出的图像最清晰。2021年，'
        'OpenAI的Prafulla Dhariwal和Alex Nichol用一篇论文的标题说出了发生的事：'
        "扩散模型在图像合成上打败了GAN。<bookmark mark='a'/>在256像素的ImageNet上，"
        "BigGAN-deep的FID是6.95；带引导的扩散模型是4.59。<bookmark mark='b'/>"
        'GAN的精确率最高，但召回率只有0.28：它画出的是世界里一个狭窄切片的逼真图像。'
        "<bookmark mark='c'/>原因正是本部分遇到过的那些：一个漏掉每个峰都要付代价的目标，"
        '一个稳定的回归而不是一场博弈，以及一个随着规模变大不断改进的配方。',

    'Meanwhile the families combined.':
        '与此同时，几个家族结合了起来。2017年，Aaron van den Oord、'
        'Oriol Vinyals和Koray Kavukcuoglu给VAE配了一个离散编码。'
        "<bookmark mark='a'/>编码器的每个向量都吸附到一个学出来的码本里最近的那一项上，"
        "于是一张图像变成了一个整数网格：词元。梯度直接穿过这个吸附。<bookmark mark='b'/>在词元之上，"
        "一个PixelCNN学出先验。<bookmark mark='c'/>2021年，"
        'VQGAN加了一个GAN损失让解码器更清晰，并在词元之上用了一个Transformer；'
        'DALL-E用一个Transformer同时写文本词元和图像词元。用VAE做出词元，用GAN让它们好看，'
        '再用自回归模型把它们写出来：这就是今天图像系统的前端，第22部分和第23部分会把它打开来看。',

    'f"We built a small one: each digit':
        '我们做了一个小的：每个数字变成一个7乘7的词元网格，每个词元是{K}个码本项之一，解码器再把网格变回来。'
        "<bookmark mark='a'/>码本的困惑度是{perp:.1f}：实际上，"
        "它的{K}项里大约有这么多在被使用。<bookmark mark='b'/>直接写下来，"
        '一个网格是{rawb:.0f}比特；一个小Transformer只用{prb:.0f}比特就能预测它。'
        "<bookmark mark='c'/>从Transformer里采样词元，再解码，就画出了新的数字。"
        '{verdict}',

    'Reading order is slow,':
        '阅读顺序很慢，而且对一幅图来说是个奇怪的顺序。2024年，'
        '字节跳动和北京大学的Keyu Tian和同事预测的不是下一个词元，而是下一个尺度。'
        "<bookmark mark='a'/>先是整张图像的一个词元，然后是一个2乘2的图，然后是更大的图，"
        "每一张都在所有更粗的图的条件下一次性预测出来。<bookmark mark='b'/>"
        '在256像素的ImageNet上：FID是1.73，而光栅顺序是18.65，快了大约20倍；'
        '这是NeurIPS 2024的杰出论文。',

    "And the GAN didn't die. Diffusion needs":
        '而GAN并没有死。扩散模型每张图像要过几十遍网络；生成器只要一遍。为了找回一步生成，人们把扩散模型蒸馏成生成器，'
        "而最好的蒸馏方法都用了判别器。<bookmark mark='a'/>"
        'Stability AI的Axel Sauer和同事，用GAN损失加一个扩散教师，'
        '训练出了一到四步出图的SDXL-Turbo；后来又做了SD3-Turbo，它的判别器是用扩散模型搭的。'
        "<bookmark mark='b'/>Tianwei Yin和同事的DMD2加了一个作用在真实图像上的GAN损失："
        "在小尺寸的ImageNet图像上，一步就达到了1.28的FID。<bookmark mark='c'/>"
        'R3GAN用一个有原则的损失重建了GAN本身。一致性模型两步就达到扩散模型的质量；2026年，'
        '何恺明的团队训练出一步生成器，方法是让它们的样本漂移到数据上：在ImageNet上的FID是1.54。',
})
