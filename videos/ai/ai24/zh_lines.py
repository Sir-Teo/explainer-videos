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
        "都是人一个个输入的。<bookmark mark='b'/>可是没有标签的图片几乎是免费的。2023年的DINOv2在1.42亿张无标签图像上训练；"
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
