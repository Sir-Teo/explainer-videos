# Chinese narration guide for *Analysis, Built* (分析学，从零搭建)

The Chinese version of each part is the same video with Chinese narration and Chinese subtitles; the on-screen
formulas and labels are unchanged.  Each part's translation lives in `videos/analysisN/narration_zh.json`
(maintained with `tools/translate_narration.py`).

## How to translate a line

* **Spoken Mandarin, not written Chinese.** This is a voice-over for a 3Blue1Brown-style video: warm, clear, and
  natural to the ear, like a good lecturer talking, not a textbook.  Short sentences.  Prefer 我们 / 你 / 来看 /
  注意.  Avoid stiff written forms (之、其、该、乃、亦、故而).  It is fine to restructure a sentence so it sounds
  natural, as long as the mathematics and the order of ideas stay the same.
* **Keep every bookmark** `<bookmark mark='x'/>` exactly as written, in the same order, at the place in the Chinese
  sentence where the same idea is being said.  The animation is timed to the bookmark: put it right before the
  Chinese words that correspond to the English words after it.  Never drop, rename, or reorder one.
* **Same content, similar length.** Don't add explanations or drop clauses.  Chinese narration of the same content
  runs a little shorter than English; that is fine.
* **Punctuation**: full-width Chinese punctuation (，。；：？！“”（）、).  End every sentence with 。？or！.
* **Numbers**: Arabic digits for numbers that appear on screen (1.414、2/3 → 三分之二 when spoken as a fraction,
  10^6 → 10的6次方, 0.5 → 0.5).  Years as digits: 1807年.  Rudin's theorem numbers as digits: 定理2.43.
* **Math read aloud** the way a Chinese lecturer says it:
  * single Latin letters stay Latin: x、n、f、K、E (read as letter names); f of x → f(x) 或 f x 在 …；
  * Greek letters as the symbol: ε、δ、π、μ、σ、λ、ω、φ、Ω (the voice reads them correctly);
  * x squared → x的平方；square root of two → 根号2；a sub n → a_n 读作 “a n”，写成 a_n is fine;
  * the sum of … from n = 1 to infinity → n从1到无穷的……之和；the limit as n goes to infinity → 当n趋于无穷时的极限；
  * less than or equal to → 小于等于；if and only if → 当且仅当；for every → 对任意；there exists → 存在。
* **Chapter titles** (`chapters`) are short; keep their numbering (“1. …”).  The part title (`title`) follows the
  pattern `分析学，从零搭建 · 第1部分：实数与空间的形状`.
* **Names** use the standard Chinese transliteration below; the book titles use their Chinese editions.

## Glossary

| English | 中文 |
|---|---|
| Walter Rudin | 沃尔特·鲁丁 (鲁丁) |
| *Principles of Mathematical Analysis* | 《数学分析原理》 |
| *Real and Complex Analysis* | 《实分析与复分析》 |
| *Functional Analysis* | 《泛函分析》 |
| real / rational / irrational numbers | 实数 / 有理数 / 无理数 |
| field, ordered field | 域，有序域 |
| least upper bound (property) | 最小上界（性质），上确界性质 |
| supremum / infimum | 上确界 / 下确界 |
| Dedekind cut | 戴德金分割 |
| Archimedean property | 阿基米德性质 |
| dense | 稠密 |
| countable / uncountable | 可数 / 不可数 |
| diagonal argument | 对角线论证 |
| metric space, metric, distance | 度量空间，度量，距离 |
| neighborhood, ball | 邻域，球 |
| open / closed set | 开集 / 闭集 |
| limit point, isolated point | 极限点，孤立点 |
| interior, closure, boundary | 内部，闭包，边界 |
| open cover, finite subcover | 开覆盖，有限子覆盖 |
| compact (set) | 紧（集） |
| Heine–Borel theorem | 海涅–博雷尔定理 |
| Cantor set, perfect set | 康托尔集，完全集 |
| connected | 连通 |
| sequence, subsequence | 序列，子序列 |
| series, partial sum | 级数，部分和 |
| converge / diverge | 收敛 / 发散 |
| Cauchy sequence, complete | 柯西序列，完备 |
| lim sup / lim inf | 上极限 / 下极限 |
| ratio test / root test / comparison test | 比值判别法 / 根值判别法 / 比较判别法 |
| absolutely / conditionally convergent | 绝对收敛 / 条件收敛 |
| rearrangement (Riemann's theorem) | 重排（黎曼重排定理） |
| power series, radius of convergence | 幂级数，收敛半径 |
| summation by parts | 分部求和 |
| continuous, uniformly continuous | 连续，一致连续 |
| intermediate value theorem | 介值定理 |
| mean value theorem | 中值定理 |
| Taylor's theorem | 泰勒定理 |
| L'Hôpital's rule | 洛必达法则 |
| Darboux's theorem | 达布定理 |
| Thomae's function | 托马函数 |
| Riemann integral, upper / lower sum | 黎曼积分，上和 / 下和 |
| Riemann–Stieltjes integral | 黎曼–斯蒂尔切斯积分 |
| fundamental theorem of calculus | 微积分基本定理 |
| pointwise / uniform convergence | 逐点收敛 / 一致收敛 |
| equicontinuous, Arzelà–Ascoli | 等度连续，阿尔泽拉–阿斯科利定理 |
| Weierstrass (approximation) theorem | 魏尔斯特拉斯（逼近）定理 |
| Stone–Weierstrass | 斯通–魏尔斯特拉斯定理 |
| Fourier series / coefficient | 傅里叶级数 / 系数 |
| Fejér, Parseval, Gibbs phenomenon | 费耶尔，帕塞瓦尔，吉布斯现象 |
| sup norm | 上确界范数 |
| linear map, operator norm | 线性映射，算子范数 |
| contraction (mapping), fixed point | 压缩映射，不动点 |
| inverse / implicit function theorem | 反函数定理 / 隐函数定理 |
| Picard iteration | 皮卡迭代 |
| differential form, Stokes' theorem | 微分形式，斯托克斯定理 |
| measure, measurable, σ-algebra | 测度，可测，σ代数 |
| Lebesgue measure / integral | 勒贝格测度 / 积分 |
| null set, almost everywhere | 零测集，几乎处处 |
| Vitali set | 维塔利集 |
| simple function | 简单函数 |
| monotone / dominated convergence theorem | 单调收敛定理 / 控制收敛定理 |
| Fatou's lemma, Egorov, Lusin | 法图引理，叶戈罗夫定理，卢津定理 |
| Riesz representation theorem | 里斯表示定理 |
| Fubini's theorem | 富比尼定理 |
| Jensen, Hölder, Minkowski, Young | 詹森，赫尔德，闵可夫斯基，杨 |
| L^p space, norm | L^p 空间，范数 |
| Hilbert space, inner product | 希尔伯特空间，内积 |
| orthogonal projection, orthonormal basis | 正交投影，标准正交基 |
| parallelogram law | 平行四边形法则 |
| Riesz–Fischer | 里斯–费舍尔定理 |
| complex measure, total variation | 复测度，全变差 |
| Radon–Nikodym | 拉东–尼科迪姆定理 |
| holomorphic, conformal | 全纯，共形 |
| winding number, residue, argument principle | 环绕数，留数，辐角原理 |
| Goursat, Cauchy's theorem / formula | 古尔萨，柯西定理 / 柯西积分公式 |
| Schwarz lemma, Runge, Montel | 施瓦茨引理，龙格定理，蒙泰尔定理 |
| Riemann mapping theorem, Schwarz–Christoffel | 黎曼映射定理，施瓦茨–克里斯托费尔 |
| Poisson integral, harmonic | 泊松积分，调和 |
| Weierstrass / Blaschke product | 魏尔斯特拉斯乘积 / 布拉施克乘积 |
| Hardy space H^p | 哈代空间 H^p |
| Banach space, Fréchet space | 巴拿赫空间，弗雷歇空间 |
| Baire category theorem | 贝尔纲定理 |
| uniform boundedness principle | 一致有界原理 |
| Lebesgue constants | 勒贝格常数 |
| open mapping / closed graph theorem | 开映射定理 / 闭图像定理 |
| Hahn–Banach theorem | 哈恩–巴拿赫定理 |
| dual space, weak / weak-* convergence | 对偶空间，弱收敛 / 弱*收敛 |
| Mazur, Banach–Alaoglu, Krein–Milman | 马祖尔，巴拿赫–阿劳格鲁定理，克列因–米尔曼定理 |
| compact operator, Fredholm | 紧算子，弗雷德霍姆 |
| distribution, test function | 分布（广义函数），检验函数 |
| mollifier | 磨光函数 |
| Fourier transform, Schwartz space | 傅里叶变换，施瓦茨空间 |
| tempered distribution | 缓增分布 |
| Plancherel, Poisson summation | 普朗歇尔定理，泊松求和公式 |
| Paley–Wiener, Denjoy–Carleman | 佩利–维纳定理，当茹瓦–卡莱曼定理 |
| Sobolev, fundamental solution | 索伯列夫，基本解 |
| Wiener's Tauberian theorem | 维纳陶伯定理 |
| Banach algebra, spectrum, spectral radius | 巴拿赫代数，谱，谱半径 |
| shift operator, Volterra operator | 移位算子，沃尔泰拉算子 |
| Gelfand transform, C*-algebra | 盖尔范德变换，C*代数 |
| self-adjoint, unitary, normal | 自伴，酉，正规 |
| spectral theorem, Born rule | 谱定理，玻恩定则 |
| Cayley transform, Stone's theorem | 凯莱变换，斯通定理 |
| Fourier, Lagrange, Cantor, Euler, Gauss | 傅里叶，拉格朗日，康托尔，欧拉，高斯 |
| Cauchy, Riemann, Weierstrass, Hilbert | 柯西，黎曼，魏尔斯特拉斯，希尔伯特 |
| Lebesgue, Banach, Riesz, von Neumann | 勒贝格，巴拿赫，里斯，冯·诺伊曼 |
| ledger (the series' running table) | 账本 |
| swap two limits | 交换两个极限（的次序） |
| Joseph Fourier, Georg Cantor, Richard Dedekind, Maurice Fréchet | 约瑟夫·傅里叶，格奥尔格·康托尔，理查德·戴德金，莫里斯·弗雷歇 |
| Méray, Liouville, Hermite, Lindemann | 梅雷，刘维尔，埃尔米特，林德曼 |
| Bolzano–Weierstrass, Cauchy–Schwarz | 波尔查诺–魏尔斯特拉斯定理，柯西–施瓦茨不等式 |
| k-cell (Rudin 2.17) | k-胞腔 |
| path-connected | 道路连通 |
| devil's staircase (the Cantor function) | 魔鬼阶梯（康托尔函数） |
| the bisection engine | 二分法引擎 |
| the hop (Part 1's p ↦ (2p+2)/(p+2)) | 那一跳 |
| script A (𝒜) | 花体A |
| bookkeeping (a technicality) | 技术性的规定 (not 记账: 账本 is the ledger) |
| the hook (a part's opening chapter) | 开场 |
| museum piece (a pathology card); into the museum | 博物馆藏品；收进我们的博物馆 |
| alternating harmonic / harmonic / geometric series | 交错调和级数 / 调和级数 / 几何级数 |
| running total; overshoot; swing | 累计的和；冲过头；摆动 |
| the first / second player (ε, then N or δ) | 第一个玩家 / 第二个玩家 |
| band (ε, horizontal) / strip (δ, vertical) | 带子、横带 / 竖带 |
| the ε/2 trick, ε/3 | 二分之ε技巧，三分之ε技巧 |
| tail (E_N); diameter | 尾部；直径 |
| subsequential limit | 子序列极限 |
| high-water / low-water mark | 高水位线 / 低水位线 |
| R^k (spoken "R k") | k维空间 |
| Cauchy criterion; condensation test | 柯西准则；柯西凝聚判别法 |
| Dirichlet's test; alternating series test | 狄利克雷判别法；交错级数判别法 |
| telescope (a sum) | 裂项相消 |
| Cauchy product | 柯西乘积 |
| Abel, Dirichlet, Nicole Oresme, Mertens, Bolzano, Darboux | 阿贝尔，狄利克雷，尼科尔·奥雷姆，梅滕斯，波尔查诺，达布 |
| Euler's constant | 欧拉常数 |
| pile (Riemann's positive / negative piles) | 堆 |
| compound interest | 复利 |
| preimage, pull back | 原像，拉回 |
| bijection; one to one; onto | 双射；一对一；满射 |
| extreme value theorem | 最值定理 (not 极值定理) |
| discontinuity of the first (simple) / second kind; one-sided limit | 第一类（简单）间断 / 第二类间断；单侧极限 |
| difference quotient, secant, tangent, chord | 差商，割线，切线，弦 |
| chain rule; (vertical) shear | 链式法则；（竖直方向的）错切 |
| intermediate value property | 介值性质 |
| f′(x), f′(0); g′, g″ | f在x处的导数、f在0处的导数；g的一阶导数、二阶导数 (no prime symbols in the text) |
| p′ (a second point, not a derivative) | p撇 |
| smooth / analytic; bump function | 光滑 / 解析；鼓包函数 |
| vector-valued function | 向量值函数 |
| partition (of an interval); refine; common refinement | 分划；加细；公共加细 (not 分割: that's the Dedekind cut) |
| upper / lower integral; integrable | 上积分 / 下积分；可积 |
| integrator (α in ∫f dα); integrate against α | 积分子；f关于α的积分 |
| unit step; singular measure | 单位阶跃；奇异测度 |
| Dirichlet's function (1 on Q, 0 off Q) | 狄利克雷函数 |
| inscribed polygon (curve length) | 内接折线 |
| uniformly Cauchy; Weierstrass M-test | 一致柯西；魏尔斯特拉斯M判别法 |
| the convergence dashboard: lens, probe, energy | 仪表盘：镜头，探针，能量 |
| the camera (functions plotted as points) | 相机 |
| limits pass through continuity / integrals | 极限穿过连续性 / 积分 |
| Dini's theorem / Dini's test; Lipschitz | 迪尼定理 / 迪尼判别法；利普希茨 |
| zigzag (Rudin's φ, distance to the nearest even integer) | 之字形函数 (not 锯齿: that's the sawtooth) |
| Peano, Schoenberg, Marshall Stone, Bernstein | 皮亚诺，舍恩伯格，马歇尔·斯通，伯恩斯坦 |
| Brownian motion; almost surely | 布朗运动；几乎必然 |
| pointwise / uniformly bounded | 逐点有界 / 一致有界 |
| dyadic points | 二进有理点 |
| Landau kernel (Rudin's bump Q_n); Dirichlet / Fejér kernel | 兰道核（鼓包）；狄利克雷核 / 费耶尔核 |
| law of large numbers | 大数定律 |
| algebra of functions; separates points; vanishes at no point | 函数代数；分离点；在任何一点都不全为零 |
| uniform closure; the cap (Stone–Weierstrass, step four) | 一致闭包；帽子 |
| complex conjugate, z bar | 复共轭，z的共轭 |
| trigonometric polynomial | 三角多项式 |
| Abel's theorem; Abel limit | 阿贝尔定理；阿贝尔极限 |
| fundamental theorem of algebra | 代数基本定理 |
| orthogonality; mean square; Pythagoras | 正交性；均方；勾股定理 |
| Bessel's inequality; Parseval's theorem / equation | 贝塞尔不等式；帕塞瓦尔定理 / 等式 |
| Du Bois-Reymond, Wilbraham, Gibbs | 杜布瓦–雷蒙，威尔布拉汉姆，吉布斯 |
| overshoot (Gibbs); ringing | 冲过头；振铃 |
| gamma function; Bohr–Mollerup; Stirling's formula | 伽马函数；玻尔–莫勒鲁普定理；斯特林公式 |
| Rudin's theorem 8.11; Rudin's chapter 7 / this video's chapter 15 | 鲁丁的定理8.11；鲁丁书中第7章 / 第十五章 |
| 3Blue1Brown | 3B1B (Latin runs of 4+ letters fail the check) |
| Jacobian (matrix / determinant); gradient; level curves | 雅可比矩阵 / 雅可比行列式；梯度；等高线 |
| directional derivative; second difference; iterated limits / integrals | 方向导数；二阶差分；累次极限 / 累次积分 |
| contraction principle | 压缩映射原理 |
| folium of Descartes; rank theorem | 笛卡儿叶形线；秩定理 |
| differentiation under the integral sign | 积分号下求导 |
| change of variables; partition of unity | 换元公式；单位分解 |
| exterior derivative; closed / exact form; Poincaré's lemma | 外微分；闭形式 / 恰当形式；庞加莱引理 |
| f_x, f_y, f_xy (partials, written with underscores) | f_x、f_y、f_xy (the voice reads "f x") |
| 2g, 2 times g | 2倍的g (never "2g": read as grams) |
| outer measure; nowhere dense | 外测度；无处稠密 |
| Borel sets; indicator function; counting measure; Dirac mass | 博雷尔集；示性函数；计数测度；狄拉克测度 |
| lid (an integrable dominating function) | 盖子 |
| mass escaping; the spike / the runaway / the spreading | 质量的逃逸；尖刺 / 滑走 / 摊开 |
| typewriter sequence; improper integral | 打字机序列；反常积分 |
| Urysohn's lemma; plateau function; collar | 乌雷松引理；平台函数；边沿 |
| Littlewood's three principles; Lusin; Vitali–Carathéodory | 李特尔伍德的三条原则；卢津；维塔利–卡拉泰奥多里定理 |
| Tonelli; monotone class; sigma-finite | 托内利；单调类；σ有限 |
| layer cake formula; Banach–Tarski | 千层蛋糕公式；巴拿赫–塔斯基悖论 |
| Basel sum | 巴塞尔和 |

## Conventions settled while translating Part 1

* Subscripts as `x_1`, `E_n`, `f_n`, `G_α` (the voice reads `x_n` as "x n"); a star as `x*` (read "x 星").
* `sin`, `cos`, `sup`, `inf`, `lim`, `ln`, `log` stay in Latin letters: sin x、cos n、sup E.
* Spoken fractions in words (三分之一, 二十八分之十二); numbers shown on screen as digits (0.527, 1.414).
* Function arguments that are expressions get full-width parentheses when spoken: sin（根号2乘n）、sin（x分之1）.
* "whole numbers" in a counting context is 正整数; for p and q in p/q it is 整数.
