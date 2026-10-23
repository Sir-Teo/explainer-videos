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
        "为什么猜噪声就是在学分数函数；让时间倒流，用随机方程或确定性方程，以及求解它们的采样器；各种设计选择，从噪声调度到EDM和"
        "DPM-Solver；流匹配与最优传输；怎样从50步走到1步；怎样要求它画出特定的东西；还有用于文本的扩散，我们自己的一个语言模型"
        "也会登上记分牌。这里的每一个模型，都是在这台电脑上训练的。",

    # ------------------------------------------------------------------ Forward
    'Chapter one. Destroying data slowly.':
        '第1章。慢慢地摧毁数据。',

    'f"Annealed Langevin, at the end of Part 20':
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
        "{worst:.3f}，<bookmark mark='c'/>{verdict}跑完全部1000步后，阿尔法拔是{f['abar_T']:.1e}：一个点剩下的部分，"
        "只有它原来的{math.sqrt(f['abar_T']):.4f}。",

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
        "从同一份噪声里画出一些点。<bookmark mark='a'/>还没训练时，它把这些点甩得到处都是。<bookmark mark='b'/>{early}"
        "<bookmark mark='c'/>剩下的都是精修：损失几乎不动，但笔画越来越清晰，与数据的距离从{sw[k1]:.2f}降到{sw[-1]:.2f}，{trend}。"
        "训练的每一步，只要求它猜出一个模糊的点里的噪声；字母就从数百万次这样的猜测中浮现出来。",

    "f'Within {checks[k1]} steps it has the rough shape, and the loss":
        '不到{checks[k1]}步，它就有了大致的形状，损失也已经完成了整个降幅的{100 * min(drop, 1):.0f}%。',

    "f'Within {checks[k1]} steps it has the rough shape, though":
        '不到{checks[k1]}步，它就有了大致的形状，不过损失还在下降。',

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
        'ODE一路下来，都和真实边缘分布的新样本一样接近它；SDE用了1000个随机步，在最后稍有偏离，{end_s:.3f}，对比ODE的{end_o:.3f}：'
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
        "这一步恰好就是概率流ODE的一个欧拉步，所用的坐标是x除以阿尔法，以及西格玛除以阿尔法。<bookmark mark='c'/>宋佳铭、孟晨霖和埃尔蒙"
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
        "用4种噪声水平的间隔方式。<bookmark mark='a'/>{verdict}<bookmark mark='b'/>{edm_note}",

    "On image models EDM's spacing has become a standard; on our letters":
        '在图像模型上，EDM的间隔方式已经成了标准；在我们的字母上，它并不总是最好的。间隔方式是采样器的一个设置，和别的设置一样需要调。',

    "On image models EDM's spacing has become a standard, and on our letters":
        '在图像模型上，EDM的间隔方式已经成了标准，在我们的字母上，它也是最好的。',

    "f'One spacing wins for all three":
        '有一种间隔方式对三者都最好：{sp_ddim}。',

    "f'No spacing wins for every solver":
        '没有哪种间隔方式对每个求解器都最好：对DDIM来说，最好的是{sp_ddim}，对休恩法是{sp_heun}，对DPM-Solver++则是{sp_dpm}。',

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

    'f"Here are three of them after about {budget} evaluations':
        "这是其中三种在大约{budget}次调用之后的结果，旁边是精确解：DDIM的点仍然向内模糊，二阶方法的点则很清晰。"
        "<bookmark mark='a'/>{verdict}而网络自己的误差设定了一个下限：精确求解时，它的ODE落在离数据{net_ref:.3f}的地方，"
        "而字母的一份新样本是{fl:.3f}。<bookmark mark='b'/>那么，10到30次调用，再配上一个懂得这个方程的求解器。比这更少，"
        "就需要另一种想法：第12章。",

    'With our trained network in place of the exact denoiser, the ranking is the same,':
        '用我们训练好的网络代替精确的去噪器，排名不变，',

    'With our trained network in place of the exact denoiser, the ranking shifts,':
        '用我们训练好的网络代替精确的去噪器，排名有所变化，',
})
