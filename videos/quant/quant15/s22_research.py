from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, CASH, GOOD, IV, OPT, PART, SPOT, load

MODELS = ["LV", "Heston", "Bates", "VG"]
COLS = {"LV": QC.SPOT, "Heston": QC.OPTION, "Bates": QC.GAIN, "VG": QC.IMPLIED}
NAMES = {"LV": r"local vol", "Heston": r"Heston", "Bates": r"Bates", "VG": r"variance gamma"}
UP, LO = QC.IDEA, GREY_B


class Research(VoiceoverScene):
    def construct(self):
        t = load("touch_bounds")
        self.card()
        self.superhedge()
        self.bounds()
        self.band(t)
        self.pathwise(t)
        self.table(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"What the vanillas alone say about a one-touch", r"Without choosing a model, how high or low "
                          r"can a barrier option's price be?", part=PART)
        with self.voiceover("For the researcher: Chapter 14 showed four models that agree on every vanilla and still "
                            "disagree on the exotics. How far can that disagreement go? For the one-touch there is an "
                            "exact answer, a hedge that works in every model, and a bound that some model attains."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def superhedge(self):
        rows = [cmath(r"\frac{(K - S_T)^+}{K - B}", r"+", r"\mathbf 1_{\{\tau \le T\}}\,\frac{S_T - S_\tau}{K - B}", font_size=32,
                      colors={r"\frac{(K - S_T)^+}{K - B}": OPT}),
                cmath(r"\text{touched}:", r"\ \ge\ ", r"\frac{(K - S_T)^+ + S_T - B}{K - B}\ \ge\ \frac{K - B}{K - B} = 1",
                      font_size=30, colors={r"\text{touched}:": BAD}),
                cmath(r"\text{not touched}:", r"\ \ge\ ", r"0", font_size=30, colors={r"\text{not touched}:": GOOD})]
        whys = [why(r"a down one-touch at $B < S_0$ pays 1 if the price ever reaches $B$. Hold $1/(K - B)$ puts struck at "
                    r"some $K > B$; at the first touch $\tau$, buy $1/(K - B)$ forwards, which cost nothing at zero rates"),
                why(r"with continuous paths $S_\tau = B$; then $(K - x)^+ + x - B \ge K - B$ for every $x$: the hedge pays at "
                    r"least the one-touch (and a gap below $B$ only helps, since the forwards are then bought cheaper)"),
                why(r"untouched, the puts are worth something or nothing, and the one-touch pays nothing: the hedge "
                    r"dominates on every path, in every model")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Here is the hedge. A down one-touch pays one if the price ever reaches B. <bookmark mark='a'/> Hold one "
            "over K minus B puts at any strike K above B, and at the first touch, buy the same number of forwards; at "
            "zero rates they cost nothing. <bookmark mark='b'/> If the barrier is touched, the puts plus the forwards "
            "pay at least K minus B over K minus B: one. A gap through the barrier only helps, because the forwards "
            "are then bought cheaper. <bookmark mark='c'/> If it is never touched, the hedge is worth something or "
            "nothing, and the one-touch nothing. It dominates the one-touch on every path, in every model."
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

    def bounds(self):
        rows = [cmath(r"\operatorname{OT}(B)", r"\le", r"\min_{K > B}\ \frac{P(K)}{K - B}", font_size=34,
                      colors={r"\operatorname{OT}(B)": UP}),
                cmath(r"\operatorname{OT}(B)", r"\ge", r"\Pr\nolimits^{\mathbb Q}(S_T \le B) = \partial_K P(K)\big|_{K = B}",
                      font_size=32, colors={r"\operatorname{OT}(B)": LO})]
        whys = [why(r"the cheapest such hedge: an arbitrage bound from the put prices alone. The minimizing strike "
                    r"$K^*$ balances the put's price against its distance from the barrier"),
                why(r"a path that ends below $B$ must have touched it: the digital put is a floor, again read from the "
                    r"puts (Breeden and Litzenberger)")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.3, buff=0.55, edge=6.9)
        thm = theorem_card(r"Robust bounds for barrier options", wrapped_label(
            r"given the prices of vanilla options at the maturity, the upper bound is sharp: there is a model with "
            r"continuous paths, consistent with every put, whose one-touch costs exactly $\min_K P(K)/(K - B)$; it runs "
            r"the price to the extreme its terminal law allows (an Az\'ema--Yor construction)", 10.6, 20, GREY_A),
            who=r"Hobson (1998); Brown, Hobson and Rogers (2001), \textit{Mathematical Finance} 11", width=11.6,
            font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "So the one-touch is worth at most the cheapest such hedge. <bookmark mark='a'/> Minimize the cost over "
            "the strike: an arbitrage bound from the put prices alone. <bookmark mark='b'/> And a path that ends below "
            "the barrier must have touched it, so the digital put, also read from the puts, is a floor. "
            "<bookmark mark='c'/> The upper bound is sharp: David Hobson showed in 1998, and Haydyn Brown, Hobson and "
            "Chris Rogers in 2001 for barrier options generally, that some model consistent with every put attains it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(thm))
        self.wait(0.5)
        self.clear_scene()

    def band(self, t):
        B = np.asarray(t["B"], float)
        h = t["models"]["Heston"]
        g = axes([0.58, 0.97], [0, 1], x_length=8.2, y_length=4.4, xlabel=r"barrier $B$ (spot 1)",
                 ylabel=rf"price of a {t['days']}-day down one-touch", xticks=[0.6, 0.7, 0.8, 0.9],
                 yticks=[0, 0.25, 0.5, 0.75, 1], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        up = curve(ax, B, h["upper"], UP, stroke_width=3.5)
        lo = curve(ax, B, h["digital"], LO, stroke_width=3)
        models = VGroup(*[curve(ax, B, t["models"][m]["touch"], COLS[m], stroke_width=2.5) for m in MODELS])
        bsc = curve(ax, B, h["bs"], WHITE, stroke_width=2)
        leg = legend([(UP, r"upper bound, $\min_K P(K)/(K - B)$"), (LO, r"lower bound, the digital put")]
                     + [(COLS[m], NAMES[m]) for m in MODELS] + [(WHITE, r"Black--Scholes at the ATM vol")],
                     font_size=15).to_edge(RIGHT, buff=0.25).shift(UP * 1.2)
        fit_right(leg)
        j = int(np.argmin(np.abs(B - 0.8)))
        side = wrapped_label(rf"bounds from the Heston fit's own puts (the four models' puts nearly coincide, all fitted "
                             rf"to the Surface); model prices from 20{{,}}000 daily paths each. At $B = 0.8$: band "
                             rf"[{h['digital'][j]:.2f}, {h['upper'][j]:.2f}], models "
                             rf"{min(t['models'][m]['touch'][j] for m in MODELS):.2f}--"
                             rf"{max(t['models'][m]['touch'][j] for m in MODELS):.2f}", 3.3, 13, GREY_A).next_to(
            leg, DOWN, buff=0.25)
        fit_right(side)
        with self.voiceover(
            "Now on the Bitcoin Surface, with the four models of Chapter 14, each fitted to the same smile. "
            "<bookmark mark='a'/> The upper bound from the puts, and the digital floor: every model must price the "
            "one-touch between them. <bookmark mark='b'/> The four models: local volatility, Heston, Bates and "
            f"variance gamma. At a barrier of point eight they agree to within two cents, between "
            f"{min(t['models'][m]['touch'][j] for m in MODELS):.2f} and {max(t['models'][m]['touch'][j] for m in MODELS):.2f}. "
            f"<bookmark mark='c'/> But the vanillas alone allow anything from {h['digital'][j]:.2f} to {h['upper'][j]:.2f}. "
            "The models' agreement is a property of the models, not of the market. <bookmark mark='d'/> And "
            "Black-Scholes at the at-the-money volatility, ignoring the smile, prices near barriers higher than any "
            "of them, and far barriers much lower: it has no fat left tail."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(up), Create(lo), FadeIn(leg[0]), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in models], lag_ratio=0.3), FadeIn(leg[2:6]), run_time=2)
            vo.wait_until("c")
            self.play(Indicate(up, color=UP), Indicate(lo, color=LO))
            vo.wait_until("d")
            self.play(Create(bsc), FadeIn(leg[6]))
        self.wait(0.4)
        self.clear_scene()

    def pathwise(self, t):
        sh = t["superhedge"]
        e = np.asarray(sh["hist_edges"])
        hst = np.asarray(sh["hist"], float)
        g = axes([-0.2, 1.8], [0, 1.0], x_length=8.0, y_length=4.0, xlabel=r"hedge minus one-touch payoff, per path",
                 ylabel=r"share of paths", xticks=[0, 0.5, 1.0, 1.5], yticks=[0, 0.5, 1.0], font_size=15).move_to(
            LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        w = e[1] - e[0]
        bars = VGroup()
        for x0, c in zip(e[:-1], hst / hst.sum()):
            if c <= 0:
                continue
            p0, p1 = ax.c2p(x0, 0), ax.c2p(x0 + w, max(c, 0.004))
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=GOOD,
                               fill_opacity=0.8).move_to((p0 + p1) / 2))
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1.0), color=BAD, stroke_width=2)
        stats = VGroup(MathTex(rf"K^* = {sh['K']:.3f},\ \ \text{{cost}} = {sh['cost']:.3f}", font_size=26),
                       MathTex(rf"\text{{one-touch}} = {sh['touch']:.3f}", font_size=26),
                       MathTex(rf"\min = {sh['surplus_min']:.3f},\ \ \text{{mean}} = {sh['surplus_mean']:.3f}", font_size=26,
                               color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        fit_right(stats)
        side = wrapped_label(r"the Heston fit's 20{,}000 daily paths, barrier 0.8; forwards bought at the first close at or "
                             r"below the barrier. The mean surplus is the bound minus the model's price: the cost of not "
                             r"knowing the model", 3.3, 14, GREY_A).next_to(stats, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Check the hedge path by path, on the Heston fit's paths, at a barrier of point eight. <bookmark mark='a'/> "
            f"Buy the cheapest put, struck at {sh['K']:.2f}, and the forwards at the first close at or below the "
            "barrier. Subtract what the one-touch pays. <bookmark mark='b'/> On not one of twenty thousand paths is the "
            "result negative: the minimum is zero. The mean is what the hedge costs above the model's own price: the "
            "price of not knowing the model."
        ) as vo:
            self.play(FadeIn(g), FadeIn(stats[0]), FadeIn(stats[1]), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.03), Create(zero))
            vo.wait_until("b")
            self.play(FadeIn(stats[2]))
        self.wait(0.4)
        self.clear_scene()

    def table(self, t):
        B = np.asarray(t["B"], float)
        picks = [int(np.argmin(np.abs(B - b))) for b in (0.7, 0.8, 0.9)]
        h = t["models"]["Heston"]
        hx = [-4.8, -2.6, -0.6, 1.4, 3.4, 5.5]
        head = VGroup(label(r"barrier", font_size=18, color=GREY_B), label(r"floor", font_size=20, color=LO),
                      *[label(NAMES[m], font_size=18, color=COLS[m]) for m in ("LV", "Heston", "VG")],
                      label(r"ceiling", font_size=20, color=UP))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(MathTex(rf"{B[i]:.2f}", font_size=26),
                                                 MathTex(rf"{h['digital'][i]:.3f}", font_size=26),
                                                 *[MathTex(rf"{t['models'][m]['touch'][i]:.3f}", font_size=26)
                                                   for m in ("LV", "Heston", "VG")],
                                                 MathTex(rf"{h['upper'][i]:.3f}", font_size=26)) for i in picks]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.5 - 0.75 * j, 0])
            tab.add(row)
        vg = t["models"]["VG"]
        foot = wrapped_label(r"floor and ceiling from the Heston fit's puts; prices from 20{,}000 daily paths. The bounds "
                             r"hold with jumps too: after a gap through the barrier the forwards are bought below $B$, "
                             r"which only adds to the hedge; continuous paths are needed only for the model that attains "
                             r"the ceiling", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "In numbers, at three barriers. <bookmark mark='a'/> The models sit close together, inside a band "
            "almost as wide as the price itself. <bookmark mark='b'/> And variance gamma, which moves only by jumps, "
            "is inside too. The hedge never needed continuous paths: after a gap through the barrier, the forwards "
            "are bought cheaper, so the hedger gains. Continuity matters only for the model that attains the bound."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: bounds with more information", r"adding the smiles at intermediate dates, or the "
                          r"prices of other barriers, narrows the band; computing the sharp bounds is a multi-marginal "
                          r"transport problem (Part 9), tractable only in special cases", width=12.4, font_size=18),
            desk_question(r"open: bounds a desk can use", r"the extreme model is unrealistic; bounds over models with "
                          r"plausible paths (bounded volatility, Chapter 13's uncertain volatility) are tighter but "
                          r"model-dependent again, and how to choose the class is unsettled", width=12.4, font_size=18),
            desk_question(r"open: jumps and discrete monitoring", r"robust bounds for gapping prices and for barriers "
                          r"watched only at the close are known only partially", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Adding the smiles at intermediate dates, or the prices of "
            "other barriers, narrows the band; the sharp bounds become a multi-marginal transport problem, Part 9's "
            "tool, tractable only in special cases. <bookmark mark='b'/> The extreme model is unrealistic. Bounds over "
            "models with plausible paths, such as Chapter 13's uncertain volatility, are tighter but depend on a model "
            "class again, and how to choose it is unsettled. <bookmark mark='c'/> And for gapping prices, and barriers "
            "watched only at the close, robust bounds are known only in part."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"write the super-hedge for an up one-touch at $B > S_0$ using calls. What bound does it give, and "
                       r"why does an upward gap through $B$ help the hedger rather than hurt?")
        with self.voiceover(
            "Pause and predict. Write the super-hedge for an up one-touch, using calls. What bound does it give? And "
            "why does an upward gap through the barrier help the hedger, rather than hurt?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
