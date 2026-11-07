from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, CASH, GOOD, IV, OPT, PART, SPOT, load, axes, data_range, pause_card

MODELS = ["LV", "Heston", "Bates", "VG"]
COLS = {"LV": QC.SPOT, "Heston": QC.OPTION, "Bates": QC.GAIN, "VG": QC.IMPLIED}
NAMES = {"LV": r"local vol", "Heston": r"Heston", "Bates": r"Bates", "VG": r"variance gamma"}
CEIL, FLOOR = QC.IDEA, GREY_B


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
        with self.voiceover('For the researcher: can vanilla prices constrain a one-touch without choosing volatility dynamics? Yes, once we state the contract and martingale assumptions. We will derive a pathwise super-hedge and a sharp upper bound in a continuous martingale class. A simple terminal digital also gives a lower bound, whose sharpness we do not assert.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def superhedge(self):
        rows = [cmath(r"\frac{(K - S_T)^+}{K - B}", r"+", r"\mathbf 1_{\{\tau \le T\}}\,\frac{S_T - S_\tau}{K - B}", font_size=32,
                      colors={r"\frac{(K - S_T)^+}{K - B}": OPT}),
                cmath(r"\text{touched}:", r"\ \ge\ ", r"\frac{(K - S_T)^+ + S_T - B}{K - B}\ \ge\ \frac{K - B}{K - B} = 1",
                      font_size=30, colors={r"\text{touched}:": BAD}),
                cmath(r"\text{not touched}:", r"\ \ge\ ", r"0", font_size=30, colors={r"\text{not touched}:": GOOD})]
        whys = [why(r"a down one-touch at $B < S_0$ pays 1 if the price ever reaches $B$. Hold $1/(K - B)$ puts struck at "
                    r"some $K > B$; at the first touch $\tau$, buy $1/(K - B)$ forwards, with delivery price $S_\tau$; assume zero rates/dividends and a nonnegative UI price martingale"),
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
        rows = [cmath(r"\operatorname{OT}(B)", r"\le", r"\inf_{K > B}\ \frac{P(K)}{K - B}", font_size=34,
                      colors={r"\operatorname{OT}(B)": CEIL}),
                cmath(r"\operatorname{OT}(B)", r"\ge", r"\Pr\nolimits^{\mathbb Q}(S_T \le B) = \partial_K^{+} P(K)\big|_{K = B}",
                      font_size=32, colors={r"\operatorname{OT}(B)": FLOOR})]
        whys = [why(r"the cheapest such hedge: an arbitrage bound from the put prices alone. The minimizing strike "
                    r"$K^*$ balances the put's price against its distance from the barrier"),
                why(r"a path that ends below $B$ must have touched it: the digital put is a floor, again read from the "
                    r"puts (Breeden and Litzenberger)")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.3, buff=0.55, edge=6.9)
        thm = theorem_card(r"Robust bounds for barrier options", wrapped_label(
            r"given an integrable nonnegative terminal law of mean $S_0$, and its full continuum of vanilla prices at one maturity, the upper bound is sharp in a class of UI martingales with "
            r"continuous paths, consistent with every put, whose one-touch costs the infimum of $P(K)/(K-B)$; it runs "
            r"the price to the extreme its terminal law allows (an Az\'ema--Yor construction)", 10.6, 20, GREY_A),
            who=r"Hobson (1998); Brown, Hobson and Rogers (2001), \textit{Mathematical Finance} 11", width=11.6,
            font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Assume zero rates and dividends, frictionless trading, and a nonnegative uniformly integrable price martingale starting above B. The contract pays one at maturity if the barrier is reached. <bookmark mark='a'/> Every strike K above B gives an upper price bound from its put; take the infimum over available strikes. <bookmark mark='b'/> Ending at or below B implies a prior touch, so the terminal digital is a lower bound. At an atom, the right derivative of the put price includes equality. <bookmark mark='c'/> For a full compatible terminal law of mean equal to the initial spot, the classical embedding construction gives a sharp upper bound in the continuous martingale class. This is an upper-attainment theorem; it does not establish that the simple digital floor is sharp or that every price in the displayed band is attainable."
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
        up = curve(ax, B, h["upper"], CEIL, stroke_width=3.5)
        lo = curve(ax, B, h["digital"], FLOOR, stroke_width=3)
        models = VGroup(*[curve(ax, B, t["models"][m]["touch"], COLS[m], stroke_width=2.5) for m in MODELS])
        bsc = curve(ax, B, h["bs"], WHITE, stroke_width=2)
        leg = legend([(CEIL, r"upper bound, $\min_K P(K)/(K - B)$"), (FLOOR, r"lower bound, the digital put")]
                     + [(COLS[m], NAMES[m]) for m in MODELS] + [(WHITE, r"Black--Scholes at the ATM vol")],
                     font_size=15).to_edge(RIGHT, buff=0.25).shift(UP * 1.2)
        fit_right(leg)
        j = int(np.argmin(np.abs(B - 0.8)))
        side = wrapped_label(rf"bounds from the Heston fit's own empirical puts; the models have different marginals. Fitted "
                             rf"to one Surface; model prices from 20{{,}}000 daily paths each. At $B = 0.8$: band "
                             rf"[{h['digital'][j]:.2f}, {h['upper'][j]:.2f}], models "
                             rf"{min(t['models'][m]['touch'][j] for m in MODELS):.2f}--"
                             rf"{max(t['models'][m]['touch'][j] for m in MODELS):.2f}", 3.3, 13, GREY_A).next_to(
            leg, DOWN, buff=0.25)
        fit_right(side)
        lo8 = min(t["models"][m]["touch"][j] for m in MODELS)
        hi8 = max(t["models"][m]["touch"][j] for m in MODELS)
        with self.voiceover(
            f"Now separate the theorem from the illustration. These floor and ceiling estimates use the Heston simulation's own terminal put prices, minimized on a finite strike grid. <bookmark mark='a'/> They are not market-wide certified bounds for every approximately fitted model. <bookmark mark='b'/> The four daily-monitoring model prices are shown for comparison. At B 0.8 they range from {lo8:.2f} to {hi8:.2f}. <bookmark mark='c'/> The Heston reference floor and grid ceiling are {h['digital'][j]:.2f} and {h['upper'][j]:.2f}. The other models have different terminal laws, so their inclusion in this reference band is an observed numerical result, not a shared-marginal certificate. <bookmark mark='d'/> The white Black-Scholes curve matches only Heston's ATM volatility. Its different smile and monitoring convention also matter. Close model prices do not prove a uniquely identified market price."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(up), Create(lo), FadeIn(leg[0]), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in models], lag_ratio=0.3), FadeIn(leg[2:6]), run_time=2)
            vo.wait_until("c")
            self.play(Indicate(up, color=CEIL), Indicate(lo, color=FLOOR))
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
        for x0, c in zip(e[:-1], hst / 20000):
            if c <= 0:
                continue
            p0, p1 = ax.c2p(x0, 0), ax.c2p(x0 + w, c)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=GOOD,
                               fill_opacity=0.8).move_to((p0 + p1) / 2))
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1.0), color=BAD, stroke_width=2)
        stats = VGroup(MathTex(rf"K^* = {sh['K']:.3f},\ \ \text{{cost}} = {sh['cost']:.3f}", font_size=26),
                       MathTex(rf"\text{{one-touch}} = {sh['touch']:.3f}", font_size=26),
                       MathTex(rf"\min = {sh['surplus_min']:.3f},\ \ \text{{mean}} = {sh['surplus_mean']:.3f}", font_size=26,
                               color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        fit_right(stats)
        side = wrapped_label(r"the Heston fit's 20{,}000 daily paths, barrier 0.8; forwards bought at the first close at or "
                             r"below the barrier. Histogram shares use all 20,000 paths; values outside the window are omitted. Finite-sample forward gains make mean surplus differ from cost minus touch probability; "
                             r"this is a numerical illustration", 3.3, 14, GREY_A).next_to(stats, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"Check the super-hedge on the Heston reference sample at B 0.8. <bookmark mark='a'/> The selected put strike is {sh['K']:.2f}; forwards begin at the first sampled close at or below B. Algebra ensures the terminal hedge dominates this daily-observation touch payoff, even if that close overshoots below B. <bookmark mark='b'/> All twenty thousand sampled surpluses are nonnegative. Their mean is {sh['surplus_mean']:.3f}; the separately reported put cost minus touch estimate is {sh['cost'] - sh['touch']:.3f}. The difference is the sample mean forward gain, not an exact pricing identity. Under the stated true-martingale conditions that gain has zero expectation. Histogram shares divide by all twenty thousand paths; any surplus outside the plotted window is omitted, not renormalized."
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
        head = VGroup(label(r"barrier", font_size=18, color=GREY_B), label(r"floor", font_size=20, color=FLOOR),
                      *[label(NAMES[m], font_size=18, color=COLS[m]) for m in ("LV", "Heston", "VG")],
                      label(r"ceiling", font_size=20, color=CEIL))
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
            "Here are three barrier levels. <bookmark mark='a'/> The floor and grid ceiling belong to the Heston empirical terminal law, while each model's daily touch estimate belongs to its own law. Their approximate calibrations are different. <bookmark mark='b'/> The jump model also happens to lie within this reference band. The pathwise hedge remains valid after a downward gap if the first crossing can be traded at its observed price. Pricing the dynamic gain at zero still requires martingale and admissibility conditions. Continuous paths enter the stated sharp-attainment theorem; we do not claim this daily Monte Carlo calculation verifies that theorem's exact hypotheses."
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
            desk_question(r"implementation: add more information", r"adding the smiles at intermediate dates, or the "
                          r"prices of other barriers, narrows the band; computing the sharp bounds is a multi-marginal "
                          r"transport problem (Part 9); our one-maturity strike grid does not solve it", width=12.4, font_size=18),
            desk_question(r"implementation: specify an admissible class", r"the extreme model is unrealistic; bounds over models with "
                          r"plausible paths (bounded volatility, Chapter 13's uncertain volatility) are tighter but "
                          r"model-dependent again; its choice needs a stated purpose and validation", width=12.4, font_size=18),
            desk_question(r"implementation: match observation and trading", r"match the information set, attainable trades and payoff for barriers "
                          r"watched only at the close; our current grid is an illustration, not a certified sharp solver", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        head = label(r"Implementation questions", font_size=30).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Three implementation questions remain for this project. <bookmark mark='a'/> Adding intermediate smiles or other option prices requires compatible constraints; our one-maturity calculation does not solve that enlarged transport problem. <bookmark mark='b'/> A bounded-volatility or other restricted class changes the bounds. Its assumptions must be specified and checked for the use at hand. <bookmark mark='c'/> Observation times, gaps and executable trading times must match the contract. A stronger next implementation would certify numerical and calibration error. These are gaps in our implementation, not claims that the corresponding research literatures are unsolved."
        ) as vo:
            self.play(FadeIn(head))
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
        self.wait(3)
        answer = MathTex(r"OT_{\uparrow}(B)\le\inf_{K<B}\frac{C(K)}{B-K}", font_size=38, color=GOOD)
        reason = wrapped_label(r"hold calls; sell forwards at the first upward crossing. $S_\tau\ge B$ makes the terminal hedge at least one on a hit. Zero rates/dividends and a UI martingale justify its price.", 10.8, 22, GREY_A).next_to(answer, DOWN, buff=0.4)
        self.play(FadeOut(q), FadeIn(answer), FadeIn(reason))
        self.wait(6)
        self.clear_scene()
