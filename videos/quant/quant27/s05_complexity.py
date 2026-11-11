from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import (BAD, COMPLEX, GOOD, HURDLE, LINEAR, MKT, MOM, NET, PART, TREE, ask, comma,
                                         fit_right, illustration, load)


def _years(ym):
    ym = np.asarray(ym)
    return ym // 100 + (ym % 100 - 0.5) / 12


class Complexity(VoiceoverScene):
    def construct(self):
        k = load("kmz")
        self.card()
        self.setup_rff()
        self.sharpe(k)
        self.r2(k)
        self.descent(load("descent"))
        self.why()
        self.question()

    def card(self):
        c = chapter_card(4, r"The virtue of complexity", r"Can more parameters than data be better?", lit=(2019, 2025),
                         part=PART)
        with self.voiceover('Chapter four. Random-feature complexity, regularisation and their conditional empirical and mathematical behaviour.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_rff(self):
        rows = [cmath(r"z_j(x)", r"=", r"\sqrt{2/P}\,\big(\sin(w_j^{\top}x),\ \cos(w_j^{\top}x)\big),\quad w_j \sim "
                      r"\mathcal{N}(0, \gamma^2 I)", font_size=34, colors={r"z_j(x)": COMPLEX}),
                cmath(r"\hat\beta(\lambda)", r"=", r"\arg\min_\beta \textstyle\sum_{s = t-12}^{t-1}\big(r_s - "
                      r"\beta^{\top}z(x_{s-1})\big)^2 + \lambda T\,|\beta|^2", font_size=34,
                      colors={r"\hat\beta(\lambda)": COMPLEX}),
                cmath(r"c", r"=", r"P / T", font_size=40, colors={r"c": HURDLE})]
        whys = [why('Fixed Gaussian sine/cosine projections approximate a specified kernel as feature count grows; a finite map does not guarantee learning an arbitrary economic signal.'),
                why(r"ridge regression on the last $T = 12$ months only, refitted every month, from 1931 to 2020; the "
                    r"forecast for next month times its return is the timing strategy"),
                why('More features than observations allows interpolation only at adequate rank and zero penalty. Positive ridge generally does not interpolate; its zero-penalty limit is minimum norm.')]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.5, buff=0.42, edge=6.9)
        with self.voiceover(
            "The illustration is inspired by Kelly, Malamud and Zhou. <bookmark mark='a'/> Fixed Gaussian random projections produce sine and cosine features. Their large-feature limit approximates a specified kernel, rather than guaranteeing that any finite map learns an economic signal. <bookmark mark='b'/> The unchanged original fits rolling twelve-month ridge regressions and averages feature draws. <bookmark mark='c'/> More features than observations permits interpolation only with suitable rank and a zero-penalty limit. Positive ridge usually does not fit every point exactly. Complexity, regularisation and scaling must be considered together."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def sharpe(self, k):
        c = np.log10(np.asarray(k["c"]))
        S = np.asarray(k["grid"]["sharpe"])
        zs = k["z"]
        lo=min(-.1,float(S[:,[0,2,4]].min())-.05);hi=max(.6,float(S[:,[0,2,4]].max())+.05,k["sr_market"]+.05)
        g = axes([-1, 3.1], [lo,hi], x_length=7.4, y_length=4.2, xlabel=r"complexity $c = P/T$",
                 ylabel=r"timing strategy's Sharpe ratio, 1931--2020", xticks=[-1, 0, 1, 2, 3],
                 yticks=list(np.linspace(lo,hi,5)), log_x=True, font_size=17).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        pick = [(0, r"$\lambda = 10^{-3}$", NET), (2, r"$\lambda = 0.1$", COMPLEX), (4, r"$\lambda = 10$", TREE)]
        lines = [curve(ax, c, S[:, j], col, stroke_width=3) for j, _, col in pick]
        mk = DashedLine(ax.c2p(-1, k["sr_market"]), ax.c2p(3.1, k["sr_market"]), color=MKT, stroke_width=2)
        one = DashedLine(ax.c2p(0,lo), ax.c2p(0,hi), color=GREY_C, stroke_width=1.5)
        leg = legend([(col, nm) for _, nm, col in pick] + [(MKT, r"holding the market")], font_size=15)
        side = VGroup(leg, MathTex(rf"c = 1000:\ {S[-1, 2]:.2f}", font_size=26, color=COMPLEX),
                      MathTex(rf"c = 1:\ {S[2, 2]:.2f}", font_size=24, color=BAD),
                      wrapped_label(rf"{k['n']} months; 10 draws of the features averaged; positions on returns scaled "
                                    r"by their trailing volatility, as in the paper", 3.4, 22, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"The original saved grid contains {len(k['P'])*len(k['z'])} capacity and penalty settings. <bookmark mark='a'/> Several selected penalty curves are displayed; this is an illustrative implementation, not an exact independent replication of the paper. <bookmark mark='b'/> At complexity one thousand and penalty point one, gross scaled-return timing Sharpe is {S[-1,2]:.3f}; at complexity one it is {S[2,2]:.3f}. <bookmark mark='c'/> The corresponding scaled-market benchmark is {k['sr_market']:.3f}. The saved grid is descriptive and does not justify choosing a configuration after seeing its research results."
        ) as vo:
            self.play(FadeIn(g), Create(one))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], FadeIn(leg), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(mk))
        self.add(illustration(r"Welch--Goyal predictors; the House's \texttt{ml.kmz\_timing}"))
        self.wait(0.4)
        self.clear_scene()

    def r2(self, k):
        c = np.log10(np.asarray(k["c"]))
        R = np.asarray(k["grid"]["r2"]) * 100
        lo=float(5*np.floor(min(0,R[:,[0,2]].min())/5));hi=float(max(5,5*np.ceil(R[:,[0,2]].max()/5)))
        g = axes([-1, 3.1], [lo, hi], x_length=7.4, y_length=4.2, xlabel=r"complexity $c = P/T$",
                 ylabel=r"out-of-sample $R^2$, \%", xticks=[-1, 0, 1, 2, 3], yticks=list(np.linspace(lo,hi,5)),
                 log_x=True, font_size=17).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        lines = [curve(ax, c, R[:,j], col, stroke_width=3) for j, col in ((0, NET), (2, COMPLEX))]
        zero = DashedLine(ax.c2p(-1, 0), ax.c2p(3.1, 0), color=GREY_C, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"c = 1,\ \lambda = 10^{{-3}}:\ {R[2, 0]:.0f}\%", font_size=24, color=BAD),
            MathTex(rf"c = 1000,\ \lambda = 0.1:\ {R[-1, 2]:+.1f}\%", font_size=24, color=COMPLEX),
            wrapped_label('Selected original capacity/penalty curves; complete vertical range. Interpolation peaks and implicit regularisation are conditional, rather than universal monotonic improvements.', 3.4, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"The full saved R-squared curves matter. <bookmark mark='a'/> At complexity one and penalty one thousandth, the zero-benchmark value is {R[2,0]:.1f} percent. At complexity one thousand and penalty point one, it is {R[-1,2]:.2f} percent. <bookmark mark='b'/> A peak near interpolation and subsequent error reduction can occur under particular scaling and noise assumptions. Positive ridge, feature normalisation and finite random maps change the shape. These R-squared numbers alone cannot order coefficient norms or prove discovery of a new economic signal."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], FadeIn(side[0]), FadeIn(side[1]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def descent(self,d):
        c=np.log10(np.asarray(d["c"]));r0=np.asarray(d["r2"]["1e-08"]);r1=np.asarray(d["r2"]["0.01"])
        transform=lambda y:np.sign(y)*np.log10(1+np.abs(y)/.01)
        lo=float(transform(min(r0.min(),r1.min())*1.05));hi=float(transform(.01))
        ticks=np.array([-10,-1,-.1,-.01,0,.01]);tickpos=list(transform(ticks))
        g=axes([-2.1,1.6],[lo,hi],x_length=7.4,y_length=4.2,xlabel=rf"features per observation ($N={comma(d['N'])}$)",ylabel=r"test $R^2$, \%; symmetric logarithmic scale",xticks=[-2,-1,0,1],yticks=tickpos,yfmt=lambda y:f"{100*np.sign(y)*.01*(10**abs(y)-1):g}",log_x=True,font_size=17).to_edge(LEFT,buff=.5).shift(DOWN*.3)
        l0=curve(g.ax,c,transform(r0),NET,stroke_width=3);l1=curve(g.ax,c,transform(r1),COMPLEX,stroke_width=3)
        peak=DashedLine(g.ax.c2p(0,lo),g.ax.c2p(0,hi),color=GREY_C)
        zero=DashedLine(g.ax.c2p(-2.1,0),g.ax.c2p(1.6,0),color=GREY_B)
        leg=legend([(NET,r"near-zero ridge penalty"),(COMPLEX,r"positive ridge 0.01")],font_size=20).to_edge(RIGHT,buff=.25).shift(UP*1.7)
        side=VGroup(wrapped_label(r"Full saved ranges; vertical transform $\operatorname{sign}(u)\log_{10}(1+|u|/0.01)$. Tick labels retain original $R^2$ percentages.",3.6,23,GREY_A),MathTex(rf"\min R^2={100*min(r0.min(),r1.min()):.1f}\%",font_size=27,color=BAD),wrapped_label(r"Different training draws across capacities and penalties; not a perfectly paired ablation. Tiny penalty is only approximately ridgeless.",3.6,23,GREY_A)).arrange(DOWN,buff=.3).next_to(leg,DOWN,buff=.4)
        fit_right(VGroup(leg,side))
        with self.voiceover(f"A second original illustration uses {d['N']} crypto observations and saved random-feature fits. <bookmark mark='a'/> It displays the complete saved test-R-squared curves, including extreme negative values. A symmetric logarithmic vertical scale compresses large magnitudes; the ticks retain original R-squared percentages and the transformation is stated. <bookmark mark='b'/> Training draws change across capacities and penalties, so this is not a perfectly paired capacity ablation. A near-zero penalty is only approximately ridgeless. The shapes illustrate this implementation; neither a reduced peak nor a larger model establishes a tradable edge.") as vo:
            self.play(FadeIn(g),Create(peak),Create(zero),FadeIn(leg))
            vo.wait_until("a");self.play(Create(l0),Create(l1))
            vo.wait_until("b");self.play(FadeIn(side))
        self.clear_scene()

    def why(self):
        cards = VGroup(
            desk_question(r"why the far side can work", 'Suitable minimum-norm regimes redistribute fitted directions. Scaling, signal alignment and noise determine the bias-variance trade-off.',
                          width=12.2, font_size=29),
            desk_question(r"why the peak", 'Poor conditioning near interpolation can amplify noise. Positive ridge suppresses small-singular-value directions.', width=12.2, font_size=29),
            desk_question(r"what it does not say", r"that the complex model found something the simple ones missed. "
                          r"That is the next chapter's question", width=12.2, font_size=29),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why can extra capacity sometimes reduce error? <bookmark mark='a'/> In suitable overparameterised models, the minimum-norm solution distributes fitted directions and changes the variance-bias trade-off. Feature scaling and signal orientation matter. <bookmark mark='b'/> Near a poorly conditioned interpolation threshold, small singular values can amplify noise. Positive ridge suppresses those directions. <bookmark mark='c'/> The curve does not identify whether new economic information was learned. A matched-information baseline and independent evaluation remain necessary."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                if k_:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q=ask(r"Two differently sized random-feature ridge models have $R^2=-40\%$ and $+1\%$. Can those values alone rank their coefficient norms? Which scaling and model details are missing?")
        with self.voiceover("Pause and predict. Two differently sized random-feature ridge models have R squared minus forty and plus one percent. Can those values alone rank coefficient norms? Identify the missing feature scaling, penalties and model details."):
            self.play(FadeIn(q))
        self.clear_scene()
