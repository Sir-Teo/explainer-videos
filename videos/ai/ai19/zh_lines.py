"""Chinese narration for ai19: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = '人工智能，从零搭建 · 第19部分：推断'

CHAPTERS = {
    'Hook': '一次一个词元',
    'Phases': '1. 预填充与解码',
    'KVCache': '2. 键值缓存的代价',
    'Batching': '3. 批处理：速度与成本',
    'Scheduling': '4. 连续批处理',
    'Paging': '5. 分页与共享前缀',
    'Exact': '6. 先猜几步，一次核对',
    'Drafters': '7. 草稿模型',
    'Rounding': '8. 舍入误差',
    'Outliers': '9. 离群值与SmoothQuant',
    'GPTQ': '10. GPTQ：从最优脑外科说起',
    'Rotation': '11. 旋转：QuaRot与SpinQuant',
    'Formats': '12. 4比特浮点数：MXFP4与NVFP4',
    'KVQuant': '13. 用更少的比特存缓存',
    'Flash': '14. FlashAttention',
    'ServeAttention': '15. 服务时的注意力',
    'Grammar': '16. 约束解码',
    'Frontier': '17. 前沿，2026年末',
    'Outro': '回顾、习题，以及接下来',
}

ZH = {
    # ---------------------------------------------------------------- Hook
    "When a big model writes, it writes one token at a time.":
        "大模型写东西的时候，一次只写一个词元。而每写一个，它都得把自己的每一个权重，统统读一遍。<bookmark mark='a'/>对一个700亿参数的模型来说，每个数按16比特存，也就是2个字节，这就是141GB的数据，从内存一路流进芯片，<bookmark mark='b'/>只为了一个词元。下一个词元，又要全部再读一遍；再下一个，还是这样。<bookmark mark='c'/>每秒能从内存流进芯片多少字节，这叫作内存带宽：在这里，是每秒3.35TB。",

    'f"So memory sets a speed limit.':
        "所以，内存给速度定了一个上限。每秒能写出的词元数，超不过内存带宽除以权重的字节数：在一块NVIDIA H100上，大约是每秒{TOKENS_S:.0f}个词元。<bookmark mark='a'/>与此同时，芯片的算力几乎一直闲着。<bookmark mark='b'/>{use_say}<bookmark mark='c'/>拿训练好的模型来得到回答，不再学习，只是使用它，这叫作推断；它和第7部分的变分推断不是一回事。推断的难处，在于搬运数字，而不在于做乘法。",

    'One conversation uses a third of one percent of it.':
        '一段对话，只用掉其中的三分之一个百分点。',

    "f'One conversation uses {100":
        '一段对话，只用掉其中的{100 * USE:.2f}%。',

    'f"How did we get here?':
        "我们是怎么走到这一步的？2017年的Transformer，就已经是一次写一个词元，并且把读过的内容的键和值保存下来，也就是第15部分讲的缓存。<bookmark mark='a'/>2019年，诺姆·沙泽尔让所有的头共用一套键和值，好少读一些。2020年，GPT-3开始按词元出售，一个词元的成本，从此成了一门生意。<bookmark mark='b'/>2022年，这一部分的想法纷纷登场：FlashAttention、连续批处理、推测解码，还有GPTQ的4比特权重。<bookmark mark='c'/>2023年，llama.cpp在笔记本电脑上跑起了大模型，vLLM开始按页管理缓存。<bookmark mark='d'/>接着，DeepSeek压缩了缓存本身，服务器把读提示和写回答拆开，2025年，OpenAI发布了gpt-oss，它的专家用的是4比特浮点数。<bookmark mark='e'/>与此同时，词元的价格一路下跌。一个至少和GPT-3一样好的模型，2021年每百万词元要60美元，2024年每百万输入词元只要1角5分：只剩原来的{pr[0][2] / pr[-1][2]:.0f}分之1。",

    'This is Part 19 of AI, Built,':
        "这是《人工智能，从零搭建》的第19部分，也是第三幕的最后一部分。<bookmark mark='a'/>本部分的内容：为什么读提示和写回答是两个不同的问题；一台服务器怎样让很多人共用一个模型；推测解码，并证明它是精确的；量化，从舍入误差讲到4比特浮点数；FlashAttention，一步步推导出来；还有约束解码。每一样，都在我们自己的模型上、在这台电脑上实测。",

    # ---------------------------------------------------------------- Phases
    'Chapter one. Prefill and decode.':
        '第1章。预填充与解码。',

    'f"A model with N parameters':
        "一个有N个参数的模型，每读一个词元，大约要做2N次运算：每个权重一次乘法、一次加法。<bookmark mark='a'/>而模型每跑一遍，都要把每个权重读一次：用16比特的数，就是2N个字节。<bookmark mark='b'/>写回答的时候，每跑一遍，每段对话只处理一个新词元。一批里有B段对话，运算强度，也就是每个字节对应的运算次数，就正好是B。<bookmark mark='c'/>读提示的时候，提示里的全部T个词元一遍就过完，和训练时一样：这叫作预填充，它的运算强度是T。<bookmark mark='d'/>按第17部分的屋顶线，一块H100只有在每字节大约{ridge:.0f}次运算以上，才能全速运转。一个1000词元的提示，够得着。只为一段对话写回答，运算强度只有1，就差得远：解码受限于内存。",

    '"We can watch this happen on this computer.':
        "在这台电脑上，就能看到这件事。<bookmark mark='a'/>12个权重矩阵，{big}让一批B个向量依次乘过这12个矩阵，测一下用时。<bookmark mark='b'/>屋顶线预言了一个下限：光是读一遍权重，就要{mem_t:.0f}毫秒，不管B是多少，直到运算追上读取为止。<bookmark mark='c'/>{how}<bookmark mark='d'/>于是，每秒处理的向量数，从批大小为1时的{tps[0]:.0f}个，涨到批大小为{int(B[k512])}时的{tps[k512]:.0f}个：同样的权重，干出了{x_(tps[k512] / tps[0])}倍的活。",

    "f'{mb:.0f} megabytes, more than any of its caches hold":
        '共{mb:.0f}MB，比它任何一级缓存都大：一个大到没法待在处理器旁边的模型。',

    'f"{mb:.0f} megabytes; this processor':
        '共{mb:.0f}MB；这台处理器最大的缓存能装{cache / 1000000.0:.0f}MB，所以其中一部分可能会待在近处。',

    "f'The measured points stay close to that":
        '测出来的点和它很接近：用时在批大小约为{knee_m:.0f}时第一次翻倍，屋顶线给出的是{knee_p:.0f}。',

    'f"The measured time starts climbing sooner':
        '测出来的用时，比屋顶线说的更早开始上升：批大小约为{knee_m:.0f}时就已经翻倍，而不是{knee_p:.0f}，因为这台处理器的矩阵库，是为大的乘法调校的，而不是为寥寥几个向量。即便如此，16个向量的用时也只是1个的{r16:.1f}倍，而不是16倍。',

    'f"Now our own model,':
        "现在换成我们自己的模型，也就是本系列的小说模型，跑在我们为这一部分写的推断引擎上。<bookmark mark='a'/>预填充：一个T个词元的提示，一遍处理完。<bookmark mark='b'/>解码：每跑一遍，给B段对话各写一个新词元。<bookmark mark='c'/>只写一段对话时，速度是每秒{dtps[0]:.0f}个词元；每一步都要读遍全部{n / 1000000.0:.1f}百万个权重，每秒读{bwu / 1000000000.0:.1f}GB。同一个模型读一个{int(T[kp])}词元的提示，速度是每秒{ptps[kp]:,.0f}个词元：是前者的{x_(ratio)}倍，因为这些词元共用了同一次读取。<bookmark mark='d'/>把解码也成批地做，就能把大部分差距补回来：{int(B[kd])}段对话一起写，合计每秒{dtps[kd]:,.0f}个词元。可每段对话，现在只分到每秒{per_user:.0f}个。一个人的速度，对上所有人的总工作量：服务器就是围绕这个取舍来搭建的。",

    # ---------------------------------------------------------------- KVCache
    'Chapter two. The key-value cache, priced.':
        '第2章。键值缓存的代价。',

    'Part 15 built the key-value cache:':
        "第15部分搭起了键值缓存：模型读过的每个词元，都会在每一层的每个注意力头里留下一个键和一个值，这样下一个词元回头看它时，就不必重新计算。<bookmark mark='a'/>有L层、n h个头、每个头大小为d h，那么每个词元就是2乘L乘n h乘d h个数。<bookmark mark='b'/>2019年，诺姆·沙泽尔让所有的头共用一个键和一个值；2023年，分组查询注意力找到了折中：n g个组，每组由几个查询头共用。<bookmark mark='c'/>2024年，DeepSeek走得更远。多头潜在注意力为每个词元只缓存一个压缩过的向量，大小为d c，外加一个携带旋转位置信息的小键，再从它重建出每个头的键和值。",

    'f"Here is what that means for real models.':
        "这对真实的模型意味着什么？<bookmark mark='a'/>Llama 3.1 70B有80层，64个查询头，每个头128个数。如果每个头都有自己的键和值，每个词元就要占{bnum(pt['llama70_mha']):g}{bunit(pt['llama70_mha'])}。<bookmark mark='b'/>它实际用的是8个组，所以一个词元占{bnum(pt['llama70']):g}{bunit(pt['llama70'])}，只有前者的{k['gqa_ratio']:.0f}分之1。<bookmark mark='c'/>DeepSeek-V3有128个头，不压缩的话，每个词元要占{bnum(pt['dsv3_mha']):g}{bunit(pt['dsv3_mha'])}。<bookmark mark='d'/>用了MLA，只占{bnum(pt['dsv3']):g}{bunit(pt['dsv3'])}：只有不压缩时的{cut:.0f}分之1，大约相当于{k['mla_groups']:.2f}个组的分组注意力所保存的量。<bookmark mark='e'/>gpt-oss每个词元占{bnum(pt['oss_full']):g}{bunit(pt['oss_full'])}，我们的小模型占{bnum(pt['ours']):g}{bunit(pt['ours'])}。",

    'f"And the cache grows with every token':
        "而且，缓存随着对话的每个词元不断增长。<bookmark mark='a'/>在对数坐标上，每个模型都是一条直线：每个词元的字节数，乘以词元数。<bookmark mark='b'/>拿权重来比一比。Llama 3.1 70B的权重要占141GB。用分组注意力，一段对话的缓存在大约{cr / 1000.0:.0f}K个词元时就超过了权重；如果每个头都有自己的键和值，是在{k['cross_llama70_mha'] / 1000.0:.0f}K个词元时。<bookmark mark='c'/>而一台服务器要同时装下很多段对话。一块H100，总共只有80GB。<bookmark mark='d'/>gpt-oss让它的直线换了个弯法：每隔一层，只回看128个词元，所以这些层的缓存不再增长；到12.8万个词元时，它保存的量只有处处都用全注意力时的{osf[i128] / osc[i128]:.1f}分之1。",

    'f"We measured the same thing on our model.':
        "我们在自己的模型上也测了同样的东西。<bookmark mark='a'/>一个解码步，批大小分别是1、8和{Bs[-1]}段对话，每段对话已经缓存了{ctxs[0]}到{ctxs[-1]:,}个词元。<bookmark mark='b'/>把每一步的用时，对着它要读的字节数画出来，{trend}：每一步的搬运速度，都在每秒{lo_r / 1000000000.0:.0f}到{hi_r / 1000000000.0:.0f}GB之间。批大小为{Bs[i]}、{ctxs[-1]:,}个词元时，缓存有{kv_last / 1000000.0:,.0f}MB，是权重的{x_(kv_last / wbytes)}倍，一步的用时是{ctxs[0]}个词元时的{x_(grow)}倍。<bookmark mark='c'/>{mem_say}长对话把解码变成了读缓存：要么把它缩小，像MLA那样；要么少看一些，像窗口那样；要么用更少的比特来存，这是第13章的内容。",

    'f"Every extra byte of cache costs time at about {slope / 1000000000.0:.1f} gigabytes a second, near':
        '缓存每多一个字节，就要多花时间，折算下来大约是每秒{slope / 1000000000.0:.1f}GB，接近这台处理器直接读内存的速度，每秒{bw / 1000000000.0:.0f}GB。',

    "f'Every extra byte of cache costs time at about {slope / 1000000000.0:.1f} gigabytes a second, against":
        '缓存每多一个字节，就要多花时间，折算下来大约是每秒{slope / 1000000000.0:.1f}GB，而直接读内存是每秒{bw / 1000000000.0:.0f}GB。',

    'time grows with the bytes, though not on one line':
        '用时随字节数增长，只是并不在一条直线上',

    # ---------------------------------------------------------------- Batching
    'Chapter three. Batching: speed against cost.':
        '第3章。批处理：速度与成本。',

    'f"Every server faces the trade':
        "每台服务器都要面对第1章里的那个取舍。<bookmark mark='a'/>这是我们的模型在这台电脑上的情形：每个点是一个批大小，横轴是单段对话的速度，纵轴是总工作量。<bookmark mark='b'/>单独一段对话，每秒能得到{user[0]:.0f}个词元。和另外255段一起成批，这台电脑总共每秒写出{tot[k]:,.0f}个词元，是原来的{x_(tot[k] / tot[0])}倍，可每段对话只分到{user[k]:.0f}个。<bookmark mark='c'/>往左上是便宜，往右下是快。服务商在这条曲线上挑一个点，价格也就跟着定了。",

    'To see what this means for a real model on a real chip':
        "要看清这对真实芯片上的真实模型意味着什么，就用屋顶线给它建个模。<bookmark mark='a'/>一个解码步要读权重，W个字节，还要读每段对话的缓存：c个词元，每个κ字节。它不可能比内存更快，也就是β。<bookmark mark='b'/>也不可能比运算更快：2NB次运算，每秒P次。<bookmark mark='c'/>而且一切都得装进内存，这就限制了批大小。<bookmark mark='d'/>机器的时间是大家共用的，所以一个词元的成本，就是每秒的价格除以每秒写出的词元数。<bookmark mark='e'/>我们用一块H100跑Llama 3.1 8B，每小时2美元：这是DeepSeek给自家服务算成本时用的租用价格。2022年，谷歌的赖纳·波普和同事为PaLM算过这样一笔账：同样的权重，要么读得更快，要么分给更多人。",

    'f"Here is what the model gives.':
        "这个模型给出的结果是这样的。<bookmark mark='a'/>每条线是一个上下文长度；沿着它，批大小从1开始增大，一路往左下走，直到内存用完。<bookmark mark='b'/>上下文是1000个词元时，单独一段对话，每百万词元要{d1['cost'][0]:.2f}美元。批大小到{d1['bmax']}，就降到{d1['cost'][-1]:.3f}：只有原来的{fall:.0f}分之1，而每段对话的速度降到原来的{x_(slow)}分之1。即便如此，芯片也只做了它能做的运算的{100 * mfu:.0f}%。<bookmark mark='c'/>到12.8万个词元时，{d128['bmax']}段对话就把内存装满了，每百万词元至少要{d128['cost'][-1]:.2f}美元。这就是长上下文更贵的原因，也是这一部分花这么多篇幅讲怎样缩小缓存的原因。",

    # ---------------------------------------------------------------- Scheduling
    'Chapter four. Continuous batching.':
        '第4章。连续批处理。',

    'f"A server has many conversations to write at once,':
        "一台服务器同时有很多段对话要写，它们不是一起到达，也不是一起结束。<bookmark mark='a'/>直到2022年，通常的做法都是静态批处理：凑齐一批，把所有提示都预填充，然后一直解码，直到这批里的每个回答都写完。短的回答写完了，它的位置就空着，等最长的那个写完；新来的请求只能在外面等。<bookmark mark='b'/>2022年，首尔国立大学的一个团队在一个叫Orca的系统里提出了解决办法：每一步都调度一次，而不是每一批才调度一次。<bookmark mark='c'/>一段对话一结束，它的位置就在紧接着的下一步交给下一个等待者。这是同一批请求，两种方式各跑一遍，用的是这台电脑上测得的成本：连续批处理{t_c:.1f}秒就全部写完；静态批处理要{fin_s:.1f}秒。",

    'f"With more traffic the difference is stark.':
        "流量一大，差别就很明显了。<bookmark mark='a'/>我们按这台电脑上测得的成本，模拟了一台服务器：400个请求随机到达，每秒{s['rate']:g}个，长度呈长尾分布，就像真实的聊天。<bookmark mark='b'/>静态批处理{st_say}连续批处理每秒写出{tp[1]:.0f}个，是它的{x_(gain)}倍，{co_say}<bookmark mark='c'/>再看等到第一个词元要多久：{wait_say}从那以后，服务系统一直是这样工作的。",

    'f"can\'t keep up: they write':
        '跟不上：它每秒写出{tp[0]:.0f}个词元，比请求的还少，所以队列越排越长。',

    "f'write {tp[0]:.0f} tokens a second, and keep up.'":
        '每秒写出{tp[0]:.0f}个词元，跟得上。',

    "f'a median of {tt[0]:.0f} seconds":
        '静态批处理的中位数是{tt[0]:.0f}秒，连续批处理是{1000.0 * tt[1]:.0f}毫秒。',

    "f'a median of {1000.0 * tt[0]:.0f} milliseconds":
        '静态批处理的中位数是{1000.0 * tt[0]:.0f}毫秒，连续批处理是{1000.0 * tt[1]:.0f}毫秒。',

    'f"Continuous batching has a cost of its own.':
        "连续批处理也有它自己的代价。<bookmark mark='a'/>新的提示加入时，它的整个预填充都在一步之内跑完，批里的每段对话都得等它。<bookmark mark='b'/>在我们的模拟里，一个回答相邻两个词元之间的间隔，中位数是{1000.0 * c['gap'][0]:.0f}毫秒，最长的却有{1000.0 * c['gap'][3]:.0f}毫秒。<bookmark mark='c'/>2024年，Sarathi-Serve把提示切成小块，并给每一步定一个预算：先放下所有的解码，再放进尽量多的提示。<bookmark mark='d'/>用256个词元的块，最长的间隔降到{1000.0 * ch['gap'][3]:.0f}毫秒，只有原来的{x_(cut)}分之1，中位数却几乎不变。",

    'f"There is another way to keep prompts from stalling answers':
        "还有一种办法，能让提示不耽误回答：把它们放到不同的机器上。<bookmark mark='a'/>预填充是运算，解码是内存，所以2024年，Splitwise和DistServe给两者各配了自己的GPU，每个提示处理完，就把它的缓存传过去。DeepSeek就是这样部署V3的：预填充以{F.DSV3['prefill_unit'][1]}块GPU为一个单元，解码以{F.DSV3['decode_unit'][1]}块为一个单元。<bookmark mark='b'/>我们在模拟里试了一下：四个既做预填充又做解码的工作节点，对比一个专做预填充、三个专做解码的。<bookmark mark='c'/>{verdict}",

    "f'Splitting cut the 99th-percentile gap {x_(tail)} times, but":
        '拆开之后，第99百分位的间隔缩短到原来的{x_(tail)}分之1，可等待第一个词元的中位时间，却变成了原来的{x_(dt)}倍，因为现在所有的预填充都压在一个节点上：怎么拆，要按流量来定。',

    "f'Splitting cut the 99th-percentile gap {x_(tail)} times, with":
        '拆开之后，第99百分位的间隔缩短到原来的{x_(tail)}分之1，而第一个词元并没有因此变慢。',

    "Here splitting didn't help the gaps:":
        '在这里，拆开并没有缩短间隔：我们的提示都很短，彼此本来就干扰不大。',

    # ---------------------------------------------------------------- Paging
    'Chapter five. Pages and shared prefixes.':
        '第5章。分页与共享前缀。',

    'f"Where in memory should each conversation':
        "每段对话的缓存，该放在内存的什么地方？没人知道一个回答会有多长。<bookmark mark='a'/>所以，服务器过去会为每段对话预留出允许的最长回答所需的空间，在这里是{mx:,}个词元。大部分空间都空着：在我们模拟的服务器里，平均只有{used[0]:.0f}%的内存装着词元，同时只能容纳{run[0]:.1f}段对话。2023年，vLLM团队测得真实系统只用上了20%到38%。<bookmark mark='b'/>正好预留所需的长度，就得预知未来；而且随着对话来来去去，内存还是会被切得七零八落：{used[1]:.0f}%。<bookmark mark='c'/>vLLM的答案来自操作系统：虚拟内存。把缓存切成每页16个词元，每一页放在哪里都行，再用一张表记下它们的位置。对话需要时，才领一页。<bookmark mark='d'/>现在{used[2]:.0f}%的内存装着词元，同时能容纳{run[2]:.1f}段对话，是原来的{x_(cg)}倍；{tsay}",

    "f'and it writes {x_(tg)} times":
        '每秒写出的词元数，也是原来的{x_(tg)}倍。',

    'f"Here that buys only':
        '不过在这里，每秒的词元数只多了{100 * (tg - 1):.0f}%，因为在这台电脑上，每多一段对话，读它自己那份缓存的开销，几乎就抵掉了它带来的收益；在GPU上，读权重才是大头，vLLM测得的是2到4倍。',

    'f"How big should a page be?':
        "一页该多大？<bookmark mark='a'/>平均来说，一段对话的最后一页会空着一半，所以浪费的比例，大约是半页除以对话的长度，这里对话长{L:.0f}个词元。<bookmark mark='b'/>页小，浪费就少，但页表就长，每个注意力步都要查它。vLLM选了16个词元：对我们的对话来说，浪费了{w[k16]:.1f}%的内存。256个词元一页的话，会浪费{w[-1]:.0f}%。",

    'f"Pages make one more thing possible: sharing.':
        "分页还让另一件事成为可能：共享。<bookmark mark='a'/>大多数请求的开头都一样：系统提示、指令、之前的对话。它们的键和值每次都一样，所以只算一次，把这些页留着，凡是这样开头的请求，都指向它们。<bookmark mark='b'/>我们模拟了40段对话，每段6轮，全都以一个{sysn}词元的系统提示开头。如果给前缀留1000个词元的空间，{saved[1]:.0f}%的提示词元不必重算；如果什么都留得下，是{saved[-1]:.0f}%，因为每一轮都会重复之前的对话。<bookmark mark='c'/>在我们的模型上，预填充一个256词元的提示要{tf:.0f}毫秒；如果前224个词元已经在缓存里，只要{ts:.0f}毫秒：速度是原来的{x_(tf / ts)}倍。2023年，SGLang把这些前缀存在一棵树里；从2024年起，DeepSeek对它在缓存里找到的输入，最多少收{F.DEEPSEEK_CACHE['cut']}%的钱。",

    # ---------------------------------------------------------------- Exact
    'Chapter six. Guess ahead, check at once.':
        '第6章。先猜几步，一次核对。',

    'Chapter one showed that decoding one conversation':
        "第1章说过，只为一段对话解码时，芯片的算力是闲着的，而每跑一遍都要读遍所有权重。<bookmark mark='a'/>那就让一个又小又快的模型，先往前起草几个词元。<bookmark mark='b'/>然后，大模型只跑一遍，就把它们全部核对一遍，就像读提示那样：读一次权重，换来好几个词元。<bookmark mark='c'/>它认可的草稿就留下；碰到第一处分歧，就采用大模型自己的选择，再从那里重新开始。2018年，米切尔·斯特恩、诺姆·沙泽尔和雅各布·乌斯科雷特，就为一个总是选最可能词元的模型这样做过。",

    'f"Sampling is harder:':
        "采样就难一些了：大模型没有唯一的答案，它有的是一个分布，而草稿来自另一个分布。2022年底，谷歌的亚尼夫·列维坦、马坦·卡尔曼和约西·马蒂亚斯找到了一条规则，能让输出分毫不差，DeepMind查理·陈的团队也找到了它。<bookmark mark='a'/>这是两个模型对下一个字符的猜测，用的是我们自己的模型：第13部分的Transformer当大模型，一个只看前两个字符的计数模型当草稿。<bookmark mark='b'/>草稿里的一个字符，以q分之p的概率被接受，最大取1：草稿把哪个字符猜得太频繁，多出来的部分就被扔掉。<bookmark mark='c'/>如果被拒绝，就从p减去q之后剩下的部分里采样：恰好是草稿猜得太少的地方。<bookmark mark='d'/>把这条规则运行{int(s['N']):,}次：它写出的字符，{same}。",

    'Why is that exact?':
        "为什么它是精确的？<bookmark mark='a'/>这条规则写出x，有两种途径：要么x被起草出来并被接受，要么某个草稿被拒绝、然后重新采样得到x。<bookmark mark='b'/>起草并被接受的概率，是q乘以接受概率，也就是p和q中较小的那个。<bookmark mark='c'/>被拒绝的概率是1减去这些最小值之和；因为p的总和是1，这也就是p剩余部分的总和。<bookmark mark='d'/>而重新采样所用的分布，正是这部分剩余，再除以同一个和来归一化。<bookmark mark='e'/>乘起来，两个和正好约掉：最小值加上剩余部分，就是p。不管草稿是什么，写出的词元都恰好服从大模型的分布。草稿只决定，能省下多少遍。",

    'f"One more check, on the novels model,':
        "再做一次检验，在小说模型上，用的是下一章要训练的那个小草稿模型。<bookmark mark='a'/>在一部留出的小说里的某个位置，我们每次起草两个词元，让这条规则运行{int(jt['N']):,}次，记下它写出的前两个词元。精确的答案是已知的：大模型给第一个词元的概率，乘以在第一个词元之后它给第二个词元的概率。<bookmark mark='b'/>{verdict}：总变差是{jt['tv_spec']:.3f}，直接采样是{jt['tv_direct']:.3f}。<bookmark mark='c'/>如果不核对就直接留下草稿，得到的就是草稿的分布：{jt['tv_naive']:.3f}。",

    'Speculative sampling is as close to exact':
        '推测采样和直接从大模型采样一样接近精确答案：剩下的只是有限样本的噪声',

    'Speculative sampling lands farther from exact':
        '推测采样离精确答案比直接采样更远，超出了有限样本的噪声',

    # ---------------------------------------------------------------- Drafters
    'Chapter seven. Drafters.':
        '第7章。草稿模型。',

    'How much does it save?':
        "它能省下多少？把一个草稿词元被接受的概率叫作α，并且暂时假设，每个草稿能否存活彼此独立。<bookmark mark='a'/>那么前i个草稿全部存活的概率，就是α的i次方。<bookmark mark='b'/>前i个草稿都存活时，这一遍就会写出第i加1个词元；而且它总会写出一个词元，也就是它自己的那个。所以每遍期望写出的词元数，是α的i次方从0到k求和。<bookmark mark='c'/>这是一个几何级数：1减α的k加1次方，除以1减α。<bookmark mark='d'/>起草不是免费的：如果起草一步的开销相当于大模型跑c遍，就再除以1加k乘c。列维坦和同事推导的正是这个结果。",

    'f"Where does a draft come from?':
        "草稿从哪里来？我们在这台电脑上，为小说模型训练了两个。<bookmark mark='a'/>第一个就是一个小语言模型：两层而不是六层，在同样的小说上训练了{mins_d:.0f}分钟。<bookmark mark='b'/>第二个仿照EAGLE，来自Yuhui Li和同事2024年的工作。它根本不读文本。它读的是大模型最后一层的隐藏状态，加上刚选出的词元，预测下一个隐藏状态，再由大模型自己的输出层把它变成词元。它只有一个模块，在大模型冻结的情况下训练了{mins_e:.0f}分钟。<bookmark mark='c'/>在它们训练的过程中，我们在留出的文本上测量它们的接受率：一个草稿词元通过核对的概率。<bookmark mark='d'/>小模型达到{ev_d[-1, 2]:.2f}；EAGLE头达到{ev_e[-1, 2]:.2f}：{why_}。",

    "reading the big model's own features,":
        'EAGLE头读的是大模型自己的特征，起点远远高于一个小模型能学到的东西',

    'the small model, reading the text itself,':
        '直接读文本的小模型，最终反而猜得更准',

    'f"Now the real thing:':
        "现在来真的：在12段留出的开头上做推测采样，每段96个词元。<bookmark mark='a'/>每遍起草4个时，小模型能让大模型每跑一遍得到{meas['draft'][k4]:.2f}个词元，EAGLE头是{meas['eagle'][k4]:.2f}个。<bookmark mark='b'/>图中的线是那个公式，α用第一个草稿测得的值。{fit}<bookmark mark='c'/>{dep_say}<bookmark mark='d'/>{greedy_say}",

    'f"Draft by draft, the head\'s acceptance falls':
        '一个草稿接一个草稿地看，EAGLE头的接受率，从第一个的{e0:.2f}，降到第四个的{e3:.2f}，因为它是在拿自己的猜测当输入；小模型则从{d0:.2f}变到{d3:.2f}。',

    'f"Draft by draft, the head\'s acceptance goes':
        '一个草稿接一个草稿地看，EAGLE头的接受率，从第一个的{e0:.2f}，变到第四个的{e3:.2f}，小模型则从{d0:.2f}变到{d3:.2f}：一段文本一旦好猜，下一个草稿往往也会猜对。',

    "f'Decoding greedily, the drafts survive more often":
        '如果用贪心解码，草稿存活得更多：{who}每遍能得到{gr[best]:.2f}个词元。',

    "f'Decoding greedily, {who} gets":
        '如果用贪心解码，{who}每遍能得到{gr[best]:.2f}个词元。',

    'The formula, with its one number alpha,':
        '这个公式只用α一个数，就把测量结果预测得很好。',

    'The measurements beat the formula:':
        '测量结果比公式更好：接受与否并不独立，遇到好猜的段落，好几个草稿会接连通过。',

    'The formula is only a guide:':
        '这个公式只能作为参考：接受与否并不独立，后面的草稿建立在前面的猜测之上，境遇和第一个不一样。',

    '"And the clock?':
        "那么，看时钟呢？<bookmark mark='a'/>在这台电脑上，{check}<bookmark mark='b'/>{verdict}<bookmark mark='c'/>在GPU上，跑一遍几个词元和跑一遍一个词元的开销差不多，公开发表的系统表现更好。Medusa给模型加上额外的头；EAGLE-3报告最快到6.5倍；DeepSeek-V3则在预训练时就训练了自己的草稿模型，也就是第18部分的多词元预测模块，它的第二个词元有85%到90%的时候被接受。",

    'f"checking five tokens in one pass costs {five':
        '一遍核对5个词元的开销，是1个词元的{five:.1f}倍：处理器核心没有多少富余的算力，所以核对并不像在GPU上那样几乎免费。',

    "f'checking five tokens in one pass costs only":
        '一遍核对5个词元的开销，只是1个词元的{five:.1f}倍：这一遍主要是在读权重，和GPU上一样。',

    "f'The best, {name} with {best_c[1]} drafts, writes":
        '最好的是{name}，每遍起草{best_c[1]}个，写一个词元要{tpt[best_c]:.2f}毫秒，不用草稿要{plain:.2f}毫秒：速度是原来的{sp:.1f}倍。',

    "f'The best, {name} with {best_c[1]} drafts, is barely":
        '最好的是{name}，每遍起草{best_c[1]}个，也只是快了一点点：每个词元{tpt[best_c]:.2f}毫秒，不用草稿是{plain:.2f}毫秒。',

    "f'The best, {name} with {best_c[1]} drafts, is no":
        '最好的是{name}，每遍起草{best_c[1]}个，却一点也没有更快：每个词元{tpt[best_c]:.2f}毫秒，不用草稿是{plain:.2f}毫秒。',

    # ---------------------------------------------------------------- Rounding
    'Chapter eight. Rounding error.':
        '第8章。舍入误差。',

    'Quantization is the other half of this part:':
        "量化是这一部分的另一半：用更少的比特存每个数，就能少搬运一些字节。<bookmark mark='a'/>最简单的量化，把每个权重舍入到一组等间距的值里最近的那个，相邻两个值相隔一个步长δ。误差e在两个方向上都不超过半个步长。<bookmark mark='b'/>如果权重平滑地铺在很多个步长上，误差落在这个区间里任何地方的可能性都一样，它的均方，就是e的平方在区间上的积分，再除以δ。<bookmark mark='c'/>结果是δ的平方除以12。这是贝尔实验室的W. R. 贝内特在1948年算出来的，当时是为了把语音和电视信号变成数字来传送。<bookmark mark='d'/>用b个比特，关于0对称，步长由最大的权重决定：δ等于最大值，除以2的b减1次方再减1。<bookmark mark='e'/>所以每多一个比特，步长减半，误差变成四分之一：就像音频工程师说的，每个比特6分贝。",

    'f"Does it hold for a real model?':
        "它在真实的模型上成立吗？<bookmark mark='a'/>我们把小说模型的所有模块权重，每个矩阵的每一行配一个缩放因子，分别舍入到2到8比特，测出均方误差。<bookmark mark='b'/>从{bits[ok]}比特往上，测量值和δ平方除以12相差不到{100 * max(abs(ratio[ok:] - 1)):.1f}%：这些线是直的，每个比特差4倍。<bookmark mark='c'/>到2比特时，公式高估了误差：大多数权重这时都落在0那一格里，它们的误差只是它们自己那点小小的数值，并没有铺满整个步长。<bookmark mark='d'/>灰色的点是整个矩阵只用一个缩放因子：每个误差都更大，因为任何地方的一个大权重，都会替其余所有权重定下步长。",

    'f"Here is why the scale':
        "这就是缩放因子管多大范围很重要的原因。<bookmark mark='a'/>这是我们模型里一个矩阵的权重：大多数都挤在0附近窄窄的一条带里。<bookmark mark='b'/>如果整个矩阵只用一个4比特缩放因子，它唯一那个最大的权重就定下了步长，大多数权重只能挤在0附近的寥寥几个值上。<bookmark mark='c'/>一行典型的最大权重，只有整个矩阵最大权重的{x_(ratio)}分之1，所以每行一个缩放因子，就能把这些值放到这一行的权重所在的地方。每32个或64个权重一组配一个缩放因子，效果更好，只是每组要多花几个比特来存。",

    '"What the model loses:':
        "模型损失了什么：它在留出小说上的损失，每种位宽、每种缩放方式都测一遍。<bookmark mark='a'/>{say8}<bookmark mark='b'/>到4比特，就要看缩放因子了：整个矩阵一个，每个词元损失{L['tensor'][i4]:.3f}奈特；每行一个，{L['row'][i4]:.3f}；每32个权重一个，{L['32'][i4]:.3f}，算下来每个权重一共{bpw['32'][i4]:.1f}比特。<bookmark mark='c'/>到3比特，简单舍入开始伤筋动骨了，每行一个缩放因子也要损失{L['row'][i3]:.2f}奈特；到2比特，模型就坏掉了。<bookmark mark='d'/>后面的所有内容，都是为了在3比特和4比特上做得比简单舍入更好。",

    'At eight bits, nothing measurable is lost.':
        '8比特时，测不出任何损失。',

    "f'At eight bits, the loss grows by":
        '8比特时，损失增加了{L[\'row\'][i8]:.4f}奈特。',

    # ---------------------------------------------------------------- Outliers
    'Chapter nine. Outliers and SmoothQuant.':
        '第9章。离群值与SmoothQuant。',

    'f"Weights are only half of a matrix product.':
        "权重只是矩阵乘法的一半。要用8比特或4比特来做运算，输入，也就是激活值，也得舍入，而且每个词元都要现场舍入。<bookmark mark='a'/>2022年，蒂姆·德特默斯和同事发现了这件事难在哪里。从大约67亿参数起，有少数几个特征维度，大约占千分之一，携带的值比其余的大到20倍，而且每一层都是如此。<bookmark mark='b'/>我们的模型小得多，但这种效应已经出现了。这是一层的每个通道在校准文本上见过的最大输入。最大的是中位数的{ratio:.1f}倍。<bookmark mark='c'/>如果一个词元的激活值只用一个缩放因子来舍入，这几个通道就替其余所有通道定下了步长，其余通道只能分到寥寥几个值。",

    'f"SmoothQuant, from Guangxuan Xiao':
        "SmoothQuant出自MIT和NVIDIA的Guangxuan Xiao和同事，2022年，它把问题挪了个地方。<bookmark mark='a'/>一个线性层，是X乘以W。<bookmark mark='b'/>把激活值的第j个通道除以一个数s j，再把权重的同一个通道乘以它：乘积不变，而且这次除法可以并进前一层，所以运行时不花任何代价。<bookmark mark='c'/>s j取激活值范围的α次方，除以权重范围的1减α次方。<bookmark mark='d'/>α取二分之一时，两边最后的范围一样，都是两者的几何平均。激活值的离群值被抹平到了权重里，而权重是离线舍入的，承受得住：在我们这一层上，最大的激活值从中位数的{sa:.1f}倍，降到了{sb:.1f}倍。",

    'f"What does it buy on our model?':
        "在我们的模型上，它换来了什么？<bookmark mark='a'/>8比特时，什么都不需要：每种方法和完整模型相差都在{d8:.4f}奈特以内。<bookmark mark='b'/>6比特时，代价开始出现。<bookmark mark='c'/>到4比特，把每个模块的输入都简单舍入，每个词元损失{p4:.3f}奈特；{s_say}；而像LLM.int8()处理离群值那样，把最大的1%的通道保留为全精度，损失{k4:.3f}。<bookmark mark='d'/>我们的离群值很温和，是中位数的{o['ratio'][o['worst']]:.0f}倍，而不是20倍，所以没多少可抹平的。4比特的激活值需要更强的手段：在下下一章。",

    "f'SmoothQuant helps only a little,":
        'SmoothQuant只帮了一点点，{s4:.3f}',

    "f'SmoothQuant cuts that to":
        'SmoothQuant把它降到{s4:.3f}，少了{100 * (1 - s4 / p4):.0f}%',

    # ---------------------------------------------------------------- GPTQ
    'Chapter ten. GPTQ, from Optimal Brain Surgeon.':
        '第10章。GPTQ：从最优脑外科说起。',

    'Plain rounding treats each weight alone.':
        "简单舍入是把每个权重单独处理的。但真正要紧的，是这一层的输出。<bookmark mark='a'/>对一层W，在真实输入X上，输出的误差是对每一行求和，每一行是舍入误差的一个二次型，矩阵是H。<bookmark mark='b'/>H是X乘以X的转置，也就是输入的二阶矩，用一点校准文本就能估出来。<bookmark mark='c'/>两个输入一起变化时，一个权重上的误差，可以靠轻推另一个权重来抵消：沿着这个二次型的山谷走很便宜，横穿它就很贵。所以，舍入一个权重，然后用还没舍入的那些权重去弥补损失。",

    'The question is old.':
        "这个问题由来已久。<bookmark mark='a'/>把第q个权重固定在舍入后的值上，其余所有权重移动δ，让输出误差，也就是二分之一δ转置Hδ，尽可能小。<bookmark mark='b'/>用拉格朗日乘子，最优解满足Hδ与第q个权重的方向平行。<bookmark mark='c'/>解出来：δ等于舍入误差除以H逆的第q个对角元，再乘以H逆的第q列。<bookmark mark='d'/>剩下的误差，是舍入误差的平方，除以那个对角元的2倍。<bookmark mark='e'/>这就是巴巴克·哈西比和大卫·斯托克1993年提出的最优脑外科，它承接了杨立昆的最优脑损伤：他们用它来给网络剪枝。2022年，埃利亚斯·弗朗塔尔和丹·阿利斯塔尔用它来做舍入。",

    '"Rounding one weight at a time,':
        "一次舍入一个权重，每次都做最优的更新，对几十亿个权重来说太慢了。<bookmark mark='a'/>GPTQ出自弗朗塔尔、阿什克布斯、霍夫勒和阿利斯塔尔，2022年，它做了三处改动：按一个固定的顺序舍入各列，每一行都用同一个顺序；所有的更新，都来自H逆的同一次楚列斯基分解；并且分块来做。一个1750亿参数的模型，只用了大约4个GPU时。<bookmark mark='b'/>这是它在我们模型一个真实层的一行上，3比特时的样子。每一列被舍入，它的误差被推给后面还没处理的列。<bookmark mark='c'/>最终的权重，并不是离原值最近的那些值，也就是灰色的轮廓，{trace_say}<bookmark mark='d'/>放到整个层上，每个输入都能分担误差，GPTQ的误差是{lg_:.3f}，而简单舍入是{lr_:.3f}。",

    "f'but together they make a better output:":
        '但合在一起，它们给出更好的输出：在校准输入上误差是{eg:.3f}，而逐个单独舍入是{er:.3f}。',

    "f'but together they make a slightly better output:":
        '但合在一起，它们给出稍好一点的输出：在校准输入上误差是{eg:.3f}，而逐个单独舍入是{er:.3f}。只有16个权重，能用来弥补误差的余地很小。',

    'f"A simpler idea came next.':
        "接着出现了一个更简单的想法。2023年，Ji Lin和同事注意到，一个权重有多重要，和它的输入有多大成正比。<bookmark mark='a'/>所以，舍入之前，把每个输入通道的权重乘以s，再把输入除以s，这一步可以免费并掉。相对于这个通道，舍入误差缩小到原来的s分之1。<bookmark mark='b'/>AWQ让s等于这个通道输入的平均大小，再取一个α次方，α在校准文本上挑选：这就是激活感知的权重量化。<bookmark mark='c'/>在我们的模型上，最好的α很小，在{min(alphas):.2f}到{max(alphas):.2f}之间：我们的输入相当均匀，没多少需要保护的。",

    'f"All three, on the whole model:':
        "三种方法，用在整个模型上：每个模块矩阵都舍入，在留出小说上测损失；GPTQ和AWQ各自在三份不同的文本样本上校准。<bookmark mark='a'/>4比特、每64个权重一个缩放因子时，简单舍入每个词元损失{r4:.3f}奈特，GPTQ损失{g4:.3f}。<bookmark mark='b'/>3比特、每行一个缩放因子时，{gptq_say}至于AWQ，{awq_say}<bookmark mark='c'/>把误差花在输入不在意的方向上，正是让3比特和4比特变得可用的关键。",

    "f'the difference is large:":
        '差别就大了：简单舍入损失{r3:.3f}，GPTQ损失{g3:.3f}，少了{100 * cut3:.0f}%，不管它看的是哪份校准文本。',

    "f'rounding costs {r3:.3f}, GPTQ {g3:.3f} on average":
        '简单舍入损失{r3:.3f}，GPTQ平均损失{g3:.3f}，少了{100 * cut3:.0f}%，具体少多少，要看校准文本。',

    "f'it costs {a3:.3f}: on our model":
        '它损失{a3:.3f}：在我们的模型上，几乎没什么帮助。',

    "f'it costs {a3:.3f}, {100":
        '它损失{a3:.3f}，比简单舍入少{100 * (1 - a3 / r3):.0f}%。',

    # ---------------------------------------------------------------- Rotation
    'Chapter eleven. Rotations.':
        '第11章。旋转。',

    'f"In 2024 Saleh Ashkboos, Dan Alistarh':
        "2024年，萨利赫·阿什克布斯、丹·阿利斯塔尔和同事找到了一个办法，让离群值干脆消失，而不是绕着它们走。<bookmark mark='a'/>从每一层前面的归一化说起，也就是RMSNorm：把一个向量除以它的长度，再乘以一个学到的增益γ，而γ可以并进下一层的权重里。<bookmark mark='b'/>剩下的就是除以长度，而旋转不改变长度，所以对旋转过的向量做归一化，等于把归一化过的向量旋转一下。<bookmark mark='c'/>于是，把整条残差流都用Q旋转：每个读它的层，拿到W乘以Q；每个往里写的层，拿到Q转置乘以W，<bookmark mark='d'/>嵌入层和输出头也都乘上Q。整个网络算的还是完全相同的函数。我们在自己的模型上验证过：任何一个logit最大的变化，是{mant}乘以10的{int(ex)}次方，也就是舍入误差。",

    'f"Which rotation?':
        "用哪个旋转？<bookmark mark='a'/>这是我们模型某一层的一个词元的输入，一个通道一个通道地画出来。它最大的分量，平均下来是典型大小的{r['crest']:.1f}倍。<bookmark mark='b'/>用一个哈达玛矩阵来旋转它：元素是正负根号n分之1，可以靠不断加倍构造出来，用n log n步就能算完，就像快速傅里叶变换。每个输出都平等地混合了所有输入，所以一个通道里的尖峰，会被摊到所有通道上。<bookmark mark='c'/>现在峰值只是典型大小的{r['crest_rot']:.1f}倍：每个词元一个缩放因子，就能照顾到它所有的通道，4比特的那些值，不再被浪费。",

    'f"Now the hard case:':
        "现在来看难的情形：4比特权重加4比特激活值，每个模块的输入都现场舍入。<bookmark mark='a'/>直接做的话，我们的模型每个词元损失{p:.3f}奈特；SmoothQuant是{vals[1]:.3f}。<bookmark mark='b'/>先旋转：残差流用一个哈达玛矩阵，每个前馈输出层的输入用一个随机旋转，{say}。<bookmark mark='c'/>{rnd_say}<bookmark mark='d'/>{learn_say}",

    "f'Three different random rotations give {min(rnd):.3f} to {max(rnd):.3f}: on our model":
        '三个不同的随机旋转，给出{min(rnd):.3f}到{max(rnd):.3f}：在我们的模型上，几乎一样。但在2024年，Meta的Zechun Liu和同事发现，在大模型上，不同的随机旋转在一个基准上最多能差13分，于是问：为什么不把旋转学出来？',

    "f'Three different random rotations give {min(rnd):.3f} to {max(rnd):.3f}. In 2024":
        '三个不同的随机旋转，给出{min(rnd):.3f}到{max(rnd):.3f}。2024年，Meta的Zechun Liu和同事注意到了这样的差别，在一个基准上最多差13分，于是问：为什么不把旋转学出来？',

    "f'We did, small: {lv:+.3f}, better":
        '我们也做了，小规模的：{lv:+.3f}，比它出发时的哈达玛旋转更好。',

    "f'We did, small: {lv:+.3f}, no better":
        '我们也做了，小规模的：{lv:+.3f}，并不比它出发时的哈达玛旋转更好。',

    "f'We did, small: {lv:+.3f}, a little worse":
        '我们也做了，小规模的：{lv:+.3f}，比它出发时的哈达玛旋转还差一点。',

    "f'the Hadamard rotation cuts it to":
        '哈达玛旋转把它降到{h_:.3f}，少了{100 * cut:.0f}%',

    "f'the Hadamard rotation barely changes it":
        '哈达玛旋转几乎没改变它，{h_:.3f}',

    '"Learning a rotation needs care,':
        "学习一个旋转需要小心，因为在旋转矩阵上走一步梯度，它就不再是旋转了。<bookmark mark='a'/>SpinQuant从构造上保证它始终是旋转。把Q写成哈达玛矩阵乘以一个反对称矩阵A的凯莱映射：每个A都给出一个旋转，所以A可以随便训练。<bookmark mark='b'/>我们在4比特权重和激活值下，用我们模型的损失来训练A，梯度直接穿过舍入，从哈达玛旋转出发。<bookmark mark='c'/>{learn_say}",

    'f"Over {st} steps the held-out loss fell':
        '训练{st}步，留出损失从{ev[0, 1]:.3f}降到{ev[-1, 1]:.3f}：这个旋转学到了我们模型的离群值在哪里。',

    "f'Over {st} steps the held-out loss went":
        '训练{st}步，留出损失从{ev[0, 1]:.3f}变到{ev[-1, 1]:.3f}：哈达玛这个起点，已经接近这种训练所能找到的最好结果。',

    "f'Over {st} steps the held-out loss rose":
        '训练{st}步，留出损失反而从{ev[0, 1]:.3f}升到{ev[-1, 1]:.3f}：这个旋转拟合的是它那一点点校准文本，而不是小说。',

    # ---------------------------------------------------------------- Formats
    'Chapter twelve. Four-bit floats: MXFP4 and NVFP4.':
        '第12章。4比特浮点数：MXFP4与NVFP4。',

    'Part 17 met the smallest floating-point format in use,':
        "第17部分见过正在使用的最小的浮点格式，FP4，布局是E2M1。<bookmark mark='a'/>1个符号位，2个指数位，1个尾数位：16个编码，8种大小。<bookmark mark='b'/>0和0.5，然后是1和1.5，2和3，4和6：在每个2的幂之内，间隔都一样，从一个幂到下一个幂，间隔翻倍。<bookmark mark='c'/>单靠它自己，只能覆盖0到6。要存一个模型的权重，而权重根本不是这个大小，就得给每一块权重配一个缩放因子，当今芯片上的两种格式，区别恰恰在于怎么配。",

    'f"MXFP4 comes from the Open Compute Project':
        "MXFP4来自开放计算项目2023年9月的微缩放标准，由AMD、Arm、英特尔、Meta、微软、NVIDIA和高通共同制定。<bookmark mark='a'/>这是我们模型里的32个真实权重，一个块。<bookmark mark='b'/>这个块共用一个缩放因子，而且缩放因子必须是2的幂，用一个8比特的指数来存，叫E8M0。规则是：取块里最大权重的指数，减去2，让这个权重落在4到8之间：这里是2的{e}次方。<bookmark mark='c'/>把每个权重除以缩放因子，舍入到最近的E2M1值，保留它的4比特编码：就是中间那一行。解码回来，是最后一行。<bookmark mark='d'/>可是E2M1最大只到6。{clamp_say}在我们的整个模型里，有{100 * f['clipped_share']:.0f}%的块，最大的值都这样被削掉了一截：这就是缩放因子只能取2的幂的代价。",

    'f"This block\'s largest weight is {ratio:.2f} times the scale, above':
        '这个块里最大的权重，是缩放因子的{ratio:.2f}倍，超过了6，所以被截到6。',

    'f"This block\'s largest weight is {ratio:.2f} times the scale, below':
        '这个块里最大的权重，是缩放因子的{ratio:.2f}倍，没有超过6，所以什么都没被截掉。',

    "NVIDIA's NVFP4, on its Blackwell chips,":
        "NVIDIA的NVFP4，用在它的Blackwell芯片上，改了两处。<bookmark mark='a'/>每块16个数，这样一个大权重连累的邻居更少。<bookmark mark='b'/>而且块的缩放因子本身是一个小浮点数，8比特的E4M3，有3个尾数位：它几乎能把块里最大的权重恰好放到6上，所以什么都不会被截掉。<bookmark mark='c'/>E4M3能表示的范围有限，所以整个矩阵再配一个32比特的缩放因子，把每个块的缩放因子都挪进这个范围。<bookmark mark='d'/>代价是：每个权重4.5比特，而MXFP4是4.25比特。",

    '"Which is better on our model?':
        "在我们的模型上，哪个更好？<bookmark mark='a'/>每个模块权重都用两种方式各存一遍，缩放因子也算在内，在留出小说上测损失。<bookmark mark='b'/>{a}<bookmark mark='c'/>{b_say}",

    'f"NVFP4\'s finer, float-valued scales':
        'NVFP4更细的、取浮点值的缩放因子胜过了MXFP4：{nv:.4f}奈特，对{mx:.4f}。',

    "f'MXFP4 matches NVFP4 here:":
        '在这里，MXFP4和NVFP4打成平手：{mx:.4f}奈特，对{nv:.4f}。',

    'f"But give plain four-bit integers':
        '但如果给普通的4比特整数用上NVFP4的那套缩放因子，它们还会更好，{i16:.4f}：我们的权重在一个块内分布得很均匀，16个等间距的值，比E2M1那些不均匀的值更贴合它们。浮点数的用武之地，在范围更宽的数上，尤其是激活值，也因为芯片能直接拿它们做乘法。',

    "f'Four-bit integers with the same scales":
        '用同样缩放因子的4比特整数，结果是{i16:.4f}：并不比浮点数好。',

    'f"This is how a frontier-size open model fits on one chip.':
        "一个前沿规模的开放模型，就是这样装进一块芯片的。<bookmark mark='a'/>2025年8月，OpenAI发布了gpt-oss-120b：1170亿个参数，每个词元只用到其中50亿，因为大部分参数都在专家里。<bookmark mark='b'/>专家的权重用MXFP4存，其余的用16比特。加起来是{gib:.1f}GiB，和模型卡上的{o['ckpt_gib']}一致。<bookmark mark='c'/>如果全用16比特，它要{full / 1000000000.0:.0f}GB；用4比特，一块80GB的GPU就装得下。<bookmark mark='d'/>而且4比特正在进入训练本身：2026年，Kimi K3从一开始就用MXFP4学习它的权重，第18部分讲过。",

    # ---------------------------------------------------------------- KVQuant
    'Chapter thirteen. The cache in fewer bits.':
        '第13章。用更少的比特存缓存。',

    'f"Chapters two and three showed':
        "第2章和第3章说过，长对话的大头是缓存：用Llama 3.1 70B进行一段12.8万词元的对话，要保存{bnum(big):g}{bunit(big)}的键和值。所以，缓存也舍入吧。<bookmark mark='a'/>但键和值是两种不同的动物。这是我们模型的一个头在一段文本上的情况：每个键和值的分量有多大，按通道、按词元画出来。<bookmark mark='b'/>{chan_say}<bookmark mark='c'/>所以2024年，Zirui Liu和同事在KIVI里，给键每个通道配一个缩放因子，给值每个词元配一个缩放因子，两者都用2比特存。",

    '"On our model, the cache rounded as it is written,':
        "在我们的模型上，缓存在写入时就舍入，在留出小说上测损失。<bookmark mark='a'/>{say8}4比特时，每个词元一个缩放因子，损失{L['token_4'] - base:.3f}。<bookmark mark='b'/>3比特时，每个词元一个缩放因子，每个词元损失{t3:.3f}奈特；KIVI的分法是{k3:.3f}。<bookmark mark='c'/>到2比特，差别拉大了：按词元{t2:.2f}，旋转后{r2:.2f}，KIVI{k2:.2f}。{best_say}",

    'f"The keys have outlier channels,':
        '键有离群通道，整行对每个词元都很大，最大的是中位数的{ratio:.1f}倍；值最大的通道，只是它们中位数的{vratio:.1f}倍。',

    "f\"Both have channels larger than the rest:":
        '两者都有比其余更大的通道：键最大的是中位数的{ratio:.1f}倍，值是{vratio:.1f}倍。',

    'At eight bits, integer or FP8, nothing measurable is lost.':
        '8比特时，不管是整数还是FP8，都测不出任何损失。',

    "f'At eight bits, integer or FP8, the loss grows":
        '8比特时，不管是整数还是FP8，损失最多增加{max(e8, f8):.4f}奈特。',

    "The best here is KIVI's split.":
        '这里最好的是KIVI的分法。键的离群通道必须得到照顾：要么给它们单独的缩放因子，要么用旋转把它们摊开。',

    'The best here is the rotation.':
        '这里最好的是旋转。键的离群通道必须得到照顾：要么给它们单独的缩放因子，要么用旋转把它们摊开。',

    'Here one scale per token does best:':
        '在这里，每个词元一个缩放因子就是最好的：我们的键的离群通道太温和，用不着更多手段。',

    # ---------------------------------------------------------------- Flash
    'Chapter fourteen. FlashAttention.':
        '第14章。FlashAttention。',

    'f"Part 17 ended with FlashAttention,':
        "第17部分以FlashAttention收尾，并且答应要推导它。现在就来。<bookmark mark='a'/>GPU有一块大而慢的内存，HBM，还有一块芯片上小而快的内存，SRAM。计算注意力的标准做法，要把T乘T的分数表写出来，<bookmark mark='b'/>再读回来做softmax，写出概率，<bookmark mark='c'/>然后再把概率读一遍，去给值加权。<bookmark mark='d'/>输入很长时，这张表大得惊人：12.8万个词元时，单单一个头就要{tbl / 2 ** 30:.0f}GiB，而这么多的读写，让运算一直在等。2022年，斯坦福的Tri Dao和同事，展示了怎样根本不写出这张表。",

    'The key is the softmax.':
        "关键在于softmax。<bookmark mark='a'/>为了算得稳妥，要先减去最大的分数，这样指数就不会溢出，再除以总和：看起来，得先有整行才行。<bookmark mark='b'/>但其实可以一块一块地来，一路记着当前的最大值m。<bookmark mark='c'/>来了一个更大的分数时，就把到目前为止的和，乘以e的旧最大值减新最大值次方，重新缩放，再加上新这一块的各项。<bookmark mark='d'/>输出也这样保存，先不归一化，到最后再除以总和。NVIDIA的马克西姆·米拉科夫和娜塔莉亚·吉梅尔申在2018年发表了这种在线softmax。<bookmark mark='e'/>这是它在第13部分Transformer的一个真实查询上，一块一块地运行：看最大值怎样跳升，和又怎样缩小来给它腾地方。",

    'With that, the table is never needed.':
        "有了它，那张表就根本用不着了。<bookmark mark='a'/>取一块查询，放在快速内存里。<bookmark mark='b'/>让键和值一块一块地流过，每块都小到能放在它旁边；算出每块的分数，更新当前的最大值、和与输出，然后把这块扔掉。<bookmark mark='c'/>再处理下一块查询。<bookmark mark='d'/>我们在第13部分Transformer的真实注意力上验证过：分块算出的结果，和直接按公式算的一样，只差舍入误差，64位和32位的数都是如此。",

    'f"How much traffic does that save?':
        "这能省下多少读写？<bookmark mark='a'/>快速内存能放M个数，每个头大小为d，那么一块键和值能装下M除以4d个。<bookmark mark='b'/>键和值各读一次。<bookmark mark='c'/>查询和当前的输出，每处理一块键，就要读写一次：一共T除以B c次，加起来大约是12乘T的平方乘d的平方再除以M个数。<bookmark mark='d'/>标准做法是T的平方加T乘d，所以只要d的平方小于M，它就更小；Dao和同事还证明了，没有哪种精确的方法能对每个M都做得更好。<bookmark mark='e'/>用一块H100的共享内存，我们实际运行这个算法的循环，数了搬运的数：头大小为128时，只有标准做法的{r128:.1f}分之1；为64时，只有{r64:.1f}分之1。<bookmark mark='f'/>2023年的FlashAttention-2交换了循环的顺序，并且削减了矩阵乘法之间的工作；2024年的FlashAttention-3，在Hopper GPU上让数据搬运和运算重叠起来，达到了芯片峰值的75%。",

    # ---------------------------------------------------------------- ServeAttention
    'Chapter fifteen. Attention at serve time.':
        '第15章。服务时的注意力。',

    'f"FlashAttention was built for reading prompts,':
        "FlashAttention是为读提示而设计的，那时成千上万个查询共用每一块键。解码时，每段对话只有一个查询，面对的缓存却可能有一百万个键。<bookmark mark='a'/>FlashAttention把每个头的工作交给GPU的一个多处理器。只有一段对话、{heads}个头时，一块H100的{n}个多处理器里，只有{heads}个有活干：{100 * occ[0]:.0f}%。<bookmark mark='b'/>Flash-Decoding出自Tri Dao和同事，2023年，它还把缓存切成小块，并行地对每一块做注意力，再用和在线softmax一样的技巧，把部分结果合起来：每块的输出和总和，都乘以e的这块最大值减总最大值次方。<bookmark mark='c'/>每个头切成8块，芯片上就有{100 * occ[k8]:.0f}%有活干。我们在第13部分的注意力上验证了这种合并：精确到舍入误差。它的作者测得，在长上下文下，生成最快到原来的8倍。",

    'f"The other way to read less of the cache':
        "少读缓存的另一种办法，是少看一些。<bookmark mark='a'/>用全注意力，每一步都要读整个缓存，读的量随对话一起增长。<bookmark mark='b'/>gpt-oss是交替的：每隔一层，只回看128个词元，所以有一半的读取不再增长。到12.8万个词元时，它读的量只有全注意力的{rf / ro:.1f}分之1。<bookmark mark='c'/>2025年的Gemma 3，让六层里的五层只看1024个词元的窗口：只有{x_(rf / rg)}分之1。<bookmark mark='d'/>而DeepSeek在V3.2里的稀疏注意力，保留所有词元，但让一个又小又快的索引器，为每个查询挑出其中2048个。索引器仍然要扫一眼每个词元，用的是几个很小的8比特头，但主注意力的读取量不再增长：到12.8万个词元时，只有{x_(rf / rd)}分之1。<bookmark mark='e'/>在我们自己的模型上，窗口很容易试：{ctxs[-1]:,}个词元时，给8段对话解码一步，全注意力要{full[-1]:.1f}毫秒，128词元的窗口要{win[-1]:.1f}毫秒。它在质量上要付出多少代价，取决于模型学会了怎样利用它：这些模型都是带着各自的窗口训练出来的。",

    # ---------------------------------------------------------------- Grammar
    'Chapter sixteen. Constrained decoding.':
        '第16章。约束解码。',

    '"Programs that call a model often need':
        "调用模型的程序，常常需要它的回答符合固定的格式：一条记录、一次函数调用、一个数字。<bookmark mark='a'/>我们的小说模型从没见过这种东西。给它看三条旅店客人的记录，让它写下一条，<bookmark mark='b'/>它就又回去写小说了：{un_say}大模型要好得多，但对程序来说，“通常没问题”是不够的。",

    "f'of {gr['n']} tries, not one":
        "试了{gr['n']}次，一条合格的记录都没有。",

    "f'of {gr['n']} tries, {gr['valid_un']}":
        "试了{gr['n']}次，其中{gr['valid_un']}次是合格的记录。",

    'f"The fix is to make invalid output impossible.':
        "解决办法，是让不合格的输出根本不可能出现。<bookmark mark='a'/>把格式写成一个模式，也就是正则表达式，再把它编译成一个自动机：一些状态，以及在状态之间转移的字符。我们的自动机有{gr['states']}个状态。<bookmark mark='b'/>可是模型写的是词元，不是字符，一个词元可能有好几个字符长。2023年，布兰登·威拉德和雷米·卢夫在Outlines里，提前一次性建好一个索引：对每个状态、词表里的每个词元，把这个词元的字符送进自动机走一遍，记下它能不能活下来，以及落在哪个状态。<bookmark mark='c'/>对我们{V:,}个词元的词表，这花了{gr['t_index']:.2f}秒。一开始，只允许一个词元，就是左花括号；在名字中间，允许{gr['mid_allowed']:,}个。然后解码时，把每个不允许的词元的概率设为0，每一步查一次表就行。",

    '"<bookmark mark=\'a\'/> With the mask,':
        "<bookmark mark='a'/>加上掩码之后，{mask_say}至于速度，{cost_say}<bookmark mark='b'/>不过，看看那些名字。模型根本不知道这一栏该填什么；掩码只是排除了不可能的东西。掩码管得了形式，管不了意思。比模式更复杂的语法，比如带嵌套的JSON，还需要一个栈；2024年，XGrammar把这些也做快了。",

    "f'every one of the {gr['n']} outputs":
        "{gr['n']}个输出，每一个都是合格的记录。",

    "f'{gr['valid_co']} of the {gr['n']} outputs":
        "{gr['n']}个输出里，有{gr['valid_co']}个是合格的记录；其余的还没来得及收尾，就用完了长度。",

    "f'it costs nothing we can measure:":
        '它的开销小到测不出来：每个词元{tc:.2f}毫秒，不加掩码是{tu:.2f}毫秒。',

    "f'it costs {100 * over:.0f} percent":
        '每个词元要多花{100 * over:.0f}%的时间。',

    'f"Masking has a subtler flaw.':
        "掩码还有一个更隐蔽的毛病。<bookmark mark='a'/>让第13部分的字符模型，在《马耳他之鹰》的一行之后，写出五个名字中的一个，然后比较两样东西。<bookmark mark='b'/>一样是模型自己给每个完整名字的概率，在这五个名字上重新归一化：如果你一遍又一遍地采样，只留下这几个名字，得到的就是它。<bookmark mark='c'/>另一样，是掩码一个字母一个字母地，实际采出来的结果。在第一个字母上，掩码只问S、A或E有多大可能，而不管它会是哪个词的开头。于是{names[i_big]}得到了{100 * mk[i_big]:.0f}%，尽管模型给这个完整名字的概率只有{100 * ex[i_big]:.1f}%。<bookmark mark='d'/>每一步局部都合理的选择，加起来却是一个被扭曲的答案。2024年，Kanghee Park和同事展示了怎样改从真正的条件分布里采样。",

    # ---------------------------------------------------------------- Frontier
    'Chapter seventeen. The frontier, late 2026.':
        '第17章。前沿，2026年末。',

    'f"Reasoning models, Part 28':
        "推理模型，也就是第28部分的主题，是用词元来思考的，而每个词元都是一个解码步。<bookmark mark='a'/>2025年5月，DeepSeek对R1的更新，把它在一项高难度数学竞赛上的成绩，从{R['acc_old']:.0f}%提高到{R['acc_new']}%，部分原因就是想得更久：每道题{R['tokens_new'] // 1000}K个词元，而不是{R['tokens_old'] // 1000}K个。<bookmark mark='b'/>长度要花多少钱？拿第3章那个GPU服务模型的模型来，写出各种长度的回答，每次都同时容纳内存装得下的最多对话。<bookmark mark='c'/>词元多到{tok:.1f}倍，成本就高到{x_(ratio)}倍，因为缓存变大，批变小，每个词元都更贵了：从每百万{th[k1]['per_mtok']:.2f}美元，涨到{th[k2]['per_mtok']:.2f}美元。想得更久，是一个解码问题，而这一部分讲的一切，都是为了让它负担得起。",

    'f"Meanwhile the price of a token has collapsed.':
        "与此同时，词元的价格一落千丈。<bookmark mark='a'/>拿至少和最初的GPT-3一样好的、最便宜的OpenAI模型来看：2021年每百万词元60美元，2022年降价后20美元，2023年ChatGPT所用的模型2美元，2024年GPT-4o mini是1角5分。<bookmark mark='b'/>大约三年半里，价格只剩原来的{fr['price_total']:.0f}分之1，相当于每年降到{fr['price_fall']:.1f}分之1。<bookmark mark='c'/>Epoch AI追踪了许多基准，发现达到某个固定能力水平的价格，每年降到9分之1到900分之1不等，取决于任务。其中一部分归功于这一部分的方法，一部分归功于第17部分的硬件，还有一部分，是像第12部分讲的那样，用更多数据训练出的更小的模型。",

    'f"Chapter one\'s speed limit':
        "第1章的速度上限，还说明了谁能运行这些模型。<bookmark mark='a'/>用一台设备的内存带宽，除以一个词元要读的字节数。<bookmark mark='b'/>一台装着苹果M5的笔记本电脑，带宽每秒153GB，跑gpt-oss-20b最多每秒写{bound[i_m5, j_oss]:.0f}个词元，它的专家用MXFP4存，每个词元要读的不到2GB；一块H100，是{bound[i_h, j_oss]:,.0f}个。<bookmark mark='c'/>这就是为什么4比特格式和专家，对在家里运行模型这么重要，llama.cpp正是2023年从这里起步的；这也是为什么苹果2025年的端侧模型，是为2比特权重训练的。{eff_say}<bookmark mark='d'/>预填充和解码的分工，也正在走进硬件：2025年9月，NVIDIA发布了Rubin CPX，一种内存更便宜、算力充足的GPU，专门用来做读提示这种长上下文的工作，NVIDIA说它将在2026年底前出货。",

    "f'Our own model on this computer reaches":
        '我们自己的模型在这台电脑上，达到了它上限的{100 * eff:.0f}%。',

    "f\"Our own model on this computer beats its bound":
        '我们自己的模型在这台电脑上，超过了它的上限，达到{100 * eff:.0f}%：它的权重装得进处理器的缓存，而缓存比内存快。',

    # ---------------------------------------------------------------- Outro
    "Let's take stock.":
        '我们来盘点一下。读提示是运算，写回答是读内存，所以服务器把写回答成批地做，一个词元的价格，取决于它能负担多大的批。连续批处理让批始终是满的，分页让内存始终是满的。草稿模型先往前猜，大模型一遍核对，输出完全不变。舍入误差是δ平方除以12；GPTQ和旋转把它花在伤害最小的地方，4比特浮点数则把数存得紧凑。而FlashAttention，从来不把它的表写下来。',

    'All of this comes back.':
        '这些都会再出现。一次生成一个像素的图像，以及减少步数的竞赛，是第20和第21部分。推理模型用词元思考，而这些词元要靠解码来买单，在第28部分；智能体要跑很长的上下文，要做很多次共享前缀的调用，在第29部分。第9章的离群通道，是一条线索，指向模型内部那些方向的含义：第30部分会展示，一个网络怎样装下比它的维数还多的特征。而第31部分要问的是，怎样才能信任它输出的东西。',

    'Here are six problems to try,':
        '这里有六道习题可以试试，从草稿模型的公式，到Flash-Decoding的合并。在这里暂停一下，把它们做一做；完整的解答，都在这一部分的笔记里。',

    'Next time, the fourth act begins: generation.':
        '下一次，第四幕开始：生成。在扩散模型之前，有四种让模型学会创造的办法：一次一个像素；通过一个学到的编码；让两个网络相互博弈；或者，把空间本身弯折。第20部分：生成的四种方法。',

    'To go further, the vLLM and FlashAttention papers':
        '想深入下去，vLLM和FlashAttention的论文是很好的起点。感谢观看，第20部分见。',
}

PHRASES = {
    # units, said after a number (``{bnum(b):g} {bunit(b)}``)
    'bytes': '字节',
    'kilobytes': 'KB',
    'megabytes': 'MB',
    'gigabytes': 'GB',
    'terabytes': 'TB',
    # short spliced values
    'the points fall close to one line': '这些点差不多落在一条直线上',
    'and keeps up with the traffic.': '跟得上流量。',
    'and still falls behind.': '但仍然落在后面。',
    'as close to p as sampling p itself': '和直接从p采样一样接近p',
    'close to p': '接近p',
    'the small model': '小模型',
    'the EAGLE head': 'EAGLE头',
}
