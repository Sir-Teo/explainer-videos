"""Act IV, Return Premia (P): Parts 23-29."""

from videos.quant.course import Part

PARTS = [
    Part(
        n=23, level="U", widget="frontier", prereq=(1, 6),
        question="Why should one asset be expected to earn more than another, and what is a unit of risk worth?",
        story="Under Q everything earns the riskless rate. Under P it does not, and this part is where the "
              "series turns to ask why. Markowitz's frontier shows that only risk you cannot diversify should "
              "be paid; the CAPM names that risk as beta, and the data draw the line too flat. One equation "
              "contains every asset-pricing model, price equals the expectation of a discount factor times "
              "the payoff, and the models differ only in what the discount factor is: consumption, factors, "
              "the wealth of intermediaries, the demand of inelastic investors. The equity premium is too "
              "large and prices move too much for the simplest versions. Behaviour, limits of arbitrage and "
              "bubbles close the part.",
        handoff="The factors that fill the gap are Part 24; the optimizer's weakness is Part 30; the limits of "
                "arbitrage are measured in crises (Part 41).",
        outside="Parts 1 and 6.",
        objectives={
            "U": ["Draw an efficient frontier and find the tangency portfolio; explain diversification.",
                  "State the CAPM, compute a beta, and say what the flat security market line means."],
            "M": ["Derive the frontier and the CAPM; write any pricing model as p = E[m x] and derive the "
                  "Hansen-Jagannathan bound.",
                  "Estimate a consumption model by GMM and state the equity-premium and excess-volatility "
                  "puzzles; decompose returns with Campbell and Shiller."],
            "D": ["Derive prices with heterogeneous beliefs and short-sale constraints (Harrison and Kreps; "
                  "Scheinkman and Xiong): the resale option as a bubble; read intermediary and demand-system "
                  "asset pricing."],
            "I": ["Explain why arbitrageurs with outside capital can be forced out at the worst time (Shleifer "
                  "and Vishny)."],
        },
        results=[
            ("The pricing equation", r"p_t=\mathbb E_t\bigl[m_{t+1}\,x_{t+1}\bigr]"),
            ("CAPM", r"\mathbb E[R_i]-R_f=\beta_i\bigl(\mathbb E[R_m]-R_f\bigr),\qquad \beta_i=\frac{\operatorname{Cov}(R_i,R_m)}{\operatorname{Var}(R_m)}"),
            ("Tangency portfolio", r"w^\ast\propto\Sigma^{-1}(\mu-R_f\mathbf 1)"),
            ("Hansen-Jagannathan bound", r"\frac{\sigma(m)}{\mathbb E[m]}\ \ge\ \frac{|\mathbb E[R^e]|}{\sigma(R^e)}"),
        ],
        U=(1, 2, 3, 11, 12), I=(13,), D=(9, 10),
    ),
    Part(
        n=24, level="U", widget="sorts", prereq=(23,),
        question="Small, cheap and rising stocks have beaten the market for decades. Are those premia, "
                 "mistakes, or accidents of the sample?",
        story="Six research indices open the part: the market and five long-short spreads from 1963. A factor "
              "is a portfolio, long one kind of stock and short another, and a factor model claims those few "
              "spreads explain all average returns. The part tests that claim (GRS, Fama-MacBeth), then visits "
              "each factor with its evidence and its failure: size, value and its lost decade, momentum and "
              "the spring of 2009 when it gave back years in three months, profitability, investment, low "
              "risk. The same patterns are checked in other countries and asset classes, and in China, where "
              "the factors are different.",
        handoff="Hundreds more factors were published: Part 25 asks how many are real. The factor library "
                "becomes the risk model of Part 31.",
        outside="Part 23; Part 6 for the tests.",
        objectives={
            "U": ["Explain what a factor portfolio is and how it is built from a sort.",
                  "Describe the size, value and momentum effects and one failure of each."],
            "M": ["Test a factor model with time-series alphas, GRS and Fama-MacBeth.",
                  "Construct a factor from characteristics (two-by-three sorts) and measure whether another "
                  "model spans it."],
            "D": ["Decompose momentum profits (Lo and MacKinlay) into autocovariance, cross-autocovariance and "
                  "dispersion in means, and estimate the pieces."],
            "I": ["Explain how factor products are built and sold, and what must be fixed before a fresh test "
                  "of a factor means anything."],
        },
        results=[
            ("A factor", r"f_t=R^{\text{long}}_t-R^{\text{short}}_t"),
            ("A factor model", r"\mathbb E[R^e_i]=\sum_k\beta_{ik}\,\mathbb E[f_k]"),
            ("GRS", r"\frac{T-N-K}{N}\,\frac{\hat\alpha'\hat\Sigma^{-1}\hat\alpha}{1+\bar f'\hat\Omega^{-1}\bar f}\sim F_{N,\,T-N-K}"),
            ("Momentum", r"\text{signal}_{i,t}=\prod_{s=t-12}^{t-2}(1+R_{i,s})-1"),
        ],
        U=(2, 3, 4, 8), I=(12, 13, 14), D=(),
    ),
    Part(
        n=25, level="U", widget="lucky", prereq=(6, 24),
        question="Hundreds of factors have been published with t-statistics above two. How many of them are "
                 "real?",
        story="Toss two hundred coins twenty times each and a few will look biased. The published factors were "
              "found the same way, by many researchers testing many ideas on one history. The part raises the "
              "hurdle properly: family-wise error and false discovery rates, replication studies with open "
              "data, the decay of returns after publication, shrinkage of t-statistics toward what they would "
              "be without selection. Then it asks the constructive question, how to compress hundreds of "
              "characteristics into a few priced components, with shrinkage of the cross-section, principal "
              "components and instrumented PCA.",
        handoff="The same arithmetic applies to your own research: Part 26 turns it on the backtest.",
        outside="Parts 6 and 24.",
        objectives={
            "U": ["Explain why testing many factors raises the bar for each, and compute a Bonferroni "
                  "threshold.",
                  "Describe publication bias and post-publication decay."],
            "M": ["Control the false discovery rate with Benjamini-Hochberg and estimate the share of true "
                  "nulls; shrink a cross-section of t-statistics by empirical Bayes.",
                  "Extract latent factors with PCA, RP-PCA and IPCA and compare models out of sample."],
            "D": ["Prove that Benjamini-Hochberg controls the FDR under independence; derive Storey's estimator "
                  "and the local false discovery rate; state the weak-factor problem."],
            "I": ["Read a factor paper as an allocator would: what was tried, what was reported, what survives "
                  "costs."],
        },
        results=[
            ("Bonferroni hurdle", r"|t|>N^{-1}\!\Bigl(1-\frac{\alpha}{2M}\Bigr)"),
            ("Benjamini-Hochberg", r"\text{reject } p_{(1)},\dots,p_{(k)},\qquad k=\max\Bigl\{i:\ p_{(i)}\le\frac{i}{M}\,q\Bigr\}"),
            ("Best of M under the null", r"\mathbb E\bigl[\max_{i\le M}t_i\bigr]\approx\sqrt{2\ln M}"),
            ("Empirical-Bayes shrinkage", r"\mathbb E[\theta_i\mid t_i]=m+\frac{v}{v+1}\,(t_i-m)"),
        ],
        U=(1, 2), I=(11, 12), D=(6, 7, 8),
    ),
    Part(
        n=26, level="U", widget="overfit", prereq=(6, 25),
        question="You tested ten thousand trading rules and the best one has a Sharpe ratio of two. What have "
                 "you learned?",
        story="Almost nothing, and the part shows exactly how little. Three leaks make a backtest lie: using "
              "information that was not yet known, using only the firms that survived, and choosing the best "
              "of many. The first two are fixed by engineering, a point-in-time store and an event-driven "
              "backtester that cannot see the future. The third is statistics: the Sharpe ratio's own error, "
              "the expected maximum of many trials, the deflated Sharpe ratio, purged cross-validation, "
              "reality checks. A market with planted alpha, where the truth is known, shows which procedures "
              "find it and which find noise.",
        handoff="Every strategy in the rest of the series is held to this protocol (registered before its test, "
                "its trials counted); the finale asks what such a record can and cannot establish.",
        outside="Parts 6 and 25.",
        objectives={
            "U": ["Name look-ahead, survivorship and selection bias and give an example of each.",
                  "Compute a Sharpe ratio's standard error and the years needed to trust it."],
            "M": ["Compute the expected best Sharpe ratio of N skill-less trials and the deflated Sharpe ratio "
                  "of a result.",
                  "Run purged, embargoed cross-validation and a walk-forward test; estimate the probability "
                  "of backtest overfitting."],
            "D": ["Do inference on the winner: White's reality check, Hansen's SPA, Romano-Wolf, and the "
                  "conditional approach of Andrews, Kitagawa and McCloskey."],
            "I": ["Write a backtest protocol: what is registered before the hold-out is opened, how trials are "
                  "counted, how a live strategy is monitored."],
        },
        results=[
            ("Standard error of a Sharpe ratio", r"\operatorname{se}(\widehat{\mathrm{SR}})\approx\sqrt{\frac{1+\tfrac12\mathrm{SR}^2}{T}}"),
            ("Expected best of N", r"\mathbb E[\max\widehat{\mathrm{SR}}]\approx\sqrt{V}\Bigl((1-\gamma)\,N^{-1}\bigl(1-\tfrac1N\bigr)+\gamma\,N^{-1}\bigl(1-\tfrac1{Ne}\bigr)\Bigr)"),
            ("Deflated Sharpe ratio", r"\mathrm{DSR}=N\!\Bigl(\frac{(\widehat{\mathrm{SR}}-\mathrm{SR}_0)\sqrt{T-1}}{\sqrt{1-\hat\gamma_3\widehat{\mathrm{SR}}+\tfrac{\hat\gamma_4-1}{4}\widehat{\mathrm{SR}}^2}}\Bigr)"),
            ("Minimum backtest length", r"T_{\min}\approx\Bigl(\frac{\mathbb E[\max_N z]}{\mathrm{SR}}\Bigr)^2\ \text{years}"),
        ],
        U=(1, 2, 3, 5), I=(14, 15, 16), D=(11, 12),
    ),
    Part(
        n=27, level="M", widget="descent", prereq=(6, 26),
        question="A model that explains four tenths of one percent of next month's returns is a good model. "
                 "What can machine learning add when the signal is that small?",
        story="Returns are almost all noise, so the usual instincts from image and language models fail: more "
              "capacity fits more noise. The part trains the standard zoo on the cross-section of stocks "
              "(penalized regressions, trees, networks, ensembles), shows where the gains come from, and "
              "takes the 'virtue of complexity' claim seriously, with its critics. The theory chapter explains "
              "double descent with random-matrix tools: why the ridgeless interpolator can generalize, and "
              "why at return-like signal-to-noise only regularization helps. Autoencoders, adversarial "
              "discount factors, attention across assets and conformal intervals follow.",
        handoff="Text is the next source of signal (Part 28); searching for formulas instead of fitting them "
                "is Part 29.",
        outside="Parts 6 and 26; AI, Built, Parts 4-13 for the networks.",
        objectives={
            "U": ["Explain why predicting returns is a low signal-to-noise problem and what out-of-sample R "
                  "squared means."],
            "M": ["Train and evaluate ridge, lasso, gradient-boosted trees and network ensembles on a panel of "
                  "returns with proper time splits.",
                  "Turn predictions into portfolios and measure what survives costs; put a conformal interval "
                  "on a forecast."],
            "D": ["Derive the out-of-sample risk of ridge and ridgeless regression as P/N grows "
                  "(Marchenko-Pastur; Hastie, Montanari, Rosset and Tibshirani) and relate random features to "
                  "kernels."],
            "I": ["Describe a production pipeline for learned signals: labels, purging, monitoring, and what "
                  "firms have said in public about theirs."],
        },
        results=[
            ("Out-of-sample R squared", r"R^2_{\text{oos}}=1-\frac{\sum_t(r_{t+1}-\hat r_{t+1})^2}{\sum_t r_{t+1}^2}"),
            ("Ridge", r"\hat\beta_\lambda=(X'X+\lambda I)^{-1}X'y"),
            ("Ridgeless risk", r"\mathcal R(\gamma)=\sigma^2\frac{\gamma}{1-\gamma}\ (\gamma<1),\qquad r^2\Bigl(1-\frac1\gamma\Bigr)+\frac{\sigma^2}{\gamma-1}\ (\gamma>1)"),
            ("Sharpe from R squared", r"\mathrm{SR}^2_{\text{timing}}\approx\frac{\mathrm{SR}^2_{\text{buy-hold}}+R^2}{1-R^2}"),
        ],
        U=(1,), I=(12, 14, 15, 16), D=(6, 8, 11),
        also=(("AI, Built (the networks, trained from scratch)", "videos/ai/README.md"),),
    ),
    Part(
        n=28, level="U", widget="words", prereq=(6, 26),
        question="One sentence in a central bank's statement moves the bond market. Can a machine read it, and "
                 "can it read it without knowing the future?",
        story="Text is turned into numbers in the order the field did it: word counts and finance "
              "dictionaries, supervised word lists that learn which words precede a rise, topics, embeddings, "
              "transformers, and large language models that read the news directly. Each is tried on Federal "
              "Reserve statements and on returns. The central problem is the one nobody noticed until "
              "recently: a language model trained on text from after the event already knows what happened. "
              "The part builds time-sliced models to measure that look-ahead, and applies the series' "
              "evaluation protocol to a text signal.",
        handoff="Agents that write and test their own signals are Part 29; language models as traders return "
                "in Part 42.",
        outside="Part 6. AI, Built, Parts 13-14, for transformers.",
        objectives={
            "U": ["Represent a document as word counts and score its tone with a dictionary.",
                  "Explain look-ahead bias in a language model."],
            "M": ["Build a supervised sentiment score (screening, topic weights, scoring) and test it out of "
                  "sample; compute embeddings and topics.",
                  "Design a time-sliced evaluation for a text or LLM signal."],
            "D": ["Prove why screening recovers sentiment-charged words (sure screening) and how many "
                  "documents it takes."],
            "I": ["Assess an alternative-data set: coverage, history, point-in-time integrity, decay, cost."],
        },
        results=[
            ("TF-IDF", r"w_{d,j}=\mathrm{tf}_{d,j}\cdot\ln\frac{N}{\mathrm{df}_j}"),
            ("Screening", r"f_j=\frac{\#\{\text{documents with word } j \text{ and a positive return}\}}{\#\{\text{documents with word } j\}}"),
            ("Document tone", r"\text{tone}_d=\frac{N^+_d-N^-_d}{N_d}"),
            ("Attention", r"\operatorname{softmax}\Bigl(\frac{QK^\top}{\sqrt d}\Bigr)V"),
        ],
        U=(1, 2, 11), I=(14, 15, 16, 17), D=(13,),
        also=(("How Large Language Models Work", "videos/ml/llm/README.md"),),
    ),
    Part(
        n=29, level="M", widget="winner", prereq=(26, 27),
        question="If a machine can try ten thousand formulas a minute, is research finished, or has "
                 "overfitting been automated?",
        story="A formulaic alpha is a small program: rank this, difference that, correlate over twenty days. "
              "The space of such programs is astronomically large, and the part searches it three ways, at "
              "random, by genetic programming and by reinforcement learning, and then lets a language-model "
              "agent propose and revise formulas. Every search is run against the trial counter. The winner's "
              "curse is measured directly: the best formula in sample, out of sample. Combining many weak "
              "alphas helps only until the weights themselves become the thing being overfitted. China's "
              "quant industry, and the fund that produced DeepSeek, are the industry file.",
        handoff="The mined signals need a portfolio (Part 30) and a risk model (Part 31); the trials the search "
                "added are part of any honest account of what it found (Part 43).",
        outside="Parts 26 and 27.",
        objectives={
            "U": ["Explain what a formulaic alpha and an information coefficient are.",
                  "Explain the winner's curse of a search."],
            "M": ["Implement random search and genetic programming over expression trees and score candidates "
                  "by IC on held-out days.",
                  "Combine alphas with shrinkage and measure the combination out of sample."],
            "D": ["Derive how many alphas can be combined: the out-of-sample Sharpe ratio of plug-in weights "
                  "as the number of signals grows with the sample."],
            "I": ["Describe an alpha factory: submission, correlation limits, decay monitoring, capacity."],
        },
        results=[
            ("Information coefficient", r"\mathrm{IC}_t=\operatorname{corr}_i\bigl(\text{signal}_{i,t},\ r_{i,t+1}\bigr)"),
            ("Combining alphas", r"w\propto\bigl(\hat\Sigma+\lambda I\bigr)^{-1}\hat\mu"),
            ("Out-of-sample Sharpe of K alphas", r"\mathrm{SR}_{\text{oos}}\approx\frac{\mathrm{SR}^\ast}{\sqrt{1+K/(T\,\mathrm{SR}^{\ast2})}}"),
            ("Size of the search", r"\#\{\text{trees of depth}\le d\}\ \text{grows doubly exponentially in } d"),
        ],
        U=(1, 3), I=(9, 10, 11, 12, 14), D=(6,),
    ),
]
