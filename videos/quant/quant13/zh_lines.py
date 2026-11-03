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

    'f"This part builds models that let volatility move:':
        "这一部分搭建让波动率动起来的模型：第二条随机的河、跳跃，以及莱维过程。带着一个谜题往下看：把其中五个拟合到同一组比特币期权上，"
        "让五个模型在每个香草期权上都一致。<bookmark mark='p'/>它们还能在什么事情上意见不一吗？<bookmark mark='a'/>"
        "给一份棘轮期权定价，它支付有上限的月度收益之和，因而押注的是未来的波动率。它们的价格相差"
        "{100 * (v.max() - v.min()) / v.mean():.0f}%，而屏幕上没有任何一个期权能裁决。弄明白为什么，就是这一部分的任务。",

    "How we got here. 1973:":
        "我们是怎么走到这里的。1973年：布莱克、斯科尔斯和默顿，一个不变的波动率；1976年：默顿的跳跃。<bookmark mark='m2'/>"
        "然后是1987年10月，那个世界终结的一天。<bookmark mark='m3'/>赫尔和怀特、斯科特和威金斯让波动率变成随机的；"
        "<bookmark mark='m4'/>斯坦因兄弟给了它一个奥恩斯坦–乌伦贝克过程；<bookmark mark='m5'/>赫斯顿找到了闭式解。"
        "<bookmark mark='m6'/>杜皮尔、德曼–卡尼和鲁宾斯坦精确地拟合了微笑。<bookmark mark='m7'/>贝茨加上了跳跃，"
        "<bookmark mark='m8'/>马丹、卡尔和张给方差伽马定价，<bookmark mark='m9'/>2002年带来了SABR、寇的模型和CGMY。"
        "<bookmark mark='m10'/>卡尔和吴联生变换了时钟，Cboe上市了VIX期货；<bookmark mark='m11'/>贝尔戈米让方差曲线成为状态；"
        "<bookmark mark='m12'/>VIX期权上市；<bookmark mark='m13'/>安德森模拟了赫斯顿模型，盖瑟尔提出了标普–VIX问题。"
        "<bookmark mark='m14'/>居永和亨利-拉博代尔用粒子完成校准，<bookmark mark='m15'/>居永解开了联合难题，"
        "<bookmark mark='m16'/>而Terra和FTX让比特币的波动率之河泛滥。",

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

    'f"The two rivers are tied together.':
        "两条河是连在一起的。每个点是一天：横轴是比特币的收益，纵轴是DVOL的变化；白线是到目前为止的最佳拟合。"
        "在比特币下跌超过百分之五的日子里，DVOL平均上升{f['dvol_change_down5']:.0f}%；大涨的日子里它几乎不动。"
        "费希尔·布莱克称之为杠杆效应。<bookmark mark='a'/>2022年的相关系数是{by['2022']:+.2f}。<bookmark mark='b'/>"
        "然后2023年的上涨把点云扭向另一边，{by['2023']:+.2f}，因为看涨期权被抢购。全部{f['n']}天合起来：{f['leverage_corr']:+.2f}。"
        "所以收益只解释了DVOL日变化方差的大约{100 * f['leverage_corr'] ** 2:.0f}%；其余{100 * (1 - f['leverage_corr'] ** 2):.0f}%"
        "是波动率自己的噪声。这正是GARCH与随机波动率的区别：GARCH里明天的方差是今天收益的函数，随机波动率里波动率有自己的布朗运动。"
        "模型既需要这份噪声，也需要这个相关性，而且相关性最好允许变化。",

    'f"Two more facts. Returns themselves have no memory':
        "再看两个事实。收益本身没有记忆：它们的自相关落在灰色带内。<bookmark mark='a'/>收益的大小却有记忆：滞后一天为"
        "{acf_a[0]:.2f}，两个月后仍为正。风暴成群出现，正如第7部分的GARCH所发现的。<bookmark mark='b'/>而且波动率均值回复。"
        "像衡量价格的波动率那样衡量波动率的波动率，<bookmark mark='c'/>再把明天的对数DVOL对今天的做回归：斜率{vf['ar1_phi']:.3f}。"
        "<bookmark mark='d'/>这就是第5部分的奥恩斯坦–乌伦贝克过程：一次冲击大约{hl:.0f}天衰减一半，回到{100 * vf['dvol_mean']:.0f}%附近。",

    'f"Equity markets learned this the hard way.':
        "股票市场是吃了苦头才学会这一点的。1987年10月19日，标普500指数从{c['close_before']:.0f}跌到{c['close']:.0f}，"
        "对数收益为{100 * c['ret']:.1f}%。<bookmark mark='a'/>以前一年的波动率衡量，这是{abs(c['z']):.0f}个标准差，"
        "在正态分布下的概率大约是10的负{abs(c['log10p']):.0f}次方。从那以后，虚值指数看跌期权一直很贵：这就是鲁宾斯坦的偏斜，"
        "以及贝茨发现的被定价的崩盘恐惧。<bookmark mark='b'/>停下来预测一下：比特币今天涨了百分之十。隐含波动率是升还是降？两种情况都发生过。"
        "如果波动率会变，期权价格会怎样？下一章：随机波动率造出微笑。",

    # ------------------------------------------------------------------ Mixing
    "Chapter two. Random volatility makes a smile.": "第2章。随机波动率产生微笑。",

    'f"Why does moving volatility make a smile?':
        "为什么变动的波动率会产生微笑？拿拟合好的赫斯顿模型，关掉相关性。没有波动率的波动率时，三个月后的对数价格就是一个高斯分布，"
        "微笑是平的。<bookmark mark='a'/>让方差动起来。每条细曲线是给定一条方差路径时对数价格的分布：又是高斯分布，方差是这条路径实现的方差。"
        "模型的密度是这一群曲线的平均，橙色的那条。<bookmark mark='b'/>调高波动率的波动率：平静的路径窄，狂野的路径宽，平均起来就有了尖峰和厚尾。"
        "微笑两端都抬起来了。<bookmark mark='p'/>再加倍一次：平值波动率和两翼，哪个变得更多？<bookmark mark='c'/>两翼上升，"
        "从{100 * wing['1']:.0f}%到{100 * wing['2']:.0f}%；平值处下降，从{100 * atm['1']:.1f}到{100 * atm['2']:.1f}。"
        "它是对称的，也必须对称。<bookmark mark='d'/>恢复相关系数，负{abs(m['params'][4]):.2f}：高方差路径伴随下跌，宽的高斯分布向左滑，"
        "微笑倾斜成偏斜。",

    "Now the proof. With no correlation":
        "现在来证明。没有相关性时，价格的布朗运动独立于方差路径，所以给定路径，对数价格服从以积分方差为方差的高斯分布。"
        "<bookmark mark='a'/>由塔性质，价格就是布莱克-斯科尔斯价格对实现方差取平均：赫尔和怀特1987年的定理。<bookmark mark='b'/>"
        "对波动率的波动率展开到二阶：修正项是布莱克-斯科尔斯价格对方差的曲率的一半，乘以实现方差的方差。<bookmark mark='c'/>"
        "这个曲率等于vega乘以d1乘d2再除以sigma：平值处为负，两翼为正。所以两翼升高、中间下降，而且是对称的：这是勒诺和图齐的结论。"
        "<bookmark mark='d'/>有相关性时，把价格的噪声分解成沿着方差噪声的部分和与之正交的部分。<bookmark mark='e'/>"
        "以方差的噪声为条件：价格又是对数正态的，方差更小，现价被因子xi T平移。rho为负时，高方差路径的xi T较小。"
        "这就是罗马诺和图齐的公式：偏斜。",

    'f"The theorem is also an algorithm.':
        "这个定理也是一个算法。模拟拟合模型的{m['N']:,}条方差路径。普通蒙特卡罗还要模拟价格：灰色的误差条。<bookmark mark='a'/>"
        "条件估计量把每条路径平移后的现价和缩小的方差代入布莱克-斯科尔斯公式：误差条窄了大约{ratio:.0f}倍，因为给定路径时价格自身的噪声"
        "已经被精确积分掉了。平值处精确的隐含波动率是{100 * r['cos_iv'][6]:.2f}%，条件估计为{100 * r['cond_iv'][6]:.2f}。"
        "<bookmark mark='b'/>在全部十三个行权价上：{verdict}只要一个模型在给定波动率路径时是高斯的，交易台就会用这种条件蒙特卡罗。"
        "下一章：交易台用得最多的模型——赫斯顿模型，从它的特征函数讲起。",

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

    "Look at the object.":
        "看看这个对象。特征函数把一个频率映射成一个复数，所以把它画在三维空间里。<bookmark mark='a'/>"
        "它从1开始，以漂移的速率旋转，同时收缩；衰减得慢意味着厚尾。<bookmark mark='b'/>三个月的曲线塌缩得更快：分布更宽，变换更窄。",

    'f"Now the trap.':
        "现在来看陷阱。赫斯顿的论文用的是另一个根：g倒过来，e的正d T次方。代数上一样，数值上不一样。看一年期时它对数里面的那个数。"
        "<bookmark mark='a'/>半径被压缩了，角度是真实的：在u等于{cu:.2f}处，它穿过负实轴，也就是对数的分支切割。<bookmark mark='b'/>"
        "在那里计算机的对数跳了2πi；阿尔布雷赫尔等人的“小陷阱”形式保持连续。<bookmark mark='c'/>在我们的拟合上，原始形式从u等于"
        "{fw['fit_1']['u']:.2f}起就是错的，一年期平值看涨期权给出{100 * p1['iv_original'][1]:.0f}%的隐含波动率，"
        "而不是{100 * p1['iv_little'][1]:.0f}%。教科书参数能撑到一年；我们剧烈的拟合撑不住。",

    "f\"The House's implementation: eleven lines":
        "这是公司的实现：十一行，根选对了方向。<bookmark mark='a'/>它把方方和奥斯特莱的基准复现到小数点后"
        "{-np.floor(np.log10(b['err'])):.0f}位，并找到原始形式失效的地方。<bookmark mark='b'/>停一下：给定方差路径，对数价格是正态的吗？"
        "只有rho为零时才是。"
        "下一章：每个参数怎样改变微笑曲线。",

    # ------------------------------------------------------------------ HestonFit
    "Chapter four. What each of Heston's parameters does": "第4章。赫斯顿的每个参数做什么，以及拟合。",

    "Five numbers bend a whole surface.":
        "五个数字弯曲整张曲面。这是拟合好的赫斯顿模型在行权价和期限上的隐含波动率，白色的是曲面的报价。一次只动一个参数。"
        "<bookmark mark='v0'/>今天的方差抬高短端。<bookmark mark='theta'/>长期水平抬高长端。<bookmark mark='kappa'/>"
        "均值回复决定一个变成另一个有多快。<bookmark mark='rho'/>相关系数让每个微笑旋转，偏向看跌或看涨。<bookmark mark='xi'/>"
        "波动率的波动率让每个微笑弯曲，短端最明显。五个旋钮，各司其职；校准器同时设定这五个。",

    'f"Watch it set them.':
        "看它怎么设定。校准器用傅里叶方法给每个报价定价，再让最小二乘优化器找更好的参数；每一次求值都被记录下来。右边是三个起点的损失，"
        "取到目前为止的最好值；左边是三个期限的微笑。<bookmark mark='a'/>从默认起点出发时微笑是平的；优化器先提高波动率的波动率、"
        "倾斜相关系数，再让kappa和xi一起上升，沿着我们将在第16章画出的山谷，到达kappa {r0['x'][1]:.1f}和xi {r0['x'][3]:.1f}。"
        "<bookmark mark='c'/>从{r1['trace']['best'][0]:.0f}和{r2['trace']['best'][0]:.0f}开始的随机起点，最后都停在同一个损失"
        "{r0['rmse']:.3f}。这个损失是价格误差除以vega，是一个快速的替代；隐含波动率误差是{frames[-1]['iv_rmse']:.2f}个点。",

    'f"Expiry by expiry:':
        "逐个期限来看：一个布莱克-斯科尔斯波动率误差为{c['fits']['BS']['rmse']:.1f}个点。<bookmark mark='a'/>赫斯顿为{h['rmse']:.1f}。"
        "<bookmark mark='b'/>代价是：半衰期{365 * np.log(2) / p['kappa']:.0f}天，波动率的波动率{100 * p['xi']:.0f}%，费勒比值"
        "{c['feller']:.2f}，而{days[0]}天的期限仍然差{d3:.1f}个点。",

    'f"Why that limit?':
        "为什么有这个极限？推导短期限的偏斜。当期限趋于零时，对数行权价k处的隐含方差是沿着到k的直线的局部方差平均：这是Berestycki、"
        "Busca和Florent的结果。<bookmark mark='a'/>由久永定理，局部方差是给定价格时方差的期望；短时间内两者都是高斯的，回归斜率是rho xi。"
        "<bookmark mark='b'/>沿直线平均，斜率减半。<bookmark mark='c'/>对平方根求导：偏斜等于rho xi除以四倍根号v0，是一个常数。"
        "<bookmark mark='d'/>在我们的拟合上，公式给出{sl['skew_formula']:.3f}，模型在两天处给出{sl['skew_2d']:.3f}。要匹配陡峭的三天偏斜，"
        "xi必须巨大；曲率随xi平方增长。<bookmark mark='e'/>停一下：让rho为正。短期偏斜翻向看涨一侧，就像2023年的上涨中那样。"
        "价格可以用公式算；对冲和奇异期权需要路径。下一章：诚实地模拟赫斯顿模型。",

    # ------------------------------------------------------------------ Simulate
    "Chapter five. Feller's condition, and simulating": "第5章。费勒条件，以及老老实实地模拟赫斯顿模型。",

    'f"Desks price exotics by simulation.':
        "交易台用模拟给奇异期权定价。所以从一个低水平0.05出发，让拟合的方差走一周，抽十万次。白色的是精确分布，堆在零附近。"
        "<bookmark mark='a'/>欧拉格式加一个高斯冲击：{100 * a['neg']:.0f}%的抽样变成负数。把它们截断在零，均值是{a['mean_euler']:.3f}，"
        "而不是{a['mean_exact']:.3f}，这个偏差会累积。<bookmark mark='b'/>安德森的二次-指数格式在零处放一个点质量，这里是"
        "{a['zero_qe']:.2f}，再加一条指数尾，大小恰好匹配均值和方差：{a['mean_qe']:.3f}。<bookmark mark='c'/>"
        "从高处出发时，QE切换成缩放的高斯平方，几乎完全吻合。",

    'f"Why is this hard?':
        "为什么这很难？在我们的拟合上费勒比值是{fel:.2f}，小于一，所以由第5部分的边界检验，方差会到达零，它的分布在那里有一个尖峰。"
        "<bookmark mark='a'/>用到精确分布的传输距离给每个格式打分，三个起始值、三个步长。<bookmark mark='b'/>QE九次全胜，中位数优势"
        "{ratio:.0f}倍。费勒条件不成立时，它的优势最大。",

    "QE, derived.":
        "推导QE。一步之内，方差的条件均值和条件方差是精确已知的：第5部分的CIR矩。<bookmark mark='a'/>它们的比值psi衡量相对宽度。"
        "<bookmark mark='b'/>psi小时：一个常数乘以平移后的高斯平方。它的均值是a乘以一加b平方，方差是二倍a平方乘以一加二倍b平方；"
        "令它们等于m和s平方并求解，就得到这里的b和a。<bookmark mark='c'/>psi大时：以概率p取零，否则取速率为beta的指数分布。"
        "均值是一减p除以beta，二阶矩是它的两倍再除以beta；匹配得到p和beta。安德森在1.5处切换，两个分支在那里都有效。"
        "<bookmark mark='d'/>对价格，从方差方程解出它的随机积分并代入；只有正交部分需要新的高斯抽样，再用一个常数让价格精确地成为鞅。",

    "In the House: the exact moments, the switch on psi":
        "在公司的代码里：精确矩、按psi切换、两个分支，以及价格步。<bookmark mark='a'/>拿一份三个月平值看涨期权，与精确的傅里叶价格对比，"
        "分别用两步、八步和三十二步。QE一开始就很接近；欧拉格式需要几十步。",

    "Three pointers. Broadie and Kaya":
        "三个延伸。布罗迪和卡亚在2006年精确地模拟了赫斯顿模型：无偏，但慢。<bookmark mark='a'/>崔和郭在2024年用泊松条件化让精确型抽样变快。"
        "<bookmark mark='b'/>安德森和皮特巴格证明，价格的矩可能在有限时间内爆炸，这限制了微笑两翼：与第12部分李氏公式的联系。"
        "下一章：利率和外汇交易台偏爱的模型——SABR。",

    # ------------------------------------------------------------------ SABR
    "Chapter six. SABR: Hagan's formula": "第6章。SABR：哈根公式与骨架。",

    "Rates and FX desks wanted a smile":
        "利率和外汇交易台想要一个可以逐个期限拟合、用几个数字表达的微笑。2002年，哈根、库马尔、莱斯涅夫斯基和伍德沃德给了他们SABR："
        "远期以波动率alpha运动，并取骨架幂次beta，而alpha本身是对数正态的，有波动率的波动率nu和相关系数rho。nu为零时它是常弹性方差模型；"
        "beta也为零时就是巴舍利耶模型。实践中beta按惯例固定，利率常取二分之一，外汇和加密资产取一，其余三个参数拟合。"
        "<bookmark mark='a'/>奇异摄动理论直接给出隐含波动率：大致是沿着通往行权价的最可能路径的波动率，再做时间上的修正。"
        "<bookmark mark='b'/>所有的弯曲都在z除以x(z)里。",

    'f"Term by term:':
        "逐项来看：把x(z)在零附近展开，z除以x(z)等于一，减去rho z的一半，再加一个二次项。<bookmark mark='a'/>因为z等于负nu k除以alpha，"
        "平值斜率是rho nu的一半：偏斜等于相关系数乘以波动率的波动率。<bookmark mark='b'/>曲率正比于nu平方除以alpha。"
        "<bookmark mark='c'/>在平值处是alpha乘以F的beta减一次方：这就是骨架。<bookmark mark='d'/>在51天的切片上，公式的斜率是"
        "{sl['skew_formula']:.3f}。四个看得懂的数字：这就是交易员说SABR的原因。",

    'f"Fit it slice by slice and watch:':
        "逐个切片拟合，并观察：每个期限的微笑从初始猜测移到报价上，它的三个数字落到右边。<bookmark mark='a'/>alpha几乎不动；"
        "rho停在负三分之一附近。<bookmark mark='b'/>但nu稳步下降，在对数坐标上成一条直线：大约是T的{c['sabr_nu_power']:.2f}次方。"
        "逐个切片拟合时，SABR的误差只有{c['sabr_rmse']:.2f}个点，用了{3 * len(c['sabr'])}个数字。一个全局的nu会拟合不足短期偏斜，"
        "和赫斯顿的诊断一样；这个平方根规律是第14部分的线索。",

    "Assemble the nine smiles into a surface.":
        "把九个微笑拼成一张曲面。<bookmark mark='a'/>短端是一道又深又窄的山谷，长端几乎是平的。SABR里没有任何东西把一个切片和下一个连起来："
        "这是每个期限一个模型，而不是关于时间的模型。",

    "Beta is the backbone:":
        "beta是骨架：平值波动率如何随远期变动。beta为一时，微笑随价格滑动。<bookmark mark='a'/>beta为零时，价格上涨波动率就下降，"
        "适合利率。今天的拟合几乎看不到beta；对冲却看得到。在第12部分的检验里，比特币的微笑随价格移动：beta接近一。"
        "这也是哈根写这篇论文的原因：局部波动率预测微笑朝错误的方向移动，它的Delta比布莱克-斯科尔斯还差。"
        "但哈根的公式有一个缺陷。下一章。",

    # ------------------------------------------------------------------ SABRFix
    "Chapter seven. Where SABR's formula breaks": "第7章。SABR公式在哪里失效，交易台又如何修复它。",

    'f"SABR\'s formula is an expansion, and expansions break.':
        "SABR的公式是一个展开式，而展开式会失效。一个类似利率的微笑：远期百分之三，beta二分之一。一年期时隐含密度没问题。"
        "<bookmark mark='a'/>十年期时它在低行权价处为负，积分只有{d10['mass']:.2f}：一个价格为负的蝶式价差，由公式制造。"
        "2010年代利率贴近零时，这是每天的麻烦。<bookmark mark='b'/>公司检查每个切片的套利；真正的修复是直接求解密度本身。",

    "In 2014 the same authors published arbitrage-free SABR":
        "2014年，同一批作者发表了无套利SABR：把波动率从SABR的前向方程里积分掉，精度与旧公式相同，保留一个关于远期密度的方程。"
        "<bookmark mark='a'/>这是一个一维扩散，带有有效局部波动率D，<bookmark mark='b'/>再乘以一个来自相关性的慢变因子E。"
        "<bookmark mark='c'/>到达零的概率质量被吸收并保留，所以账目平衡；扩散的密度不会变负。",

    'f"Solve it forward in time, on':
        "在时间上向前求解，用{p['n']}个网格单元。每条绿色切片是一个期限上的密度，直到十年。<bookmark mark='a'/>驼峰展开并下沉，"
        "零处的紫色柱子长高：到十年时被吸收了{100 * p['QL']:.0f}%。<bookmark mark='b'/>红色的哈根公式在头几年吻合，然后骤降："
        "十年时为负{abs(hmin[-1]):.0f}。<bookmark mark='c'/>偏微分方程让总质量保持为一，精确到小数点后十位，并且始终为正。用它给期权定价："
        "平值处波动率{100 * p['atm_pde']:.1f}%，哈根为{100 * p['atm_hagan']:.1f}%，很接近；但在0.5%的行权价上，"
        "{100 * p['pde_iv'][lo]:.0f}%对哈根的{100 * p['hagan_iv'][lo]:.0f}%。那些过贵的低行权价，正是负密度的镜像。展开式不是分布。",

    "Other repairs: Obłój":
        "其他修复：奥布沃伊在2008年修正了首项。<bookmark mark='a'/>欧元利率转负时，安东诺夫、科尼科夫和斯佩克特用自由边界SABR让利率穿过零。"
        "<bookmark mark='b'/>在交易台上，日常的修复是平移，或者改用正态波动率。",

    "And the hedge. The price is Black's formula":
        "再看对冲。价格是布莱克公式代入SABR的波动率。<bookmark mark='a'/>哈根的Delta在alpha固定时移动远期。<bookmark mark='b'/>"
        "但alpha随远期一起动：它的期望变动是rho nu除以F的beta次方。<bookmark mark='c'/>加上它，就是巴特利特2006年的Delta："
        "rho为负时，看涨期权的Delta更小。第17章会在比特币上检验这个想法。"
        "扩散过程是连续变动的。下一章：会跳的价格。",

    # ------------------------------------------------------------------ Jumps
    "Chapter eight. Jumps: Merton, Kou, and Bates.": "第8章。跳跃：默顿、寇与贝茨。",

    "A diffusion cannot gap.":
        "扩散过程不会跳空。罗伯特·默顿在1976年加入了跳跃，他的模型有一个精确解，最好把它看成一个千层蛋糕。三个月里价格跳零次、一次、两次；"
        "给定次数，对数价格是高斯的。<bookmark mark='a'/>所以分布是一层层高斯分布的叠加，每层按跳跃平移，按泊松概率加权。"
        "<bookmark mark='b'/>提高强度：权重移向跳跃层，左尾变厚，这正是看跌期权买到的崩盘保险。<bookmark mark='c'/>"
        "降低强度，蛋糕塌缩回布莱克和斯科尔斯。",

    "In symbols: the price diffuses, and jumps":
        "用符号写：价格扩散，并在泊松时钟响起时乘以e的J次方；漂移项负lambda k bar让它保持公平。<bookmark mark='a'/>"
        "给定n次跳跃，对数价格是独立高斯变量之和。<bookmark mark='b'/>以n为条件，用布莱克-斯科尔斯定价，按泊松概率加权：这就是默顿级数，"
        "公司的实现与傅里叶定价在小数点后八位一致。<bookmark mark='c'/>独立的因子相乘，所以贝茨1996年的模型就是赫斯顿乘以默顿的跳跃因子。"
        "寇在2002年用双指数跳跃，它无记忆的越界量让障碍期权有闭式价格，这是寇和王的结果。",

    'f"Now fit every model in the part to the same':
        "现在把这一部分的每个模型都拟合到同样的{c['n']}个报价上。一个布莱克-斯科尔斯波动率误差为{c['fits']['BS']['rmse']:.1f}个点。"
        "<bookmark mark='a'/>默顿达到{F['Merton']['rmse_iv']:.1f}，跳跃每年{m['lam']:.2f}次，每次大约下跌{100 * abs(m['mj']):.0f}%。"
        "{shape}它的{d0}天期限仍然差{mv[d0]:.1f}。寇：{F['Kou']['rmse_iv']:.1f}。<bookmark mark='b'/>"
        "赫斯顿：{c['fits']['Heston']['rmse']:.2f}。贝茨：{c['fits']['Bates']['rmse']:.2f}，每年{b['lam']:.0f}次跳跃，"
        "每次{100 * abs(b['mj']):.0f}%。<bookmark mark='c'/>同样的跳跃意味着相反的东西：没有随机波动率时是崩盘；有了它，是第二个扩散。"
        "在这个平静的日子，曲面没有给随机波动率解释不了的崩盘定价。",

    "Rare and huge: crash insurance":
        "稀少而巨大：这是崩盘保险，是常数波动率模型让短期看跌期权变贵的唯一办法。",

    "Frequent and moderate:":
        "频繁而温和：跳跃起到了额外曲率的作用。",

    'f"Watch the Bates fit from three starts:':
        "看贝茨模型从三个起点开始的拟合：损失、跳跃强度、跳跃大小。<bookmark mark='a'/>赫斯顿部分稳定下来时损失下降；然后跳跃参数开始漂移。"
        "{drift}<bookmark mark='b'/>许多小跳看起来和更多的扩散一模一样。停一下：按默顿的强度，一份三天期权到期前不发生跳跃的概率是多少？"
        "大约{100 * np.exp(-lf['fits']['Merton']['params']['lam'] * 3 / 365):.1f}%。短期期权定价的是可能性，而不是频率。",

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

    'f"Another way to make a smile:':
        "产生微笑的另一种办法：保留布朗运动，改变时钟。上面是一条以交易时间为横轴的布朗路径。<bookmark mark='a'/>"
        "下面是一个把日历时间变成交易时间的伽马时钟：它一顿一顿地向前，繁忙时走得快，市场睡着时是平的。<bookmark mark='b'/>"
        "把同一条路径改用日历时间重画。一瞬间流过的交易时间变成一次跳跃；安静的段落变平。完全没有扩散，只有跳跃，大多很小："
        "这是马丹和塞内塔的方差伽马，由马丹、卡尔和张用于期权定价。<bookmark mark='c'/>时钟的随机性就是nu。在曲面上拟合出的nu只有"
        "{nu_fit:.3f}：一个几乎规则的时钟，偏斜来自漂移。",

    "The characteristic function in three lines.":
        "三行推出特征函数。对数价格是一个漂移加一个布朗运动，两者都按伽马时钟运行。<bookmark mark='a'/>给定时钟，它是高斯的。"
        "<bookmark mark='b'/>对时钟取平均：就是伽马分布在复数自变量处的矩母函数。<bookmark mark='c'/>一个漂移修正让远期保持公平。"
        "<bookmark mark='d'/>CGMY推广了跳跃密度，并给出闭式积分。它的Y是精细结构：小于零时跳跃有限多；不超过一时无穷多但可加；"
        "大于一时是无界变差，像扩散一样。<bookmark mark='e'/>卡尔和吴联生把莱维过程放在CIR时钟上：结果又是赫斯顿的仿射公式。"
        "随机波动率就是一个随机时钟。",

    'f"The fine structure, drawn:':
        "把精细结构画出来：三个Y值的跳跃密度，缩放到相同方差，以及各自一年的路径。<bookmark mark='a'/>Y为负二分之一：只有几次跳跃，"
        "大约{cg['-0.5']['lam_eps']:.0f}次。<bookmark mark='b'/>Y为二分之一：一大群，大于千分之一的有{cg['0.5']['lam_eps']:.0f}次。"
        "<bookmark mark='c'/>Y为一点五：{cg['1.5']['lam_eps']:.0f}次，路径看起来像扩散。停一下：一个没有布朗部分的过程能看起来连续吗？"
        "在图上，可以。",

    'f"In the House: the characteristic function with its drift correction':
        "在公司的代码里：带漂移修正的特征函数，以及抽取伽马增量和缩放高斯变量的模拟器。<bookmark mark='a'/>"
        "用两种方法给拟合模型下的三十天平值看涨期权定价。{verdict}",

    "f'The two agree within": "两者在{abs(z):.1f}个标准误差以内一致。",

    "f'They differ by": "两者相差{abs(z):.1f}个标准误差：需要更多路径，或者更细的时钟。",

    'f"Race the pure-jump models on the Surface:':
        "让纯跳跃模型在曲面上赛跑：方差伽马、NIG（巴恩多夫-尼尔森在逆高斯时钟上运行的布朗运动），以及把Y分别限制在一以下和一以上的CGMY。"
        "<bookmark mark='a'/>它们都停在远高于赫斯顿{hes:.1f}的地方。{v1}<bookmark mark='v'/>{v2}<bookmark mark='b'/>"
        "为什么都比不上随机波动率，是下一章的那张图。"
        "下一章：偏斜怎样随期限衰减，逐个模型来看。",

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

    'f"Now the same thing as numbers.':
        "现在用数字说同一件事。把平值偏斜对期限作图，两轴都取对数，这样幂律就是直线，斜率就是幂次。白点是曲面；绿色方块是逐切片拟合的SABR，"
        "按构造跟随白点。<bookmark mark='a'/>在全部九个期限上，市场的斜率是{mkt['all']:.2f}，接近负二分之一。局部来看，两周以内是"
        "{mkt['short']:.2f}，五十天以后是{mkt['long']:.2f}。<bookmark mark='b'/>赫斯顿在短端的斜率是{h['short']:.2f}：平的，"
        "一个常数偏斜；长端是{h['long']:.2f}，均值回复在那里把它压低。方差伽马是{vg['short']:.2f}和{vg['long']:.2f}：在每个期限上都是"
        "一除以期限，这是独立增量的标志；NIG是{ni['short']:.2f}和{ni['long']:.2f}。默顿和寇的跳跃下面有扩散，短端在平值附近是平的，"
        "{me['short']:.2f}和{ko['short']:.2f}。{cgmy_s}<bookmark mark='c'/>{end_s}",

    "f'Only CGMY, with Y of":
        "只有CGMY，Y为{Y:.2f}，一种几乎像扩散一样的无界变差跳跃，在短端接近市场：{cg['short']:.2f}。",

    "f\"CGMY's short-end slope is": "CGMY的短端斜率是{cg['short']:.2f}。",

    "So at the short end the market sits between":
        "所以在短端，市场处于扩散模型和纯跳跃模型之间。这一部分没有任何模型在每个期限上都得到正确的幂次，而大约负二分之一的整体斜率，"
        "正是第14部分的起点。",

    "The market does not sit neatly between":
        "在这里市场并不恰好落在两个家族之间；第14部分会讨论概括它的幂律。",

    'f"Why one over maturity for jumps?':
        "为什么跳跃给出一除以期限？莱维过程有独立同分布的增量，所以每个累积量都与时间成正比。<bookmark mark='a'/>"
        "偏度，即三阶累积量除以方差的二分之三次方，按一除以根号T消失。<bookmark mark='b'/>在格拉姆–沙利耶展开的一阶，"
        "微笑的斜率是偏度除以sigma根号T：一除以T。<bookmark mark='c'/>扩散过程很难很快走远，所以它的偏斜趋于第4章的常数。"
        "<bookmark mark='d'/>停一下：短期偏斜是常数的模型能拟合三天的期限吗？只有靠巨大的波动率的波动率：赫斯顿拟合出的xi是"
        "{c['fits']['Heston']['params']['xi']:.1f}。",

    "Two repairs. Carr, Geman, Madan and Yor":
        "两种修复。卡尔、盖曼、马丹和约尔的可加过程，增量独立但不同分布，修好了莱维模型的期限结构。<bookmark mark='a'/>"
        "阿比·贾贝尔和德卡瓦略证明，均值回复极快的赫斯顿模型会模仿跳跃；第18章会把我们的拟合往那个方向推。"
        "没有一个模型能拟合所有期限。下一章：把随机波动率和局部波动率结合起来。",

    # ------------------------------------------------------------------ SLV
    "Chapter eleven. Stochastic local volatility": "第11章。随机局部波动率，以及粒子方法。",

    "Local volatility fits today exactly and predicts the wrong future; stochastic":
        "局部波动率精确拟合今天，却预测错误的未来；随机波动率正好相反。交易台把两者相乘：赫斯顿的方差，波动率的波动率乘以混合比例eta，"
        "再乘以一个杠杆函数。<bookmark mark='a'/>由久永定理，当杠杆的平方乘以给定价格时方差的期望等于杜皮尔的局部方差时，"
        "它能给每个香草期权重新定价。<bookmark mark='b'/>但这个期望是在模型自己的分布下取的，而分布取决于杠杆："
        "这是一个麦肯–弗拉索夫方程。<bookmark mark='c'/>居永和亨利-拉博代尔2012年的解法：让粒子一起模拟，每一步用核回归在粒子之间估计这个期望。"
        "<bookmark mark='d'/>窗口宽度在偏差和噪声之间权衡，这暗示误差按N的负五分之二次方下降：这是一个经验估计，下面来测量。",

    "Here it runs.":
        "这就是它运行的样子。每个点是一个粒子，一个对数价格和一个方差，它们一起出发。<bookmark mark='a'/>每一步，金色曲线是给定价格时方差期望的"
        "核估计；右边是它推出的杠杆；然后每个粒子用它所在价格处的杠杆走一步。<bookmark mark='b'/>点云散开并倾斜：相关性为负时，"
        "下跌的粒子带着高方差。点云对市场的局部波动率来说太狂野的地方，杠杆降到一以下；太平静的地方，杠杆抬高它。模型一边模拟一边校准自己。",

    "Stack the leverage every ten days":
        "把每十天的杠杆叠成一张关于价格和时间的曲面。<bookmark mark='a'/>平值附近低于一，两翼升高，短期最陡，"
        "随着随机方差承担更多负载而趋向于一。",

    'f"The step itself, eleven lines:':
        "这一步本身，十一行：一个子样本、西尔弗曼带宽、核权重、一次矩阵乘法得到条件方差、杠杆，以及每个粒子的欧拉步。<bookmark mark='a'/>"
        "四万个粒子，一百二十天：模型把曲面的微笑重新定价到三十天时{rep[0]['err']:.2f}个波动率点、一百二十天时{rep[-1]['err']:.2f}，"
        "剩下的是蒙特卡罗噪声和局部波动率中的有限差分误差。",

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

    "The rival is the PDE route":
        "它的对手是任、马丹和钱以及利普顿的偏微分方程路线：在网格上求解联合密度。<bookmark mark='a'/>理论是最近才有的："
        "赖辛格和齐亚尼在2025年证明这个粒子系统收敛，速率为二分之一。<bookmark mark='b'/>停一下：把波动率的波动率设为零。"
        "杠杆就是局部波动率除以确定性的根号方差：局部波动率。下一章转动这个旋钮。",

    # ------------------------------------------------------------------ MixFrac
    "Chapter twelve. The mixing fraction": "第12章。混合比例：两个世界之间的一个旋钮。",

    'f"The mixing fraction, eta, is the share':
        "混合比例eta，是模型保留的赫斯顿波动率的波动率的份额。eta为零时，方差是确定的，杠杆承担一切：这就是用粒子运行的局部波动率。"
        "eta为一时，是赫斯顿完整的波动率的波动率，杠杆只做修正。在五个设定下运行粒子方法，每个四万个粒子，观察三样东西：六十天时的杠杆、"
        "六十天后的三十天微笑，以及本部分开头那份棘轮期权的价格。<bookmark mark='a'/>把旋钮调高。杠杆趋向于一，因为更多的波动率来自随机方差。"
        "远期微笑离开局部波动率的平坦形状而变陡：偏斜从{100 * sks[0]:.1f}个点变到{100 * sks[-1]:.1f}。{v1}<bookmark mark='b'/>"
        "再看下面的香草期权重新定价误差。{v0}<bookmark mark='c'/>{v2}",

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

    "Why does a dial that vanillas cannot see":
        "为什么一个香草期权看不到的旋钮会改变奇异期权？对每个eta，杠杆都会重新计算以满足久永条件：每个设定都是边际分布相同的不同模型。"
        "<bookmark mark='a'/>eta为零时没有波动率的波动率，模型就是局部波动率。<bookmark mark='b'/>未来某个日期的微笑偏斜来自那时价格与波动率的协方差，"
        "按第2章的论证，它与模型保留的波动率的波动率成比例。<bookmark mark='c'/>所以一阶近似下，任何押注未来微笑的东西，远期起始期权、棘轮期权，"
        "都随eta单调变化。停下来预测一下：一年期欧式期权、远期起始期权和棘轮期权，哪个对eta最敏感？欧式期权完全不敏感：它是香草期权。"
        "远期起始期权和棘轮期权都敏感。",

    "So how does a desk set the dial?":
        "那么交易台怎么设定这个旋钮？不能靠香草期权：它们看不到。外汇交易台广泛使用这个模型，它们用银行间本身有报价的奇异期权，"
        "障碍期权和无触碰期权，来设定它，伊恩·克拉克的教科书描述了这种做法。<bookmark mark='a'/>粒子方法让这变得可行："
        "旋钮的任何设定都能在一次模拟中校准到香草期权。然后其余的奇异期权在两者之间定价。在加密市场，流动的奇异期权很少，"
        "旋钮是一个建模选择，它的范围就是模型风险。"
        "下一章：模型的另一种状态变量——远期方差。",

    # ------------------------------------------------------------------ Bergomi
    "Chapter thirteen. Bergomi's models": "第13章。贝尔戈米的模型：以远期方差为状态。",

    'f"A variance swap\'s strike times its maturity':
        "方差互换的执行价乘以期限，是截至那一天被定价的总方差；它的斜率是远期方差，在相邻到期日之间为常数。<bookmark mark='a'/>"
        "注意那个凹陷：13日星期六和14日星期日的到期日夹住一个周末的日子，定价为{100 * fv[sat]:.0f}%，两边都在百分之五十左右。"
        "过去两年比特币的星期六实现了{100 * b['by_dow'][5]:.0f}%，工作日为{100 * np.mean(b['by_dow'][:5]):.0f}%。"
        "<bookmark mark='b'/>赫斯顿的曲线是一条指数曲线：它不能为周末下凹。",

    "Lorenzo Bergomi turned this around:":
        "洛伦佐·贝尔戈米把这件事反过来做：让整条曲线成为状态，今天的曲线直接取自市场。每一点是那个日期方差的期望，所以是一个鞅："
        "一份远期方差互换的费率。<bookmark mark='a'/>在他的两因子模型里，每一点都对数正态地运动，由一快一慢两个奥恩斯坦–乌伦贝克因子驱动，"
        "影响随距离衰减。<bookmark mark='b'/>积分之后：今天的曲线乘以一个对数正态鞅。<bookmark mark='c'/>由伊藤公式，每一点的波动率只取决于它的距离tau："
        "一个波动率的波动率的期限结构，与今天的曲线无关。<bookmark mark='d'/>赫斯顿的每一点都由同一个冲击乘以e的负kappa tau次方驱动，"
        "而同一个kappa还决定今天曲线的形状：一个数字，两份工作。",

    'f"Let it move.':
        "让它动起来。从曲面的曲线出发，把贝尔戈米模型逐日模拟四个月；每天加一条切片，向前三百天。<bookmark mark='a'/>前端剧烈摆动，"
        "远端几乎不动，周末凹陷漂移过来又过去。omega的设定让模型的三十天指数像DVOL一样波动。<bookmark mark='b'/>对两千条路径取平均，"
        "曲线与起点相差不超过{100 * dev:.1f}%：一个鞅。<bookmark mark='c'/>赫斯顿的曲线作为一条指数曲线运动，而kappa接近十五时，"
        "几周以外的部分根本不动。",

    'f"One plot says it:':
        "一张图就说清楚了：曲线上每一点的波动率，对它的距离作图。<bookmark mark='a'/>贝尔戈米的在几周内下降，然后趋平：三个月外为"
        "{100 * bs['volvol_bergomi'][i90]:.0f}%。<bookmark mark='b'/>赫斯顿的起点高得多，几周内就消失：三个月时为"
        "{100 * bs['volvol_heston'][i90]:.0f}%。贝尔戈米的第一篇《微笑动态》论文正是这个观点：在赫斯顿模型里，一个kappa同时固定了"
        "波动率的波动率的期限结构、远期偏斜和现价–波动率相关性，它们无法分开设定。棘轮期权押注的正是这条曲线。<bookmark mark='c'/>"
        "停一下：一年期方差互换和一周期方差互换，谁的费率更动荡？一周期的。",

    'f"One more dynamic:':
        "再看一个动态性质：偏斜粘性比，即对数价格每变动一个单位，平值波动率变动多少，以偏斜为单位。<bookmark mark='a'/>"
        "在赫斯顿模型里，方差的期望变动是每单位对数价格rho xi；<bookmark mark='b'/>平值波动率是根号v，所以它变动rho xi除以二倍根号v。"
        "<bookmark mark='c'/>除以第4章的偏斜：R等于二，和局部波动率一样。<bookmark mark='d'/>在我们的拟合上精确计算：两天时{r2['R']:.2f}，"
        "一年时降到{r365['R']:.2f}。短期内，随机波动率和局部波动率对微笑如何移动意见一致；再远就分道扬镳。"
        "模型之间的分歧在远期微笑上。下一章：远期微笑与棘轮期权。",

    # ------------------------------------------------------------------ Forward
    "Chapter fourteen. Forward smiles, and cliquets.": "第14章。远期微笑与棘轮期权。",

    'f"A forward smile is the smile a model predicts':
        "远期微笑是模型对未来某个日期预测的微笑：这里是六十天后的三十天微笑。没有市场报它的价；远期起始期权和棘轮期权按它支付。"
        "对赫斯顿模型可以用两种方法计算。白色的是一个一维积分，稍后推导。<bookmark mark='a'/>点是蒙特卡罗：九十天路径中最后一个月的收益。"
        "五百条路径时它们很分散；随着路径累积，它们稳定下来。<bookmark mark='b'/>{verdict}",

    "f'The three seeds average to within":
        "三个种子的平均在每个行权价上都与积分相差不到{dev:.1f}个波动率点，落在它们自己{spread:.1f}的离散范围内：模拟与公式一致。",

    'f"The seeds\' average misses the integral by up to':
        "种子的平均与积分最多相差{dev:.1f}个点，超过它们{spread:.1f}的离散范围：模拟有离散化偏差。",

    'f"Ask every fitted model the same question.':
        "问每个拟合好的模型同一个问题。<bookmark mark='a'/>正如第12部分所示，局部波动率把远期微笑压平：偏斜{100 * lv['fwd_skew']:.1f}个点，"
        "今天是{100 * e['today_skew']:.1f}。未来日期的局部波动率只是价格的函数，而远处的局部偏斜是平的。<bookmark mark='b'/>"
        "赫斯顿保持{100 * he['fwd_skew']:.1f}个点，贝茨{100 * e['models']['Bates']['fwd_skew']:.1f}：无论从何时开始，它们的方差都是随机的。"
        "方差伽马重复今天的微笑，{100 * vg['fwd_skew']:.1f}，随机局部波动率处在旋钮指定的位置，{100 * e['models']['SLV']['fwd_skew']:.1f}。"
        "同一组香草期权，五个未来。",

    "Why. A forward-start payoff ignores":
        "为什么？远期起始期权的收益不关心第一个日期的价格水平，所以到那时它就是现价为一的普通期权，价值是模型在当时状态下的价格。"
        "<bookmark mark='a'/>在莱维模型里状态无关紧要：远期微笑就是今天的微笑。<bookmark mark='b'/>在赫斯顿模型里状态是方差："
        "把赫斯顿价格对第一个日期方差的卡方分布取平均，就是白色曲线。那时方差高意味着远期微笑高而平，方差低则低而陡；"
        "对这种离散取平均，正是赫斯顿的远期微笑保持曲率的原因。<bookmark mark='c'/>棘轮期权是一串这样的期权：每个票息是一个下限加一个远期起始看涨价差。"
        "<bookmark mark='d'/>停一下：在哪里远期起始期权恰好等于今天的期权？在每个指数莱维模型里。",

    "The cliquet on three simulated paths:":
        "三条模拟路径上的棘轮期权：每个灰色轮廓是一个月的收益。<bookmark mark='a'/>每个月下限为零、上限为百分之十，收益是它们的和。"
        "<bookmark mark='b'/>所以它的价值取决于未来每个月的波动率和偏斜：远期微笑。今天的香草期权只固定到每个日期的总收益，"
        "而不固定它在各月之间如何分配。",

    'f"Price two such exotics.':
        "给两个这样的奇异期权定价。棘轮期权在五个模型下的价格在名义本金的{100 * v1.min():.1f}%到{100 * v1.max():.1f}%之间："
        "相差{100 * (v1.max() - v1.min()) / v1.mean():.0f}%。<bookmark mark='a'/>六十天后按平值起始的远期起始期权：相差"
        "{100 * (v2.max() - v2.min()) / v2.mean():.0f}%，局部波动率最贵。<bookmark mark='b'/>没有香草期权能解决这个问题。"
        "这个差距就是模型风险，诚实的交易台会报告它。"
        "下一章：最难的联合检验——SPX/VIX难题，在比特币上测量。",

    # ------------------------------------------------------------------ Puzzle
    "Chapter fifteen. The S&P–VIX puzzle": "第15章。标普–VIX难题，在比特币上测量。",

    "A harder test. In 2004 Cboe listed futures":
        "一个更难的检验。2004年Cboe上市了VIX期货，VIX是标普500的三十天波动率指数，2006年又上市了它的期权：波动率有了自己的微笑，"
        "而拟合到标普期权的模型会预测它。<bookmark mark='a'/>盖瑟尔在2008年证明，两个方差因子只能近似地同时拟合两者。<bookmark mark='b'/>"
        "2020年，居永把难题说得很尖锐：在连续模型里，陡峭的短期标普偏斜需要很大的波动率的波动率，这会让模型的平值VIX隐含波动率过高。"
        "孔特和科克霍尔姆曾用跳跃把两者解耦；居永用非参数方法解决了它；第14部分讨论解法。这里我们在比特币上测量这个难题。",

    'f"The fitted Heston has its own thirty-day index:':
        "拟合好的赫斯顿模型有它自己的三十天指数：未来一个月方差期望的平方根。把它模拟四年，放在真实的DVOL旁边。<bookmark mark='a'/>"
        "模型的河狂野得多，每当方差触及零就掉到一个下限。<bookmark mark='b'/>它的日变化宽了大约{r_:.1f}倍：波动率的波动率为"
        "{100 * h['volvol_median']:.0f}%，DVOL为{100 * vp['dvol_volvol']:.0f}%。倾斜方向是对的，相关系数{h['corr_median']:+.2f}，"
        "对比{vp['dvol_corr']:+.2f}；大小却不对。这就是比特币上的居永难题。",

    "Why it is the same puzzle.":
        "为什么这是同一个难题。赫斯顿的指数平方是远期方差曲线在三十天上的平均：对方差是仿射的。<bookmark mark='a'/>平方根是凹的，"
        "所以由詹森不等式，VIX期货最多等于远期方差互换波动率，而后者由香草期权微笑固定。<bookmark mark='b'/>差距大约是指数的方差除以"
        "两倍均值：VIX期货和期权给波动率的波动率定价。<bookmark mark='c'/>而由吉尔萨诺夫定理，测度变换只改变漂移，不改变扩散系数，"
        "所以在定价测度下拟合的波动率的波动率可以用历史来检验。",

    'f"Jensen\'s gap, drawn:':
        "把詹森缺口画出来：平方根，以及三十天后指数平方可能的位置。<bookmark mark='a'/>方差互换波动率是{100 * vs:.1f}%；"
        "公平的期货更低，{100 * fut:.1f}%。<bookmark mark='b'/>还有一个下限：方差为零时，指数也不能低于{100 * h['floor']:.0f}%。"
        "停一下：VIX期货能交易在方差互换波动率之上吗？永远不能。",

    'f"Price options on the model\'s index:':
        "给模型指数上的期权定价：三十天平值隐含波动率{100 * a30:.0f}%，九十天{100 * a90:.0f}%，微笑向上倾斜，和VIX期权一样。"
        "<bookmark mark='a'/>{verdict}<bookmark mark='b'/>一个提醒：这是在定价测度下拟合的波动率的波动率，对比的是DVOL的历史。"
        "在模型内部这是合理的；在真实世界里，差距中还包含波动率风险溢价。无论如何，方向和居永说的一样。"
        "这里的每个结果都取决于校准。下一章：校准的山谷与不稳定性。",

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

    'f"Make the valley precise.':
        "把山谷说精确。损失在最小值处的曲率是黑塞矩阵；在这两个参数上，其余参数重新优化后，它有两个特征向量。<bookmark mark='a'/>"
        "白色的沿着山谷：曲率小。红色的横穿山谷：曲率是它的{hs['profile_cond']:.0f}倍。数据确定了红色方向，几乎确定不了白色方向。",

    'f"In symbols: least squares, with the Gauss–Newton Hessian':
        "用符号写：最小二乘，高斯–牛顿黑塞矩阵J转置乘J。<bookmark mark='a'/>在最优点附近损失是一个碗；小特征值是一个平坦方向，"
        "一个数据几乎确定不了的组合。<bookmark mark='b'/>线性化后，参数的协方差是噪声水平乘以黑塞矩阵的逆。我们的特征值跨越"
        "{hs['cond']:.0f}倍；仅凭一天的报价，kappa的不确定性大约是{100 * se[1]:.0f}%。<bookmark mark='c'/>"
        "解药是更多信息：向上周的参数拉。每个特征值都增加lambda，平坦方向变硬；孔特和坦科夫为跳跃模型提出了相对熵版本。",

    'f"Recalibrate Heston every Wednesday for two years':
        "两年里每个星期三重新校准赫斯顿，看看这些常数。均值回复，模型里世界的一个固定属性，在典型的一周里变动四分之一，"
        "并有{100 * kb:.0f}%的周停在上界。<bookmark mark='a'/>波动率的波动率在一到六之间摆动；费勒条件在{100 * fe:.0f}%的周里不成立。"
        "<bookmark mark='b'/>相关系数在{100 * rp:.0f}%的周里为正：这些周里大多数时候比特币的微笑在看涨一侧更贵。<bookmark mark='c'/>"
        "每周都变的常数让模型变成插值工具：报香草期权没问题，用于对冲和奇异期权就危险了。",

    'f"Now replay the hundred weekly fits':
        "现在把一百次周度拟合回放成在谷底上的一次漫步。每个星期三校准器把赫斯顿重新拟合到那天早上的曲面，黄点跳到新的均值回复和波动率的波动率。"
        "<bookmark mark='a'/>它在两个数量级的范围内游荡，从接近零的均值回复到上界二十，而且主要沿着一条对角线：kappa上升时xi也跟着上升，"
        "对数的相关系数为{corr:+.2f}。右边的拟合误差几乎没有反应。模型周复一周地沿着山谷走，因为单张曲面里没有任何东西告诉它该站在哪里。",

    'f"So regularise.':
        "所以要正则化。这是公司的版本：拟合的残差，再叠加一个向上周参数的拉力，每个参数按相对变化衡量，用lambda加权。十行。"
        "<bookmark mark='a'/>用两种拉力强度把一百周全部重跑一遍，每次运行画成一个点：参数在典型的一周里移动多少，对比模型拟合得多好。"
        "<bookmark mark='b'/>{verdict}<bookmark mark='c'/>这就是交易台做的交换：牺牲一点拟合，换来下周意义不变的参数，以及不会突然跳动的对冲。"
        "停下来预测一下：一夜之间kappa从三跳到二十，拟合几乎没变。哪些价格变了？香草期权几乎不变。远期起始期权、棘轮期权和每个对冲比率，变化很大。"
        "下一章：谁构建这些模型，交易台怎样评判它们。",

    "f'The strongest pull cuts the typical weekly change":
        "最强的拉力把典型的周度变化缩小了{cut:.0f}倍，代价是中位拟合误差增加{cost:.2f}个波动率点。",

    "f'Even the strongest pull cuts the weekly change only":
        "即使最强的拉力也只把周度变化缩小了{cut:.1f}倍，代价是{cost:.2f}个波动率点的拟合：不稳定不只是噪声。",

    # ------------------------------------------------------------------ Industry
    "Chapter seventeen. The industry:": "第17章。业界：谁在建这些模型，交易台如何评判一个模型。",

    "Who builds these models? To a remarkable degree, one group.":
        "谁在建这些模型？在很大程度上，是同一个团队。在法国兴业银行，股票衍生品量化研究主管洛伦佐·贝尔戈米写了《微笑动态》系列论文，"
        "获评《Risk》杂志2009年度量化人物。朱利安·居永和皮埃尔·亨利-拉博代尔在那里发展了粒子方法。亨利-拉博代尔在2013年和2023年获得该奖；"
        "居永在2025年的颁奖中获奖，表彰他与斯坎德·穆斯塔法合作的神经网络标普–VIX联合校准。这类银行卖出的棘轮期权和自动赎回产品，"
        "正是依赖微笑动态的合约。<bookmark mark='a'/>交易所则把波动率变成了资产：Cboe的VIX期货和期权，以及比特币上Deribit的DVOL。",

    "How does a desk judge a model?":
        "交易台如何评判一个模型？不看拟合：这里每个模型都能拟合。看对冲。最干净的检验是最小方差Delta：把期权的变化对现价的变化做回归。"
        "<bookmark mark='a'/>一阶近似下，期权随现价和隐含波动率变动。<bookmark mark='b'/>所以最好的Delta是布莱克-斯科尔斯的Delta，"
        "加上vega乘以每单位现价变动对应的波动率期望变动：赫尔和怀特，2017年。<bookmark mark='c'/>在赫斯顿模型里那就是rho xi，"
        "又是巴特利特的思想。<bookmark mark='d'/>停一下：价格下跌时波动率上升。持有看涨期权时，应该比布莱克-斯科尔斯说的持有更多还是更少的标的？"
        "更少：波动率上升缓冲了下跌。",

    'f"Test it on Bitcoin.':
        "在比特币上检验。从2021到2025年，每天一份按DVOL定价的三十天平值看涨期权对冲一天，分别用布莱克-斯科尔斯的Delta和最小方差Delta，"
        "beta来自DVOL变化对收益的回归；把平方误差加起来。最小方差Delta平均为{rc['mean_mv']:.2f}，对比{rc['mean_bs']:.2f}。"
        "<bookmark mark='a'/>{v_fix}<bookmark mark='b'/>{v_roll}<bookmark mark='c'/>动态对对冲很重要，而在比特币上它们并不稳定。"
        "这是描述性的对冲，不是策略：试验计数器不变。",

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

    'f"Now where the truth is known:':
        "现在换到真相已知的地方：在拟合的赫斯顿模型内部，两千个模拟的月份，一份看涨期权每天用三种方法对冲。<bookmark mark='a'/>{v}"
        "<bookmark mark='b'/>{v2}三种方法都留下了大部分风险：不对冲时{hh['unhedged_sd']:.3f}，对冲后大约{hh['MV']['sd']:.3f}。"
        "剩下的是vega风险，没有任何Delta能消除；交易台也对冲vega，就像第11部分那样。",

    'f"The minimum-variance delta is best, but only by':
        "最小方差Delta最好，但只比按期权自身隐含波动率计算的布莱克-斯科尔斯Delta好{gap:.1f}%。",

    "f'Here the": "这里{best}的Delta最好；最小方差Delta没有胜出。",

    "Heston's own delta, which holds the variance fixed":
        "赫斯顿自己的Delta保持方差不变，是三者中最差的：它忽略了模型本身预测的、与价格相关的波动率变动。",

    "Heston's own delta is not the worst here.": "这里赫斯顿自己的Delta不是最差的。",

    "The published horse races agree.":
        "已发表的比赛结果一致。巴克希、曹和陈在1997年发现，在标普期权上，带跳跃的随机波动率定价最好，但单纯的随机波动率对冲得一样好。"
        "<bookmark mark='a'/>在比特币上，马蒂奇、帕克姆和哈德勒发现跳跃很少，而且对较长期的期权，在随机波动率下用多种工具对冲能降低尾部风险。"
        "<bookmark mark='b'/>监管者则把分歧放到资产负债表上：按照欧洲的审慎估值规则，要根据合理模型的范围计提模型风险调整，置信度百分之九十。"
        "第14章的棘轮期权价差就是这样一个范围；第15部分把它变成准备金。",

    "The House's volatility desk now runs all of this.":
        "公司的波动率交易台现在运行这一切。<bookmark mark='a'/>每个模型的特征函数，都检查过鞅性质；与基准和默顿级数对上的傅里叶定价；"
        "记录路径、能固定参数、能正则化的校准器；无套利SABR；模拟器、粒子、波动率指数、远期微笑，以及最小方差对冲。每一项都有测试。"
        "最后，前沿。",

    # ------------------------------------------------------------------ Frontier
    "Chapter eighteen. The frontier, 2023 to 2026.": "第18章。前沿，2023到2026年。",

    'f"Start with one computed tie-in.':
        "先看一个计算出来的联系。爱德华多·阿比·贾贝尔和内森·德卡瓦略在2023年证明，均值回复趋于无穷、波动率的波动率随之放大的赫斯顿模型，"
        "会收敛到正态逆高斯型的跳跃过程，或类似粗糙的极限：这就是回复型赫斯顿模型。所以把kappa固定在十五、三十、六十和一百二十，"
        "把另外四个参数重新拟合到曲面上。<bookmark mark='p'/>停下来预测一下：要保持短期偏斜，xi必须怎么变？<bookmark mark='a'/>{v1}"
        "<bookmark mark='b'/>{v2}我们拟合的赫斯顿模型，kappa为十五，已经在这条路上走了一段：一个费力模仿跳跃的扩散。",

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

    "Five papers from the last three years.":
        "过去三年的五篇论文。阿比·贾贝尔、伊朗和李的五次奥恩斯坦–乌伦贝克模型，让波动率成为一个快速因子的五次多项式。于是VIX的平方是"
        "一个高斯变量的多项式，VIX期权很容易定价，标普和VIX微笑用六个有效参数一起拟合，而且不需要粗糙性：这是对第15章的一个马尔可夫式回答。"
        "<bookmark mark='a'/>居永和穆斯塔法用一个单因子随机局部波动率模型在买卖价差内同时拟合两个市场，它的漂移和扩散是神经网络，"
        "直接通过模拟本身训练。<bookmark mark='b'/>崔和郭通过对一个泊松变量取条件，让精确的赫斯顿模拟变快，去掉了布罗迪和卡亚方法中缓慢的贝塞尔抽样。"
        "<bookmark mark='c'/>赖辛格和齐亚尼给第11章的粒子方法建立了收敛理论。<bookmark mark='d'/>今年，王和合作者报告了一个神经算子，"
        "一次给出整个局部-随机波动率校准，从大约一百毫秒降到不到一毫秒，奇异期权价格与粒子方法接近，这是在合成数据上的测试。"
        "第14部分讨论粗糙波动率和联合校准；第17部分讨论神经校准器和深度对冲。",

    # ------------------------------------------------------------------ Outro
    "Part thirteen in ten lines.":
        "第13部分的十句话。波动率会动，随机波动率产生微笑，相关性让它倾斜。赫斯顿的第二条河有闭式特征函数，只要注意分支切割，"
        "但它只靠剧烈的波动率的波动率才能拟合曲面。安德森的格式通过匹配矩来模拟它。SABR用四个数字读出微笑，无套利SABR修好了它的密度。"
        "跳跃和莱维过程是时钟；它们的偏斜像一除以期限那样爆炸，而扩散保持平坦，市场处在两者之间。随机局部波动率精确拟合今天，"
        "并用一个旋钮选择明天。在每个香草期权上一致的模型在奇异期权上意见不一，因为它们对未来的微笑意见不一。微笑要求的波动率的波动率，"
        "比波动率实际拥有的更多。而校准是一个反问题：要正则化，并用对冲来评判模型。",

    "Three desk questions.":
        "三个交易台问题。在赫斯顿模型里，相关系数决定偏斜，波动率的波动率决定曲率。<bookmark mark='a'/>给棘轮期权定价，绝不能只信局部波动率："
        "它压平了棘轮期权所押注的未来微笑。<bookmark mark='b'/>VIX期货永远不能交易在方差互换波动率之上：平方根是凹的，"
        "差距就是波动率的波动率的价格。完整解答在讲义里。",

    "And seven problems:":
        "还有七道习题：赫斯顿的里卡蒂方程、它的短期偏斜、莱维模型的远期微笑、费勒条件、杠杆函数为什么有效、默顿级数，以及方差伽马的特征函数。"
        "中英文解答都在讲义里。",

    "Where this comes back.":
        "这些内容会在哪里再出现。平方根规律是第14部分的起点。第15部分在这些模型之间给结构化产品定价。第16部分让定价变快，"
        "第17部分训练网络在几微秒内完成校准。同样的想法会在利率中再次出现，跳到零就变成信用，而外汇交易台每天都在运行随机局部波动率。",

    "The textbook chapters this part covers, and the papers it draws on, from":
        "本部分涵盖的教科书章节，以及它引用的论文，从默顿的跳跃到今年的神经算子。数据是曲面和一百个由Deribit成交重建的周度曲面、"
        "币安的比特币价格、Deribit的DVOL，以及1987年的标普500。",

    'f"The volatility desk can now fit, simulate and compare':
        "波动率交易台现在能拟合、模拟并比较波动率变动的模型，它还新增一条规则。第十三条规则：交易台用的每个模型都由校准器拟合，"
        "校准器记录误差，以及参数自上周以来移动了多远。每个奇异期权至少用两个拟合到同一曲面的模型定价，差距作为模型风险报告。"
        "这一部分没有检验任何策略，所以试验计数器仍为{env['trials']}。<bookmark mark='a'/>下一部分，第14部分：粗糙与路径依赖波动率。"
        "偏斜为什么遵循平方根规律，波动率是粗糙的意味着什么，以及关于它是否粗糙的争论。",
}
