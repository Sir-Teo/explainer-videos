"""Chinese narration for ai24: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第24部分：无标签学习'

CHAPTERS = {
    'Hook': '没有人告诉它什么是数字',
    'Problem': '1. 无标签学习',
    'Pretext': '2. 自己出一道题',
    'InfoNCE': '3. 分辨真假',
    'SimCLR': '4. 同一个数字的两个视图',
    'Sphere': '5. 对齐与均匀',
    'Collapse': '6. 坍缩',
    'BYOL': '7. 没有负样本：BYOL与SimSiam',
    'Barlow': '8. 去相关：Barlow Twins与VICReg',
    'DINO': '9. 自蒸馏：DINO',
    'Scale': '10. 规模与数据筛选',
    'Masked': '11. 填空：MAE与BEiT',
    'JEPAScene': '12. 预测含义，而不是像素',
    'Budget': '13. 所有方法，同一份预算',
    'Embeddings': '14. 用于搜索的嵌入',
    'Platonic': '15. 所有模型看到的是同一个世界吗？',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'f"These six hundred dots are handwritten digits.':
        "这600个点是手写数字。一个网络把每个数字压缩成仅仅3个数，也就是球面上的一个点。<bookmark mark='a'/>颜色是数字的标签，"
        "从0到9。<bookmark mark='b'/>可是这个网络从来没见过任何标签。它被问到的唯一问题是：哪两张被扭曲过的图来自同一个数字。"
        "<bookmark mark='c'/>然而，问一个数字在这个球面上的近邻它是几，它们答对的比例是{pct(zk, 0)}%。",

    'Here is how it got there. At the start the points are scattered at random.':
        "它是这样走到这一步的。一开始，这些点是随机散开的。<bookmark mark='a'/>每一步给网络看128个数字，每个数字有两个版本，"
        "被裁剪、被倾斜、被涂抹过。它把每个数字的两个版本拉到一起，<bookmark mark='b'/>把其余的一切推开。这条规则里根本没提到5或7。"
        "<bookmark mark='c'/>可是簇还是出现了，因为一个5的两份涂抹副本彼此相像的方式，正是所有5彼此相像的方式。"
        "<bookmark mark='d'/>如果去掉“推开”，网络就会找到一个更偷懒的答案：所有数字都落在同一个点上。",

    'That is the question of this part: how does a network learn what matters':
        "这就是本部分的问题：没有人给数据打标签时，网络怎样学到什么是重要的？<bookmark mark='a'/>这个领域找到了三类答案。"
        "藏起输入的一部分，让网络把它找回来。<bookmark mark='b'/>给出同一个输入的两个版本，让网络使它们一致。"
        "<bookmark mark='c'/>或者藏起输入的一部分，不要它的像素，而要它的含义。<bookmark mark='d'/>而且每一类都必须避开我们刚才看到的"
        "同一个陷阱：一个对什么输入都给出同一个答案的网络，和自己完全一致。",

    'This is Part 24 of AI, Built: learning without labels.':
        "这是《人工智能，从零搭建》的第24部分：无标签学习。<bookmark mark='a'/>本部分的内容：这个领域是怎样走到今天的，以及怎样评判"
        "一个网络学到了什么；<bookmark mark='o2'/>对比学习，从word2vec的负样本到SimCLR；<bookmark mark='o3'/>球面的几何；"
        "<bookmark mark='o4'/>坍缩，先让它发生，再用四种办法阻止它；<bookmark mark='o5'/>自蒸馏，以及把它做大需要什么；"
        "<bookmark mark='o6'/>掩码模型与联合嵌入预测；<bookmark mark='o7'/>同一份预算下的所有方法，以及用于搜索的嵌入；"
        "<bookmark mark='o8'/>最后，不同的网络最终看到的世界是否一样。本部分的每一个模型，都是在制作这个视频的电脑上训练的。",

    # ------------------------------------------------------------------ Problem
    'Chapter one. Learning without labels.':
        '第1章。无标签学习。',

    'For thirty years, a network learned to see by being told.':
        "三十年来，网络都是靠被告知来学会看东西的。本部分用到的MNIST数字带着6万个标签；<bookmark mark='a'/>ImageNet带着一百多万个，"
        "每一个都经过人工核对。<bookmark mark='b'/>可是没有标签的图片几乎是免费的。2023年的DINOv2在1.42亿张无标签图像上训练；"
        "<bookmark mark='c'/>2025年的DINOv3用了17亿张，是从大约170亿张里挑出来的。<bookmark mark='d'/>这些图永远不会有人去标注。"
        "问题是：怎样照样从中学习。",

    'In 2016 Yann LeCun drew intelligence as a cake.':
        "2016年，杨立昆把智能画成了一块蛋糕。<bookmark mark='a'/>监督学习，也就是从标签中学习，是蛋糕上的糖霜；强化学习，从奖励中"
        "学习，是顶上的樱桃。<bookmark mark='b'/>蛋糕本身，是学会从输入的任何一部分预测其他任何一部分：一张图片里的信息远远多于它的标签。"
        "<bookmark mark='c'/>后来他给这块蛋糕起了现在的名字：自监督学习。藏起输入的一部分，或者改变它，或者把它和另一个输入配对，"
        "然后让网络找回被藏起的东西，或者说出哪个和哪个是一对。<bookmark mark='d'/>答案不是人写的，是数据自己给的。我们要留下的不是答案，"
        "而是网络内部的向量，也就是它的表示。",

    'How we got here. In 1961 the neuroscientist Horace Barlow':
        "我们是怎样走到这里的。1961年，神经科学家霍勒斯·巴洛提出，感官会把接收到的信息重新编码，去掉其中的冗余。"
        "<bookmark mark='a'/>1992年，苏·贝克尔和杰弗里·辛顿训练了两个小网络，它们看着图像中相邻的部分，被要求彼此一致，结果它们学会了"
        "感知深度。<bookmark mark='b'/>随后出现了用于签名验证的孪生网络，然后是一种对比损失：把相似的样本对拉近，把其余的推开。"
        "<bookmark mark='c'/>去噪自编码器藏起输入的一部分；噪声对比估计和word2vec则通过分辨真实数据和噪声来学习。"
        "<bookmark mark='d'/>2015年前后出现了各种前置任务，2018年出现了InfoNCE损失。<bookmark mark='e'/>2019到2021年间，MoCo、"
        "SimCLR、BYOL、DINO和MAE追平了监督训练。<bookmark mark='f'/>此后：在表示空间里做预测，以及在数十亿张图像和视频上训练的模型。",

    'How do you judge a representation, when the whole point was not to use labels?':
        "既然初衷就是不用标签，又该怎样评判一个表示呢？先把网络冻结，<bookmark mark='a'/>然后看它的向量有多容易读出来。"
        "<bookmark mark='b'/>线性探针：只在上面训练一个线性分类器，用全部标签。如果在这个空间里，不同的数字能被平直的墙隔开，"
        "那么活儿就是网络干的。<bookmark mark='c'/>近邻投票：完全不训练，只问离它最近的20个训练数字。<bookmark mark='d'/>还有实践中最重要的"
        "检验：只用每个数字10个带标签的样本，训练一个线性分类器。",

    'f"Our test bench is MNIST:':
        "我们的试验台是MNIST：6万个手写数字用来学习，1万个用来测试。<bookmark mark='a'/>每种方法都用同一个小网络，同样的"
        "{v['steps']}次更新，同样的视图，从三个不同的随机起点开始。<bookmark mark='b'/>先看三把标尺：原始像素；一个未训练的网络；"
        "以及用全部标签训练的同一个网络。<bookmark mark='c'/>{verdict}自监督方法的成绩，应该落在未训练的网络和被告知答案的网络之间。",

    "f'Raw pixels already score {pct(knn[0], 1)} percent by nearest neighbours":
        '原始像素用近邻法已经能得到{pct(knn[0], 1)}%：在这一点上，MNIST很容易。难的检验是每个数字只给10个标签，这时像素只有'
        '{pct(few[0], 0)}%，而见过全部6万个标签的监督网络是{pct(few[2], 0)}%。',

    "f'With ten labels per digit, pixels manage {pct(few[0], 0)} percent":
        '每个数字10个标签时，像素得到{pct(few[0], 0)}%，监督网络得到{pct(few[2], 0)}%。',

    # ------------------------------------------------------------------ Pretext
    'Chapter two. Invent a puzzle.':
        '第2章。自己出一道题。',

    'The first idea was to invent a puzzle whose answer comes free with the data.':
        "最早的想法是出一道题，它的答案随数据免费附送。<bookmark mark='a'/>把图像切成小块，问一块相对另一块在哪里。"
        "<bookmark mark='b'/>把小块打乱，问原来的顺序。<bookmark mark='c'/>去掉颜色，让它把颜色找回来。<bookmark mark='d'/>挖一个洞，"
        "问那里原来是什么。<bookmark mark='e'/>或者把图像转一下，问哪边朝上。当时的想法是：要答对这些题，网络必须知道东西长什么样。"
        "<bookmark mark='f'/>问题在于，网络解的是你出的题，而不是你心里想的那个问题。",

    'f"We trained the rotation puzzle.':
        "我们训练了旋转这道题。每一步，64个数字各被转四种角度，网络要说出它看到的是哪一种。<bookmark mark='a'/>这里是四个测试数字，"
        "每个都有四种转法，旁边是网络给出的四个概率；绿色是正确答案。<bookmark mark='b'/>几百步之内，它就能答对大约"
        "{pct(np.mean(fin), 0)}%。<bookmark mark='c'/>而绿色的曲线才是我们真正关心的：网络的向量会不会把5放在5的旁边。它从没见过标签，"
        "可在这个快速测试里，它在数字上的近邻准确率从{pct(k0, 0)}%升到了{pct(k1, 0)}%。",

    'f"The puzzle has blind spots, and we can measure them.':
        "这道题有盲区，而且我们可以测量出来。这是训练好的网络在每个数字上找对转角的比例，取三个种子的平均。<bookmark mark='a'/>最差的是"
        "{names}。<bookmark mark='b'/>{why_}任务决定了网络关注什么，一个数字一个数字地决定。",

    'These are the digits that look much the same turned half a turn':
        '这些数字转半圈之后看起来差不多，所以对它们来说这道题没有答案，网络也就从它们身上学不到哪边朝上。',

    'Some of these look much the same turned around':
        '其中一些转过来看起来差不多，所以对它们来说，这道题有一部分是答不出来的。',

    'f"So how good is the representation?':
        "那么，这个表示有多好？<bookmark mark='a'/>{line}<bookmark mark='b'/>在真实照片上，这些题也被找到了捷径。2015年最早的拼块题，"
        "有一部分是靠色差解出来的：镜头在照片边缘附近加上的彩色镶边，会暴露一块图来自哪里。作者们只好去掉小块的颜色。"
        "<bookmark mark='c'/>前置任务让这个领域明白：免费的标签行得通，而题目的选择决定了学到什么。",

    "f'The rotation puzzle lifts the ten-label test":
        '旋转这道题把10个标签的检验从未训练网络的{pct(un_few, 0)}%提高到了{pct(rot_few, 0)}%；见过全部标签的监督网络是'
        '{pct(rows[3][3], 0)}%。',

    "f'The rotation puzzle barely moves the ten-label test":
        '旋转这道题几乎没有改变10个标签的检验：{pct(rot_few, 0)}%，未训练的网络是{pct(un_few, 0)}%。',

    'One puzzle turned out to be different from the rest':
        "有一道题和其他的都不一样，因为它不关乎图像的任何具体性质：让每张图像自成一类。<bookmark mark='a'/>它被变换出的副本算同一类；"
        "其他每张图像都算不同的类。阿列克谢·多索维茨基和同事在2014年试过这个办法，<bookmark mark='b'/>2018年，吴志荣和同事把它扩展到"
        "一百万个类，ImageNet的每张照片一个类，办法是为每张图像存一个向量，拿来做比较。<bookmark mark='c'/>把一张图像和其他所有图像"
        "区分开，这就是对比的思想，下一章讲它的数学。",

    # ------------------------------------------------------------------ InfoNCE
    'Chapter three. Telling the real from the fake.':
        '第3章。分辨真假。',

    'Contrastive learning starts from a statistics trick of 2010.':
        "对比学习起源于2010年的一个统计技巧。你想给数据建模，可模型的概率需要对所有可能的输入求一个归一化的和，这根本算不出来。"
        "<bookmark mark='a'/>那就自己选一些噪声加进来，训练一个分类器去分辨数据和噪声。<bookmark mark='b'/>迈克尔·古特曼和阿波·许韦里宁"
        "证明了：最好的这种分类器必须知道数据密度与噪声密度之比，所以它不用那个和就能学到模型。他们称之为噪声对比估计。",

    'Three years later, word2vec made the trick simple enough for everyone.':
        "三年后，word2vec把这个技巧变得人人都能用。拿一个词，dog，再拿一个真正出现在它附近的词，barked。<bookmark mark='a'/>把它们向量"
        "的打分推高。<bookmark mark='b'/>然后按词频的四分之三次方随机抽几个词，把它们的打分压低。<bookmark mark='c'/>这就是负采样，"
        "一种简化的噪声对比估计，也正是第3部分在那些书上训练的版本。一个真实的对，对上几个假的：接下来三章里的每种方法都是这个样子。",

    'In 2018 Aaron van den Oord, Yazhe Li and Oriol Vinyals wrote the modern form.':
        "2018年，亚伦·范登奥尔德、李雅哲和奥里奥尔·维尼亚尔斯写出了它的现代形式。拿一个x，和N个候选。<bookmark mark='a'/>其中一个，"
        "y1，真正和x是一对；其余N减1个是随机抽来的。<bookmark mark='b'/>一个打分函数f给每一对打分，softmax把分数变成一个猜测，损失就是"
        "猜中伙伴的交叉熵。他们叫它InfoNCE，<bookmark mark='c'/>因为它是变成了N选一的噪声对比估计，也因为它测量的东西：信息。",

    'Why information? Call K the slot where the partner sits.':
        "为什么是信息？把伙伴所在的位置叫作K。损失就是一个分类器猜K的交叉熵。<bookmark mark='a'/>交叉熵永远不小于它所猜之物的真实熵。"
        "<bookmark mark='b'/>K在N个位置上是均匀的，所以这个熵是log N，减去x和候选们透露的关于K的信息。<bookmark mark='c'/>候选们自己"
        "什么也透露不了：单看伙伴，它和其他任何一次抽样都一样。<bookmark mark='d'/>由链式法则，x透露的关于K的信息，至多是x和整组候选"
        "共有的信息，<bookmark mark='e'/>而这恰好就是x和它的伙伴共有的信息，也就是互信息。<bookmark mark='f'/>所以log N减去损失，"
        "是互信息的一个下界。又因为损失永远不为负，这个界永远说不出多于log N的信息。",

    'f"We can watch the ceiling.':
        "我们可以亲眼看到这个天花板。取几对高斯向量，它们共有的信息量是已知的：{mis[0]:g}、{mis[1]:g}或{mis[2]:g}奈特。"
        "在每个候选数N下用InfoNCE训练一个小的打分网络，N从2到512，然后读出log N减去损失。<bookmark mark='a'/>{s_line}"
        "<bookmark mark='b'/>可是要找{big:g}奈特时，估计值沿着log N那条线往上爬，停在{e_big:.1f}奈特，即使有{Ns[-1]}个候选也是如此。"
        "损失看到的信息，不可能多于候选数允许它看到的。<bookmark mark='c'/>这就是对比学习想要大批量的一个原因。",

    "f'With {small:g} nats to find, the estimate comes within ten percent":
        '要找{small:g}奈特时，候选数达到{near[0]}个后，估计值就和真值相差不到10%。',

    "f'Even with {small:g} nats to find, the estimate never comes within ten percent":
        '即使只要找{small:g}奈特，估计值也始终没能和真值相差在10%以内。',

    "The paper's own model, contrastive predictive coding":
        "论文自己的模型，对比预测编码，把这个用在了序列上。对一段语音或一行图像块做编码，<bookmark mark='a'/>把过去汇总成一个上下文向量，"
        "<bookmark mark='b'/>再用它从N个候选里挑出真正的未来编码。它在语音、图像、文本和三维游戏上都管用。<bookmark mark='c'/>本部分所有"
        "对比式的方法，都是这个损失，只是对“什么算伙伴”做了不同的选择。",

    # ------------------------------------------------------------------ SimCLR
    'Chapter four. Two views of one digit.':
        '第4章。同一个数字的两个视图。',

    'Contrastive learning for pictures needs a partner for each picture':
        "图片上的对比学习需要给每张图片找一个伙伴，而这个伙伴是造出来的，不是找来的。<bookmark mark='a'/>拿一个数字，随机地改变它："
        "裁剪缩放、倾斜、改对比度、模糊、擦掉一块、加噪声。<bookmark mark='b'/>每个版本都还是同一个数字。同一个数字的两个版本构成一个"
        "正样本对；<bookmark mark='c'/>批里其他每个数字的每个版本都是负样本。这些选择是我们给网络的唯一知识：它们规定了什么不该重要。",

    'In 2020 Ting Chen, Simon Kornblith, Mohammad Norouzi and Geoffrey Hinton':
        "2020年，陈挺、西蒙·科恩布利斯、穆罕默德·诺鲁齐和杰弗里·辛顿把这些拼在一起，做成了SimCLR。一个数字的两个视图通过同一个"
        "网络f，<bookmark mark='a'/>得到两个表示h。<bookmark mark='b'/>一个小的头g把它们各自映到单位球面上的向量z。"
        "<bookmark mark='c'/>损失就是以余弦为打分的InfoNCE：在128个数字的一批里，256个视图中的每一个都要从其余255个里认出自己的伙伴，"
        "温度为τ。<bookmark mark='d'/>训练完后，头被扔掉，留下h。",

    'f"Here is our SimCLR learning.':
        "这是我们的SimCLR在学习。六个测试数字，每个旁边是向量离它最近的8个测试数字，同一个数字的标绿，不同的标红。"
        "<bookmark mark='a'/>一开始网络是随机的，只有{pct(same[0], 0)}%的近邻是对的。<bookmark mark='b'/>随着训练，邻域里填满了正确的"
        "数字：最后达到{pct(same[-1], 0)}%。<bookmark mark='c'/>在完整的测试集上，用它的向量做线性探针，正确率是{pct(fin['linear'][0])}%，"
        "取三次训练的平均；近邻投票是{pct(fin['knn'][0])}%。",

    'f"Why throw the head away?':
        "为什么要扔掉那个头？因为损失要求z忽略两个视图之间所有不一致的东西：倾斜、大小、对比度。<bookmark mark='a'/>这个代价由头来付，"
        "下面一层的h保留得更多。<bookmark mark='b'/>{verdict}<bookmark mark='c'/>SimCLR的作者在ImageNet上也发现了这一点，差了十多个点；"
        "用一个很宽的网络和非常大的批量，他们的线性探针达到了76.5%，和用全部标签训练的同一个网络一样好。",

    "f'Ours agrees: reading the digits from h gives {pct(hl)} percent":
        '我们的结果也一样：从h读数字得到{pct(hl)}%，从z只有{pct(zl)}%。',

    "f'On our digits the difference is small: {pct(hl)} percent from h":
        '在我们的数字上差别很小：从h是{pct(hl)}%，从z是{pct(zl)}%。',

    'f"SimCLR needs its negatives in the batch':
        "SimCLR的负样本必须在批里，所以它需要巨大的批量：论文用到了8000张图。几个月前，何恺明和同事已经找到了另一条路，MoCo。"
        "<bookmark mark='a'/>把过去几批的键存进一个队列，用它们当负样本。<bookmark mark='b'/>为了让旧键和新键可以比较，用第二个编码器来算"
        "键，它是第一个编码器缓慢移动的平均。<bookmark mark='c'/>我们用4096个键的队列训练了MoCo。{mo_line}<bookmark mark='d'/>{crop_line}",

    "f\"On our digits, MoCo's linear probe reaches {pct(ml[0])} percent against SimCLR's {pct(sl[0])}: the queue":
        '在我们的数字上，MoCo的线性探针达到{pct(ml[0])}%，SimCLR是{pct(sl[0])}%：队列多出来的负样本有一点帮助。',

    "f\"On our digits, MoCo's linear probe reaches {pct(ml[0])} percent against SimCLR's {pct(sl[0])}: about":
        '在我们的数字上，MoCo的线性探针达到{pct(ml[0])}%，SimCLR是{pct(sl[0])}%：差不多；只有十种数字时，几百个负样本已经足够了。',

    "f\"On our digits, MoCo's linear probe reaches {pct(ml[0])} percent against SimCLR's {pct(sl[0])}: slightly":
        '在我们的数字上，MoCo的线性探针达到{pct(ml[0])}%，SimCLR是{pct(sl[0])}%：稍微落后；只有十种数字时，更多的负样本换不来什么。',

    "f\"And the views matter more than either":
        '而视图比两者都重要：只用裁剪，不改对比度、不模糊、不擦除、不加噪声，SimCLR的探针就降到{pct(crop[\'linear\'][0])}%。',

    "f\"With crops alone, SimCLR's probe is":
        '只用裁剪时，SimCLR的探针是{pct(crop[\'linear\'][0])}%：在干净的黑白数字上，其他变化帮助不大。',
}

PHRASES = {}

ZH.update({
    # ------------------------------------------------------------------ Sphere
    'Chapter five. Alignment and uniformity.':
        '第5章。对齐与均匀。',

    'f"Watch the contrastive loss work on a sphere.':
        "来看对比损失在球面上是怎么工作的。这是一个输出只有3个数的SimCLR网络，所以每个数字都是一个我们看得见的点。"
        "<bookmark mark='a'/>两个量讲出了整个故事。对齐：同一个数字的两个视图落得有多远。均匀性：所有点聚得有多紧，按定义，"
        "越低表示铺得越均匀。<bookmark mark='b'/>两者都在下降。每个数字的视图聚到一起，而不同的数字铺满整个球面，彼此离得尽可能远。"
        "<bookmark mark='c'/>到最后，对齐是{al[-1]:.2f}，均匀性是{un[-1]:.2f}；又因为网络没法把所有的5彼此推开，而不同时把它们和自己的"
        "视图分开，所以5最终都聚在一起。",

    'f"Where did the digits land?':
        "数字们落在了哪里？取每个数字在球面上的平均方向。<bookmark mark='a'/>最近的一对是{a1}和{b1}，相隔{ang[a1, b1]:.0f}度，"
        "其次是{a2}和{b2}。<bookmark mark='b'/>相隔最远的是{far[0]}和{far[1]}。没有人告诉网络哪些数字写法相近；球面的几何把它记了下来。"
        "<bookmark mark='c'/>最松散的一簇是数字{loose}：它的点散得最开。",

    'Tongzhou Wang and Phillip Isola showed why, in 2020.':
        "2020年，王同舟和菲利普·伊索拉说明了原因。用单位向量写出一个视图的损失：一项把它拉向伙伴，一项对所有样本求对数和。"
        "<bookmark mark='a'/>负样本很多时，这个和就变成N乘以一个平均值。<bookmark mark='b'/>在球面上，和伙伴的点积等于1减去两者距离"
        "平方的一半。于是损失分成两项：<bookmark mark='c'/>一个对齐项，就是视图之间的距离；一个均匀项，当点均匀铺满球面时最小。"
        "对比学习就是这两股力量，温度决定它们的平衡。",

    'f"We trained SimCLR at five temperatures, from 0.05 to 1.':
        "我们在5个温度下训练了SimCLR，从0.05到1。<bookmark mark='a'/>{line}<bookmark mark='b'/>右边是每个温度最后的对齐和均匀性。{geo}",

    "f'Accuracy peaks in the middle, at tau {TAUS[best]}":
        '准确率在中间达到峰值，τ为{TAUS[best]}时是{pct(means[best])}%，两端都下降：τ为{TAUS[0]}时是{pct(means[0])}%，'
        'τ为{TAUS[-1]}时是{pct(means[-1])}%。',

    "f'The best is tau {TAUS[best]}, with {pct(means[best])} percent":
        '最好的是τ为{TAUS[best]}，{pct(means[best])}%；最差的是τ为{TAUS[worst]}，{pct(means[worst])}%。',

    'Low temperatures spread the points most evenly, and pay for it in alignment':
        '低温度把点铺得最均匀，代价是对齐变差；高温度让视图对齐，却让点聚成一团。',

    'The temperature moves each run along the trade between the two terms.':
        '温度让每次训练沿着两项之间的权衡移动。',

    'f"The temperature has a second effect.':
        "温度还有第二个作用。在softmax里，每个负样本按它的权重施加推力，而权重取决于它已经有多相似。<bookmark mark='a'/>τ为{lo_t}时，"
        "每个视图最相似的10个负样本占了推力的{pct(top_lo, 0)}%：损失全在跟最难的那几个较劲。<bookmark mark='b'/>τ为{hi_t}时，它们只占"
        "{pct(top_hi, 0)}%；推力分散到所有负样本上。<bookmark mark='c'/>可是一个难负样本，往往只是另一个长得像这个5的5。把它推开，"
        "就把一个类撕开了；不管它，球面又会聚成一团。王峰和刘华平把这称为均匀性与容忍度的两难。",

    # ------------------------------------------------------------------ Collapse
    'Chapter six. Collapse.':
        '第6章。坍缩。',

    'Before going further, a question.':
        "继续之前，先问一个问题。假如唯一的规则是：让每个数字的两个视图得到同一个向量。没有负样本，没有任何东西把它们推开。"
        "网络会学到什么？先停下来想一想。<bookmark mark='a'/>这是我们的网络做的事。损失是两个视图向量之间余弦的相反数，网络把它降到最低"
        "<bookmark mark='b'/>的办法是：把每个数字都送到同一个点上。两个视图完全一致，损失停在最小值，而这个向量对输入什么也没说。"
        "这就是坍缩。",

    'f"To see collapse in a network with many output numbers':
        "要在输出有很多个数的网络里看到坍缩，我们需要一个度量。有效秩取一组向量的奇异值，把它们变成比例，然后问有多少个方向承担了权重："
        "如果每个向量都指向同一个方向，就是1；如果它们铺满了空间，最多等于维数。<bookmark mark='a'/>SimCLR把它的向量分布在它{dim}个维度"
        "中的大约{r_s:.0f}个上。<bookmark mark='b'/>只把两者拉到一起的网络降到了{r_n:.1f}：一个方向。",

    'f"The whole spectrum shows more.':
        "整个谱能说明更多。这是两个网络向量的奇异值，从大到小，取对数刻度。<bookmark mark='a'/>坍缩的网络只有一个方向，然后什么都没有。"
        "<bookmark mark='b'/>{drop}即使是对比学习，也留下了一部分空间没有用上。这叫作维度坍缩，是完全坍缩温和一些的表亲；"
        "景立、杨立昆和同事把它归因于强烈的数据增强，以及各层权重共同演化的方式。",

    'f\'SimCLR declines slowly and then drops off a cliff':
        'SimCLR先缓慢下降，然后掉下悬崖：大约{cliff}个方向之后，其余方向比第一个弱一千倍。',

    'SimCLR declines slowly, and its weakest directions end far below its strongest.':
        'SimCLR缓慢下降，它最弱的方向远远低于最强的方向。',

    'f"Collapse is not harmless to the network underneath.':
        "坍缩对下面的网络并非无害。坍缩的向量是一个小头的输出；在它下面，编码器的表示h才是我们要留下的。<bookmark mark='a'/>{v}"
        "<bookmark mark='b'/>一旦头对所有输入都输出同样的东西，损失就停在最小值，梯度也消失了：编码器停在坍缩最初那几步把它扔下的地方。",

    'f"Its nearest-neighbour accuracy falls from {pct(k0, 0)} percent':
        '它的近邻准确率从随机网络起步时的{pct(k0, 0)}%降到了{pct(k1, 0)}%。线性探针最后是{pct(fl_)}%，低于未训练网络的{pct(un)}%。',

    "f'Its nearest-neighbour accuracy goes from {pct(k0, 0)} to {pct(k1, 0)} percent":
        '它的近邻准确率从{pct(k0, 0)}%变到{pct(k1, 0)}%，线性探针最后是{pct(fl_)}%，未训练的网络是{pct(un)}%。',

    'This trap is old.':
        "这个陷阱由来已久。2005到2006年，蕾娅·哈德塞尔、苏米特·乔普拉和杨立昆训练孪生网络时，用的损失已经有了两半。"
        "<bookmark mark='a'/>对相似的一对，取两者输出距离的平方：拉近。<bookmark mark='b'/>对不相似的一对，只有当它们比一个间隔更近时"
        "才惩罚：推开，但不多推。没有后一半，就没有什么能阻止网络把一切都映到同一个点上。",

    'Every method from here on is a way out of this trap.':
        "从这里开始的每一种方法，都是走出这个陷阱的一条路。<bookmark mark='a'/>对比式的方法把其他图像推开。<bookmark mark='b'/>BYOL和"
        "SimSiam打破两个分支之间的对称。<bookmark mark='c'/>Barlow Twins和VICReg要求每个维度都保持散开、互不相关。<bookmark mark='d'/>"
        "而DINO让一个老师在两种相反的坍缩之间保持平衡。",

    # ------------------------------------------------------------------ BYOL
    'Chapter seven. No negatives: BYOL and SimSiam.':
        '第7章。没有负样本：BYOL与SimSiam。',

    'In June 2020 a DeepMind team led by Jean-Bastien Grill':
        "2020年6月，让-巴蒂斯特·格里尔带领的DeepMind团队干脆去掉了负样本。<bookmark mark='a'/>BYOL有两个网络。在线网络看一个视图，"
        "再通过一个额外的小网络，也就是预测器，去预测<bookmark mark='b'/>目标网络对另一个视图给出的结果。<bookmark mark='c'/>没有梯度流进"
        "目标网络；它的权重是在线网络权重的缓慢移动平均。<bookmark mark='d'/>没有任何东西把图像推开，它却没有坍缩，还超过了SimCLR："
        "用ResNet-50在ImageNet上达到74.3%。",

    'f"Five months later, Xinlei Chen and Kaiming He removed the moving average too.':
        "五个月后，陈鑫磊和何恺明把移动平均也去掉了。SimSiam只有一个网络，用在两个视图上，一边有预测器，另一边有停止梯度："
        "目标向量被当作常数。<bookmark mark='a'/>我们训练了它，带停止梯度三次，不带两次。<bookmark mark='b'/>{v}<bookmark mark='c'/>"
        "在球面上，用3个输出数，SimSiam不用推就把数字分开了，而只拉不推的网络停在一个点上。",

    "f'With the stop-gradient, the spread holds at {sg_end:.3f}; without it, it falls":
        '有停止梯度时，散度保持在{sg_end:.3f}；没有它，散度降到{no_end:.3f}，有效秩降到{r_no:.1f}，而有它时是{r_sg:.0f}。'
        '删掉一行代码，网络就坍缩了。',

    "f'With the stop-gradient, the spread ends at {sg_end:.3f}; without it, at":
        '有停止梯度时，散度最后是{sg_end:.3f}；没有它，是{no_end:.3f}。',

    'Why does one stop-gradient matter so much?':
        "为什么一个停止梯度这么重要？陈鑫磊和何恺明给了一个解释。设想每张图像都有一个自由的目标向量η，损失把每个视图的输出拉向它所属"
        "图像的目标。<bookmark mark='a'/>轮流来最小化它。固定目标，对网络走一步梯度：这恰恰就是停止梯度所做的。<bookmark mark='b'/>固定"
        "网络，最好的目标就是这张图像所有视图输出的平均。<bookmark mark='c'/>SimSiam用一个抽样的视图代替平均，预测器学着补上其中的差别。"
        "<bookmark mark='d'/>坍缩成常数仍然能使损失最小；只是这种下降方式不会走到那里。田渊栋、陈鑫磊和苏里亚·甘古利推导出了其中的"
        "动力学：预测器和停止梯度一起，让有用的方向不会消亡。",

    'f"How do they compare, on the same budget?':
        "在同一份预算下，它们比起来怎样？<bookmark mark='a'/>{line}<bookmark mark='b'/>每个数字10个标签时：SimCLR {pct(few[0][0])}，"
        "BYOL {pct(few[1][0])}，SimSiam {pct(few[2][0])}%。<bookmark mark='c'/>还有一个转折：有人怀疑BYOL暗地里是对比式的，"
        "因为批归一化会在一批之间混合信息。它的作者换成了一种一次只看一张图像的归一化，达到了73.9%。",

    "f'At our budget the three land within {pct(diff)} points":
        '在我们的预算下，三者在线性探针上相差不到{pct(diff)}个百分点，{leader}领先。',

    "f'At our budget {leader} leads the linear probe":
        '在我们的预算下，{leader}在线性探针上领先，比最后一名高{pct(diff)}个百分点。',

    # ------------------------------------------------------------------ Barlow
    'Chapter eight. Decorrelate: Barlow Twins and VICReg.':
        '第8章。去相关：Barlow Twins与VICReg。',

    'In 1961 the neuroscientist Horace Barlow argued':
        "1961年，神经科学家霍勒斯·巴洛主张，感官应该把输入重新编码，让每个神经元都携带别的神经元没有的东西。<bookmark mark='a'/>六十年后，"
        "尤雷·兹邦塔尔、景立、伊尚·米斯拉、杨立昆和斯特凡·德尼用他的名字命名了一个方法。把一批的两个视图都送进网络，再把一个视图的"
        "每个输出维度和另一个视图的每个维度求相关。<bookmark mark='b'/>损失希望这个矩阵是单位矩阵。对角线上，每个维度在两个视图之间"
        "必须一致：这是不变性。<bookmark mark='c'/>对角线之外，不同的维度必须互不相关：没有冗余。常数输出满足不了对角线，因为相关需要"
        "变化。坍缩被损失本身排除了。",

    'f"Here is the matrix in our Barlow Twins':
        "这是我们的Barlow Twins里的这个矩阵，取它512个维度中的前24个，在测试数字上边训练边测。<bookmark mark='a'/>一开始它是噪声。"
        "<bookmark mark='b'/>随着每个维度学会忽略视图之间的变化，对角线亮了起来，平均相关达到{dg[-1]:.2f}，<bookmark mark='c'/>其余部分"
        "暗了下去，非对角线上的典型相关是{np.sqrt(off[-1]):.3f}。512个维度，每个都说着不同的东西，每个在视图变化下都保持稳定。",

    'f"VICReg, from Adrien Bardes, Jean Ponce and Yann LeCun':
        "VICReg出自阿德里安·巴尔德、让·蓬斯和杨立昆，它把同一个想法拆成三个有名字的项。<bookmark mark='a'/>不变项：两个视图的向量应该"
        "接近。<bookmark mark='b'/>方差项：每个维度在一批里的标准差至少要保持为1，这是一个合页，只在某个维度开始坍缩时才起作用。"
        "<bookmark mark='c'/>协方差项：不同的维度不应该相关。<bookmark mark='d'/>每一项都可以去掉，看看它起什么作用，于是我们去掉了"
        "方差项。{v}",

    "f'Without it, the spread of each dimension falls to {s_n:.3f}":
        '去掉之后，每个维度的散度降到{s_n:.3f}：另外两项最喜欢一切都是零，网络就照办了。它的近邻准确率最后是{pct(kn)}%，'
        'VICReg是{pct(kv)}%。',

    "f'Without it, the spread ends at {s_n:.2f}, against {s_v:.2f}.'":
        '去掉之后，散度最后是{s_n:.2f}，而VICReg是{s_v:.2f}。',

    'f"The two families are closer than they look.':
        "这两个家族比看上去更接近。对比损失让一批里的图像彼此不相似；Barlow Twins和VICReg让维度彼此不相似。<bookmark mark='a'/>"
        "昆汀·加里多和同事证明，把式子写出来，两者几乎是同一个目标，一个作用在数据的行上，另一个作用在列上。<bookmark mark='b'/>{line}"
        "<bookmark mark='c'/>这条线上最新的是LeJEPA，2025年由兰德尔·巴莱斯特里耶罗和杨立昆提出：只把向量推向各向同性的高斯分布，"
        "别的什么都不要，没有停止梯度，没有老师。",

    'On our digits, Barlow Twins and VICReg match SimCLR to within a point.':
        '在我们的数字上，Barlow Twins和VICReg与SimCLR相差不到一个百分点。',

    "f'On our digits: SimCLR {pct(sc)}, Barlow Twins {pct(bt)}, VICReg {pct(vr)} percent.'":
        '在我们的数字上：SimCLR {pct(sc)}%，Barlow Twins {pct(bt)}%，VICReg {pct(vr)}%。',

    # ------------------------------------------------------------------ DINO
    'Chapter nine. Self-distillation: DINO.':
        '第9章。自蒸馏：DINO。',

    'Mathilde Caron and colleagues at Facebook':
        "玛蒂尔德·卡龙和她在Facebook的同事，多年来一直用聚类来教网络：先把图像分组，再学着预测这些组。<bookmark mark='a'/>2021年，"
        "他们把它变成了无标签的蒸馏：DINO。学生网络看一个视图，<bookmark mark='b'/>输出在K个原型上的概率，原型是它空间里学出来的方向。"
        "<bookmark mark='c'/>老师看另一个视图，做同样的事，<bookmark mark='d'/>学生被训练去匹配老师的概率，用的是交叉熵。老师根本不训练："
        "它的权重是学生权重的移动平均，和BYOL一样。",

    'A student copying a teacher that copies the student':
        "学生模仿老师，老师又模仿学生，这样可能以两种相反的方式坍缩。<bookmark mark='a'/>一个原型可能对所有图像都胜出：老师总是满怀自信"
        "地说同一件事。<bookmark mark='b'/>或者每个原型对每张图像都一样可能：老师什么也没说。<bookmark mark='c'/>DINO的答案是对老师施加两种"
        "相反的压力。中心化减去老师输出的移动平均，于是没有哪个原型能对所有人都胜出；单靠它，结果会漂向均匀的答案。"
        "<bookmark mark='d'/>锐化让老师的温度比学生低，于是它的回答更自信；单靠它，结果会漂向唯一的胜者。<bookmark mark='e'/>损失可以"
        "拆成老师的熵，加上两者之间的KL；任何一种坍缩都会把KL推到零，而熵卡在一端。",

    'f"We trained DINO, and DINO with each half of the balance removed.':
        "我们训练了DINO，以及分别去掉平衡中一半的DINO。<bookmark mark='a'/>左边是老师回答的熵；右边是老师和学生之间的KL。"
        "<bookmark mark='b'/>{v}",

    'f"Without centring, the teacher\'s entropy falls to':
        "没有中心化，老师的熵降到{Hn['nocenter']:.2f}：所有东西都归一个原型。没有锐化，熵升到{Hn['nosharpen']:.2f}，也就是{K}的对数："
        "每个原型都一样。两种情况下，KL都降到几乎为零，学生没有东西可学了。两者都有时，熵稳定在{Hn['dino']:.2f}，KL保持在"
        "{KLn['dino']:.2f}：还有东西可学。",

    'f"The teacher\'s entropy ends at {Hn[\'nocenter\']:.2f} without centring':
        "老师的熵最后：没有中心化时是{Hn['nocenter']:.2f}，没有锐化时是{Hn['nosharpen']:.2f}，两者都有时是{Hn['dino']:.2f}。",

    'f"The same story, as the teacher\'s average answer':
        "同一个故事，换成老师在512个测试数字上的平均回答，按使用最多的原型往下排。<bookmark mark='a'/>没有中心化，一根柱子拿走一切："
        "到最后，只有{u['nocenter']:.1f}个原型在用。没有锐化，柱子变平，全部{u['nosharpen']:.0f}个都被平均地使用，每个数字都一样。"
        "<bookmark mark='b'/>DINO在不同数字之间用着{u['dino']:.0f}个原型，而每个数字自己的回答依然自信。",

    'f"And the representation?':
        "那么表示呢？<bookmark mark='a'/>{v}<bookmark mark='b'/>在ImageNet上配合视觉Transformer，DINO是一个转折点：小模型用近邻法达到78.3%，"
        "它最后一层的注意力描出了物体的轮廓，尽管从来没有人给它看过轮廓。",

    'f"At our small budget DINO is behind SimCLR':
        "在我们的小预算下，DINO落后于SimCLR：线性探针{pct(ds['linear'][0])}%，SimCLR是{pct(ss['linear'][0])}%。大家知道自蒸馏需要长时间"
        "训练，DINO论文自己的训练有几百轮；我们的只有几轮。",

    'f"At our budget DINO reaches':
        "在我们的预算下，DINO的线性探针达到{pct(ds['linear'][0])}%，SimCLR是{pct(ss['linear'][0])}%。",
})

ZH.update({
    # ------------------------------------------------------------------ Scale
    'Chapter ten. Scale and curation.':
        '第10章。规模与数据筛选。',

    "To scale self-distillation, Meta's DINOv2 team":
        "为了把自蒸馏做大，Meta的DINOv2团队在2023年发现，数据和模型一样重要。网上的原始图像被少数几类图片占据，还大量重复。"
        "<bookmark mark='a'/>于是他们靠检索来构建数据集。从ImageNet这样精选的数据集出发；<bookmark mark='b'/>用一个自监督网络给12亿张"
        "去过重的网络图像做嵌入；让每张精选图像从图像池里取回它最近的4个邻居。<bookmark mark='c'/>得到的1.42亿张图像，训练了一个"
        "11亿参数的视觉Transformer，<bookmark mark='d'/>损失是DINO的损失，加上一个掩码词元项和一个把向量铺开的项：在ImageNet上用"
        "线性探针达到86.5%，而它从没见过一个标签。",

    'f"We can try the same recipe on digits.':
        "我们可以在数字上试同样的配方。取{int(pc.sum()):,}个训练数字，像网络图像那样不均衡：最常见的数字{common}占了图像池的"
        "{pct(pc[common] / pc.sum(), 0)}%，最少的只占{pct(pc.min() / pc.sum(), 1)}%。<bookmark mark='a'/>然后筛选：一个1000个数字的"
        "小而均衡的集合，每个数字100个，扮演精选数据集。每个从池里取回它最近的4个邻居，嵌入用的是我们的SimCLR网络，重复的去掉。"
        "<bookmark mark='b'/>筛选后的池有{int(cc.sum()):,}个数字，最常见与最少见类别的比例从{ratio_raw:.0f}比1缩小到{ratio_cur:.1f}比1。",

    'f"Then train the same SimCLR, for the same number of steps, on each pool':
        "然后在每个池上训练同样的SimCLR，步数相同，并在通常那个均衡的测试集上测试。<bookmark mark='a'/>这是每个数字上的准确率，原始池里"
        "最常见的放在左边。<bookmark mark='b'/>{v}",

    'f"On the three rarest digits, the curated pool\'s network is better by':
        "在最少见的三个数字上，用筛选池训练的网络好了{pct(gain_rare)}个百分点；在最常见的三个上，差别是{pct(gain_common)}。总体："
        "线性探针{pct(lc)}%对{pct(lr)}%，每个数字10个标签时{pct(fc)}%对{pct(fr)}%，而图像池小了{n_r / n_c:.0f}倍。",

    'f"On the three rarest digits the curated pool\'s network is not better':
        "在最少见的三个数字上，用筛选池训练的网络并没有更好：差别是{pct(gain_rare)}个百分点。总体：线性探针{pct(lc)}%对{pct(lr)}%，"
        "而图像池小了{n_r / n_c:.0f}倍。只有十种数字时，即使是少见的那些，也已经见得够多了。",

    'In August 2025 came DINOv3':
        "2025年8月，DINOv3问世：一个70亿参数的Transformer，在17亿张图像上训练，这些图是从大约170亿张里挑出来的，<bookmark mark='a'/>"
        "办法是把它们分五层聚类，再从各个簇里均匀抽样，加上检索。<bookmark mark='b'/>它在ImageNet上的线性探针达到88.4%，和用文字说明"
        "训练的最好模型相差不到一个百分点。<bookmark mark='c'/>它的新成分解决了长时间训练的一个问题：分割所需要的单个图像块的特征，"
        "会随着全局特征变好而变差。格拉姆锚定让学生的图像块之间的相似度，保持在一个较早检查点的水平上。",

    'Is language necessary?':
        "语言是必需的吗？用文字说明训练的视觉模型，比如第23部分的CLIP，在视觉问答上一直领先，但它们用的训练数据也不一样。"
        "<bookmark mark='a'/>2025年，范大卫、谢赛宁和同事在同样的20亿张图像上把两种都训练了一遍。在70亿参数时，从没见过一句文字说明的"
        "DINO式模型在16个问答任务上平均得到53.87分；CLIP模型是52.97分。<bookmark mark='b'/>自监督模型随着规模变大一直在进步。"
        "<bookmark mark='c'/>而对于关于文字和图表的问题，数据又一次起了作用：只保留含有文字的图像，就胜过了一个用文字说明训练的模型。",

    # ------------------------------------------------------------------ Masked
    'Chapter eleven. Fill in the blanks: MAE and BEiT.':
        '第11章。填空：MAE与BEiT。',

    'The second family hides part of the input and asks for it back.':
        "第二个家族藏起输入的一部分，再让网络把它找回来。2008年，去噪自编码器破坏一个输入，再学着把它复原。<bookmark mark='a'/>2018年，"
        "BERT藏起一个句子里15%的词，靠猜这些词学会了语言，第14部分讲过。<bookmark mark='b'/>2021年，这个想法两次来到视觉Transformer上："
        "BEiT预测被藏起的图像块的离散词元，MAE预测它们的像素。<bookmark mark='c'/>和文本相比，最大的变化是藏多少。词语里的含义很密集；"
        "图像却很冗余，一个相邻的像素就能把被藏的像素泄露大半。MAE藏起图像的四分之三。",

    "Kaiming He's masked autoencoder is simple.":
        "何恺明的掩码自编码器很简单。把图像切成小块，随机藏起其中四分之三，<bookmark mark='a'/>对剩下的编码，<bookmark mark='b'/>"
        "再让一个小解码器画出整张图像，只按它看不见的那些块打分。<bookmark mark='c'/>MAE的编码器是视觉Transformer，它可以直接跳过被藏的"
        "块，所以训练快了三倍以上；经过微调，最大的模型在ImageNet上达到87.8%。<bookmark mark='d'/>我们的版本和本部分其他所有方法一样，"
        "用的是同一个卷积网络，所以被藏的块是被涂黑，而不是被跳过。49个4乘4像素的块，藏起其中37个。",

    'Here is ours learning, on six test digits':
        "这是我们的模型在学习，用六个测试数字，每个快照里藏起的块都一样。<bookmark mark='a'/>一开始，解码器画出一团灰糊。几十步之内，"
        "它就学会了画面大部分是黑的，<bookmark mark='b'/>接着学会笔画会落在哪里，到最后，它能补出它从没见过的笔画，把看得见的那些接下去。"
        "<bookmark mark='c'/>要做到这一点，它得懂一点数字是怎么写的。",

    '"How much to hide?':
        "藏多少？藏得太少，网络可以从邻居那里照抄；藏得太多，它只能瞎猜。<bookmark mark='a'/>我们在三个比例下训练了它。"
        "<bookmark mark='b'/>{v}",

    "f'Hiding three quarters gives the best probe":
        '藏起四分之三时探针最好，{pct(lin[1][0])}%；藏一半是{pct(lin[0][0])}%，藏十分之九是{pct(lin[2][0])}%。',

    "f'On our digits the best ratio is {pct(float(best), 0)} percent hidden":
        '在我们的数字上，最好的比例是藏起{pct(float(best), 0)}%：藏一半、四分之三和十分之九时，探针分别是{pct(lin[0][0])}%、'
        '{pct(lin[1][0])}%和{pct(lin[2][0])}%。',

    'f"BEiT\'s targets are tokens instead of pixels.':
        "BEiT的目标是词元，而不是像素。它借用了OpenAI第一代DALL·E的图像分词器，把每个块变成8000多个离散编码中的一个。"
        "<bookmark mark='a'/>我们的更简单，是第23部分里那样的码本：在4乘4的块上做k均值，64个编码。<bookmark mark='b'/>一个数字变成49个"
        "词元，<bookmark mark='c'/>网络看到的是藏起了40%块的数字，必须说出每个被藏块的编码，就像BERT说出被藏的词。到最后，它答对的比例是"
        "{pct(np.mean(accs), 0)}%。",

    'f"So, does filling in teach what a digit is?':
        "那么，填空能教会网络什么是数字吗？<bookmark mark='a'/>{v}<bookmark mark='b'/>在大规模上也是同样的规律：MAE的线性探针落后于"
        "对比式方法，只有在整个网络都被微调之后，它才大放异彩。像素目标让网络把力气花在精确的笔画上，而其中很多是分类器用不上的。"
        "这就引出了第三条路：去预测，但不预测像素。",

    'f"Not on our network. Filling in pixels leaves a representation':
        "在我们的网络上不能。填像素留下的表示，线性探针只有{pct(ml)}%，甚至低于未训练网络的{pct(un)}%，远低于SimCLR的{pct(sl)}%；"
        "预测编码得到{pct(bl)}%。为了画出笔画，那张小特征图的每个格子学的是它附近哪里有墨迹；在整张图上一平均，这些对“是哪个数字”"
        "就说明不了多少了。",

    "f'Filling in pixels gives a representation {pct(sl - ml)} points behind SimCLR":
        '填像素得到的表示，在线性探针上比SimCLR落后{pct(sl - ml)}个百分点，用近邻法落后{pct(sk - mk)}个百分点。预测编码而不是像素，'
        '得到{pct(bl)}%。',

    'f"On our digits, filling in pixels does as well as contrast':
        "在我们的数字上，填像素和对比做得一样好：MAE {pct(ml)}%，SimCLR {pct(sl)}%，预测编码的模型{pct(bl)}%。",

    # ------------------------------------------------------------------ JEPA
    'Chapter twelve. Predict the meaning, not the pixels.':
        '第12章。预测含义，而不是像素。',

    'In 2022 Yann LeCun laid out the third way':
        "2022年，杨立昆在一篇关于机器怎样学会世界模型的长文里，提出了第三条路。<bookmark mark='a'/>联合嵌入的方法，就像第4章以来的所有"
        "方法，让两个视图一致；它们需要人工设计的视图，还需要防止坍缩。<bookmark mark='b'/>生成式的方法，比如MAE，预测被藏部分的像素，"
        "每一个细节，可预测的和不可预测的都一样。<bookmark mark='c'/>联合嵌入预测架构，也就是JEPA，转而预测被藏部分的编码：由网络决定"
        "被藏部分里哪些值得预测，其余的可以丢掉。",

    'LeCun frames all of this with energies':
        "杨立昆用能量来描述这一切，也就是第20部分的语言。JEPA的能量就是它的预测误差：y和x相符时低，不符时高。<bookmark mark='a'/>坍缩"
        "就是处处都低的能量：每个y都和每个x相符。<bookmark mark='b'/>有两种办法给它塑形。对比式的方法在真实的对上压低能量，在选出的负样本"
        "上抬高能量，word2vec和SimCLR就是这样。<bookmark mark='c'/>正则化的方法则限制空间里有多少地方能有低能量：VICReg的方差下限、"
        "Barlow的去相关，以及BYOL、DINO和JEPA的预测器与移动平均。杨立昆认为第二种更容易扩展，因为在高维空间里，需要推的地方太多了。",

    'I-JEPA, from Mahmoud Assran and colleagues in 2023':
        "I-JEPA是2023年马哈茂德·阿斯兰和同事提出的图像版本。藏起图像的几个块。<bookmark mark='a'/>上下文编码器看剩下的部分。"
        "<bookmark mark='b'/>目标编码器是上下文编码器的缓慢移动平均，和BYOL一样，它看整张图像，它在被藏块上的输出就是目标。"
        "<bookmark mark='c'/>预测器被告知被藏块的位置，必须从上下文里给出那个目标。不预测任何像素，除了裁剪也不需要别的视图。"
        "<bookmark mark='d'/>我们的版本和其他方法用同一个网络：目标是它最后那张4乘4特征图上的格子，两个2乘2的块。",

    'f"We trained I-JEPA, MAE and SimCLR on the same network':
        "我们在同一个网络上、用同样的步数训练了I-JEPA、MAE和SimCLR。<bookmark mark='a'/>{v}<bookmark mark='b'/>在论文里，用最大的"
        "视觉Transformer，I-JEPA的线性探针胜过了MAE，79.3%对77.2%，用的计算量少了十倍以上。",

    'f"Predicting the meaning beats predicting the pixels: I-JEPA\'s linear probe reaches {pct(jl)} percent, MAE\'s {pct(ml)}, and':
        "预测含义胜过预测像素：I-JEPA的线性探针达到{pct(jl)}%，MAE是{pct(ml)}%，而用人工视图的SimCLR是{pct(Sm['linear'][0])}%。",

    'f"Predicting the meaning beats predicting the pixels: I-JEPA\'s linear probe reaches {pct(jl)} percent, MAE\'s {pct(ml)}, ahead':
        "预测含义胜过预测像素：I-JEPA的线性探针达到{pct(jl)}%，MAE是{pct(ml)}%，甚至超过了SimCLR的{pct(Sm['linear'][0])}%。",

    "f'On our digits, predicting the encoding does not beat predicting the pixels":
        '在我们的数字上，预测编码并没有胜过预测像素：I-JEPA的线性探针是{pct(jl)}%，MAE是{pct(ml)}%。4乘4的特征图是一个粗糙的目标，'
        '而我们的预算也很短。',

    "f'On our digits the two are level":
        '在我们的数字上，两者持平：I-JEPA {pct(jl)}%，MAE {pct(ml)}%。',

    'On video, the idea becomes a model of the world.':
        "在视频上，这个想法变成了一个世界模型。V-JEPA预测被藏起的时空块。<bookmark mark='a'/>2025年6月的V-JEPA 2在一百多万小时的视频"
        "上训练。然后，用不到62小时的无标签机器人视频，它学会了机械臂的动作怎样改变它看到的东西，并且能在从没见过的实验室里抓取和放置"
        "物体，办法是搜索那些预测结果看起来像目标图片的动作。<bookmark mark='b'/>它2026年的后继者为每个图像块学到细致的特征，抓取也更"
        "可靠。<bookmark mark='c'/>而LeJEPA干脆去掉了停止梯度和老师。世界模型会在第29部分回来。",

    # ------------------------------------------------------------------ Budget
    'Chapter thirteen. Every method, one budget.':
        '第13章。所有方法，同一份预算。',

    'f"Here is every method, trained on the same network':
        "这是每一种方法，在同一个网络上、用同样的步数、从三个随机起点训练，用全部标签的线性探针来评判。<bookmark mark='a'/>最上面是作为"
        "参照的监督网络：{pct(s_)}%。<bookmark mark='b'/>不用标签的方法里最好的是{SPOKEN.get(best, best)}，{pct(b)}%，落后"
        "{pct(s_ - b)}个百分点。<bookmark mark='c'/>学习过的方法里垫底的是{SPOKEN.get(worst, worst)}，{pct(rows[worst]['linear'][0])}%；"
        "未训练的网络得到{pct(un)}%，原始像素得到{pct(rows['pixels']['linear'][0])}%。<bookmark mark='d'/>{below_s}",

    'f\'{len(below)} of the learned methods score below the untrained network.\'':
        '学习过的方法里，有{len(below)}种低于未训练的网络。',

    "f'One learned method scores below the untrained network":
        '有一种学习过的方法低于未训练的网络：{SPOKEN.get(below[0], below[0])}。',

    'Every learned method beats the untrained network.':
        '每一种学习过的方法都胜过了未训练的网络。',

    'f"The full probe flatters everyone':
        "完整的探针让每个方法都显得不错：有6万个标签，连原始像素都表现很好。自监督学习当初要回答的问题是：只有很少的标签时能做什么。"
        "<bookmark mark='a'/>所以：每种数字只用10个带标签的样本，训练一个线性分类器。<bookmark mark='b'/>{v}<bookmark mark='c'/>原始像素"
        "得到{pct(px)}%；监督网络在做这个每类10个标签的探针之前，已经用全部6万个标签训练过，得到{pct(s_)}%。从{pct(px)}%到{pct(b)}%"
        "的这段差距，就是那些无标签的数字教给网络的。",

    "f'The leader is the same: {lead}":
        '领先的还是同一个：{lead}，用100个标签得到{pct(b)}%。',

    "f'The order changes:":
        "名次变了：这里领先的是{SPOKEN.get(best, best)}，用100个标签得到{pct(b)}%，而在完整探针上最好的{SPOKEN.get(lin_best, lin_best)}"
        "得到{pct(rows[lin_best]['few'][0])}%。",

    'f"A frozen network is one test.':
        "冻结的网络是一种检验。另一种常用的检验让整个网络都可以改变，从它学到的东西出发，用同样的100个标签。<bookmark mark='a'/>从零开始"
        "用100个数字训练，我们的网络达到{pct(sc)}%。<bookmark mark='b'/>{len(ssl)}个自监督的起点里，有{n_up}个超过了它；最好的是"
        "{SPOKEN.get(best, best)}，{pct(rows[best]['ft'][0])}%。<bookmark mark='c'/>{mv}",

    "f'The masked models gain the most from it":
        "掩码模型从中获益最多：MAE从冻结网络的{pct(lin['mae'])}%升到微调后的{pct(mae)}%，I-JEPA从{pct(lin['ijepa'])}%升到{pct(ij)}%。",

    "f'Fine-tuning helps the masked models less than the literature would suggest":
        '微调对掩码模型的帮助比文献所说的要小：MAE最后是{pct(mae)}%，I-JEPA是{pct(ij)}%。',

    '"Chapter five\'s two numbers can be measured':
        "第5章的那两个数，可以在每种方法的表示上测量，而不只是SimCLR的。<bookmark mark='a'/>这里每种方法都放在它的均匀性和对齐的位置上。"
        "<bookmark mark='b'/>{v}",

    "f'Lower is better for both, so Wang and Isola predict negative correlations, and both are":
        "两者都是越低越好，所以王同舟和伊索拉预测相关是负的，而两个都是：均匀性{ru:.2f}，对齐{ra:.2f}。",

    'f"Lower is better for both, so Wang and Isola predict negative correlations. Uniformity':
        "两者都是越低越好，所以王同舟和伊索拉预测相关是负的。均匀性的相关很强，{ru:.2f}；对齐的只有{ra:.2f}：能让点保持散开的方法表现"
        "更好，不管它们把视图抓得多紧。",

    'f"Lower is better for both, so Wang and Isola predict negative correlations. Alignment':
        "两者都是越低越好，所以王同舟和伊索拉预测相关是负的。对齐的相关很强，{ra:.2f}；均匀性的只有{ru:.2f}。",

    "f'Lower is better for both, so Wang and Isola predict negative correlations; across":
        "两者都是越低越好，所以王同舟和伊索拉预测相关是负的；在我们的方法之间，两者都很弱：均匀性{ru:.2f}，对齐{ra:.2f}。",

    'f"Can you tell which representation is good without any labels at all?':
        "能不能完全不用标签，就看出哪个表示好？昆汀·加里多和同事提出了有效秩：在他们的实验里，向量占满更多维度的方法，下游表现更好。"
        "<bookmark mark='a'/>这里是我们每种方法的有效秩，和它在10个标签检验上的准确率。<bookmark mark='b'/>{v}",

    "f'Across our methods, the rank correlation is {rho:.2f}: a fuller":
        '在我们的方法之间，秩相关是{rho:.2f}：表示越饱满，通常也越好，和RankMe的发现一致。',

    "f'Across our methods, the rank correlation is only {rho:.2f}":
        '在我们的方法之间，秩相关只有{rho:.2f}：只是个暗示，不是规律。',

    "f'Across our methods, the rank correlation is {rho:.2f}: no useful":
        '在我们的方法之间，秩相关是{rho:.2f}：没有有用的关系。把维度占满，本身并不能让它们有用。',
})

ZH.update({
    # ------------------------------------------------------------------ Embeddings
    'f"How far should this scoreboard be trusted?':
        "这张记分牌该信几分？它只是一个小网络、800次更新、十种数字。<bookmark mark='a'/>已知需要长时间训练的方法，DINO和掩码模型，"
        "在这么短的预算下吃亏。<bookmark mark='b'/>在ImageNet的规模上，用视觉Transformer，名次就不一样了：DINO这一系在冻结特征上领先，"
        "掩码模型在微调之后表现很好。<bookmark mark='c'/>在这里，{len(ssl)}种方法中有{len(good)}种，在没有一个标签的情况下学到了足够多"
        "关于数字的东西，在每个数字只给10个标签时胜过了未训练的网络。",

    'f"One meter for all of them':
        "给它们用同一个仪表：嵌入的散度，缩放成1表示向量均匀铺满球面，0表示已经坍缩。<bookmark mark='a'/>SimCLR最后是"
        "{ends['simclr']:.2f}，BYOL是{ends['byol']:.2f}，SimSiam是{ends['simsiam']:.2f}。<bookmark mark='b'/>没有停止梯度时，SimSiam"
        "最后是{ends['simsiam_nosg']:.2f}，只拉不推的网络是{ends['naive']:.2f}。",

    'Chapter fourteen. Embeddings for search.':
        '第14章。用于搜索的嵌入。',

    'f"Everything so far was judged by how well a classifier could read the vectors.':
        "到目前为止，一切都是按分类器能多好地读出向量来评判的。可世界上很多地方直接拿向量来用，用来搜索。<bookmark mark='a'/>每个条目"
        "嵌入一次；把查询也嵌入；返回向量最近的那些条目。<bookmark mark='b'/>这是我们的SimCLR网络当作数字搜索引擎：四个查询和它们最近的"
        "测试数字，同一个数字的标绿。其中{pct(same, 0)}%是对的。<bookmark mark='c'/>在整个网络的规模上，最近邻是近似找到的，靠的是在"
        "数十亿个向量上搭建的图。",

    "Search engines today mostly embed text":
        "今天的搜索引擎主要是给文本做嵌入，这段历史从第3部分的词向量一直延续到这里。<bookmark mark='a'/>2019年的Sentence-BERT训练孪生"
        "网络，把相似的句子放到一起。2020年的DPR把问题和段落配对，把同一批里的其他段落当作负样本：又是InfoNCE。<bookmark mark='b'/>"
        "2021年的SimCSE连配对都不需要：把同一个句子输入两次，网络里随机的dropout就造出了两个视图。<bookmark mark='c'/>接着是在数亿对"
        "网络文本上的对比预训练，以及一个用来比较结果的基准，MTEB。<bookmark mark='d'/>今天领先的是被改造成编码器的语言模型。2025年的"
        "Qwen3-Embedding用InfoNCE和温度来训练；<bookmark mark='e'/>谷歌2026年的Gemini Embedding 2把文本、图像、视频和声音放进同一个"
        "空间。同样的损失，以图片和文字说明作为两个视图，就是第23部分里训练CLIP和SigLIP的方法。",

    'Vectors cost memory: a billion items at a thousand numbers each is four terabytes.':
        "向量要占内存：十亿个条目，每个一千个数，就是4TB。人们常常想先用短向量搜一遍，再用长向量细化。<bookmark mark='a'/>套娃表示学习"
        "出自2022年阿迪蒂亚·库苏帕蒂和同事，它训练一个向量，让它的前两个数、前四个数、前八个数，依此类推，每一段单独拿出来都是一个好的"
        "嵌入，就像一个套一个的俄罗斯套娃。<bookmark mark='b'/>损失就是把通常的损失用在每一个前缀上，再取平均。<bookmark mark='c'/>"
        "Qwen3-Embedding支持它，OpenAI 2024年的模型也能这样截短：截到256个数，大模型仍然胜过它前代模型完整的1536个数。",

    'f"We trained SimCLR with the Matryoshka loss, three times':
        "我们用套娃损失训练了SimCLR三次，并和普通的SimCLR比较，后者的向量只是被直接截短。<bookmark mark='a'/>各自只保留前几个数，"
        "重新归一化，再问最近邻。<bookmark mark='b'/>{v}",

    "f'With only four numbers, the ordinary embedding finds the right digit":
        '只用4个数时，普通的嵌入找对数字的比例是{pct(p4, 0)}%；套娃嵌入是{pct(m4, 0)}%。用完整的128个数时，两者相差不到'
        '{pct(abs(pf - mf))}个百分点。',

    "f'With four numbers: {pct(p4, 0)} percent for the ordinary embedding":
        '用4个数时：普通嵌入{pct(p4, 0)}%，套娃嵌入{pct(m4, 0)}%。',

    'f"Here is what that means for search:':
        "这对搜索意味着什么：同样六个查询，只用前4个数来回答。<bookmark mark='a'/>截短后，普通的SimCLR返回同一个数字的比例是"
        "{pct(fa, 0)}%；<bookmark mark='b'/>套娃嵌入是{pct(fb, 0)}%。一个向量，训练一次，就能按预算截短。",

    # ------------------------------------------------------------------ Platonic
    'Chapter fifteen. Do all models see the same world?':
        '第15章。所有模型看到的是同一个世界吗？',

    'How do you compare what two networks learned?':
        "怎样比较两个网络学到的东西？它们的坐标本身毫无意义：把一个表示旋转一下，它知道的东西一点也没变。所以要比较几何。对一组输入，"
        "在每个表示里列出每一对输入有多相似。<bookmark mark='a'/>把这两张表中心化，测量它们有多像：这个统计量叫作HSIC。<bookmark mark='b'/>"
        "用普通的点积时，它就变成两个中心化表示的互乘积的大小的平方。<bookmark mark='c'/>再归一化，就得到中心化核对齐，CKA：两者几何"
        "相同时为1。<bookmark mark='d'/>它不在乎旋转和整体缩放，但正如西蒙·科恩布利斯和合作者所说，它并不是对任何可逆映射都不变："
        "在高维空间里，一个对所有线性映射都宽容的度量，会认为任何两个网络都完全相同。",

    'f"Here is the CKA between every pair of our representations':
        "这是我们每一对表示之间的CKA，在同样2000个测试数字上算出；越亮越像。<bookmark mark='a'/>学习过的方法里最像的一对是"
        "{SPOKEN.get(names[a], names[a])}和{SPOKEN.get(names[b], names[b])}，{bv:.2f}；<bookmark mark='b'/>最不像的是"
        "{SPOKEN.get(names[wa], names[wa])}和{SPOKEN.get(names[wb], names[wb])}，{wv:.2f}。<bookmark mark='c'/>作为参照：同一个配方"
        "从两个随机起点训练，自己和自己的一致度在{s_lo:.2f}到{s_hi:.2f}之间。",

    'In 2024 Minyoung Huh, Brian Cheung, Tongzhou Wang and Phillip Isola made a bold claim.':
        "2024年，许敏英、布赖恩·张、王同舟和菲利普·伊索拉提出了一个大胆的论断。用不同数据、不同目标、甚至不同感官训练出来的网络，"
        "正在以同样的方式表示世界。用他们的话说：<bookmark mark='a'/>我们假设，这种趋同正在走向一个共同的、关于现实的统计模型。他们把它"
        "叫作柏拉图表示假说，取自柏拉图洞穴墙上的影子。<bookmark mark='b'/>他们的证据：在78个视觉模型里，能力越强的彼此越一致；语言模型"
        "越好，它对一句文字说明的理解，就越和视觉模型对那张图的理解一致。<bookmark mark='c'/>一致性是用共同的近邻来衡量的，而在不同"
        "感官之间，它的绝对值仍然很低。",

    'f"We can run a small version of their first test on our own models.':
        "我们可以在自己的模型上做一个他们第一个检验的小型版本。对每种方法，看它和其他所有方法在共同近邻上的平均一致度，"
        "对比它的表示有多好。<bookmark mark='a'/>{v}",

    "f'The more accurate methods do agree more with the rest":
        '越准确的方法，确实和其他方法更一致：秩相关为{rho:.2f}。正如论文所说：强的模型都是相似的，弱的模型各有各的弱。',

    "f'The relation is weak: a rank correlation of {rho:.2f}.'":
        '这个关系很弱：秩相关为{rho:.2f}。',

    "f'We see no such relation here: the rank correlation is {rho:.2f}.'":
        '我们在这里看不到这样的关系：秩相关为{rho:.2f}。',

    '"A sharper test borrows Becker and Hinton\'s setting from 1992':
        "一个更尖锐的检验借用了贝克尔和辛顿1992年的设定：两个网络看着世界的不同部分。编码器A只看每个数字的上半部分，编码器B只看下半部分。"
        "<bookmark mark='a'/>它们各自单独用SimCLR训练，从不知道对方的存在。它们会在“哪些数字相像”这件事上达成一致吗？"
        "<bookmark mark='b'/>{v_}<bookmark mark='c'/>两种感官，分开训练，却朝着关于同一批数字的同一幅图景靠拢：这是那个假说的缩影。",

    "f'As each learns, they agree more":
        '随着各自学习，它们越来越一致：从开始时的{a0[0]:.2f}，到两次训练中的{a0[-1]:.2f}和{a1[-1]:.2f}，远高于原始像素的{px:.2f}，'
        '但低于两个看同一半的编码器之间的{cs:.2f}。',

    'f"Their agreement goes from {a0[0]:.2f} to':
        "它们的一致度从{a0[0]:.2f}变到{a0[-1]:.2f}和{a1[-1]:.2f}；原始像素的是{px:.2f}。",

    'The authors list the caveats themselves.':
        "作者们自己列出了这些保留意见。不同的感官携带不同的信息：一句文字说明说不尽一张照片里的一切。<bookmark mark='a'/>怎样衡量一致性，"
        "至今仍有争论。<bookmark mark='b'/>趋同可能来自共同的训练数据、共同的架构，或者建造它们的人的共同习惯。<bookmark mark='c'/>而我们的"
        "只是一个只有十种数字的玩具。尽管如此，这是一个很动人的想法：无标签的学习，不管从哪个角度出发，都会找到同样的结构，因为那个结构"
        "真实存在。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock.":
        "来总结一下。前置任务教会网络的是这道题所需要的东西，包括它的盲区。对比损失是在候选之间做分类，也是信息的一个下界，上限是候选数"
        "的对数。在球面上，它是两股力量，对齐与均匀，由温度来平衡。没有东西把它们推开，一致性就会坍缩成常数，而且我们可以测量它。"
        "BYOL和SimSiam靠不对称逃脱，Barlow Twins和VICReg靠维度去相关，DINO靠让老师在两种坍缩之间保持平衡。掩码模型靠填空学习；"
        "JEPA预测的是含义而不是像素。而分开训练、各看同一批数字不同一半的网络，最终达成了一致。",

    'All of this comes back.':
        "这些都会再回来。数据增强教网络该忽略什么；下一次，第25部分会把这种对称性直接造进网络里。<bookmark mark='p2'/>在表示空间里做"
        "预测，是第29部分世界模型的核心。<bookmark mark='p3'/>探针和CKA，是第30部分读出网络知道什么的方法，<bookmark mark='p4'/>套娃式的"
        "嵌套特征也会在那里回来，出现在稀疏自编码器里。<bookmark mark='p5'/>老师和学生会在第27部分的蒸馏里回来；<bookmark mark='p6'/>"
        "而嵌入就是第29部分的智能体所检索的记忆。",

    'Here are six problems to try':
        '这里有六道题，从InfoNCE的界到DINO的两种坍缩。在这里暂停，把它们做一做；完整的解答在本部分的讲义里。',

    'Next time: symmetry.':
        "下一次：对称性。我们的网络学会忽略纸张转动，只是因为我们给它看了转动过的纸张。第25部分会把对称性造进网络里，让它的回答在输入"
        "转动时要么保持不变，要么跟着一起转动，并沿着这个思路，从图一直讲到蛋白质、天气和数学。",

    'To go deeper, the Cookbook of Self-Supervised Learning':
        "想深入的话，兰德尔·巴莱斯特里耶罗等人写的《自监督学习食谱》（A Cookbook of Self-Supervised Learning）是本部分所有内容的实用"
        "指南，凯文·墨菲的第二卷讲了其中的理论。感谢收看，我们第25部分见。",
})

PHRASES.update({
    'the supervised network': '监督网络',
    'rotation prediction': '旋转预测',
    'the Matryoshka model': '套娃模型',
    'the BEiT-style model': 'BEiT式模型',
    'the untrained network': '未训练的网络',
    'raw pixels': '原始像素',
    'SimCLR': 'SimCLR',
    'MoCo': 'MoCo',
    'BYOL': 'BYOL',
    'SimSiam': 'SimSiam',
    'Barlow Twins': 'Barlow Twins',
    'VICReg': 'VICReg',
    'DINO': 'DINO',
    'MAE': 'MAE',
    'I-JEPA': 'I-JEPA',
})
