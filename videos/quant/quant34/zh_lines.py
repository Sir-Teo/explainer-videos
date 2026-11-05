"""Chinese narration for quant34: see tools/zh_lines.py (literal lines by prefix). Terms follow
videos/quant/QUANT_ZH_GUIDE.md; new terms of this part: 自营交易 (proprietary trading), 做市商 (market maker), 多策略平台
(multi-manager platform), 投资团队/组 (pod), 基金经理 (portfolio manager), 回撤止损 (drawdown stop), 波动率预算
(volatility budget), 费用转嫁 (pass-through fees), 轧差风险 (netting risk), 孵化 (incubation), 预交易检查 (pre-trade
checks), 熔断开关 (kill switch), 幌骗 (spoofing), 分层挂单 (layering), 尾盘操纵 (marking the close), 对敲交易 (wash
trades), 订单流付费 (payment for order flow), 合并审计追踪 (Consolidated Audit Trail), 量化私募 (China's quant private
funds), 停止时间 (stopping time), 反射 (reflection)."""

TITLE = '量化金融，从零搭建 · 第34部分：走进量化公司'

CHAPTERS = {
    'Hook': '一个席位能坐多久',
    'Models': '1. 量化公司的六种形态',
    'Disclosed': '2. 公司披露了什么',
    'Pods': '3. 多策略平台模式',
    'Process': '4. 从想法到资本',
    'Risk': '5. 公司层面的风险',
    'Tech': '6. 技术',
    'Compliance': '7. 监控与案例',
    'Interview': '8. 面试',
    'Culture': '9. 公开讲述的创业故事',
    'Stops': '10. 回撤止损有用吗？',
    'House': '11. 第34条规则：公司',
    'Research': '写给研究者：一个席位能坐多久，精确解',
    'Outro': '回顾、交易台问题与习题',
}

ZH = {

    # ------------------------------------------------------------------ Hook
    "Part thirty-four. Inside a quant firm":
        "第34部分。走进量化公司：运作这些策略的公司如何搭建、如何付酬、如何治理、如何受监管，以及决定一个交易员能保住席位多久的那套算术。",

    'f"A manager joins a platform.':
        "一位基金经理加入一个平台。他们真实的夏普比率是一，非常优秀，运行百分之十的波动率。规则，正如各大平台的规则被报道的那样：从高点回撤百分之五，组合就被削减。"
        "<bookmark mark='a'/>看着损益和它的历史高点。<bookmark mark='b'/>平均来说，这么优秀的基金经理能保住满额组合多久？"
        "答案是精确的，大约{months:.0f}个月。这一部分讲的是设定这类规则的公司，以及它为什么仍然要设定它们。",

    'f"Three things this part shows.':
        "这一部分展示三件事。<bookmark mark='a'/>一家做市商披露，一千二百三十八个交易日里只有一天亏损。"
        "在正态模型下，这相当于日度夏普比率{v['normal']:.1f}，每年约{v['annual']:.0f}：不是天才，而是把大数定律用在数以百万计的小交易上。"
        "<bookmark mark='b'/>半个波动率深的止损，平均{12 * S1[0]:.1f}个月就会让一位夏普为一的基金经理止损出局；一个波动率深的止损，需要{S1[2]:.1f}年。"
        "席位的寿命随夏普比率乘以止损深度呈指数增长。<bookmark mark='c'/>而公司仍然要止损，因为技能是未知的："
        "止损是一种检验，它淘汰差的基金经理比淘汰好的更快。在模拟的平台上，投资者的夏普比率从{s_off:.2f}升到{s_on:.2f}。",

    "Where this sits. Parts thirty to thirty-three":
        "这一部分在系列中的位置。第30到33部分构建了组合、风险模型和策略。这一部分退后一步，看运作它们的公司："
        "它的商业模式、资本、风险限额、技术、合规部门，以及它招聘的人。它用到第8部分的回撤控制、第26部分的多重检验和第31部分的容量。",

    "The firms, by founding date":
        "按成立年份排列的公司，来自公开记录。1969年的Princeton/Newport；1982年的文艺复兴；1988年的D. E. Shaw；1989年的Millennium。"
        "<bookmark mark='a'/>1990年的Citadel；1998年的AQR；2000年的Jane Street；2001年的Two Sigma；2008年的Virtu。"
        "<bookmark mark='b'/>还有公司的另一段历史：2012年骑士资本的四十五分钟、幌骗案件，以及随之而来的规则。",

    "The plan: six business models":
        "本部分的安排：六种商业模式；公司披露了什么以及意味着什么；多策略平台模式，模拟一遍；一个想法如何变成资本；公司层面的风险；技术；"
        "监控与案例；面试；公开讲述的创业故事；回撤止损在真实溢价上是否有用；以及基金经理能保住席位多久的精确公式。",

    "In the House, this part builds the compliance desk":
        "在本系列公司里，这一部分建立合规部门，并把各交易台一直在遵守的公司层面规则写下来：限额、止损、审查，以及每一次试验的记录。",

    # ------------------------------------------------------------------ Models
    "Chapter one. Every quant firm answers three questions":
        "第一章。每家量化公司都要回答三个问题：交易谁的钱，出售什么优势，成功时谁拿报酬。六种答案覆盖了这个行业的大部分。",

    "The economics in one line.":
        "一句话的经济学。<bookmark mark='a'/>利润等于优势乘以容量，减去成本，而第31部分表明容量是有限的。"
        "<bookmark mark='b'/>用自有资本交易的公司拿走全部利润，也承担全部风险。"
        "<bookmark mark='c'/>用投资者资本交易的公司收取费用，按资产和利润的一定比例，这改变了它想要的规模。",

    "First, proprietary trading firms.":
        "第一，自营交易公司。<bookmark mark='a'/>Jane Street、Hudson River Trading、Jump Trading和XTX Markets用合伙人自己的资本交易数以千计的品种，"
        "主要靠报价，以及预测接下来几秒或几分钟。<bookmark mark='b'/>它们出售的是即时性，第33部分的那个词：给任何想现在交易的人一个价格。"
        "它们赚取价差，扣掉比它们掌握更多信息的交易者拿走的部分，再扣掉交易所的费用。第38部分会建立这个模型。",

    "Second, the market makers, overlapping":
        "第二，做市商，与第一类有重叠。<bookmark mark='a'/>Citadel Securities、Virtu和Optiver在交易所做市，有些还承接券商转来的散户订单。"
        "<bookmark mark='b'/>Virtu是上市公司，所以它的收入和交易日都在公开文件里；第二章会读其中一份。其余大多数只通过债券发行、法庭案件和监管命令披露信息。",

    "One part of the market-making business":
        "做市业务中有一部分值得单独一张卡片。<bookmark mark='a'/>在美国，批发做市商向零售券商付费，购买其客户的订单。"
        "散户订单不太可能带有信息，所以与之交易的成本更低，而这笔费用让券商可以提供零佣金交易。"
        "<bookmark mark='b'/>利益冲突在于：券商对客户负有最佳执行义务，却同时从成交该订单的公司那里收钱，而这些付款必须披露。"
        "<bookmark mark='c'/>别处的答案不同：英国监管机构从2012年起认为这种做法与其规则不符，欧盟则同意在2026年年中前逐步取消。",

    "Third, the multi-manager platforms.":
        "第三，多策略平台。<bookmark mark='a'/>Millennium、Citadel、Balyasny和Point72运营着数百个独立团队，称为投资组，每个都有自己的资本、风险限额和回撤止损，"
        "由一个中央风险部门统管。<bookmark mark='b'/>据报道，很多平台向投资者收取转嫁费用：平台的成本，包括支付给团队的报酬，都计入基金，再加上业绩报酬。"
        "第三章会模拟这给投资者留下多少。",

    "Fourth, the systematic funds.":
        "第四，系统化基金。<bookmark mark='a'/>文艺复兴、D. E. Shaw、AQR、Two Sigma和Man集团的AHL，用一个研究流程运作多个模型、覆盖多个资产类别。"
        "<bookmark mark='b'/>它们覆盖了本系列的整个范围：快速的统计套利，较慢的因子与趋势组合。它们的费用也覆盖了整个范围，"
        "从因子基金的零点几个百分点，到据报道文艺复兴大奖章基金的百分之五资产费和百分之四十四业绩费。",

    "Fifth, the banks.":
        "第五，银行。<bookmark mark='a'/>银行仍然做电子化做市，并向客户出售量化指数策略，但沃尔克规则限制了它们的自营交易，几个自营团队离开了，其中包括2012年摩根士丹利的PDT。"
        "<bookmark mark='b'/>银行的资产负债表融资便宜但监管严格，第21部分的资本规则给每个头寸都定了价，所以银行保留了客户业务，而独立公司承担了风险。",

    "Sixth, China's quant private funds.":
        "第六，中国的量化私募。<bookmark mark='a'/>私募发行的基金，交易A股、股指期货和商品，很多成立于2010年代，据报道最大的管理着数百亿元人民币，"
        "出售指数增强产品：跑赢中证500或1000指数。<bookmark mark='b'/>它们在不同的约束下运作：T+1结算、做空受限、每日涨跌停，"
        "以及在第29部分提到的2024年2月小盘股回撤之后，据报道对高频交易和直接市场接入交易的新限制。",

    "Side by side.":
        "放在一起比较。<bookmark mark='a'/>谁的资本，什么优势，一个头寸持续多久。这一部分其余内容讲的是六者共有的机制："
        "资本如何交给交易员又如何收回，想法如何变成资本，以及公司如何让交易员守规矩。",

    "Pause and predict. A fund charges two percent":
        "暂停并预测。一只基金收取百分之二的资产管理费和百分之二十的业绩报酬，扣费前赚百分之十。一个平台转嫁百分之六的成本，再拿走剩余部分的百分之二十。哪个给投资者留下的更多？",

    # ------------------------------------------------------------------ Disclosed
    "Chapter two. Quant firms are private":
        "第二章。量化公司对方法守口如瓶，但并非沉默：上市公司要报送账目，私人公司借钱时必须向贷款人展示数字，书籍和法庭案件补上其余部分。文件里的一个数字可以说明很多。",

    "The number. <bookmark mark='a'/> In 2014 the market maker":
        "这个数字。<bookmark mark='a'/>2014年，做市商Virtu Financial申请上市。它的注册说明书报告，从2009年到2013年，在一千二百三十八个交易日中只有一天亏损，"
        "并把这归功于风险管理和技术。媒体把它当作轰动新闻。它究竟意味着什么？",

    'f"Read it as a Sharpe ratio.':
        "把它读成一个夏普比率。<bookmark mark='a'/>如果每日损益服从正态分布，亏损日的比例就是在负的日度夏普比率处的正态尾部概率。"
        "<bookmark mark='b'/>一千二百三十八分之一，对应日度比率{v['normal']:.2f}，每年约{v['annual']:.0f}。"
        "<bookmark mark='c'/>只亏一次是很小的样本，所以取亏损率的置信上限：它仍然意味着每年超过{v['annual_lower']:.0f}。一只好基金的水平是一到二。",

    'f"And if the daily profit has fat tails?':
        "如果每日利润有厚尾呢？<bookmark mark='a'/>用自由度为四的学生t分布，同样的亏损率需要日度比率{v['t4']:.1f}。"
        "<bookmark mark='b'/>自由度为三时，{v['t3']:.1f}。<bookmark mark='c'/>厚尾让大的偏离更可能出现，所以同样罕见的亏损需要更大的均值，隐含比率随之上升。"
        "正态的解读是保守的：无论分布形状如何，日度比率都在三以上。",

    'f"Where such a ratio comes from.':
        "这样的比率从哪里来。<bookmark mark='a'/>给每笔交易一个微小的优势，只有其自身标准差的百分之一：一枚正面朝上概率为百分之五十点四的硬币。"
        "<bookmark mark='b'/>每天一百笔独立交易，{ys[0]:.0f}%的日子亏损。一万笔，{ys[2]:.0f}%。十万笔，{ys[3]:.2f}%，大约两千天才亏一天。"
        "公司的日度夏普比率等于单笔交易的比率乘以交易笔数的平方根。这就是这个统计量的全部秘密，也是它的局限：它需要海量的、几乎独立的小赌注。",

    "Turn it around.":
        "反过来看。<bookmark mark='a'/>要得到三点一五的日度比率，每天需要的独立交易笔数，等于这个比率除以单笔比率再平方。"
        "单笔比率为百分之五时，约四千笔；为百分之一时，约十万笔。真实的交易彼此相关，所以公司需要更多。做市商的优势不是预测，而是一座工厂。",

    'f"What the number does not mean.':
        "这个数字不意味着什么。<bookmark mark='a'/>一只夏普比率为二的基金，有{100 * fl['2']:.0f}%的日子亏损：从内部看，一只出色的基金感觉像抛硬币。"
        "这两种业务在这个统计量上不可比。<bookmark mark='b'/>做市商的容量是到来的订单流；资本翻倍并不会让交易翻倍。"
        "<bookmark mark='c'/>而一天的交易利润是在固定成本之前的：薪酬、数据、会员资格和机器，每天都要付。",

    "A private firm's numbers reach the public":
        "私人公司的数字在它借钱时才会公开。<bookmark mark='a'/>彭博在2024年报道，为Jane Street发债准备的文件显示，其2023年净交易收入约一百零六亿美元，"
        "后来的报道称2024年接近二百亿美元。这些是媒体对发行文件的解读，公司是私人公司；它们显示了出售即时性这门生意的规模。",

    "And the most famous number.":
        "还有最有名的数字。<bookmark mark='a'/>Gregory Zuckerman关于文艺复兴的书报道，大奖章基金从1988年到2018年，扣费前平均每年约百分之六十六，扣费后百分之三十九。"
        "这些是年度收益的算术平均，而这只基金一直保持小规模，从2000年代中期起只对公司自己的员工开放：第31部分的容量，被主动选择。",

    'f"Check the two numbers against each other.':
        "把这两个数字互相核对。<bookmark mark='a'/>净收益等于毛收益，减去管理费，再减去剩余部分的业绩报酬。"
        "<bookmark mark='b'/>按报道中后来年份的费率，百分之五和百分之四十四，百分之六十六的毛收益给出{100 * net:.0f}%的净收益。"
        "<bookmark mark='c'/>报道的百分之三十九很接近：早年的费率较低，而年度收益的平均并不精确复利。两个报道的数字彼此一致。",

    "How to read the public record.":
        "如何解读公开记录。<bookmark mark='a'/>把每个披露的数字变成一个统计量，配上模型和样本。"
        "<bookmark mark='b'/>问它排除了什么：固定成本、费用、记录开始之前的年份，以及已经关闭的基金。"
        "<bookmark mark='c'/>并把公司和基金区分开：公司的利润包括它的费用，投资者的收益在费用之后。",

    "Pause and predict. A firm has five losing days":
        "暂停并预测。一家公司在一千二百五十天里有五天亏损。在正态模型下，这意味着怎样的日度和年度夏普比率？",

    # ------------------------------------------------------------------ Pods
    "Chapter three. The fastest-growing kind of hedge fund":
        "第三章。过去十年增长最快的对冲基金形态是平台：一家中央公司雇用数百个小团队，给每个团队一份资本，并按规则收回。它的算术就是回撤止损的算术。",

    "The structure. <bookmark mark='a'/> A pod is a manager":
        "结构。<bookmark mark='a'/>一个投资组是一位基金经理、几位分析师和一份风险预算，通常以波动率而不是金额设定。"
        "<bookmark mark='b'/>中央提供资本、融资、执行和风险系统，并对冲各组共有的因子暴露。"
        "<bookmark mark='c'/>整个组合是许多小的、几乎独立的优势之和：第31部分的广度，被组织成一门生意。",

    "The rule that makes it work.":
        "让它运转的规则。<bookmark mark='a'/>《华尔街日报》在2024年报道，在Millennium，一位从高点亏损百分之五的基金经理可能被削减一半资本，"
        "亏损百分之七点五可能被解聘。第8部分为一位投资者建立了回撤底线。这里的问题是，这样的规则多久触发一次，以及它对一家有数百位基金经理的公司意味着什么。",

    "How a pod is sized.":
        "一个投资组的规模如何确定。<bookmark mark='a'/>它得到资本和一份波动率预算，头寸按比例缩放，使其利润的预测波动率等于预算。"
        "<bookmark mark='b'/>十亿美元、百分之五的预算，以及自身波动率为百分之八的策略：这个组运行十亿的八分之五作为风险加权头寸。"
        "<bookmark mark='c'/>而止损，资本的百分之七点五，深度是一点五个预算。研究章节表明，决定这个组能存续多久的是这个比率，而不是止损本身。",

    'f"How investors pay.':
        "投资者如何付费。<bookmark mark='a'/>传统基金收取固定费用，比如百分之二，然后拿走利润的五分之一：在百分之十五的毛收益上，剩下{100 * fund:.1f}%。"
        "<bookmark mark='b'/>一个转嫁成本的平台，包括它付给各组的报酬，然后再拿五分之一：成本为百分之六时，剩下{100 * pt:.1f}%。"
        "<bookmark mark='c'/>只有毛收益又高又稳时，转嫁模式才行得通，而这正是止损的用途。",

    "The simulation. <bookmark mark='a'/> Two hundred seats":
        "模拟。<bookmark mark='a'/>两百个席位，三十年。每位基金经理真实的夏普比率在被雇用时抽取，平台并不知道："
        "要么在基金经理之间有差异，围绕二分之一，要么每位都恰好是二分之一。"
        "<bookmark mark='b'/>按月计的损益，波动率为百分之十或百分之五，回撤百分之五时减半，百分之七点五时解聘，每位被解聘者都换上新人。"
        "<bookmark mark='c'/>每个组拿走自己盈利年份的五分之一，不与亏损者轧差，各组共享一个共同冲击。",

    'f"When skill varies.':
        "当技能存在差异时。<bookmark mark='a'/>在百分之十的波动率下，规则频繁触发：每年{fa:.0f}%的席位。在百分之五时，{fb:.0f}%。"
        "<bookmark mark='b'/>而止损有回报：有止损时，投资者的夏普比率是{sb:.2f}；没有止损时，{sc:.2f}。规则把正在亏损的基金经理换成新抽取的人，而亏损者往往是没有技能的那些。",

    'f"When every manager has the same skill.':
        "当每位基金经理技能相同时。<bookmark mark='a'/>规则触发得同样频繁，因为回撤主要是运气。"
        "<bookmark mark='b'/>但现在解聘一位基金经理只是换上一个完全相同的人：投资者的夏普比率有止损时是{sb:.2f}，没有时是{sc:.2f}，彼此相差在一个标准误左右。止损只有作为对存在差异的技能的检验时才值得。",

    'f"Why it works, measured.':
        "为什么有效，测出来看。<bookmark mark='a'/>被规则解聘的基金经理，平均真实夏普比率为{b['fired_skill']:.2f}，低于新雇员的二分之一。"
        "<bookmark mark='b'/>三十年后，席位上的基金经理平均为{b['final_skill']:.2f}；没有止损时为{c['final_skill']:.2f}，即人才池的水平。"
        "<bookmark mark='c'/>回撤止损是一种用真钱进行的、关于基金经理是否有技能的序贯检验。研究章节会精确计算它的检验功效。",

    'f"And a cost the headline hides.':
        "还有一项被表面数字掩盖的成本。<bookmark mark='a'/>每个组按自己的利润拿报酬，亏损的组不退回任何东西。"
        "<bookmark mark='b'/>投资者拥有的是总和，亏损者也包括在内。"
        "<bookmark mark='c'/>所以平台利润中支付出去的比例是{100 * b['payout_share']:.0f}%，而不是百分之二十：这就是轧差风险。投资者向每个组都卖出了一份看涨期权。"
        "第2部分在单只基金的业绩报酬里给同样的看涨期权定过价。",

    "The people. <bookmark mark='a'/> Platforms compete":
        "人。<bookmark mark='a'/>平台用保底报酬和资本争夺团队，因为团队的业绩记录每天晚上都会走出公司大门。"
        "<bookmark mark='b'/>公司用竞业限制条款和花园假来保护策略，也通过法院：2024年，Jane Street就一项印度期权策略起诉了Millennium和两名前交易员，据报道案件在当年晚些时候和解。"
        "<bookmark mark='c'/>许多同一行业的组最终持有相似的头寸，所以中央会测量重叠并加以对冲：一家公司内部的拥挤仍然是拥挤。",

    "Pause and predict. Two pods each run ten percent":
        "暂停并预测。两个组都运行百分之十的波动率，都没有技能。一个赚百分之十，另一个亏百分之十。平台对每个盈利年份支付五分之一。它的利润中有多少比例被支付出去？",

    # ------------------------------------------------------------------ Process
    "Chapter four. A quant firm produces thousands of ideas":
        "第四章。一家量化公司每年产生数千个想法，只资助其中少数几个。挑选它们的流程才是公司真正的产品，也正是本系列从第1部分起一直在本系列公司里运行的流程。",

    "The pipeline, as quant firms describe it.":
        "量化公司所描述的流水线。<bookmark mark='a'/>一个想法；检验它的数据；一次回测；由没有参与构建的人来审查。"
        "<bookmark mark='b'/>然后是孵化，小规模交易；资本；监控；最终是退役。大多数想法止步于回测或审查，而一家公司的好坏，就看有多少坏想法能闯过这两关。",

    "What a review asks, collected from this series.":
        "审查要问什么，从本系列中汇总。<bookmark mark='a'/>找到它用了多少次试验？<bookmark mark='b'/>它是否在扣除成本之后、在公司实际运行的规模上成立？"
        "<bookmark mark='c'/>它为什么应该有效，谁在付钱？<bookmark mark='d'/>它给公司已持有的东西增加了什么？一个策略可能通过全部四项，却因最后一项被拒绝。",

    'f"The House has been running this pipeline.':
        "本系列公司一直在运行这条流水线。<bookmark mark='a'/>它的计数器已经计入{trials:,}次试验，即三十三个部分中比较过的每一种配置。"
        "<bookmark mark='b'/>登记了{n_rows}个策略。<bookmark mark='c'/>每一个都在封存年份上只打开一次，这是本系列公司对孵化的替代。"
        "所以本系列公司可以问一家公司对自己研究部门提出的问题：登记的组合遇到新数据时会缩水多少？",

    'f"The House\'s own record.':
        "本系列公司自己的记录。<bookmark mark='a'/>每个点是一个登记的组合：研究年份的夏普比率对封存年份的夏普比率，带一个标准误。虚线表示没有缩水。"
        "<bookmark mark='b'/>拟合的斜率是{b1:.2f}：一个在研究期好一个夏普点的组合，在新数据上大约好{b1:.2f}。平均值从{h['mean_research']:.2f}降到{h['mean_holdout']:.2f}，"
        "{100 * h['share_positive']:.0f}%仍为正。这些大多是有长历史的经典溢价；一家公司自己的研究，每个想法用的试验更多，缩水也更多，这就是审查要清点试验次数的原因。",

    'f"Incubation. <bookmark mark=\'a\'/> Trading a little real money':
        "孵化。<bookmark mark='a'/>用少量真钱交易，检验回测所假设的东西：成交、成本、迟到或修订的数据，以及公司自身的冲击。"
        "<bookmark mark='b'/>它无法检验夏普比率：六个月的收益给出的标准误约为{se6:.1f}。孵化能发现坏掉的策略，而不是平庸的策略。"
        "<bookmark mark='c'/>所以资本是分阶段赢得的，每一阶段都要求成本和滑点保持在审查所预测的范围之内。",

    "How much capital, as the record grows.":
        "随着记录增长，给多少资本。<bookmark mark='a'/>取一个以零为中心的真实夏普比率先验，以及T年的实盘记录。"
        "<bookmark mark='b'/>后验均值把测得的比率向零收缩，收缩因子随记录长度增加而上升。"
        "<bookmark mark='c'/>先验标准差为二分之一时，一年的记录只被相信五分之一；四年，一半；十年，接近四分之三。按比例确定规模，资本就跟随证据：这正是平台凭经验法则运行的资本爬坡。",

    "And retirement. <bookmark mark='a'/> Decay is the default":
        "还有退役。<bookmark mark='a'/>衰减是常态：本系列中的每一种优势在发表或拥挤之后都减弱了。"
        "<bookmark mark='b'/>一个组合依据证据退役：当它的实盘记录让后验夏普比率小到不足以支付其资本时。"
        "<bookmark mark='c'/>它仍留在日志里，连同它的试验次数，这样下一个与之相似的想法就要为整个家族付账。",

    "Pause and predict. A strategy shows a live Sharpe ratio of two":
        "暂停并预测。一个策略一年的实盘夏普比率为二。先验以零为中心、标准差为二分之一，后验均值是多少？四年保持同样水平之后呢？",

    # ------------------------------------------------------------------ Risk
    "Chapter five. A desk's risk model":
        "第五章。交易台的风险模型，来自第31部分，衡量的是一个组合。公司的风险部门任务更难：把每个组合加总，找出任何模型都看不到的损失，并且能在几秒钟内停止交易。",

    "Four layers. <bookmark mark='a'/> Pre-trade checks":
        "四个层次。<bookmark mark='a'/>每笔订单离开公司之前、在微秒内完成的预交易检查。<bookmark mark='b'/>日内：每个交易台的头寸和利润集中在一处，实时可见。"
        "<bookmark mark='c'/>日终：第31部分的因子模型用于全公司，加上压力测试和流动性。"
        "<bookmark mark='d'/>还有治理：谁可以越过限额，必须通知谁。没有独立于交易员、能够执行限额的人，限额就毫无意义。",

    "The limits a desk lives under.":
        "交易台所受的限额。<bookmark mark='a'/>来自风险模型的波动率预算；总敞口和净敞口；因子贝塔，即一个组没有获得报酬去承担的风险；"
        "对任何单一证券或交易对手的集中度；以天数衡量的退出流动性；以及第三章的回撤规则。每一项都是交易员看得到、风险部门能执行的数字。",

    'f"Liquidity is a limit measured in time.':
        "流动性是用时间衡量的限额。<bookmark mark='a'/>退出天数：头寸除以公司允许自己占日成交量的比例。"
        "<bookmark mark='b'/>在一只日成交两千万美元的股票上持有五千万美元，按成交量的十分之一卖出，需要{days:.0f}天。"
        "<bookmark mark='c'/>按第31部分的平方根定律，成本约{cost_bp:.0f}个基点。危机中成交量下降、波动率上升，两者同时变坏，所以限额是按危机而不是按平常日子设定的。",

    "Stress tests find the losses the model does not.":
        "压力测试找出模型找不到的损失。<bookmark mark='a'/>历史情景：把今天的组合放进1987年、2007年8月、2008年秋、2020年3月和2022年重演一遍。"
        "<bookmark mark='b'/>假设情景：一个因子变动五个标准差，相关性趋于一，一个交易对手倒闭。"
        "<bookmark mark='c'/>还有反向压力测试：从会终结公司的那个损失出发，问要发生什么才会导致它。",

    'f"Why firm risk is not the sum of desk risks':
        "为什么公司风险不是各交易台风险之和，直到它变成之和。<bookmark mark='a'/>有N个交易台，波动率相同，平均相关系数为rho，公司的波动率就是这个。"
        "<bookmark mark='b'/>五十个交易台，相关系数为百分之五，分散后只剩一个交易台风险的{div_calm:.2f}。"
        "<bookmark mark='c'/>危机中相关性一起上升：在零点四时为{div_crisis:.2f}，约为原来的{r:.1f}倍，而没有任何交易台改变一个头寸。按平静时期相关性设定的限额，是被市场突破的，而不是被交易员。",

    "The case every risk desk studies.":
        "每个风险部门都要研究的案例。<bookmark mark='a'/>2012年8月1日，骑士资本的一次软件部署让旧的、未使用的代码在八台服务器中的一台上仍处于激活状态。"
        "开盘后它发出数百万笔非预期订单，在大约四十五分钟内，公司建立的头寸让它损失超过四亿六千万美元，这是美国证券交易委员会命令中的数字，该命令认定其控制在市场准入规则下不充分。"
        "几天之内公司就需要救助资本，后来被收购。",

    "What would have stopped it.":
        "什么本可以阻止它。<bookmark mark='a'/>价格检查拒绝远离市场的订单。<bookmark mark='b'/>规模和频率限额能抓住失控的循环，它在显示为亏损之前，先表现为不可能的下单频率。"
        "<bookmark mark='c'/>信用限额限制任何算法能建立的规模，正如美国证券交易委员会2010年的市场准入规则所要求的。<bookmark mark='d'/>还有熔断开关，以及有权限、也有习惯去按下它的人。",

    "The other side of the trade.":
        "交易的另一面。<bookmark mark='a'/>2021年3月，家族办公室Archegos通过与多家银行的互换持有非常大的集中股票头寸，没有一家银行看到全貌。"
        "股价下跌时它无法满足追加保证金，卖得最慢的银行亏得最多；瑞士信贷报告的损失约五十五亿美元。一家公司的风险包括其交易对手的集中度，而这只能询问，无法看到。",

    "Pause and predict. A book holds five days":
        "暂停并预测。一个组合持有一只股票五天的成交量。危机中成交量减半、波动率翻倍。它的退出天数和平方根成本如何变化？",

    # ------------------------------------------------------------------ Tech
    "Chapter six. A quant firm is a software company":
        "第六章。量化公司是一家碰巧在做交易的软件公司。它构建什么取决于它的期限：每月调仓的基金需要干净的数据和严谨的研究代码；做市商则需要每一微秒。",

    "The stack. <bookmark mark='a'/> Data, stored point in time":
        "技术栈。<bookmark mark='a'/>数据，按时点存储，这样公司能说清楚自己在什么时候知道什么。<bookmark mark='b'/>研究：笔记本、集群和GPU，每次试验都有记录。"
        "<bookmark mark='c'/>生产，最好与研究用同一套代码，因为为生产重新实现的策略就是另一个策略。<bookmark mark='d'/>还有执行：网关、第五章的检查，以及与交易所的连接。",

    "Languages, from the public record.":
        "编程语言，来自公开记录。<bookmark mark='a'/>Jane Street用OCaml编写其系统，Yaron Minsky在2011年解释了原因：严格的类型系统能在错误造成亏损之前就把它们抓住。"
        "<bookmark mark='b'/>在延迟决定谁拿到交易的地方，公司用贴近硬件的C++编写，绕过操作系统的网络栈，把逻辑放到可编程芯片上。"
        "<bookmark mark='c'/>大多数研究是在编译库之上的Python，就像本系列；难点在于把它原封不动地送进生产。",

    "Data. <bookmark mark='a'/> A day of American equity quotes":
        "数据。<bookmark mark='a'/>美国股票一天的报价和成交多达数十亿条消息，时间戳精确到微秒。"
        "<bookmark mark='b'/>它们按列存储，所以关于一个字段一年的查询只读这个字段：Kx的kdb+是经典例子。"
        "<bookmark mark='c'/>每个值都与它成为已知的时间一起存储，这样重述的账目和修订的数字永远不会泄漏进回测。",

    'f"How fast is fast?':
        "多快才算快？<bookmark mark='a'/>引领美国股市的期货在芝加哥附近的数据中心交易；股票在新泽西，相距约{km:.0f}公里。"
        "<bookmark mark='b'/>光在真空中走完这段距离需要{vac:.2f}毫秒：任何技术都无法打破的下限。"
        "<bookmark mark='c'/>在玻璃光纤中，按其折射率变慢，至少{fib:.1f}毫秒。2010年，一家公司在两地之间挖了一条更直的光纤线路，随后其他公司建起微波链路，"
        "因为在空气中传播的信号几乎达到真空光速。这是一场与物理的竞赛，而它几乎已经赢了。",

    "Inside the exchange's building.":
        "在交易所的大楼里。<bookmark mark='a'/>交易所在撮合引擎旁出租机位，给每个客户相同长度的线缆。"
        "<bookmark mark='b'/>速度值得花钱，因为消息到来时报价过时的做市商会被狙击：速度既是进攻也是保护。"
        "<bookmark mark='c'/>批评者Eric Budish、Peter Cramton和John Shim认为，连续交易市场浪费地奖励微小的速度优势，并提议改为每秒举行多次的集合竞价。第38部分会回到这个问题。",

    "Research computing.":
        "研究计算。<bookmark mark='a'/>处理器集群用于回测，它们天然可以并行；GPU用于神经网络。"
        "<bookmark mark='b'/>好的研究平台完整记录每次试验：代码、数据版本、参数和结果。"
        "<bookmark mark='c'/>还有第29部分的教训，放大到公司的规模：试验越便宜，试验就越多，每个结果的门槛就越高。",

    'f"And reproducibility.':
        "还有可复现性。<bookmark mark='a'/>在本系列公司里，每个数据文件都要与一份包含{n_files}个条目的清单中的摘要核对，屏幕上的每个数字都由具名代码计算并缓存。"
        "<bookmark mark='b'/>这不是为了整洁。无法重跑的结果就无法审查，而一个悄悄改变的数字，就是一次没人清点的试验。",

    "Pause and predict. A microwave link saves three milliseconds":
        "暂停并预测。一条微波链路比光纤快三毫秒。一个期货变动以每笔交易半个基点的优势预测一只股票的下一次变动。这个速度值多少钱？对谁值钱？",

    # ------------------------------------------------------------------ Compliance
    "Chapter seven. An algorithm can break the law":
        "第七章。算法和人一样可能违法，而且更快。每家公司都有一个监控自身订单的合规部门，而每个监管机构现在都有数据来监控所有人的订单。",

    "The abuses an algorithm can commit.":
        "算法可能犯下的违规行为。<bookmark mark='a'/>幌骗：下达你打算在成交前撤销的订单，多德-弗兰克法案在美国期货市场明确将其定为违法。"
        "<bookmark mark='b'/>分层挂单：在多个价位堆叠这样的订单，制造一侧有压力的假象，而你在另一侧交易。"
        "<bookmark mark='c'/>尾盘操纵：通过交易推动合约结算所依据的价格。<bookmark mark='d'/>还有对敲交易：与自己交易来伪造成交量。",

    "What it looks like in the order book.":
        "它在订单簿里是什么样子。<bookmark mark='a'/>左边是买单，右边是卖单。<bookmark mark='b'/>一个分层挂单的交易者在市价下方堆起大额买单，看起来像需求。"
        "<bookmark mark='c'/>读订单簿的买家抬高报价，交易者卖给他们。然后那些大额买单被撤销，它们从来就不打算成交。"
        "这种模式就是监控要寻找的特征：大额订单，很快撤销，方向与交易者自己的成交相反。",

    "The cases, from court records.":
        "案例，来自法庭记录。<bookmark mark='a'/>Navinder Sarao是一位在伦敦附近父母家中交易的交易员，2015年在美国被控幌骗E-mini期货，包括2010年闪电崩盘当天。"
        "他在2016年认罪，提供了合作，2020年被判处一年居家监禁。监管机构没有说他的订单导致了崩盘；指控的是幌骗。",

    "And at the largest scale.":
        "还有最大规模的案例。<bookmark mark='a'/>2020年9月，摩根大通同意向美国三家机构支付约九亿二千万美元，以了结其贵金属和国债交易台交易员在约八年间的幌骗行为。"
        "其中几名交易员后来在审判中被定罪。幌骗不是小交易员的罪行。",

    "Who watches.":
        "谁在监控。<bookmark mark='a'/>在美国股票和期权市场，美国证券交易委员会的合并审计追踪记录每笔订单的完整生命周期，按客户区分，自2020年起开始报送。"
        "<bookmark mark='b'/>每家交易所监控自己的订单簿。<bookmark mark='c'/>而公司被期望首先抓住自己的交易员和算法，这正是这一部分为本系列公司增设的合规部门。",

    "How surveillance looks for it.":
        "监控如何寻找它。<bookmark mark='a'/>单看撤单比率会把所有人都标记出来，因为做市商正当地撤销几乎每一个报价。"
        "<bookmark mark='b'/>所以检验针对的是意图：一侧的大额订单被撤销，与另一侧的成交同步，在几秒之内。"
        "<bookmark mark='c'/>警报不等于违规：由人来审查，结合订单数据，往往还有交易员自己的消息，大多数案件正是这样被证实的。",

    "And a case not yet decided.":
        "还有一个尚未判决的案件。<bookmark mark='a'/>2025年7月，印度证券交易委员会发布临时命令，指控Jane Street旗下实体在期权到期日操纵指数水平，在案件审理期间禁止它们进入其市场，"
        "并扣押了它所称的非法所得。公司对这些认定提出异议，存入了这笔款项，据报道获准恢复交易。这些是有争议、尚未判决的指控；"
        "它们为每家公司提出的问题是：对冲和提供流动性在哪里结束，影响结算价格又从哪里开始。",

    "The compliance desk the House adds.":
        "本系列公司增设的合规部门。<bookmark mark='a'/>新策略和新市场在交易之前，先审查它们在监管者眼中会是什么样子。"
        "<bookmark mark='b'/>订单和消息被记录、保存、抽样，每一条警报都要审查。<bookmark mark='c'/>这个部门是独立的：它向公司领导层汇报，而不是向它所监控的交易台汇报，并且它可以叫停一个策略。",

    "Pause and predict. A market maker cancels ninety-eight percent":
        "暂停并预测。一家做市商撤销了百分之九十八的报价。这是幌骗的证据吗？什么样的额外模式才是？",

    # ------------------------------------------------------------------ Interview
    "Chapter eight. Quant firms hire by testing":
        "第八章。量化公司通过考试来招聘，而考题是公开的：概率、期望值、压力下的估算、做市，以及代码。每一项都检验这份工作每天要用的技能。下面是一场模拟面试，答案都算出来了。",

    "What is tested. <bookmark mark='a'/> Probability":
        "考什么。<bookmark mark='a'/>概率，精确而快速地回答，通常借助对称性。<bookmark mark='b'/>期望值和仓位大小，因为价格是期望，赌注要定规模。"
        "<bookmark mark='c'/>做市：报价，根据成交更新，管理你最终持有的东西。<bookmark mark='d'/>还有代码，先正确，再快。",

    'f"Question one. Roll two dice':
        "第一题。掷两颗骰子，较大那颗的期望值是多少？<bookmark mark='a'/>最大值不超过k，当且仅当两颗骰子都不超过k，所以它的分布是平方之差。"
        "<bookmark mark='b'/>期望值是三十六分之一百六十一，约{fe:.2f}。<bookmark mark='c'/>再检查：大于一颗骰子的三点五，小于六。面试官要听的是方法和检查，而不是算术。",

    'f"Question two, the market-making game.':
        "第二题，做市游戏。对即将掷出的三颗骰子之和做市。<bookmark mark='a'/>公允价值是十点五。<bookmark mark='b'/>标准差约{sd:.1f}，它决定你能承受持有多少。"
        "<bookmark mark='c'/>报十买、十一卖：从任何不比你知道得多的人那里，你赚半个点。",

    "Then the twist.":
        "然后是转折。<bookmark mark='a'/>面试官说对方看到了一颗骰子，是六：他们的公允价值是十三。"
        "<bookmark mark='b'/>如果他们在你的十一买入，你的期望损失是二。知情交易者只在你的报价错误时才交易。"
        "<bookmark mark='c'/>所以对方买入之后，把两边报价都抬高，如果怀疑对方有信息，就把价差拉宽。成交本身就是信息，这就是第38部分的全部理论，浓缩在一次交易里。",

    'f"Question three, a classic.':
        "第三题，经典题。<bookmark mark='a'/>抛硬币直到第一次出现正面；你得到二的若干次方，次数就是正面出现在第几次。你愿意付多少钱来玩？"
        "<bookmark mark='b'/>每多抛一次，期望值就增加一美元，永无止境：无穷大。<bookmark mark='c'/>但没有人能付出比自己拥有的更多。"
        "把赔付上限设为十亿美元，期望值约为{evf:.0f}美元。面试官想要的答案是关于交易对手，而不是关于无穷大。",

    'f"Question four, sizing.':
        "第四题，仓位大小。一枚硬币在等额赌注中有百分之六十的胜率。你下注多少？<bookmark mark='a'/>凯利公式，来自第8部分：两倍胜率减一，即财富的{f:.1f}。"
        "<bookmark mark='b'/>每次下注的增长率是{g:.3f}。<bookmark mark='c'/>下注两倍，增长率是{g2:.3f}：为负。手握一枚会赢的硬币，下注过大也会破产。"
        "面试官问这个，是因为仓位过大的交易员是公司最常见的亏钱方式。",

    'f"Question six, an estimate.':
        "第六题，估算。一家大型美国股票做市商每天做多少笔交易？<bookmark mark='a'/>从市场出发：数量级上每天约一百亿股。"
        "<bookmark mark='b'/>一家大型做市商占五分之一，每笔约一百股。<bookmark mark='c'/>每天约{trades_m:.0f}百万笔交易。第二章的大数定律需要约十万笔独立交易，所以披露的统计量是可信的。"
        "估算题考的正是这个：一串粗略的数字，每一个都要能自圆其说。",

    "Question five, code.":
        "第五题，代码。计算一个策略的最大回撤。二次复杂度的答案比较每一对日期；面试官想要的答案是维护历史高点和从高点的最大跌幅，一遍扫描。"
        "这是本系列公司自己的版本，本系列里每一个回撤背后都是这个函数。",

    "How to prepare.":
        "如何准备。<bookmark mark='a'/>经典书籍：Mosteller的五十道概率难题、Crack的《华尔街面试》，以及周欣峰的量化金融面试实用指南。"
        "<bookmark mark='b'/>先说思路，再计算，然后用一个界或特例检验；在做市游戏中，说出每笔成交告诉了你什么。"
        "<bookmark mark='c'/>真正考的是在计时压力下对不确定性的冷静推理，这也正是这份工作。",

    "Pause and predict. You roll a die and may re-roll once":
        "暂停并预测。你掷一颗骰子，可以重掷一次，保留第二次的结果。用最优策略，期望值是多少？",

    # ------------------------------------------------------------------ Culture
    "Chapter nine. The founding stories of quant firms":
        "第九章。量化公司的创业故事被讲了太多遍，已经成了一种文体。下面是创始人和他们的传记作者公开讲述的版本，以及这些故事的共同点。",

    "Two mathematicians.":
        "两位数学家。<bookmark mark='a'/>Edward Thorp在1962年出版了一本关于击败二十一点的书，1967年又出版了一本关于对冲认股权证的书，然后用同样的数学运作一只基金，正如他在回忆录里讲述的。"
        "<bookmark mark='b'/>James Simons，一位几何学家、前密码破译员，曾任石溪大学数学系主任，1978年开始交易，1982年把公司命名为文艺复兴。"
        "它雇用数学家、物理学家和语音识别研究者，而且出了名地几乎不雇华尔街的人。",

    "Two founders from computing and from trading.":
        "两位分别来自计算和交易的创始人。<bookmark mark='a'/>David Shaw，来自哥伦比亚大学、研究并行计算机的计算机科学家，1986年加入摩根士丹利的量化小组，两年后创立了自己的公司。"
        "<bookmark mark='b'/>Kenneth Griffin据广泛报道从1987年起在大学宿舍里交易可转债，1990年创立Citadel，2002年又增设做市商Citadel Securities。",

    "And two that defined business models.":
        "还有两家定义了商业模式的公司。<bookmark mark='a'/>据报道，Jane Street于2000年由一小群交易员创立，其中几位来自Susquehanna International Group，作为交易所交易基金的做市商成长起来。"
        "<bookmark mark='b'/>Millennium由Israel Englander于1989年创立，据报道起步资金约三千五百万美元，后来成长为第三章的平台。",

    "And the next generation, founded by alumni.":
        "还有由前员工创立的下一代。<bookmark mark='a'/>AQR由Clifford Asness与几位高盛资产管理部门的同事于1998年创立，其业务部分建立在发表研究之上：本系列在第24和32部分用到的因子和趋势序列就出自他们。"
        "<bookmark mark='b'/>据报道，Two Sigma于2001年由D. E. Shaw的前员工John Overdeck和计算机科学家David Siegel创立。每一代公司都由上一代的员工创立。",

    "What the stories share.":
        "这些故事的共同点。<bookmark mark='a'/>一种来自金融以外的方法：概率、编码理论、并行计算。"
        "<bookmark mark='b'/>一个反应迟缓的市场：认股权证、可转债、交易所交易基金、配对，那里的价格靠经验法则设定。"
        "<bookmark mark='c'/>还有幸存者偏差：我们听到的是存活下来的公司的故事。许多做过同样尝试而倒闭的公司不会写回忆录，这是第26部分的教训用在创始人身上。",

    "And culture.":
        "还有文化。<bookmark mark='a'/>有些公司把共享研究和共享报酬描述为防止团队之间互相保密的手段；平台则选择相反的做法，独立的投资组。"
        "<bookmark mark='b'/>策略随人员流失，所以公司两者都要守护，代价是它们学到的东西几乎都不发表。"
        "<bookmark mark='c'/>而展示一个好回测的压力，在公司内部和在学术期刊里是一样的。防线是第四章的审查，而不是美德。",

    "Pause and predict. A thousand firms start with no skill":
        "暂停并预测。一千家公司起步时都没有技能，每家每年存活的概率是二分之一。有多少家连续存活了十年？它们的创始人会怎么解释原因？",

    # ------------------------------------------------------------------ Stops
    "Chapter ten. Platforms stop managers":
        "第十章。平台会让基金经理止损出局；止损对一个有真实溢价的策略有帮助吗？本系列公司在Kenneth French半个世纪的因子上检验它，对照一个零假设，它准确地说明了在收益独立时止损应该起什么作用。",

    "The test. <bookmark mark='a'/> Six factors":
        "检验。<bookmark mark='a'/>六个因子：市场、规模、价值、盈利能力、投资和动量，每个都只用过去三年的数据缩放到百分之十的波动率。"
        "<bookmark mark='b'/>一个止损：当从高点的回撤达到D时，空仓w个月，然后重新开始。"
        "<bookmark mark='c'/>三种深度，一到两个波动率，两种空仓期：六条规则，六个因子，三十六种组合。",

    "What theory predicts.":
        "理论的预测。<bookmark mark='a'/>如果收益独立，回撤对未来毫无信息，止损只是随机地丢掉一些月份。"
        "<bookmark mark='b'/>均值按投资时间的比例下降，波动率只按其平方根下降，所以止损只会降低夏普比率。"
        "<bookmark mark='c'/>所以零假设是对打乱顺序的月份施加同样的规则：保留因子自身的分布，去掉一切序列相关。止损只有胜过它的打乱版本才算有帮助。",

    'f"One rule, a stop one and a half volatilities deep':
        "一条规则，一个一点五个波动率深、空仓一年的止损。<bookmark mark='a'/>每个因子不加止损和加止损时的夏普比率。"
        "<bookmark mark='b'/>还有打乱后的结果：总是比不加止损略低，正如理论所说。价值从{h0:.2f}变为{h1:.2f}，远高于它的打乱版本；动量从{u0:.2f}变为{u1:.2f}，与打乱版本持平。市场和其余因子居于两者之间。",

    'f"All thirty-six, measured against their shuffles.':
        "全部三十六种组合，与各自的打乱版本对比。<bookmark mark='a'/>绿色表示止损胜过打乱版本；红色表示输给它。"
        "有{n_pos}种组合胜出超过两个标准差，有{n_neg}种以同样幅度落后。"
        "<bookmark mark='b'/>模式取决于因子而不是规则：这里几乎每一种溢价相对其打乱版本都从止损中获益，因为它的亏损会持续；动量是例外，处处与打乱版本持平，在最紧的止损和最长的空仓期下低于它。",

    "Why. <bookmark mark='a'/> Value and profitability lose":
        "为什么。<bookmark mark='a'/>价值和盈利能力在漫长而缓慢的阶段中亏损，比如价值在1998到2000年以及2018年以后，所以回撤预示着更多回撤，退到一旁可以避开其中一部分。"
        "<bookmark mark='b'/>动量最严重的亏损是会恢复的突然反转，比如2009年；止损在底部卖出，错过了反弹。"
        "<bookmark mark='c'/>止损是押注亏损会持续。有些溢价具备这个性质，有些不具备。",

    "And the caveat.":
        "还有一个提醒。<bookmark mark='a'/>试了三十六种组合，所以现在为每个因子挑选最好的止损，就会犯第26部分的错误。"
        "<bookmark mark='b'/>对平台来说问题不同：它让基金经理止损是为了了解未知的技能，而这些因子不需要证明这一点。"
        "<bookmark mark='c'/>所以本系列公司把这记为研究，注明三十六次试验，并且不给任何已登记的组合加止损。",

    "Pause and predict. A strategy with independent returns":
        "暂停并预测。一个收益独立、夏普比率为零点六的策略有四分之一的时间被止损空仓。把空仓的月份也算上，它显示的夏普比率大约是多少？",

    # ------------------------------------------------------------------ House
    "Chapter eleven. The House's thirty-fourth rule":
        "第十一章。本系列公司的第34条规则不是关于某个策略的，而是关于公司：本系列公司里每个交易台现在都要遵守的限额、控制和记录。",

    "The first sheet. <bookmark mark='a'/> A disclosed loss rate":
        "第一张汇总表。<bookmark mark='a'/>一个披露的亏损率意味着日度夏普比率在三以上。一位夏普为一的基金经理，在半个波动率深的止损下几个月就会出局，在一个波动率深的止损下约两年。"
        "一个一点五个波动率深的止损，在三年内会让大多数没有技能的基金经理出局，也会让四分之一的好基金经理出局。在技能存在差异的平台上，止损提高了投资者留下的收益，而支付给各组的比例超过其表面份额。"
        "本系列公司自己登记的组合保住了大约四分之三的研究期夏普比率。止损对亏损会持续的价值因子有帮助。",

    "The research chapter's formulas, in eight lines.":
        "研究章节的公式，八行代码。到回撤止损的期望时间：sigma平方除以二倍mu平方，乘以e的a次方减一再减a，其中a是两倍漂移乘以止损再除以方差。"
        "止损前的期望高点：sigma平方除以二倍mu，乘以e的a次方减一。当基金经理没有技能时，两者都退化为无漂移的情形。",

    "Chapter ten's rule.":
        "第十章的规则。逐个遍历收益；空仓时倒数空仓期，然后从新的高点重新开始；否则计入收益，更新历史高点，如果从高点的跌幅达到阈值，记一次止损并空仓。"
        "本系列公司施加的每一次止损都经过这几行代码。",

    "And Chapter three's platform, one month at a time.":
        "还有第三章的平台，一次一个月。每个组的收益，带一个共同冲击；历史高点和回撤；在第一个阈值减半；在第二个阈值解聘基金经理，记录其真实技能，从人才池中雇用新人。"
        "规则解聘的技能和保留的技能，就是这一章衡量选择效应的方式。",

    "The tools this part adds, in the House's new firm module":
        "这一部分新增的工具，在本系列公司新的公司模块里：定理、它的检验、平台，以及披露统计量的换算。<bookmark mark='a'/>还有图上点亮的合规部门。"
        "<bookmark mark='b'/>第34条规则。一个交易台要在本系列公司里交易，只能在它看得到、独立部门能执行的限额之下：波动率预算、因子和集中度上限、按危机设定的流动性限额，"
        "以及事先算好止损时间的回撤规则；在预交易检查和熔断开关之后；每笔订单都被记录和监控；每个策略都要经过审查、孵化和按证据确定规模的资本爬坡才能获得资本，并且清点它的试验次数。",

    "The rule against three cases.":
        "用这条规则检验三个案例。<bookmark mark='a'/>一个推销夏普比率为三的平台：问关闭了多少个组，它们的亏损是否在记录里，以及各组拿走了毛利润的多大比例。"
        "<bookmark mark='b'/>一位在百分之七点五被止损出局的基金经理：问这以波动率计有多深。<bookmark mark='c'/>还有一个周五上线的算法：问它的检查、它的信用限额，以及谁握着熔断开关。",

    # ------------------------------------------------------------------ Research
    "For the researcher. Every platform runs drawdown stops":
        "写给研究者。每个平台都在运行回撤止损，每位基金经理都想知道胜算。本章精确推导到止损的期望时间，以及止损前赚到的利润，并把止损读成一种统计检验。",

    "The setup. <bookmark mark='a'/> A manager's cumulative profit":
        "设定。<bookmark mark='a'/>基金经理的累计利润是带漂移的布朗运动：漂移是技能，波动率是预算。<bookmark mark='b'/>它的历史高点，以及从高点的回撤。"
        "<bookmark mark='c'/>止损是回撤第一次达到d的时刻。<bookmark mark='d'/>对时间和金额做尺度变换后，只有两个数要紧：夏普比率，以及以基金经理自身波动率为单位的止损深度。",

    "Lemma one. <bookmark mark='a'/> The drawdown moves like the profit":
        "引理一。<bookmark mark='a'/>回撤的变动与利润相反，只是在零处会被推回去：每当利润创出新高时。它是一个漂移为负mu、在零处反射的布朗运动。"
        "<bookmark mark='b'/>令f(y)为从回撤y出发到止损的期望时间。<bookmark mark='c'/>迪金公式，与第33部分完全一样：生成元作用在f上等于负一；f在止损处为零；而高点处的反射使它在那里的斜率为零。",

    "The solution is two lines.":
        "解只有两行。<bookmark mark='a'/>方程对斜率是一阶的：一个常数，即一除以mu，加上一个指数项，由高点处的零斜率确定。"
        "<bookmark mark='b'/>从止损积分回高点，到止损的期望时间就是sigma平方除以二倍mu平方，乘以e的a次方减一再减a。"
        "<bookmark mark='c'/>而a是两倍夏普比率乘以以波动率计的止损深度。一个数决定一切。",

    "Lemma two: how much the manager makes":
        "引理二：基金经理在止损前赚多少。<bookmark mark='a'/>在每个新高处，过程重新开始。尺度函数给出在高点再上升一点之前先下跌d的概率：与那一点点成正比。"
        "<bookmark mark='b'/>所以止损按每单位新高以恒定速率到来。<bookmark mark='c'/>因此止损前达到的高点服从指数分布，均值如图。"
        "<bookmark mark='d'/>止损时的利润是高点减去d，而瓦尔德恒等式，即漂移乘以期望时间，给出同一个数：对两个引理的检验。",

    "The theorem. <bookmark mark='a'/> In years":
        "定理。<bookmark mark='a'/>以年计，年化夏普比率为S，止损深度为delta个波动率，到止损的期望时间是e的二S delta次方减一再减二S delta，除以二倍S平方；止损前的期望高点有同样的指数。"
        "<bookmark mark='b'/>没有技能时，时间是delta平方，即扩散本身的尺度。技能很高时，它随S乘以delta呈指数增长。这些公式是经典的，Taylor的1975年和Lehoczky的1977年；这里的证明是本系列自己的。",

    'f"The formula as a table.':
        "把公式做成表。<bookmark mark='a'/>行是夏普比率，列是以波动率计的止损。十个百分点波动率预算上的百分之五止损，是半个波动率：一位夏普为一的基金经理平均坚持{g1[0]:.2f}年，夏普为二的{g2[0]:.2f}年。"
        "<bookmark mark='b'/>一个波动率深时，分别为{g1[2]:.1f}年和{g2[2]:.1f}年。两个波动率深时，{g1[4]:.0f}年和{g2[4]:.0f}年。止损相对于波动率的深度，比基金经理的技能重要得多。",

    "Three regimes.":
        "三种情形。<bookmark mark='a'/>亏损的基金经理漂向止损：时间等于距离除以速度。"
        "<bookmark mark='b'/>没有技能的基金经理只靠扩散到达止损：一个波动率深的止损平均需要一年。"
        "<bookmark mark='c'/>有技能的基金经理只有运气差才会到达止损，而漂移让这变得指数级罕见：大偏差速率为二倍S delta。正是这种不对称让止损能区分这三者。",

    'f"The distribution behind the mean.':
        "均值背后的分布。<bookmark mark='a'/>六千位模拟的夏普为一的基金经理，止损深度为一个波动率。"
        "<bookmark mark='b'/>均值与定理吻合，但中位数只有{med:.1f}年，而{long_share:.0f}%的基金经理坚持超过均值的两倍。"
        "止损时间大致服从指数分布：大多数好的基金经理因运气早早出局，少数能坚持十年。",

    'f"Checked by simulation.':
        "用模拟来检验。<bookmark mark='a'/>按日步长，模拟的时间偏长：每日检查会晚一些才发现回撤，与第33部分交易区间的偏差相同。"
        "对夏普为一、止损深度一个波动率的情形，模拟为{r['sim_daily']:.2f}年，定理为{r['theory']:.2f}年。"
        "<bookmark mark='b'/>把两种步长外推到连续监测，得到{r['extrap']:.2f}，每一行都在几个百分点以内，高点也是。",

    'f"The stop as a test.':
        "把止损当作检验。<bookmark mark='a'/>按真实夏普比率，基金经理在三年内被止损出局的概率。止损深度为一个波动率时，没有技能的基金经理有{100 * pr[0.0]['d1.0_3y']:.0f}%被止损，"
        "但夏普为一的基金经理也有{100 * pr[1.0]['d1.0_3y']:.0f}%：一个功效很低的检验。"
        "<bookmark mark='b'/>一点五个波动率深时，{100 * pr[0.0]['d1.5_3y']:.0f}%对{100 * pr[1.0]['d1.5_3y']:.0f}%：一个敏锐得多的检验，代价是让亏损的基金经理运行得更久。",

    "Designing the test.":
        "设计这个检验。<bookmark mark='a'/>两种错误：解聘一位有技能的基金经理，以及留下一位没有技能的。"
        "<bookmark mark='b'/>更深的止损让第一种更少见，第二种更常见。"
        "<bookmark mark='c'/>而深度是以波动率衡量的，所以同样的百分之七点五止损，在百分之十和百分之五的波动率下是不同的检验。平台主要通过给每位基金经理的波动率预算来设计它的检验。",

    'f"What a seat earns before its stop.':
        "一个席位在止损前赚多少。<bookmark mark='a'/>由瓦尔德恒等式，等于漂移乘以期望时间。<bookmark mark='b'/>止损深度为半个波动率时，一位夏普为一的基金经理在出局前赚{a1:.2f}个波动率。"
        "<bookmark mark='c'/>一点五个波动率深时，{a3:.1f}个。浅的止损丢掉了好基金经理的大部分价值；它的好处是也很快丢掉了差的。第三章的模拟就是这种权衡，技能从人才池中抽取。",

    "Where this sits. <bookmark mark='a'/> Howard Taylor and John Lehoczky":
        "这个结果的位置。<bookmark mark='a'/>Howard Taylor和John Lehoczky在1970年代解决了在回撤处停止的问题。"
        "<bookmark mark='b'/>Sanford Grossman和Zhongquan Zhou找到了一个绝不能跌破高点一定比例的投资者应如何投资：第8部分的底线。"
        "<bookmark mark='c'/>Malik Magdon-Ismail和合作者计算了固定期限内的期望最大回撤，这是基金经理会问的另一个问题。",

    "Three open questions.":
        "三个开放问题。<bookmark mark='a'/>有了关于技能的先验，止损就是一个有等待成本的序贯检验；最优边界作为时间和记录的函数，对于平台的收益结构没有闭式解。"
        "<bookmark mark='b'/>看得到止损的基金经理可能在接近止损时降低风险，也可能孤注一掷；策略性的基金经理与凸性报酬之间的均衡尚未解决。"
        "<bookmark mark='c'/>而第十章发现了亏损会持续的溢价，对它们来说布朗运动是错误的模型。",

    "Pause and predict. A manager with a Sharpe ratio of one and a half":
        "暂停并预测。一位夏普比率为一点五的基金经理运行百分之四的波动率，止损为百分之六。到止损的期望时间是多少？止损前的期望利润是多少？",

    # ------------------------------------------------------------------ Outro
    "Part thirty-four in fourteen lines.":
        "第34部分，十四行。六种商业模式，按交易谁的资本、出售什么优势来区分。一个披露的亏损率意味着日度夏普比率在三以上，来自大量的小交易。"
        "著名的数字，按报道解读并互相核对。在平台上，当技能存在差异时，止损提高了投资者留下的收益，而各组拿到的超过表面份额。"
        "本系列公司自己的记录从研究期到新数据缩水了约四分之一。以及公司层面的风险，从限额到熔断开关。",

    "Technology, against the speed of light.":
        "技术，与光速赛跑。监控，以及定义了幌骗的那些案件。面试，以及它真正考的东西。创业故事，以及讲述它们的幸存者。"
        "真实溢价上的止损，在亏损持续的地方有帮助，对动量没有。第34条规则。还有定理：一个席位的期望寿命随夏普比率乘以止损深度呈指数增长。",

    "Six desk questions. What does one losing day":
        "六个交易台问题。一千二百三十八天里一天亏损意味着什么？日度夏普比率在三以上，来自大量的小交易。"
        "<bookmark mark='a'/>在半个波动率深的止损下，一位夏普为一的基金经理能坚持多久？约四个月。<bookmark mark='b'/>为什么要让可能优秀的基金经理止损？因为技能是未知的，止损是一种检验。",

    "What is netting risk?":
        "什么是轧差风险？给盈利者付钱，而投资者也承担亏损者。<bookmark mark='a'/>什么本可以阻止骑士资本？每笔订单的检查和一个熔断开关。"
        "<bookmark mark='b'/>高撤单比率是幌骗吗？不是；意图才是证据。完整解答在讲义里。",

    'f"The pause questions, answered. At ten percent gross':
        "暂停题的答案。在百分之十的毛收益下，二加二十的结构留下{100 * fund:.1f}%；平台留下{100 * plat:.1f}%。"
        "<bookmark mark='a'/>一千二百五十天里五天亏损，对应日度比率{s5:.2f}，每年约{a5:.0f}。"
        "<bookmark mark='b'/>两个没有技能的组，一个赚一个亏：平台什么也没赚到，却仍要支付百分之二。",

    "A live Sharpe ratio of two is believed":
        "一年的实盘夏普比率二被相信为零点四，四年后为一。<bookmark mark='a'/>当成交量减半、波动率翻倍时，退出天数和成本都翻倍。"
        "<bookmark mark='b'/>速度是赢家通吃：优势归于最快的公司，第二快的几乎什么也得不到。",

    'f"Cancelling most quotes is normal':
        "撤销大部分报价对做市商来说很正常；意图才是证据。<bookmark mark='a'/>低于四就重掷，期望值{reroll:.2f}；一千家没有技能的公司中，约有一家能存活十年，并把它归功于技能。"
        "<bookmark mark='b'/>被止损的策略显示{stop_s:.2f}；夏普为一点五、止损深度为一点五个波动率的基金经理大约能坚持{et:.0f}年。",

    "And twelve problems: a disclosed loss rate":
        "还有十二道习题：一个披露的亏损率；两种费用结构；轧差；后验夏普比率；危机中的流动性；三道经典面试题和凯利；以及被止损策略的夏普比率。"
        "然后是两道资格考试题：由反射回撤推导止损时间公式，以及高点的指数分布。中英文解答都在讲义里。",

    "Where this comes back. Part thirty-five maps":
        "这些内容会在哪里再次出现。第35部分描绘谁与谁交易。第37部分测量一笔交易的成本。第38部分是做市，骰子游戏背后的理论。第41部分回到监管与危机。",

    "The books this part follows, and its sources":
        "这一部分所依据的书籍及其来源：关于回撤和市场的论文，以及公开记录，包括文件、命令和法庭案件，媒体报道均标注为据报道。屏幕上的每个数字都由本系列公司的代码算出，或引自这些来源。",

    "The House is now a firm":
        "本系列公司现在是一家公司了：有限额的交易台，监控它们的合规部门，清点试验次数的研究流程，以及任何组合能保住资本多久的规则。"
        "<bookmark mark='a'/>下一部分，第六幕开始：市场微观结构。第35部分：谁与谁交易，通过哪些场所，以及为什么同样一笔订单对一个交易者毫无成本，对另一个却代价不菲。",

}
