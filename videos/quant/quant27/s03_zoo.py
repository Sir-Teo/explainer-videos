from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import ml as ML
from videos.quant.quant27.common import (BAD, COIN, GOOD, HURDLE, LINEAR, MOM, NET, OOS_C, PART, TREE, ask, comma,
                                         fit_right, house_lab, load)

FAMILY = {"OLS": LINEAR, "OLS-3": LINEAR, "ENet": LINEAR, "PCR": LINEAR, "PLS": LINEAR, "GBRT": TREE, "NN1": NET,
          "NN2": NET, "NN3": NET}
GROUPS = [(r"momentum", ("r1d", "r1w", "r4w", "r12w", "r26w"), MOM),
          (r"risk", ("vol28", "max28", "skew28", "beta", "ivol"), BAD),
          (r"liquidity proxies", ("range7", "lqv", "dqv", "amihud"), TREE),
          (r"age", ("age",), COIN)]
NAMES = {"r1d": r"last day", "r1w": r"last week", "r4w": r"weeks 2--4", "r12w": r"weeks 5--12", "r26w": r"weeks 13--26",
         "vol28": r"volatility", "max28": r"max daily return", "skew28": r"skewness", "beta": r"beta to Bitcoin",
         "ivol": r"idiosyncratic vol", "range7": r"high--low range", "lqv": r"USDT quote volume", "dqv": r"volume change",
         "amihud": r"Amihud illiquidity", "age": r"days since first close"}


class Zoo(VoiceoverScene):
    def construct(self):
        z = load("zoo")
        self.card()
        self.universe()
        self.features()
        self.models()
        self.protocol()
        self.lab()
        self.results(z)
        self.power(z)
        self.importance(z)
        self.question()

    def card(self):
        c = chapter_card(2, r"The model zoo", r"Which learner forecasts best, and can the test tell them apart?",
                         part=PART)
        with self.voiceover('Chapter two. A nine-model illustration inspired by Gu, Kelly and Xiu, using the original venue-specific USDT-quoted coin research calculations. Its archive selection, target clocks and execution assumptions need examination; it is not a replication of the American stock experiment.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def universe(self):
        head = label(r"A frozen archive is not a historical investable universe", font_size=30).to_edge(UP, buff=.4)
        if head.width > 12.3: head.scale_to_fit_width(12.3)
        cards = VGroup(
            desk_question(r"public archive coverage", r"701 symbol names in the frozen November 2026 list; ordinary readers use 2017--2025 public daily files before research masks", width=12, font_size=29),
            desk_question(r"each included research week", r"at least 10 eligible coins; 60 calendar days since the first available close; past-28-day median quote volume at least 250,000 USDT", width=12, font_size=29),
            desk_question(r"missing quotes and exits", r"the original target uses the last available next-week close, or the current close if none; no liquidation or executable exit price is established", width=12, font_size=29),
        ).arrange(DOWN, buff=.2)
        if cards.height>5.3:cards.scale_to_fit_height(5.3)
        cards.next_to(head,DOWN,buff=.3)
        foot = wrapped_label(r"The panel-sealing original is excluded. Archive membership, the 30-record history screen and later vintages can condition coverage; USDT volume and tradability require separate treatment.", 12, 19, GREY_A).to_edge(DOWN, buff=.35)
        with self.voiceover("Start with the source boundary. The frozen public list contains 701 symbol names. That is later archive coverage, not a reconstruction of what an investor could have bought in each research week. <bookmark mark='a'/> The original reader keeps symbols with at least thirty recorded daily observations and reads public archives through 2025 before applying its research masks. <bookmark mark='b'/> Included weeks need at least ten eligible coins. Eligibility uses sixty calendar days since the first available close and a past-twenty-eight-day median quote volume of at least 250,000 USDT. <bookmark mark='c'/> The next-week target uses the last available close in the following seven days, or the current close when none is observed. That is not a verified liquidation return or proof that delisting losses are complete. <bookmark mark='d'/> This review excludes the panel-sealing output. We can explain the input protocol without showing its future-universe counts or opening a strategy experiment.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until('b'); self.play(FadeIn(cards[1]))
            vo.wait_until('c'); self.play(FadeIn(cards[2]))
            vo.wait_until('d'); self.play(FadeIn(foot))
        self.clear_scene()

    def features(self):
        cols = VGroup()
        for name, keys, col in GROUPS:
            items = VGroup(label(name, font_size=22, color=col),
                           *[label(NAMES[k], font_size=23, color=GREY_A) for k in keys]).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.12)
            cols.add(items)
        cols.arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to(UP * 0.6)
        if cols.width > 12.8:
            cols.scale_to_fit_width(12.8)
        rank = cmath(r"c_{i,t}", r"=", r"2\,\frac{\operatorname{rank}_t(x_{i,t}) - 1}{N_t - 1} - 1\ \in [-1, 1]",
                     font_size=32, colors={r"c_{i,t}": HURDLE}).to_edge(DOWN, buff=1.7)
        note_ = wrapped_label('each week, each characteristic is replaced by its cross-sectional rank (a missing value by the median, 0), as in Gu, Kelly and Xiu: the models see where a coin stands, not its raw level',12.0,22,GREY_B).to_edge(DOWN,buff=.35)
        head = label(r"15 characteristics per coin (the stock zoo has 94)", font_size=28).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The illustration uses fifteen characteristics per coin. <bookmark mark='a'/> Momentum spans several past horizons. Risk features include volatility, extremes, skewness, Bitcoin beta and residual variation. Liquidity proxies include quote volume, price range and Amihud illiquidity; age measures days since the first available close, rather than a verified exchange listing date. <bookmark mark='b'/> Each date's features become cross-sectional ranks from minus one to one, and missing ranks become zero. Even the pointwise models therefore already use relative cross-sectional information."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cols], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rank), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def models(self):
        rows = [cmath(r"\text{OLS}", r":", r"\min_\beta \textstyle\sum (y - c^{\top}\beta)^2\quad(\text{and OLS-3: "
                      r"momentum, volume, volatility})", font_size=28, colors={r"\text{OLS}": LINEAR}),
                cmath(r"\text{ENet}", r":", r"\min_\beta \textstyle\sum (y - c^{\top}\beta)^2 + \lambda\big(\alpha|\beta|_1 + "
                      r"\tfrac{1 - \alpha}{2}|\beta|_2^2\big)", font_size=28, colors={r"\text{ENet}": LINEAR}),
                cmath(r"\text{PCR, PLS}", r":", r"y \approx (C W_K)\,\theta,\ \ W_K = \text{top } K \text{ directions of } "
                      r"C\ \text{(PCR) or of } \operatorname{Cov}(C, y)\ \text{(PLS)}", font_size=28,
                      colors={r"\text{PCR, PLS}": LINEAR}),
                cmath(r"\text{GBRT}", r":", r"\hat f = \textstyle\sum_{m} \nu\, T_m(c),\ \ T_m \text{ a depth-2 tree "
                      r"fitted to the residuals}", font_size=28, colors={r"\text{GBRT}": TREE}),
                cmath(r"\text{NN1--3}", r":", r"\hat f = W_L\,\sigma(\cdots\sigma(W_1 c)),\ \ 32,\ 32\text{--}16,\ "
                      r"32\text{--}16\text{--}8\ \text{units, 5 seeds averaged}", font_size=28,
                      colors={r"\text{NN1--3}": NET})]
        whys = [why('All fifteen predictors and a chosen three-variable crypto baseline; not the stock-paper design'),
                why(r"the elastic net: the lasso's selection and ridge's shrinkage at once, $\lambda$ chosen on validation"),
                why(r"dimension reduction: regress on a few combinations of the characteristics, chosen for their "
                    r"variance (PCR) or for their covariance with the target (PLS)"),
                why(r"boosting (Part 20's engine): many small trees, each correcting the last, shrunk by $\nu = 0.03$; "
                    r"stopped early on validation"),
                why('Feed-forward ReLU networks, regularisation, early stopping and five seeds; a simplified implementation')]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Nine models illustrate three families. <bookmark mark='a'/> Least squares uses all fifteen predictors, or a chosen three-variable crypto baseline. This is not the stock paper's exact characteristic design. <bookmark mark='b'/> Elastic net combines shrinkage and sparsity; a zero coefficient does not prove a feature useless. <bookmark mark='c'/> Principal components target predictor variation, while partial least squares uses target covariance. <bookmark mark='d'/> Boosted trees add small corrective trees. <bookmark mark='e'/> Three network depths average five seeds with regularisation and early stopping. These are simplified implementations inspired by the literature, rather than an exact replication."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
        self.wait(0.5)
        self.clear_scene()

    def protocol(self):
        years = [(r"2018", 0.0, 1.0), (r"2019", 1.0, 2.0), (r"2020", 2.0, 3.0)]
        line = NumberLine(x_range=[0, 3, 1], length=10.0, include_numbers=False, color=GREY_C).move_to(UP * 0.4)
        labels = VGroup(*[label(y, font_size=20).next_to(line.n2p((a + b) / 2), UP, buff=0.5) for y, a, b in years])

        def bar(a, b, col, y, txt):
            r = Rectangle(width=line.n2p(b)[0] - line.n2p(a)[0], height=0.34, stroke_width=0, fill_color=col,
                          fill_opacity=0.8).move_to([(line.n2p(a)[0] + line.n2p(b)[0]) / 2, y, 0])
            return VGroup(r, label(txt, font_size=15, color=BLACK).move_to(r))
        t1 = VGroup(bar(0.0, 1.0 - 0.5, LINEAR, -0.4, r"train"), bar(0.5, 1.0, HURDLE, -0.4, r"validate"),
                    bar(1.0, 2.0, OOS_C, -0.4, r"test 2019"))
        t2 = VGroup(bar(0.0, 1.5, LINEAR, -1.0, r"train"), bar(1.5, 2.0, HURDLE, -1.0, r"validate"),
                    bar(2.0, 3.0, OOS_C, -1.0, r"test 2020"))
        note_ = wrapped_label('Schematic expanding refits; 26 validation weeks. Integer-date cuts do not calendar-purge labels. Training and validation targets are separately winsorised at 1\\% and 99\\%; test targets remain raw.', 12.0, 23, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The original illustration expands its research window. <bookmark mark='a'/> It selects penalties and stopping times using the final twenty-six weeks before each test year. <bookmark mark='b'/> It refits for twenty nineteen and twenty twenty, but subtracting seven from an integer date is not seven calendar days. A late-December feature can have a target ending in early January. Training and validation labels are winsorised separately using their own outcomes; test targets stay raw. These limitations remain in the unchanged algorithm, so this is not a clean calendar-purged protocol."
        ) as vo:
            self.play(Create(line), FadeIn(labels))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in t1], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in t2], lag_ratio=0.3), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"The network ensemble, in the House", ML.MLPEnsemble.fit, "for s in self.seeds:", 8,
                         width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            'The unchanged ensemble fits a fresh network for each seed, with seeded batches and mean squared error. Validation selects an early stopping point. Averaging can reduce seed variation when errors are imperfectly correlated, but does not remove shared bias or guarantee useful information. In this original, validation outcomes also select the model; they are not an untouched later calibration set.'
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def results(self, z):
        rows = z["rows"]
        models = z["models"]
        n = len(models)
        se0 = {m: math.sqrt((1+rows[m]["sr_ew"]**2/(2*52))/(rows[m]["years"])) for m in models}
        lo = float(np.floor(min(0,*(rows[m]["sr_ew"]-2*se0[m] for m in models))))
        hi = float(np.ceil(max(0,*(rows[m]["sr_ew"]+2*se0[m] for m in models))))
        g = axes([-0.6, n - 0.4], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"",
                 ylabel=r"quintile long-short Sharpe ratio, 2019--2020, equal weights", xticks=[],
                 yticks=list(np.linspace(lo,hi,5)), font_size=17).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        se = {}
        bars, errs, names = VGroup(), VGroup(), VGroup()
        for i, m in enumerate(models):
            r = rows[m]
            sr = r["sr_ew"]
            s_ = se0[m]
            se[m] = s_
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, sr)[1]
            bars.add(Rectangle(width=0.5, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=FAMILY[m],
                               fill_opacity=0.85).move_to([ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]))
            errs.add(Line(ax.c2p(i, sr - 2*s_), ax.c2p(i, sr + 2*s_), color=WHITE, stroke_width=2))
            names.add(label(m, font_size=16, color=FAMILY[m]).next_to(ax.c2p(i, lo), DOWN, buff=0.15))
        zero = DashedLine(ax.c2p(-0.6, 0), ax.c2p(n - 0.4, 0), color=GREY_B, stroke_width=1.5)
        r2s = [rows[m]["r2"] for m in models]
        side = VGroup(
            MathTex(rf"R^2_{{\text{{oos}}}}:\ {100 * min(r2s):.1f}\%\ \text{{to}}\ {100 * max(r2s):.1f}\%", font_size=24,
                    color=BAD),
            MathTex(rf"\pm 2\,\text{{s.e.}}\ \approx \pm {2 * np.mean(list(se.values())):.1f}", font_size=24),
            wrapped_label(rf"{rows[models[0]]['coins_week']:.0f} coins a week on average, {rows[models[0]]['years']:.1f} "
                          r"years of weekly tests. White bars: two IID-normal approximate standard errors; dependence and selection unadjusted", 3.3,
                          22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"The original zero-benchmark out-of-sample R squared ranges from {100*min(r2s):.2f} to {100*max(r2s):.2f} percent. <bookmark mark='a'/> This describes these model configurations and dates, rather than all possible return forecasts. <bookmark mark='b'/> Equal-weight quintile long-short gross Sharpe ratios range from {min(rows[m]['sr_ew'] for m in models):.2f} to {max(rows[m]['sr_ew'] for m in models):.2f}. Same-close fills, short availability and costs are not established. <bookmark mark='c'/> The full white ranges show two approximate IID-normal standard errors, using weekly Sharpe units before annualisation. Dependence and selection are omitted. Overlapping individual intervals do not replace inference on paired strategy differences."
        ) as vo:
            self.play(FadeIn(g), FadeIn(names), Create(zero),FadeIn(side[0]))
            vo.wait_until("a")
            self.wait(.1)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if rows[m]["sr_ew"] >= 0 else UP)
                                    for b_, m in zip(bars, models)], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(e_) for e_ in errs], lag_ratio=0.1), FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()

    def power(self,z):
        head=label(r"Precision, power and paired comparisons",font_size=34).to_edge(UP,buff=.35)
        rows=VGroup(MathTex(r"\operatorname{se}(\widehat{SR}_{ann})\approx\sqrt{(1+SR_{ann}^2/(2q))/T_{years}}",font_size=32),MathTex(r"q=52,\quad SR_{ann}=1,\quad T=2:\quad SE\approx0.71",font_size=30),MathTex(r"T\approx4/SR_{ann}^2\quad\text{(two-SE precision heuristic)}",font_size=30),wrapped_label(r"Four years at Sharpe 1, sixteen at 0.5 under the small-per-period-Sharpe approximation. This is not an 80\% power calculation.",11.5,25,HURDLE),wrapped_label(r"Compare paired strategy returns with their covariance, dependence and search history. More correlated coins are not proportionally more independent dates.",11.5,25,GREY_A)).arrange(DOWN,buff=.42).next_to(head,DOWN,buff=.5)
        with self.voiceover("Precision and power are different. For stationary IID normal weekly returns, the annualised Sharpe standard error uses the weekly Sharpe inside its variance correction. An annual Sharpe of one over two years gives about point seven one. The simpler two-standard-error heuristic is four divided by annual Sharpe squared: about four years at one and sixteen at half. It is not a prospective power calculation. A model comparison needs paired returns and their covariance, dependence and selection adjustments. Extra correlated assets do not supply proportionally more independent dates."):
            self.play(FadeIn(head),FadeIn(rows))
        self.clear_scene()

    def importance(self,z):
        imp=z["importance"];panels=VGroup()
        for model in [m for m in ("OLS","GBRT","NN3") if m in imp]:
            order=sorted(z["features"],key=lambda f:abs(imp[model][f]),reverse=True)[:6]
            rows=VGroup(*[wrapped_label(rf"{NAMES[f]}: $\Delta R^2={imp[model][f]:+.4f}$",3.9,22) for f in order]).arrange(DOWN,aligned_edge=LEFT,buff=.25)
            panels.add(VGroup(label(model,font_size=28,color=FAMILY[model]),rows).arrange(DOWN,buff=.3))
        panels.arrange(RIGHT,buff=.45,aligned_edge=UP).move_to(UP*.4)
        head=label(r"Training sensitivity: six largest absolute changes",font_size=30).to_edge(UP,buff=.3)
        foot=wrapped_label(r"Set one ranked characteristic to its median. Signed training-fit changes are descriptive; correlated inputs and interactions prevent a unique causal interpretation.",12.2,25,GREY_A).to_edge(DOWN,buff=.35)
        with self.voiceover("These are training sensitivities, not causal importance. For each model, the six largest absolute changes are selected and their signed values displayed. Replacing a characteristic by its median may interact with correlated inputs. This does not identify liquidity frictions as the cause of a return pattern, or establish that a feature will help on future dates."):
            self.play(FadeIn(head),FadeIn(panels),FadeIn(foot))
        self.clear_scene()

    def question(self):
        q=ask(r"Two years of weekly returns give annual Sharpe 1. Under IID normality, estimate its uncertainty. What extra information is needed to compare it with another model and to calculate power?")
        with self.voiceover("Pause and predict. Estimate the uncertainty of annual Sharpe one over two years under IID normal weekly returns. Then identify the extra information needed for a paired model comparison and a prospective power calculation."):
            self.play(FadeIn(q))
        self.clear_scene()
