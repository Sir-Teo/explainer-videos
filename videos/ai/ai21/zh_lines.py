"""Chinese narration for ai21: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第21部分：扩散与流'

CHAPTERS = {
    'Hook': '从噪声开始',
    'Forward': '1. 慢慢地摧毁数据',
    'ELBO': '2. 下界，以及猜噪声',
    'Tweedie': '3. 特威迪公式',
    'DSM': '4. 去噪分数匹配',
    'SDE': '5. 让时间倒流',
    'Samplers': '6. DDPM与DDIM',
    'Schedules': '7. 噪声调度',
    'EDM': '8. EDM：预条件化与休恩法',
    'DPMSolver': '9. DPM-Solver：精确求解线性部分',
    'Transport': '10. 最优传输与流匹配',
    'Reflow': '11. 整流流与重流',
    'Distill': '12. 蒸馏',
    'OneStep': '13. 从零开始的一步生成',
    'Guidance': '14. 引导',
    'Pictures': '15. 从点到图片',
    'Discrete': '16. 离散数据上的扩散',
    'TextLM': '17. 扩散语言模型',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    'Noise: three hundred random points.':
        "噪声：300个随机的点。<bookmark mark='a'/>一个就在这台电脑上训练出来的网络，把每个点轻轻推一下，推50次。"
        "<bookmark mark='b'/>第20部分结束在朗之万动力学上：沿着分数函数，也就是数据对数密度的坡度，往上走，"
        "同时把噪声一级一级地调小。这里的网络，已经只凭例子，学会了每个噪声水平下的那个坡度。",

    'How we got here. In 2015 Jascha Sohl-Dickstein':
        "我们是怎么走到这里的。2015年，亚沙·索尔-迪克斯坦和同事从物理学借来一个想法：用噪声慢慢地摧毁数据里的结构，"
        "再学会把这个摧毁过程倒着运行。<bookmark mark='a'/>2019年，宋飏和斯特凡诺·埃尔蒙在许多噪声水平上学习分数函数；"
        "<bookmark mark='b'/>2020年，乔纳森·何、阿杰·贾因和彼得·阿比尔把配方变得很简单：只要猜噪声。"
        "<bookmark mark='c'/>2021年，一个框架把它们统一起来，扩散模型超过了GAN。<bookmark mark='d'/>2022年，"
        "潜空间扩散成了Stable Diffusion，并公开了权重；<bookmark mark='e'/>接着，Transformer当上了去噪器，"
        "<bookmark mark='f'/>直线式的流训练出了2024年的图像模型，视频也随之而来；<bookmark mark='g'/>到2025年，同一个想法开始写文字，"
        "<bookmark mark='h'/>2026年，Google发布了一个开放权重的扩散语言模型。",

    'This is Part 21 of AI, Built: diffusion and flow.':
        "这是《人工智能，从零搭建》的第21部分：扩散与流。<bookmark mark='a'/>本部分的内容：前向过程，以及训练反向过程的那个下界；"
        "为什么猜噪声就是在学分数函数；<bookmark mark='b'/>让时间倒流，用随机方程或确定性方程，以及求解它们的采样器；"
        "<bookmark mark='c'/>各种设计选择，从噪声调度到EDM和DPM-Solver；<bookmark mark='d'/>流匹配与最优传输；"
        "<bookmark mark='e'/>怎样从50步走到1步；怎样要求它画出特定的东西；<bookmark mark='f'/>还有用于文本的扩散，"
        "我们自己的一个语言模型也会登上记分牌。<bookmark mark='g'/>这里的每一个模型，都是在这台电脑上训练的。",

    # ------------------------------------------------------------------ Forward
    'Chapter one. Destroying data slowly.':
        '第1章。慢慢地摧毁数据。',

    'Annealed Langevin, at the end of Part 20':
        "第20部分末尾的退火朗之万方法，需要每个噪声水平下的分数函数。这些噪声水平从哪里来？来自一个故意摧毁数据的过程。"
        "<bookmark mark='a'/>把每个点朝原点缩一点点，再加上一点高斯噪声。<bookmark mark='b'/>这样做1000次。缩小让散布不会越来越大；"
        "噪声则一步一步地抹掉字母，直到只剩下一团圆圆的钟形噪声。<bookmark mark='c'/>这就是前向过程。它没有参数：里面没有任何东西是学出来的。",

    "You don't have to run the thousand steps":
        "要知道一个点最后落在哪里，并不需要真的跑完1000步。先写出一步：缩小后的点，加上新的噪声。<bookmark mark='a'/>把前一步代进去。"
        "<bookmark mark='b'/>两份噪声是相互独立的高斯变量，所以它们的和还是一个高斯变量，方差等于两者方差之和。<bookmark mark='c'/>"
        "一直往下代到干净的点，整条链就塌缩成一次跳跃：数据乘以阿尔法拔的平方根，再加上方差为1减阿尔法拔的噪声，"
        "其中阿尔法拔是所有缩小因子的乘积。<bookmark mark='d'/>所以训练时可以直接抽取任意一个噪声水平，不必模拟整条链。",

    'f"Check it on our letters. Run twenty thousand points':
        "在我们的字母上检验一下。让2万个点跑完全部1000步，并在{len(rows)}个时刻，把它们所在的位置对它们的起点做回归。"
        "<bookmark mark='a'/>斜率应该是阿尔法拔的平方根：在第500步，它是{r5['slope']:.3f}，公式给出{r5['slope_pred']:.3f}。"
        "<bookmark mark='b'/>剩余的方差应该是1减阿尔法拔：{r5['resid']:.3f}，对比{r5['resid_pred']:.3f}。任何地方最大的差距是"
        "{worst:.3f}，<bookmark mark='c'/>{verdict}跑完全部1000步后，阿尔法拔是{man:.1f}乘以10的负{ex}次方："
        "一个点剩下的部分，只有它原来的{left:.4f}。",

    'and whole clouds agree as well as two independent jumps':
        '整团点云的吻合程度，也和两次独立跳跃之间的吻合程度一样。',

    'and whole clouds agree nearly as well as two independent jumps':
        '整团点云的吻合程度，也几乎和两次独立跳跃之间一样。',

    "One more fact, and the model's job is defined.":
        "再说一个事实，模型的任务就定下来了。把一步倒过来走，并假设你知道干净的点。<bookmark mark='a'/>贝叶斯公式说，前一个点的分布，"
        "等于前向的那一步，乘以跳到第t减1步的那次跳跃：两者都是前一个点的高斯函数，所以配方之后得到一个高斯分布，"
        "<bookmark mark='b'/>它的均值是干净的点和带噪声的点的一个混合。<bookmark mark='c'/>在连续时间里，用阿尔法表示缩小，用西格玛表示噪声："
        "两者的平方加起来等于1。我们的选择是四分之一个圆，余弦和正弦，也就是第5部分奥恩斯坦-乌伦贝克那一章的前向过程，换了一个时钟来跑。"
        "<bookmark mark='d'/>只要知道你是从哪里出发的，每一步往回走都是一个已知的高斯分布。模型却得在不知道的情况下完成这件事。",

    # ------------------------------------------------------------------ ELBO
    'Chapter two. The bound, and guessing the noise.':
        '第2章。下界，以及猜噪声。',

    "Part 20's variational autoencoder had a code and a bound.":
        "第20部分的变分自编码器有一个编码，还有一个下界。这里的编码，是那些带噪声的版本，从x 1到x T，而编码器就是前向过程，固定不变。"
        "<bookmark mark='a'/>解码器把这条链倒着运行，每一步是一个高斯分布，它的均值由一个网络来决定。詹森不等式给出的，"
        "还是和以前一样的对数似然下界。<bookmark mark='b'/>两条链都是各步的乘积，所以这个下界是对各步的求和。<bookmark mark='c'/>"
        "现在用上一章的那个事实：在已知干净点的条件下，用贝叶斯公式改写每一个前向步。多出来的那些跳跃两两抵消，剩下的是一串KL散度，"
        "每步一个：在已知干净点时，网络往回走的一步，离真正往回走的一步有多远。",

    'Each term compares two Gaussians with the same variance':
        "每一项比较的是两个方差相同的高斯分布，所以它就是两者均值之间距离的平方。<bookmark mark='a'/>把干净的点代换掉，"
        "用带噪声的点和造成它的那份噪声来写出真正的均值。<bookmark mark='b'/>这提示了乔纳森·何、贾因和阿比尔在2020年选用的参数化方式："
        "让网络输出对噪声的猜测，再用同样的方式构造它的均值。<bookmark mark='c'/>这样，下界的每一项，都是一个权重拉姆达t，"
        "乘以噪声猜测的平方误差。训练扩散模型就是做回归：看着一个带噪声的点，说出加进去的是什么噪声。",

    'f"How big are the weights?':
        "这些权重有多大？在DDPM的调度下，把每一步的方差设成贝塔，拉姆达从第一步的{lam[0]:.2f}，降到最后一步的{lam[-1]:.3f}，"
        "相差{ratio:.0f}倍：这个下界最在意的，是那些几乎干净的步。<bookmark mark='a'/>乔纳森·何和同事发现，干脆把权重全部去掉，"
        "每一步一视同仁，画出来的图反而更好：在CIFAR-10上FID达到3.17，是当时最好的成绩。<bookmark mark='b'/>这就是简化损失，"
        "此后几乎所有的扩散模型，训练用的都是类似它的损失。精确的加权会在第7章回来：它其实是在选择最常练习哪些噪声水平。",

    '"Here is our own denoiser learning on the letters':
        "这是我们自己的去噪器，正在字母上学习，用的是简化损失，每个训练样本随机抽一个噪声水平。在每个检查点，我们停下来，"
        "从同一份噪声里画出一些点。<bookmark mark='a'/>还没训练时，它把这些点甩到了边上。<bookmark mark='b'/>{early}"
        "<bookmark mark='c'/>到第{c_read:,}步，字母已经认得出来了。剩下的都是精修：损失几乎不动，但笔画越来越清晰，"
        "与数据的距离从{s_read:.2f}降到{s_end:.2f}，{trend}。"
        "训练的每一步，只要求它猜出一个模糊的点里的噪声；字母就从数百万次这样的猜测中浮现出来。",

    "f'Within {checks[k1]} steps the loss has made":
        '不到{checks[k1]}步，损失就已经完成了整个降幅的{pct:.0f}%，这些点也收拢成了一团，离数据{sw[k1]:.2f}。',

    "f'Within {checks[k1]} steps the points have pulled in":
        '不到{checks[k1]}步，这些点就收拢成了一团，离数据{sw[k1]:.2f}，损失还在下降。',

    # ------------------------------------------------------------------ Tweedie
    "Chapter three. Tweedie's formula.":
        '第3章。特威迪公式。',

    'A noisy point could have come from many clean ones.':
        "一个带噪声的点，可能来自许多不同的干净点。这是一个一维的数据分布，两个鼓包。<bookmark mark='a'/>我们看到一个带噪声的值x t，"
        "噪声水平中等。<bookmark mark='b'/>贝叶斯公式给出它所来自的干净值的分布：很宽，因为噪声很宽，同时又被拉向那两个鼓包。"
        "<bookmark mark='c'/>期望平方误差最小的猜测，就是这个分布的平均值，也就是后验均值。用平方误差训练出来的网络，"
        "只要做得到，学会输出的就是它。<bookmark mark='d'/>移动这个带噪声的值，后验均值就在两个鼓包之间滑动，却从来到不了任何一个。",

    'That average has a formula. Herbert Robbins':
        "这个平均值有一个公式。赫伯特·罗宾斯在1956年发表了它，并把功劳归于莫里斯·特威迪：后验均值等于带噪声的点，"
        "加上西格玛平方乘以分数函数，再除以阿尔法。<bookmark mark='a'/>证明只有三行。加了噪声的密度，是干净密度的一个模糊版本。"
        "<bookmark mark='b'/>在积分号下求导：只有那个高斯函数依赖于x。<bookmark mark='c'/>除以这个密度，贝叶斯公式就把积分变成了后验均值。"
        "<bookmark mark='d'/>再看噪声。对噪声的最佳猜测，是带噪声的点减去阿尔法乘以最佳的干净点，再除以西格玛：也就是负的西格玛乘以分数函数。"
        "一个被训练来猜噪声的网络，就是在学分数函数。扩散模型之所以行得通，原因就在这里。",

    'f"Check it. In one dimension, compute the posterior mean':
        "检验一下。在一维情形下，用蛮力算出后验均值，在一张很细的网格上积分，再和用精确分数函数算出的特威迪公式比较。"
        "<bookmark mark='a'/>两者在小数点后{decimals}位上都一致：这个公式是精确的。<bookmark mark='b'/>在二维的字母上，用蒙特卡洛方法估计每个后验均值，"
        "按5万个干净点各自产生这个带噪声点的可能性来加权。<bookmark mark='c'/>这些估计平均落在离公式{worst_mc:.3f}以内的地方。"
        "<bookmark mark='d'/>{net_says}",

    'f"Our trained network\'s guesses sit within':
        '我们训练出来的网络，它的猜测离公式的结果在{worst_net:.3f}以内，和{spread:.2f}的散布相比很小：它学会了分数函数。',

    'f"Our trained network\'s guesses are within':
        '我们训练出来的网络，它的猜测离公式的结果在{worst_net:.3f}以内，而散布是{spread:.2f}：接近，但不精确。',

    'f"What does the best denoiser do with very noisy points?':
        "面对噪声很大的点，最好的去噪器会怎么做？这是它对500个带噪声的点的猜测，在4个噪声水平下。<bookmark mark='a'/>噪声很大时，"
        "每个猜测都落在字母的中间附近：一个平均的字母，平方误差是{e0:.2f}。<bookmark mark='b'/>随着噪声减小，猜测散开到笔画上，"
        "误差降到{e1:.3f}。<bookmark mark='c'/>所以不能一步从纯噪声跳到一个样本：最好的一跳，落在一片模糊上。采样器于是改走许多小步，"
        "随着噪声降低不断重新猜测：这是第5章和第6章的内容。",

    # ------------------------------------------------------------------ DSM
    'Chapter four. Denoising score matching.':
        '第4章。去噪分数匹配。',

    'f"Tweedie says the network should learn the score.':
        "特威迪公式说，网络应该学分数函数。可是，没有人会把真实图像的分数函数交给我们去拟合。2005年，阿波·许韦里宁在能量模型上"
        "遇到了同样的问题：在目标未知的情况下，用平方误差把一个函数s拟合到分数函数上。<bookmark mark='a'/>分部积分把目标消掉了："
        "剩下的是s的雅可比矩阵的迹，加上它长度的平方，再对数据取平均。<bookmark mark='b'/>可是这个迹，每个维度都要做一次反向传播："
        "一张512乘512像素的彩色图像，就要{d:,}次，而且每个训练样本都要这么多。",

    'In 2011 Pascal Vincent found the way around.':
        "2011年，帕斯卡尔·文森特找到了绕过去的办法。给每个样本加上噪声，然后去拟合这份噪声本身的分数函数，这是我们确切知道的。"
        "<bookmark mark='a'/>定理是：这个损失，等于对整个加噪数据的分数函数的损失，再加上一个常数。原因如下。把左边的平方展开。"
        "<bookmark mark='b'/>唯一可能不同的，是交叉项。把加噪数据的分数函数，写成它的梯度除以它自己；<bookmark mark='c'/>加噪数据，"
        "是围绕每个样本的噪声的平均，所以它的梯度也是它们梯度的平均；<bookmark mark='d'/>这正是左边的交叉项。其余的都是常数。"
        "<bookmark mark='e'/>而所加噪声的分数函数，等于负的噪声除以西格玛：拟合它，恰恰就是第2章的猜噪声。",

    'f"Our letters let us check the theorem directly':
        "在我们的字母上，可以直接检验这个定理，因为那里的精确分数函数是已知的。取我们的去噪器在训练中每个检查点的状态，"
        "在最低的噪声水平，t等于{ts[k]:g}。<bookmark mark='a'/>白色曲线是在新噪声上的损失。灰色的线是那个常数：就连精确的分数函数，"
        "也会有这么大的损失，因为一个带噪声的点里的噪声，没法被完全恢复。<bookmark mark='b'/>橙色曲线是网络相对于精确分数函数的误差，"
        "是直接测出来的。<bookmark mark='c'/>定理说，损失减去常数就是这个误差，而那些点正好落在曲线上：到最后，{f0[0]:.4f}减"
        "{f0[1]:.4f}，对比{f0[2]:.4f}。证明中说会平均掉的那个交叉项，在训练结束时最多只有{cross:.4f}，{n_seeds}个随机种子都是如此。"
        "<bookmark mark='d'/>损失永远到不了0，也不需要到0：高出常数的那一截，才是训练能够去掉的部分。",

    "f'Where is the score hardest to learn?":
        "分数函数在哪里最难学？训练结束时，误差在t等于{worst:g}时最大，在{best:g}时最小：{where}<bookmark mark='a'/>2019年，"
        "宋飏和斯特凡诺·埃尔蒙就用这种方法，为许多噪声水平训练了同一个网络，并用第20部分的退火朗之万方法来采样。"
        "<bookmark mark='b'/>在每个噪声水平上去噪，只靠普通的回归：每一个扩散模型学的，都是这个。",

    'the nearly clean levels, where the score is sharp':
        '几乎干净的那些水平最难，因为在那里，分数函数围绕每一笔都很陡。',

    'the hardest level is not the cleanest one.':
        '最难的水平并不是最干净的那个。',
}

PHRASES = {}

ZH.update({
    # ------------------------------------------------------------------ SDE
    'Chapter five. Running time backwards.':
        '第5章。让时间倒流。',

    'In 2021 Yang Song and colleagues let the number of steps go to infinity.':
        "2021年，宋飏和同事让步数趋于无穷。<bookmark mark='a'/>由许多小的缩小和小的冲击组成的链，变成了一个随机微分方程："
        "一个朝向原点的漂移，加上布朗运动，也就是第5部分的奥恩斯坦-乌伦贝克过程，只是速率随时间上升。"
        "<bookmark mark='b'/>运行它，字母就溶解成一团钟形的噪声。",

    'In 1982 Brian Anderson showed':
        "1982年，布赖恩·安德森证明，这样的扩散过程在时间上反过来，也还是一个扩散过程：同样的缩小和冲击，再加上一股沿那一刻"
        "加噪数据的分数函数往上推的力。<bookmark mark='a'/>其中唯一不知道的就是分数函数，而前面三章讲了网络怎样学会它。"
        "<bookmark mark='b'/>这里用我们字母的精确分数函数来运行它：噪声流回字母里，每个点一路都在抖动。",

    'There is a second way back, with no randomness at all.':
        "还有第二条回去的路，完全没有随机性。从第5部分关于密度的福克-普朗克方程出发：漂移让它移动，噪声让它扩散。"
        "<bookmark mark='a'/>扩散项可以改写，因为p的梯度等于p乘以对数p的梯度。<bookmark mark='b'/>这样两项都成了某个量乘以p的散度："
        "一个连续性方程，也就是粒子随一个速度场运动的流体所遵守的定律。<bookmark mark='c'/>所以，只要粒子沿着这个速度走，"
        "完全不加噪声，它们在每一刻的密度，就和那些带噪声的粒子完全一样。<bookmark mark='d'/>宋飏和同事把它叫作概率流常微分方程："
        "同一个分数函数的又一种用法。",

    'f"Here are both, run with the exact score from the same forty starting points.':
        "这是两者，都用精确的分数函数，从同样的40个起点出发。<bookmark mark='a'/>SDE的路径弯弯绕绕：平均每条长{float(s['sde_len']):.1f}。"
        "ODE的路径则是滑过去的，{float(s['ode_len']):.1f}。它们的终点不一样。<bookmark mark='b'/>但是，在每一个时刻，把整团点云和真实密度的"
        "新样本相比。{verdict}<bookmark mark='c'/>而且ODE可以双向运行：从数据到噪声，再回来，点回到起点，精确到小数点后{dec}位："
        "一个可逆的映射，也就是第20部分的连续归一化流，带有精确的似然。一个学到的分数函数，两条回去的路；接下来几章讲的，"
        "就是怎样用尽可能少的步数求解它们。",

    'Both stay as close to the true marginals':
        '两者都和真实边缘分布的新样本一样接近它，在我们测量的每一个时刻都是如此。',

    'f"The ODE stays as close to the true marginals':
        'ODE一路下来，都和真实边缘分布的新样本一样接近它；SDE用了{n_sde:,}个随机步，在最后稍有偏离，{end_s:.3f}，对比ODE的{end_o:.3f}：'
        '随机的步子需要更小。',

    "f'Both stay near the true marginals":
        '两者都在真实边缘分布附近；到最后，SDE离它{end_s:.3f}，ODE离它{end_o:.3f}。',

    # ------------------------------------------------------------------ Samplers
    'Chapter six. DDPM and DDIM.':
        '第6章。DDPM与DDIM。',

    'Two ways to discretize the walk back':
        "把往回走的过程离散化，有两种方法，都用我们训练好的去噪器。DDPM，也就是2020年的配方，离散化的是反向SDE：每一步，"
        "它先猜出干净的点，再走到第1章的那个高斯分布，并加上一点新的噪声。<bookmark mark='a'/>它的路径弯弯绕绕，"
        "就像它所反转的布朗运动。<bookmark mark='b'/>一年以后的DDIM完全不加噪声：每个点都滑向一个固定的终点，而且需要的步数少得多。",

    "DDIM's step is two lines.":
        "DDIM的一步只有两行。从带噪声的点出发，网络对噪声的猜测，通过特威迪公式，给出对干净点的猜测。<bookmark mark='a'/>要走到更低的噪声水平，"
        "就把这个干净的猜测放回去，配上更少的噪声，并保持噪声的方向：同一份噪声，只是变小了。<bookmark mark='b'/>除以阿尔法，"
        "这一步恰好就是概率流ODE的一个欧拉步，所用的坐标是x除以阿尔法，以及西格玛除以阿尔法。<bookmark mark='c'/>宋佳铭、孟辰霖和埃尔蒙"
        "是从另一个具有相同边缘分布的前向过程推出它的，还给了它一个旋钮，伊塔：等于0时不加噪声，就是ODE；等于1时，又回到DDPM。"
        "网络不变，变的只是采样器。",

    'f"How few steps will do?':
        "最少几步就够？量一量样本落在离数据多远的地方，<bookmark mark='w'/>用切片瓦瑟斯坦距离：把两团点都投到许多条随机的直线上，"
        "比较它们的点落在哪里。<bookmark mark='a'/>用5步DDIM，字母是模糊的，距离{sw[0]:.2f}；{close}到100步时是{sw[-1]:.3f}，"
        "而数据本身的一份新样本是{floor:.3f}，这是下限。<bookmark mark='b'/>每一步都要运行一次网络，所以步数越少，出图越快。"
        "这些路径是弯的，而弯的路径需要很多小步：接下来三章，讲的都是怎样少走几步。",

    'f"by {k_close} it is about as close':
        '到{k_close}步时，它就和DDPM的200步差不多接近了；',

    "even at a hundred it trails DDPM's two hundred;":
        '即使到了100步，它还是不如DDPM的200步；',

    # ------------------------------------------------------------------ Schedules
    'Chapter seven. Noise schedules.':
        '第7章。噪声调度。',

    'f"A noise schedule says how much signal survives':
        "噪声调度规定了每个时刻有多少信号保留下来。它的核心是一个数：信噪比，阿尔法平方除以西格玛平方，最好在对数尺度上看。"
        "<bookmark mark='a'/>DDPM的线性贝塔、亚历克斯·尼科尔和普拉富拉·达里瓦尔的余弦调度、我们的调度，以及流匹配的直线，"
        "都是从信号充足走到几乎没有信号，只是速度各不相同。<bookmark mark='b'/>有一个细节很要紧：DDPM的最后一步，对数信噪比还有"
        "{lt:.1f}，而不是负无穷。<bookmark mark='c'/>2024年，Shanchuan Lin和同事指出，一个从来没在纯噪声上训练过的模型，"
        "画不出很暗或很亮的图片，于是他们重新缩放调度，让它在终点降到0。",

    'Does the schedule change what is being learned?':
        "调度会不会改变学到的东西？2021年，迪德里克·金马、蒂姆·萨利曼斯、本·普尔和乔纳森·何把这个下界推广到连续时间："
        "对时间积分的干净点误差，权重是信噪比下降的快慢。<bookmark mark='a'/>把变量换成信噪比本身，调度就消失了：只剩下它的两个端点。"
        "端点相同的调度，下界都一样。<bookmark mark='b'/>调度真正改变的是练习：时间均匀抽取时，每种调度访问各个噪声水平的频率不同，"
        "而网络在练得最多的地方学得最好。<bookmark mark='c'/>下一章的EDM干脆跳过调度，直接从对数正态分布里抽噪声水平。",

    'f"We trained the same noise-guessing network four ways':
        "我们用4种方式训练同一个猜噪声的网络，只改变它练习哪些噪声水平：预算相同，每种{len(heun['cos'])}个随机种子。"
        "<bookmark mark='a'/>因为我们字母的精确去噪器是已知的，可以看出每一种错在哪里。在低噪声时，它们都一致。"
        "<bookmark mark='b'/>在最高的噪声水平，{SPOKEN[hi_err]}偏得最远，而{SPOKEN[lo_hi]}最接近：正是在那里练得最多的那一个。"
        "<bookmark mark='c'/>{verdict}",

    "f'After sampling, the spreads overlap":
        '采样之后，各自的散布互相重叠：平均来看，{SPOKEN[best]}最好，{SPOKEN[worst]}最差，但随机种子之间的差别，和调度之间的差别一样大。',

    "f'After sampling, {SPOKEN[best]} is best":
        '采样之后，{SPOKEN[best]}最好，{SPOKEN[worst]}最差，前者的每个随机种子都胜过后者的每个随机种子。',

    '"The schedule also decides where a sampler puts its steps.':
        "调度还决定了采样器把步子放在哪里。这里是3种采样器，用精确的去噪器，在同样大约16次网络调用的预算下，"
        "用4种噪声水平的间隔方式。<bookmark mark='a'/>{v1}<bookmark mark='b'/>{v2}<bookmark mark='c'/>{v3}"
        "<bookmark mark='d'/>{edm_note}",

    "On image models EDM's spacing has become a standard; on our letters":
        '在图像模型上，EDM的间隔方式已经成了标准；在我们的字母上，它并不总是最好的。间隔方式是采样器的一个设置，和别的设置一样需要调。',

    "On image models EDM's spacing has become a standard, and on our letters":
        '在图像模型上，EDM的间隔方式已经成了标准，在我们的字母上，它也是最好的。',

    "f'For DDIM, the best of the four spacings is":
        '对DDIM来说，最好的是{sp_ddim}；',

    'f"for Heun\'s method, the best is {sp_heun} too;"':
        '对休恩法，也是{sp_heun}；',

    'f"for Heun\'s method, the best is {sp_heun};"':
        '对休恩法，是{sp_heun}；',

    "f'and for DPM-Solver plus plus, {sp_dpm} as well":
        '对DPM-Solver++，同样是{sp_dpm}：有一种间隔方式对三者都最好。',

    "f'and for DPM-Solver plus plus, {sp_dpm}: no spacing":
        '而对DPM-Solver++，是{sp_dpm}：没有哪种间隔方式对每个求解器都最好。',

    # ------------------------------------------------------------------ EDM
    'Chapter eight. EDM: preconditioning and Heun.':
        '第8章。EDM：预条件化与休恩法。',

    'By 2022 there were many diffusion models':
        "到2022年，扩散模型已经有很多种，每种都有自己的调度、参数化和采样器。英伟达的泰罗·卡拉斯和同事把它们一一拆开。"
        "<bookmark mark='a'/>去掉缩小：让x等于干净的点加上大小为西格玛的噪声，西格玛从80一直降到几乎为0。<bookmark mark='b'/>"
        "取阿尔法等于1，特威迪公式说，分数函数就是去噪器的修正量除以西格玛平方。<bookmark mark='c'/>概率流ODE也变得非常朴素："
        "x随西格玛的变化率，等于x减去它去噪后的版本，再除以西格玛。<bookmark mark='d'/>一切，每一种调度和参数化，都只是计算去噪器D的一种方式。",

    'f"Their first idea is preconditioning':
        "他们的第一个想法是预条件化：把网络包装起来，让它在每个噪声水平上面对的任务看起来都一样。把去噪器写成一条跳跃连接，"
        "加上一个缩放过的网络。<bookmark mark='a'/>把输入缩放到单位方差，<bookmark mark='b'/>选择跳跃连接的系数，让网络的误差被放大得尽量少，"
        "<bookmark mark='c'/>然后选输出的缩放，让目标也具有单位方差。<bookmark mark='d'/>为什么这很重要：如果预测噪声，输出里的一个误差，"
        "会让干净点的猜测移动西格玛倍那么多，在最高处是80倍。如果预测干净的点，那么即使几乎没有噪声，网络也得把整个答案输出出来。"
        "EDM的混合目标从来不比两者中的任何一个差。在我们的字母上，数据的散布西格玛d是{sd:.2f}，它的目标的散布，"
        "在每个噪声水平都保持在{tf.min():.2f}和{tf.max():.2f}之间。",

    'f"We tested it: the same network':
        "我们做了测试：同一个网络，同样来自EDM对数正态分布的噪声水平，同样的预算，用三种方式解读它的输出，每种{len(heun['eps'])}个随机种子。"
        "<bookmark mark='a'/>和精确的去噪器相比，在最高的噪声水平，{PSPOKEN[worst_hi]}偏得最远；在最低的噪声水平，偏得最远的是"
        "{PSPOKEN[worst_lo]}。<bookmark mark='b'/>{claim}<bookmark mark='c'/>采样之后，平均来看，{PSPOKEN[best]}离数据最近。",

    "EDM's mixture is close to the better of the two":
        'EDM的混合目标在每个水平上，都接近两者中较好的那一个。',

    "EDM's mixture is not the best at every level":
        'EDM的混合目标并不是在每个水平上都最好，但它避开了两种失败。',

    'f"Their second idea is the solver.':
        "他们的第二个想法是求解器。欧拉法沿着一步起点处的斜率走，在弯曲的路径上，它会冲过头。<bookmark mark='a'/>休恩法先走这一个欧拉步，"
        "量出落点处的斜率，再用两个斜率的平均值重走这一步：这是二阶方法，步长减半，误差就降为四分之一，每步需要两次网络调用。"
        "EDM的最后一步是普通的欧拉步。<bookmark mark='b'/>在我们的字母上，{low}在{nfe_h[j31]}次调用时，休恩法的误差比欧拉法小"
        "{ratio:.1f}倍，在{nfe_h[j63]}次时，小{ratio63:.1f}倍。靠这两个想法，再加上精心安排的步长间隔，卡拉斯和同事在CIFAR-10上，"
        "用35次调用就达到了1.79的FID。",

    "f'below about {cross} evaluations":
        '在大约{cross}次调用以下，这个修正可能有害，普通的欧拉法反而更好；但是',

    # ------------------------------------------------------------------ DPMSolver
    'Chapter nine. DPM-Solver: an exact linear part.':
        '第9章。DPM-Solver：精确求解线性部分。',

    'In 2022 Cheng Lu and colleagues at Tsinghua':
        "2022年，清华大学的路橙和同事注意到，这个ODE有一部分根本不需要网络。<bookmark mark='a'/>x除以西格玛这一项，对x是线性的，"
        "可以精确求解，就像用积分因子解一个线性方程那样。<bookmark mark='b'/>剩下的是去噪器在这一步上的积分，权重是拉姆达的指数函数，"
        "拉姆达就是负的对数西格玛。只有这个积分需要近似。这类方法叫作指数积分器。<bookmark mark='c'/>在一步之内把去噪器固定不变，"
        "得出的恰好就是DDIM的更新。所以DDIM本来就是一阶的指数积分器；只要干净点的猜测在这一步里不变，它就是精确的。",

    'To do better, approximate how the denoiser changes':
        "要做得更好，就得近似去噪器在这一步里怎样变化。<bookmark mark='a'/>DPM-Solver-2在这一步的中点，按拉姆达来算的中点，"
        "多花一次调用，用那里的去噪器。<bookmark mark='b'/>DPM-Solver++的两步多步形式，什么额外的都不花：它重用上一步的去噪器，"
        "并把经过这两点的直线延长出去。每步一次网络调用，二阶精度。<bookmark mark='c'/>在CIFAR-10上，最初的版本用10次调用达到了4.70的FID，"
        "用20次达到2.87；它的多步形式，已经收进了常用的扩散模型软件库。",

    'f"Here is the whole family on our letters':
        "这是整个家族在我们字母上的表现，都用精确的去噪器，所以唯一的误差来自求解器，全部用EDM的间隔方式，从同一份噪声出发。"
        "误差是相对于ODE精确解来测的。<bookmark mark='a'/>在对数坐标上，一阶方法的直线斜率是负1，二阶方法是负2。"
        "<bookmark mark='b'/>大约8次调用时，最好的是{SPOKEN[b8]}，误差{e8['err']:.3f}。大约32次时，{SPOKEN[b32]}比DDIM精确"
        "{r32:.0f}倍。<bookmark mark='c'/>{euler_note}<bookmark mark='d'/>{ddpm_note}",

    "f'DDPM, with its fresh noise, has no single path":
        'DDPM每步都加新的噪声，没有一条单一的路径可以比较；它的样本要到{n_ok}次调用，才进入下限的1.5倍以内。',

    'DDPM, with its fresh noise, has no single path to compare, and even at 128':
        'DDPM每步都加新的噪声，没有一条单一的路径可以比较，而且即使到128次调用，它的样本离下限还差得远。',

    "f'One surprise: on our letters, plain Euler":
        '有一个意外：在我们的字母上，在方差保持的时间里用普通欧拉法，反而胜过DDIM，在16次时是{eu:.3f}对{dm:.3f}。'
        'DDIM在干净点的猜测保持不变时是精确的；欧拉法则是在速度保持不变时精确。哪一种一阶方法更好，取决于数据。',

    "f'Plain Euler in time trails DDIM":
        '在时间上用普通欧拉法不如DDIM，在16次时是{eu:.3f}对{dm:.3f}：把干净点的猜测固定住，是更好的一阶选择。',

    'f"{bs}\'s points are the closest to it':
        '{bs}的点离它最近，{ws}的点偏得最远。',

    'f"Here are three of them after about {budget} evaluations':
        "这是其中三种在大约{budget}次调用之后的结果，旁边是精确解。{close_note}"
        "<bookmark mark='a'/>{verdict}而网络自己的误差设定了一个下限：精确求解时，它的ODE落在离数据{net_ref:.3f}的地方，"
        "而字母的一份新样本是{fl:.3f}。<bookmark mark='b'/>那么，10到30次调用，再配上一个懂得这个方程的求解器。比这更少，"
        "就需要另一种想法：第12章。",

    'With our trained network in place of the exact denoiser, the ranking is the same,':
        '用我们训练好的网络代替精确的去噪器，排名不变，',

    'With our trained network in place of the exact denoiser, the ranking shifts,':
        '用我们训练好的网络代替精确的去噪器，排名有所变化，',
})

ZH.update({
    # ------------------------------------------------------------------ Transport
    'Chapter ten. Optimal transport and flow matching.':
        '第10章。最优传输与流匹配。',

    'Step back to an older question.':
        "退回到一个更古老的问题。1781年，加斯帕尔·蒙日问：怎样用最少的功，把一堆土移进一个坑里。<bookmark mark='a'/>"
        "把每一点噪声和每一点数据配成对，让平均的移动距离平方尽可能小：这是列昂尼德·康托罗维奇1942年的版本，它的最小值就是"
        "第20部分的瓦瑟斯坦距离。<bookmark mark='b'/>2000年，让-大卫·贝纳穆和扬·布雷尼耶把同一个问题写成一个流："
        "在所有把一个密度带到另一个密度的速度场里，找出动能最小的那个。<bookmark mark='c'/>答案让每个粒子都以恒定的速度走直线，"
        "而且这些直线从不相交。",

    'Flow matching borrows the straight lines':
        "流匹配借用了这些直线，却不去求解运输问题。2023年，三个团队同时提出了它：Meta的雅龙·利普曼和同事、得克萨斯的刘星超和同事，"
        "以及纽约的迈克尔·阿尔贝戈和埃里克·范登-艾因登。<bookmark mark='a'/>把噪声和数据随机配对，用直线连起每一对，"
        "这一对的速度就是数据减去噪声。<bookmark mark='b'/>可是这些直线会相交，而一个流不可以：在交点处，一个粒子需要两个速度。"
        "挽救它的是这个定理：时刻tau的密度，是对所有配对的平均，<bookmark mark='c'/>每一对都以自己的速度运动，"
        "<bookmark mark='d'/>所以它满足连续性方程，所用的是每一点上的平均速度：在一条直线经过x的条件下，数据减噪声的期望。"
        "<bookmark mark='e'/>而对配对的速度做回归，学到的恰好就是这个平均，和去噪分数匹配用的是同一个技巧。",

    'f"On our letters this average velocity is known exactly.':
        "在我们的字母上，这个平均速度是精确已知的。这是它在4个时刻的样子：一开始，一切都奔向中间；到后来，每个点都奔向最近的笔画。"
        "<bookmark mark='a'/>从噪声出发跟着它走，再把这些粒子和同一时刻随机配对的直线插值相比。{verdict}<bookmark mark='b'/>"
        "但看看这些路径：它们是弯的，直度只有{st:.2f}。<bookmark mark='c'/>再看代价：{cost_note}它的动能是{act:.2f}，远高于它的代价："
        "路径是弯的，速度也不均匀。流匹配不是最优传输；它是一个好的开始。",

    'f"the flow\'s own map moves points {cf:.3f} on average, close':
        '这个流自己的映射，平均把点移动{cf:.3f}，接近最优的{co:.3f}，远低于随机配对的{ci:.2f}。',

    'f"the flow\'s map moves points {cf:.3f} on average, between':
        '这个流的映射，平均把点移动{cf:.3f}，介于最优的{co:.3f}和随机配对的{ci:.2f}之间。',

    'At every time we checked, they are as close to it as fresh samples are':
        '在我们检查的每一个时刻，它们都和新样本一样接近它：定理成立。',

    'At every time we checked, they are close to it, nearly as close':
        '在我们检查的每一个时刻，它们都很接近它，几乎和新样本一样接近。',

    '"Albergo and Vanden-Eijnden\'s framing makes the family clear':
        "阿尔贝戈和范登-艾因登的框架，让这一族方法看得很清楚：随机插值用任意两条系数曲线混合噪声和数据，还可以再加上噪声。"
        "<bookmark mark='a'/>流匹配的直线是一种选择；扩散模型的四分之一圆，余弦和正弦，是另一种，而同样的平均速度论证，"
        "能把任何一种变成一个流。<bookmark mark='b'/>{verdict}配对之间的直线，并不会造就笔直的流。<bookmark mark='c'/>"
        "弯曲来自对随机配对的平均；要把流拉直，就得改变配对。这是下一章的内容。",

    'f"Measured on our letters, the diffusion path\'s flow':
        '在我们的字母上测量，扩散路径的流反而更直一些：{st:.2f}对{sf:.2f}。',

    'f"Measured on our letters, the straight line\'s flow':
        '在我们的字母上测量，直线的流更直：{sf:.2f}对{st:.2f}。',

    # ------------------------------------------------------------------ Reflow
    'Chapter eleven. Rectified flow and reflow.':
        '第11章。整流流与重流。',

    'f"Here is a flow-matching network learning our letters':
        "这是一个流匹配网络正在学习我们的字母，每个检查点都从同一份噪声出发。<bookmark mark='a'/>损失降得很快，然后停住，远高于0。"
        "<bookmark mark='b'/>它到不了0：随机配对给每个点许多个速度，网络只能学到它们的平均。<bookmark mark='c'/>而且它的路径是弯的："
        "直度{st[0]:.2f}，{len(st)}个随机种子从{st.min():.2f}到{st.max():.2f}。",

    'Xingchao Liu, Chengyue Gong and Qiang Liu called the fix reflow.':
        "刘星超、Chengyue Gong和刘强把这个修正叫作重流。<bookmark mark='a'/>运行训练好的流，把每个噪声点和流实际把它带去的地方配成一对。"
        "这些配对彼此不再相交，于是用它们训练第二个流：那个把路径弄弯的平均，已经没有东西可平均了。<bookmark mark='b'/>"
        "他们证明，对任何凸的代价，新的配对的运输代价都不会更高，而且重复下去，路径会越来越直。<bookmark mark='c'/>"
        "在我们的字母上，做一次，再做两次。",

    'f"Measured, at the same budget for every model':
        "测量结果，每个模型的预算相同，各3个随机种子：用给定步数的欧拉法之后，与数据的距离。<bookmark mark='a'/>普通的流匹配需要很多步："
        "只走一步时，它的样本离数据{fm1:.3f}，而噪声本身是{noise:.2f}。<bookmark mark='b'/>{rf_note}最好的单步结果属于{KS[best1]}，"
        "距离{one[best1].mean():.3f}，{sep_note}<bookmark mark='c'/>{ot_vs}<bookmark mark='d'/>直度说明了原因：在一条直的路径上，"
        "一个欧拉步就是精确的。",

    "f'Pairing each batch optimally, as Alexander Tong":
        '像亚历山大·童和同事、阿拉姆-亚历山大·普拉迪安和同事在2023年提出的那样，在每个批次里做最优配对，只训练一次就走完了大部分路：'
        '一步{one[\'ot\'].mean():.3f}。',

    "f'Pairing each batch optimally, the 2023 proposal":
        '在每个批次里做最优配对，也就是童和普拉迪安等人2023年的提议，一步能达到{one[\'ot\'].mean():.3f}。',

    'After one reflow, one step is nearly as good as a hundred;':
        '重流一次之后，一步就几乎和100步一样好；',

    "f'After one reflow, one step lands {r1:.3f}":
        '重流一次之后，一步落在离数据{r1:.3f}的地方，而100步是{r100:.3f}；',

    'every seed of it ahead of every seed of the others.':
        '它的每个随机种子都胜过其他方法的每个随机种子。',

    'Here is what one step looks like on our letters, from each of the four.':
        "这是在我们的字母上，四种方法各走一步的样子。<bookmark mark='a'/>实际应用中：2023年的InstaFlow把重流和蒸馏结合起来，"
        "让Stable Diffusion一步就能出图。<bookmark mark='b'/>2024年的Stable Diffusion 3和FLUX.1，都是作为整流流训练的，"
        "也就是噪声和数据之间的直线，至于它们的架构，那是第22部分的故事。",

    # ------------------------------------------------------------------ Distill
    'Chapter twelve. Distillation.':
        '第12章。蒸馏。',

    'f"Solvers can only do so much':
        "求解器能做的有限：弯的路径就是需要步数。蒸馏改变的则是网络本身。<bookmark mark='a'/>一个慢的老师得出的结果，"
        "成为一个快的学生要命中的目标。<bookmark mark='b'/>蒂姆·萨利曼斯和乔纳森·何在2022年提出的渐进蒸馏：学生学着把老师的两步并成一步；"
        "然后它自己成为老师，步数再减半。他们从数千步一直减到4步，在CIFAR-10上FID为3.0。<bookmark mark='c'/>我们的版本从我们的"
        "流匹配老师的{rounds[0]}步开始，减半{len(rounds) - 1}次，每一轮训练{per:,}步。{verdict}",

    'f"After {nh} halvings the one-step student lands {s1:.3f} from the data, against the teacher\'s {t64:.3f} with {n0} steps."':
        '减半{nh}次之后，一步的学生落在离数据{s1:.3f}的地方，而老师用{n0}步是{t64:.3f}。',

    'f"After {nh} halvings the one-step student lands {s1:.3f} from the data, against the teacher\'s {t64:.3f} with {n0} steps: each':
        '减半{nh}次之后，一步的学生落在离数据{s1:.3f}的地方，而老师用{n0}步是{t64:.3f}：每减半一次，就损失一点。',

    'f"Consistency models, from Yang Song':
        "一致性模型，由宋飏、普拉富拉·达里瓦尔、陈马克和伊利亚·苏茨克维在2023年提出，省掉了一轮一轮的减半。<bookmark mark='a'/>"
        "教一个网络，把ODE路径上的每一个点，直接送到这条路径的终点。这样，任何一个点，包括纯噪声，离一个样本都只有一跳。"
        "<bookmark mark='b'/>把边界条件做进去：在数据那一端，这一跳什么都不用做。<bookmark mark='c'/>再训练自洽性：一个点的跳跃，"
        "必须和沿着老师的路径再走一步之后的跳跃一致，而那个目标是固定不动的。<bookmark mark='d'/>我们的版本，从同一个老师蒸馏出来，"
        "训练中从同一份噪声跳一次：最后离数据{sw_s}，是{len(sw)}个随机种子的平均。<bookmark mark='e'/>2024年，路橙和宋飏让连续时间的"
        "版本在大规模下稳定下来：两步，在512像素的ImageNet上FID为1.88。",

    'f"A third way matches distributions rather than paths.':
        "第三种方法匹配的是分布，而不是路径。Tianwei Yin和同事的分布匹配蒸馏，训练一个一步的生成器，让它的样本在被模糊到每一个噪声水平时，"
        "都和老师的样本看起来一样。<bookmark mark='a'/>那个KL散度的梯度，沿着每个样本求出来，是两个分数函数之差："
        "生成器自己分布的分数函数，减去真实分布的。<bookmark mark='b'/>真实的分数函数就是老师。假的那个，来自第二个扩散模型，"
        "它一直在生成器最新的样本上训练。<bookmark mark='c'/>我们的版本：生成器一开始就是老师那模糊的一步，然后被一个样本一个样本地"
        "推到字母上：最后离数据{sw.mean():.3f}，{len(sw)}个随机种子。<bookmark mark='d'/>大规模时，一步就在小尺寸的ImageNet图像上"
        "达到2.62的FID；再加上GAN损失，DMD2达到了1.28。",

    'f"Side by side, one step from the same noise.':
        "并排放在一起，都从同一份噪声出发走一步。老师自己的一步是一片模糊，离数据{vals['t1'].mean():.3f}。<bookmark mark='a'/>"
        "{verdict}<bookmark mark='b'/>预算各不相同，实际中也是这样，而在图像上，排名取决于规模和细心程度。如今许多最快的图像模型"
        "都是蒸馏出来的；比如FLUX.1最快的版本，用的是一种对抗形式的蒸馏，1到4步就能出图。它们都需要一个老师。"
        "一个模型能不能从零开始就一步生成？",

    'f"The best student here is {spoken[best]}, at {vals[best].mean():.3f}, within':
        '这里最好的学生是{spoken[best]}，距离{vals[best].mean():.3f}，和老师的{n0}步相差不到{pc:.0f}%。',

    'f"The best student here is {spoken[best]}, at {vals[best].mean():.3f}, still':
        '这里最好的学生是{spoken[best]}，距离{vals[best].mean():.3f}，仍然是老师用{n0}步时距离的{gap:.1f}倍。',

    # ------------------------------------------------------------------ OneStep
    'Chapter thirteen. One step from scratch.':
        '第13章。从零开始的一步生成。',

    'In 2025 Zhengyang Geng, Kaiming He and colleagues':
        "2025年，耿正阳、何恺明和同事训练出了一个完全不需要老师的一步模型。<bookmark mark='a'/>这是在我们的流模型下，一个点的路径："
        "它是弯的。流匹配学的是v，也就是每一刻的速度，所以它不得不迈很多小步。<bookmark mark='b'/>MeanFlow学的则是u："
        "两个时刻s和t之间的平均速度，就像整段旅程的平均速度，而不是速度表的读数。<bookmark mark='c'/>有了它，从s到t一跳，"
        "就能落在路径上，不管路径弯得多厉害。<bookmark mark='d'/>要精确得到u，就得沿着路径把速度积分出来：这正是我们想避免的慢功夫。"
        "诀窍是：把t减s乘以u，写成z t减z s，再对s求导。得出一个恒等式：平均速度，等于此刻的速度，加上t减s，乘以起点沿路径移动时，"
        "平均速度变化得有多快。<bookmark mark='e'/>这个导数只需要一次雅可比-向量积，大约相当于多运行一次网络。<bookmark mark='f'/>"
        "所以网络被训练去匹配右边那一项，并把它固定住：没有积分，也没有老师。在256像素的ImageNet上，它一步就达到了3.43的FID。",

    'Here is ours learning: one jump from the same noise':
        "这是我们的版本在学习：训练中的各个检查点，都从同一份噪声跳一次。<bookmark mark='a'/>早一年，凯文·弗兰斯和同事的捷径模型"
        "走的是另一条路：告诉网络这一跳有多大，并训练它，让一次大小为2d的跳跃，等于两次大小为d的跳跃，从大小为0时的普通流匹配开始。"
        "<bookmark mark='b'/>看它们俩都学会落在字母上。",

    'f"Here is every one-step model of this part':
        "这是本部分所有的一步模型，都从同一份噪声出发，每个网络的训练步数大致相同，各{len(rows[0][3])}个随机种子。<bookmark mark='a'/>"
        "最好的单步结果属于{best_name}，距离{best[3].mean():.3f}，{sep_note}<bookmark mark='b'/>在没有老师的模型里，最好的是"
        "{bs_name}，距离{bs[3].mean():.3f}。<bookmark mark='c'/>普通流匹配的一步，距离{rows[0][3].mean():.3f}，是每种方法的起点，那片模糊。",

    "f'and every one of its seeds beats":
        '而且它的每个随机种子都胜过亚军{second_name}的每个随机种子。',

    'f"though its seeds overlap with the runner-up\'s':
        '不过它的随机种子和亚军{second_name}的互相重叠。',

    # ------------------------------------------------------------------ Guidance
    'Chapter fourteen. Guidance.':
        '第14章。引导。',

    'So far the model draws whatever it likes.':
        "到目前为止，模型想画什么就画什么。要让它画某样东西，就告诉它你要什么：一段图片说明，或者在这里，是哪个字母。"
        "<bookmark mark='a'/>我们在A和I两个字母上训练了一个流模型，告诉它每个样本来自哪个字母，只是每5次里有1次，什么也不告诉它。"
        "<bookmark mark='b'/>一个网络同时学会了两样东西：要求它画的那个字母，以及一般意义上的字母。<bookmark mark='c'/>"
        "这是它在学习的样子，每个检查点都要它画一个A。",

    "The first way to ask came from Bayes' rule.":
        "第一种提要求的方法来自贝叶斯公式。<bookmark mark='a'/>取对数再求梯度，符合一个标签的图像的分数函数，等于普通的分数函数，"
        "加上一个分类器对数概率的梯度：证据p of y不依赖于x，所以消失了。<bookmark mark='b'/>把分类器的推力乘以一个大于1的权重w，"
        "就是从一个锐化的版本里采样，数据被重新加权，偏向分类器最有把握的那些。<bookmark mark='c'/>普拉富拉·达里瓦尔和亚历克斯·尼科尔"
        "在2021年这样做了，用的是一个在带噪声图像上训练的分类器，在ImageNet上击败了GAN。",

    'Classifier guidance needs a second network.':
        "分类器引导需要第二个网络。2022年，乔纳森·何和蒂姆·萨利曼斯注意到，被告知标签的模型和什么都没被告知的模型里，"
        "已经藏着一个分类器：<bookmark mark='a'/>给定x时y的对数概率的梯度，就是两者之差。<bookmark mark='b'/>所以从无条件的方向出发，"
        "沿着这个差往前推，推向条件的方向，再越过它，推多远由权重w决定。<bookmark mark='c'/>一个网络，每步两次调用，不需要分类器。"
        "这就是无分类器引导，它成了文生图模型遵循提示词的标准做法。",

    'f"Ask for an A, from the same starting noise, at three weights.':
        "从同一份起始噪声出发，用三个权重要求它画一个A。<bookmark mark='a'/>w等于0时，要求被忽略了：{100 * on[0.0]:.0f}%的样本落在A上。"
        "<bookmark mark='b'/>等于1时，就是普通的条件模型：{100 * on[1.0]:.0f}%。<bookmark mark='c'/>到4时，你是故意推过头："
        "{100 * on[4.0]:.0f}%，样本挤向最像A的那些笔画，散布从{sp[1.0]:.2f}缩小到{sp[4.0]:.2f}。<bookmark mark='d'/>"
        "在整个扫描中，用{len(np.asarray(g['cfg_prec']))}个随机种子：精确率，也就是看起来像真实A的样本所占的比例，在w等于{ws[jr]:g}时最高。"
        "{drop_note}",

    "f'Recall, how much of the real A the samples cover":
        '召回率，也就是样本覆盖了多少真实的A，到w等于{r_drop:g}时减半：更忠实，但变化更少。',


    '"Guidance trades variety for fidelity.':
        "引导是用多样性换忠实度。把每个权重画在一个平面上：横轴是召回率，纵轴是精确率。<bookmark mark='a'/>{cls_note}"
        "<bookmark mark='b'/>2024年，泰罗·卡拉斯和同事问：为什么非得远离无条件模型？它的毛病在于它更差：那就改用同一个条件模型的"
        "一个更小、训练得更少的版本来引导。这样的推力纠正的是模型自己的错误，而不会把它拖向另一个分布。他们在ImageNet上创下纪录："
        "64像素时FID为1.01，512像素时为1.25。<bookmark mark='c'/>我们的弱模型更窄，训练时间只有八分之一。{verdict}",

    'Classifier-free guidance and classifier guidance trace similar curves.':
        '无分类器引导和分类器引导画出的曲线很相似。',

    'Classifier-free guidance reaches a better balance':
        '无分类器引导达到的平衡，比用我们这个小的带噪声分类器的分类器引导更好。',

    'Classifier guidance, with our small noisy classifier, reaches a better balance':
        '用我们这个小的带噪声分类器，分类器引导达到的平衡，比无分类器引导更好。',

    'f"On our letters the best balance of fidelity and variety is autoguidance':
        '在我们的字母上，忠实度和多样性之间最好的平衡属于自引导，在w等于{wbest[\'auto\']:g}时。',

    'f"On our letters the best balance of fidelity and variety is {MSPOKEN[best]}':
        '在我们的字母上，忠实度和多样性之间最好的平衡属于{MSPOKEN[best]}，在w等于{wbest[best]:g}时；自引导的最好结果也很接近。',

    # ------------------------------------------------------------------ Pictures
    'Chapter fifteen. From points to pictures.':
        '第15章。从点到图片。',

    'f"Points in a plane were a warm-up.':
        "平面上的点只是热身。一张图片也是一个点：这里是来自许多字体的大写字母，{n}乘{n}像素。<bookmark mark='a'/>每张图片是一串"
        "{n * n}个数，也就是{n * n}维空间里的一个点。<bookmark mark='b'/>模型就是我们在A和I字母上训练的那种流匹配，只是进出的数多了。",

    'Here it is learning: sixteen pictures':
        "这是它在学习的样子：每个检查点，都从同一份噪声画出16张图。<bookmark mark='a'/>一开始，是雪花噪点。<bookmark mark='b'/>"
        "然后，在字母通常出现的地方出现灰色的团块，<bookmark mark='c'/>然后是形状，最后是字母。<bookmark mark='d'/>"
        "这是一张图片诞生的过程：雪花噪点，然后一片模糊，然后一个形状，然后一个字母。",

    'f"A batch of samples: rough, speckled':
        "一批样本：粗糙、有斑点，大多是认得出来的大写字母，风格各异。<bookmark mark='a'/>它们是复制品吗？平均来看，每个样本离它最近的"
        "训练图片{near.mean():.2f}；而一张训练图片离它最近的另一张是{tn:.2f}。所以这些样本{verdict}",

    'further from the training set than the training pictures':
        '离训练集的距离，比训练图片彼此之间的距离还远：它们是新的图片，不是复制品。',

    'about as close to the training set as the training pictures':
        '离训练集的距离，和训练图片彼此之间差不多：有些可能接近复制品。',

    'f"Real images have millions of numbers':
        "真实的图像有数百万个数，给每一个都去噪代价很高。2022年，罗宾·龙巴赫、帕特里克·埃塞尔、比约恩·奥默和同事改在一个压缩的空间里"
        "做扩散：一个自编码器把图片变成一小块潜变量网格，扩散模型在那里工作，再由解码器把结果变回像素，数少了{ratio}倍，"
        "文字则通过交叉注意力来引导。<bookmark mark='a'/>那年8月公开权重之后，它成了Stable Diffusion，和OpenAI的DALL-E 2、"
        "Google的Imagen同一年。<bookmark mark='b'/>接着，威廉·皮布尔斯和谢赛宁把去噪器的卷积换成了Transformer，<bookmark mark='c'/>"
        "到2024年，扩散和流的Transformer已经在生成视频，比如OpenAI的Sora，还有120亿参数的图像模型。<bookmark mark='d'/>"
        "到2025年，Google的Veo 3用潜空间扩散，把视频和它的声音一起生成出来。<bookmark mark='e'/>编码器、Transformer和视频模型，"
        "是下一部分的内容。",

    # ------------------------------------------------------------------ Discrete
    'Chapter sixteen. Diffusion for discrete data.':
        '第16章。离散数据上的扩散。',

    "Text is made of symbols, not numbers":
        "文本是由符号构成的，不是由数构成的，所以高斯噪声用不上。2021年，Google的雅各布·奥斯汀和同事把扩散推广到符号上："
        "<bookmark mark='a'/>每一步按照一个概率矩阵，随机替换一个符号，这些矩阵相乘得到一个闭式解，就像那些高斯分布一样。"
        "<bookmark mark='b'/>有两种选择很重要。把一个字母换成随机的另一个，<bookmark mark='c'/>或者用一个特殊的掩码符号把它涂掉，"
        "而它之后就一直是空白：吸收态噪声。空白赢了。到最后，一切都是空白，反向过程则把空白填上。",

    'With blanks, the bound becomes remarkably simple.':
        "有了空白，这个下界变得出奇地简单。每个字母以概率t成为空白。<bookmark mark='a'/>从时刻t往回走到更早的时刻s，"
        "一个空白要么保持空白，概率是s除以t，要么露出它的字母。<bookmark mark='b'/>模型往回走的一步，只可能在露出哪个字母上有所不同，"
        "所以每一项KL，都是露出的概率乘以猜这个字母的交叉熵。<bookmark mark='c'/>把各步加起来，下界就成了一个积分："
        "t分之1，乘以根据仍然可见的字母猜出每一个空白的交叉熵。2024年，三个团队推导出了这一点。<bookmark mark='d'/>"
        "再换一次变量，从时间换成空白的个数k，t分之1就变成了k分之1：这个下界，是对每一种空白个数，求每个空白的平均损失，再取平均。"
        "<bookmark mark='e'/>这就是一个自回归模型的损失，在字母可能被揭开的每一种顺序上取平均。",

    'f"Check it where everything can be enumerated':
        "在一切都能枚举的地方检验它：由a、b、c组成的{L}个字母的字符串，来自一个马尔可夫链，每个概率都已知。三个模型来预测空白："
        "精确的条件概率，同样的条件概率但向均匀分布模糊了一些，以及一个忽略上下文的模型。<bookmark mark='a'/>T步链的下界，精确计算："
        "只有一步时，精确模型的下界是每个字母{d1:.4f}比特；{Ts[-1]:,}步时是{dT:.4f}，逐渐落到那个积分上，也就是那些虚线。"
        "<bookmark mark='b'/>积分、加权交叉熵，以及对每一种揭开顺序的平均，对每个模型都在小数点后{dp}位上一致。<bookmark mark='c'/>"
        "{tight_note}",

    'And with the exact conditionals, the bound equals the true entropy':
        '而用精确的条件概率时，这个下界等于真实的熵：它是紧的。一个把条件概率学得完美的模型，不会为这个下界付出任何代价。',

    'And with the exact conditionals, the bound is close to the true entropy.':
        '而用精确的条件概率时，这个下界接近真实的熵。',

    'The idea has a lineage.':
        "这个想法有它的谱系。2014年，贝尼尼奥·乌里亚、伊恩·默里和雨果·拉罗谢尔，为一个自回归模型的每一种顺序训练了同一个网络；"
        "<bookmark mark='a'/>2022年，埃米尔·胡格布姆和同事把这类任意顺序的模型和扩散联系了起来。<bookmark mark='b'/>2024年，"
        "Aaron Lou、孟辰霖和斯特凡诺·埃尔蒙为离散数据定义了一种分数函数，也就是概率之比，并获得了ICML的最佳论文奖；<bookmark mark='c'/>"
        "同一年，两个团队，Subham Sahoo的和Jiaxin Shi的，分别表明，普通的掩码扩散，也就是那个加权交叉熵，效果一样好，<bookmark mark='d'/>"
        "而Jingyang Ou和同事则表明，模型甚至不需要知道时间。<bookmark mark='e'/>正是这些，让下一步成为可能：用这种方法大规模训练的语言模型。",

    # ------------------------------------------------------------------ TextLM
    'Chapter seventeen. Diffusion language models.':
        '第17章。扩散语言模型。',

    'In February 2025 Shen Nie, Chongxuan Li and colleagues trained LLaDA':
        "2025年2月，聂燊、李崇轩和同事训练了LLaDA，一个80亿参数的语言模型，完全用掩码扩散训练：2.3万亿个词元，每个训练样本都是"
        "一段被随机涂掉一部分的文字。它和同样规模的LLaMA 3不相上下，还在倒着补全一首诗、也就是根据下一句写出上一句的任务上胜过了"
        "GPT-4o，这是从左往右的模型很难做到的。<bookmark mark='a'/>我们造了一对模型来比较：一个掩码扩散模型和一个自回归模型，"
        "大小完全一样，在小说上训练，初始权重、批次和步数都相同。唯一的区别是注意力掩码和任务。",

    'f"Here they are learning.':
        "这是它们在学习的样子。在保留的文本上，自回归模型精确的每字符比特数，和扩散模型的下界，都在下降。<bookmark mark='a'/>"
        "上面，扩散模型在每个检查点，填补测试段落里被涂掉一半字符的一行；下面，另一个模型自己在写。<bookmark mark='b'/>"
        "到最后，扩散模型猜对了{100 * fr:.0f}%的空白。{gap_note}",

    "f'Its bound ends at {m0:.2f} bits per character; the autoregressive":
        '它的下界最后是每字符{m0:.2f}比特；自回归模型是{a0:.2f}，低{gap:.2f}。',

    'f"Its bound ends at {m0:.2f} bits per character, below':
        '它的下界最后是每字符{m0:.2f}比特，低于自回归模型的{a0:.2f}。',

    'f"And here is ours writing {T} characters':
        "这是我们的模型在写{T}个字符，从全是空白开始，分{len(frames) - 1}轮。<bookmark mark='a'/>每一轮，它猜出每一个空白，"
        "保留它最有把握的那些猜测，其余的仍然留空，这是LLaDA的规则。<bookmark mark='b'/>词语哪里先有把握，就先出现在哪里，"
        "其余的再围绕着它们填上：先一下子全部写出，再慢慢修改，而不是从左往右写。",

    'f"At equal size, data and steps':
        "在同样的规模、数据和步数下，在{T}个字符的保留文本块上，{winner}：下界是每字符{np.mean(mv):.3f}比特，对比{np.mean(av):.3f}。"
        "<bookmark mark='a'/>对这个下界的三种不同估计，按推导它们的期望是相等的，{agree_note}。<bookmark mark='b'/>{l2r_note}"
        "<bookmark mark='c'/>这个差距并不是故事的结局：2025年，米希尔·普拉布德赛和同事发现，当数据稀缺、必须重复很多个轮次时，"
        "扩散模型在自回归模型过拟合之后，仍然在进步。",

    "f'Read strictly left to right, the diffusion model scores {l2r:.3f}, better":
        '严格地从左往右读，扩散模型的得分是{l2r:.3f}，比它自己的下界还好：大多数揭开顺序都比按顺序读更难，而下界要为所有顺序付账。',

    "f'Read strictly left to right, the diffusion model scores {l2r:.3f}, no better":
        '严格地从左往右读，扩散模型的得分是{l2r:.3f}，并不比它的下界好：它从来没有被训练去偏爱这个顺序。',

    'f"On the scoreboard\'s passage, in blocks of':
        "在记分牌的测试段落上，按{int(t['T'])}个字符一块：掩码扩散模型的下界是每字符{m:.2f}比特，误差大约{se:.2f}，"
        "自回归的孪生模型是{a:.2f}。<bookmark mark='a'/>第13部分的Transformer，上下文是它们的{ratio}倍，得分{tf['bits']:.2f}。"
        "下界是一个上限：扩散模型真正的编码长度只会更低。",

    'f"Writing {T} characters one round per character':
        "每轮写一个字符，写{T}个字符就要{T}次网络调用，和自回归模型一样。扩散的承诺是轮数更少，每轮写好几个字符。这在质量上要付出多少代价？"
        "用另一个随机种子的自回归模型来评判每个样本：越低，读起来越像那些小说；真实的文本得分{judge_real:.2f}。<bookmark mark='a'/>"
        "用{T}轮时是{c64['judge']:.2f}；用8轮时是{c8['judge']:.2f}；一次全部写出时是{c1['judge']:.2f}：一下子独立地猜许多个字符，"
        "会让它们彼此对不上。<bookmark mark='b'/>{order_note}<bookmark mark='c'/>{blk_note}",

    "f'Writing in four blocks, left to right":
        '分成4块从左往右写，总共16轮，得分{b16[\'judge\']:.2f}，而整串一次性写是{w16[\'judge\']:.2f}。',

    "f'Revealing the surest guesses first reads better":
        '先揭开最有把握的猜测，读起来比随机揭开更好，{c64[\'judge\']:.2f}比特对{r64[\'judge\']:.2f}比特，尽管下界描述的是随机揭开。',

    "f'Revealing at random reads as well as the surest-first rule":
        '随机揭开读起来和最有把握优先的规则一样好，{r64[\'judge\']:.2f}对{c64[\'judge\']:.2f}。',

    'Fixed-length writing has a cost':
        "定长的写法有代价：什么都没法缓存，长度也得事先定好。玛丽安娜·阿里奥拉和同事的块扩散取了个折中：块与块之间从左往右，"
        "像自回归模型，每块之内则用扩散。<bookmark mark='a'/>2025年，Inception Labs推出了Mercury，号称第一个商用的扩散语言模型，"
        "在一块GPU上每秒能写1000多个词元；<bookmark mark='b'/>Google的Gemini Diffusion报告的速度接近每秒1500个，代码能力大约相当于"
        "一个小号的Gemini；<bookmark mark='c'/>Fast-dLLM给开放的模型加上了缓存和有把握时的并行解码，最多快了27倍；<bookmark mark='d'/>"
        "LLaDA 2.0通过改造一个自回归模型，达到了1000亿参数。<bookmark mark='e'/>2026年6月，Google发布了开放权重的DiffusionGemma："
        "每块256个词元，在一块GPU上每秒超过1000个词元，而且按Google自己的说法，质量低于标准的Gemma 4。这个交换是用一点质量换速度，"
        "也正是我们那两个小模型测出来的。",

    # ------------------------------------------------------------------ Outro
    "Let's take stock. A diffusion model destroys data slowly":
        "我们来盘点一下。扩散模型用噪声慢慢地摧毁数据，再学会把它复原。训练它的那个下界，是一串猜噪声误差的和，"
        "而由特威迪公式，最好的噪声猜测就是分数函数；去噪分数匹配用普通的回归把它学出来。时间可以用随机方程或确定性方程倒着运行；"
        "DDPM和DDIM把它们离散化，EDM和DPM-Solver用10到30步把它们解出来。流匹配学的是沿直线的速度，重流把路径拉直，"
        "蒸馏或MeanFlow则做到了一步。引导把一个要求变成一股推力。同一套机制能画出图片，而用空白当作噪声，还能写出文字。",

    'This machinery comes back.':
        "这套机制还会回来。下一次，它要面对真实的图像和视频，在压缩的潜空间里进行，并用Transformer做去噪器。"
        "语音和声音的生成器也用它，那是第23部分；把去噪当作学习特征的一种方法，会在第24部分回来；扩散能构建分子和蛋白质结构，"
        "那是第25部分；世界模型用它来想象下一帧画面，那是第29部分；而让它变快，是第19部分故事的一部分。",

    'Here are six problems, from the forward process':
        '这里有6道习题，从前向过程的闭式解，到掩码扩散的下界。请在这里暂停，动手做一做；完整的解答在本部分的讲义里。',

    'Next time: images, video and 3D.':
        "下一次：图像、视频与3D。一张图片被切成一个个图像块，这些图像块变成词元，<bookmark mark='a'/>这样，第13部分的Transformer"
        "就能看图片，并给它们去噪。",

    "To go deeper, Simon Prince's Understanding Deep Learning":
        "想深入下去，西蒙·普林斯的《理解深度学习》把扩散讲得很清楚，而且免费；桑德·迪勒曼关于扩散的那些博客文章，也是绝佳的参考读物。"
        "感谢观看，我们第22部分再见。",
})

ZH.update({  # spliced sentences, also listed by --todo
    'on the whole, if not at every checkpoint': '总体上如此，虽然不是每个检查点都这样',
    'come close, though not within their error bars': '很接近，但不在误差范围之内',
    'the autoregressive model wins in both seeds': '两个随机种子里都是自回归模型赢',
})

PHRASES.update({
    # spliced-in English values
    'Recall stays high across the sweep.': '在整个扫描中，召回率都保持在高位。',
    'on the whole, if not at every checkpoint': '总体上如此，虽然不是每个检查点都这样',
    'at every checkpoint': '每个检查点都是如此',
    'our cosine schedule': '我们的余弦调度',
    'the linear-beta schedule': '线性贝塔调度',
    'the straight-line schedule': '直线调度',
    "EDM's log-normal": 'EDM的对数正态分布',
    'uniform in time': '时间上均匀',
    "DDPM's own steps": 'DDPM自己的步',
    'uniform in log signal-to-noise': '对数信噪比上均匀',
    "EDM's spacing": 'EDM的间隔方式',
    'predicting the noise': '预测噪声',
    'predicting the clean point': '预测干净的点',
    "EDM's mixture": 'EDM的混合目标',
    'plain Euler in time': '时间上的普通欧拉法',
    'DDIM': 'DDIM',
    'Heun': '休恩法',
    'DPM-Solver-2': 'DPM-Solver-2',
    'DPM-Solver plus plus': 'DPM-Solver++',
    'plain flow matching': '普通的流匹配',
    'minibatch optimal-transport pairing': '小批量最优传输配对',
    'one reflow': '一次重流',
    'two reflows': '两次重流',
    'though the seeds overlap.': '不过随机种子之间互相重叠。',
    'progressive distillation': '渐进蒸馏',
    'consistency distillation': '一致性蒸馏',
    'distribution matching': '分布匹配',
    'minibatch optimal-transport flow matching': '小批量最优传输流匹配',
    'MeanFlow': 'MeanFlow',
    'the shortcut model': '捷径模型',
    'classifier-free guidance': '无分类器引导',
    'classifier guidance': '分类器引导',
    'autoguidance': '自引导',
    'the autoregressive model wins in both seeds': '两个随机种子里都是自回归模型赢',
    'the two overlap across seeds': '两者在不同随机种子之间互相重叠',
    'agree within their error bars': '在误差范围内一致',
    'come close, though not within their error bars': '很接近，但不在误差范围之内',
})
