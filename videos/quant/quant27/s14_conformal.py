from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import BAD, COIN, GOOD, HURDLE, NET, OOS_C, PART, TREE, ask, fit_right, load


class Conformal(VoiceoverScene):
    def construct(self):
        c = load("conformal")
        self.card()
        self.split()
        self.panel(c)
        self.drift(c["btc"])
        self.aci(c["btc"])
        self.question()

    def card(self):
        c = chapter_card(13, r"Conformal prediction", r"How wide is a forecast's error, with no model of the errors?",
                         part=PART)
        with self.voiceover('Chapter thirteen. Prediction intervals: separate the exchangeable rank theorem, a selected empirical illustration and the boundary conditions behind adaptive counting guarantees.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def split(self):
        rows = [cmath(r"R_i", r"=", r"|\,y_i - \hat f(x_i)\,|,\quad i = 1, \dots, n\ \ \text{(calibration)}", font_size=34,
                      colors={r"R_i": TREE}),
                cmath(r"\hat q", r"=", r"R_{(k)},\quad k = \lceil (n + 1)(1 - \alpha) \rceil", font_size=34,
                      colors={r"\hat q": TREE}),
                cmath(r"C(x)", r"=", r"\big[\hat f(x) - \hat q,\ \hat f(x) + \hat q\,\big]", font_size=34,
                      colors={r"C(x)": NET}),
                cmath(r"\Pr\big(y \in C(x)\big)", r"\ge", r"1 - \alpha", font_size=34,
                      colors={r"\Pr\big(y \in C(x)\big)": GOOD})]
        whys = [why('Fit independently of calibration labels; then require calibration and new scores to be exchangeable conditional on the fitted predictor.'),
                why('Rank $k=\\lceil(n+1)(1-\\alpha)\\rceil$; use $+\\infty$ if $k>n$. The House helper caps k at n, so the general theorem does not extend to tiny alpha.'),
                why(r"the interval for a new point: the forecast, plus or minus that quantile; any model, any $\hat f$"),
                why(r"if the new point and the calibration points are exchangeable, the new error is equally likely to "
                    r"rank anywhere among the $n + 1$, so it exceeds $\hat q$ with probability at most $\alpha$ "
                    r"(Vovk, Gammerman and Shafer 2005; Lei et al.\ 2018)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.5, buff=0.42, edge=6.9)
        with self.voiceover(
            "Split conformal starts with a predictor fitted independently of calibration labels. <bookmark mark='a'/> Compute calibration residual scores using that fixed predictor. <bookmark mark='b'/> Choose rank k equal to the ceiling of n plus one times one minus alpha. If k exceeds n, use infinite width; the unchanged House helper instead caps the rank at n. <bookmark mark='c'/> Construct the prediction interval from that score quantile. <bookmark mark='d'/> Conditional on training, exchangeable calibration and new scores imply marginal coverage at least one minus alpha. Ties can make it conservative. This is not per-asset or regime-conditional coverage, and model selection on calibration labels removes the standard independent-fitting argument."
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
        self.wait(0.5)
        self.clear_scene()

    def panel(self, c):
        weekly = {a: np.asarray(c[a]["weekly"]) for a in ("0.1", "0.2")}
        n = len(weekly["0.1"])
        g = axes([0, n - 1], [0.0, 1.0], x_length=7.4, y_length=3.8, xlabel=r"test week, 2020",
                 ylabel=r"share of coins inside their interval", xticks=[0,(n-1)//2,n-1], yticks=[0,.2,.4,.6,.8,1],
                 font_size=17).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lines = VGroup()
        for a, col in (("0.1", NET), ("0.2", TREE)):
            lines.add(curve(ax, np.arange(n), weekly[a], col, stroke_width=2.5))
        tgt = VGroup(DashedLine(ax.c2p(0, 0.9), ax.c2p(n - 1, 0.9), color=NET, stroke_width=1.5, stroke_opacity=0.7),
                     DashedLine(ax.c2p(0, 0.8), ax.c2p(n - 1, 0.8), color=TREE, stroke_width=1.5, stroke_opacity=0.7))
        side = VGroup(
            MathTex(rf"90\%:\ \text{{covered}}\ {100 * c['0.1']['cover']:.1f}\%", font_size=24, color=NET),
            MathTex(rf"80\%:\ \text{{covered}}\ {100 * c['0.2']['cover']:.1f}\%", font_size=24, color=TREE),
            MathTex(rf"\text{{worst week}}:\ {100 * weekly['0.1'].min():.0f}\%", font_size=24, color=BAD),
            wrapped_label('Original NN2 selection/early stopping reuses the later calibration labels. Dependence, drift and integer-date label boundaries add limitations. Coverage is descriptive; the standard split theorem does not certify this illustration.', 3.5, 22,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"The original crypto intervals reuse the validation labels for both model selection and calibration. <bookmark mark='a'/> That violates the standard independent-fitting construction before considering coin dependence, drift and imperfect calendar boundaries. <bookmark mark='b'/> Saved nominal ninety-percent coverage is {100*c['0.1']['cover']:.2f} percent and nominal eighty-percent coverage is {100*c['0.2']['cover']:.2f}. The worst saved ninety-percent week is {100*weekly['0.1'].min():.2f} percent. All weekly values are visible on zero-to-one axes. Near-nominal pooled coverage is descriptive, not certification. A time sequence need not logically violate exchangeability, but the needed symmetry is not justified by this selected market sample."
        ) as vo:
            self.play(FadeIn(g), Create(tgt))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def drift(self, b):
        r = np.asarray(b["r"])
        T = len(r)
        top = max(float(np.max(np.abs(r)))*1.05,float(b["q_static"])*1.05,.1)
        g = axes([0, T - 1], [0, top], x_length=10.0, y_length=3.8, xlabel=r"day, from May 2018 to December 2020",
                 ylabel=r"Bitcoin's absolute daily return", xticks=[0,(T-1)//2,T-1], yticks=list(np.linspace(0,top,5)),
                 yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=13).move_to(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Line(ax.c2p(i, 0), ax.c2p(i, abs(v)), stroke_width=1.2,
                             color=BAD if abs(v) > b["q_static"] else COIN, stroke_opacity=0.8) for i, v in enumerate(r)])
        stat = DashedLine(ax.c2p(0, b["q_static"]), ax.c2p(T - 1, b["q_static"]), color=HURDLE, stroke_width=2.5)
        cap = MathTex(rf"\text{{fixed interval, from the first 120 days}}:\ \pm {100 * b['q_static']:.1f}\%\ \ \to\ "
                      rf"\text{{covered}}\ {100 * b['cover_static']:.0f}\%", font_size=24, color=HURDLE).to_edge(UP,
                                                                                                      buff=0.5)
        with self.voiceover(
            f"A second original illustration forecasts Bitcoin daily log returns as zero. <bookmark mark='a'/> A fixed interval is calibrated on the first one hundred and twenty observations. Its half-width is {100*b['q_static']:.2f} percent in log-return units. <bookmark mark='b'/> Saved later coverage is {100*b['cover_static']:.2f} percent. This describes a fixed historical path; it neither proves exchangeability nor identifies an optimal width. The plot includes every saved absolute return and the full interval threshold."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in bars], lag_ratio=0.002, run_time=2))
            vo.wait_until("b")
            self.play(Create(stat), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def aci(self,b):
        head=label(r"Adaptive counting: identity and conditions",font_size=34).to_edge(UP,buff=.35)
        eqs=VGroup(MathTex(r"a_{t+1}=a_t+\gamma(\alpha-e_t)",font_size=36),MathTex(r"\frac1T\sum_t e_t-\alpha=\frac{a_1-a_{T+1}}{\gamma T}",font_size=34),wrapped_label(r"Bounded state gives a finite counting bound. Ideal boundary conventions use infinite intervals at $a_t\le0$ and empty sets at $a_t\ge1$.",11.6,27),wrapped_label(r"The original uses a finite past maximum at the lower boundary and zero width at the upper boundary. Its state need not stay bounded.",11.6,27,HURDLE)).arrange(DOWN,buff=.45).next_to(head,DOWN,buff=.5)
        with self.voiceover("Adaptive counting starts with an exact telescoping identity. After a miss, lower the working level; after a hit, raise it. Summing the updates relates average error to the change in the working level. A vanishing counting error requires the state change to be sublinear in time; a bounded state suffices. Ideal infinite-interval and empty-set boundary conventions can ensure a finite bound. The unchanged House implementation uses a finite past maximum and zero width instead, so it does not inherit that arbitrary-sequence guarantee."):
            self.play(FadeIn(head),FadeIn(eqs))
        self.clear_scene()
        ra,rs=np.asarray(b["roll_aci"]),np.asarray(b["roll_static"]);n=len(ra)
        g=axes([0,n-1],[0,1],x_length=8.4,y_length=4.2,xlabel=r"saved evaluation day",ylabel=r"past-60-day coverage",xticks=[0,round((n-1)/2),n-1],yticks=[0,.2,.4,.6,.8,1],font_size=14).to_edge(LEFT,buff=.6).shift(DOWN*.35)
        la=curve(g.ax,np.arange(n),ra,NET,stroke_width=3);ls=curve(g.ax,np.arange(n),rs,HURDLE,stroke_width=3)
        target=DashedLine(g.ax.c2p(0,.9),g.ax.c2p(n-1,.9),color=GREY_B)
        side=VGroup(MathTex(rf"\text{{adaptive: }}{100*b['cover_aci']:.2f}\%",font_size=28,color=NET),MathTex(rf"\text{{fixed: }}{100*b['cover_static']:.2f}\%",font_size=28,color=HURDLE),wrapped_label(r"Original finite-quantile rule, 120-day history, step 0.01. One observed path; no arbitrary-sequence or regime-conditional guarantee.",3.6,24,GREY_A)).arrange(DOWN,buff=.35).to_edge(RIGHT,buff=.3)
        with self.voiceover(f"The saved Bitcoin path has coverage {100*b['cover_aci']:.2f} percent for the adaptive finite-quantile rule and {100*b['cover_static']:.2f} percent for the fixed interval. Every rolling coverage value is displayed. These are descriptive outcomes of the original rule with step point zero one and a one-hundred-twenty-day window. They do not certify arbitrary-sequence, conditional or future coverage."):
            self.play(FadeIn(g),Create(target),Create(la),Create(ls),FadeIn(side))
        self.clear_scene()
        counter=definition_card(r"Why a finite past maximum is insufficient",wrapped_label(r"Fixed mathematical counterexample: residual scores increase strictly forever. Every next score exceeds the finite past maximum, so every interval misses. Then $a_{t+1}=a_t-\gamma(1-\alpha)$ and $a_t\to-\infty$. The telescoping identity remains true, but its remainder need not vanish.",10.6,29),width=11.8,font_size=28)
        with self.voiceover("A fixed mathematical counterexample shows the limitation. Let residual scores increase strictly forever. Each new score exceeds the finite past maximum, so every interval misses, even after the working level becomes negative. The level then decreases without bound. The telescoping identity remains correct, but its remainder does not vanish. Infinite-width boundary conventions would change this example; this original does not use them. No additional market experiment is needed to see the distinction."):
            self.play(FadeIn(counter))
        self.clear_scene()

    def question(self):
        q = ask(r"a conformal interval for a strategy's monthly return is calibrated on 2010--2019 and covers 90\% "
                r"there. In 2020 it covers 70\%. Is the guarantee broken, and what would you change?")
        with self.voiceover(
            "Pause and predict. A conformal interval for a strategy's monthly return is calibrated on the 2010s and "
            "covers ninety percent there. In 2020 it covers seventy. Is the guarantee broken, and what would you "
            "change?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
