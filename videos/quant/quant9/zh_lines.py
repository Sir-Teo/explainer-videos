"""Chinese narration for quant9: see tools/zh_lines.py (literal lines by prefix, computed lines as templates).
Terms follow videos/quant/QUANT_ZH_GUIDE.md."""

TITLE = '量化金融，从零搭建 · 第9部分：无套利'

CHAPTERS = {
    'Hook': '同一个价格，以及我们怎样走到这里',
    'Parity': '1. 平价关系，亲手拼出来',
    'Breaks': '2. 平价在哪里失效',
    'Geometry': '3. 套利的几何',
    'FTAP': '4. 基本定理：证明与求解',
    'StatePrices': '5. 状态价格、贴现因子与Q',
    'Tree': '6. 二叉树：先复制，再倒推',
    'Incomplete': '7. 不完备市场：区间即线性规划',
    'Completing': '8. 让市场完备；跨时间的超复制',
    'Continuous': '9. 连续时间：吉尔萨诺夫即重新加权',
    'FreeLunch': '10. 免费午餐、加倍策略与泡沫',
    'Numeraire': '11. 计价单位变换',
    'Density': '12. 蝶式价差拼出密度',
    'DensitySurface': '13. 曲面上的密度',
    'Ross': '14. 罗斯复原及其批评',
    'MOT': '15. 不依赖模型的界',
    'MOTConverge': '16. 有限网格界与数值敏感性',
    'Industry': '17. 套利怎样做，为什么受限',
    'Frontier': '18. 研究前沿，2023—2026',
    'Research': '写给研究者：有摩擦时的套利',
    'Outro': '套利检查器、回顾、交易台问题与习题',
}

ZH = {
    'Part nine. No arbitrage. The derivatives act begins':
        '第9部分。无套利。衍生品篇从一个想法开始，期权定价的其余一切都由它推出：得到同一收益的两种方法，必须花同样的钱。',
    'A desk interview question. A call costs ten':
        "一道交易台面试题。一份看涨期权10元，一份看跌期权7元，行权价都是100，到期日相同。股价103，利率为零。有套利吗？<bookmark mark='a'/>买入看涨、卖出看跌：到期时无论发生什么，你都得到股价减100。这就是一份远期，所以两者必须同价：这就是看涨看跌平价，汉斯·斯托尔在1969年写下了它。<bookmark mark='b'/>两边都是3：没有平价套利。如果看跌期权是6元，你就能白白锁定1元。这只在无摩擦且结算匹配的假设下证明该平价关系一致，并不认证所有可能的市场交易。",
    'f"Parity also lets us compare observed prices. On Deribit, inverse Bitcoin optio':
        "平价也能比较观测价格。在BTC贴现因子为一时，Deribit反向比特币期权满足图中的平价。相同执行价与到期日的看涨、看跌成交在十分钟内配对。<bookmark mark='a'/>曲面当天有{p['n_pairs']}对，一半距该到期日的隐含远期中位数不超过{p['trade_p50']:.1f}基点。这些是异步观测，不是同时买卖价的套利检验。<bookmark mark='b'/>观测年化远期基差约从百分之三升至五，反映持有成本与市场条件。本部分结合已有市场观测、固定种子的数值例子，以及单独引用的文献事实，没有注册新的策略试验。",
    'How we got here. In 1902 Gyula Farkas':
        "我们怎样走到这里。1902年，法卡斯·久拉证明了一个关于线性不等式的引理，它就是单期中的整个定理。<bookmark mark='a'/>阿罗在1964年为状态证券定价，斯托尔在1969年写下平价，罗斯在1976年证明期权让市场完备。<bookmark mark='b'/>然后是理论：1979年的二叉树与哈里森和克雷普斯，1981年的哈里森和普利斯卡，1994年的德尔班和沙赫迈尔。<bookmark mark='c'/>还有前沿与失败：1998年不依赖模型的界和长期资本管理公司的倒下，2013年的鞅最优传输，2015年的罗斯复原，以及2021年的游戏驿站。",
    'A question to hold on to.':
        "先记住一个问题。要发现交易台问题里的套利，你需要对股票做任何预测吗？<bookmark mark='a'/>不需要：只要今天的价格。这就是本部分的精神：仅凭价格，不对未来建任何模型，能说出什么。",
    'The plan: parity, checked against Bitcoin futures':
        '本部分的安排：平价关系，用比特币期货检验，以及它在哪里失效；基本定理，在三维中看见、证明，再用单纯形法求解；状态价格与Q；二叉树；不完备市场；连续时间；计价单位变换；期权价格里的密度；罗斯复原；不依赖模型的界；以及业界怎样做这一切。',
    "In the House, this part builds the arbitrage checker. <bookmark mark='a'/> It di":
        "本部分为House搭建套利检查器。<bookmark mark='a'/>它在明确假设下诊断平价与形状不一致。曲面的拟合、修复和检查需要迭代；抽样诊断不能认证整个市场没有可执行套利。",
    'Chapter one. Parity, assembled.':
        '第1章。平价关系，亲手拼出来。',
    'A definition first. An arbitrage costs nothing':
        "先给定义。套利就是今天不花钱或者花得更少、永远不会亏、有时还会赚的组合。<bookmark mark='a'/>一价定律随之而来：如果两个组合在每种状态下收益相同、价格却不同，就买便宜的、卖贵的，把差价留下。注意这个定义不需要什么：不需要概率，不需要股票模型，甚至不需要大家对未来看法一致。只要今天的价格，和状态的清单。假定融资无摩擦、多空交易可执行，日期与结算一致，且相关状态具有正概率。正银行资产可将严格负成本再投资为正终值支付。",
    'Now build parity. Payoffs at expiry':
        "现在来拼出平价。横轴是股价，纵轴是到期收益：买入看涨期权是一根在行权价处向上弯的曲棍球杆。<bookmark mark='a'/>卖出看跌期权向下弯。<bookmark mark='b'/>把它们加起来：两个拐点抵消，剩下一条直线，股价减行权价，在每种状态下都是一份远期。<bookmark mark='c'/>这条直线也能用一股股票加上借入贴现后的行权价买到。收益相同，价格就相同：看涨减看跌等于股价减贴现行权价。<bookmark mark='d'/>对反向比特币期权，假定BTC利率为零，对应平价为1减K除以F。算一个例子：股价103、行权价100、利率为零时，右边是3。如果一年期利率是4%，就是103减去96.08，约6.92。反向比特币公式假定BTC贴现因子为一。一般形式还要乘这个因子，而不是简单把每个即期美元价格除以远期。",
    'Now misprice the put at six':
        "现在把看跌期权错定为6元，看套利怎样锁定。看涨减看跌是4，比远期的3多。<bookmark mark='a'/>以10元卖出看涨。<bookmark mark='b'/>以6元买入看跌。<bookmark mark='c'/>买入股票：这条线变平了。<bookmark mark='d'/>借入缺口的99元：这个组合不花钱，到期付你1元。<bookmark mark='e'/>到期时200个可能的价格，全都落在同一条线上。对冲好的头寸里，已经没有世界的状态了。",
    'f"Here is the House\'s code that reads the forward from real trades':
        "这是公司从真实成交里读出远期的代码：把早上的期权成交按到期日和行权价分组，每个看涨配上时间最近的看跌，要求相隔十分钟以内且接近平值。<bookmark mark='a'/>每一对都给出远期：行权价除以1减去看涨减看跌的价格。<bookmark mark='b'/>{p['n_pairs']}对，覆盖{len(ex)}个到期日，一半与各自中位数相差不到{p['trade_p50']:.1f}个基点。",
    'f"Is that forward real?':
        "这个远期是真的吗？Deribit在同样的到期日上挂有期货，公司抓取了同一时段全部{fb['n_trades']:,}笔期货成交。<bookmark mark='a'/>圆点是期权平价隐含的远期，方块是定期期货的成交价。在两者都有的{fb['n_matched']}个到期日上，差距的中位数是{gp50:.1f}个基点，最大{gmax:.1f}个。<bookmark mark='b'/>{tail}永不到期的永续合约，在同一时段里与指数相差不到{fb['perp']['basis_bp']:.1f}个基点。这里假定BTC贴现因子为一。成交时间并不相同，因此是观测一致性检查，不是可执行套利检验。",
    "They agree to within a quote's width":
        '它们的差别不到一个报价的宽度；要是差得更多，期现套利的交易员会把差距抹平。',
    'That is wider than a quote':
        '这比一个报价还宽：两个市场之间的基差本身就是一笔交易。',
    'Pause and predict. If the put were eight':
        "暂停预测一下。如果看跌期权是8元，哪几条腿要反过来？<bookmark mark='a'/>全部四条：买入看涨、卖出看跌、卖空股票、放贷：今天就拿到1元。理论上平价不可能失效。下一章：它失效的那些日子。",
    'Chapter two. Where parity breaks.':
        '第2章。平价在哪里失效。',
    'Parity assumed you can sell short':
        "平价假设你能卖空，而卖空意味着借入股票；股票稀缺时，要付借券费h。重做一遍复制。组合A是看涨期权加一张支付行权价的债券：价值是股价与行权价中较大的那个。<bookmark mark='a'/>组合B是看跌期权加上一部分出借的股票；借券费让它到期时长成一整股。<bookmark mark='b'/>收益相同，价格相同：借券费就像一笔股息。<bookmark mark='c'/>反过来读，期权价格就揭示了借券费。奥费克、理查森和怀特洛在2004年证明，平价的违背出现在最难卖空的地方。它们不是免费的钱，而是一个价格。算一个数：股价55，借券费每年30%，还剩三个月，它在平价里的分量是55乘以e的负0.075次方：约51，而不是55。这个等式是理想化出借收益模型，要求收益可交易并可再投资成股票。实际借入和出借条款不同，股票可能被召回，约束通常给出价格区间。反推的h只是特定假设下的平价诊断，不是唯一识别出的费率。",
    'f"The famous case. On the second of March 2000':
        "最有名的案例。2000年3月2日，3Com向公众出售了Palm的5%，并承诺把其余部分分给自己的股东：每股3Com大约对应1.5股Palm。<bookmark mark='a'/>Palm收在95美元，所以每股3Com里的Palm价值约{hold:.0f}美元。<bookmark mark='b'/>3Com收在82美元。3Com的其余部分被定价为每股负{abs(stub):.0f}美元，合计负220亿美元。<bookmark mark='c'/>买入3Com、卖空Palm需要借到Palm的股票，而空头仓位达到了流通股的147%。平价给这种稀缺定了价：3月16日，用期权构造的空头只要39美元，而股票是55美元。拉蒙特和塞勒在2003年记录了这一切。",
    'In January 2021, GameStop, heavily shorted':
        '2021年1月，被大量做空的游戏驿站成了Reddit的宠儿。美国证监会工作人员的报告：1月从低点到高点涨了约2700%，随后跌了86%以上。做空它的梅尔文资本需要城堡和Point72注资27.5亿美元。当借入股票代价高昂甚至不可能时，这个代价就体现在看跌期权的价格里。',
    'Stack two parities and the stock, and its fee, cancel':
        "把两个平价叠起来，股票和它的借券费都抵消了：一个看涨价差多头加一个看跌价差空头，叫箱式组合，在每种状态下都支付两个行权价之差。<bookmark mark='a'/>所以箱式组合就是一笔贷款，它的价格就是利率；第17章会讲谁在交易它。<bookmark mark='b'/>但前提是欧式行权。2019年，一位罗宾汉用户用美式期权搭的箱式组合被提前行权，亏损远超这笔交易看起来的风险；罗宾汉随后禁止了箱式组合。算一个例子：行权价100和110，一年，利率4%。箱式组合一定支付10，所以它值10乘以e的负0.04次方，约9.61；买入它就是以4%放贷。",
    'Pause and predict. The stub stayed negative for weeks.':
        "暂停预测一下。残值连续几周为负。为什么不买入3Com、卖空Palm，然后等着？<bookmark mark='a'/>空头那条腿稀缺、昂贵、还可能被召回，而收敛没有截止日期：1985到2000年的82个负残值案例中，30%在价差收敛之前，母子公司的联系就被切断了。下一章：所有这些交易背后的规律，用几何来看。",
    'Chapter three. The geometry of arbitrage.':
        '第3章。套利的几何。',
    'Here is what no arbitrage looks like.':
        "无套利是这个样子的。单期市场：一张支付1的债券，一只价值80、100或125的股票。三种状态，所以一个收益就是三维空间里的一个点。<bookmark mark='a'/>绿色的盒子装着永不亏损的收益。套利就是一个免费组合，它的收益落在这里、又不在原点。<bookmark mark='b'/>哪些收益是免费的？卖空一股，持有等于股价的债券：股价100时，它支付20、0，或者负25。把它放大缩小、反过来，就描出这条蓝线。<bookmark mark='c'/>无套利意味着这条线只在原点碰到绿色的角，于是可以过这条线放一个平面，让整个角都在一侧。它的法向量，紫色的箭头，严格为正。为什么是一条直线？两种资产，一个价格约束：不花钱的组合构成一维的族，所以它们的收益是一条过原点的直线。",
    "Raise the stock's price. The line and the plane turn. The normal's first two com":
        "抬高股票现价，直线和平面随之转动。法向量前两个分量缩小，第三个增大。<bookmark mark='a'/>到125时，状态价格是零、零、一：只有弱正法向量，平面落在角的一张面上。<bookmark mark='b'/>再往外，就不存在严格正的分离法向量。卖空股票、持有等额债券，可以免费得到每个状态都为正的支付。<bookmark mark='c'/>在130时支付为50、30、5。在这个市场，严格正状态价格的存在等价于无套利；仅有带零分量的法向量不够。",
    'In symbols. D holds the payoffs':
        "用符号写。D装着收益，每个资产一行、每个状态一列；p是价格。免费收益是D转置乘以theta，theta是不花钱的组合。<bookmark mark='a'/>套利就是落在角里、又不是零的免费收益。<bookmark mark='b'/>法向量为psi的平面包含这条线，当且仅当psi与每个免费收益正交。<bookmark mark='c'/>于是D乘psi与每个不花钱的组合正交，所以它是价格的倍数；重新缩放，D乘psi就等于p。下一章证明：正的psi存在，当且仅当没有套利。在股价100处验证一下，那里的法向量是十三分之五、十三分之四、十三分之四：80的十三分之五，加上100的十三分之四，再加上125的十三分之四，恰好是100；三者之和是1，正是债券的价格。银行资产价格和支付都为一，因此拉姆达等于正状态价格之和，严格为正，才能这样归一化。银行资产还把负初始成本转成零成本的正支付。",
    'Pause and predict. At exactly a hundred and twenty-five':
        "暂停预测一下。股价恰好是125时，有套利吗？<bookmark mark='a'/>有：卖空一股，持有125的债券。它不花钱，支付45、25或0。为零的状态价格还不够正。下一章：准确说明何时不存在这类交易的定理，及其证明。",
    'Chapter four. The fundamental theorem of asset pricing, proved and solved.':
        '第4章。资产定价基本定理：证明与求解。',
    'The theorem. With one period and finitely many states':
        "定理。在一期、有限多个状态的市场里，没有套利，当且仅当存在严格为正、能给每个资产定价的状态价格。<bookmark mark='a'/>哈里森和克雷普斯在1979年这样表述它；它的底下是法卡斯1902年的引理，以及施蒂姆克1915年的严格正形式。假定交易无摩擦，多空头寸不受限，有正银行资产，且每个列出的状态都有正实际概率。一般价格空间应使用支付锥的相对内部。",
    'The easy direction. If strictly positive state prices exist, every attainable no':
        "容易的方向：若存在严格正状态价格，任何可复制的非负非零支付都要花钱。<bookmark mark='a'/>反过来，把负成本和支付收集为子空间L。无套利意味着它与非负正交锥只在零点相交。<bookmark mark='b'/>用超平面把L与紧单纯形分开。在线性子空间上有界的线性函数必须为零，其法向量拉姆达每个分量严格为正。<bookmark mark='c'/>除以第一个正分量，得到严格正状态价格。关键在于存在性：不完备市场可以同时有带零分量的弱状态价格和严格正状态价格，而没有套利。只有当单状态支付可复制时，其零价格才构成套利。",
    'f"The same fact in price space.':
        "同一个事实，在价格空间里看。每个状态是一支箭头，表示两种资产在那里支付多少，箭头的正组合填满这个锥。<bookmark mark='a'/>无套利，当且仅当价格向量严格在锥内。<bookmark mark='b'/>提高股价：点在125时碰到锥的边缘，到130时已经在外面，这时线性规划返回的是那个分离组合。<bookmark mark='c'/>它是上一章图像的对偶，在同一时刻失效。130时线性规划给出的组合：持有{th[0]:.2f}的债券，卖空{abs(th[1]):.4f}股，成本是负{abs(f['ftap_130']['cost']):.3f}，在任何状态下支付都不小于零。",
    'f"The House decides it by linear programming':
        "公司用线性规划来判定：在价格等于收益乘状态价格的约束下，最大化最小的状态价格t。下面是求解它的教学版单纯形法。<bookmark mark='a'/>从人工变量出发，然后转轴：编号最小、检验数为负的列进基，这是布兰德法则，保证不会循环；比值检验决定谁出基。<bookmark mark='b'/>股价为100时，{len(st100)}次转轴把人工变量赶到零，最小的状态价格是{x100[3]:.3f}。<bookmark mark='c'/>股价为130时，{len(st130)}次转轴之后就卡住了：不存在状态价格。卡住的单纯形表的对偶变量就是证书：持有125的债券、卖空一股，成本负5，支付45、25或0。这就是机器执行的法卡斯引理。布兰德法则还要求在最小比值并列时选择基变量索引最小者离开；仅规定入基规则并不是完整防循环法则。",
    'Pause and predict. Add only states between the existing extremes. Can no arbitra':
        "暂停预测：只在原有极端之间增加状态。股票现价严格介于80与125之间时，无套利会失效吗？<bookmark mark='a'/>不会。有限状态凸包不变，内部价格仍有严格正状态价格。到80或125时只有弱边界向量，并存在套利。开区间很重要。",
    'Chapter five. State prices, the discount factor, and Q.':
        '第5章。状态价格、贴现因子与Q。',
    'Name that normal. Kenneth Arrow':
        "给这个法向量起名字。肯尼斯·阿罗在1964年设想了一种只在一个状态下支付1单位的证券：它的价格就是状态价格，任何收益都是它们的组合。<bookmark mark='a'/>再乘以、除以每个状态的真实概率：价格就是收益乘以m的期望，m就是随机贴现因子。<bookmark mark='b'/>债券在每种状态下都支付1，所以状态价格之和是1除以1加r。<bookmark mark='c'/>把它们重新缩放到总和为1：这就是概率Q，价格就是贴现后的Q期望，斯蒂芬·罗斯在1978年这样写道。<bookmark mark='d'/>Q相对P的密度就是归一化的贴现因子。Q不是预测：它是重新加权后的P。用股价100处的状态价格算一个例子：十三分之五、十三分之四、十三分之四。利率为零时它们之和已经是1，所以这个Q就是这三个数；行权价100、只在繁荣时支付25的看涨期权，值25的十三分之四，约7.7。图中的状态价格只是股票与债券价格的一种选定正扩张。在这个Q下，看涨价格等于所述期望；只有足够支付参与交易、市场完备后，价格才由市场唯一确定。",
    'f"As one animation: three states':
        "把它做成一段动画：三个状态，崩盘、持平、繁荣；琥珀色的柱子是虚构的真实概率，在它下面股票预计会上涨。<bookmark mark='a'/>用它们去除状态价格：崩盘时贴现因子是{m[0]:.2f}，其他状态都低于1。崩盘时的一元钱很贵。<bookmark mark='b'/>重新归一化，柱子变成紫色：这就是Q。崩盘的柱子变高，繁荣的柱子变矮，在Q下股票的期望价格正好停在100。而贴现因子在P下的平均就是债券的价格，1除以1加r：这里正好是1。这是一个方便的正状态价格选择；在这个不完备市场中，不是由市场唯一识别的崩盘状态价格。",
    'Here Q is not unique.':
        "这里的Q不唯一。三角形装着三个状态上的所有概率。<bookmark mark='a'/>能正确给股票定价的测度构成紫色线段，从崩盘九分之五、繁荣九分之四，到全部放在持平状态。<bookmark mark='b'/>提高股价：线段滑向繁荣的那个角，在125时缩成一个点，然后离开三角形，正好就是免费收益刺进角里的那个价格。线段上的每一点都能正确地给债券和股票定价；它们只在两种资产构造不出来的收益上意见不同。只有这个线段中严格正的部分才与全支持实际概率等价。在125时剩下的弱向量为零、零、一；它能给资产定价，却不等价，不能排除套利。",
    'f"Now an observational density-ratio illustration. Q is a fitted sixteen-day opt':
        "这是观测性的密度比示例。Q是拟合的16日期权密度，分母是来自{k['n_windows']}个不重叠收益窗口的历史无条件核密度，再移到今日价格。<bookmark mark='a'/>比值为q除以p。随机贴现因子还包含贴现，并需要合适的条件实际分布。<bookmark mark='b'/>拟合曲线有驼峰，类似定价核之谜。仅有风险厌恶并不能保证它随股票价格单调，还需要经济假设。<bookmark mark='c'/>百分之五到九十五的逐点区间只重采样历史P，固定Q拟合，遗漏Q拟合和制度变化的不确定性。把事后选出的峰与端点比较不是同时显著性检验，区间重叠也不能证明左侧平坦。",
    'It has a hump: it rises toward the forward':
        '它是驼峰形的：向远期方向上升，越过远期后下降，下降超出了阴影带。',
    'It falls from left to right, as theory says.':
        '它从左到右下降，与理论一致。',
    "Pause and predict. Q gives a crash twice P's probability.":
        "暂停预测一下。Q给崩盘的概率是P的两倍。那里的贴现因子高于还是低于1除以1加r？<bookmark mark='a'/>高于：是它的两倍。Q比P重的地方，一元钱就贵。下一章：在多步上用Q定价——二叉树。",
    'Chapter six. The tree: replication, then folding back.':
        '第6章。二叉树：先复制，再倒推。',
    'Cox, Ross and Rubinstein made the theorem computable':
        "考克斯、罗斯和鲁宾斯坦在1979年让这个定理可以计算。一步：股价从100变成120或80；行权价100的看涨期权支付20或0：平面上的两个点。<bookmark mark='a'/>股票加债券是一条直线，恰好有一条穿过这两个点：这就是复制组合。<bookmark mark='b'/>它在今天股价处的高度就是期权价格，10：买入半股，借入40。<bookmark mark='c'/>用符号写：匹配两个状态，相减，代回。<bookmark mark='d'/>价格是两个收益的加权平均。<bookmark mark='e'/>权重q只来自涨跌幅和利率，与任何人认为上涨的概率无关；它落在0到1之间，当且仅当没有套利。检验这个对冲：上涨时半股值60，减去欠的40，是20；下跌时40减40，是零。两个收益都恰好对上。两分支都具有正实际概率，允许无摩擦再平衡，银行收益严格介于下跌和上涨因子之间。因此q必须严格介于零和一之间；端点不够。",
    'f"Now four steps: a call at a hundred':
        "现在是四步：行权价100、波动率25%、一年期的看涨期权。到期时就是收益。<bookmark mark='a'/>倒推：每个节点是后面两个节点的风险中性平均，它的Delta是两者的斜率。树根：{t['four_price']:.2f}。<bookmark mark='b'/>现在来交易：从这么多钱开始，持有每个节点的Delta，其余部分用债券融资。跟着一条路径走。<bookmark mark='c'/>到期时账本恰好等于收益，这条路径如此，一千条路径中的每一条都如此，误差在{t['rep_max_err']:.0e}以内。这就是复制。注意这些Delta：深度实值处接近1，深度虚值处接近0，正如第10部分布莱克—斯科尔斯的Delta那样。",
    'f"The House\'s tree in ten lines':
        "公司的二叉树只有十行：由波动率得到上涨和下跌因子，算出风险中性概率，叶子上放收益，再用一行一步一步往回折。<bookmark mark='a'/>先跑1到4步，再让N变大。<bookmark mark='b'/>价格锯齿形摆动，奇数步高于偶数步，逼近布莱克—斯科尔斯的{t['bs']:.3f}；200步时是{P[199]:.3f}。整棵树大约需要N平方除以2次运算，误差大致按N分之一缩小，上面再叠加锯齿形摆动。",
    'f"One more line makes it American':
        "再加一行就变成美式：在每个节点取立即行权与继续等待中较大的那个。<bookmark mark='a'/>对利率5%的看跌期权，在{len(nodes)}个深度实值的节点上行权更好，看跌期权值{t['am_put']:.2f}，而欧式的是{t['eu_put']:.2f}。施里夫的第4章完整讲了这一点。行权更好的节点与等待更好的节点之间的分界线，就是第8和第10部分的提前行权边界。",
    'Pause and predict. Why the zigzag':
        "暂停预测一下。为什么奇数步和偶数步之间会锯齿形摆动？<bookmark mark='a'/>N为偶数时，有一个节点正好落在行权价上，也就是收益的拐点；N为奇数时，行权价落在两个节点之间，误差的符号就变了。二叉树之所以可行，是因为每个收益都能被复制。下一章：不能复制时会怎样。",
    'Chapter seven. Incomplete markets: the interval as a linear program.':
        '第7章。不完备市场：区间即线性规划。',
    'f"Give the stock three outcomes':
        "让股票有三种结果，80、100或125，只能交易股票和债券。看涨期权支付0、0或25：没有一条直线能穿过这三个点，所以它无法复制。<bookmark mark='a'/>卖方做超复制：找一条在三个点上方或经过它们的最便宜的直线。像盖子一样把它放下来；它停在最差和最好的两个状态上，高度是{s['upper']:.2f}。<bookmark mark='b'/>买方从下面往上推一条线；它停在零。区间之外，总有一方存在套利。<bookmark mark='c'/>右边是同一个问题，放在债券和股数的平面上：每个状态是一个半平面，成本是一条滑动的直线，停在一个顶点上：借入{abs(B):.2f}，持有{D:.3f}股。盖子的斜率，九分之五股，就是超对冲者的Delta；截距就是借款。",
    'Linear programs come in pairs.':
        "线性规划总是成对出现。卖方的问题：最便宜的占优组合。<bookmark mark='a'/>它的对偶给每个状态一个乘子：债券那一列让它们之和为1，股票那一列让它们给股票定价。对偶在风险中性测度上最大化这个期权的期望。<bookmark mark='b'/>最优的测度是第5章线段的一个端点，给出100除以9，也就是盖子的11.11。<bookmark mark='c'/>下界是另一个端点，零；严格为正的测度永远到不了端点：区间是开的。<bookmark mark='d'/>哈里森和普利斯卡1981年的第二基本定理：市场完备，当且仅当鞅测度唯一。只有两个状态时，测度的线段缩成一个点，区间缩成一个价格：这就是第6章。",
    'f"The teaching simplex solves the seller\'s problem too':
        "教学版单纯形法也能解卖方的问题，自由变量拆成两部分，每个状态一个剩余变量。<bookmark mark='a'/>{len(v)}次转轴到达顶点，成本{s['upper']:.4f}；HiGHS求解器的结果每一位都一样。最后一张单纯形表的对偶变量就是那个极端测度：九分之五、零、九分之四。",
    'f"Do more states close the gap?':
        "更多的状态能缩小差距吗？在2到33个状态的网格上，看一个平值看涨期权。<bookmark mark='a'/>两个状态：一个点。三个或更多：每次都是同一个区间，因为只有极端状态起作用。<bookmark mark='b'/>模型会在区间里挑一个价格；缩小差距的是增加可交易的资产，而不是状态。20%波动率下的布莱克—斯科尔斯给出{inc['bs']:.3f}：区间里无穷多个选择中的一个。新增状态仍在相同固定极端之间，因此本例价格界不变。布莱克—斯科尔斯数值是区间内的参考；它的无界连续分布不是这个有限网格分布。",
    'Pause and predict. Add a fourth state at a hundred and ten.':
        "暂停预测一下。在110加第四个状态。区间会变吗？<bookmark mark='a'/>不会：它的收益10，在盖子下面、地板上面。下一章：可交易的期权怎样收窄这个区间。",
    'Chapter eight. Completing the market, and super-replication through time.':
        '第8章。让市场完备，以及跨时间的超复制。',
    'f"Options close the gap in real markets.':
        "在真实市场里，是期权缩小了差距。33个状态，一个在1.1以上支付1的数字期权。只用股票和债券，它的价值在{r0['lower']:.2f}到{r0['upper']:.2f}之间：几乎什么都不知道。<bookmark mark='a'/>现在让看涨期权一个行权价一个行权价地上市，每个都给市场能构造的东西加上一个拐点。<bookmark mark='b'/>一个看涨期权：{r1['lower']:.2f}到{r1['upper']:.2f}。十个：{rl['lower']:.2f}到{rl['upper']:.2f}，围着真实价格{true:.2f}。斯蒂芬·罗斯在1976年证明，有足够多行权价的期权，市场就完备了。看涨期权为什么有用？每个新的行权价都加了一个拐点，也就是收益空间里的一个新方向，超复制的盖子就能弯得更贴近这个收益。这是33状态模型。足够多的独立看涨支付可张成有限支付空间；有限个期权一般不能使连续状态市场完备。闭区间柱表示超对冲极限；除非支付可复制，等价测度价格位于内部。",
    'Now remove the options and add time.':
        "现在拿走期权，加上时间。三叉树：每一步上涨、持平或下跌，只有股票和债券，每个节点都不完备。<bookmark mark='a'/>卖方从后往前做超复制：在每个节点，取一步鞅测度上最大的期望。<bookmark mark='b'/>这些测度构成一条线段，两个端点分别只用外侧两个分支，或者只用中间分支。<bookmark mark='c'/>对凸的收益，外侧的端点总是胜出：外侧分支亮起，中间分支变暗。<bookmark mark='d'/>所以超复制价格就是在最宽波动率下的二叉树价格，极限是那个波动率下的布莱克—斯科尔斯：这就是不确定波动率模型，阿韦利亚内达、利维和帕拉斯，以及莱昂斯，1995年。在这个模型里，只知道波动率在某个区间内的卖方，对凸的收益按区间上端的布莱克—斯科尔斯收费，对凹的收益按下端收费。",
    'f"Run it on trinomial trees':
        "在最多256步的三叉树上运行，最宽波动率25%：超复制价格是{up[-1]:.3f}，而25%波动率下的布莱克—斯科尔斯是{st['bs']:.3f}。<bookmark mark='a'/>下复制价格把全部质量放在中间分支：股票从不变动，看涨期权只值内在价值，零。无套利区间大得惊人；交易台靠交易期权，或者选择一个模型，来把它收窄。一步时，树的价格是{up[0]:.2f}；两步时，{up[1]:.2f}：又是第6章奇偶步的锯齿，因为超复制价格就是二叉树价格。",
    'Pause and predict. With two traded calls':
        "暂停预测一下。有两个可交易的看涨期权，哪一对能把数字期权的区间完全合上？<bookmark mark='a'/>两个中间没有状态、夹住跳跃点的行权价：把它们的看涨价差放大，在每种状态下都等于这个数字期权。用1.1和1.12的看涨期权，线性规划给出的区间宽度为零。下一章：连续时间中的同样思想。",
    'Chapter nine. Continuous time: Girsanov as reweighting.':
        '第9章。连续时间：吉尔萨诺夫即重新加权。',
    'The theorem grew up. In finite frictionless markets, no arbitrage is equivalent ':
        "定理继续发展。在有限无摩擦市场，无套利等价于存在等价鞅测度。<bookmark mark='a'/>连续时间中，局部有界半鞅的一般定理使用风险趋零无免费午餐，以及等价局部鞅测度。完备性和唯一性还要规定过滤与支付类别。<bookmark mark='b'/>有统一下界的可容许贴现财富一般只是上鞅，并不自动是真鞅。只有复制出的贴现价值具有所需可积性并为真鞅时，复制价格才等于期望。本课常系数布莱克—斯科尔斯例子满足这些条件。",
    "Continuous-time state prices come from Girsanov's theorem.":
        "连续时间的状态价格来自吉尔萨诺夫定理。在P下，股票以mu增长。<bookmark mark='a'/>贴现之后，它以mu减r漂移。<bookmark mark='b'/>把多出来的漂移折进噪声里，平移lambda，也就是风险的市场价格：贴现股价变成了鞅。<bookmark mark='c'/>吉尔萨诺夫：在这个指数密度下，新的噪声是布朗运动。<bookmark mark='d'/>所以价格既是加权的P期望，也是不加权的Q期望；权重的二阶矩决定了蒙特卡洛的代价。用我们的数字，10%的漂移、25%的波动率，lambda是0.4：每单位风险获得0.4单位的超额收益。假定有限期限、常数波动率严格为正，银行账户初值为一。常数拉姆达满足诺维科夫条件，所以密度均值为一。此处定价等式适用于这个完备布朗模型中的可积支付。蒙特卡洛误差由加权支付的方差决定，而不只是权重。",
    'Here is what a change of measure looks like.':
        "测度变换是这个样子的。真实测度下150条股价路径，每年10%的漂移；它们的平均，那条粗线，在上升，右边是它们的终点。<bookmark mark='a'/>现在一条路径也不动。给每条路径吉尔萨诺夫规定的权重，它只取决于这条路径的噪声最后停在哪里：涨得多的路径变细，跌的路径变粗。<bookmark mark='b'/>加权平均压平到今天的价格上：在Q下股票是公平游戏。终点的直方图从P滑到Q。路径一点没变，变的只是每条路径算多少分量。Q的密度就是P的密度乘以权重，它的均值是今天的价格，100。线宽为可见性按最大权重缩放。两个终值直方图使用相同的概率刻度，并包含所有模拟观测。终值直方图使用两万个缓存终值观测，路径扇和加权均值使用150条路径。有限样本均值不必精确平坦。",
    'f"With {g[\'n\']:,} paths':
        "用{g['n']:,}条路径，收益的简单平均是{g['price_naive']:.2f}：这是错误的价格，忽略了风险。<bookmark mark='a'/>加权之后是{g['price_weighted']:.2f}，标准误{g['se']:.3f}，而布莱克—斯科尔斯是{g['bs']:.2f}。{tail}<bookmark mark='b'/>有效样本是路径数的{100 * g['ess']:.1f}%；公式预测的是{100 * g['ess_pred']:.1f}%。不加权的平均之所以太高，是因为在P下股票每年向上漂移10%：它把这个漂移当成了免费的。有效样本公式是大样本相对极限；有限样本会有波动。",
    'Within two standard errors.':
        '在两个标准误以内。',
    'More than two standard errors away':
        '超出了两个标准误：值得再看一眼。',
    'f"Pause and predict. Raise the drift to sixty percent.':
        "暂停预测一下。把漂移提高到60%。权重会怎样？<bookmark mark='a'/>它们会崩塌：有效样本降到大约{100 * g['ess60_pred']:.1f}%，实测{100 * g['ess60']:.1f}%。少数几条路径扛起了整个价格，这就是定价者直接在Q下模拟的原因。连续时间带来了新的作弊方式。下一章：免费午餐、加倍下注与泡沫。",
    'Chapter ten. Free lunches, doubling, and bubbles.':
        '第10章。免费午餐、加倍策略与泡沫。',
    'Continuous time allows a trick one period never did.':
        "连续时间允许一个单期里做不到的把戏。在一个公平游戏上，越临近截止时间押得越重：持有剩余时间平方根的倒数。<bookmark mark='a'/>收益的方差是T除以剩余时间的对数，它在截止之前就趋于无穷。<bookmark mark='b'/>由丹比斯、杜宾斯和施瓦茨的定理，收益是这个时钟上的布朗运动，所以它一定会在T之前到达正1。到那里就停：从一个公平游戏里拿到稳赚的利润。<bookmark mark='c'/>代价在途中：由第4部分的赌徒破产公式，财富先跌破负k的概率是1除以1加k。一半的路径会跌破负1。",
    'f"A hundred and twenty doublers.':
        "120个加倍者。<bookmark mark='a'/>它们一个接一个到达正1并停下，变成绿色，而它们最大亏损的直方图长出一条不断延伸的尾巴。<bookmark mark='b'/>在{f['n']:,}个模拟的加倍者中，{100 * fr['1']:.1f}%在获胜前跌破负1，理论是一半；{100 * fr['10']:.1f}%跌破负10，理论是十一分之一。<bookmark mark='c'/>解决办法：可容许策略，财富永远不低于某个负a。在负1处放一个下限，一半的加倍者会被强制止损。可容许的加倍者，在负1或正1处停下，一半时间赢、一半时间输：又成了公平游戏。可视路径使用离散网格首达，并在缓存时刻加上示意停止端点。可视时钟60时，120条中有17条尚未到达。另一个两万路径模拟在有限最大时钟处仍有少量路径未到达。桥修正的穿越与最低点统计仍有有限步长和联合修正近似误差。几乎必然最终成功是连续、无限时钟的结论。",
    'Admissibility is still not quite enough.':
        "可容许性还不太够。克雷普斯在1981年看到，近似套利的极限，也就是免费午餐，也必须排除。<bookmark mark='a'/>在离散时间里，达朗、莫顿和威林格在1990年证明，在任何概率空间上，单纯的无套利就够了。<bookmark mark='b'/>在连续时间里，德尔班和沙赫迈尔在1994年找到了条件：没有风险消失的免费午餐。<bookmark mark='c'/>它等价于存在等价局部鞅测度，在最一般的情形下，1998年，是sigma鞅测度：这是定理的最终形式。为什么是风险消失？要排除的不只是精确的套利，还有亏损趋于零而收益留下的交易序列；正是这一点让可达到的收益集合保持闭合，第4章的分离超平面在无穷维中才仍然存在。",
    'f"One strange object lives inside the theorem. Start a three-dimensional Brownia':
        "定理允许一个奇特对象：让三维布朗运动从一、零、零出发，价格等于它到原点距离的倒数。这个严格正、无漂移价格是严格局部鞅。<bookmark mark='a'/>它的期望低于初值，公式和已有模拟都展示这一点。超出图窗的尖峰被省略，而不是压平。<bookmark mark='b'/>它可以满足NFLVR，同时股票交易价格高于终值期望，形成泡沫。如果看涨和看跌期权都采用最小期望价格，两者之差使用终值股票期望，而不是股票现价。但不能断言所有定价方式都破坏平价：抵押与可容许约定会决定可用的期权价格和交易。",
    'Pause and predict. The doubler costs nothing':
        "暂停预测一下。加倍策略不花钱，最后也从不亏钱。为什么它不是套利？<bookmark mark='a'/>它不是可容许的：途中需要无限的信用，而一旦亏损有界，它就不再稳赢。Q以现金为计价单位定价。下一章：用任何你喜欢的单位定价。",
    'Chapter eleven. Change of numeraire.':
        '第11章。计价单位变换。',
    'So far prices were measured in units of the bank account. A strictly positive tr':
        "此前价格用银行账户衡量。严格正的可交易资产也可作为单位，但其贴现价格必须为真鞅，保证所定义密度的均值为一。<bookmark mark='a'/>配合适当可积性，就可用新单位定价。Geman、El Karoui和Rochet于1995年把它发展成一般工具。上一章泡沫那样的严格局部鞅并不自动满足均值为一的要求。",
    'Two lines. A price divided by the numeraire':
        "两行就够。价格除以计价单位，是它的测度下的期望；除以银行账户，是Q下的期望。<bookmark mark='a'/>两者对每个收益都成立，所以两个测度相差的就是两个计价单位的相对增长。<bookmark mark='b'/>用在看涨期权上：实值时，你收到的股票减去你支付的行权价。<bookmark mark='c'/>行权价那部分是Q概率；股票那部分，以股票为单位，是股票测度下的概率。<bookmark mark='d'/>在那里对数价格的漂移高出整整一个sigma平方：N(d1)和N(d2)是同一个事件在两种单位下的样子。这里的等式针对贴现价值为真鞅的可复制支付。图中的正态概率使用无分红、常波动率股票。",
    'f"See it. A stock at a hundred':
        "看一看。股价100，波动率25%，一年，行权价100的看涨期权。Q的密度，以及到期实值的概率：{n['Nd2']:.4f}，也就是N(d2)。<bookmark mark='a'/>把单位换成股票：密度乘以价格。它向右倾斜，同一个事件的概率变成{n['Nd1']:.4f}，也就是N(d1)。<bookmark mark='b'/>100乘以前者减去100乘以后者：{n['call']:.2f}。一个收益，两种单位，一个价格。在Q下，对数价格的漂移是负二分之一sigma平方；在股票测度下是正二分之一sigma平方：两个密度之间恰好差一个因子，s除以S0。",
    'f"It pays off on an option to exchange':
        "它在交换期权上立了大功。以第二种资产为单位，收益就是两者比值上行权价为1的看涨期权。<bookmark mark='a'/>在那种资产的测度下，比值是鞅，波动率由两者的波动率和相关性决定。<bookmark mark='b'/>所以价格就是比值上的布莱克—斯科尔斯，没有利率：马格雷布，1978年。<bookmark mark='c'/>在这组数字下，公式给出{n['margrabe']:.2f}；Q下的一百万条路径给出{n['mc_Q']:.2f}；第二种资产测度下的一百万条路径给出{n['mc_S2']:.2f}。波动率相同、相关性为二分之一时，比值的波动率等于各自的波动率，30%；相关性为1时它是零，平值的交换期权一文不值。",
    'f"The bond gives the forward measure, and the annuity gives the swap measure. Bl':
        "债券给出远期测度，年金给出互换测度。Black互换期权公式还需要互换利率对数正态模型。<bookmark mark='a'/>在这个拟合有限网格例子里，未贴现的美元远期价值为{n['usd']:,.0f}，比特币权利金为{n['btc']:.4f}。两者不是同一个即期美元金额。<bookmark mark='b'/>取BTC贴现因子为一，用拟合网格均值选择一致的美元贴现因子{df_usd:.5f}。BTC权利金乘今日现价{spot:,.0f}，得到美元现值{spot_pv:,.0f}；乘拟合远期均值则得到未贴现远期价值。价内概率分别为{n['Q_itm']:.2f}与{n['QB_itm']:.2f}，但贴现价格换成同一当前单位后相等。这些贴现选择用于演示恒等式，不是独立估计两条货币曲线。",
    "Pause and predict. Under the stock's own measure":
        "暂停预测一下。在股票自己的测度下，股票的漂移比无风险利率快还是慢？<bookmark mark='a'/>快，快sigma平方：按终点给路径加权，会把漂移往上推。下一章：直接从期权价格中读出Q的整个分布。",
    'Chapter twelve. Butterflies build the density.':
        '第12章。蝶式价差拼出密度。',
    "Chapter five's state price can be bought with calls.":
        "第5章的状态价格可以用看涨期权买到。在90买入一份。<bookmark mark='a'/>在100卖出两份。<bookmark mark='b'/>在110买入一份：一顶帐篷，也就是蝶式价差，只在100附近支付。<bookmark mark='c'/>它的价格就是落在这个区间的价格：一个状态价格，而且永远不低于零。除以h平方之后，帐篷的面积是1：一根小小的直方图柱子，所以不同宽度的柱子可以互相比较。",
    'f"Tile the strike axis with butterflies':
        "用蝶式价差铺满行权价轴，用曲面上16天后到期的期权。每根柱子是一个蝶式价差的价格除以宽度的平方。<bookmark mark='a'/>宽度减半，再减半：柱子变细，顶端收敛到一条光滑的曲线。<bookmark mark='b'/>这就是风险中性密度，布里登和利曾伯格1978年的极限。它的积分是{b['mass']:.5f}，均值{b['mean']:,.0f}美元，正是远期。导数恒等式使用看涨价格；本数值重建还使用拟合SVI的设定。导数恒等式不依赖特定模型，但这里的看涨价格由SVI插值和外推。有限报价本身不能唯一确定密度。本示例采用零贴现。这里曲面的美元曲线是未贴现远期价值，即反向BTC权利金乘拟合远期；不是即期美元权利金。美元现值还要乘美元贴现因子。",
    'The proof is two derivatives.':
        "证明就是求两次导数。看涨期权是收益的贴现期望。<bookmark mark='a'/>对行权价求导：得到负的贴现后到期高于行权价的概率，也就是一个数字期权的价格。<bookmark mark='b'/>再求一次：就是密度。<bookmark mark='c'/>而蝶式价差除以h平方是二阶差分，所以它收敛到二阶导数。<bookmark mark='d'/>静态无套利恰好就是：看涨价格随行权价下降，降得不比债券快，并且向上弯。算一个例子：如果行权价99和101之间的看涨价差值1.1，那么到期高于100的概率大约是1.1除以2，也就是0.55，还没算贴现。这些密度公式假定终值分布绝对连续且足够光滑。一般情况下二阶执行价导数是测度；有原子时数字期权使用单侧导数。完整静态无套利刻画除递减、凸性和斜率界外，还需要支付界和正确端点极限。看涨价差例子中，要再除以贴现因子才得到概率。",
    'Both derivatives on the real call curve':
        "两个导数放在真实的看涨曲线上：切线的斜率是到期高于行权价的概率，弯曲程度是密度。<bookmark mark='a'/>把行权价往上滑：概率在曲线最弯的地方，也就是远期附近，下降得最快；远处的曲线是直的，市场几乎看不到概率。",
    'f"The House checks these conditions on every surface':
        "公司在每张曲面上检查这些条件：正的斜率就是价格为负的看涨价差；下降的斜率就是负的蝶式价差。<bookmark mark='a'/>在16天的到期日上：用原始成交得到的{n}个行权价上，有{b['raw_fly']}个负蝶式价差；用曲面的中位数报价，有{b['mark_fly']}个；用拟合后的微笑曲线，{b['svi_fly']}个。<bookmark mark='b'/>{verdict}这不是免费的钱：成交发生在不同时刻，落在一个好几个蝶式宽的买卖价差里。所以公司从不对原始价格求导；先拟合。四十个里有七个听起来吓人，但相邻的行权价成交相隔好几分钟，远离平值时，买卖价差占价格的比例很大。",
    'Raw prices fail.':
        '原始价格不合格。',
    'Even the raw prices pass.':
        '连原始价格都合格。',
    'Pause and predict. A butterfly is offered at minus point one.':
        "暂停预测一下。有人以负0.1的价格卖一个蝶式价差。你怎么交易，可能出什么问题？<bookmark mark='a'/>买下它：别人付钱让你持有一个永不为负的收益。风险在执行：三条腿必须同时以这些价格成交。下一章：真实曲面上的密度。",
    'Chapter thirteen. The density on the Surface.':
        '第13章。曲面上的密度。',
    'f"The density is only as good as the smile it comes from':
        "密度的好坏取决于它来自的微笑曲线，所以来看公司拟合一条。白点：曲面在{fit['T'] * 365:.0f}天后的隐含波动率；紫色：从粗略初值出发的盖瑟尔SVI微笑曲线；下面是它隐含的密度。<bookmark mark='a'/>最初几步，微笑曲线大幅摆动，密度跟着摆，时而一边倒，时而双峰。<bookmark mark='b'/>大约25次函数计算之内，误差稳定在{rmse[-1]:.2f}个波动率点，密度不再变动。它继承了拟合的每一次晃动。五个参数分别是水平、斜率、偏斜、平移和曲率：五个数压缩了整个到期日。每个点都从相同初值重新拟合，允许更大的函数求值预算；收敛后求解器实际求值可能少于上限。回放横轴表示预算。",
    'The coordinates: total implied variance against log-moneyness.':
        "坐标：总隐含方差对对数价值度。<bookmark mark='a'/>SVI在这里是一条双曲线，五个参数。<bookmark mark='b'/>在微笑曲线上给每个行权价定价，再求两次导数。<bookmark mark='c'/>跨到期日看，在同样的价值度上总方差不能随期限下降，否则日历价差就是免费的。<bookmark mark='d'/>李的界限制了两翼的斜率。第12部分会证明这两点。原始SVI在两翼仍可能出现蝶式套利；盖瑟尔和雅基耶的曲面版本SSVI把两类套利都排除了，第12部分会拟合它。这里的日历单调性针对确定持有成本和当前归一化下的固定远期价内程度。李氏翼部斜率是必要约束，不是完整蝶式无套利证书。满足参数限制的SSVI可保证两类无套利，任意原始SVI参数则不能。",
    'f"Now every expiry of the Surface at once':
        "现在一次看曲面的全部到期日：{len(R)}个，从{R[0]['T'] * 365:.0f}天到{Tmax:.0f}天，每个都拟合、求导，在三维中立起来。<bookmark mark='a'/>沿着期限走。山脊在变宽，因为不确定性随时间增长：标准差从今天价格的{100 * R[0]['sd']:.0f}%增加到{100 * R[-1]['sd']:.0f}%。{lean}<bookmark mark='b'/>在每个价值度上，总方差都随期限上升，{verdict}每条脊线分别按自身峰值归一化，因此高度不能比较密度大小。这里是抽样日历检查，不是覆盖所有翼部与到期日的全局证书。",
    "f'And their shape turns":
        '它们的形状也在转变：最短的向左偏，偏度{k0:.2f}，市场在为下跌保护付钱；最长的向右偏，偏度{k1:.2f}，就像一个不断展开的对数正态，因为价格最多跌到零，涨却没有上限。',
    "f'Their skewness goes from":
        '它们的偏度从最短期限的{k0:.2f}变到最长期限的{k1:.2f}。',
    "f'and the checker finds no calendar arbitrage":
        '检查器在任何两个相邻到期日之间都没有发现日历套利。',
    "f'and the checker flags":
        "检查器标出了{term['calendar_total']}处日历违背，公司会先修复它们。",
    'f"How much of a density do the quotes pin down? Fit the same {sp[\'T\'] * 365:.0f}':
        "这些报价能确定多少密度？对相同的{sp['T'] * 365:.0f}日观测，分别拟合SVI、波动率样条、双对数正态和三对数正态混合。<bookmark mark='a'/>vega加权均方根误差最多{sp['rmse_max']:.1f}个波动率点，不是每个报价的最大误差。<bookmark mark='b'/>样条有负曲率，因此不是概率密度。图中只显示缓存的正部，尾部积分不是有效概率。其余拟合候选在有限积分网格上，跌幅百分之三十的尾部积分相差{100 * spread:.2f}个百分点。<bookmark mark='c'/>Shikhman等人2026年的数值条件分析说明：精确期权价格不一定能识别潜在密度。有限报价、数值积分与外推保留了模型设定不确定性；本示例没有对任何拟合做全局认证。",
    " The spline's density even dips below zero":
        '样条的密度甚至跌到零以下，所以检查器拒绝了它。',
    'Pause and predict. Four fits have small weighted quote RMSE. Must their crash pr':
        "暂停预测：四个拟合的加权报价均方根误差都很小，崩盘概率必须相同吗？<bookmark mark='a'/>不必。有限报价与加权平均误差不能识别唯一尾部，外推很重要。密度有负值的拟合应拒绝，不能给它赋予崩盘概率。这些是Q候选，不是实际崩盘预测。",
    'Chapter fourteen. Ross recovery, and its critique.':
        '第14章。罗斯复原及其批评。',
    'Option prices give Q. Can they give P':
        "期权价格给出Q。它们能给出P，也就是市场真正相信的东西吗？斯蒂芬·罗斯在2015年声称能。期权揭示了从状态i转到状态j的价格：真实转移概率乘以贴现因子。<bookmark mark='a'/>罗斯假设贴现因子等于一个贴现率乘以状态的某个函数之比，就像代表性投资者的边际效用。<bookmark mark='b'/>那么真实概率就是重新缩放的状态价格。<bookmark mark='c'/>每行之和必须为1，所以那个函数的倒数是状态价格矩阵的特征向量。<bookmark mark='d'/>佩龙和弗罗贝尼乌斯：这样的矩阵恰好有一个正的特征向量。于是P被确定了，只凭价格。这里的复原假定有限状态的转移价格矩阵严格为正，并且定价核具有转移独立结构。当前单一状态的一组期权并不能提供完整转移矩阵。佩龙—弗罗贝尼乌斯只识别相差尺度的唯一正特征向量；实际概率解释依赖定价核限制。",
    'f"The House finds it the oldest way':
        "公司用最古老的办法找它：拿一个平坦的向量，一次又一次乘以状态价格矩阵，每次重新归一化。<bookmark mark='a'/>它先晃动，然后冻结成佩龙向量，增长因子稳定下来：一步后{lam[0]:.4f}，十步后{lam[9]:.4f}，六十步后{lam[-1]:.5f}，而真实值是{sw['delta']:.2f}。",
    'f"Test it where the truth is known':
        "在已知真相的地方检验：九个状态，一个代表性投资者，正好满足罗斯的假设。<bookmark mark='a'/>复原结果与真相一直吻合到最后一位。<bookmark mark='b'/>现在给贴现因子加一个永久成分，也就是永远不会消散的冲击。答案干净利落，却是错的：它是悲观的，把长期水平放在趋势以下{100 * abs(r['mean_rec2']):.1f}%，而真相是高于趋势{100 * r['mean_true']:.1f}%。这种倾斜把复原出的长期分布推向坏状态，正是风险调整会把它放的地方。",
    'Borovička, Hansen and Scheinkman explain the identification problem. The stochas':
        "Borovička、Hansen和Scheinkman解释了识别问题。随机贴现因子除了状态函数比值，还可包含永久鞅分量。<bookmark mark='a'/>这时佩龙复原得到的是偏离实际概率的长期定价测度，不会自动得到实际概率。将其与长期债券计价单位联系起来，还需要额外长期分解条件。<bookmark mark='c'/>非平凡的永久风险调整无法由这个复原限制识别。本例中的悲观偏移依赖模型；悲观和消费趋势都不是普遍结论。仅有状态价格不能把概率与所有可能贴现因子区分开。",
    'f"How fast does it go wrong?':
        "错得有多快？把永久部分从零开始调大，这里一个经济，再加{sw['n_econ']}个随机经济。<bookmark mark='a'/>在零处，所有经济的复原都精确；然后误差平滑地增长，中位数到{sw['err_med'][-1]:.3f}。没有安全的门槛。这个扫描描述固定的一族合成经济体，并不是说每个永久分量都会产生单调误差或悲观偏移的定理。",
    'The evidence. Jensen, Lando and Pedersen':
        "实证证据。延森、兰多和佩德森在2019年推广了复原。<bookmark mark='a'/>杰克沃斯和门纳，2020年：在标普500期权上，复原出的分布未能预测收益，而简单的基准无法被拒绝。<bookmark mark='b'/>费伦茨·霍瓦特，2025年：一种基于套利的复原，据他报告，在26年里能预测标普500的月度收益分布。<bookmark mark='c'/>争论仍在继续；公司把密度当作价格，而不是预测。",
    'Pause and predict. Recovery gives a gloomy distribution.':
        "暂停预测一下。复原给出了一个悲观的分布。这是投资者悲观的证据吗？<bookmark mark='a'/>不是：永久成分会以同样的方式把它倾斜。价格无法把信念和风险调整分开。如果香草期权确定不了信念，它们能确定什么？下一章：不依赖模型的界。",
    'Chapter fifteen. Bounds without a model.':
        '第15章。不依赖模型的界。',
    'f"A claim on the price at two dates':
        "取决于两个日期价格的收益，要看两者怎样连接，而普通期权的价格不会透露这一点。这是曲面两个到期日的看涨曲线。<bookmark mark='a'/>在所有连接方式中，这个收益的价格有最高值和最低值。<bookmark mark='b'/>一种连接必须同时匹配两个密度，并且是鞅。<bookmark mark='c'/>这样的连接存在，当且仅当后一条看涨曲线处处在前一条之上，这是施特拉森1965年的定理，这里正是如此。剩下的就是线性规划：鞅最优传输。这里前一个边际分布有{len(x)}个原子，后一个有{len(y)}个，所以线性规划有{len(x) * len(y):,}个未知数。这里X等于S1除以F1，Y等于S2除以F2。假定持有成本确定，并有共同定价测度使远期归一化变量成为鞅。支付为Y除以X减一的绝对值，不是原始S2除以S1减一。SVI边缘分布经过截断、归一化、离散化和单位均值缩放，因此这些界以有限网格为条件。",
    'Its dual is a trading strategy.':
        "它的对偶是一个交易策略。乘子：u对应第一个密度，v对应第二个，h对应鞅条件。<bookmark mark='a'/>当成交易来看：第一个日期支付u的期权，第二个日期支付v的期权，中间持有h份标的，无论发生什么都至少支付这个收益。<bookmark mark='b'/>弱对偶：对任何连接积分；交易项平均为零。<bookmark mark='c'/>强对偶，拜格尔伯克、亨利-拉博代尔和彭克纳，2013年：模型价格的最高值，就是最便宜的不依赖模型的超对冲。加利雄、亨利-拉博代尔和图兹把连续时间中的对偶变成了一个控制问题。所以任何占优于这个收益的静态期权组合，加上任何Delta，成本都至少等于每个鞅模型下的价格。有限可行线性规划有精确强对偶。连续版本需要可积性、支持集和可容许条件。图中的对偶只认证这个离散支持集。",
    'The dual in three dimensions.':
        "三维中的对偶。底面是每一对价格；红色曲面是收益，沿对角线是一道山谷。<bookmark mark='a'/>金色曲面是线性规划对偶给出的最优对冲，从高处开始。<bookmark mark='b'/>把它放下来：它在离散支持点上支配收益，成本给出有限网格上界。插值曲面可能在点之间穿过收益。<bookmark mark='c'/>紫色的点，也就是最贵的模型放质量的地方，正好位于接触的地方：这就是看得见的互补松弛。在接触集之外，对冲严格高于收益：这是在极端模型从不到达的状态里多付的钱。曲面在中央窗口对离散对冲进行插值。精确占优和互补松弛在LP支持点认证；插值只是示意，不能认证连续域。",
    'f"The numbers for the normalized claim. The straddle bounds are {lo:.3f} and {up':
        "归一化支付的数值：跨式界为{lo:.3f}和{up:.3f}。<bookmark mark='a'/>用平值远期方差构造的对数正态代理给出{model:.3f}。它恰好位于内部，但不匹配完整边缘分布，不能保证一定在区间内。<bookmark mark='b'/>若X为正、满足可积性且Y给定X的期望等于X，Y除以X减一的期望为零，所以远期起始看涨的极值正好是跨式的一半。二阶矩有限时，平方变化等于两个边缘二阶矩之差。<bookmark mark='c'/>对数比平方的区间有非零宽度，为{cl['logsq']['lower']:.4f}到{cl['logsq']['upper']:.4f}。这些是有限网格的闭优化界，不同于不可复制支付在等价测度下的开定价区间。",
    'Pause and predict. Why is the normalized squared change a single number? <bookma':
        "暂停预测：为什么归一化平方变化只有一个价格？<bookmark mark='a'/>二阶矩有限时，鞅恒等式给出Y平方期望减X平方期望，由边缘分布决定。复制表达式需要两个静态平方支付，还需要在两日之间持有负二X的动态头寸。仅有静态普通期权不能复制交叉项。所有价格都以所述归一化有限支持和可执行支付假设为条件。下一章讨论这些界的数值敏感性。",
    'Chapter sixteen. Finite-grid bounds and numerical sensitivity.':
        '第十六章，有限网格界与数值敏感性。',
    'f"Here is the existing linear program for the finite, forward-normalized margina':
        "这是有限、远期归一化边缘分布的已有线性规划。每对价格一个未知量，约束规定边缘分布和鞅条件。<bookmark mark='a'/>最小化和最大化归一化支付。{n1}乘{n2}的支持集给出{n1 * n2:,}个未知量，界为{m['lower']:.3f}到{m['upper']:.3f}。凸序检查描述的是离散化拟合边缘分布；若不可行，说明这些输入不一致，不能自动证明异步市场报价中存在可执行套利。",
    'f"The band depends on the discretization. Refine the existing grids from nine by':
        "价格带依赖离散化。已有网格从9乘25细化到81乘361个原子。<bookmark mark='a'/>算出的端点从{lo[0]:.3f}、{up[0]:.3f}移到{lo[-1]:.3f}、{up[-1]:.3f}。这些重新分箱并不嵌套，边缘测度也变了，因此可行集没有包含关系。<bookmark mark='b'/>本例最后两个网格较接近。这是敏感性检查，不是单调收敛证明，也不是连续域误差界。平值对数正态代理恰好位于区间内；它并不复制两个完整拟合边缘分布，未必是可行的校准模型。",
    'It widens: a coarse grid cannot represent':
        '区间变宽了：粗网格表示不了最极端的连接方式。',
    'It narrows as the grid refines.':
        '随着网格细化，区间变窄了。',
    'A second method scales to far bigger problems.':
        "第二种方法能扩展到大得多的问题。给连接方式偏离独立的程度加一个小惩罚，也就是权重为epsilon的熵。<bookmark mark='a'/>最优连接于是有了一个显式的指数形式，对偶变量在指数里。<bookmark mark='b'/>固定其他变量，每个u都有闭式解，是一个和的对数，每个v也一样：这就是Sinkhorn矩阵缩放。<bookmark mark='c'/>鞅乘子h没有闭式解，但每一个都是单变量方程的根，用一步牛顿法求。三者轮流更新，缩小epsilon，值就逼近线性规划的值。惩罚还让问题变成严格凹的，所以解是唯一的，并随数据平滑变化。这些有限网格公式假定参考质量为正、可行集非空；完全求解的熵问题有唯一最优解。有限次坐标迭代有残差，缩小epsilon本身不能证明有限运行已经收敛。",
    'f"For the existing upper-side runs, shrink epsilon from a tenth to three thousan':
        "对已有的上界侧运行，把epsilon从0.1缩到0.003。<bookmark mark='a'/>图中画的是不含熵罚项的期望支付，不是调整后的目标值。数值为{runs[0]['value']:.4f}、{runs[1]['value']:.4f}、{runs[2]['value']:.4f}、{runs[3]['value']:.4f}，LP为{m['upper']:.4f}。<bookmark mark='b'/>这些运行终止时最大的L1边缘误差为{max((r['trace'][-1][2] for r in runs)):.1e}，最大的L1鞅误差为{max((r['trace'][-1][3] for r in runs)):.1e}。可行耦合不能超过LP最大值，但有限容差仍很重要。虽然熵参考是乘积测度，独立性本身一般违反鞅条件。回放省略零次迭代时尚未约束的初值，从下一个记录的扫描开始。其余缓存支付完整显示，不按分位数压平；早期不可行迭代可超过LP值。左图快照是各epsilon最终耦合，不是全部中间迭代。",
    'Pause and predict. Can a finer grid give a lower upper endpoint? <bookmark mark=':
        "暂停预测：更细网格的上端点能否下降？<bookmark mark='a'/>能。重新分箱改变了边缘测度，因此没有必然顺序。单调性需要其他输入相同且可行集嵌套。应报告离散化和数值残差。",
    'Chapter seventeen. How arbitrage is traded, and why it is limited.':
        '第17章。套利怎样做，为什么受限。',
    'Who enforces the law of one price?':
        "谁在执行一价定律？ETF的份额和它持有的证券都在全天交易。授权参与者，也就是大型交易商，在基金偏贵时交付一篮子证券来创设份额，偏便宜时赎回份额；美国证监会在2019年把这个流程标准化了。<bookmark mark='a'/>它一直有效，直到套利者自己的资本成为约束。2020年3月，流动性最好的债券基金相对持仓大幅折价，越安全的债券折价越大，哈达德、莫雷拉和缪尔记录了这一点：投资者卖出最容易卖的东西，而交易商的资产负债表已经满了。算一个例子：如果基金比一篮子证券贵1%，授权参与者就买入篮子、交付换取新份额再卖出，赚到1%减去成本，而这些卖出把价格推回来。债券ETF持仓估值可能滞后或依赖估计，申赎篮子可能不同于公布持仓，成本与资产负债表约束也很重要。报告的净值折价并不自动构成可执行套利。",
    'f"The box spread as a business.':
        "箱式组合是一门生意。在纽约联储，范宾斯伯根、戴蒙德和范塔塞尔发现，1996到2023年，箱式利率平均比国债高35个基点。<bookmark mark='a'/>这个差距是国债的便利收益，范宾斯伯根、戴蒙德和格罗泰里亚测出约40个基点，金融危机时翻了两番。<bookmark mark='b'/>现在有一只基金专门通过箱式组合放贷：BOXX，2022年底成立，据它的年报，到2025年9月持有80亿美元。<bookmark mark='c'/>第1章的加密版本，差距只有{fb['gap_p50']:.1f}个基点。35基点估计对应1996年至2023年4月的特定样本，约40基点来自另一项研究，并非同一估计。抵押、税费、结算与交易成本不同。本课加密市场比较使用异步观测。",
    "Convergence trades with funding and event risk. Royal Dutch and Shell's economic":
        "收敛交易存在融资与事件风险。荷兰皇家和壳牌的经济分配为六比四，但1980至1995年相对平价的平均绝对偏差约百分之九点五。<bookmark mark='a'/>负残值交易还有另一风险：Mitchell、Pulvino和Stafford报告，其样本约百分之三十在收敛前关联就被切断。<bookmark mark='b'/>借券可用性、召回、资本与事件风险，都可能使理论上吸引人的价格关系无法成为无风险可执行交易。",
    'f"Shleifer and Vishny, The Limits of Arbitrage, 1997':
        "施莱弗和维什尼，《套利的极限》，1997年：套利者投资的是别人的钱，别人按最近的收益评判他们。来模拟一下：一个注定在第20期前收敛的错误定价，一只加了杠杆的基金，投资者在任何亏损后撤回a倍的亏损。<bookmark mark='a'/>当错误定价扩大，资本被撤走，碰到保证金下限时基金被清算，错过了它本来判断正确的收敛。<bookmark mark='b'/>每种情形一千条路径：{verdict}资金流等于亏损时，{100 * r1['p_liq']:.1f}%被清算；两倍于亏损时，{100 * rows[-1]['p_liq']:.1f}%。<bookmark mark='c'/>而清算发生在错误定价最大的时候：限制套利的是资金，不是眼光。第20期必然收敛是这个简化模拟强加的条件。清算比例依赖固定参数，不是实证估计，也不能证明一般因果效应大小。三条示例路径保留全部缓存价差和资本范围；表格汇总另一组固定模拟路径。",
    'without flows, none are liquidated.':
        '没有资金流时，没有一只被清算。',
    "f'even without flows,":
        "即使没有资金流，也有{100 * rows[0]['p_liq']:.1f}%被清算。",
    'The crisis file: Long-Term Capital Management':
        "危机档案：长期资本管理公司，1994年由约翰·梅里韦瑟创立，收益率依次为20%、43%、41%和17%，交易它预计会收敛的价差。总统金融市场工作组报告：1998年初它有48亿美元的权益，对应1290亿美元的资产，杠杆资产／权益约27倍。<bookmark mark='a'/>俄罗斯违约之后，价差扩大了；它仅8月就亏损44%。9月23日，纽约联储召集的14家机构出资36亿美元，换取基金90%的股份。没有动用美联储的钱。第41部分会讲完整的故事。本部分的教训：每一笔收敛交易，都是一个暗藏融资假设的无套利论证。",
    'Pause and predict. A trade is certain to converge.':
        "暂停预测一下。一笔交易注定会收敛。什么决定了它还会不会让你破产？<bookmark mark='a'/>你的资金期限与收敛所需的时间相比，再加上途中的亏损。最后，前沿。",
    'Chapter eighteen. The frontier, 2023 to 2026.':
        '第18章。研究前沿，2023到2026年。',
    "Three directions in recent transport work. Neufeld and Sester's 2023 paper learn":
        "近期传输研究的三个方向。Neufeld和Sester的2023年论文从市场输入学习模型无关界，以离线训练支持快速在线定价，也研究固定边缘MOT。神经罚项方法建立在更早工作之上，包括Eckstein与Kupper。<bookmark mark='a'/>Hasenbichler、Joseph、Loeper、Obloj和Pammer研究鞅Sinkhorn，在论文的矩与可行性假设下寻找连接边缘分布且最接近布朗运动的鞅。<bookmark mark='b'/>Engstrom、Kallblad和Karlsson利用序列结构与熵正则化处理多边缘问题，包括回望和亚式例子。下面的计算演示神经对偶罚项求解器，并非复现某篇论文的完整实证研究。",
    'f"The House restores the existing neural dual illustration. Three networks repre':
        "House恢复已有神经对偶示例。三个网络表示静态支付u、v，以及两日间头寸h。损失等于原始对冲成本加加权平方短缺罚项。<bookmark mark='a'/>左图在中央窗口抽样显示对冲减支付：红色为违反，金色为高于。右图画三个固定种子的原始成本，保留全部缓存范围。<bookmark mark='b'/>初始成本低于LP值，罚项优化随后大幅超调到高成本，再回到LP附近。{verdict}<bookmark mark='c'/>对这个小型有限问题，线性规划精确且更快。神经近似可帮助更大问题，但需要独立检查可行性与优化。很小的加权平均短缺或密集采样窗口，都不能认证整个连续域。",
    'f"All three land just above':
        '三个种子都落在线性规划的界上方一点，高出{min(gaps):.2f}%到{max(gaps):.2f}%：光滑的网络画不准对冲的拐点。',
    'f"They land within':
        '它们落在线性规划的界{max((abs(g) for g in gaps)):.2f}%以内，两侧都有：惩罚过的约束不是保证。',
    "Beyond transport: Guyon's 2024 framework studies joint SPX and VIX calibration a":
        "传输之外，Guyon的2024年框架研究SPX与VIX联合校准，以及其约束下的无套利可行性问题。<bookmark mark='a'/>Neufeld、Papapantoleon和Xiang推导多资产超对冲界，并用半无限规划计算，包括60资产的例子。<bookmark mark='b'/>Bartl、Beiglbock和Pammer发展适应Wasserstein几何，包括其过程空间中鞅的闭性与测地凸性。<bookmark mark='c'/>Heston、Jacobs和Kim发现，仅凭期权拟合区分经济性质不同的定价核，统计功效较低。单调性与路径独立限制在其经验模型内消除异常。Horvath的复原研究与Shikhman等人的逆密度分析是另外两个例子；各项结论都依赖自身模型、数据与假设。",
    'Pause and predict. When is a neural dual cost a certified upper bound? <bookmark':
        "暂停预测：神经对偶成本何时才是经认证的上界？<bookmark mark='a'/>必须先证明对冲在支付的整个支持集上占优。罚项并不强制满足约束。有限支持上逐对检查可认证离散问题；密集抽样本身不能认证连续域。",
    'f"The House\'s arbitrage checker holds the tools: <bookmark mark=\'a\'/> parity dia':
        "House套利检查器汇集了这些工具：<bookmark mark='a'/>平价诊断、状态价格、超复制、抽样静态与日历检查、有限网格传输界，以及带假设说明的罗斯复原。<bookmark mark='b'/>第十条规则是检查拟合价格与输入一致性，修复或拒绝被标记曲面，并区分数值诊断与可执行套利。本部分恢复已有计算及回顾性得分示例。计数为{env['trials']}，没有新增注册试验，也没有打开留出集。",
    'Part nine in ten lines. Parity diagnoses matching payoff prices under trading as':
        '第九部分十条要点。平价在交易假设下诊断同支付价格。借券约束改变价格界。有限状态无套利等价于严格正状态价格存在。给定P后，状态价格定义贴现因子与Q。完备模型复制支付，不完备模型给出区间。足够多独立支付可使有限市场完备。连续时间需要可容许性与NFLVR。计价单位变换要求均值为一的密度。完整价格曲线的曲率识别测度，有限报价则需拟合假设。复原依赖定价核限制，传输对指定边缘分布给出条件价格界。',
    'Four desk questions. The call at ten and put at seven satisfy parity: both sides':
        "四个交易台问题。看涨10、看跌7满足平价，两边都是3；这是在匹配交易假设下检查这一关系。<bookmark mark='a'/>一年后支付10、利率百分之四的欧式箱式组合约值9.61；美式提前行权可能破坏固定支付。<bookmark mark='b'/>宽度为一的看涨价差成本为0.5，只是数字期权近似；两个有限报价不能唯一确定精确价格。执行价处连续时，价差收窄趋于看涨价格斜率的负值，并包含贴现。<bookmark mark='c'/>负残值交易遇到借券、召回、融资期限与事件风险时，并不是无风险可执行交易。讲义列出假设与计算。",
    'And nine problems':
        '还有九道习题：含借券费用的平价，由施蒂姆克引理证明定理，二叉树概率，蝶式价差与密度，三叉区间及其对偶，远期开始看涨期权的区间，以及用计价单位变换推导马格雷布公式。其中两道是资格考试题：分数布朗运动的记忆，以及有成本时的最佳交易频率。中英文解答见笔记。',
    'Where this comes back:':
        '这些内容会在哪里再出现：第10部分的布莱克、斯科尔斯和默顿；第12部分的波动率曲面；第14和15部分的奇异期权；第18和19部分的远期测度；第23部分的贴现因子；第21和41部分的融资与危机；第38部分的ETF。最重要的是，第10部分会把本部分的连续时间定理变成一个公式和一个可以运行的对冲。',
    'The textbooks and papers provide the theorem assumptions and published observati':
        '教材与论文提供定理假设和已发表的观测。数值例子使用已有固定种子计算，市场示例使用已登记数据源。',
    'The House can now tell a price from an arbitrage.':
        "我们的公司现在能分辨价格与套利了。<bookmark mark='a'/>下一部分，第10部分：布莱克、斯科尔斯和默顿，波动率交易台随之开张。",
    'For the researcher: fractional Brownian log prices and trading frictions. With H':
        '研究者部分：分数布朗对数价格与交易摩擦。H不等于二分之一时，价格指数不是半鞅，经典无摩擦随机积分需要谨慎处理。我们先区分符号增量得分和投资财富，再介绍交易成本下排除套利的一致价格系统条件。',
    'Take fractional Brownian motion as a log price, with H strictly between zero and':
        "把分数布朗运动作为对数价格，H严格介于零与一之间。<bookmark mark='a'/>协方差如图；H等于二分之一时就是普通布朗运动。<bookmark mark='b'/>等长相邻增量的相关系数在每个尺度都相同，等于二的二H减一次方再减一。<bookmark mark='c'/>低于二分之一时二次变差发散，排除连续半鞅。高于二分之一时二次变差为零，这还不够：分数布朗运动的总变差也无限。而二次变差为零的连续半鞅必须有有限变差。因此H不等于二分之一时不是半鞅。经典套利结果还需要规定交易策略和可容许条件。",
    'Consider a sign-increment score, not a self-financing investment return. <bookma':
        "考虑符号增量得分，它不是自融资投资收益。<bookmark mark='a'/>每步使用上一对数增量的符号，正相关时跟随，负相关时反向。<bookmark mark='b'/>对相关正态变量，用条件期望和正态绝对值均值可以算出图中的单步期望。<bookmark mark='c'/>若这些得分独立，把单步均值和方差年化，会得到这里的根号n参考线。但得分存在依赖，公式忽略序列协方差。正均值或发散的参考夏普比率都不能证明套利。罗杰斯和切里迪托研究的是特定策略类别下分数市场的实际套利。",
    "Here are the existing simulations without costs. <bookmark mark='a'/> Dots show ":
        "这是已有的无成本模拟。<bookmark mark='a'/>点表示160条独立一年路径中，年度得分均值除以样本标准差。<bookmark mark='b'/>线把单步矩当作得分独立来年化，只是参考，并非精确年度风险公式。<bookmark mark='c'/>H等于二分之一时条件均值优势为零。点与线的差异包含依赖和有限样本误差；这些得分不能证明可容许投资套利。",
    "Now charge a linear turnover penalty in the score proxy. <bookmark mark='a'/> Th":
        "现在给代理得分加上线性换手惩罚。<bookmark mark='a'/>相邻增量符号不同时，头寸变化为二。正态对的谢泼德公式给出翻转概率。<bookmark mark='b'/>减去epsilon乘换手，忽略初始和终止边界项，得到图中的均值得分m(n)：单步毛优势缩小，而换手收费不变。<bookmark mark='c'/>求导得到有限最优频率。它只优化这个特定代理均值，不能证明无套利，也不是指数价格市场中比例交易成本下的精确财富。",
    "f'Here it is at H of point six.":
        "这是H为零点六的情形。<bookmark mark='a'/>没有成本时，均值一直上升，冲出图表顶部。<bookmark mark='b'/>一个基点时，它在每年约两千三百次交易处达到峰值，约为{100 * b1['mean']:.0f}%，超过一万次后变为负值。<bookmark mark='c'/>十个基点时，峰值约在每年五十次交易，为{100 * b10['mean']:.0f}%。模拟落在公式上。图中的百分比表示对数增量得分单位，不是投入财富的收益率。各收费情景都使用相同的固定模拟。",
    'A consistent price system gives a sufficient condition for no arbitrage with a s':
        "一致价格系统给出有价差时无套利的充分条件。<bookmark mark='a'/>要求存在等价概率测度，以及在每个时刻都位于贴现买卖价之间的局部鞅，并配以通常可容许条件。逆向结果还需要其他假设。这里的乘法价差不同于前面的线性得分收费。<bookmark mark='b'/>有条件全支持的严格正连续过程，对任意小的正价差都有这样的系统。条件全支持是指，每条正连续未来路径的任意一致邻域都有正条件概率。分数布朗运动的指数满足条件。<bookmark mark='c'/>粗糙波动率把粗糙性放在方差中。随机积分价格仍可为半鞅，但这一点本身不能证明无套利；仍需有效定价测度和可容许条件。",
    'f"What do existing Bitcoin observations show? These are 2019 and 2020 log increm':
        "已有比特币观测说明什么？这里使用2019和2020年的对数增量，采样间隔为1、5、15、60分钟。<bookmark mark='a'/>全样本相关系数很小且为负。反演分数公式只得到一个标为隐含H的数，并不能证明价格遵循分数布朗运动。同一全样本还选择了反向交易方向，因此这是回顾性展示。<bookmark mark='b'/>表中报告已有的符号增量得分、线性换手收费的盈亏平衡点，以及收取1基点后的得分。<bookmark mark='c'/>这些只是描述性结果，没有未触碰的预测检验，并忽略执行价差、冲击和融资。一致价格系统定理既不预测测得的相关系数，也不预测其盈亏平衡收费。",
    "Three project research directions. <bookmark mark='a'/> For a specified fraction":
        "三个项目研究方向。<bookmark mark='a'/>对指定的分数价格模型和价差，构造一致价格系统及实用的超复制价格带。<bookmark mark='b'/>在明确的记忆、成本和可容许条件下求解效用问题，研究小成本行为。<bookmark mark='c'/>实证扩展应预先定义方向和采样选择，再在未触碰数据上检验信号能否覆盖执行成本。本课没有进行这种新检验。",
    'Pause and predict. At H of point six, one basis point gives a best proxy frequen':
        "暂停预测：H为0.6时，1基点收费给出每年约2300次的代理最优频率。收费翻倍，最优频率变为多少倍？<bookmark mark='a'/>公式给出二的负一除以H次方，约0.315。频率降至每年约730次；结论仅限这个均值得分近似。",
}

ZH.update({'These are comparisons of observations over the same hours.': '这些观测来自同一时段。没有同时可执行的买卖价、融资与费用，不能证明存在现金持有套利利润。'})

ZH.update({"f'Raw dual costs differ from the LP": '原始对偶成本与LP相差{min(gaps):.2f}到{max(gaps):.2f}百分比。加权平均正短缺为{min(deficits):.5f}到{max(deficits):.5f}。这不是最大违反量，不能认证超对冲。此次运行未分离逼近、优化与罚项误差。'})

ZH.update({'and the checker flags no violation at the sampled moneyness points between neighboring expiries.': '检查器在相邻到期日之间的抽样价内程度点上没有标记违反。'})
