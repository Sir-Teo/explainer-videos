"""Chinese narration for ai22: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第22部分：图像、视频与三维'

CHAPTERS = {
    'Hook': '从噪声里画出字母',
    'ViT': '1. 图像是一个序列',
    'Bias': '2. 卷积还是注意力？',
    'Latent': '3. 更小的空间',
    'REPA': '4. 借来的眼睛',
    'UNet': '5. U-Net还是Transformer',
    'AdaLN': '6. adaLN-Zero',
    'Prompt': '7. 从文字到图片',
    'SD3': '8. Stable Diffusion 3与Flux',
    'Tokens': '9. 把图片变成词元',
    'Scales': '10. 由粗到细',
    'Unified': '11. 文字和图片，一个模型',
    'Video': '12. 压缩时间',
    'Clips': '13. 彼此一致的帧',
    'Forcing': '14. 向前滚动',
    'NeRF': '15. 穿过体积的光',
    'Splat': '16. 高斯泼溅',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'Every letter here was drawn from pure noise':
        "这里的每一个字母，都是一个我们在这台电脑上训练的小Transformer，从纯噪声里画出来的，要它画哪个字母，它就画哪个。"
        "<bookmark mark='a'/>它把每张图片看成一串图块，就像语言模型看待词语一样；训练它用的是第21部分的流匹配。"
        "<bookmark mark='b'/>同一个配方，放大十万倍，就能画照片、拍电影，还能生成可以走进去的整个场景。",

    'How we got here. In 2012 a convolutional network':
        "我们是怎么走到这里的。2012年，一个卷积网络AlexNet以很大的优势赢得了ImageNet比赛，这是第10部分讲过的故事。"
        "<bookmark mark='a'/>2014年出现了GAN：一个生成器，和一个评判者对抗着训练，这是第20部分的故事。"
        "<bookmark mark='b'/>2020年，一个普通的Transformer把图像当作一串图块来读。<bookmark mark='c'/>2021年，DALL-E用词元的方式根据文字画图，"
        "扩散模型在画质上超过了GAN。<bookmark mark='d'/>2022年有了DALL-E 2、Imagen，还有公开权重的Stable Diffusion。"
        "<bookmark mark='e'/>到2024年，流匹配Transformer在画图，Sora在生成视频。<bookmark mark='f'/>2025年，视频带上了声音，"
        "一个模型既能读图又能画图，视频的生成速度也赶上了播放速度。<bookmark mark='g'/>到了2026年，开放的模型能把声音和画面一起生成。",

    'This is Part 22 of AI, Built: images, video and 3D.':
        "这是《人工智能，从零搭建》的第22部分：图像、视频与三维。<bookmark mark='a'/>首先，Transformer怎样读一张图片，以及卷积什么时候仍然更好。"
        "<bookmark mark='b'/>然后是模型作画所在的压缩空间，以及借用一个视觉模型的眼睛怎样加快训练。<bookmark mark='c'/>接着是去噪器本身，"
        "以及要求是怎样传进去的。<bookmark mark='d'/>从文字到图片，从DALL-E到Flux。<bookmark mark='e'/>把图片写成词元，"
        "以及文字和图片共用一个模型。<bookmark mark='f'/>视频。<bookmark mark='g'/>还有三维。<bookmark mark='h'/>这一部分的每个模型都在这里训练，"
        "用的是字母、短片和一个小场景，我们会看着每一个模型学习。",

    # ------------------------------------------------------------------ ViT
    'Chapter one. An image is a sequence.':
        '第1章。图像是一个序列。',

    'A transformer reads sequences of tokens.':
        "Transformer读的是词元序列。那就把图片切成小方块，叫作图块，排成一行。<bookmark mark='a'/>每个图块变成一个词元：它的像素乘以一个学到的矩阵，"
        "再加上一个学到的向量，标明它原来在哪里。<bookmark mark='b'/>接下来就是第13部分的那套机器，一点不改：注意力和MLP，一层接一层。"
        "2020年做这件事的论文，作者是Google的阿列克谢·多索维茨基和同事，标题就说明了一切：一张图像值16乘16个词。",

    'f"We trained a small one, with':
        "我们训练了一个小的，有{int(v['n_params']) // 1000}千个权重，让它说出每张图片里是哪个字母；它在"
        "{int(v['n_fonts']) - int(v['n_test_fonts'])}种字体上训练，在{int(v['n_test_fonts'])}种从没见过的字体上测试。"
        "这是它学习的过程。<bookmark mark='a'/>{start}<bookmark mark='b'/>到第{checks[k_half]:,}步，它在没见过的字体上答对了"
        "{100 * accs[k_half]:.0f}%，最后答对{100 * accs[-1]:.0f}%。<bookmark mark='c'/>同时，看看中心那个图块的位置向量，它从零开始：{pos_line}",

    "it comes to resemble its neighbours' vectors":
        '它变得更像邻居们的向量，而不像远处的。',

    "it hardly changes shape: the neighbours":
        '它的形状几乎没变：邻居们并没有被挑出来。',

    'At first it calls almost everything the same letter.':
        '一开始，它几乎把所有图片都叫成同一个字母。',

    'At first its guesses are scattered at random.':
        '一开始，它的猜测是随机分散的。',

    'f"How does it decide? The transformer adds one extra token':
        "它是怎么判断的？Transformer多加了一个词元，叫汇总词元，里面没有任何图片内容。<bookmark mark='s'/>它一层一层地从每个图块收集信息，"
        "最后只凭它自己的向量说出是哪个字母。<bookmark mark='a'/>这是最后一层里汇总词元在看哪里，四个字母都来自一种没见过的字体："
        "它{100 * on_ink:.0f}%的注意力落在有墨迹的图块上，而这些图块只占图片的{100 * ink_share:.0f}%。<bookmark mark='b'/>"
        "再看每个注意力头平均看多远。{reach}",

    'f"Our heads in the first layer already look between':
        "我们的第一层注意力头已经看向{lo:.1f}到{hi:.1f}个像素之外，和随便挑两个图块之间的距离{uniform:.1f}差不多："
        "从第一层开始，它们就到处看。卷积的第一层只看得到几个像素。",

    "f'Our heads in the first layer look between":
        '我们的第一层注意力头看向{lo:.1f}到{hi:.1f}个像素之外，而随便挑两个图块相距{uniform:.1f}：有些头只看附近，像卷积一样。',

    'f"All twenty-five position vectors at the end of training':
        "训练结束时的全部25个位置向量：每一小格显示一个图块的向量和其他每个图块的有多像。<bookmark mark='a'/>相邻的平均{near:.2f}，"
        "相距很远的{far:.2f}。{pattern}",

    'Each tile lights up around its own place.':
        '每一小格都在自己的位置周围亮起来。没有人告诉模型这些图块排成5乘5的网格；它从图片里学到了图片的几何结构。',

    "There's little pattern: a few thousand letters":
        '几乎看不出规律：几千个字母还不足以让它需要这些。在原始的视觉Transformer里，用几百万张照片训练，每一小格都会在自己的位置周围亮起来。',

    # ------------------------------------------------------------------ Bias
    'Chapter two. Convolutions or attention?':
        '第2章。卷积还是注意力？',

    'From 2012, convolutional networks ruled vision:':
        "从2012年起，卷积网络统治了视觉：先是AlexNet，然后是VGG和ResNet，这是第10部分的故事。<bookmark mark='a'/>注意力以附加组件的身份"
        "悄悄进来。<bookmark mark='b'/>接着，2020年的视觉Transformer彻底扔掉了卷积。只用ImageNet的一百多万张图片训练时，它比ResNet差几个百分点；"
        "先在三亿张图片上预训练，它达到了88.55%。作者的总结是：大规模训练胜过归纳偏置。<bookmark mark='c'/>几个月之内，DeiT只用ImageNet，"
        "加上大量数据增强和蒸馏，把它训练到83%；Swin又把局部窗口和层级结构带了回来。<bookmark mark='d'/>2022年，ConvNeXt为卷积扳回一局，"
        "追平了Swin。<bookmark mark='e'/>但在大规模上，Transformer赢了：今天的视觉编码器，比如DINOv2，都是视觉Transformer。",

    'What did the transformer give up? An inductive bias:':
        "Transformer放弃了什么？归纳偏置：在任何数据到来之前就内置的假设。<bookmark mark='a'/>卷积假设了局部性，也就是一个单元只需要看一小块邻域；"
        "还假设同一组权重在图片的每个位置都适用。<bookmark mark='b'/>注意力两者都不假设：任何图块都可以看任何其他图块，权重是当场算出来的。"
        "<bookmark mark='c'/>假设对了，需要的例子就少；假设少了，要学的就多，但能学到的也更多。所以谁赢，要看有多少数据。",

    'f"We can test that on our letters.':
        "我们可以在自己的字母上检验。两个模型，权重差不多一样多，训练步数、批次和数据增强都一样；一个是视觉Transformer，一个是卷积网络。"
        "它们分别从{sizes[0]}种、{sizes[1]}种或全部{sizes[-1]}种字体中学习，再在两者都没见过的4种字体上测试。"
        "<bookmark mark='a'/>暂停一下，预测：数据少的时候谁赢？数据多了以后会变吗？",

    '"Here are the results, three seeds each:':
        "结果在这里，每种三个随机种子：每个点是一次训练。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>{cost}<bookmark mark='c'/>"
        "过去十年的教训是：数据少，就把假设内置进去；数据多，就让模型自己学。这一部分的每个生成器都是Transformer。",

    "f'The convolution also spends":
        '卷积每张图片的计算量也是它的{ratio:.1f}倍：它的模板要在每个像素上运行。',

    "f'The two spend about the same arithmetic":
        '两者每张图片的计算量差不多，{ratio:.1f}比1。',

    "f'The convolutional network wins at every size, by {100 * gap[0]:.0f} points with {sizes[0]} fonts, and the gap":
        '每种规模都是卷积网络赢：{sizes[0]}种字体时领先{100 * gap[0]:.0f}个百分点，用全部{sizes[-1]}种时差距缩小到'
        '{100 * gap[-1]:.0f}个百分点：数据越多，越不需要内置的假设。',

    "f'The convolutional network wins at every size, by {100 * gap[0]:.0f} points with {sizes[0]} fonts and":
        '每种规模都是卷积网络赢：{sizes[0]}种字体时领先{100 * gap[0]:.0f}个百分点，用全部{sizes[-1]}种时领先'
        '{100 * gap[-1]:.0f}个百分点：在这个规模上，内置的假设一直有回报。',

    "f'With {sizes[0]} fonts the convolutional network wins by {100 * gap[0]:.0f} points; with all {sizes[-1]} the transformer passes":
        '{sizes[0]}种字体时，卷积网络领先{100 * gap[0]:.0f}个百分点；用全部{sizes[-1]}种时，Transformer反超了{-100 * gap[-1]:.0f}个百分点。',

    "f'With {sizes[0]} fonts the convolutional network wins by {100 * gap[0]:.0f} points; with all {sizes[-1]} the transformer has":
        '{sizes[0]}种字体时，卷积网络领先{100 * gap[0]:.0f}个百分点；用全部{sizes[-1]}种时，Transformer追上来了。',

    'f"Here the transformer holds its own even on':
        "在这里，即使只有{sizes[0]}种字体，Transformer也不落下风：卷积网络在那里领先{100 * gap[0]:.0f}个百分点，"
        "用全部{sizes[-1]}种时领先{100 * gap[-1]:.0f}个百分点。这么小的字母，并不太需要局部性。",

    # ------------------------------------------------------------------ Latent
    'Chapter three. A smaller space.':
        '第3章。更小的空间。',

    'Real pictures have millions of pixels, and most of that detail':
        "真实的图片有几百万个像素，而其中大部分细节都是可以预测的纹理。2022年，罗宾·龙巴赫、帕特里克·埃塞尔、比约恩·奥默和同事把这件事拆成两步。"
        "<bookmark mark='a'/>一个自编码器把图片压缩成一小格潜变量，再把它重建出来：这一步去掉了没人会注意的细节。<bookmark mark='b'/>"
        "然后扩散模型只需要学剩下的部分，也就是内容。<bookmark mark='c'/>Stable Diffusion的自编码器叫KL-f8，每条边缩小8倍，保留4个通道："
        "数字少了48倍，再加上一丝第20部分的KL惩罚，让潜变量保持规矩。",

    'f"How small can the space be?':
        "这个空间能有多小？我们在字母上训练了八个自编码器，每个都把图片压缩成一个网格，每格有若干个通道，总共从16个数到100个数。"
        "<bookmark mark='a'/>这是每个自编码器在没见过的字体上的重建误差：从{best[0]}乘{best[0]}乘{best[1]}的{rm[best]:.3f}，"
        "到{worst[0]}乘{worst[0]}乘{worst[1]}的{rm[worst]:.3f}。<bookmark mark='b'/>{same}<bookmark mark='c'/>{coarse}",

    "f'And at the same count, the coarser grid":
        '而在数字个数相同的时候，更粗的网格配更多通道，三组里赢了{coarse_wins}组：空间压得很狠也没关系，只要每一格有足够的通道来描述它那一块。',

    "f'At the same count, the finer grid wins":
        '在数字个数相同的时候，更细的网格三组里赢了{3 - coarse_wins}组：在这里，保留布局比更多的通道更重要。',

    'More numbers rebuild better:':
        '数字越多，重建越好：在每种网格里，加通道都会降低误差。',

    "Adding channels doesn't steadily help here.":
        '在这里，加通道并不总有帮助。',

    '"Now run Part 21\'s flow matching inside each space':
        "现在在每个空间里运行第21部分的流匹配：同样的小网络，同样的步数，两个随机种子，再测量生成的字母离真实字母有多远。"
        "<bookmark mark='a'/>{verdict}<bookmark mark='b'/>这就是重建与生成的两难，此后它影响了每一个图像模型。",

    "f'Here the best autoencoder,":
        '在这里，最好的自编码器，{best_r[0]}乘{best_r[0]}乘{best_r[1]}，同时也最容易在里面生成。在这么简单的字母上，两个目标是一致的。',

    'f"The space that rebuilds best,':
        "重建最好的空间，{best_r[0]}乘{best_r[0]}乘{best_r[1]}，并不是生成最好的那个：生成最好的是{best_g[0]}乘{best_g[0]}乘{best_g[1]}。"
        "一个空间可以保留每一个细节，却仍然很难在里面生成。",

    'Real models went both ways at once.':
        "真实的模型同时朝两个方向走。<bookmark mark='a'/>Stable Diffusion 3把潜变量从4个通道加宽到16个，模型足够大以后，这样做就有回报。"
        "<bookmark mark='b'/>2024年10月，韩松的团队压得更狠：用深度压缩自编码器，每条边缩小32到128倍。他们的诀窍是：把每一小块像素折叠进通道里，"
        "这一步不丢任何信息，网络只需要学在此基础上改什么。<bookmark mark='c'/>在512像素的分辨率上，在这个空间里的扩散模型采样快了19倍，"
        "效果还更好。<bookmark mark='d'/>在空间上狠狠压缩，保留足够的通道，并让这个空间容易生成：下一章就讲怎样塑造它。",

    # ------------------------------------------------------------------ REPA
    'Chapter four. Borrowed eyes.':
        '第4章。借来的眼睛。',

    'A diffusion transformer has to learn two things at once:':
        "扩散Transformer要同时学两件事：图片是由什么构成的，以及怎样去掉噪声。<bookmark mark='p'/>但是用几百万张图片训练出来的视觉编码器，比如第24部分的DINOv2，"
        "已经懂得第一件事。<bookmark mark='q'/>去探测扩散Transformer的中间层，会发现它确实学到了图片里有什么，也慢慢变得像那样的编码器，但落后得很远。"
        "<bookmark mark='a'/>2024年10月，Sihyun Yu、谢赛宁和同事在损失里加了一项。取去噪器某个早期块之后的词元，经过一个小投影头，"
        "<bookmark mark='b'/>再按余弦相似度，把它们拉向冻结的编码器对干净图片给出的词元。<bookmark mark='c'/>他们称之为REPA，表示对齐。"
        "一个大型扩散Transformer达到同样的质量，快了17.5倍。",

    'f"We tried it on our letters, with chapter 1':
        "我们在字母上试了，用第1章的视觉Transformer当冻结的老师：同一个扩散Transformer，同样的数据、步数和随机种子，有和没有这一项。"
        "<bookmark mark='a'/>评判网络把生成的字母读成所要求字母的比例，加REPA最后是{100 * ra_end:.0f}%，不加是{100 * za_end:.0f}%。"
        "<bookmark mark='b'/>{verdict}<bookmark mark='c'/>{align}",

    'f"And the alignment itself climbs':
        '对齐程度本身也在上升，从{a0:.2f}升到{a1:.2f}，去噪器的词元越来越像老师的。',

    "f'The alignment itself barely moves":
        '对齐程度本身几乎没动，从{a0:.2f}到{a1:.2f}。',

    'f"With REPA, the generated letters reach':
        "加了REPA，生成的字母在第{reach:,}步就达到了普通模型最后的距离，快了{ev[-1] / reach:.1f}倍，最后还更近：{r_end:.0f}对{z_end:.0f}。",

    "f'With REPA the generated letters end closer":
        '加了REPA，生成的字母最后离真实字母更近，{r_end:.0f}对{z_end:.0f}，不过差得不多。',

    'f"Here REPA doesn\'t help:':
        "在这里REPA没有帮助：加了它距离最后是{r_end:.0f}，不加是{z_end:.0f}。我们的老师只学过说出字母的名字，而字母本身很容易看清；"
        "REPA的收益来自用几百万张各式各样的图片训练出来的编码器。",

    'The same idea then moved into the latent space itself.':
        "后来，同一个想法进入了潜空间本身。<bookmark mark='a'/>VA-VAE把自编码器的潜变量和一个视觉模型的特征对齐，让这个空间既容易重建，"
        "又容易生成。<bookmark mark='b'/>REPA-E把自编码器和去噪器放在一起训练，由REPA防止这个空间塌缩。<bookmark mark='c'/>2025年10月，"
        "表示自编码器干脆不要VAE了：把DINOv2冻结起来当编码器，只训练一个解码器，直接在编码器自己的特征里做扩散。"
        "<bookmark mark='d'/>模型生成所在的空间，本身就应该有意义。",

    # ------------------------------------------------------------------ UNet
    'Chapter five. U-Net or transformer.':
        '第5章。U-Net还是Transformer。',

    'Who does the denoising? For the first diffusion models, a U-Net.':
        "由谁来去噪？最早的扩散模型用的是U-Net。奥拉夫·龙内贝格尔和同事在2015年设计它，是为了在显微镜图片里勾画细胞。"
        "<bookmark mark='a'/>卷积一步步把图片缩小，让每个单元看到更大的范围；<bookmark mark='b'/>然后网络再把它放大回去，"
        "<bookmark mark='c'/>跳跃连接把精细的细节直接跨过U形送过去，不必挤过瓶颈。<bookmark mark='d'/>DDPM用的就是它；2021年，"
        "普拉富拉·达里瓦尔和亚历克斯·尼科尔把它放大，在低分辨率处加上注意力，把噪声水平送进每一个归一化层，扩散模型就超过了GAN。"
        "Stable Diffusion的去噪器也是U-Net。",

    'In 2023 William Peebles and Saining Xie replaced the U-Net':
        "2023年，威廉·皮布尔斯和谢赛宁用一个普通的Transformer取代了U-Net，这就是扩散Transformer，DiT。<bookmark mark='a'/>带噪声的图片被切成图块词元，"
        "和第1章一样。<bookmark mark='b'/>Transformer块处理它们，输出的是速度，一个图块一个图块地输出。<bookmark mark='c'/>噪声水平和要求从每一个块进入；"
        "具体怎么进入，是下一章的内容。<bookmark mark='d'/>它的质量跟着计算量走：模型更大，或者图块更小，画出来的图就更好，最大的那个在ImageNet上创了纪录。"
        "它像语言模型一样可以扩展，此后的图像和视频模型几乎都是Transformer。",

    '"So which is better? We trained a small U-Net':
        "那么哪个更好？我们训练了一个小U-Net和一个小扩散Transformer，权重数量差不多，用同样的字母、同样的步数、批次和随机种子。"
        "<bookmark mark='a'/>{verdict}<bookmark mark='b'/>Transformer的理由从来不是在小规模上赢。而是它会随着变大一直变好，只用一个简单的配方，和语言模型一样。",

    'f"With similar weights and the same steps, the U-Net wins here:':
        "在权重相近、步数相同时，这里是U-Net赢：它的字母最后的距离是{u_end:.0f}，Transformer是{z_end:.0f}；被读成所要求字母的有"
        "{100 * ua_end:.0f}%，Transformer是{100 * za_end:.0f}%。但它为此每张图片付出了{mu / mz:.0f}倍的计算量，而且在这么小的字母上，"
        "卷积的假设正好合适。",

    'f"With similar weights and the same steps, the transformer wins:':
        "在权重相近、步数相同时，Transformer赢了：它的字母最后的距离是{z_end:.0f}，U-Net是{u_end:.0f}，尽管U-Net每张图片花了{mu / mz:.0f}倍的计算量。",

    "f'With similar weights and the same steps they end close:":
        '在权重相近、步数相同时，两者最后很接近：U-Net的距离是{u_end:.0f}，Transformer是{z_end:.0f}，尽管U-Net每张图片花了{mu / mz:.0f}倍的计算量。',

    # ------------------------------------------------------------------ AdaLN
    'Chapter six. adaLN-Zero.':
        '第6章。adaLN-Zero。',

    'The denoiser must know the noise level and what it was asked to draw;':
        "去噪器必须知道噪声水平，以及它被要求画什么；把两者合起来叫作c。皮布尔斯和谢赛宁比较了几种送进去的方式。"
        "<bookmark mark='a'/>上下文方式：把c作为额外的词元接在序列后面，让注意力去找它们。<bookmark mark='b'/>自适应层归一化：让c来设定每个归一化的缩放和平移，"
        "这样它能到达每个块里的每个词元。<bookmark mark='c'/>还有adaLN-Zero：同样的做法，再在每个块的输出上加一个门，这个门从零开始。",

    'f"Here is adaLN-Zero exactly.':
        "这就是adaLN-Zero的准确形式。<bookmark mark='a'/>条件c为每个归一化设定一个缩放伽马和一个平移贝塔，并在每个分支的输出上设一个门阿尔法。"
        "<bookmark mark='b'/>这六个量都来自c的同一个线性映射，而这个映射从零开始。<bookmark mark='c'/>所以一开始每个门都是关着的，每个块都把输入原样传过去："
        "一个从恒等映射开始的深层网络。<bookmark mark='d'/>这是我们的模型在训练中的门：它们从零开始打开，到最后平均大小是{opened:.2f}，"
        "网络为每个块都找到了用处。",

    'f"Here is ours learning: the same noise, asked for the same ten letters':
        "这是我们的模型在学习：同样的噪声，要求同样的十个字母，从A到J，在{total:,}步训练中的各个检查点画出来，步数是后面那些比较的{total / cmp_n:.0f}倍。"
        "<bookmark mark='a'/>在第{steps[0]}步，每个块还是恒等映射，所以噪声原样穿过。<bookmark mark='b'/>在第{steps[3]:,}步，"
        "评判网络把十个里的{reads[3]}个读成了所要求的字母；<bookmark mark='c'/>第{steps[j]:,}步时是{reads[j]}个；"
        "<bookmark mark='d'/>最后是{reads[-1]}个。同时，损失从{loss0:.2f}降到{L[-1, 1]:.2f}。",

    '"Does the way in matter?':
        "送进去的方式重要吗？三种我们都训练了，每种三个随机种子，数据和步数相同；两种adaLN版本为缩放、平移和门控多带了一些权重。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>"
        "在论文里，训练到40万步时，adaLN-Zero的距离差不多只有上下文方式的一半，而代价相同。",

    "f'As in the paper, adaLN-Zero comes out best:":
        "和论文一样，adaLN-Zero最好：距离是{fd['zero'].mean():.0f}，普通adaLN是{fd['ada'].mean():.0f}，上下文词元是{fd['context'].mean():.0f}。",

    'f"Here {names[order[0]]} comes out best':
        "在这里最好的是{names[order[0]]}，距离{fd[order[0]].mean():.0f}，adaLN-Zero是{fd['zero'].mean():.0f}：只有四个块深的时候，"
        "从恒等映射开始，不像论文里28个块时那么重要。",

    'And here is our adaLN-Zero model, asked for each letter':
        "这是我们的adaLN-Zero模型，按第21部分的引导方式，要它画字母表里的每个字母。<bookmark mark='a'/>换一份噪声再要一次，"
        "它画出同样的字母，但风格不同：要求决定画什么，噪声决定怎么画。",

    # ------------------------------------------------------------------ Prompt
    'Chapter seven. Words into pictures.':
        '第7章。从文字到图片。',

    'Until 2020, the sharpest generated pictures came from GANs':
        "直到2020年，最清晰的生成图片都来自GAN，也就是第20部分的BigGAN和StyleGAN。从文字到图片，是从两个方向走过来的。"
        "<bookmark mark='a'/>2021年1月，OpenAI的DALL-E把它当作语言建模：一个有120亿个权重的Transformer，先写出描述文字的词元，"
        "再写出一个32乘32的图片词元网格。<bookmark mark='b'/>同年5月，达里瓦尔和尼科尔证明扩散模型在画质上超过了GAN。<bookmark mark='c'/>"
        "2022年，扩散模型接管了文生图：DALL-E 2把描述变成一个CLIP图片嵌入，再用扩散解码出来；<bookmark mark='d'/>谷歌的Imagen发现，"
        "用一个更大的冻结语言模型来读提示词，比用更大的去噪器帮助更大；<bookmark mark='e'/>Parti坚持走词元路线，用了200亿个权重；"
        "<bookmark mark='f'/>Stable Diffusion公开了权重，把潜空间扩散交到了每个人手里。<bookmark mark='g'/>2023年，DALL-E 3发现瓶颈在数据："
        "它改用一个模型写的又长又详细的描述来重新训练，对提示词的遵循好了很多。",

    'How does the prompt reach the denoiser?':
        "提示词是怎样到达去噪器的？在Stable Diffusion里，靠的是交叉注意力。一个冻结的文本编码器把提示词变成词元。<bookmark mark='a'/>"
        "在每个块里，每个图片词元提出一个问题，也就是它的查询，提示词的词元提供键和值：这样每个图块都能拉进对它重要的词。"
        "<bookmark mark='b'/>这就是第13部分的注意力，只是查询来自一个序列，键来自另一个。<bookmark mark='c'/>注意，文字只是被读取，从不被图片更新。"
        "下一章的模型改变了这一点。",

    '"And how hard should it listen?':
        "那它应该听得多认真？第21部分的无分类器引导，用一个权重w把去噪器从它的无条件猜测上推开；Stable Diffusion的默认值是7.5。"
        "我们在字母Transformer上扫了一遍，把字母本身当作提示词。<bookmark mark='a'/>{verdict}<bookmark mark='v'/>{spread}"
        "<bookmark mark='b'/>{close}",

    "f'And the drawings of one letter grow alike:":
        '同一个字母的不同画法也越来越像：它们的散布从{v0:.2f}降到{vN:.2f}。',

    'f"But the drawings of one letter don\'t grow alike:':
        '但同一个字母的不同画法并没有变得更像：它们的散布从{v0:.2f}升到{vN:.2f}，因为太强的引导会冲过头，自己添出斑块。',

    'Guidance buys faithfulness with variety.':
        '引导用多样性换来了忠实。',

    'Large models trade variety for faithfulness; ours shows the other cost, overshooting.':
        '大模型用多样性换忠实；我们的模型显示的是另一种代价：冲过头。',

    'In large models, guidance buys faithfulness with variety.':
        '在大模型里，引导用多样性换来忠实。',

    "f'Their variety barely changes":
        '它们的多样性几乎没变，从{v0:.2f}到{vN:.2f}。',

    "f'At w = 0, the model without its prompt":
        'w等于0时，也就是不看提示词的模型，评判网络把{100 * a0:.0f}%读成所要求的字母，而碰运气是4%；w等于1时，也就是只用带提示词的模型，'
        '是{100 * a1:.0f}%；w等于2时是{100 * a2:.0f}%；w等于{ws[-1]:g}时是{100 * aN:.0f}%。w等于{best_w:g}时，字母最像真实的字母。',

    # ------------------------------------------------------------------ SD3
    'Chapter eight. Stable Diffusion 3 and Flux.':
        '第8章。Stable Diffusion 3与Flux。',

    'In March 2024 Patrick Esser, Robin Rombach and colleagues at Stability AI':
        "2024年3月，Stability AI的帕特里克·埃塞尔、罗宾·龙巴赫和同事发表了Stable Diffusion 3：用第21部分的整流流，加上一个新的Transformer，MM-DiT。"
        "它把提示词的词元和图片的图块放进同一个序列。<bookmark mark='a'/>两类词元各自保留一套权重，因为词和图块是不同的东西；"
        "<bookmark mark='b'/>然后对合并后的序列做一次注意力。<bookmark mark='c'/>所以每个图块都能读每个词，而且和交叉注意力不同，词语会随着图片被画出来而被改写。"
        "<bookmark mark='d'/>对查询和键做归一化让训练保持稳定；三个冻结的文本编码器读取提示词；最大的模型有80亿个权重。",

    '"SD3 also changed which noise levels it trains on.':
        "SD3还改变了在哪些噪声水平上训练。<bookmark mark='a'/>第21部分是均匀地抽取时间t。但在接近纯噪声的地方，最好的猜测就是平均图片；"
        "在接近数据的地方，又没什么可修的：难的是中间。<bookmark mark='b'/>所以抽一个正态分布的数，再用sigmoid函数压一下：这就是logit-normal分布，"
        "它在中间训练得最多。在论文比较的众多选择里，它排第一。<bookmark mark='c'/>我们用两种方式训练了流匹配，每种三个随机种子。{verdict}",

    "f'Trained logit-normally, our letters come out closer to real ones at every number":
        '用logit-normal训练，我们的字母在每种采样步数下都更接近真实字母，{few_s}时差别最大。',

    "f'Trained logit-normally, our letters come out closer to real ones on average":
        '用logit-normal训练，我们的字母平均来说更接近真实字母，{few_s}时差别最大，不过并不是每种步数都如此。',

    'On our letters, uniform does as well or better:':
        '在我们的字母上，均匀抽取一样好，甚至更好：在只有16个数的空间里，难点并不在中间。在大图片上，论文发现logit-normal是它比较过的众多方案里最好的。',

    'f"One more thing changes with size.':
        "随着尺寸变化，还有一件事会变。<bookmark mark='a'/>给一个小字母，和它的一个像素多16倍的版本，加上同样的噪声。大的那个看起来更清楚，"
        "而且确实如此：把每个4乘4的小块取平均，噪声就从{sig}降到{float(s['demo_left']):.2f}。相邻的像素共享信息，所以一个能毁掉小图片的噪声水平，"
        "会让大图片依然可以辨认。<bookmark mark='b'/>SD3把这一点做成了精确的公式。用西格玛表示噪声所占的份额。<bookmark mark='c'/>"
        "考虑最坏的情况，一张均匀的图片：每个像素都是同一个值c。对n个像素求平均：噪声缩小到原来的根号n分之一。<bookmark mark='d'/>"
        "所以关于c剩下的不确定性，是西格玛除以1减西格玛，再除以根号n。<bookmark mark='e'/>要求m个像素时的不确定性一样，<bookmark mark='f'/>"
        "解出来：噪声水平按一个因子阿尔法偏移，阿尔法是像素数之比的平方根。在对数信噪比里，这是一个常数偏移。",

    'f"Does it hold for real pictures?':
        "它对真实图片成立吗？我们把同样的五百多个字母分别画成20、40和80像素见方，加上噪声，再问精确的后验分布：这是哪一张字母图片？"
        "<bookmark mark='a'/>在20像素时，噪声水平为{half[20]:.2f}时它有一半的机会答对；40像素时是{half[40]:.2f}；80像素时是{half[80]:.2f}。"
        "公式预测的是{pred[40]:.2f}和{pred[80]:.2f}。<bookmark mark='b'/>{verdict}<bookmark mark='c'/>SD3的作者说均匀图片的假设并不现实，"
        "就请人来评判不同的偏移，最后在1024像素见方时选定阿尔法等于3。",

    'f"After the shift the curves nearly line up:':
        "偏移之后，几条曲线几乎重合：和小图片曲线的最大差距从{g80b:.2f}降到{g80a:.2f}。",

    'f"After the shift they move together, but don\'t fully line up:':
        "偏移之后它们一起移动，但没有完全重合：最大差距只从{g80b:.2f}降到{g80a:.2f}，因为80像素的真实图画比公式假设的均匀图片有更精细的细节。",

    "Several of SD3's authors went on to found Black Forest Labs.":
        "SD3的几位作者后来创办了Black Forest Labs。<bookmark mark='a'/>2024年8月，他们发布了FLUX.1：120亿个权重，先是MM-DiT块，"
        "再接上更便宜的单流块，用旋转位置编码，还有一个经过蒸馏、不需要引导的开放版本。<bookmark mark='b'/>2025年，FLUX.1 Kontext把输入图片的词元"
        "接到序列里来编辑图片，<bookmark mark='c'/>FLUX.2则长到了320亿个权重，由一个视觉语言模型来读提示词，最多可以用十张参考图片。"
        "<bookmark mark='d'/>配方已经定型：一个潜空间，整流流，一个同时处理词和图块的Transformer。",

    # ------------------------------------------------------------------ Tokens
    'Chapter nine. Pictures as tokens.':
        '第9章。把图片变成词元。',

    'f"Diffusion isn\'t the only way to draw.':
        "扩散不是唯一的作画方式。语言模型一次写一个词元；要这样画图，先得把图片变成词元。<bookmark mark='a'/>第20部分的VQ-VAE和第23部分的码本"
        "就能做到：把图片编码成一个小网格，再把每一格对齐到一个学出来的码本里最近的条目。条目的编号就是词元。<bookmark mark='b'/>2020年12月，"
        "帕特里克·埃塞尔、罗宾·龙巴赫和比约恩·奥默用感知损失和一个GAN的评判者来训练这样的分词器，让一个16乘16的词元网格能重建出清晰的图片："
        "这就是VQGAN。<bookmark mark='c'/>我们的分词器把一个字母压成25个词元，每个是{int(d['K'])}个码之一，在没见过的字母上重建误差是"
        "{float(d['single_rmse']):.3f}。",

    'Then write the tokens the way a language model writes words:':
        "然后像语言模型写字那样写这些词元：从左到右，从上到下，每个词元都由前面的词元来预测。<bookmark mark='a'/>对我们来说，"
        "就是在网络里过25遍。<bookmark mark='b'/>这样行得通：DALL-E和Parti就是这么做的。但一千个词元就要过一千遍，而且这对图片来说是个奇怪的顺序："
        "上面几行已经定下来了，下面的还什么都没有。",

    'In February 2022 Huiwen Chang and colleagues at Google':
        "2022年2月，谷歌的Huiwen Chang和同事改用一个像BERT那样的Transformer来训练：随机遮住一部分词元，在能看到所有其他词元的情况下，"
        "一次把它们全部预测出来。这就是MaskGIT。<bookmark mark='a'/>作画时，从全部遮住开始。预测每一个词元；留下最有把握的那些；"
        "把其余的重新遮住，再重复。一个余弦调度决定每次留多少：开始少，后来越来越快。<bookmark mark='b'/>这是我们的模型用八遍画四个字母。"
        "每一遍都同时在整张图片上确定一些词元，先少后多。论文用八遍而不是256遍画出ImageNet图片，而且画得更好。",

    'f"Here are the token models learning':
        "这是几个词元模型在学习，每个三个随机种子，包括下一章要讲的那个。<bookmark mark='a'/>在{int(d['K'])}个码里均匀地猜，"
        "每个词元要花{np.log(int(d['K'])):.2f}奈特；光栅顺序最后是{ends['raster']:.2f}，MaskGIT是{ends['maskgit']:.2f}。"
        "这些数字的含义不同：MaskGIT只在它看不见的词元上评分，而其他所有词元都在眼前。",

    'f"We trained both on the same tokens':
        "我们用同样的词元训练了这两个模型，Transformer一样大，步数一样，每个三个随机种子。<bookmark mark='a'/>{verdict}"
        "<bookmark mark='b'/>评判网络把光栅顺序画的字母的{100 * a_r:.0f}%读成所要求的字母，MaskGIT的是{100 * a_m:.0f}%。",

    'f"MaskGIT\'s letters are closer to real ones':
        "MaskGIT的字母更接近真实字母，{m_m:.0f}对{m_r:.0f}，而且只用了大约三分之一的遍数。",

    'f"Raster order\'s letters are closer to real ones here':
        "在这里光栅顺序的字母更接近真实字母，{m_r:.0f}对MaskGIT的{m_m:.0f}：并行解码时，同时猜的几个词元看不到彼此的选择。"
        "MaskGIT只用了大约三分之一的遍数。",

    # ------------------------------------------------------------------ Scales
    'Chapter ten. Coarse to fine.':
        '第10章。由粗到细。',

    'f"There\'s a more natural order for a picture:':
        "对图片来说，有一种更自然的顺序：由粗到细。2024年4月，北京大学和字节跳动的田柯宇、王立威和同事做了一个有五个尺度的分词器。"
        "<bookmark mark='a'/>第一个尺度只有一个词元，表示整张图片大致的平均；<bookmark mark='b'/>之后的每个尺度，在更细的网格上，只编码更粗的尺度漏掉的东西："
        "残差。<bookmark mark='c'/>这是我们的分词器处理一个没见过的字母：误差从一个词元后的{errs[0]:.3f}，降到全部"
        "{sum((s * s for s in sizes))}个词元后的{errs[-1]:.3f}。<bookmark mark='d'/>用符号写出来：把剩下的部分平均缩小到这个尺度再量化；"
        "再平滑放大，加回去。",

    'Then train a transformer to predict each whole scale at once':
        "然后训练一个Transformer，根据所有更粗的尺度，一次预测出一整个尺度：下一尺度预测，VAR。<bookmark mark='a'/>注意力掩码是块因果的："
        "每个词元看得到自己这个尺度和更粗的尺度，从不看更细的。<bookmark mark='b'/>所以一张图片每个尺度只要过一遍。这是我们的模型用五遍画四个字母："
        "先是一团模糊，然后是形状，最后是笔画。",

    '"All three, side by side:':
        "三个模型放在一起：Transformer一样大，步数和引导都一样，每个三个随机种子。<bookmark mark='a'/>{verdict}",

    "f'VAR comes out best here,":
        "在这里VAR最好，距离是{m['var']:.0f}，MaskGIT是{m['maskgit']:.0f}，光栅顺序是{m['raster']:.0f}，而且遍数最少。",

    'f"Here {names[best]} comes out best,':
        "在这里最好的是{names[best]}，距离{m[best]:.0f}；VAR用五遍达到{m['var']:.0f}。只有25个词元，我们的字母留给顺序发挥作用的余地很小；"
        "VAR的优势要在上千个词元时才显出来。",

    "On ImageNet, VAR's own raster-order baseline":
        "在ImageNet上，VAR自己的光栅顺序基线的距离是18.65；VAR是1.73，超过了扩散Transformer，生成速度快了大约20倍：十个尺度，"
        "从一个词元到16乘16，共680个词元，只要十遍，而光栅顺序要256遍。它的损失随模型大小按幂律下降，就像语言模型一样。它获得了NeurIPS 2024的最佳论文奖。"
        "<bookmark mark='a'/>还有人干脆不要码本：何恺明团队的MAR用连续的词元，每个词元由一个很小的扩散模型画出来。<bookmark mark='b'/>"
        "Infinity则把每个词元变成最多64位的二进制串，一位一位地预测：词表最大可达2的64次方。<bookmark mark='c'/>词元还有另一层意义："
        "语言模型正是通过它们来画图的。",

    # ------------------------------------------------------------------ Unified
    'Chapter eleven. One model for words and pictures.':
        '第11章。文字和图片，一个模型。',

    'So far, one model reads pictures and another draws them.':
        "到目前为止，一个模型读图，另一个模型画图。一个网络能两样都做吗？<bookmark mark='a'/>2024年，Meta的Chameleon把图片变成和文字同一个词表里的词元，"
        "在所有东西上只训练一个下一词元损失。<bookmark mark='b'/>Meta的Chunting Zhou和同事做的Transfusion，则让图片保持连续：一个Transformer，两个损失，"
        "文字用下一词元预测，图片的图块用扩散。在70亿个权重的规模上，它比把图片变成离散词元扩展得更好。<bookmark mark='c'/>DeepSeek的Janus发现，"
        "读图和画图需要不同的眼睛，于是给了它两个编码器。<bookmark mark='d'/>字节跳动的BAGEL给两项工作各配了一个Transformer专家，共享同一个注意力，"
        "在数万亿个混合词元上训练；自由形式的编辑能力自己冒了出来。",

    'One network does both, though drawing lags':
        '一个网络两样都能做，只是画画落在后面',

    '"We built a tiny Transfusion:':
        "我们搭了一个很小的Transfusion：一个Transformer，用三种序列训练，每个批次里都混在一起。<bookmark mark='a'/>画：一个风格和一个字母，"
        "然后是一张图片，从噪声开始。命名：一张图片，然后用文字写出它的字母和风格。编辑：一张图片，一个词“粗体”，然后是同一个字母在它那种字体里的粗体。"
        "<bookmark mark='b'/>注意力从左到右，只有在一张图片内部，所有图块互相都能看到。<bookmark mark='c'/>文字词元用下一词元的交叉熵；"
        "正在画的那张图片的图块用流匹配。它的模块用的是第6章的adaLN-Zero：每个图块的噪声水平，加上目前读到的提示，设定它的缩放和门控。"
        "<bookmark mark='d'/>{both}：对没见过的字体，它能说出{100 * na.mean():.0f}%的字母，"
        "它画的图有{100 * da.mean():.0f}%被读成所要求的字母。",

    'f"Here it is learning: four terms of one loss':
        "这是它学习的过程：一个损失的四项，每个批次都全部计算。<bookmark mark='a'/>文字项是交叉熵；图片项是流匹配的平方误差。"
        "命名这一项降到{name_end:.2f}奈特；{prompt}",

    'f"the prompt\'s text term stays higher':
        "提示词的文字项一直更高，在{prompt_end:.2f}，因为没有任何东西能告诉模型陌生人会要哪个字母。",

    'f"the prompt\'s text term ends at':
        "提示词的文字项最后是{prompt_end:.2f}。",

    '"The edit is the interesting one.':
        "编辑是最有意思的。我们留出了两对字体：它们的常规体从来没见过，更别说编辑了。<bookmark mark='a'/>这是这些字体里的字母、"
        "我们的模型对“粗体”的回答，以及真正的粗体。<bookmark mark='b'/>{verdict}<bookmark mark='c'/>要编辑的图片，只是序列里更多的词元而已："
        "这就是上下文编辑。",

    'f"Its bold versions are closer to the real ones':
        "它画的粗体比原图更接近真正的粗体：距离{er.mean():.3f}对{cr.mean():.3f}。它把笔画加粗了{ink.mean():.2f}倍，真正的粗体是"
        "{tink.mean():.2f}倍，而且有{100 * el.mean():.0f}%的时候保持了原来的字母。",

    'f"It thickens the strokes, by a factor of':
        "它把笔画加粗了{ink.mean():.2f}倍，真正的粗体是{tink.mean():.2f}倍，有{100 * el.mean():.0f}%的时候保持了原来的字母；"
        "但它并没有比原图更接近真正的粗体：{er.mean():.3f}对{cr.mean():.3f}。",

    'Editing has become a kind of generation.':
        "编辑已经变成了一种生成。<bookmark mark='a'/>2022年，InstructPix2Pix用其他模型做出来的编辑样本对来训练一个去噪器。"
        "<bookmark mark='b'/>2025年3月，OpenAI的GPT-4o开始原生地画图，也能编辑给它看的图片。<bookmark mark='c'/>FLUX.1 Kontext的编辑方式和我们的字母一样，"
        "把要改的图片接进序列；Qwen-Image和谷歌的Gemini 2.5 Flash Image也把输入图片当作上下文，所以一张脸、一种风格或一个产品能在编辑中保持下来。"
        "<bookmark mark='d'/>下一步：在时间上用同样的办法。",

    # ------------------------------------------------------------------ Video
    'Chapter twelve. Squeezing time.':
        '第12章。压缩时间。',

    'Video is pictures in time.':
        "视频就是时间里的图片。2024年2月，OpenAI的Sora展示了扩散Transformer能用它做什么：长达一分钟的视频片段，用视频和图片一起训练。"
        "<bookmark mark='a'/>随后是Meta的Movie Gen，有300亿个权重。<bookmark mark='b'/>接着是开放权重：腾讯的HunyuanVideo和阿里巴巴的Wan。"
        "<bookmark mark='c'/>2025年，谷歌的Veo 3和OpenAI的Sora 2把声音和画面一起生成。<bookmark mark='d'/>开放模型也跟了上来，小到一块消费级显卡就能运行，"
        "<bookmark mark='e'/>2026年1月，Lightricks发布了LTX-2，一个开放模型同时生成声音和画面。它们都建立在同样的三块基石上："
        "压缩时间，在三个维度上给词元定位，然后去噪。",

    'f"First the squeeze.':
        "先说压缩。和图片一样，一个自编码器压缩视频，现在在时间和空间上都压缩，一个词元就是一小块时空。<bookmark mark='a'/>"
        "按典型的压缩率，每秒16帧的720p视频，五秒钟大约是{round(t720['tokens'], -3):,.0f}个词元。",

    'f"The squeeze comes from a video autoencoder':
        "压缩来自一个视频自编码器，它的卷积既在空间上也在时间上运行。<bookmark mark='v'/>卷积在图片上滑动的那个小模板，变成了一个小立方体，"
        "也在帧之间滑动，而且只往回看。<bookmark mark='a'/>我们在一个字母弹来弹去的短片上训练了一个小的。第一帧单独压缩；<bookmark mark='b'/>"
        "之后每四帧变成一个潜帧，它只能看到它自己那一帧及之前的帧：和语言模型一样，是因果的。<bookmark mark='c'/>这有两个好处。"
        "视频可以边流入边编码；而一张静止图片就是一帧的视频，所以视频模型也能用图片训练。图片多，教外观；视频教运动；多数视频模型两样都用。"
        "<bookmark mark='d'/>这里{int(d['pixels']):,}个像素变成{int(d['numbers'])}个数，少了{ratio:.0f}倍，重建误差是{float(d['rmse']):.3f}；"
        "一张静止图片单独重建，误差是{float(d['still_rmse']):.3f}。",
}

ZH.update({
    'f"A token now has three coordinates:':
        "现在一个词元有三个坐标：哪一帧，哪一行，哪一列。第13部分的旋转位置编码可以很自然地推广。<bookmark mark='a'/>把每个头的数两两一组，分成三份："
        "一些按帧号旋转，一些按行旋转，一些按列旋转，每组有自己的频率。<bookmark mark='b'/>因为每组都是一个旋转，两个词元之间的分数只取决于它们在时间、"
        "高度和宽度上相距多远，和一维时完全一样。<bookmark mark='c'/>推广起来不那么优雅的是代价：{round(n5, -3):,.0f}个词元，意味着注意力要比较"
        "{n5 * n5 / 1000000000.0:.1f}十亿对，每一层、每一个去噪步都是如此。长度加倍，对数就变成四倍。所以视频模型要用上第15和第16部分的每一个技巧。",

    # ------------------------------------------------------------------ Clips
    'Chapter thirteen. Frames that agree.':
        '第13章。彼此一致的帧。',

    "Now let's make video ourselves.":
        "现在我们自己来做视频。这些短片里，一个字母每帧移动一个像素，碰到墙就弹回来。<bookmark mark='a'/>和真实的视频模型一样，我们在一个自编码器的潜空间里工作："
        "每一帧压成一百个数。<bookmark mark='b'/>一个小Transformer每帧看一个词元，每帧的噪声水平通过adaLN-Zero送进去，和第6章一样。"
        "<bookmark mark='c'/>任务是：给出第一帧，它来自模型从没见过的字体，画出接下来的七帧。第一个模型一次对整个片段去噪：每一帧的噪声水平相同，"
        "每一帧都关注其他每一帧。这就是全序列扩散，Sora就是这样工作的。",

    'We trained three models of this size, three seeds each:':
        "我们训练了三个这样大小的模型，每个三个随机种子：一个是整段片段的模型，另外两个逐帧生成，下一章要用到。<bookmark mark='a'/>这是它们学习的过程。"
        "它们的损失之间不能直接比较，因为每个模型被问的问题不同，但三个都稳定下来了。<bookmark mark='b'/>现在，暂停一下，预测。拿整段片段的模型，"
        "要么把一个片段的各帧一起画，要么每一帧都从同一个模型单独的一次运行里取。哪种片段能保持同一个字母、朝同一个方向移动？",

    '"Here\'s the catch with one frame:':
        "只给一帧有个问题：它说不出字母在往哪个方向移动。模型必须自己选，而每一帧都得做同样的选择。<bookmark mark='a'/>每一对里，上面一行是一起画出来的片段。"
        "下面一行的每一帧，取自同一个模型的不同样本，就好像这些帧是一帧一帧独立画出来的。<bookmark mark='b'/>{verdict}<bookmark mark='c'/>"
        "{close}而且片段的长度在训练模型时就固定了。",

    'f"Drawn together, the frames agree:':
        "一起画的时候，各帧是一致的：有{100 * jr.mean():.0f}%的片段每一帧都是对的字母，分开画只有{100 * ir.mean():.0f}%；字母路径每帧晃动"
        "{jj.mean():.2f}个像素，而每帧单独画时是{ij.mean():.2f}个像素。",

    'f"Drawn together, the motion is steadier:':
        "一起画的时候，运动更平稳：字母路径每帧晃动{jj.mean():.2f}个像素，每帧单独画时是{ij.mean():.2f}个像素；字母本身在"
        "{100 * jr.mean():.0f}%的片段里保持下来，分开画是{100 * ir.mean():.0f}%。",

    'Denoising the whole clip at once makes the frames agree.':
        '一次对整个片段去噪，让各帧彼此一致。',

    "At this size, denoising the whole clip at once doesn't buy agreement.":
        '在这个规模上，一次对整个片段去噪并没有换来一致。',

    'f"Surprisingly, drawing the frames together':
        "出人意料的是，在这里一起画并没有让运动更平稳：晃动{jj.mean():.2f}个像素，对比{ij.mean():.2f}个。",

    # ------------------------------------------------------------------ Forcing
    'Chapter fourteen. Rolling forward.':
        '第14章。向前滚动。',

    'To go on past a fixed length, write the video frame by frame':
        "要超出固定的长度继续生成，就像写文字一样一帧一帧地写视频：每一帧都由前面的帧生成，用因果注意力。<bookmark mark='a'/>最直接的训练方法是教师强制："
        "给模型干净的前几帧，教它对下一帧去噪。<bookmark mark='b'/>2024年7月，Boyuan Chen、文森特·西茨曼和同事提出了扩散强制：给每一帧各自一个随机的噪声水平，"
        "让模型学会在干净和带噪声的上下文任意混合的情况下工作。这样在生成时，它可以把自己之前画的帧当作稍带噪声的，从不完全相信它们。",

    'f"We trained a teacher-forcing model and a diffusion-forcing model':
        "我们训练了一个教师强制模型和一个扩散强制模型，和整段片段的模型一样大，用同样的八帧片段，每个三个随机种子。现在给每个模型两帧真实的帧，"
        "它们确定了运动方向，再要它们画出{L_ - 2}帧：是任何一个模型训练长度的四倍。<bookmark mark='a'/>这是按物理规律应该出现的帧，"
        "<bookmark mark='b'/>这是每个模型滚动生成的结果：教师强制；把自己画的帧当作干净的扩散强制；把它们当作稍带噪声的扩散强制；"
        "还有整段片段的模型，每次从最后两帧出发，往后延伸六帧。",

    '"Measured over sixty-four clips and three seeds:':
        "在64个片段和三个随机种子上测量：字母离物理规律给出的位置有多远，一帧一帧地看，以及评判网络是否仍然认得出正确的字母。"
        "<bookmark mark='a'/>{verdict}<bookmark mark='b'/>{ending}<bookmark mark='c'/>{why_line}",

    "f'Lowest at the end:":
        '到最后误差最低的是{names[best]}，{late[best]:.1f}个像素，最后八帧里有{100 * lr[best]:.0f}%的时候是正确的字母。',

    "f'Teacher forcing drifts most:":
        "教师强制漂移得最厉害：在训练长度之内，它的字母离应在的位置{early['teacher']:.1f}个像素；最后八帧是{late['teacher']:.1f}个像素。"
        "扩散强制最后是{late['forcing']:.1f}，用带噪声的上下文是{late['forcing_noisy']:.1f}。",

    "f'Every frame-by-frame model drifts:":
        "每个逐帧模型都会漂移：教师强制从训练长度之内偏离{early['teacher']:.1f}个像素，到最后的{late['teacher']:.1f}个像素；扩散强制到"
        "{late['forcing']:.1f}，用带噪声的上下文是{late['forcing_noisy']:.1f}。",

    "f'Our rollouts hardly drift:":
        "我们的滚动生成几乎不漂移：教师强制始终离物理规律不超过{late['teacher']:.1f}个像素，扩散强制不超过{late['forcing']:.1f}个。"
        "弹来弹去的字母很容易接下去；在真实视频里不断累积的误差要复杂得多。",

    'The errors compound because each model trained on real frames':
        '误差之所以累积，是因为每个模型都在真实的帧上训练，现在却要读自己画的、稍有偏差的帧。这种错配有个名字：暴露偏差。',

    'In real video the errors do compound,':
        '在真实视频里，误差确实会累积，因为一个在真实帧上训练的模型，必须读自己画的、稍有偏差的帧。这种错配有个名字：暴露偏差。',

    'The cure for exposure bias is to train on what the model will actually see.':
        "治疗暴露偏差的办法，是用模型将来真正会看到的东西来训练它。<bookmark mark='a'/>2024年12月，CausVid把一个各帧双向互相关注的慢模型，"
        "蒸馏成一个因果模型，每帧只要四个去噪步。<bookmark mark='b'/>2025年6月，Xun Huang和同事用自我强制更进一步：训练时，"
        "模型从自己画的帧出发滚动生成整个片段，<bookmark mark='c'/>再拿整个片段和一个老师比较打分。它在一块GPU上每秒生成17帧，"
        "第一帧不到半秒就出来：视频生成得和播放一样快。<bookmark mark='d'/>让画面响应玩家的操作，就得到了一个交互式的世界模型，"
        "比如Google DeepMind的Genie 3：那是第29部分的内容。",

    # ------------------------------------------------------------------ NeRF
    'Chapter fifteen. Light through a volume.':
        '第15章。穿过体积的光。',

    'So far, pictures and videos. Now the world behind them.':
        "到目前为止，讲的是图片和视频。现在讲它们背后的世界。这是一个小场景，一个金色的字母A和一个蓝色的球，由围成一圈的24台相机拍下来。"
        "<bookmark mark='a'/>一个网络能学会这个场景本身，从而从任何角度展示它吗？<bookmark mark='b'/>2020年，本·米尔登霍尔、"
        "普拉图尔·斯里尼瓦桑、马修·坦西克和同事把场景表示成一个函数：空间里的每一点，有一个密度，表示那里有多少东西，还有一个颜色，"
        "表示它发出的光，可以随观察方向而变。一个小网络来计算它：神经辐射场，NeRF。要渲染一个像素，就沿着穿过它的光线，把一路上的光加起来。",

    'Here is the sum, derived.':
        "这个求和，推导如下。一条光线离开相机，T(t)是来自深度t的光不受阻挡地回到相机的概率。<bookmark mark='a'/>穿过一小段dt，"
        "有西格玛乘dt的比例被挡住。<bookmark mark='b'/>所以T的变化率是负西格玛乘以T，T等于负的累积密度的指数。<bookmark mark='c'/>"
        "像素的颜色，是每个深度发出的光，西格玛乘c，乘以它到达的概率，沿着光线加起来。<bookmark mark='d'/>为了计算，把光线切成若干段，"
        "每段内密度和颜色不变：每一段的积分都是精确的，等于它的透射率乘以1减e的负西格玛德尔塔次方，再乘以它的颜色。<bookmark mark='e'/>"
        "把各段加起来：每段贡献它的不透明度阿尔法，乘以它的颜色，再乘以穿过它前面所有东西的概率。这就是阿尔法合成，"
        "从1980年代起，计算机图形学就用它来叠加半透明的图片。",

    '"Why not just add sigma times delta?':
        "为什么不直接把西格玛乘德尔塔加起来？在一个密度均匀的球上检验一下，那里精确答案是已知的。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>{edge}",

    "At every number of samples, NeRF's sum is the more accurate:":
        '无论采样多少个点，NeRF的求和都更准确：在密度不变的一段里它是精确的，误差只来自横跨球边界的那几段。',

    "NeRF's sum is exact within a segment of constant density;":
        'NeRF的求和在密度不变的一段里是精确的；误差只来自横跨球边界的那几段。',

    'f"With {Ns[0]} samples the Riemann sum gives {r0:.2f}, more light':
        "用{Ns[0]}个采样点时，黎曼和给出{r0:.2f}，比实际存在的光还多；NeRF的求和误差只有{ner[0]:.1e}。",

    'f"With {Ns[0]} samples the Riemann sum gives {r0:.2f}; NeRF':
        "用{Ns[0]}个采样点时，黎曼和给出{r0:.2f}；NeRF的求和误差只有{ner[0]:.1e}。",

    'f"Now train one: an MLP of four layers':
        "现在训练一个：一个四层的MLP，{int(d['params']):,}个权重，点的坐标先经过频率逐级升高的正弦和余弦，这样它才画得出清晰的边缘。"
        "<bookmark mark='a'/>每一步渲染{int(d['NR'])}条随机光线，每条{int(d['NS'])}个采样点，再和照片的像素比较。<bookmark mark='b'/>"
        "这是一个它从没见过的视角，在各个检查点的样子。它的峰值信噪比，越高越好，从{ps[0]:.1f}分贝升到第{checks[-2]:,}步的{ps[-2]:.1f}，"
        "最后是{ps[-1]:.1f}；三个随机种子在{tp.min():.1f}到{tp.max():.1f}之间。<bookmark mark='c'/>同样的权重还免费给出了深度："
        "从平面照片里学到的场景形状。",

    # ------------------------------------------------------------------ Splat
    'Chapter sixteen. Gaussian splatting.':
        '第16章。高斯泼溅。',

    "NeRF's catch is speed:":
        "NeRF的问题是速度：每个像素都要沿着光线计算几十次网络。2023年，伯恩哈德·克尔布尔、乔治·德雷塔基斯和同事用一团三维高斯取代了网络，"
        "数以百万计的柔软小团块。<bookmark mark='a'/>每个高斯有一个位置，<bookmark mark='b'/>一个形状，也就是由一个旋转和三个尺度构成的协方差，"
        "这样它永远是合法的协方差，<bookmark mark='c'/>还有一个不透明度和一个颜色。<bookmark mark='d'/>渲染时，把每个团块投影到屏幕上，"
        "成为一个扁平的椭圆，再从前到后把它们混合起来。不用沿光线一步步走：论文在1080p下渲染，每秒30帧以上。",

    'What ellipse does a 3D Gaussian make on the screen?':
        "一个三维高斯在屏幕上会形成什么样的椭圆？推导一下。<bookmark mark='a'/>先旋转到相机的坐标系。<bookmark mark='b'/>"
        "然后是透视投影：除以深度。这不是线性的，而高斯经过非线性映射就不再是高斯。<bookmark mark='c'/>所以做线性化：在均值附近，"
        "投影近似等于它的雅可比矩阵J。<bookmark mark='d'/>高斯经过线性映射仍是高斯，协方差是J W 西格玛 W转置 J转置。这是2001年马蒂亚斯·茨维克和同事的"
        "EWA泼溅，是这个方法核心的图形学思想。",

    'f"Is the linearization good?':
        "线性化够好吗？从一个三维高斯里采样二十万个点，每个点都精确投影，再把它们的散布和公式比较。<bookmark mark='a'/>对一个宽度是深度十分之一的高斯，"
        "公式给出的协方差偏差{100 * errs[i10]:.1f}%。<bookmark mark='b'/>误差随高斯变大而增长：从深度百分之一时的{100 * errs[0]:.2f}%，"
        "到{rel[-1]:g}时的{100 * errs[-1]:.0f}%，大致按尺寸的{slope:.1f}次方增长。泼溅用的高斯都很小，所以在用到它的地方，这个近似是成立的。",

    'f"We fitted {int(s[\'N\'])} Gaussians':
        "我们把{int(s['N'])}个高斯拟合到同样的24张照片上，通过渲染器做梯度下降，过程中把褪色的高斯挪到忙碌的高斯旁边。<bookmark mark='a'/>"
        "这是它们安顿下来时那个没见过的视角：峰值信噪比从{ps[0]:.1f}分贝升到{ps[-1]:.1f}。<bookmark mark='b'/>{verdict}<bookmark mark='c'/>{speed}",

    'f"Rendering a view takes':
        "渲染一个视角要{gr.mean():.0f}毫秒，NeRF要{nr.mean():.0f}毫秒，用的还是我们简单的代码；在GPU上，用论文的分块光栅化器，它能实时运行。",

    'f"Our plain code renders a view in':
        "我们简单的代码渲染一个视角要{gr.mean():.0f}毫秒，NeRF要{nr.mean():.0f}毫秒：我们在每个像素上计算每一个高斯。论文的GPU光栅化器把高斯分到小块里，"
        "每个像素只碰覆盖它的那几个，实时就是这样来的。",

    "f'After the same number of steps,":
        '训练步数相同时，{comp}：高斯是{gp.mean():.1f}分贝，NeRF是{npp.mean():.1f}分贝。',

    'NeRF and splatting fit one scene at a time':
        "NeRF和泼溅一次只拟合一个场景，还需要精心标定过的照片。<bookmark mark='a'/>Instant-NGP让拟合只需几秒。<bookmark mark='b'/>"
        "然后Transformer学会了直接看出三维：DUSt3R把两张没有标定的照片变成三维点，<bookmark mark='c'/>VGGT，CVPR 2025的最佳论文，"
        "从几百个视角一次就预测出相机、深度和点，不到一秒。<bookmark mark='d'/>把这些视角生成出来，就能生成世界，那是第29部分的主题。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock.":
        "我们来总结一下。一张图片是一串图块，Transformer读它，甚至学会了它来自的网格。模型在一个压缩空间里作画，这个空间有多小、"
        "有多大意义，决定了一切；借用一个视觉模型的眼睛，能加快学会画画。去噪器变成了Transformer，通过带门控的归一化被告知要画什么。"
        "更大的图片需要偏移它们的噪声，偏移的因子我们推导并检验过了。图片也可以写成词元，最好由粗到细，这让一个模型能读、能画、能编辑。"
        "视频是时间上的同一回事：一起画的帧彼此一致，一帧一帧画的帧能向前滚动。而三维，是沿着光线把光加起来，或者把高斯泼溅到屏幕上。",

    'All of this comes back.':
        "这些都会再回来。图像编码器，以及把图片和文字联系起来的CLIP和SigLIP，是第23部分的内容，那里每一种感官都变成词元。"
        "REPA借用其眼睛的自监督编码器，是第24部分。三维结构上的扩散，会在第25部分的AlphaFold 3里再出现。响应玩家操作的视频是一个世界模型，第29部分。"
        "而分辨真实图片和生成图片，是最后一部分关于信任的内容。",

    'Here are six problems,':
        '这里有六道习题，从数视觉Transformer的词元，到投影一个高斯。在这里暂停，自己做一做；完整的解答在这一部分的笔记里。',

    'Next time: every sense as a token.':
        '下一次：每一种感官都是词元。文字怎样被切成词元，声音怎样也变成词元，CLIP怎样把图片和文字联系起来，一个Transformer又怎样把它们全部读进来：第23部分。',

    "Simon Prince's Understanding Deep Learning":
        '想深入学习，图像模型可以读西蒙·普林斯的《理解深度学习》，三维可以读理查德·塞利斯基的《计算机视觉》。谢谢观看，第23部分再见。',
})

PHRASES = {
    # spliced-in English values
    'in-context tokens': '上下文词元',
    'plain adaLN': '普通adaLN',
    'adaLN-Zero': 'adaLN-Zero',
    'raster order': '光栅顺序',
    'MaskGIT': 'MaskGIT',
    'VAR': 'VAR',
    'teacher forcing': '教师强制',
    'diffusion forcing': '扩散强制',
    'diffusion forcing with noisy context': '用带噪声上下文的扩散强制',
    'the clip model': '整段片段的模型',
    'the Gaussians match the photographs more closely': '高斯和照片更吻合',
    'NeRF matches the photographs more closely': 'NeRF和照片更吻合',
    'the two match the photographs about equally well': '两者和照片吻合得差不多',
    'a single sampling step': '只采样一步',
    'One network learns both': '一个网络两样都学会了',
    '2 sampling steps': '采样2步',
    '4 sampling steps': '采样4步',
    '8 sampling steps': '采样8步',
    '16 sampling steps': '采样16步',
    '40 sampling steps': '采样40步',
}
