"""Chinese narration for quant13: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).
Terms follow videos/quant/QUANT_ZH_GUIDE.md."""

TITLE = '量化金融，从零搭建 · 第13部分：随机波动率与跳跃'

CHAPTERS = {
    'Hook': '第二条河',
    'Moves': '1. 波动率为什么必须变动',
    'Mixing': '2. 随机波动率产生微笑',
    'Heston': '3. 赫斯顿模型之一：特征函数',
    'HestonFit': '4. 赫斯顿模型之二：每个参数做什么',
    'Simulate': '5. 赫斯顿模型之三：老老实实地模拟',
    'SABR': '6. SABR之一：哈根公式与骨架',
    'SABRFix': '7. SABR之二：负密度与修正',
    'Jumps': '8. 跳跃：默顿、寇与贝茨',
    'Levy': '9. 莱维模型与时间变换',
    'Skew': '10. 跨期限的偏斜',
    'SLV': '11. 随机局部波动率：粒子方法',
    'MixFrac': '12. 混合比例',
    'Bergomi': '13. 贝尔戈米：以远期方差为状态',
    'Forward': '14. 远期微笑与棘轮期权',
    'Puzzle': '15. SPX/VIX难题：在比特币上测量',
    'Calibration': '16. 校准：山谷、可识别性与不稳定',
    'Industry': '17. 业界：谁在建这些模型，交易台如何评判它们',
    'Frontier': '18. 前沿：2023–2026',
    'Research': '写给研究者：矩爆炸与微笑的两翼',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {
    # ------------------------------------------------------------------ Hook
    "Part thirteen. Stochastic volatility and jumps.":
        "第13部分。随机波动率与跳跃。第12部分把波动率曲面当作一张静止的照片来读。这一部分要问：是什么在推动它变化。",

    "Here is Bitcoin's thirty-day implied volatility, every day for four and a half years.":
        "这是比特币的三十天隐含波动率，四年半里的每一天。它不是常数。它是一条自己的河，流淌在价格旁边。<bookmark mark='a'/>"
        "价格断裂时它就泛滥：Terra与Luna的崩溃，FTX的倒闭，还有2024年8月那一天，一笔拥挤的日元交易在所有市场上同时平仓。"
        "而在两次洪水之间，它又慢慢退去，回到一个它似乎记得的水平。",

    'f"This part gives volatility its own state, and adds jumps and random clocks. He':
        "本部分让波动率拥有自己的状态，并加入跳跃和随机时钟。问题是：把五个模型拟合或投影到同一批汇总的比特币标记价格。它们的普通期权误差不同，并非对每个期权都给出相同价格。<bookmark mark='p'/> 即使普通期权价格完全一致，不同日期之间的联合分布仍未被确定。<bookmark mark='a'/> 这份按月收益封顶的棘轮期权，在这些模型间相差{100 * (v.max() - v.min()) / v.mean():.0f}%。这里的价差同时包含动态假设、普通期权拟合差异和数值误差。下面会逐一分清。",

    "The history. 1973: Black, Scholes and Merton's constant-volatility benchmark; 19":
        "回顾历史。1973年，布莱克、斯科尔斯和默顿给出常波动率基准；1976年，默顿加入跳跃。<bookmark mark='m2'/> 1987年10月的股灾使指数下跌侧偏斜格外显著。<bookmark mark='m3'/> 赫尔与怀特、斯科特、威金斯研究随机波动率；<bookmark mark='m4'/> 斯坦与斯坦采用奥恩斯坦–乌伦贝克因子；<bookmark mark='m5'/> 赫斯顿得到仿射特征函数。<bookmark mark='m6'/> 杜皮尔、德曼–卡尼和鲁宾斯坦发展了局部波动率与隐含树。<bookmark mark='m7'/> 贝茨结合波动率与跳跃；<bookmark mark='m8'/> 马丹、卡尔和张给方差伽马定价。<bookmark mark='m9'/> 随后是SABR、寇与CGMY；<bookmark mark='m10'/> 卡尔–吴的时钟以及Cboe的VIX期货；<bookmark mark='m11'/> 贝尔戈米的方差曲线；<bookmark mark='m12'/> VIX期权；<bookmark mark='m13'/> 安德森的模拟与盖瑟罗的联合微笑问题；<bookmark mark='m14'/> 居永与亨利–拉博代尔的粒子方法；<bookmark mark='m15'/> 居永的非参数联合校准构造；<bookmark mark='m16'/> 以及比特币的Terra和FTX事件。",

    "The plan. Why volatility must move, and a proof":
        "本部分的安排。波动率为什么必须变动，以及随机性产生微笑的证明。赫斯顿模型：推导、拟合与模拟。SABR及其修复。"
        "跳跃与莱维时钟，按它们的偏斜分类。随机局部波动率及其旋钮。方差曲线、远期微笑、标普–VIX难题。然后是校准、业界与前沿。",

    "In the House, the volatility desk gets its calibrator.":
        "在我们的公司里，波动率交易台有了自己的校准器。<bookmark mark='a'/>从现在起，交易台用来定价的每个模型都由它拟合，"
        "每个奇异期权都附带一份说明：各模型之间分歧有多大。",

    # ------------------------------------------------------------------ Moves
    "Chapter one. Why volatility must move.": "第1章。波动率为什么必须变动。",

    'f"Black, Scholes and Merton assumed one volatility':
        "布莱克、斯科尔斯和默顿假设只有一个波动率，在期权的整个生命期内固定不变。这是比特币的。绿色的，是它在每个过去三十天里实现的波动率。"
        "<bookmark mark='a'/>它从每年{100 * f['rv_min']:.0f}%到{100 * f['rv_max']:.0f}%。<bookmark mark='b'/>"
        "橙色的是DVOL，市场的三十天隐含波动率。它也在动：像价格那样衡量，它的波动率大约是每年{100 * f['volvol']:.0f}%。"
        "波动率是流淌在价格旁边的第二条随机的河，而期权同时押注这两条河。",

    'f"The scatter pairs each day\'s Bitcoin return with its log-DVOL change. Its line':
        "散点把每日比特币收益与当日对数DVOL变化配对，直线是描述性回归。比特币跌幅超过5%的日子，对数DVOL平均变化乘以100为{f['dvol_change_down5']:.0f}。<bookmark mark='a'/> 2022年的相关系数为{by['2022']:+.2f}。<bookmark mark='b'/> 2023年为{by['2023']:+.2f}；符号变化本身不能识别原因。全部{f['n']}个配对交易日的相关系数为{f['leverage_corr']:+.2f}，所以同期线性拟合解释约{100 * f['leverage_corr'] ** 2:.0f}%的对数DVOL变化方差。剩余部分并不能证明存在独立的波动率噪声。这也不是对GARCH的检验，因为GARCH的状态取决于完整的收益历史。随机波动率模型把另一个冲击作为建模选择加入。",

    'f"Two descriptive patterns. Return autocorrelations are small against this point':
        "再看两个描述性特征。收益自相关相对于这条逐点噪声参考带较小，但这不能证明独立或完全没有记忆。<bookmark mark='a'/> 绝对收益会聚集：一阶自相关为{acf_a[0]:.2f}，较长滞后仍能看到正依赖。<bookmark mark='b'/> 对数DVOL也有持续性。<bookmark mark='c'/> 用今天的对数水平回归明天的水平，日度AR一阶斜率为{vf['ar1_phi']:.3f}。<bookmark mark='d'/> 按类似奥恩斯坦–乌伦贝克模型的解释，半衰期约{hl:.0f}天。拟合的长期对数水平取指数得到{100 * vf['dvol_mean']:.0f}%；这不是DVOL的算术平均值。这些都是样本概括，并非市场不变的定律。",

    'f"On 19 October 1987 the S&P 500 fell from {c[\'close_before\']:.0f} to {c[\'close\'':
        "1987年10月19日，标普500从{c['close_before']:.0f}跌至{c['close']:.0f}，对数收益为{100 * c['ret']:.1f}%。<bookmark mark='a'/> 以前250个交易日的标准差衡量，这是{abs(c['z']):.0f}个标准差。固定波动率的高斯基准给出的单侧概率约为10的负{abs(c['log10p']):.0f}次方。这个数字以刻意严格的基准为条件，并非对现实股灾概率的估计。股灾后，指数下跌侧偏斜格外显著。<bookmark mark='b'/> 暂停：比特币涨10%，隐含波动率必须升还是降？样本中两种关联符号都出现过，因此没有确定答案。接着看随机波动率如何影响价格。",

    # ------------------------------------------------------------------ Mixing
    "Chapter two. Random volatility makes a smile.": "第2章。随机波动率产生微笑。",

    'f"Set Heston\'s correlation to zero. Without variance randomness, the three-month':
        "先把赫斯顿的相关系数设为零。方差没有随机性时，三个月对数收益为高斯分布，隐含波动率微笑平坦。<bookmark mark='a'/> 方差随机时，每个条件高斯分布都有自己的积分方差。四十条细线及其平均值用来展示这种混合；下方微笑来自变换定价，并非这四十条路径。<bookmark mark='b'/> 在这组参数实验里，提高方差的波动率使混合分布更尖，也提高期权价格的两翼。<bookmark mark='p'/> 再翻一倍，平值会怎样？<bookmark mark='c'/> 翼部波动率从{100 * wing['1']:.0f}%升至{100 * wing['2']:.0f}%，平值则从{100 * atm['1']:.1f}%降至{100 * atm['2']:.1f}%。零相关的混合给出对称的隐含波动率微笑。<bookmark mark='d'/> 恢复拟合相关系数，负{abs(m['params'][4]):.2f}。方差冲击与价格冲击现在相关，这个例子向看跌翼倾斜。",

    'Use zero carry and an initial spot of one. At zero correlation, the price noise ':
        "取零持有成本，初始现货为一。零相关时，价格噪声独立于方差路径，因此给定路径的对数收益为高斯分布，方差等于积分方差。<bookmark mark='a'/> 塔式性质对平均方差下的布莱克–斯科尔斯价格取平均，这就是赫尔–怀特恒等式。<bookmark mark='b'/> 对这个方差作二阶泰勒展开，修正项为其方差的一半，乘以价格对方差的二阶导数。<bookmark mark='c'/> 记w为sigma平方，二阶导数为vega乘以d一d二减一，再除以四倍sigma立方。领先修正在平值处为负，在足够远的两翼为正。对波动率求曲率是另一个导数。<bookmark mark='d'/> 非零相关时，把价格冲击分为相关部分和正交部分。<bookmark mark='e'/> 在赫斯顿中，给定方差路径的对数收益仍为高斯：现货由xi T因子平移，剩余方差乘以一减rho平方。这是罗马诺–图齐定价恒等式。",

    'f"The identity suggests a numerical estimator. We use {m[\'N\']:,} simulated varia':
        "这个恒等式启发了数值估计器。我们模拟{m['N']:,}条方差路径，采用九十一步QE和梯形积分方差。普通蒙特卡洛还模拟价格。<bookmark mark='a'/> 条件估计器则对布莱克价格取平均。这里的抽样误差条约窄{ratio:.0f}倍，但误差条不包含离散偏差。平值处，COS基准为{100 * r['cos_iv'][6]:.2f}%，条件估计为{100 * r['cond_iv'][6]:.2f}%。<bookmark mark='b'/> 十三个行权价中，{verdict} 这是数值近似之间的比较。连续模型的条件恒等式是精确的，但模拟路径、积分和变换定价仍有数值误差。",

    "f'Every strike agrees with the exact price within":
        "每个行权价都在{zmax:.1f}个标准误差以内与精确价格一致，所以公式成立。",

    "f'The largest gap is":
        "最大的偏差是{zmax:.1f}个标准误差：模拟的时间步长显现出来了，这提醒我们定理是精确的，方差路径却不是。",

    # ------------------------------------------------------------------ Heston
    "Chapter three. Heston's model, and its characteristic function":
        "第3章。赫斯顿模型，及其特征函数的推导。",

    "Steven Heston's 1993 model":
        "史蒂文·赫斯顿1993年的模型，是写下第二条河、又能给它定价的最简单方式。价格随方差的平方根波动。<bookmark mark='a'/>"
        "方差是第5部分的CIR过程：以速度kappa被拉向theta，被它自己的波动率xi摇晃，相关系数为rho。",

    "Now derive its characteristic function.":
        "现在推导它的特征函数。记x为对数价格，tau为剩余时间，到期时e的i u x次方的期望满足模型的后向方程，这是费曼–卡茨定理。"
        "<bookmark mark='a'/>每个系数都对v是线性的，所以猜一个对v线性的指数：这是达菲、潘和辛格尔顿推广的仿射思想。<bookmark mark='b'/>"
        "代进去。含v的项给出D的里卡蒂方程；<bookmark mark='c'/>其余的项说明C以kappa theta D的速度增长。<bookmark mark='d'/>"
        "里卡蒂方程的右边是一个二次式，根是b加减d再除以xi平方；分离变量，用部分分式，并选择让e的负d tau次方衰减的那个根。"
        "<bookmark mark='e'/>对C积分。这个选择，即“小陷阱”，让对数远离它的分支切割。<bookmark mark='f'/>"
        "结果对今天的方差是指数形式的，一次傅里叶积分就能给任何香草期权定价。",

    'The characteristic function maps frequency to a complex number, which we can dra':
        "特征函数把频率映射到复数，因此可以画成三维曲线。<bookmark mark='a'/> 它从一开始，相位和振幅共同编码分布；但高频衰减慢并不是厚尾的普遍检验。<bookmark mark='b'/> 在这组拟合里，三个月的变换比三十天衰减更快。高斯分布也能说明宽度关系：分布越宽，变换越窄。但不能把这个例子当作普遍的尾部诊断。",

    'f"Now the trap.':
        "现在来看陷阱。赫斯顿的论文用的是另一个根：g倒过来，e的正d T次方。代数上一样，数值上不一样。看一年期时它对数里面的那个数。"
        "<bookmark mark='a'/>半径被压缩了，角度是真实的：在u等于{cu:.2f}处，它穿过负实轴，也就是对数的分支切割。<bookmark mark='b'/>"
        "在那里计算机的对数跳了2πi；阿尔布雷赫尔等人的“小陷阱”形式保持连续。<bookmark mark='c'/>在我们的拟合上，原始形式从u等于"
        "{fw['fit_1']['u']:.2f}起就是错的，一年期平值看涨期权给出{100 * p1['iv_original'][1]:.0f}%的隐含波动率，"
        "而不是{100 * p1['iv_little'][1]:.0f}%。教科书参数能撑到一年；我们剧烈的拟合撑不住。",

    'f"The implementation uses the decaying-root form and a consistent logarithm. <bo':
        "实现采用衰减根形式，并一致处理复对数。<bookmark mark='a'/> 在Fang与Oosterlee的数值基准上，绝对误差约为10的负{-np.floor(np.log10(b['err'])):.0f}次方；比较也揭示了原始公式直接实现对这组拟合的失败。<bookmark mark='b'/> 暂停：非零相关时，给定完整的赫斯顿方差路径，对数收益仍为高斯吗？对非退化模型，答案是是的；第二章给出了平移后的条件均值和剩余方差。零相关的独立情形只是更简单的特例。下面看参数作用。",

    # ------------------------------------------------------------------ HestonFit
    "Chapter four. What each of Heston's parameters does": "第4章。赫斯顿的每个参数做什么，以及拟合。",

    'Five interacting parameters shape this fitted surface. The white points are reco':
        "五个相互影响的参数塑造这张拟合曲面。白点由2025年12月10日零点至中午汇总的期权标记价格重建，以八点为参考，并非同时可成交的报价。每次只改变一个参数，其余保持不变。<bookmark mark='v0'/> 初始方差主要影响短端。<bookmark mark='theta'/> 长期水平影响远期。<bookmark mark='kappa'/> 均值回复改变过渡速度。<bookmark mark='rho'/> 相关系数改变偏斜。<bookmark mark='xi'/> 方差扩散系数同时影响曲率和偏斜。这些敏感度有重叠，校准器必须联合选择参数。",

    'f"Watch it set them.':
        "看它怎么设定。校准器用傅里叶方法给每个报价定价，再让最小二乘优化器找更好的参数；每一次求值都被记录下来。右边是三个起点的损失，"
        "取到目前为止的最好值；左边是三个期限的微笑。<bookmark mark='a'/>从默认起点出发时微笑是平的；优化器先提高波动率的波动率、"
        "倾斜相关系数，再让kappa和xi一起上升，沿着我们将在第16章画出的山谷，到达kappa {r0['x'][1]:.1f}和xi {r0['x'][3]:.1f}。"
        "<bookmark mark='c'/>从{r1['trace']['best'][0]:.0f}和{r2['trace']['best'][0]:.0f}开始的随机起点，最后都停在同一个损失"
        "{r0['rmse']:.3f}。这个损失是价格误差除以vega，是一个快速的替代；隐含波动率误差是{frames[-1]['iv_rmse']:.2f}个点。",

    'f"The direct implied-volatility comparison is vega-weighted. A single Black vola':
        "直接的隐含波动率比较采用vega权重。一个布莱克波动率的误差为{c['fits']['BS']['rmse']:.1f}个点。<bookmark mark='a'/> 赫斯顿误差为{h['rmse']:.1f}个点。<bookmark mark='b'/> 定价测度下，方差半衰期为{365 * np.log(2) / p['kappa']:.0f}天，扩散系数xi为{p['xi']:.2f}。费勒比率为{c['feller']:.2f}；小于一意味着方差可以到达零边界，并不使模型无效。{days[0]}天期限的误差仍为{d3:.1f}个点。这些都是回顾性的拟合诊断。",

    'f"Derive the leading short-maturity ATM skew. The BBF relation uses a harmonic m':
        "推导短期限平值偏斜的领先项。BBF关系沿通往对数行权价k的直线，对局部波动率取调和平均。在平值附近，一阶展开可以写成线性化局部方差的平均。<bookmark mark='a'/> 久恩吉恒等式配合短时间高斯线性化，给出局部方差约为初始方差加rho xi k。<bookmark mark='b'/> 对这条直线取平均，斜率减半。<bookmark mark='c'/> 再开平方，在初始方差为正、期限趋于零时，得到rho xi除以四倍初始方差平方根。<bookmark mark='d'/> 这里的极限为{sl['skew_formula']:.3f}，数值两天值为{sl['skew_2d']:.3f}。这说明本次校准的一项限制，并非对所有扩散模型、所有行权价的定理。<bookmark mark='e'/> 令rho为正，这个平值领先偏斜改变符号。下面看模拟。",

    # ------------------------------------------------------------------ Simulate
    "Chapter five. Feller's condition, and simulating": "第5章。费勒条件，以及老老实实地模拟赫斯顿模型。",

    'f"Compare one week-long variance step, started at zero point zero five. White is':
        "比较从零点零五出发的一周方差步。白色是精确CIR分布；theta为正时，它在零点没有概率原子。<bookmark mark='a'/> 欧拉的高斯候选值有{100 * a['neg']:.0f}%为负。截成零会改变均值：{a['mean_euler']:.3f}，而精确值为{a['mean_exact']:.3f}。<bookmark mark='b'/> QE近似则含有人为的零点原子，这里为{a['zero_qe']:.2f}，以及正值指数分支。总体均值和方差按构造匹配CIR矩，样本均值为{a['mean_qe']:.3f}。这个原子属于数值格式，并不属于正时间CIR分布。<bookmark mark='c'/> 初始方差较高时，QE使用缩放的高斯平方。两条分支都是对转移分布的近似。",

    'f"Feller\'s ratio is {fel:.2f}, below one, so this CIR variance can reach zero an':
        "费勒比率为{fel:.2f}，小于一，因此这条CIR方差可以到达零点，附近密度也很大。这使离散化困难，但并不使赫斯顿模型无效。<bookmark mark='a'/> 在三个初值、三个时间步长下，比较与精确转移分布的输运距离。<bookmark mark='b'/> 九个记录案例中，QE距离都较小，中位改善倍数为{ratio:.0f}。这个数值实验支持这里的比较，并非普遍精度保证，也不是收敛速率证明。",

    "QE, derived. Over one step, the variance's conditional mean and variance are kno":
        "推导QE。一步之内，方差的条件均值和条件方差是精确已知的：第5部分的CIR矩。<bookmark mark='a'/>它们的比值psi衡量相对宽度。<bookmark mark='b'/>psi小时：一个常数乘以平移后的高斯平方。它的均值是a乘以一加b平方，方差是二倍a平方乘以一加二倍b平方；令它们等于m和s平方并求解，就得到这里的b和a。<bookmark mark='c'/>psi大时：以概率p取零，否则取速率为beta的指数分布。均值是一减p除以beta，二阶矩是它的两倍再除以beta；匹配得到p和beta。安德森在1.5处切换，两个分支在那里都有效。<bookmark mark='d'/>对价格，从方差方程解出它的随机积分并代入；只有正交部分需要新的高斯抽样，再用各分支的指数矩修正，在所需矩存在时保证离散价格满足鞅条件；这并不使整个转移分布精确。",

    "In the House: the exact moments, the switch on psi":
        "在公司的代码里：精确矩、按psi切换、两个分支，以及价格步。<bookmark mark='a'/>拿一份三个月平值看涨期权，与精确的傅里叶价格对比，"
        "分别用两步、八步和三十二步。QE一开始就很接近；欧拉格式需要几十步。",

    "Three pointers. Broadie and Kaya":
        "三个延伸。布罗迪和卡亚在2006年精确地模拟了赫斯顿模型：无偏，但慢。<bookmark mark='a'/>崔和郭在2024年用泊松条件化让精确型抽样变快。"
        "<bookmark mark='b'/>安德森和皮特巴格证明，价格的矩可能在有限时间内爆炸，这限制了微笑两翼：与第12部分李氏公式的联系。"
        "下一章：利率和外汇交易台偏爱的模型——SABR。",

    # ------------------------------------------------------------------ SABR
    "Chapter six. SABR: Hagan's formula": "第6章。SABR：哈根公式与骨架。",

    'SABR describes a forward with diffusion coefficient alpha times the forward rais':
        "SABR中，远期价格的扩散系数为alpha乘以远期价格的beta次方；alpha本身服从对数正态动态，系数为nu，相关系数为rho。nu为零时退化成CEV扩散，再令beta为零就是巴舍利耶。beta通常按惯例固定；这个比特币例子取beta为一，其余参数逐期限拟合。<bookmark mark='a'/> 哈根等人推导的是隐含波动率的渐近展开，这里展示beta为一的特例。<bookmark mark='b'/> z除以x之z提供领先的行权价曲率，时间修正也只是近似。这是模型的定价近似，并非其精确分布。",

    'f"For beta one, expand x of z around zero. The ratio is one minus rho z over two':
        "取beta为一，在零点展开x之z，其比值为一减rho z的一半，再加二次项。<bookmark mark='a'/> z等于负nu k除以alpha，所以短时间平值对数行权价斜率的领先项为rho nu的一半。一般beta还会贡献骨架项。<bookmark mark='b'/> 领先曲率按nu平方除以alpha缩放，也依赖rho。<bookmark mark='c'/> 对一般beta，保持alpha不变时，领先平值布莱克波动率为alpha乘以F的beta减一次方。<bookmark mark='d'/> 在这份51天切片上，所示近似给出斜率{sl['skew_formula']:.3f}。解释这些敏感度时，必须考虑有限期限修正和beta的选择。",

    'f"Fit each expiry separately. <bookmark mark=\'a\'/> Alpha and rho vary across sli':
        "分别拟合每个期限。<bookmark mark='a'/> alpha和rho在切片之间变化。<bookmark mark='b'/> 在这个网格上，拟合nu相对于期限的双对数斜率为{c['sabr_nu_power']:.2f}。使用{3 * len(c['sabr'])}个参数时，vega加权误差为{c['sabr_rmse']:.2f}个点；这与五参数的整体赫斯顿拟合具有不同的灵活性。有限网格的幂指数估计只是第14部分的一条描述性线索，并不能证明结构性的平方根定律。独立切片拟合也不会自动保证日历无套利。",

    "Assemble the nine smiles into a surface.":
        "把九个微笑拼成一张曲面。<bookmark mark='a'/>短端是一道又深又窄的山谷，长端几乎是平的。SABR里没有任何东西把一个切片和下一个连起来："
        "这是每个期限一个模型，而不是关于时间的模型。",

    'The backbone concerns Black implied volatility as the forward changes with alpha':
        "骨架描述保持alpha不变、远期变化时的布莱克隐含波动率。beta为一时模型具有尺度不变性，微笑按对数价值状态平移。<bookmark mark='a'/> beta为零时，领先的布莱克平值波动率为alpha除以F，而领先的正态波动率为alpha；这是不同的报价惯例。单张曲面和第12部分的黏性规则回归，不能识别beta，也不能给出普遍的对冲优劣排序。哈根的研究用微笑动态和特定对冲证据来论证SABR，但近似公式仍可能违反静态无套利检查，下面就看这一点。",

    # ------------------------------------------------------------------ SABRFix
    "Chapter seven. Where SABR's formula breaks": "第7章。SABR公式在哪里失效，交易台又如何修复它。",

    'f"Take a rates-like example with a three-percent forward and beta one half. The ':
        "取一个类似利率的例子：远期3%，beta为二分之一。一年期的隐含密度在所示网格上为正。<bookmark mark='a'/> 十年期对哈根价格求导后，低行权价处出现负密度，直接违反蝶式无套利。它在有限显示区间上的积分为{d10['mass']:.2f}；这个积分不包括边界质量，本身不能用来检验总概率。<bookmark mark='b'/> 修复方法是构造具有适当边界的非负概率分布，而非在渐近公式的可靠范围之外仍信任它。",

    "Hagan and co-authors' 2014 arbitrage-free SABR approach derives an effective one":
        "哈根等人在2014年的无套利SABR方法中，按展开阶数推导有效的一维前向偏微分方程，用来近似二维SABR动态。<bookmark mark='a'/> 有效扩散系数为D，<bookmark mark='b'/> 时间因子E包含相关效应。<bookmark mark='c'/> 零点吸收的概率保留为边界质量。这个有限区间实现也保留上边界质量。非负且质量守恒的离散化给出一致的数值分布，但它并不等于完整SABR的精确分布。",

    'f"Solve the effective PDE on {p[\'n\']} cells through ten years. <bookmark mark=\'a':
        "用{p['n']}个网格单元把有效偏微分方程推进到十年。<bookmark mark='a'/> 零点边界概率达到{100 * p['QL']:.0f}%。<bookmark mark='b'/> 哈根公式求导后的密度变为负数，在此网格达到负{abs(hmin[-1]):.0f}。<bookmark mark='c'/> 这次PDE计算的总质量保持到小数点后十位，网格概率非负。平值布莱克波动率为{100 * p['atm_pde']:.1f}%，哈根为{100 * p['atm_hagan']:.1f}%；在0.5%行权价处，两者为{100 * p['pde_iv'][lo]:.0f}%与{100 * p['hagan_iv'][lo]:.0f}%。这个比较揭示了尾部价格的不可靠性；差异也包含有效模型和数值近似误差。",

    "Other developments include Obłój's corrected leading term in 2008. <bookmark mar":
        "其他发展包括Obłój在2008年修正领先项。<bookmark mark='a'/> Antonov、Konikov与Spector通过自由边界设定扩展SABR，使其允许负利率。<bookmark mark='b'/> 平移模型和正态波动率报价也很常见，但必须说明定义域和边界。改变报价惯例或加入平移，本身并不能修复渐近公式的所有套利缺陷。",

    "For the hedge, differentiate Black's price composed with the approximate SABR vo":
        "对冲时，对布莱克价格与近似SABR波动率的复合函数求导。<bookmark mark='a'/> 保持alpha不变得到一种delta。<bookmark mark='b'/> d-alpha对d-F的瞬时线性回归贡献rho nu除以F的beta次方。这是局部协方差投影，并非对未来alpha路径的预测。<bookmark mark='c'/> 加入相应的alpha敏感度，就得到巴特利特修正，在这个例子里会降低看涨delta。第17章用合成比特币期权代理量研究相关的最小方差原则，并不是对SABR巴特利特delta的直接实证检验。下面进入跳跃。",

    # ------------------------------------------------------------------ Jumps
    "Chapter eight. Jumps: Merton, Kou, and Bates.": "第8章。跳跃：默顿、寇与贝茨。",

    "A diffusion cannot gap.":
        "扩散过程不会跳空。罗伯特·默顿在1976年加入了跳跃，他的模型有一个精确解，最好把它看成一个千层蛋糕。三个月里价格跳零次、一次、两次；"
        "给定次数，对数价格是高斯的。<bookmark mark='a'/>所以分布是一层层高斯分布的叠加，每层按跳跃平移，按泊松概率加权。"
        "<bookmark mark='b'/>提高强度：权重移向跳跃层，左尾变厚，这正是看跌期权买到的崩盘保险。<bookmark mark='c'/>"
        "降低强度，蛋糕塌缩回布莱克和斯科尔斯。",

    'Under the pricing measure, assume independent Poisson jumps, Gaussian jump marks':
        "在定价测度下，假设泊松跳跃、高斯跳幅和布朗扩散相互独立。负lambda k-bar补偿项维持零持有成本的远期鞅。<bookmark mark='a'/> 给定n次跳跃，对数价格为高斯。<bookmark mark='b'/> 按泊松概率对相应布莱克价格取平均，得到默顿级数；公司的数值基准与COS在八位小数上吻合。<bookmark mark='c'/> 贝茨把赫斯顿变换与独立的默顿跳跃因子相乘。寇采用双指数跳幅，无记忆越界性质使首达时变换易于处理；有限期限障碍定价仍可能需要反演。这些公式描述模型价格，并非现实跳跃频率。",

    'f"Compare fits to the same {c[\'n\']} filtered marks. Black\'s single volatility mi':
        "比较对同一组{c['n']}个筛选后标记价格的拟合。布莱克单一波动率误差为{c['fits']['BS']['rmse']:.1f}个点。<bookmark mark='a'/> 默顿达到{F['Merton']['rmse_iv']:.1f}，定价测度跳跃强度为每年{m['lam']:.2f}次，对数跳幅均值{m['mj']:.2f}，对数跳幅标准差{m['sj']:.2f}。对数均值不是简单跌幅；平均比例跳幅等于mu加半个方差的指数，再减一。{d0}天拟合仍差{mv[d0]:.1f}个点，寇误差为{F['Kou']['rmse_iv']:.1f}。<bookmark mark='b'/> 赫斯顿为{c['fits']['Heston']['rmse']:.2f}，贝茨为{c['fits']['Bates']['rmse']:.2f}。贝茨强度{b['lam']:.0f}达到允许上界，对数跳幅均值{b['mj']:.3f}，离散程度{b['sj']:.2f}。<bookmark mark='c'/> 很小的拟合改善和约束边界解说明识别较弱，不能据此断言市场没有给股灾风险定价。",

    "Rare and huge: crash insurance":
        "稀少而巨大：这是崩盘保险，是常数波动率模型让短期看跌期权变贵的唯一办法。",

    "Frequent and moderate:":
        "频繁而温和：跳跃起到了额外曲率的作用。",

    'f"The three Bates traces show objective value, jump intensity and dispersion. Th':
        "三条贝茨轨迹展示目标函数、跳跃强度和离散程度。完整评估日志分别有345、383、345次调用，缓存每个起点保留300个点。<bookmark mark='a'/> 主要拟合改善后，跳跃参数仍相互补偿。记录的运行达到允许的强度上界和离散程度下界。有限跳跃模型在某些情形下能近似扩散效应，但这些拟合并不是精确的扩散极限。<bookmark mark='b'/> 按拟合默顿定价强度，三天没有跳跃的概率为{100 * np.exp(-lf['fits']['Merton']['params']['lam'] * 3 / 365):.1f}%。这是Q模型概率，并非对现实股灾概率的估计。短期期权价格也取决于跳幅、扩散以及完整分布。",

    "The intensity climbs, all the way":
        "强度一路上升，直到我们允许的每年二十次的上限，跳跃大小缩到下限，而损失几乎不动。",

    "The intensity and the size trade off":
        "强度和大小此消彼长，而损失几乎不动。",

    "Extensions. Duffie, Pan and Singleton":
        "延伸。达菲、潘和辛格尔顿，以及埃拉克、约翰内斯和波尔森，让波动率与价格一起跳；布罗迪、切尔诺夫和约翰内斯发现标普期权需要这样的跳跃。"
        "<bookmark mark='a'/>在比特币上，侯、王、陈和哈德勒发现价格和方差都有跳跃，而且负相关。<bookmark mark='b'/>"
        "最极端的跳跃是跳到零，也就是违约：第20部分。"
        "下一章：纯跳跃模型与时间变换。",

    # ------------------------------------------------------------------ Levy
    "Chapter nine. Lévy models, and changing the clock.": "第9章。莱维模型，以及改变时钟。",

    'f"A random clock can also produce a smile. The top path is drawn in business tim':
        "随机时钟也能产生微笑。上方路径按业务时间绘制。<bookmark mark='a'/> 下方是示意性的伽马时钟，并非实际市场活动。伽马从属过程有无穷多次跳跃，而且严格递增；图中平坦区段来自有限绘图分辨率。<bookmark mark='b'/> 把布朗运动放到这个时钟上，就得到方差伽马；日历时间下它没有布朗分量，但还有漂移修正。<bookmark mark='c'/> 拟合的时钟方差率为{nu_fit:.3f}，比示意例子小，但波动程度仍取决于观察期限。这个参数并不意味着拟合时钟是确定的。",

    "Conditioning on the gamma clock gives a Gaussian log increment. <bookmark mark='":
        "给定伽马时钟，对数增量为高斯。<bookmark mark='a'/> 条件变换是时钟时间的指数函数。<bookmark mark='b'/> 再用伽马变换取平均。<bookmark mark='c'/> 实数漂移修正要求股票的指数矩存在；方差伽马需要一减theta nu再减半个sigma平方nu为正。<bookmark mark='d'/> CGMY推广跳跃密度：Y小于零为有限活动；从零到小于一为无限活动但有限变差；从一到小于二为无限变差。这是活动度和变差分类，并非普遍的隐含偏斜幂指数。<bookmark mark='e'/> 独立的积分CIR时钟作用于布朗对数收益，得到零相关赫斯顿。适当构造的一般莱维时钟也可保持仿射形式，但相关赫斯顿需要相应依赖，不能任意使用独立时间变换。",

    'f"Compare three CGMY laws normalized to equal variance. The simulated paths use ':
        "比较三个归一到相同方差的CGMY分布。模拟使用0.1%的截断，最小跳跃作数值近似。<bookmark mark='a'/> Y为负二分之一时，超过该截断的预期次数约{cg['-0.5']['lam_eps']:.0f}。<bookmark mark='b'/> Y为二分之一时约{cg['0.5']['lam_eps']:.0f}。<bookmark mark='c'/> Y为二分之三时约{cg['1.5']['lam_eps']:.0f}，所以有限分辨率路径看起来类似扩散。视觉平滑并不证明存在布朗分量；对无限活动分布，这些截断次数也不是总跳跃次数。",

    'f"In the House: the characteristic function with its drift correction':
        "在公司的代码里：带漂移修正的特征函数，以及抽取伽马增量和缩放高斯变量的模拟器。<bookmark mark='a'/>"
        "用两种方法给拟合模型下的三十天平值看涨期权定价。{verdict}",

    "f'The two agree within": "两者在{abs(z):.1f}个标准误差以内一致。",

    "f'They differ by": "两者相差{abs(z):.1f}个标准误差：需要更多路径，或者更细的时钟。",

    'f"Fit variance gamma, NIG and two CGMY parameter domains to the same pooled mark':
        "把方差伽马、NIG和两个CGMY参数区域，拟合到相同汇集标记。损失图保留全部保存轨迹，包括超过十八的CGMY初始损失。<bookmark mark='a'/> 这些拟合的IV误差高于赫斯顿的{hes:.1f}个点。<bookmark mark='v'/> 大于一区域的CGMY拟合，Y为{c2['Y']:.2f}；不同区域给出不同近似误差。有限样本拟合更好，不能确立真实过程为无限变差，也不能排除所有其他纯跳跃设定。<bookmark mark='b'/> 下面研究这些具体模型的有限网格斜率模式，区分渐近定理与拟合幂指数。",

    "f'Fitted with Y below one, CGMY runs to the edge": "限制Y小于一时，CGMY跑到了边界，{c1['Y']:.2f}。",

    "f'Fitted with Y below one, CGMY stops at": "限制Y小于一时，CGMY停在{c1['Y']:.2f}。",

    "f'Allowed above one, it settles at Y equal to":
        "允许大于一时，它停在Y等于{c2['Y']:.2f}，拟合更好：曲面要求无界变差，跳跃小而多到像扩散一样。",

    "f'Allowed above one, it reaches": "允许大于一时，它达到{c2['Y']:.2f}，但拟合并没有更好：有界变差就够了。",

    # ------------------------------------------------------------------ Skew
    "Chapter ten. The skew across maturities": "第10章。跨期限的偏斜：一张给所有模型分类的图。",

    "Ask every fitted model one question:":
        "问每个拟合好的模型一个问题：期限临近时，你的微笑会怎样？这里有六个，每个微笑都以按根号时间缩放的价值度画出。把期限从一年往下缩。"
        "<bookmark mark='a'/>赫斯顿的形状几乎不变：扩散的偏斜趋于常数。<bookmark mark='b'/>纯跳跃模型越扭越厉害，到只剩几天时成了悬崖。"
        "默顿的罕见崩盘只出现在很远的看跌翼；贝茨和CGMY处于两者之间。",

    'f"The powers in this table are regressions over finite maturity ranges. White po':
        "表中的幂指数是有限期限区间上的回归。白点来自拟合基准曲面，绿点来自逐期限SABR对报价切片的近似。<bookmark mark='a'/> 市场代理量的整体斜率为{mkt['all']:.2f}，短端和长端为{mkt['short']:.2f}与{mkt['long']:.2f}。<bookmark mark='b'/> 赫斯顿为{h['short']:.2f}与{h['long']:.2f}；方差伽马为{vg['short']:.2f}与{vg['long']:.2f}；NIG为{ni['short']:.2f}与{ni['long']:.2f}。默顿和寇的短区间斜率为{me['short']:.2f}与{ko['short']:.2f}。Y等于{Y:.2f}的CGMY为{cg['short']:.2f}。<bookmark mark='c'/> 这些数字描述本次校准和网格，不能识别整个跳跃家族的普遍幂指数，也不能证明市场的渐近规律。第14部分会讨论这些区别。",

    "f'Only CGMY, with Y of":
        "只有CGMY，Y为{Y:.2f}，一种几乎像扩散一样的无界变差跳跃，在短端接近市场：{cg['short']:.2f}。",

    "f\"CGMY's short-end slope is": "CGMY的短端斜率是{cg['short']:.2f}。",

    "So at the short end the market sits between":
        "所以在短端，市场处于扩散模型和纯跳跃模型之间。这一部分没有任何模型在每个期限上都得到正确的幂次，而大约负二分之一的整体斜率，"
        "正是第14部分的起点。",

    "The market does not sit neatly between":
        "在这里市场并不恰好落在两个家族之间；第14部分会讨论概括它的幂律。",

    'f"Here is a useful heuristic, with its regime stated. For a Lévy process with th':
        "这里有一个必须说明适用范围的启发式。若莱维过程具有所需的有限累积量，平稳独立增量使各阶累积量与时间成正比。<bookmark mark='a'/> 因此标准化偏度按根号T的倒数缩放。<bookmark mark='b'/> 在领先的近高斯Gram–Charlier近似中，绝对隐含波动率斜率为偏度除以六倍根号T，于是得到一除以T的启发。期限趋于零时，近高斯近似一般会失效，因此这不是普遍的莱维短时间定理。<bookmark mark='c'/> 初始方差为正、系数光滑的赫斯顿动态，则具有第四章推导的有限平值偏斜极限。<bookmark mark='d'/> 本次拟合的xi为{c['fits']['Heston']['params']['xi']:.1f}。有限期限、粗糙模型和其他跳跃情形仍需各自分析。",

    "Two repairs. Carr, Geman, Madan and Yor":
        "两种修复。卡尔、盖曼、马丹和约尔的可加过程，增量独立但不同分布，修好了莱维模型的期限结构。<bookmark mark='a'/>"
        "阿比·贾贝尔和德卡瓦略证明，均值回复极快的赫斯顿模型会模仿跳跃；第18章会把我们的拟合往那个方向推。"
        "没有一个模型能拟合所有期限。下一章：把随机波动率和局部波动率结合起来。",

    # ------------------------------------------------------------------ SLV
    "Chapter eleven. Stochastic local volatility": "第11章。随机局部波动率，以及粒子方法。",

    "Local volatility targets today's marginals; stochastic volatility supplies anoth":
        "局部波动率以当日边缘分布为目标，随机波动率提供另一种微笑动态。SLV把两者结合：赫斯顿方差的波动率乘以eta，再乘杠杆函数。<bookmark mark='a'/> 在适当的存在性和正则条件下，杠杆平方乘条件方差等于杜皮尔方差，就有相同的单时点边缘分布和普通期权价格。这是理想恒等式。<bookmark mark='b'/> 条件期望采用模型自己的分布，而该分布依赖杠杆，因此形成麦基恩–弗拉索夫方程。<bookmark mark='c'/> Guyon和Henry-Labordère的粒子方法对模拟粒子进行核回归来估计它。<bookmark mark='d'/> 所示偏差与噪声平衡来自独立样本核回归的启发式分析。相互作用的粒子、时间离散、边界和稀疏翼部还会增加误差；它不是这个实现的收敛定理。",

    'Each dot is a saved log-price and Euler variance particle. This view includes al':
        "每个点代表保存的对数价格和欧拉方差粒子。图中包括所有已保存粒子，也包括少量负的欧拉方差；价格更新使用方差的正部。<bookmark mark='a'/> 金线是原始核估计。右侧用以十为底的对数展示杠杆，保留早期翼部的大值。<bookmark mark='b'/> 初始粒子几乎集中于一点。缺乏粒子支持的网格翼部，核分母可能下溢，条件方差下限会使杠杆超过一千。这是数值估计，不能解释成经济上的杠杆尖峰。原算法对网格插值，并未设置杠杆上限。中心位置和后期估计小得多。粒子计算一边模拟一边校准，但仍存在可测的重新定价误差。",

    'Stack the saved leverage grids from ten to a hundred and twenty days. The height':
        "把十天到一百二十天的杠杆网格堆成曲面。高度是杠杆的十进对数，灰平面代表杠杆为一。<bookmark mark='a'/> 这样保留原始翼部估计，而不是把它们截平在显示上限。早期缺乏粒子支持的翼部和方差下限可能主导高度。在这个拟合中，平值附近杠杆接近一或低于一。这些网格展示数值粒子方法，并非光滑且由市场唯一识别的杠杆曲面。",

    'f"The code uses a subsample, Silverman\'s bandwidth, kernel weights, and a matrix':
        "代码采用子样本、Silverman带宽、核权重和矩阵乘法来估计条件方差，再对杠杆插值并进行欧拉更新。实现还保护权重分母，并给估计方差设置下限。<bookmark mark='a'/> 四万粒子推进一百二十天后，三十天重新定价误差为{rep[0]['err']:.2f}个波动率点，一百二十天为{rep[-1]['err']:.2f}。这里包含模拟误差、时间步长、核偏差、子采样、插值、下限和局部波动率近似，不能全部归因于蒙特卡洛噪声。",

    'f"How many particles are enough?':
        "多少个粒子才够？两千、八千和四万，每个三个随机种子。<bookmark mark='a'/>{v1}<bookmark mark='b'/>N小时种子带很宽："
        "杠杆和重新定价的检验都有噪声。<bookmark mark='c'/>再看带宽，在八千个粒子时：{v2}",

    'f"The error falls from':
        "误差从两千个粒子时的{runs.mean(0)[0]:.2f}个波动率点降到四万个粒子时的{runs.mean(0)[-1]:.2f}，对数坐标上斜率为{slope:.2f}，"
        "经验估计是负0.4。",

    'f"The error does not fall with N here:':
        "这里误差没有随N下降：两千时{runs.mean(0)[0]:.2f}，四万时{runs.mean(0)[-1]:.2f}；时间步长和局部波动率自身的误差占主导。",

    'f"Halving the window gives':
        "窗口减半得到{bw[0.5]:.2f}，加倍得到{bw[2.0]:.2f}，西尔弗曼的选择是{mid:.2f}：权衡是真实的，但很平缓。",

    "The PDE route solves for the joint density on a grid. <bookmark mark='a'/> Reisi":
        "偏微分方程方法在网格上求解联合密度。<bookmark mark='a'/> Reisinger和Tsianni在2025年研究的是正则化、固定带宽的赫斯顿型粒子系统。其混沌传播结果要求费勒比率至少为一，并受临界时间限制。另一个欧拉时间离散结果在忽略对数因子时接近二分之一阶，但要求费勒比率大于二加根号三。这是两个不同的极限。默认eta为二分之一时，有效费勒比率约为1.48，高于一，却低于该时间步长条件。这里也未验证其他正则性和算法条件。<bookmark mark='b'/> 将方差波动率设为零，杠杆就是局部波动率除以确定性方差的平方根。在理想恒等式下，这给出局部波动率扩散。",

    # ------------------------------------------------------------------ MixFrac
    "Chapter twelve. The mixing fraction": "第12章。混合比例：两个世界之间的一个旋钮。",

    'f"Eta scales Heston\'s variance diffusion. At zero, deterministic variance and th':
        "eta缩放赫斯顿方差的扩散。为零时，确定性方差和理想杠杆恒等式给出局部波动率；为一时保留全部赫斯顿方差波动率，并重新校准杠杆。我们运行五个设置，每个四万粒子。<bookmark mark='a'/> 观察杠杆、远期起始微笑和棘轮价格。远期斜率从{100 * sks[0]:.1f}变为{100 * sks[-1]:.1f}个点。棘轮端点价格分别为{100 * cls[0]:.2f}%和{100 * cls[-1]:.2f}%，中间值不一定单调变化。<bookmark mark='b'/> 普通期权平均重新定价误差最高为{worst:.1f}个点。普通期权严格不变属于理想模型，这些粒子运行并未实现。<bookmark mark='c'/> eta为二分之一的三个种子，棘轮价格标准差为{10000 * sd_c:.1f}个基点，网格范围为{10000 * span:.0f}个基点。这个描述性离散程度不是置信区间，也不能证明排序；拟合和离散化误差同样进入比较。",

    'f"It stays under':
        "在每个设定下它都低于{worst:.1f}个波动率点。这正是关键：今天的香草期权看不到eta，而每个奇异期权都看得到。",

    "f'It reaches":
        "在最差的设定下它达到{worst:.1f}个波动率点，那里粒子很吃力；即便如此，香草期权几乎感觉不到这个旋钮，而每个奇异期权都能感觉到。",

    "f'The cliquet moves steadily,":
        "棘轮期权稳步变化，从eta为零时的{100 * cls[0]:.2f}%到eta为一时的{100 * cls[-1]:.2f}%。",

    "f'The cliquet moves from":
        "棘轮期权从eta为零时的{100 * cls[0]:.2f}%变到eta为一时的{100 * cls[-1]:.2f}%，但不是一条直线。",

    'f"Across three seeds at eta one half, the cliquet varies by only':
        "在eta为二分之一时的三个种子之间，棘轮期权只变化{10000 * sd_c:.1f}个基点，所以旋钮的影响{10000 * span:.0f}个基点是真实的。",

    'f"Across three seeds at eta one half, the cliquet varies by {':
        "在eta为二分之一时的三个种子之间，棘轮期权变化{10000 * sd_c:.1f}个基点，与旋钮的影响相当：要给各设定排序需要更多粒子。",

    'In the ideal construction, each eta has its own leverage and its own conditional':
        "在理想构造中，每个eta都有自己的杠杆和条件方差，用来保留单时点边缘分布。<bookmark mark='a'/> eta为零时退化为局部波动率。<bookmark mark='b'/> 但总波动率，也就是L乘根号v，其瞬时扩散同时包含杠杆的空间导数和方差冲击。改变eta并重新校准时，L也会变化；只保留rho eta xi会遗漏这一依赖。<bookmark mark='c'/> 远期起始期权和棘轮价格随eta变化，并不存在一般性的单调定理。保存的棘轮网格就是所声称单调规则的数值反例。暂停想一想：哪种收益能识别单时点边缘分布之外的动态？在精确构造中，欧式期权不能，比率远期起始期权和棘轮通常可以。相对敏感度必须实际计算，并评估数值误差。",

    "So how does a desk set the dial?":
        "那么交易台怎么设定这个旋钮？不能靠香草期权：它们看不到。外汇交易台广泛使用这个模型，它们用银行间本身有报价的奇异期权，"
        "障碍期权和无触碰期权，来设定它，伊恩·克拉克的教科书描述了这种做法。<bookmark mark='a'/>粒子方法让这变得可行："
        "旋钮的任何设定都能在一次模拟中校准到香草期权。然后其余的奇异期权在两者之间定价。在加密市场，流动的奇异期权很少，"
        "旋钮是一个建模选择，它的范围就是模型风险。"
        "下一章：模型的另一种状态变量——远期方差。",

    # ------------------------------------------------------------------ Bergomi
    "Chapter thirteen. Bergomi's models": "第13章。贝尔戈米的模型：以远期方差为状态。",

    'f"Differentiate total variance to obtain a forward-variance curve. Here total va':
        "对总方差求导，可得到远期方差曲线。这里总方差来自有限的SSVI期权条带，期限之间采用线性插值，所以导数分段常数。这是一种拟合构造，并非唯一可观测的瞬时方差曲线。<bookmark mark='a'/> 十二月十三日至十四日的区间，隐含波动率为{100 * fv[sat]:.0f}%。另一个历史样本中，周六已实现波动率平均为{100 * b['by_dow'][5]:.0f}%，工作日为{100 * np.mean(b['by_dow'][:5]):.0f}%。一个报价区间和实际测度下的季节性统计，并不能识别因果性的周末风险溢价。<bookmark mark='b'/> 赫斯顿期望方差只有一条指数曲线，无法复现任意凹陷或预定事件形状。",

    "Lorenzo Bergomi turned this around:":
        "洛伦佐·贝尔戈米把这件事反过来做：让整条曲线成为状态，今天的曲线直接取自市场。每一点是那个日期方差的期望，所以是一个鞅："
        "一份远期方差互换的费率。<bookmark mark='a'/>在他的两因子模型里，每一点都对数正态地运动，由一快一慢两个奥恩斯坦–乌伦贝克因子驱动，"
        "影响随距离衰减。<bookmark mark='b'/>积分之后：今天的曲线乘以一个对数正态鞅。<bookmark mark='c'/>由伊藤公式，每一点的波动率只取决于它的距离tau："
        "一个波动率的波动率的期限结构，与今天的曲线无关。<bookmark mark='d'/>赫斯顿的每一点都由同一个冲击乘以e的负kappa tau次方驱动，"
        "而同一个kappa还决定今天曲线的形状：一个数字，两份工作。",

    'f"Simulate an illustrative two-factor Bergomi curve for four months. Each slice ':
        "把示意性的双因子Bergomi曲线模拟四个月。每个切片展示滚动剩余期限，因此它本身不是固定日期的鞅图。<bookmark mark='a'/> 前端变动快，远端较慢。omega通过三十天内核幅度的不加权平均选定，用DVOL实测波动率之波动率作为尺度。精确指数扩散需要方差权重和向量聚合，所以这个启发式设置并不是对波动率指数价格的联合校准。<bookmark mark='b'/> 两千条路径的平均方差，与相同绝对日期的初始曲线相比，误差在{100 * dev:.1f}%以内。这才是相关的固定日期鞅检查。<bookmark mark='c'/> 赫斯顿远端冲击指数衰减；在这个kappa拟合值下很小，但并非严格为零。",

    'f"Plot the instantaneous relative diffusion magnitude of forward variance agains':
        "把远期方差的瞬时相对扩散幅度按剩余期限画出。这些百分数针对方差，并非波动率，也不是三十天指数。<bookmark mark='a'/> 示意Bergomi曲线在九十天处为{100 * bs['volvol_bergomi'][i90]:.0f}%。<bookmark mark='b'/> 赫斯顿起点接近958%，在九十天处降为{100 * bs['volvol_heston'][i90]:.0f}%。图中保留全部高度。赫斯顿一个回复速度同时约束初始远期方差形状和未来冲击衰减；Bergomi把输入曲线与因子速度分开。<bookmark mark='c'/> 对这组参数，近期远期方差点的相对扩散高于远期。方差互换率平均一个区间内的这些点，其波动率还依赖权重和相关性；单点图不能对所有互换波动率给出普遍排序。",

    'f"The skew-stickiness ratio compares the instantaneous regression of ATM implied':
        "斜率黏性比率，把平值隐含波动率对数价格的瞬时回归系数，与平值行权价斜率相比。<bookmark mark='a'/> 在赫斯顿模型的领先扩散阶，方差回归系数为rho xi。<bookmark mark='b'/> 短期限平值波动率趋于根号v，给出rho xi除以二倍根号v。<bookmark mark='c'/> 再除以正则赫斯顿的短时斜率，在斜率非零时得到二。这只是局部平值极限。<bookmark mark='d'/> 这个拟合下，有限期限数值比率在两天为{r2['R']:.2f}，一年为{r365['R']:.2f}。与局部波动率在一个短时统计量上相同，并不能说明微笑动态完全一致。远期起始价格会揭示其他差异。",

    # ------------------------------------------------------------------ Forward
    "Chapter fourteen. Forward smiles, and cliquets.": "第14章。远期微笑与棘轮期权。",

    'f"Here a forward smile means today\'s risk-neutral prices of fixed-notional ratio':
        "这里的远期微笑指今天对固定名义本金比率收益的风险中性定价，再转换成布莱克隐含波动率。期权收益是终值价格除以重设价格、减行权价后的正部：六十天后开始，持续三十天。它不是实际测度预测，也不是未来隐含波动率的平均。白线使用赫斯顿积分，内部采用数值COS定价和求积。<bookmark mark='a'/> 点表示累计路径后得到的比率收益模拟价格。<bookmark mark='b'/> 三个种子的均值最多相差{dev:.1f}个波动率点，最大种子范围为{spread:.1f}。这些只是描述性检查；落在种子范围内不能证明模拟无偏，出现差异也不能唯一识别原因。",

    "f'The three seeds average to within":
        "三个种子的平均在每个行权价上都与积分相差不到{dev:.1f}个波动率点，落在它们自己{spread:.1f}的离散范围内：模拟与公式一致。",

    'f"The seeds\' average misses the integral by up to':
        "种子的平均与积分最多相差{dev:.1f}个点，超过它们{spread:.1f}的离散范围：模拟有离散化偏差。",

    'f"Ask five implementations for the same ratio forward-start prices. They use the':
        "向五种实现询问相同比率远期起始价格。它们采用相同曲面输入，但普通期权拟合误差和数值误差不同。<bookmark mark='a'/> 在这次校准中，局部波动率远期斜率为{100 * lv['fwd_skew']:.1f}个点，当期SSVI目标为{100 * e['today_skew']:.1f}个点。这种变平来自本次拟合的局部波动率曲面，并非适用于所有局部波动率模型的定理。<bookmark mark='b'/> 赫斯顿为{100 * he['fwd_skew']:.1f}，Bates为{100 * e['models']['Bates']['fwd_skew']:.1f}，方差伽马为{100 * vg['fwd_skew']:.1f}，SLV为{100 * e['models']['SLV']['fwd_skew']:.1f}。方差伽马重复的是它自己的当前微笑，而非目标曲面。比较同时包含动态差异和不相等的拟合误差。",

    'For this ratio payoff, condition at the reset date and normalize spot to one. We':
        "对这个比率收益，在重设日期条件化，并把价格标准化为一。示例采用零利率。<bookmark mark='a'/> 平稳独立增量使指数莱维模型重复自己当前的三十天微笑。<bookmark mark='b'/> 赫斯顿需要把条件标准化价格，对重设日普通风险中性CIR方差分布求平均。若收益另乘重设价格，就需要资产权重和不同测度。<bookmark mark='c'/> 每个局部保底封顶票息，都等于保底加一个比率看涨价差；线性性允许从这些远期起始价格定价总和。若另有生效的全局保底，就需要票息联合信息。本例票息下限为零，因此零全局保底是多余的。<bookmark mark='d'/> 莱维平稳性只保证这个合约与模型自己的当日期权相等，并不强制匹配虚线SSVI目标。",

    "The cliquet on three simulated paths:":
        "三条模拟路径上的棘轮期权：每个灰色轮廓是一个月的收益。<bookmark mark='a'/>每个月下限为零、上限为百分之十，收益是它们的和。"
        "<bookmark mark='b'/>所以它的价值取决于未来每个月的波动率和偏斜：远期微笑。今天的香草期权只固定到每个日期的总收益，"
        "而不固定它在各月之间如何分配。",

    'f"The four-coupon cliquet costs {100 * v1.min():.1f} to {100 * v1.max():.1f} per':
        "四票息棘轮在这些实现中的价格，占名义本金{100 * v1.min():.1f}%至{100 * v1.max():.1f}%，相对于均值的范围为{100 * (v1.max() - v1.min()) / v1.mean():.0f}%。<bookmark mark='a'/> 平值比率远期起始期权价格范围为{100 * (v2.max() - v2.min()) / v2.mean():.0f}%，这里局部波动率最高。<bookmark mark='b'/> 单时点边缘分布无法识别完整联合分布，但这个观测价差还包含不相等的普通期权拟合误差和数值误差。它不是独立的动态风险估计，也不是统计置信区间。交易台用它制定估值准备前，应先核对这些误差。接下来用比特币输入，说明相关的波动率指数难题。",

    # ------------------------------------------------------------------ Puzzle
    'Chapter fifteen. A Bitcoin illustration of a volatility-index calibration challe': '第十五章。用比特币说明波动率指数校准的难题。',

    'VIX futures began trading in 2004 and VIX options in 2006. A model for S&P price':
        "VIX期货于2004年上市，VIX期权于2006年上市。标普价格模型还必须预测未来波动率指数的分布。<bookmark mark='a'/> Gatheral在2008年研究了双方差因子的联合拟合。<bookmark mark='b'/> Guyon在2020年的研究描述了常见连续模型中，陡峭短期SPX斜率与较高VIX期权隐含波动率之间的矛盾，并提供特定的非参数离散时间构造。跳跃及其他更丰富动态也提供途径。这里的比特币练习，把拟合模型指数与历史DVOL相比。计算没有使用比特币波动率期权曲面，因此这是说明性例子，并非实测的联合校准检验。",

    'f"The fitted Heston implies a thirty-day index from expected future variance. Co':
        "拟合的赫斯顿通过未来期望方差，给出三十天指数。把四年定价测度模拟与观测DVOL相比。<bookmark mark='a'/> 下限和变动程度取决于此次校准。这些独立路径仅为说明而对齐，并不是历史路径预测。<bookmark mark='b'/> 模拟对数指数的波动率之波动率中位数为{100 * h['volvol_median']:.0f}%，历史值为{100 * vp['dvol_volvol']:.0f}%，比值{r_:.1f}。相关性分别为{h['corr_median']:+.2f}和{vp['dvol_corr']:+.2f}。两百条模拟路径描述Q下的采样离散程度。与P历史的差异还涉及漂移、状态占用和指数构造，不能单独证明模型无法定价比特币波动率期权。",

    "Heston's squared model index is its thirty-day forward variance averaged over th":
        "赫斯顿的模型指数平方，是指数窗口内三十天远期方差的平均。<bookmark mark='a'/> 詹森不等式把指数的Q期望，约束在指数平方Q期望的平方根以下，要求日期、窗口和指数定义一致。这里比较的是匹配的远期方差，而非任意即期起始方差互换。<bookmark mark='b'/> 在离散程度小时，差值近似为指数方差除以均值的两倍。<bookmark mark='c'/> 等价的吉尔萨诺夫测度变换，在相同状态下保留条件瞬时二次变差，但会改变漂移。它不一定保留无条件日收益方差、平稳状态分布或过滤指数的统计量。因此历史检验需要指定P模型，并使用可比观测。",

    'f"Draw the square root against the model\'s squared index in thirty days. <bookma':
        "把平方根函数与模型三十天后的指数平方一起画出。<bookmark mark='a'/> 对匹配的Q分布，均方根为{100 * vs:.1f}%，指数期货为{100 * fut:.1f}%。<bookmark mark='b'/> 这次赫斯顿拟合还给出约{100 * h['floor']:.0f}%的指数下限。詹森上界适用于相同远期窗口和指数定义。比较不同时段的互换、不同指数或有摩擦的市场报价，是另一个问题。",

    'f"Model-index option ATM implied volatility is {100 * a30:.0f} percent at thirty':
        "模型指数期权的平值隐含波动率，三十天为{100 * a30:.0f}%，九十天为{100 * a90:.0f}%，所示网格微笑向上。<bookmark mark='a'/> 在这个拟合下，Bates模拟指数的波动率之波动率为{100 * B['volvol_median']:.0f}%。这些是特定校准的预测。<bookmark mark='b'/> 这里没有观测到的比特币指数期权价格供比较，吉尔萨诺夫也不能让Q模拟直接等同于P下无条件统计。练习旨在引出联合市场检验和明确的P动态，并不估计波动率风险溢价。下面讨论校准稳定性。",

    "f'Bates, with its jumps, does no better:":
        "带跳跃的贝茨也好不了多少：它的指数的波动率的波动率是{100 * B['volvol_median']:.0f}%，因为它的扩散部分要拟合同样的偏斜。",

    'f"Bates\'s jumps relieve the diffusion:':
        "贝茨的跳跃减轻了扩散的负担：它的指数的波动率的波动率是{100 * B['volvol_median']:.0f}%，更接近DVOL。",

    # ------------------------------------------------------------------ Calibration
    "Chapter sixteen. Calibration, as an inverse problem.": "第16章。校准，作为一个反问题。",

    'f"Calibration is an optimization; look at its landscape.':
        "校准是一个优化问题；看看它的地形。固定赫斯顿的均值回复和波动率的波动率，重新拟合另外三个，记录误差，在网格上做一遍。"
        "<bookmark mark='a'/>最小值是那颗黄星，位于一道又长又弯的山谷尽头，更快的均值回复和更高的波动率的波动率在那里此消彼长："
        "正是第4章回放中滑过的山谷。kappa取{Ld['kappa'][i0]:.0f}而不是{best[1]:.0f}时，误差只从{Lm.min():.2f}升到{along:.2f}。"
        "<bookmark mark='b'/>十二个随机起点都落到黄星；但数据确定的是两者的组合，而不是各自的值。",

    'f"Approximate the local loss curvature using Gauss–Newton, J transpose J. The fi':
        "用高斯–牛顿矩阵J转置乘J近似局部损失曲率。前四个参数采用对数坐标，rho不变换；对其他三个坐标进行剖面处理采用舒尔补。<bookmark mark='a'/> 在这个坐标系中，跨谷曲率是沿谷曲率的{hs['profile_cond']:.0f}倍。这描述拟合目标的局部敏感度，并非与坐标无关的信息度量。",

    'f"The optimizer minimizes squared price errors divided by quote vega. This appro':
        "优化器最小化价格误差除以报价vega后的平方和。它在局部近似隐含波动率误差，但报告的vega加权IV均方根误差是不同统计量。<bookmark mark='a'/> 高斯–牛顿曲率识别所选坐标中局部平坦的方向。<bookmark mark='b'/> 所示协方差公式还要求误差独立、尺度正确且模型适当。示意kappa标准误差为{100 * se[1]:.0f}%，条件数为{hs['cond']:.0f}；对汇集期权标记和可能失配的模型，这些假设未经验证，所以不是实证置信区间。<bookmark mark='c'/> 对这里的原始残差，相对惩罚增加报价数乘lambda W转置乘W。将整个目标除以报价数，就得到归一化惯例。这个惩罚公式采用原始参数；上面的对数坐标诊断还需要转换权重。除非W为单位阵，否则各特征值并不统一增加相同幅度。这是施加稳定性信息，而非自动恢复缺失的市场信息。",

    'f"Recalibrate on a hundred weekly pooled-mark surfaces. Single-day fits use matu':
        "对一百张每周汇集标记曲面重新校准。单日拟合使用两天以上期限，每周拟合使用六天以上，因此样本范围不同。kappa每周变化的中位数为{100 * h['median_weekly_change']['kappa']:.0f}%，有{100 * kb:.0f}%的周达到边界。<bookmark mark='a'/> {100 * fe:.0f}%的周不满足CIR严格正值的费勒条件，这意味着可以到达零，而非模型无效。<bookmark mark='b'/> {100 * rp:.0f}%的周，拟合rho为正。<bookmark mark='c'/> 参数漂移可能来自曲面变化、风险溢价、数据稀疏、模型误差、优化器表现和弱可识别性。这些拟合不能确立不变的实际测度常数；对奇异产品和对冲的影响还需计算。",

    'f"Replay the hundred weekly fits across log kappa and log xi. <bookmark mark=\'a\'':
        "在对数kappa和对数xi平面上回放一百次每周拟合。<bookmark mark='a'/> 两者经常同向变化，在这些坐标中的相关系数为{corr:+.2f}。右图保留完整拟合误差范围。这类似局部校准谷，但对变化市场输入的时间序列，并不等同于在固定曲面上扰动参数；弱可识别性和输入变化都可能贡献其中。",

    'f"The House stacks price-over-vega residuals with a penalty on relative paramete':
        "House把价格除以vega的残差，与相对上周参数变化的惩罚堆叠。<bookmark mark='a'/> 用两种惩罚强度，重跑相同一百个日期，比较参数变化中位数与拟合误差中位数。<bookmark mark='b'/> {verdict} <bookmark mark='c'/> 这里衡量稳定性与拟合的取舍，并未实测对冲改善。暂停：若kappa从三跳到二十，而拟合误差几乎不变，可以推出什么？普通期权价格可能仍接近；远期起始、棘轮和对冲比率可能变化，但仅凭kappa不能推出方向或幅度，其他拟合参数和收益结构同样重要。接下来评估对冲。",

    "f'The strongest pull cuts the typical weekly change":
        "最强的拉力把典型的周度变化缩小了{cut:.0f}倍，代价是中位拟合误差增加{cost:.2f}个波动率点。",

    "f'Even the strongest pull cuts the weekly change only":
        "即使最强的拉力也只把周度变化缩小了{cut:.1f}倍，代价是{cost:.2f}个波动率点的拟合：不稳定不只是噪声。",

    # ------------------------------------------------------------------ Industry
    "Chapter seventeen. The industry:": "第17章。业界：谁在建这些模型，交易台如何评判一个模型。",

    'Bank research groups developed many of these methods alongside academic work. Be':
        "银行研究团队与学界共同发展了许多方法。Bergomi的微笑动态论文，以及Guyon和Henry-Labordère的粒子方法，都与法国兴业银行的股票衍生品实践密切相关。Henry-Labordère获得2023年Risk量化奖，Guyon因与Mustapha合作的联合校准研究获得2025年奖项。这些描述历史任职与研究贡献，不代表所有人目前的雇佣关系。<bookmark mark='a'/> 交易所还创建了可交易的波动率市场，例如Cboe的VIX衍生品。Deribit的DVOL是比特币隐含波动率指数，有自己的构造和产品体系；这不等于本计算完成了比特币VIX期权校准。",

    'A desk evaluates pricing error, hedge behavior and numerical reliability togethe':
        "交易台会同时评估定价误差、对冲表现和数值可靠性。局部最小方差对冲，把期权变动对价格变动回归。<bookmark mark='a'/> 采用布莱克价格代理时，一阶变动包括delta乘价格变化，以及vega乘隐含波动率变化。<bookmark mark='b'/> 若beta是隐含波动率变动对比例价格收益的回归系数，修正就是vega beta除以S。<bookmark mark='c'/> 在赫斯顿中，精确瞬时模型公式使用方差敏感度：C下标S，加C下标v乘rho xi除以S。若改用波动率敏感度，必须加入相应链式因子。<bookmark mark='d'/> 对正vega看涨期权及负beta，布莱克代理的最小方差delta更低。这是局部协方差论证，并非普遍预测，也不能保证离散对冲结果。",

    'f"This is a synthetic daily hedge exercise driven by Bitcoin spot and DVOL. Each':
        "这是由比特币价格和DVOL驱动的合成日频对冲练习。每天建立三十天平值布莱克看涨代理，次日剩二十九天，并非跟踪可执行期权标记。它忽略交易费用和融资。平均delta分别为{rc['mean_mv']:.2f}和{rc['mean_bs']:.2f}。<bookmark mark='a'/> {v_fix} <bookmark mark='b'/> {v_roll} 滚动系数严格使用此前观测。窗口比较只是描述，并非新筛选的交易策略，也不是未经触碰的留出检验。<bookmark mark='c'/> 练习展示对估计时期和代理假设的敏感性，既不能证明实际期权交易表现，也不直接检验SABR巴特利特delta。试验计数保持不变。",

    "f'Fit beta on 2021 and 2022":
        "用2021和2022年拟合beta，那时下跌伴随着波动率飙升，样本内对冲误差方差下降{100 * fx['in']:.0f}%。然后把它用到2023到2025年，"
        "杠杆效应减弱并反转，误差方差上升{100 * -fx['out']:.0f}%。",

    "f'A beta fitted on 2021 and 2022 changes":
        "用2021和2022年拟合的beta，样本内使误差方差变化{100 * fx['in']:+.0f}%，之后变化{100 * fx['out']:+.0f}%。",

    "f'Re-estimate beta every day":
        "每天用最近六十天重新估计beta，在整个期间都有帮助：方差减少{100 * ro['60']['all']:.0f}%；在各个窗口中最好为"
        "{100 * ro[best]['all']:.0f}%。效果温和，而且不是每年都有效。",

    "f'Even a rolling sixty-day beta":
        "即使是滚动六十天的beta，总体上也没有帮助：{100 * ro['60']['all']:+.0f}%。",

    'f"Use two thousand simulated Heston paths and daily hedges of a thirty-day call.':
        "用两千条赫斯顿模拟路径，对三十天看涨期权每日对冲。这是数值模型实验：价格来自插值COS网格，包含对数价格外推和方差截限。<bookmark mark='a'/> {v} <bookmark mark='b'/> {v2} 未对冲标准差为{hh['unhedged_sd']:.3f}，最小方差对冲后为{hh['MV']['sd']:.3f}。这里移除了约九成未对冲方差，而非保留大部分风险。残差包含正交方差冲击、离散对冲、网格近似和模拟影响。增加工具可以对冲方差敞口，但这个计算不能分离每项残差来源。",

    'f"The minimum-variance delta is best, but only by':
        "最小方差Delta最好，但只比按期权自身隐含波动率计算的布莱克-斯科尔斯Delta好{gap:.1f}%。",

    "f'Here the": "这里{best}的Delta最好；最小方差Delta没有胜出。",

    "Heston's own delta, which holds the variance fixed":
        "赫斯顿自己的Delta保持方差不变，是三者中最差的：它忽略了模型本身预测的、与价格相关的波动率变动。",

    "Heston's own delta is not the worst here.": "这里赫斯顿自己的Delta不是最差的。",

    'Published comparisons are specific to datasets and methods. Bakshi, Cao and Chen':
        "已发表的比较都依赖具体数据和方法。Bakshi、Cao与Chen的标普研究发现，加入跳跃对定价和对冲的收益不同。<bookmark mark='a'/> Matic、Packham与Härdle的比特币研究报告低跳跃频率，也研究无限活动模型，并发现某些多工具对冲有益。其重建期权数据与研究设计不同于我们的合成代理。<bookmark mark='b'/> 欧盟审慎估值第十一条，用合理模型和校准范围处理模型风险调整，目标为九成置信的审慎退出价值。我们的五模型最小至最大价差，并不是该置信计算。必须先核对不相等的拟合误差和数值误差，准备金还需要有依据的模型总体和估值程序。",

    "The House's volatility desk now runs all of this.":
        "公司的波动率交易台现在运行这一切。<bookmark mark='a'/>每个模型的特征函数，都检查过鞅性质；与基准和默顿级数对上的傅里叶定价；"
        "记录路径、能固定参数、能正则化的校准器；无套利SABR；模拟器、粒子、波动率指数、远期微笑，以及最小方差对冲。每一项都有测试。"
        "最后，前沿。",

    # ------------------------------------------------------------------ Frontier
    "Chapter eighteen. The frontier, 2023 to 2026.": "第18章。前沿，2023到2026年。",

    'f"Abi Jaber and De Carvalho\'s reversionary Heston work studies specific fast-rev':
        "Abi Jaber与De Carvalho的回复型赫斯顿研究，采用特定的快速回复和方差波动率缩放。正态逆高斯极限属于H小于等于负二分之一的区域，并非每种更快回复赫斯顿拟合的极限。这里仅对相同输入标记，用四个有限kappa重新拟合。<bookmark mark='p'/> 拟合xi如何变化？<bookmark mark='a'/> xi除以根号kappa，从{r0['xi_over_sqrt_kappa']:.2f}变为{rN['xi_over_sqrt_kappa']:.2f}。<bookmark mark='b'/> 三天误差从{r0['by_expiry']['3']:.1f}变为{rN['by_expiry']['3']:.1f}个点，总体误差从{r0['rmse_iv']:.2f}变为{rN['rmse_iv']:.2f}。有限扫描说明校准取舍，既未确立论文的渐近缩放，也不能证明市场需要跳跃或粗糙波动率。",

    "f'The vol of vol it needs grows roughly like":
        "它需要的波动率的波动率大致按kappa的平方根增长：xi除以根号kappa从{r0['xi_over_sqrt_kappa']:.2f}变到"
        "{rN['xi_over_sqrt_kappa']:.2f}。",

    "f'The vol of vol it needs grows faster than":
        "它需要的波动率的波动率比kappa的平方根增长得更快：xi除以根号kappa从{r0['xi_over_sqrt_kappa']:.2f}变到"
        "{rN['xi_over_sqrt_kappa']:.2f}。",

    "f'The three-day smile improves,":
        "三天期的微笑改善了，误差从{r0['by_expiry']['3']:.1f}降到{min((r['by_expiry']['3'] for r in runs)):.1f}个点，"
        "而整体拟合从{r0['rmse_iv']:.2f}变差到{rN['rmse_iv']:.2f}：短端想要跳跃，长端不想。",

    "f'The three-day error does not improve":
        "三天期的误差没有改善（{r0['by_expiry']['3']:.1f}到{rN['by_expiry']['3']:.1f}），整体拟合从{r0['rmse_iv']:.2f}"
        "变差到{rN['rmse_iv']:.2f}。",

    'Recent papers offer several approaches. The quintic OU model uses six effective ':
        "近期论文提供多种途径。五次OU模型采用六个有效参数，加一条输入远期方差曲线；报告的联合拟合基于选定SPX与VIX数据。<bookmark mark='a'/> Guyon和Mustapha在其数据集上，用学习的波动率因子和路径依赖结构，报告买卖价差内的联合拟合。这是特定校准结果，并非普遍拟合保证。<bookmark mark='b'/> Choi与Kwok在2024年的泊松条件化研究中，既包含精确赫斯顿方案，也包含近似变体。<bookmark mark='c'/> Reisinger与Tsianni分析正则化固定带宽粒子；第十一章已说明，粒子结果与欧拉时间结果有不同条件。<bookmark mark='d'/> Wang等人在2026年合成基准中报告，粒子约98.5毫秒，神经推断约0.6毫秒，其中包括约0.53毫秒的杜皮尔输入计算，但不包含报价接入与训练。所报告奇异产品点误差没有置信区间，接近并不构成统计等价。这些论文引出进一步检验，并不认证本实现。",

    # ------------------------------------------------------------------ Outro
    'Part thirteen in ten lines. Random variance can curve a smile, and correlation c':
        '第十三部分十点回顾。随机方差可以弯曲微笑，相关性可以使其倾斜。赫斯顿具有仿射特征函数，但需小心分支与参数相互作用。QE匹配条件方差矩，仍受数值和鞅条件限制。SABR渐近公式不同于模型本身，也不同于有效密度PDE。跳跃参数依赖拟合边界，不能直接衡量实际崩盘概率。有限网格斜率幂只是描述，并非普遍模型族定律。理想SLV保留边缘分布，粒子仍有拟合和离散误差，eta也不给出普遍单调的奇异价格规则。远期起始与棘轮比较，同时反映动态差异及不相等的拟合。比特币波动率指数练习缺少指数期权报价，无法做联合检验。校准稳定性、价格拟合和对冲表现，各自都需要证据。',

    'Three desk questions. Regular short-time Heston ATM skew depends on rho xi over ':
        "三个交易台问题。正则短时赫斯顿平值斜率取决于rho xi除以四倍根号v；有限期限曲率和斜率则涉及参数相互作用。<bookmark mark='a'/> 定价棘轮时，应比较合理联合动态，量化不同拟合和数值误差后，再把价差归因于模型风险。例子中局部波动率的远期变平并非普遍结论。<bookmark mark='b'/> 詹森比较同一Q、日期、窗口和定义下的指数期货与指数平方期望的平方根，并不对任意报价期货和即期起始方差互换排序。笔记给出合约定义和假设。",

    "And nine problems:":
        "还有九道习题：赫斯顿的里卡蒂方程、它的短期偏斜、莱维模型的远期微笑、费勒条件、杠杆函数为什么有效、默顿级数，以及方差伽马的特征函数。"
        "其中两道是资格考试题：爆炸时间，以及反解李的公式。中英文解答都在讲义里。",

    'Part fourteen examines observed skew scaling, rough and path-dependent volatilit':
        '第十四部分研究观测斜率缩放、粗糙与路径依赖波动率，以及联合校准。第十五部分跨模型比较结构化产品，第十六部分研究定价方法，第十七部分研究神经校准和对冲，并检查具体基准的延迟与精度。相关思想还会回到利率、信用和外汇。后续部分将基于这些方法及其假设继续展开。',

    "The references span Merton's jumps, affine models, kernel particles and recent n":
        '参考资料涵盖默顿跳跃、仿射模型、核粒子和近期神经算子。数据包括汇集Deribit期权标记、一百张每周曲面、Binance比特币价格、Deribit DVOL和1987年标普历史。汇集标记不是同时可执行成交。研究结论和历史示例均受已说明的模型与数值假设约束。',

    'f"The volatility desk can fit, simulate and compare models. Rule thirteen: recor':
        "波动率台现在可以拟合、模拟和比较模型。规则十三：记录校准误差、数值检查和参数变化；在多个合理校准模型下定价奇异产品，并在解释价差之前核对拟合与数值误差。没有运行新的策略试验，因此计数保持{env['trials']}。<bookmark mark='a'/> 接下来第十四部分：粗糙与路径依赖波动率、经验斜率缩放，以及哪些证据能够区分竞争动态。",

    # ------------------------------------------------------------------ Research (the PhD layer)
    "For the researcher: Chapter 5 warned in passing":
        "写给研究者：第5章顺带提醒过，在随机波动率模型中，价格的某个矩可能在有限时间内变成无穷。这里说明究竟在何时，为什么这对模拟很重要，以及把它变成微笑两翼斜率的定理。",

    "Heston is affine.":
        "赫斯顿模型是仿射的。<bookmark mark='a'/>所以对数价格的矩母函数是一个指数，对起始方差是仿射的。<bookmark mark='b'/>方差系数psi满足一个里卡蒂方程。"
        "p大于一或小于零时，它的常数项为正，把psi往上推，而二次项可能让它失控。<bookmark mark='c'/>当二次式没有实根时，psi是一个平移的正切函数，在这个时刻达到无穷。"
        "<bookmark mark='d'/>莱夫·安德森和弗拉基米尔·皮捷尔巴格在2007年证明，这恰好是价格的p阶矩变成无穷的时刻。",

    "f'The explosion times for a textbook Heston":
        "一个强负相关的教科书赫斯顿模型的爆炸时间。<bookmark mark='a'/>在零和一之间，每个矩永远有限。<bookmark mark='b'/>负矩，也就是崩盘一侧，会爆炸，"
        "而且越负越早：负三阶矩在{c3['formula']:.2f}年。白点是ODE求解器的爆破时间；它们七位数字一致。<bookmark mark='c'/>在右侧，负相关让直到约八阶的每个矩永远有限；超过之后它们也会爆炸，但更晚。上尾比下尾薄。",

    'f"Consider the inverse-cube payoff, S to the minus three. Its continuous-time He':
        "考虑价格负三次方收益。连续时间赫斯顿期望在解析爆炸时间之前有限，之后无限。<bookmark mark='a'/> 第一条保存的累计均值采用该时间的一半。<bookmark mark='b'/> 第二条采用1.6倍，出现大幅跳变，最大路径占总和{100 * a['max_share']:.0f}%。这些是有限、时间离散的QE样本；看起来不稳定不能证明期望无限，表面稳定也不能证明有限。关于连续模型的结论来自解析矩结果。有界的深度虚值看跌不会继承负幂爆炸；方差互换或对数收益也不能未经独立可积性论证，就归为负幂。",

    "Connect integrability to an asymptotic wing. <bookmark mark='a'/> The critical i":
        "把可积性连接到渐近翼部。<bookmark mark='a'/> 临界负矩是负幂期望有限时q的上确界；仅靠它不能判断边界点是否有限。<bookmark mark='b'/> 李氏公式给出总隐含方差除以对数行权价绝对值的上极限，一般并不声称局部导数收敛。临界矩趋于零时，比率上界趋于二；趋于无穷时，比率趋于零。<bookmark mark='c'/> 赫斯顿的黎卡提爆炸边界识别临界指数，更强的赫斯顿尾部渐近结果，才能支持实际比率极限及相应导数表现。这些额外结论不能转移到任意模型。",

    "f'Check it on the model's own smile":
        "在模型自己的微笑上检验，一直定价到左翼深处。<bookmark mark='a'/>由临界矩得到的李极限：{w['lee']:.3f}。<bookmark mark='b'/>总方差的局部斜率向它下降，"
        "在一又四分之一处是{dk[4]:.3f}，在八处是{dk[-1]:.3f}，平均斜率下降得更慢。收敛很慢，像距离平方根的倒数，所以只观察到几个执行价的微笑，"
        "对真实尾部所说的，比看起来要少。",

    'f"Compare finite quoted wings with a fitted model\'s asymptotic prediction. <book':
        "比较有限报价翼部与拟合模型的渐近预测。<bookmark mark='a'/> 赫斯顿见过这些输入标记，因此接近只是样本内一致性观测。更根本的是，外四分之一区间斜率位于有限行权价，而李氏关系涉及无限远的对数行权价。<bookmark mark='b'/> 只有把有限斜率外推为渐近斜率，反演才给出所示短、长期限的代理q值{rows[0]['implied_q_left']:.0f}和{last['implied_q_left']:.0f}。许多不同尾部都能在观测区间一致。这些代理值不能识别市场真实临界矩，也不能确定哪些负幂收益具有有限期望。",

    "Three further questions. <bookmark mark='a'/> Rough Heston has a fractional, or ":
        "还有三个问题。<bookmark mark='a'/> 粗糙赫斯顿具有分数阶或Volterra黎卡提方程；把精确临界矩和翼部结论推广到更广的粗糙与随机局部模型，仍有困难。<bookmark mark='b'/> 赫斯顿二阶尾部修正已知，但稳健外推稀疏市场微笑，仍需假设和不确定性分析。<bookmark mark='c'/> 定价测度和实际测度尾部不必相同。差异可能反映风险补偿、状态变化和模型误差；一条拟合翼部与历史尾部估计，无法单独识别崩盘风险溢价。",

    "Pause and predict. Using Lee's formula":
        "暂停预测。用李的公式，临界矩为二时给出多大的翼斜率？它趋于零、趋于无穷时又如何？",
}

ZH.update({'For q equal to two, the slope is two minus four times root six minus two, about ': 'q等于二时，斜率为二减四乘根号六减二，约0.202。q趋于零时，比率趋于二；q无界增大时，比率趋于零。这些是渐近总方差比率。'})
