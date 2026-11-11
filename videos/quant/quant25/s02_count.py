from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, ask, fit_right, illustration, load


class Count(VoiceoverScene):
    def construct(self):
        n, z = load("noise"), load("zoo")
        self.card()
        self.maxlaw()
        self.honest()
        self.field()
        self.maxcurve(n)
        self.hurdle(z)
        self.hlz()
        self.histogram(z)

    def card(self):
        c = chapter_card(1, r"Hundreds of factors, and a rising hurdle", r"How high must a $t$-statistic be when "
                         r"everyone is searching?", lit=(2016,), part=PART)
        with self.voiceover("Chapter one. The arithmetic of searching, and the hurdle it implies."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def maxlaw(self):
        rows = [cmath('\\Pr\\big(\\max_{i\\le n}Z_i\\le c\\big)', r"=", r"\Phi(c)^n", font_size=42,
                      colors={'\\Pr\\big(\\max_{i\\le n}Z_i\\le c\\big)': NOISE}),
                cmath('\\mathbb E\\big[\\max_{i\\le n}Z_i\\big]', r"\approx", r"\sqrt{2\ln n}\ \ (\text{slowly from below})",
                      font_size=40, colors={'\\mathbb E\\big[\\max_{i\\le n}Z_i\\big]': BAD})]
        whys = [why('exact formula for independent standard-normal $Z_i$; finite-sample return t statistics instead need their own null distribution'),
                why('so the best of them grows with the number searched, though slowly: about 1.5 for ten, 2.5 for a hundred, 3.2 for a thousand. The largest $t$ measures the search as much as the strategy')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Start with independent standard-normal Z variables. Their maximum has cumulative probability Phi c raised to n exactly. This is a normal reference model, not an exact formula for the finite-sample Student-t draws in the later simulation. <bookmark mark='a'/> For large n the expected normal maximum grows roughly as the square root of two log n, with material finite-n corrections. Typical mean maxima are near one point five for ten, two point five for one hundred and three point two for one thousand. The asymptotic expression is not an accurate small-search formula, and dependence changes the maximum's distribution."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def honest(self):
        rows = [cmath(r"p_{\text{one}}", r"=", r"1 - \Phi(2.9) = 0.0019", font_size=42, colors={r"p_{\text{one}}": GOOD}),
                cmath(r"p_{\text{best of } n}", r"=", r"1 - (1 - p_{\text{one}})^n", font_size=42,
                      colors={r"p_{\text{best of } n}": BAD}),
                cmath(r"n = 200", r"\Rightarrow", r"1 - 0.9981^{200} \approx 0.31", font_size=42, colors={r"n = 200": HURDLE})]
        whys = [why(r"a $t$ of 2.9, alone, has a one-sided $p$-value of about two in a thousand: a strong result, if it was "
                    r"the only test"),
                why(r"but the question that was really asked is how likely the best of $n$ is to reach 2.9: one minus the "
                    r"chance that all $n$ fall short (Sidak's correction, for independent tests)"),
                why(r"for two hundred tries, about 0.31: the 'discovery' is what noise produces about one time in three")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Put a number on it. A t-statistic of two point nine, on its own, has a one-sided p-value of about two in "
            "a thousand. <bookmark mark='a'/> But if it is the best of n tries, the right question is how likely the "
            "best of n is to reach two point nine: one minus the chance that all n fall short. <bookmark mark='b'/> "
            "For two hundred independent tries, about thirty-one percent. The impressive result is what noise "
            "produces about one time in three. The same number on the page means completely different things "
            "depending on a count the page does not show."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def field(self):
        rows = [cmath(r"\Pr(\text{true} \mid \text{significant})", r"=", r"\frac{\pi\,(1 - \beta)}{\pi\,(1 - \beta) + "
                      r"(1 - \pi)\,\alpha}", font_size=40, colors={r"\Pr(\text{true} \mid \text{significant})": GOOD}),
                cmath(r"\pi = 0.1,\ 1 - \beta = 0.5,\ \alpha = 0.05", r"\Rightarrow", r"\frac{0.05}{0.05 + 0.045} \approx 53\%",
                      font_size=36, colors={r"\pi = 0.1,\ 1 - \beta = 0.5,\ \alpha = 0.05": HURDLE})]
        whys = [why(r"a field's view (Ioannidis 2005, for medicine): of all ideas tested, a share $\pi$ are true; a test "
                    r"detects a true one with power $1 - \beta$ and flags a false one with probability $\alpha$"),
                why('if one idea in ten is true and tests have even odds of detecting it, only about half of what clears $t = 2$ is real. Raising the hurdle to 3 cuts $\\alpha$ to 0.003 and, if power stayed fixed, lifts the share toward 95\\%, at some cost in power')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "A fixed diagnostic illustrates base rates. Suppose one hypothesis in ten is non-null, and power at the chosen threshold is one half. <bookmark mark='a'/> With a five-percent null rejection probability, the positive predictive value is about fifty-three percent. If the null rejection probability falls to roughly three in a thousand and power were still one half, it would approach ninety-five percent. In a real test, raising the threshold also reduces power. Neither this assumed base rate nor fixed power is estimated from the zoo, so this arithmetic cannot calibrate a universal t threshold."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def maxcurve(self, n):
        rows = n["rows"]
        ns = np.asarray([r_["n"] for r_ in rows], float)
        g = axes([0, 3.1], [-1.9, 4.2], x_length=7.4, y_length=4.4, xlabel=r"strategies tried, $\log_{10} n$",
                 ylabel=r"best $t$", xticks=[0, 1, 2, 3], yticks=[-1, 0, 1, 2, 3, 4], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        lx = np.log10(ns)
        band_ = band(ax, lx, [r_["p5"] for r_ in rows], [r_["p95"] for r_ in rows], BAD, opacity=0.18)
        mean = curve(ax, lx, [r_["mean"] for r_ in rows], BAD, stroke_width=3)
        h = DashedLine(ax.c2p(0, 1.96), ax.c2p(3.1, 1.96), color=HURDLE, stroke_width=2)
        hl = label(r"$t = 1.96$", font_size=15, color=HURDLE).next_to(ax.c2p(0, 1.96), UR, buff=0.05)
        a = n["abs200"]
        side = VGroup(
            legend([(BAD, r"the best $t$ among $n$ noise strategies"), (HURDLE, r"the textbook hurdle")], font_size=16),
            MathTex(rf"n = 200:\ \mathbb{{E}}[\max t] \approx {rows[6]['mean']:.2f}", font_size=24),
            MathTex(rf"\text{{two-sided}}:\ \mathbb{{E}}[\max |t|] \approx {a['mean']:.2f}", font_size=22),
            wrapped_label('independent Student-$t$ draws with 239 degrees of freedom (240-month normal-return reference); band from the 5th to the 95th percentile. Search raises the noise maximum under the zero-premium null', 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Simulated, with twenty years of monthly data each. <bookmark mark='a'/> With ten tries the best noise "
            "strategy has a t near one and a half; with fifty, above two; with two hundred, near two point eight, or "
            "three if you are willing to flip the sign of a losing strategy and call it a short. The shaded band "
            "shows the luck around that: with two hundred tries, a best t-statistic of three and a half happens one "
            "time in twenty."
        ) as vo:
            self.play(FadeIn(g), Create(h), FadeIn(hl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(band_), Create(mean), FadeIn(side[1:]), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def hurdle(self, z):
        yrs, cnt, hd = np.asarray(z["years"]), np.asarray(z["count"]), np.asarray(z["hurdle"])
        g = axes([1970, 2017], [1.5, 4.0], x_length=8.0, y_length=4.4, xlabel=r"year",
                 ylabel=r"Bonferroni hurdle for the zoo so far", xticks=[1970, 1980, 1990, 2000, 2010],
                 yticks=[2.0, 2.5, 3.0, 3.5, 4.0], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, yrs, hd, HURDLE, stroke_width=3)
        three = DashedLine(ax.c2p(1970, 3.0), ax.c2p(2017, 3.0), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"1980:\ {hd[10]:.2f}\ \ (n = {cnt[10]})", font_size=24),
            MathTex(rf"2000:\ {hd[30]:.2f}\ \ (n = {cnt[30]})", font_size=24),
            MathTex(rf"2016:\ {hd[-1]:.2f}\ \ (n = {cnt[-1]})", font_size=24, color=HURDLE),
            wrapped_label(r"the two-sided $t$ that keeps the chance of any false discovery below 5\% when every "
                          r"predictor published so far is counted as a test. A lower bound on the true hurdle: "
                          r"unpublished tries count too", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Count each predictor published so far as one member of a declared family. Under valid standard-normal null calibration, the two-sided Bonferroni hurdle rises as that count grows. <bookmark mark='a'/> The union-bound guarantee permits arbitrary dependence; it does not fix invalid p-values. The count in this collection omits unpublished choices, and dependence-aware or selective procedures need their own assumptions. These are illustrative normal critical values, not certified finite-sample Student-t thresholds for the observed returns."
        ) as vo:
            self.play(FadeIn(g), Create(three))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def hlz(self):
        cards = VGroup(
            desk_question(r"Harvey, Liu and Zhu (2016)", r"316 published factors by 2012; adjusting for multiple tests, "
                          r"correlation among them and an estimate of unpublished tries, a new factor should need "
                          r"$t > 3.0$, not 2", width=12.0, font_size=20),
            desk_question(r"why not higher?", 'Bonferroni controls any family error under arbitrary dependence, provided marginal p-values are valid. It can be conservative for correlated tests; FDR is a different error criterion', width=12.0,
                          font_size=20),
            desk_question(r"Harvey (2017)", r"in his presidential address: the incentives to publish significant "
                          r"results, and to search until one appears, are the field's real problem", width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Harvey, Liu and Zhu estimated the scale of the published and unpublished search. <bookmark mark='a'/> Their count of three hundred and sixteen published factors by 2012 motivated a hurdle above three under their modelling choices. It is not a universal calibrated threshold for every signal. <bookmark mark='b'/> Bonferroni does not require independent tests: with valid marginal p-values it controls any family error under arbitrary dependence. Correlation can make it conservative. False discovery control answers a different question and has its own assumptions. <bookmark mark='c'/> Harvey's presidential address also emphasised incentives that reward significant results and repeated search."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def histogram(self, z):
        t = np.array([r_["t_in"] for r_ in z["recs"]])
        edges = np.arange(-2, 15.5, 0.5)
        h = np.histogram(t, edges)[0]
        g = axes([-2, 15.0], [0, max(h) * 1.15], x_length=8.4, y_length=4.2, xlabel=r"$t$ in the original sample, "
                 r"reproduced", ylabel=r"predictors", xticks=[0, 3, 6, 9, 12, 15],
                 yticks=[0, 10, 20, 30], font_size=13).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, v in enumerate(h):
            x0, x1 = edges[i], edges[i + 1]
            col = NOISE if x1 <= 1.96 else (HURDLE if x1 <= 3.0 else TRUE)
            bars.add(Rectangle(width=ax.c2p(x1, 0)[0] - ax.c2p(x0, 0)[0], height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001),
                               stroke_width=0.5, stroke_color=BLACK, fill_color=col, fill_opacity=0.85).move_to(
                [(ax.c2p(x0, 0)[0] + ax.c2p(x1, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, v)[1]) / 2, 0]))
        side = VGroup(
            MathTex(rf"t > 1.96:\ {100 * z['share_t2']:.0f}\%", font_size=24, color=HURDLE),
            MathTex(rf"t > 3:\ {100 * z['share_t3']:.0f}\%", font_size=24, color=TRUE),
            wrapped_label(r"each predictor's long--short return over the sample its own paper used, rebuilt by Chen and "
                          r"Zimmermann. A pile-up just above two is the fingerprint of selection: results that clear the "
                          r"bar get written up", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is the zoo against those hurdles. Each predictor's t-statistic in the sample its own paper used, "
            "rebuilt from the data. <bookmark mark='a'/> Eighty-seven percent clear two; fifty-eight percent clear "
            "three. A t of three is not a high bar for the zoo, because the zoo was assembled by clearing bars: we see "
            "the papers that found something. The question for the rest of this part is how much of that something "
            "survives."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03), FadeIn(side), run_time=2.5)
        self.add(illustration(r"Open Source Asset Pricing 2024.10: long--short returns, original papers' portfolios"))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"you test 200 strategies and report the best, with $t = 2.9$. What is its $p$-value, honestly computed? "
                r"And what would you need to know to compute it?")
        with self.voiceover("You test two hundred strategies and report the best, with a t-statistic of two point nine. "
                            "What is its p-value, honestly computed, and what would you need to know to compute it?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
