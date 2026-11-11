"""Chinese narration for cs42: see tools/zh_lines.py (literal lines by prefix, computed lines as templates)."""

TITLE = "计算机科学，从零搭建 · 第42部分：浏览器与 Web"

CHAPTERS = {
    "Hook": "输入一个网址之后发生了什么",
    "History": "1. Web 的三十年",
    "Parsing": "2. 解析 HTML",
    "Css": "3. 层叠",
    "Layout": "4. 布局",
    "Rendering": "5. 绘制、图层与帧",
    "Loop": "6. 事件循环",
    "Engines": "7. JavaScript 引擎",
    "Frameworks": "8. 界面框架",
    "Client": "9. 缓存、离线与本地优先",
    "Perf": "10. Web 性能",
    "Security": "11. 安全模型",
    "Access": "12. 无障碍与移动端",
    "Browser": "13. 我们的玩具浏览器",
    "Frontier": "14. 前沿：布局、引擎与证明",
    "Outro": "回顾、习题，以及它们会在哪里再出现",
}

ZH = {
    # ------------------------------------------------------------------ s01_hook
    "Type an address into a browser and press enter. In a few":
        "在浏览器里输入一个网址，按下回车。几百毫秒之后，一个页面出现了。<bookmark mark='a'/>从按下按键到像素出现，这个系列搭建过的几乎所有东西都要轮番上场。名字由第36部分的域名系统解析。"
        "接着建立一条 TCP 连接，再通过一次 TLS 握手，用第30部分的公钥密码学协商出密钥。<bookmark mark='b'/>请求发出去，"
        "HTML 的头几个字节经由第37部分的传输协议传回来。<bookmark mark='c'/>然后，浏览器自己的工作开始了。它一边接收 HTML 一边解析，发现样式表和脚本，并行地获取它们，计算每个元素的样式，"
        "对页面进行布局，再把它绘制出来。<bookmark mark='d'/>最后这一段，从字节到像素，就是这一部分的主题：浏览器拿到一个页面之后，要对它做些什么。",
    "A browser is several machines in one program. <bookmark":
        "浏览器是装在一个程序里的好几台机器。<bookmark mark='a'/>它是一个从不拒绝输入的解析器：任何字节序列，不管多么残破，都会变成一棵文档树。<bookmark mark='b'/>它是一个约束求解器，"
        "把盒子、一行行文字和空白空间拼合在一起。它是一个图形合成器，每秒60次或120次，在 GPU 上移动和混合图层。<bookmark mark='c'/>它是一个即时编译器，让不受信任的代码跑得飞快；它也是一个操作系统，"
        "把这些代码关在沙箱里。<bookmark mark='d'/>而把这一切维系在一起的，是一个事件循环，它有一个截止时间：每秒60帧时，下一帧的所有工作都必须挤进16.7毫秒。",
    'f"We will build each stage, small enough to read,':
        "我们会把每个阶段都搭建出来，小到足以通读，最后把它们一起运行，组成一个玩具浏览器。<bookmark mark='a'/>这是它的输出："
        "这个系列自己的 README 的开头。<bookmark mark='b'/>Markdown 变成 HTML；一个分词器和一个树构建器把 HTML 变成一棵有{b['nodes']}个节点的树；层叠给每个元素一个样式；"
        "布局把文字断成行，再把块堆叠起来；最后，一个绘制器用真实的字体，把文字画成真实的像素。<bookmark mark='c'/>真正的浏览器有的东西，它几乎都没有。但每一个部件都做着真实部件所做的事，"
        "它展示了这个问题的形状。",
    "This is Part 42 of Computer Science, Built, the third part":
        "这是计算机科学，从零搭建，第42部分，也是第八幕的第三部分。<bookmark mark='a'/>我们会看到：为什么 HTML 是用状态机而不是用文法来解析的；层叠如何决定哪条样式胜出；页面如何布局，"
        "一直深入到把一个段落断成行的动态规划；事件循环如何把一切调度进一帧一帧里；JavaScript 引擎做了什么，让动态代码跑得快；以及框架、缓存、安全模型和无障碍，如何全都建立在这一切之上。",
    # ------------------------------------------------------------------ s02_history
    "Chapter one. Thirty years of the web.":
        "第一章：Web 的三十年。",
    "In March 1989 Tim Berners-Lee, at CERN, proposed keeping":
        "1989年3月，CERN 的蒂姆·伯纳斯-李（Tim Berners-Lee）提议，把实验室的信息作为相互链接的文档来管理。他的上司在封面上写道：含糊，但令人兴奋。<bookmark mark='a'/>到1990年底，"
        "他已经做出了至今仍垫在每个页面底下的三件东西：任何文档都有一个名字，后来成了 URL；一个获取文档的协议，HTTP；还有一种带链接的格式，"
        "HTML。<bookmark mark='b'/>他在一台 NeXT 计算机上写出了第一个浏览器，名叫 WorldWideWeb，还写出了第一个服务器。<bookmark mark='c'/>1991年8月，"
        "他向全世界宣布了这个项目。",
    "The web spread when it became pleasant to look at. <bookmark":
        "Web 变得赏心悦目之后，就传播开了。<bookmark mark='a'/>1993年，美国国家超级计算应用中心的马克·安德森（Marc Andreessen）和 Eric Bina 发布了 Mosaic，"
        "它的图像标签把图片放进了页面本身，夹在文字之间。<bookmark mark='b'/>同年4月，CERN 把 Web 的软件放进了公有领域。<bookmark mark='c'/>1994年，"
        "安德森参与创办了 Netscape，它的 Navigator 很快占据了统治地位；伯纳斯-李则创立了万维网联盟，也就是 W3C，来编写标准。",
    "Two more languages joined HTML. <bookmark mark='a'/> In":
        "又有两门语言加入了 HTML。<bookmark mark='a'/>1994年10月，Håkon Wium Lie 提出了层叠样式表，让页面的外观可以和它的内容分开来写。"
        "CSS 第一级在1996年12月成为 W3C 推荐标准。<bookmark mark='b'/>1995年5月，在 Netscape，布兰登·艾克（Brendan Eich）"
        "用大约10天写出了第一个 JavaScript。它在1997年以 ECMAScript 的名字标准化，它的一些仓促决定至今还跟着我们。<bookmark mark='c'/>微软的回应是 Internet Explore"
        "r，与 Windows 捆绑在一起。在浏览器大战中，双方各自发明自己的标签；到2000年代初，Internet Explorer 占据了大部分市场，它的开发也随之放缓。",
    "The next leap came from a feature that almost nobody":
        "下一次飞跃，来自一个几乎没人注意到的功能。<bookmark mark='a'/>经典的页面每点击一次，就向服务器要一整个新页面。<bookmark mark='b'/>1999年，"
        "Internet Explorer 5 带来了一个对象，让脚本不离开页面就能获取数据，其他浏览器以 XMLHttpRequest 的名字照搬了它。现在，页面可以待在原地，"
        "在后台获取一小块一小块的数据。<bookmark mark='c'/>2004年的 Gmail 和2005年的 Google Maps 展示了这带来的可能；2005年2月，"
        "Jesse James Garrett 把这种技术命名为 Ajax，意思是异步 JavaScript 和 XML。",
    "Competition came back. <bookmark mark='a'/> Apple released":
        "竞争又回来了。<bookmark mark='a'/>苹果在2003年发布了基于 WebKit 引擎的 Safari，Mozilla 在2004年11月发布了 Firefox 1.0。<bookmark mark='b'"
        "/>2008年9月，谷歌发布了 Chrome，带来了两个想法。它的引擎 V8 把 JavaScript 编译成机器码，也就是第15部分的即时编译，并掀起了一场竞赛，"
        "让 JavaScript 快了许多倍。<bookmark mark='c'/>另外，过去的浏览器把所有页面放在一个进程里运行，一个坏页面就能把它们全部拖垮；Chrome 则大致上给每个标签页一个自己的进程："
        "这就是第31部分的隔离。",
    "The standards, meanwhile, had stalled. <bookmark mark='a'/>":
        "与此同时，标准停滞了。<bookmark mark='a'/>整个九十年代，W3C 发布了一个个带编号的 HTML 版本，然后是 XHTML；它作为 XML 提供时，一个错误就是致命的，"
        "可真实的页面满是错误。<bookmark mark='b'/>2004年6月，来自苹果、Mozilla 和 Opera 的人创立了 WHATWG，按照浏览器真正使用 HTML 的方式来扩展它。"
        "他们的 HTML5 第一次准确规定了如何解析任何页面，无论它合法与否；W3C 在2014年发布了它。<bookmark mark='c'/>2019年5月，两个组织在同一个 HTML 上达成一致："
        "WHATWG 的活标准（living standard），持续编辑，没有版本号。接下来要讲的，就是它的解析器。",
    # ------------------------------------------------------------------ s03_parsing
    "Chapter two. Parsing HTML.":
        "第二章：解析 HTML。",
    "An HTML parser has two stages. The first, the tokenizer, is":
        "HTML 解析器分两个阶段。第一个阶段是分词器（tokenizer），它是一个有限自动机，就像第12部分里的那些，一次读一个字符。<bookmark mark='a'/>这里它读入一个带 class 的段落、一个词，"
        "以及一个从未闭合的粗体词。在数据状态下，字符就是文本。一个小于号把它带到标签打开状态，一个字母带到标签名状态，一个空格带到属性，一个等号带到属性值，而每个大于号都让它回到数据状态，并发出一个记号（token）"
        "。<bookmark mark='b'/>出来的是5个记号。<bookmark mark='c'/>这里没有什么会失败：意外的字符也有一条转移，由标准写明；标准的分词器大约有80个状态。",
    "The second stage, the tree builder, keeps a stack of open":
        "第二个阶段是树构建器，它维护一个开放元素栈，也就是第12部分为了处理嵌套而给自动机加上的那种存储。<bookmark mark='a'/>一个开始标签创建一个元素，把它挂到栈顶元素下面，再把它压入栈；"
        "文本则挂到栈顶元素下面。<bookmark mark='b'/>接着，段落的结束标签到来了，而粗体还开着。文法会在这里拒绝输入。树构建器则把粗体也弹出，替作者把它闭合，"
        "然后再闭合段落。<bookmark mark='c'/>剩下的就是 DOM，文档对象模型：一棵由节点对象组成的树，脚本读取和修改它，这一部分其余的一切也都以它为基础。",
    "Most of the tree builder's rules close elements the author":
        "树构建器的大多数规则，是替作者闭合那些没有关上的元素。<bookmark mark='a'/>段落里不能包含段落，所以一个 p 开始标签会闭合已打开的 p，"
        "两者成为兄弟。<bookmark mark='b'/>一个列表项会闭合前一个列表项，列表的结束会闭合最后一个。<bookmark mark='c'/>一个结束标签会闭合栈上位于它的匹配元素之上的一切："
        "表格的结束同时结束了单元格和行。真正的浏览器还会在这里插入一个表格主体元素，我们简化过的解析器省掉了它。所有这些规则，标准都写了下来。",
    "Misnested tags are harder. <bookmark mark='a'/> Here bold":
        "错误嵌套的标签更难对付。<bookmark mark='a'/>这里先打开粗体，再打开斜体，但粗体先闭合。我们的树构建器把斜体连同粗体一起闭合，然后打开一个新的斜体元素，于是最后几个词仍是斜体，正如作者的本意："
        "这是标准里收养代理算法（adoption agency algorithm）的一个简化情形。<bookmark mark='b'/>一个没有东西可匹配的结束标签，比如这个多余的 span，"
        "会被忽略。<bookmark mark='c'/>而一个并不开始标签的小于号，是一个有明确结果的解析错误：它就是文本。每一个输入都会得到一棵树，而每一个遵循标准的浏览器都会得到同一棵。",
    "So why not write a grammar for HTML, and use the parsers of":
        "那么，为什么不给 HTML 写一个文法，再用第12和第13部分的解析器呢？<bookmark mark='a'/>由文法构建的解析器也会回答是或否：语言之外的输入就是语法错误，编译器会停下来。浏览器不能停。"
        "真实的页面满是错误，而读者会怪罪那个什么都不显示的浏览器。<bookmark mark='b'/>所以，标准用解析算法来定义 HTML：一个大约80个状态的分词器，加上一个树构建器，"
        "它的每一步都取决于它的栈和一个插入模式，比如 in body 或 in table。<bookmark mark='c'/>输入也不是固定的。一个在解析途中运行的脚本可以调用 document.write，"
        "在它自己后面紧接着插入新的字符，所以解析器必须暂停，运行脚本，然后接着来。",
    # ------------------------------------------------------------------ s04_css
    "Chapter three. The cascade.":
        "第三章：层叠。",
    "When rules disagree about a property, the cascade decides":
        "当多条规则对同一个属性意见不一时，由层叠决定哪一条胜出，它最有名的工具是优先级（specificity）。<bookmark mark='a'/>一个选择器的优先级是三个计数：它的 id 数、类数和标签名数。"
        "这里有10个选择器，从弱到强排列。<bookmark mark='b'/>这些计数像字典里的词那样比较：先比 id，id 打平才比类，最后比标签。"
        "所以一个 id 胜过任意多个类。<bookmark mark='c'/>当两个选择器完全打平时，比如 p.lead 和 .note p，后出现的规则胜出。",
    "Specificity is only part of the cascade's sort key.":
        "优先级只是层叠排序键的一部分。<bookmark mark='a'/>排在最前面的是来源和重要性：浏览器的默认样式，然后是用户的样式表，然后是作者的样式表；而 !important 声明的次序反过来，"
        "所以用户的 !important 偏好胜过页面。<bookmark mark='b'/>然后是优先级，style 属性胜过所有选择器。<bookmark mark='c'/>然后是出现的顺序。<bookmark mark"
        "='d'/>按这个键给所有匹配的声明排序，最后一个胜出。层叠层（cascade layers）从2022年起进入浏览器，它增加了一步，但没有带来新的思想。",
    "Now a small page with four rules. <bookmark mark='a'/> Four":
        "现在来看一个有4条规则的小页面。<bookmark mark='a'/>有4个选择器匹配 class 为 lead 的段落。先按优先级、再按顺序排序，其中3个设置了它的颜色，而最后那个，带 id 的那个，"
        "胜出。<bookmark mark='b'/>所以这个段落是绿色的，它还从 p.lead 那里得到了18像素的字号。<bookmark mark='c'/>里面的粗体元素不匹配任何规则，但颜色和字号是继承的："
        "一个元素自己没有值时，就取父元素的值，所以粗体词也是绿色的。<bookmark mark='d'/>那个普通段落只匹配 p，是灰色的。",
    "The DOM says what the page contains, <bookmark mark='a'/>":
        "DOM 说明页面包含什么，<bookmark mark='a'/>而解析后的样式表构成 CSS 对象模型，也就是 CSSOM。<bookmark mark='b'/>把两者相互匹配，就给了每个元素它的计算样式，"
        "结果就是渲染树，Chrome 现在称之为布局树：每个要被绘制的元素都在其中有一项。<bookmark mark='c'/>display 为 none 的元素没有对应的项，而像 ::before 这样的伪元素，"
        "却有一项 DOM 里所没有的。布局就在这棵树上进行。",
    'f"Matching rules to elements is the expensive part':
        "把规则和元素匹配起来，是样式计算中代价高的部分，而浏览器是倒着做的。<bookmark mark='a'/>要用 div.nav a 去测试一个链接，就从右边开始：这个元素是 a 吗？是。然后沿着它的祖先往上走，"
        "找一个 class 为 nav 的，再往上，找一个 div。<bookmark mark='b'/>大多数元素在第一项测试就失败了。从左到右的话，就要从每一个 div 出发，"
        "搜索它下面的所有东西。<bookmark mark='c'/>在一个有2000个元素、平均深度约为{m['mean_depth']:.0f}的合成页面上，"
        "我们的10个选择器从右到左大约要做{pg['right_to_left'] / 1000:.0f}千次元素测试，而从左到右要做{pg['left_to_right'] / 1000:.0f}千次。<bookmark ma"
        "rk='d'/>在这个系列那份很浅的 README 上，两者差不多，从左到右甚至还稍微便宜一点：造成差别的是深度。",
    'f"Most of those tests are never made, thanks to':
        "这些测试大多数根本不会进行，这要归功于第17部分的哈希表。<bookmark mark='a'/>每条规则都按它的选择器最右边的部分归档：它的 id；没有 id 就用一个类；"
        "再没有就用它的标签。<bookmark mark='b'/>要给一个 class 为 lead 的段落计算样式，只需查找 p、lead 和通配选择器这几个桶：这{WORDS[len(sels)]}条规则中，"
        "只尝试其中{WORDS[tried]}条，其余{WORDS[len(sels) - tried]}条根本不会被看一眼。<bookmark mark='c'/>引擎还维护一个第20部分的布隆过滤器，记录祖先的 id、"
        "类和标签，所以一个需要 class 为 nav 的祖先的选择器，常常立刻就被排除。",
    # ------------------------------------------------------------------ s05_layout
    "Chapter four. Layout.":
        "第四章：布局。",
    "Layout gives every element a box: where it goes, and how big":
        "布局给每个元素一个盒子：它放在哪里，有多大。<bookmark mark='a'/>一个盒子由内容、内边距、边框，以及让邻居保持距离的外边距组成。<bookmark mark='b'/>在常规流中，块沿着页面向下堆叠，"
        "每个块都和它的容器一样宽：宽度沿着树向下传递，高度再向上返回。<bookmark mark='c'/>在一个块内部，行内盒沿着一行排列，排不下就折到下一个行盒里。",
    "Flexbox shares out space. <bookmark mark='a'/> Three items":
        "弹性盒布局（Flexbox）负责分配空间。<bookmark mark='a'/>3个项目，基准尺寸分别是120、200和160像素，增长因子分别是1、2和0，"
        "正好填满480像素。<bookmark mark='b'/>在720像素时，有240像素空余：第一个分得一份，第二个分得两份，第三个没有。<bookmark mark='c'/>在880像素时，"
        "400像素按同样的方式分配。<bookmark mark='d'/>在360像素时，缺了120像素，按收缩因子乘以基准尺寸的比例扣除，所以最宽的那个让出的最多。<bookmark mark='e'/>在300像素时，"
        "每个都缩小八分之三。<bookmark mark='f'/>碰到尺寸限制的项目被冻结，其余的再重新分配。",
    "Grid is the two-dimensional version. <bookmark mark='a'/>":
        "网格布局（Grid）是它的二维版本。<bookmark mark='a'/>列和行都是轨道，项目跨越它们之间的网格线。<bookmark mark='b'/>一条轨道可以是固定的，也可以是剩余空间的一份：在800像素里，"
        "固定的200像素留下600像素，所以一份就是200像素。<bookmark mark='c'/>行和列是一起确定尺寸的，所以项目在两个方向上都能对齐。",
    "How should a paragraph break into lines? <bookmark":
        "一个段落应该怎样断成行？<bookmark mark='a'/>贪心规则是浏览器传统上使用的方法：只要放得下，就把每个词放在当前行上。这是《傲慢与偏见》里达西的信，宽度为360像素；"
        "红条显示每一行的欠缺量。<bookmark mark='b'/>1981年，高德纳（Knuth）和 Plass 为 TeX 一次性选定所有断点，"
        "使各行欠缺量的立方和最小。<bookmark mark='c'/>两种方法都用了17行，其中有3行不同。贪心最差的一行差了77.8像素，而另一种是54.8像素；劣度（badness）"
        "从2.4降到1.86。<bookmark mark='d'/>在这部小说的300个段落中，整体最优（total fit）在284个上胜出。",
    "Knuth and Plass saw this as a graph. <bookmark mark='a'/>":
        "高德纳和 Plass 把这看成一个图。<bookmark mark='a'/>在这部小说开头一句的每两个词之间放一个节点；只要两个节点之间的词能放进190像素宽的一行，就连一条边：一共87条边，"
        "每条边以它那一行的劣度为权重。<bookmark mark='b'/>最好的段落，就是从第一个节点到最后一个节点的最便宜路径，用第19部分的动态规划求出：到每个节点的最优代价，由它之前各节点的最优代价得出。"
        "它的总代价是5.41。<bookmark mark='c'/>贪心把那个 a 挤到第二行，结果留下一个短得多的第三行：8.53。局部最优，在全局上反而更差。",
    "Laying out the whole page on every change would waste the":
        "每次改动都把整个页面重新布局，会浪费这一帧的时间。<bookmark mark='a'/>所以引擎会保留脏位：一次编辑标记它的盒子，"
        "一个表示“有子节点需要布局”的位会一路爬到根。<bookmark mark='b'/>布局只沿着被标记的路径走。在我们玩具浏览器的 README 里编辑一个段落，会重新断开它的22个词，并移动它下面的11个块；"
        "786个词中其余的都不受影响。<bookmark mark='c'/>问题在于：从脚本里读取一个尺寸，会立刻强制执行待处理的布局，所以交替地读和写，会让页面一遍又一遍地重新布局。",
    # ------------------------------------------------------------------ s06_rendering
    "Chapter five. Paint, layers and the frame.":
        "第五章：绘制、图层与帧。",
    "With every box placed, the browser still has to make pixels,":
        "每个盒子都摆好之后，浏览器还得生成像素，它用一条流水线来完成。<bookmark mark='a'/>样式计算每个元素的属性。布局摆放盒子。绘制遍历盒子树，记录下要画什么。合成把结果组合成一帧。"
        "<bookmark mark='b'/>绘制并不直接设置像素。它产生一个显示列表，也就是按 CSS 规定的次序排列的绘图命令：先是背景和边框，然后是文字，再按层叠次序画定位元素。"
        "<bookmark mark='c'/>把这个列表变成像素，分成图块、通常在图形处理器上完成，这叫光栅化，是第51部分的主题。",
    "Browsers do not repaint the whole page for every change.":
        "浏览器不会为每一次改动都重绘整个页面。<bookmark mark='a'/>它们把页面分成图层：这里是页面本身、一个在页面滚动时保持不动的页眉，以及一张正在做动画的卡片。每个图层只光栅化一次，变成一张纹理，"
        "合成器在图形处理器上把这些纹理叠起来。<bookmark mark='b'/>给 width 这样的属性做动画，每一帧都要经过样式、布局、绘制和合成。改成给 transform 或 opacity 做动画，"
        "盒子就什么都没变：合成器只是移动或淡化一张纹理。<bookmark mark='c'/>合成器运行在自己的线程上，所以即使脚本正忙，这样的动画也会继续运行。<bookmark mark='d'/>不过图层不是免费的："
        "每个图层都是内存里的一张纹理，一个要求太多图层的页面会把内存用光。",
    "All of this has a deadline. <bookmark mark='a'/> A sixty":
        "这一切都有一个截止时间。<bookmark mark='a'/>60赫兹的显示器每16.7毫秒显示一帧新画面；在120赫兹的屏幕上，是每8.3毫秒一帧。<bookmark mark='b'/>一帧里的所有事情，"
        "脚本、样式、布局和绘制，都必须装进这个时间窗口。在我们的模拟器里，一帧的渲染步骤要花4毫秒，留给其他一切的大约是12.5毫秒。<bookmark mark='c'/>为了和显示器同步地做动画，"
        "页面会请求 requestAnimationFrame。它的回调只运行一次，就在下一帧的样式和布局之前，并且会收到那一帧的时间。而设为16毫秒的定时器，则会相对显示器逐渐漂移；另外，浏览器会在后台标签页里暂停动画帧。",
    "Here is our event-loop simulator running an animation: every":
        "这是我们的事件循环模拟器在运行一段动画：每一帧，先是一个3毫秒的 requestAnimationFrame 回调，然后是样式、布局和绘制。<bookmark mark='a'/>在第40毫秒，来了一次点击，"
        "它的处理程序在一个任务里做了120毫秒的工作。<bookmark mark='b'/>任务会一直运行到完成，渲染不能在任务中间发生。所以在一串间隔16.7毫秒的帧之后，出现了一个126.7毫秒的空档：丢了7帧，"
        "动画明显卡了一下。这种卡顿就叫 jank。<bookmark mark='c'/>现在把同样的工作拆成每块8毫秒，每一块用延迟为零的 setTimeout 来安排下一块。在两块之间，循环就有机会进行渲染。"
        "<bookmark mark='d'/>没有一帧被丢掉，尽管有些帧晚到了几毫秒。<bookmark mark='e'/>代价是吞吐量：工作在第196毫秒才完成，而不是第160毫秒。"
        "<bookmark mark='f'/>浏览器把任何超过50毫秒的任务标记为长任务，在长任务期间的一次点击也得等着。",
    # ------------------------------------------------------------------ s07_loop
    "Chapter six. The event loop.":
        "第六章：事件循环。",
    "A web page's JavaScript runs on one thread, driven by a loop":
        "网页的 JavaScript 在一个线程上运行，由一个循环驱动，HTML 标准一步一步地写出了这个循环。<bookmark mark='a'/>从一个任务队列里取出一个任务：一个定时器、一次点击、一个网络回复。"
        "把它运行到完成；没有什么能打断它。<bookmark mark='b'/>然后清空微任务队列，也就是 promise 的反应回调，要彻底清空，包括清空过程中新排进来的微任务。<bookmark mark='c'/>然后，"
        "如果该出一帧了，就运行渲染步骤：动画帧回调、样式、布局和绘制。<bookmark mark='d'/>然后再转一圈。Web 上关于次序的一切，都由这四步推出。",
    "Watch the loop run four lines. <bookmark mark='a'/> The":
        "看这个循环运行四行代码。<bookmark mark='a'/>脚本本身是第一个任务，它被放上调用栈。它输出 A。<bookmark mark='b'/>setTimeout，即使延迟为零，也是把一个回调放进任务队列，"
        "要在之后的某个任务里运行。<bookmark mark='c'/>promise 的 then 把它的回调放进微任务队列。<bookmark mark='d'/>脚本输出 D，然后结束；栈空了。"
        "<bookmark mark='e'/>在任何其他任务之前，微任务先被清空：C。<bookmark mark='f'/>直到这时，循环才取下一个任务，B 最后输出。A、D、C、B：我们的解释器根据处理模型算出了这个次序，"
        "而每个浏览器都同意。",
    "The same four steps settle harder cases, and our interpreter":
        "同样的四步也能解决更难的情形，我们的解释器把每一个都算了出来。<bookmark mark='a'/>这里有两个定时器，还有一个 promise，它的反应回调又排进了另一个。同步的输出先出现，"
        "然后是两个 promise 反应，因为清空过程中排进来的微任务，仍然在同一次清空里运行。然后是第一个定时器，它自己的微任务在第二个定时器之前运行。<bookmark mark='b'/>async 函数会同步地运行，"
        "直到它的第一个 await。它的其余部分变成一个微任务，排在下面那个 promise 之前，所以 f 在 then 之前恢复。<bookmark mark='c'/>最后，一个定时器对上一个动画帧。在我们的模型里，"
        "下一帧还有16.7毫秒，所以定时器先运行；在真实的浏览器里，这两者可能以任意次序出现，代码永远不应该依赖它。",
    "Run to completion is a strong guarantee. <bookmark":
        "运行到完成是一个很强的保证。<bookmark mark='a'/>永远不会有两段脚本同时运行，所以 JavaScript 的堆不可能出现第33部分的数据竞争：从来不需要锁。"
        "promise 和 async 函数是没有线程的并发，是循环稍后再恢复的续延。<bookmark mark='b'/>但是每一个 await 都会结束一段。快速点击两次，每次都去查询库存，每次都得知还剩一件，"
        "每次都下了一个订单：这是一个逻辑上的竞争，而根本没有线程。<bookmark mark='c'/>这个保证也有反面。一段永不结束的代码会阻塞它后面的一切，包括渲染和输入，这就是上一章那个冻住的页面。",
    "For work that really is long, a page can use more than one":
        "对于真正很长的工作，页面可以使用不止一个核心。<bookmark mark='a'/>Web Worker 是第二个线程，有它自己的事件循环和自己的堆，并且不能访问页面。"
        "<bookmark mark='b'/>两者什么都不共享；它们通过发送消息来交谈，消息以任务的形式到达。主线程发送文本，worker 统计词数，计数再传回来，而动画一直保持着它的帧。"
        "<bookmark mark='c'/>消息会被复制，或者它的缓冲区被转移，发送方手里就什么都不剩了。也有带原子操作的共享内存，但只给那些与其他源（origin）隔离的页面使用，而它又把数据竞争带了回来。",
    # ------------------------------------------------------------------ s08_engines
    "Chapter seven. JavaScript engines.":
        "第七章：JavaScript 引擎。",
    "A page arrives with its JavaScript as text, often far more":
        "一个页面带着它的 JavaScript 文本到来，往往远远超过这次访问会运行的量。<bookmark mark='a'/>所以引擎会预解析每个函数体：一次快速扫描，检查语法，并记下函数用到了哪些外层变量，以便处理闭包，"
        "但不建树。<bookmark mark='b'/>当 init 被调用时，它被完整地解析并编译；init 调用 render 时，render 也一样。结账和退款的处理程序则一直保持为文本，直到有人点击。",
    "Then comes the pipeline Part 15 measured. <bookmark":
        "接下来是第15部分测量过的那条流水线。<bookmark mark='a'/>字节码立刻在解释器里运行，解释器记下它看到的东西：到达每个运算的类型，到达每次属性访问的形状。"
        "<bookmark mark='b'/>热的函数向上走，先到基线编译器，再到优化编译器，后者利用这些反馈把代码特化，如果它的猜测失败，还有一条退回去的路。"
        "<bookmark mark='c'/>V8 的各层是 Ignition、Sparkplug、Maglev 和 TurboFan；Firefox 和 Safari 也在爬一架类似的梯子。",
    "How can a property be found quickly, when any object can":
        "既然任何对象随时都可能增加属性，怎样才能快速找到一个属性呢？<bookmark mark='a'/>每个对象都指向一个隐藏类，也就是一个形状：一张表，记着哪个属性住在哪个槽里。增加一个属性，"
        "就沿着一条共享的转换走到一个新形状。<bookmark mark='b'/>a 先得到 x，再得到 y。b 也一样，落在完全相同的形状上。<bookmark mark='c'/>c 先加 y，最后落在另一个形状上。"
        "<bookmark mark='d'/>第15部分直接问过 V8，它也同意：次序相同，形状就相同。",
    "A shape lets the engine skip the table. <bookmark mark='a'/>":
        "有了形状，引擎就可以跳过查表。<bookmark mark='a'/>代码里的每一处访问，比如这里的 p.x，都保留一个小缓存：它见过的形状，以及 x 在哪里。"
        "<bookmark mark='b'/>我们在一万个对象上对 p.x 求和。如果它们都用同一种方式构建，这个访问点就是单态的：每次访问一次形状检查。<bookmark mark='c'/>如果有两种或四种属性次序，"
        "它就是多态的，依次尝试最多四个缓存的形状，每次访问2.5次检查。<bookmark mark='d'/>有八种时，缓存溢出，访问点变成超多态：一万次访问，每一次都要查字典。",
    "The optimizer also bets on types. <bookmark mark='a'/> add":
        "优化器还会对类型下注。<bookmark mark='a'/>add 被用小整数调用了三次，所以它被编译成一条机器加法，由检查守护着，确认两个参数真的都是小整数。"
        "<bookmark mark='b'/>第5次调用传入了一个字符串。守卫失败，引擎去优化：重建解释器的栈帧，并在那里接着运行。<bookmark mark='c'/>在第8次调用时，add 被重新编译，"
        "适用于整数或字符串。<bookmark mark='d'/>第9次调用让一个小整数溢出：又一次去优化，到第12次调用时，得到一个足够宽、能容纳这三种情况的版本。反馈只会变宽，所以函数最终会稳定下来。",
    "And all those objects need collecting, with Part 15's":
        "而所有这些对象都需要回收，用的是第15部分的回收器。<bookmark mark='a'/>新对象填满一个小小的新生代的一半。<bookmark mark='b'/>大多数对象死得早："
        "一次清扫（scavenge）把少数幸存者复制到另一半，所以它的代价取决于活着的对象，而不是垃圾。<bookmark mark='c'/>存活过两次的对象被移到老年代。"
        "<bookmark mark='d'/>老年代很少回收，用的是标记—整理，标记在辅助线程上并发进行，所以 JavaScript 只会看到短暂的停顿，而且这些停顿常常被安排在帧与帧之间的空闲时间里。",
    # ------------------------------------------------------------------ s09_frameworks
    "Chapter eight. User interface frameworks.":
        "第八章：界面框架。",
    "Keeping every element in step with the program's state by":
        "手工让每个元素和程序的状态保持一致，正是界面 bug 的藏身之处。2013年发布的 React 做出了一个不同的承诺。<bookmark mark='a'/>把页面描述成状态的一个函数；状态变了，就再调用一次，"
        "得到一棵由普通对象组成的新树，也就是虚拟 DOM。<bookmark mark='b'/>把它和上一棵树比较。这里有一行的文字不同。<bookmark mark='c'/>结果是一个补丁，一次文字修改，"
        "只有它会碰到真实的 DOM，而在那里，每次改动都可能意味着重新做一遍样式、布局和绘制。",
    "How should two trees be compared? <bookmark mark='a'/>":
        "两棵树应该怎么比较？<bookmark mark='a'/>精确的做法是树编辑距离：把一棵树变成另一棵所需的最少的插入、删除和重新标记。Zhang 和 Shasha 在1989年提出的算法是动态规划，就像第19部分那样，"
        "而通用算法至今仍大约是立方级的。<bookmark mark='b'/>在只改了一行的列表上，我们的实现在120行时要花300毫秒。<bookmark mark='c'/>React 则使用两条规则："
        "类型不同的元素替换它的整棵子树，子元素按 key 或按位置匹配。这是线性的，这里只要三分之一毫秒，而且它找到的也是同一处修改。",
    "Lists need help. Here are four rows, and the user has ticked":
        "列表需要帮助。这里有四行，用户勾选了 b。<bookmark mark='a'/>在顶部加一行。按位置匹配时，旧行和新行按次序配对：每一行的文字都被重写，末尾出现一个新元素，而那个勾选，因为它存在元素里，"
        "现在跑到了 a 旁边。<bookmark mark='b'/>给每一行一个 key，一个稳定的身份：顶部一个新元素，其他的都不动，勾选也留在 b 那里。<bookmark mark='c'/>在100行上，"
        "在开头插入一行，按 key 只碰3个节点，按位置要碰103个，而且有100行最后带着别的行的状态。",
    "Keys say which rows survive, not how to move them. <bookmark":
        "key 说明的是哪些行留下，而不是怎样移动它们。<bookmark mark='a'/>把六行中的第一行和最后一行对调。React 按新的次序走一遍，记住到目前为止放置过的最靠后的旧位置。5号行排在最前面，"
        "所以之后的每一行，因为来自更左边，都要移动：移动5次。<bookmark mark='b'/>最少的移动是保留已经按递增次序排列的最长一段，也就是1到4号，只移动两行。最长递增子序列是第19部分的经典问题，"
        "Inferno 和 Vue 3 用的就是它。<bookmark mark='c'/>在100行上，反转无论用哪种方式都需要99次移动，但对调两行，React 的那一遍要花99次，而另一种只要2次：这是一个实实在在的弱点，"
        "不过实践中很少碰到。",
    "Another family of frameworks skips the virtual tree.":
        "另一类框架干脆跳过虚拟树。<bookmark mark='a'/>状态存在信号里：名、姓、一个计数。计算值读取它们，页眉又读取这些计算值；每次读取都记下一条边，所以框架知道这张图。"
        "<bookmark mark='b'/>把计数设为3：只有徽标和页眉重新运行。<bookmark mark='c'/>设置姓：全名、问候语和页眉重新运行，而徽标不会。"
        "<bookmark mark='d'/>这就是第41部分的构建图，每次写入都重新计算，并且带着它的提前截止：一个算出来没有变化的值，会让这一波停下。SolidJS 就是这样工作的，"
        "现在 Svelte、Vue、Preact 和 Angular 也是。",
    # ------------------------------------------------------------------ s10_client
    "Chapter nine. Caches, offline, and local-first software.":
        "第九章：缓存、离线与本地优先。",
    "The fastest request is the one never sent. <bookmark":
        "最快的请求，是从来没有发出的那一个。<bookmark mark='a'/>服务器在给出回答时，可以说明这个回答在多长时间内有效：max-age 60，一分钟内是新鲜的。它还会发送一个 ETag，也就是这个版本的名字。"
        "<bookmark mark='b'/>20秒之后，浏览器直接使用它的副本，不问任何人。<bookmark mark='c'/>一分钟之后，副本过期了，但并非没用。浏览器再问一次，带上 ETag。什么都没变，"
        "所以服务器回答304，Not Modified：只有头部，一次往返，但没有正文。",
    "Here one file is requested nine times in seven minutes, and":
        "这里一个文件在7分钟内被请求了9次，并在第300秒时发生了变化。<bookmark mark='a'/>用 max-age 60：先是一次未命中，然后两次新鲜命中，然后是用304回答的重新验证，直到第320秒，"
        "ETag 不再匹配，新的正文传了回来。9次请求里有7次在等网络。<bookmark mark='b'/>加上 stale-while-revalidate，120秒：过期的副本会被立刻送出，并在后台检查。"
        "只有第一次请求需要等待。<bookmark mark='c'/>代价是：在第320秒，用户会看到旧版本，一次。",
    "Build tools avoid that bet altogether. <bookmark mark='a'/>":
        "构建工具干脆完全避开这场赌博。<bookmark mark='a'/>页面每次都要重新验证，但它引用的脚本和样式，文件名里带着其内容的哈希：这是第41部分的内容寻址。"
        "<bookmark mark='b'/>一个名字对应一组字节，所以这些文件被缓存一年，并标记为 immutable，从不检查。<bookmark mark='c'/>改一行代码，构建就会产出一个新名字。页面指向它，"
        "浏览器只取这一个文件，旧的副本就再也不会被用到了。",
    "A service worker is a script the page installs between":
        "service worker 是页面安装在自己和网络之间的一段脚本。<bookmark mark='a'/>页面发出的每一个请求，都先经过这个 worker，它用普通的 JavaScript 来回答。"
        "<bookmark mark='b'/>缓存优先：从缓存回答，只有未命中时才去网络，并保留一份副本。这适合应用自己的文件，也让它在完全没有网络连接时也能打开。<bookmark mark='c'/>网络优先：先试网络，"
        "这样数据是最新的；网络断了，就退回到上一份副本。页面照样工作。",
    "Those copies need somewhere to live. <bookmark mark='a'/>":
        "这些副本需要有个地方存放。<bookmark mark='a'/>缓存存储（Cache Storage）存放响应，供 worker 使用。IndexedDB 是一个小型的事务性对象数据库，带有索引，用来存放应用的数据。"
        "localStorage 按键存放字符串，而且是同步的，所以一次大的读取会阻塞主线程。<bookmark mark='b'/>所有这些都属于同一个源，并且在存储紧张时可能被清除，除非页面申请持久化存储。",
    "Push this further, and the server stops being the home of":
        "再往前推一步，服务器就不再是数据的家了。<bookmark mark='a'/>2019年，Martin Kleppmann 和他的合著者，与研究实验室 Ink and Switch 一起，把它称为本地优先软件："
        "你的数据存在你自己的设备上，立刻打开，离线可用，服务器只是帮助设备同步。<bookmark mark='b'/>两台设备上的一张购物清单，两台都离线。手机加了牛奶；笔记本电脑加了面包，并勾掉了鸡蛋。"
        "<bookmark mark='c'/>重新连上之后，每台设备把自己的操作发给对方。<bookmark mark='d'/>第39部分的一种 CRDT 把它们合并：它的合并满足交换律、结合律和幂等律，"
        "所以无论消息以什么次序到达，两边都得到同一张清单。Automerge 和 Yjs 就是专门为此打造的库。",
    # ------------------------------------------------------------------ s11_perf
    "Chapter ten. Web performance.":
        "第十章：Web 性能。",
    "Before a page can show anything, the browser must fetch and":
        "页面要显示任何东西之前，浏览器必须先取回并处理所有阻塞渲染的资源。这是一个页面的依赖图，时间是示意性的。<bookmark mark='a'/>HTML 最先到达。它指明了一个样式表和一个同步脚本，"
        "样式表又指明了一个字体，所以每次获取都要等提到它的那个文件。<bookmark mark='b'/>首次绘制要等所有这些都完成，而最长的那条链，HTML、CSS、字体，就是关键路径：345毫秒。这就是第41部分的构建图，"
        "只不过边上标的是时间。<bookmark mark='c'/>现在把脚本延迟执行（defer），并在 HTML 里预加载（preload）字体。字体提早100毫秒开始获取，首次绘制提前到245毫秒。"
        "<bookmark mark='d'/>浏览器还会给各次获取排优先级：样式表和字体高，图片低；页面也可以调高最要紧的那一张图片。",
    "In 2020 Google named three Core Web Vitals, measured in real":
        "2020年，Google 提出了三项核心网页指标（Core Web Vitals），在真实用户的浏览器里测量。<bookmark mark='a'/>最大内容绘制（LCP）是最大的图片或文字块被画出来所需的时间；"
        "低于2.5秒算良好。<bookmark mark='b'/>交互到下一次绘制（INP）是从一次点按或按键到下一帧的延迟。2024年3月，它取代了首次输入延迟（FID），后者只计量第一次交互开始之前的等待。"
        "低于200毫秒算良好。<bookmark mark='c'/>累积布局偏移（CLS）衡量你阅读时页面跳动了多少；低于0.1算良好。<bookmark mark='d'/>四次访问中有三次良好，页面就算通过。",
    "Layout shift has its own arithmetic. <bookmark mark='a'/>":
        "布局偏移有它自己的算术。<bookmark mark='a'/>当一个可见元素移动时，这次偏移的得分是它的影响比例，也就是它在移动前后覆盖的视口份额，乘以它的距离比例，也就是它移动了多远。"
        "<bookmark mark='b'/>这是一个页面在最初10秒里的五次偏移。<bookmark mark='c'/>它们被分组成会话窗口，窗口在出现1秒的间隔之后关闭，或者总长满5秒时关闭。我们的偏移形成三个窗口，"
        "分别是0.085、0.125和0.0025。<bookmark mark='d'/>得分取最差的窗口，0.125，属于“需要改进”。常见的元凶是没有宽度和高度的图片，以及迟到的字体和广告。",
    'f"Fewer bytes arrive sooner. <bookmark mark=':
        "字节越少，到得越快。<bookmark mark='a'/>我们测量了这个系列自己的三个文件。每个浏览器都接受的 Gzip，把教学大纲压缩到原来大小的百分之{pct}。Bzip2 和 xz 压得更好，但浏览器不接受它们；"
        "而 Web 较新的编解码器 Brotli 这里没有安装，所以我们没有它的数据。<bookmark mark='b'/>图片通常占了字节的大头。AVIF 和 WebP 在同样画质下更小；"
        "源集（source set）让小屏幕获取小文件；懒加载等到图片快进入视野时才加载；而宽度和高度会为图片预留位置。",
    "Then the connection itself. <bookmark mark='a'/> HTTP one":
        "然后是连接本身。<bookmark mark='a'/>HTTP 1.1 每个连接一次只承载一个请求，所以浏览器会对每个主机开大约六个连接。2015年的 HTTP/2 在单个 TCP 连接上复用许多条流，"
        "以交错的帧来传输。<bookmark mark='b'/>但 TCP 严格按顺序交付字节，所以一旦丢了一个包，每条流都要等它重传：这就是第37部分讲过的队头阻塞。"
        "<bookmark mark='c'/>2022年标准化的 HTTP/3 运行在基于 UDP 的 QUIC 之上，QUIC 只在每条流内部保持顺序。现在一次丢包只会让它所属的那条流停顿；"
        "而且握手把第30部分的 TLS 合并了进来，省掉一次往返。",
    # ------------------------------------------------------------------ s12_security
    "Chapter eleven. The security model.":
        "第十一章：安全模型。",
    "A browser runs code from every site you visit, so its first":
        "浏览器运行着你访问的每个网站的代码，所以它的第一条规则，是关于谁可以读什么。<bookmark mark='a'/>一个源（origin）由三样东西组成：协议、主机和端口。路径不算在内。"
        "<bookmark mark='b'/>两个页面只有在三者都相同时才同源。把 https 改成 http，加一个端口，或者换到一个子域名，它们就是陌生人。"
        "<bookmark mark='c'/>页面可以从任何地方嵌入图片、脚本和框架，也可以向任何地方发送请求，但它的脚本只能读取它自己的源所提供的内容。",
    "Reading across origins needs the server to opt in. <bookmark":
        "跨源读取需要服务器主动同意。<bookmark mark='a'/>浏览器会发出请求，但响应回来时，它会寻找一个写明该页面的源的头部。没有这个头部，脚本就永远看不到响应。"
        "<bookmark mark='b'/>这是一个商店页面发出的六个请求，由我们对这些规则建立的模型来裁决。普通的 GET 总会被发出，但只有服务器允许我们，才能读取。"
        "<bookmark mark='c'/>PUT 或者自定义头部可能做出旧服务器从未预料到的事情，所以浏览器先用一次预检请求征求许可；如果被拒绝，就根本不发送这个请求。而带 cookie 的请求必须按名字明确允许，"
        "不能用通配符。",
    "The commonest attack breaks no rule: it gets the attacker's":
        "最常见的攻击不违反任何规则：它让攻击者的代码从你的源提供出来。<bookmark mark='a'/>一个页面把用户的名字粘贴进 HTML 来问候用户，而有人取了一个本身就是 HTML 的名字。"
        "<bookmark mark='b'/>我们第2章的解析器构建出树，问候语旁边多了一张带错误处理程序的图片。图片加载失败，处理程序以页面的权限运行，cookie 就被送到它想送的任何地方。这就是跨站脚本攻击（XSS）。"
        "<bookmark mark='c'/>把名字转义，让尖括号变成字符引用，同一个解析器就只生成一个文本节点：显示出来，而不是运行。",
    "A Content Security Policy is the second line of defence.":
        "内容安全策略（Content Security Policy）是第二道防线。<bookmark mark='a'/>服务器列出脚本可以来自哪里，这里只有它自己的源，"
        "<bookmark mark='b'/>浏览器则拒绝其他一切：像我们注入的那种内联处理程序，以及来自其他源的脚本。<bookmark mark='c'/>再把会话 cookie 标记为 HttpOnly，"
        "就能把它对脚本完全隐藏起来。",
    "Cookies bring the opposite danger. <bookmark mark='a'/> The":
        "cookie 带来的是相反的危险。<bookmark mark='a'/>浏览器会把一个网站的 cookie 附加到发往该网站的每个请求上，不管请求是谁发起的；所以另一个网站的页面可以向你的银行提交一个隐藏表单，"
        "而银行看到的是你已经登录：这就是跨站请求伪造（CSRF）。<bookmark mark='b'/>SameSite 属性可以阻止它。Lax cookie 只有在你于顶层点击链接时才会跨站；"
        "Strict cookie 从不跨站。<bookmark mark='c'/>从2020年起，Chrome 把没有这个属性的 cookie 当作 Lax。",
    "<bookmark mark='a'/> Browsers split themselves into":
        "<bookmark mark='a'/>浏览器把自己拆成多个进程：一个有特权的浏览器进程，以及运行页面的沙箱化渲染进程，后者不能直接接触文件或网络。<bookmark mark='b'/>2018年，"
        "Spectre 表明，第8部分讲过的推测执行能让脚本通过缓存计时，读取它自己进程里的内存，所以攻击者的框架可以读取旁边的页面。<bookmark mark='c'/>解决办法是站点隔离：每个站点都有自己的渲染进程，"
        "靠硬件的内存保护而不是引擎的检查把它们隔开。",
    "WebAssembly, in every major browser since 2017, brings":
        "WebAssembly 自2017年起进入所有主流浏览器，它把编译型语言带进了同一个沙箱。<bookmark mark='a'/>C、C++ 或 Rust 被编译成紧凑的、带类型的字节码。浏览器在运行前先验证它，"
        "然后像第15部分的 JIT 那样，把它编译成机器码。<bookmark mark='b'/>一个模块只能访问它自己的线性内存，越界的访问会触发陷阱。",
    # ------------------------------------------------------------------ s13_access
    "Chapter twelve. Accessibility and mobile.":
        "第十二章：无障碍与移动端。",
    "A screen reader does not see pixels. <bookmark mark='a'/>":
        "屏幕阅读器看不到像素。<bookmark mark='a'/>浏览器从 DOM 推导出第二棵树，也就是无障碍树，并把它交给操作系统：对于人能感知或操作的每样东西，给出一个角色、一个名称和一个状态。"
        "<bookmark mark='b'/>一个 button 元素成为名为 Buy 的按钮；复选框以它的标签命名，并且处于选中状态；图片以它的 alt 文本命名。"
        "<bookmark mark='c'/>但带点击处理程序的 div 只是通用的文本：没有可按的东西，键盘也到不了它。",
    "Many people use only a keyboard. <bookmark mark='a'/> Tab":
        "许多人只用键盘。<bookmark mark='a'/>Tab 键按 DOM 的顺序移动焦点，而不是按屏幕上的顺序，所以被 CSS 重新排列过的布局会让焦点四处乱跳。"
        "<bookmark mark='b'/>ARIA 属性可以用角色、名称或状态修补无障碍树，但这样一来，按键就得你自己处理了。ARIA 的第一条规则是优先使用原生元素，它免费带来这一切。",
    "Text must also be readable, and the Web Content":
        "文字还必须易读，而 Web 内容无障碍指南（WCAG）把“易读”变成了一个数。<bookmark mark='a'/>sRGB 值是经过伽马编码的，所以先要撤销编码：靠近黑色处是一小段直线，其余部分是2.4次幂。"
        "<bookmark mark='b'/>按每种原色看起来有多亮，给线性通道加权，主要是绿色，就得到相对亮度。<bookmark mark='c'/>对比度是较亮的亮度加0.05，除以较暗的亮度加0.05：颜色相同时是1，"
        "白底黑字是21。<bookmark mark='d'/>我们的蓝色在我们的背景上：0.37对0.0086，对比度是7.1。",
    "Normal text needs four and a half to one for level AA, large":
        "正文文字在 AA 级需要4.5比1，大号文字需要3比1，AAA 级需要7比1。<bookmark mark='a'/>在白色上，能通过 AA 的最浅灰色是十六进制 767676。"
        "<bookmark mark='b'/>在我们的背景上，这个系列调色板里除了一种颜色之外都能通过 AA，有四种能通过 AAA。<bookmark mark='c'/>最深的那种灰色不及格，只有1.84。它应该用来画线条，"
        "而不是写字，可我们自己的时间轴条却用它印年份：这正是这次检查刚刚发现的一个缺陷。",
    "On a phone, the radio's cost depends on its state, not just":
        "在手机上，无线电模块的开销取决于它的状态，而不只是字节数。<bookmark mark='a'/>在 Huang 和同事2012年测量的 LTE 模型里，唤醒无线电大约要四分之一秒，一次传输之后，"
        "它还会在一段高功耗的尾巴里停留大约11.5秒。<bookmark mark='b'/>十个小请求，每隔20秒发一个，就要付这段尾巴十次：在我们的模型里大约130焦耳。"
        "<bookmark mark='c'/>把它们一起发出，只付一次：大约16.5焦耳，少了将近八倍。所以手机会把后台工作攒起来批量处理。",
    "Native apps share the browser's problem. <bookmark":
        "原生应用也有浏览器的这个问题。<bookmark mark='a'/>每个应用都有一个 UI 线程，它处理输入，并且必须在60赫兹下每16.7毫秒交付一帧，就像第5章讲的那样。在这个线程上读一次文件，就会错过一帧。"
        "<bookmark mark='b'/>所以磁盘和网络工作都移到其他线程去做；如果一个应用5秒不响应输入，Android 会提出关闭它。",
    "<bookmark mark='a'/> Each platform has its own toolkit:":
        "<bookmark mark='a'/>每个平台都有自己的工具包：iOS 上是 UIKit 和 SwiftUI，Android 上是 Views 和 Jetpack Compose，较新的那些是声明式的，"
        "就像第8章的框架。<bookmark mark='b'/>跨平台框架共享一份代码库。2015年推出的 React Native 用 JavaScript 驱动平台自己的控件；"
        "<bookmark mark='c'/>Flutter 则自己绘制每一个像素。取舍在于：一份代码库，还是外观和行为与每个平台完全一致。",
    # ------------------------------------------------------------------ s14_browser
    "Chapter thirteen. Our toy browser.":
        "第十三章：我们的玩具浏览器。",
    'f"Here are the stages run on the README, one at a':
        "这是在 README 上运行的各个阶段，一次一个。<bookmark mark='a'/>源文件是 Markdown，有几十行。一个大约50行的转换器把标题、列表、强调和代码变成 HTML。"
        "<bookmark mark='b'/>第二章的词法分析器一次一个字符地读取这段 HTML，产生{p['tokens']}个记号，树构建器再把它们变成一棵文档树：标题、段落、列表，以及其中的文字。"
        "<bookmark mark='c'/>然后是层叠。一个有七条规则的用户代理样式表，给标题设定字号和颜色，给段落和列表项设定外边距，给代码设定它自己的颜色；而继承把字号从列表项带进它里面的粗体文字。",
    'f"Layout walks down the tree. <bookmark mark=':
        "布局沿着树往下走。<bookmark mark='a'/>每个标题、段落和列表项都成为一个块盒，一共{b['boxes']}个，在页面上自上而下堆叠，每个盒子的高度就是它里面各行的高度。"
        "<bookmark mark='b'/>在块内部，行内布局一次放一个词，用它的字体测量每个词，当下一个词会越过右边缘时就另起一行。这就是第四章的贪心断行算法。<bookmark mark='c'/>还有两个细节，"
        "真正的浏览器也必须做对。中文的词会回退到一个包含这些字符的字体。<bookmark mark='d'/>而空格来自源文件：HTML 里粗体词和它后面的冒号之间没有空格，屏幕上也就没有。然后绘制器画出每个词，"
        "右边的页面就是结果。",
    'f"How fast is it? We timed each stage on this':
        "它有多快？我们在这台机器上给每个阶段计时，取五次运行的中位数。<bookmark mark='a'/>转换 Markdown、词法分析和建树，加起来只要几毫秒。层叠大约要{ms['cascade']:.0f}毫秒，"
        "布局大约{ms['layout']:.0f}毫秒。<bookmark mark='b'/>绘制，包括编码图像文件，大约要{ms['paint']:.0f}毫秒。"
        "<bookmark mark='c'/>60赫兹下的一帧是16.7毫秒，而我们的浏览器画一页大约要{total:.0f}毫秒。<bookmark mark='d'/>真正的引擎是编译过的代码，"
        "它们只对变化的部分重新计算样式和布局，并在 GPU 上分块光栅化。所以首次加载可能要花点时间，但之后的每一帧都在预算之内。",
    "And what it leaves out. <bookmark mark='a'/> Our parser has":
        "还有它省略了什么。<bookmark mark='a'/>我们的解析器有十来个状态，以及一条修复错误嵌套格式的规则；标准的词法分析器大约有80个状态，树构建器还有针对表格、表单和脚本的插入模式。"
        "我们的 CSS 认识标签、类、ID 和后代选择器。我们的布局认识块和贪心断行，不认识浮动、表格、flexbox、grid、双向文本或断字。而且它不运行脚本，不获取任何东西，也不需要任何安全措施，因为它信任它唯一的输入。"
        "<bookmark mark='b'/>一个真正的引擎有几千万行代码。如果你想更进一步，"
        "Pavel Panchekha 和 Chris Harrelson 写的开放图书《Web Browser Engineering》用几千行 Python 构建了一个完整得多的浏览器。",
    # ------------------------------------------------------------------ s15_frontier
    "Chapter fourteen, the frontier. Can a browser be fast,":
        "第十四章，前沿。浏览器能不能同时做到快速、正确和安全？",
    'f"Is layout cheap? In normal flow, one pass down':
        "布局便宜吗？在常规流里，沿树向下一遍、再向上一遍就够了，所以代价与页面大小成线性关系。<bookmark mark='a'/>现代布局提出了更难的问题。flex 容器里的 flex 容器，先要问每个子元素它的首选尺寸，"
        "然后再按它实际得到的尺寸重新布局一次。每一层，子元素要布局两次。<bookmark mark='b'/>嵌套20层，如果不加小心，最里面的盒子大约要布局200万次："
        "我们的模型数出来是{rows[-1]['naive']:,}次。<bookmark mark='c'/>用一个以盒子和提供给它的宽度为键的缓存，它只布局{rows[-1]['cached']}次。"
        "真正的引擎恰好保留着这样的缓存，而能击败这些缓存的病态页面仍然时有出现。完整的 CSS 布局模型是否总能有线性算法，以及如何让重新布局的代价与变化成正比，都还是悬而未决的问题。",
    "If layout is a constraint problem, a solver can reason about":
        "如果布局是一个约束问题，求解器就可以对它进行推理。<bookmark mark='a'/>2016年，"
        "Pavel Panchekha 和 Emina Torlak 的 Cassius 把 CSS 布局的规则写成了逻辑公式。<bookmark mark='b'/>把这些公式和一个页面交给求解器，它就能证明某个性质成立，"
        "比如文字永远不会重叠，或者构造出一个让这个性质不成立的页面。同样的编码还可以根据草图合成样式表；它的后继者 VizAssert 能对所有屏幕尺寸一次性检查无障碍和可用性方面的性质。"
        "<bookmark mark='c'/>另一条研究路线把布局看作属性文法，通过可以并行运行的树遍历来计算；Leo Meyerovich 和 Rastislav Bodík 在2010年做了这件事，"
        "而 Mozilla 的 Servo 引擎把这个想法带进了实践，它的并行样式计算自2017年起就已在 Firefox 中发布。",
    "The JavaScript engine is where speed and safety collide.":
        "JavaScript 引擎是速度与安全相撞的地方。<bookmark mark='a'/>它的优化编译器根据类型反馈做出假设，并删除它认为多余的检查。<bookmark mark='b'/>如果其中一个推断是错的，"
        "一个本来需要的边界检查就消失了，任何网页上的脚本都能越过数组末尾去读写，并由此触及它所在进程里的任意内存。这种形态的漏洞，出在引擎的编译器和类型系统里，十年来一直是最值钱的浏览器漏洞利用之一。"
        "<bookmark mark='c'/>在这样的脚本和计算机之间，仍然挡着的是渲染进程周围的沙箱。<bookmark mark='d'/>防御是一层层加上去的：V8 在2024年在它自己的堆里加了一个沙箱，"
        "而模糊测试工具生成数以百万计的 JavaScript 程序，抢先找到这类漏洞。<bookmark mark='e'/>悬而未决的目标是一个 JIT，它的优化被证明是正确的，就像 CompCert 对 C 所做的那样，"
        "同时又快到足以发布。",
    "Security has its own formal frontier. The web's rules are":
        "安全也有它自己的形式化前沿。Web 的规则散落在数百份文档里，而攻击就藏在它们之间的缝隙中。<bookmark mark='a'/>2010年，"
        "Devdatta Akhawe、Adam Barth 和同事把 Web 的参与者和规则，即浏览器、服务器、cookie、重定向，以及一个拥有自己服务器的攻击者，写成了 Alloy 分析器里的一个模型，"
        "它在已经提出的防御上发现了新的攻击。<bookmark mark='b'/>Aaron Bohannon 和 Benjamin Pierce 的 Featherweight Firefox 为浏览器的核心建立了模型。"
        "Daniel Fett、Ralf Küsters 和 Guido Schmitz 的 Web 基础设施模型（Web Infrastructure Model）被用来发现 OAuth 上的攻击，"
        "OAuth 就是“用另一个网站的账号登录”背后的协议；它还被用来证明修复后的版本是安全的。<bookmark mark='c'/>而2023年的 WebSpec 用求解器检查浏览器规则，"
        "发现了针对 cookie 完整性的新攻击。",
    "Open problems. <bookmark mark='a'/> Incremental layout:":
        "开放问题。<bookmark mark='a'/>增量布局：重新布局的代价可以被证明与变化的大小成正比，即使有 flexbox、grid 和固有尺寸。<bookmark mark='b'/>经过验证的引擎："
        "一个优化被证明正确的 JavaScript 编译器，而且快到足以发布。<bookmark mark='c'/>关于整个 Web 的安全证明：一个足够完整的模型，使得关于它的证明能覆盖人们实际使用的浏览器。"
        "<bookmark mark='d'/>还有调度：把页面的工作拆分成任务，使得没有任何输入的等待超过某个上限，并且在工作到来时在线做出决定。"
        "<bookmark mark='e'/>这一部分的研究题要求一个带固有尺寸的 flex 布局算法，其重新布局代价以变化的大小为界，同时给出一个相匹配的下界。",
    # ------------------------------------------------------------------ s16_outro
    "What we built in this part. An HTML parser that turns every":
        "我们在这一部分构建了什么。一个 HTML 解析器，把每一份输入都变成一棵树，因为 Web 的标准规定了遇到每一种错误该怎么办。一个层叠，按来源、按优先级（specificity，"
        "作为三元组按字典序比较）、再按顺序给规则排序，并从右往左匹配选择器。把布局看作空间的分配，把断行看作最短路径，在一部小说几乎每一个段落上都胜过贪心算法。一个事件循环，运行一个任务、清空它的微任务、渲染一帧；"
        "以及一个丢掉七帧的长任务。隐藏类和内联缓存，带键的列表和信号（signal）。还有缓存、源，以及一个从光的物理推导出来的对比度。贯穿其中的是一个想法：浏览器在一个16毫秒的帧之内，尽可能少做工作，尽可能晚做工作。",
    "Where this comes back. Part 43 designs the APIs a web page":
        "这些内容会在哪里再出现。第43部分设计网页调用的 API，并在它们变化时保持兼容。第44部分用对照实验来衡量更快的页面是否会改变人们的行为。第45和第48部分把缓存和内容分发放到全球的规模上。"
        "第51部分打开光栅化器和 GPU。第54和第55部分则追问：要怎样才能信任一个编译器，包括 JavaScript 引擎里的那一个。",
    "In practice. Measure performance on real users' devices,":
        "实践中。在真实用户的设备上测量性能，少发 JavaScript，让每个任务都足够短，使输入永远不必等待。延迟脚本，预加载首次绘制需要的东西，按屏幕大小提供图片。给静态资源起包含其哈希值的名字，并永久缓存它们，"
        "同时让 HTML 的有效期保持很短。对插入页面的一切内容都进行转义，设置严格的内容安全策略，并把 cookie 标记为 SameSite。还有，先用真正的按钮和链接，再考虑 ARIA；让每个操作都能用键盘完成；"
        "让文字对比度保持在4.5比1或以上。",
    "Six problems, with full solutions in the part's notes. Pause":
        "六道习题，完整解答在这一部分的笔记里。你可以在任何一道上暂停。第五道是一道构建题：给我们的玩具浏览器加上 flexbox，并渲染一个随窗口变窄而收缩的导航栏。最后一道标有星号，是一道研究题："
        "带固有尺寸的增量 flex 布局，其代价以变化为界，并给出一个相匹配的下界。",
    "Next time, Part 43: APIs and services. When a program is":
        "下一次，第43部分：API 与服务。当一个程序被拆分到多台机器上，每次调用都变成一条可能丢失、重复或延迟的消息。我们会推导出承载这些消息的线路格式，让操作可以安全地重试，用“至少一次”加上去重构建出“恰好一次”，"
        "并防止服务彼此压垮。",
    "The books and papers this part follows are on screen and in":
        "这一部分所依据的书籍和论文，都在屏幕上和笔记里。感谢观看。",
}

PHRASES = {"one": "一", "two": "两", "three": "三", "four": "四", "five": "五", "six": "六", "seven": "七",
           "eight": "八", "nine": "九", "ten": "十"}
