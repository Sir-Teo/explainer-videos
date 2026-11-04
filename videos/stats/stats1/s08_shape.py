from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403


class Shape(VoiceoverScene):
    def construct(self):
        self.card()
        self.skew()
        self.unstable()
        self.logscale()
        self.pareto()

    def card(self):
        card = chapter_card(7, r"Shape: skew, tails and power laws", r"How lopsided, and how heavy at the edges?",
                            lit=(), part=PART)
        with self.voiceover("Chapter seven. Shape: skew, tails and power laws."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def skew(self):
        sh, w = load("shape"), load("world")
        he, hh = np.asarray(w["height_hist_edges"]), np.asarray(w["height_hist"])
        H = axes([140, 205], [0, hh.max() * 1.2], x_length=5.4, y_length=2.8, xlabel=r"height (cm)",
                 xticks=[150, 170, 190], center=[-3.5, -0.9, 0])
        hb = hist_bars(H.ax, he, hh, color=S.TRUTH, opacity=0.7, stroke_width=0)
        lh = np.asarray(sh["lin_hist"])
        I = axes([0, 300], [0, lh.max() * 1.2], x_length=5.4, y_length=2.8, xlabel=r"income (thousands)",
                 xticks=[0, 100, 200, 300], center=[3.5, -0.9, 0])
        ib = hist_bars(I.ax, np.linspace(0, 300, 61), lh, color=S.TRUTH, opacity=0.7, stroke_width=0)
        g1 = cmath(r"\text{skewness}", r"=", r"\frac1n \sum_i z_i^3", r",\quad", r"z_i = \frac{x_i - \bar x}{s}",
                   font_size=36).to_edge(UP, buff=0.45)
        k4 = cmath(r"\text{kurtosis}", r"=", r"\frac1n \sum_i z_i^4 - 3", font_size=36).next_to(g1, DOWN, buff=0.3)
        hs = MathTex(rf"\text{{skew}} = {sh['height']['skew']:.2f}", font_size=32, color=S.TRUTH)
        hs.next_to(H, UP, buff=0.2)
        hk = MathTex(rf"\text{{kurtosis}} = {sh['height']['kurt']:.2f}", font_size=28, color=GREY_A)
        hk.next_to(hs, DOWN, buff=0.1)
        is_ = MathTex(rf"\text{{skew}} = {sh['income']['skew']:.0f}", font_size=32, color=S.TRUTH)
        is_.next_to(I, UP, buff=0.2)
        ik = MathTex(rf"\text{{kurtosis}} = {fmt_int(round(sh['income']['kurt']))}", font_size=28, color=GREY_A)
        ik.next_to(is_, DOWN, buff=0.1)
        tag = simulated_tag(r"simulated: all adults of the World")
        with self.voiceover(
            "Centre and spread are two numbers. The rest of a distribution's shape takes more. "
            "<bookmark mark='a'/> Standardize every value: subtract the mean and divide by the standard deviation, "
            "so it's measured in standard deviations from the centre. Then average the cubes. Cubes keep their "
            "sign, so deviations to the right and left cancel when the distribution is symmetric, and don't when "
            "one side stretches further. That average is the skewness. <bookmark mark='b'/> The World's heights: "
            f"skewness {sh['height']['skew']:.2f}, very nearly symmetric. <bookmark mark='c'/> Its incomes: "
            f"{sh['income']['skew']:.0f}. A long tail to the right. <bookmark mark='d'/> Average the fourth powers "
            "instead, and subtract three, and you get the excess kurtosis. For years textbooks said it measured "
            "peakedness. It doesn't: fourth powers are dominated by the most extreme values, so kurtosis "
            "measures the tails, as Westfall argued in 2014. <bookmark mark='e'/> Heights: "
            f"{sh['height']['kurt']:.2f}, lighter tails than a bell curve, because mixing men and women flattens "
            f"the top. Incomes: {money(round(sh['income']['kurt']))}."
        ) as vo:
            self.play(FadeIn(H), FadeIn(hb), FadeIn(I), FadeIn(ib), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(g1))
            vo.wait_until("b")
            self.play(FadeIn(hs))
            vo.wait_until("c")
            self.play(FadeIn(is_))
            vo.wait_until("d")
            self.play(Write(k4))
            vo.wait_until("e")
            self.play(FadeIn(hk), FadeIn(ik))
        self.clear_scene()

    def unstable(self):
        sh = load("shape")
        sizes, sk = sh["sizes"], sh["skew_n"]
        bars = LiveBars([0] * len(sizes), max_value=max(sk) * 1.15, height=3.6, bar_width=1.1, gap=0.9,
                        colors=[S.EST] * len(sizes), labels=[rf"$n = {fmt_int(n)}$" for n in sizes], label_font=24,
                        show_values=True, digits=1, value_font=26).place(-1.8, x=-3.1)
        head = label(r"the sample skewness of incomes, \ as the sample grows", font_size=28,
                     color=GREY_A).to_edge(UP, buff=0.5)
        one = MathTex(rf"z_{{\max}} = {sh['z_max']:.0f}", r"\qquad", rf"\frac{{z_{{\max}}^3}}{{n}} = {sh['top_share']:.1f}",
                      font_size=34, color=S.RESID).move_to([3.9, 1.6, 0])
        expl = wrapped_label(rf"one adult, \ out of {fmt_int(int(load('world')['n_adults']))}, \ supplies "
                             rf"{sh['top_share']:.0f} of the {sh['income']['skew']:.0f}", 4.6, font_size=26,
                             color=S.RESID).next_to(one, DOWN, buff=0.3)
        thm = definition_card(r"Pareto tail, $\alpha = 2.1$", r"$P(Y > y) \propto y^{-\alpha}$: \ moments of order "
                              r"$\ge \alpha$ are infinite, \ so the skewness and kurtosis of the population "
                              r"they come from do not exist", color=S.ACCENT, width=4.8,
                              font_size=22).move_to([4.2, -1.5, 0])
        with self.voiceover(
            "Those last numbers deserve suspicion. <bookmark mark='a'/> Compute the skewness of incomes on a "
            f"thousand people, then ten thousand, then a hundred thousand, then everyone. It doesn't settle: "
            f"{sk[0]:.1f}, {sk[1]:.1f}, {sk[2]:.1f}, {sk[3]:.1f}. <bookmark mark='b'/> The reason is one person. The "
            f"richest adult in the World is {sh['z_max']:.0f} standard deviations above the mean. Cube that, divide "
            f"by the number of adults, and that single term is {sh['top_share']:.1f}: more than half of the whole "
            "skewness comes from one human being. <bookmark mark='c'/> And it's not bad luck. The World's top incomes "
            "follow a power law with exponent two point one, and for such a tail the third and fourth moments of "
            "the distribution they're drawn from are infinite. The sample skewness is estimating something that "
            "doesn't exist, so it can only jump around, dominated by whoever is richest in the sample. A summary is "
            "only as good as the thing it summarizes is real."
        ) as vo:
            self.play(FadeIn(bars), FadeIn(head))
            vo.wait_until("a")
            for i, v in enumerate(sk):
                self.play(bars.trackers[i].animate.set_value(v), run_time=0.9)
            vo.wait_until("b")
            self.play(Write(one), FadeIn(expl))
            vo.wait_until("c")
            self.play(FadeIn(thm, shift=UP * 0.2))
        bars.freeze()
        self.clear_scene()

    def logscale(self):
        sh = load("shape")
        lh = np.asarray(sh["lin_hist"])
        I = axes([0, 300], [0, lh.max() * 1.15], x_length=10.0, y_length=4.0, xlabel=r"income (thousands)",
                 xticks=[0, 50, 100, 150, 200, 250, 300], center=[0, -0.4, 0])
        ib = hist_bars(I.ax, np.linspace(0, 300, 61), lh, color=S.TRUTH, opacity=0.7, stroke_width=0)
        lg = np.asarray(sh["log_hist"])
        e = np.linspace(np.log10(3000), np.log10(3e6), 61)
        L = axes([e[0], e[-1]], [0, lg.max() * 1.15], x_length=10.0, y_length=4.0, xlabel=r"income (log scale)",
                 xticks=[np.log10(v) for v in (1e4, 1e5, 1e6)],
                 xfmt=lambda v: {4: r"10{,}000", 5: r"100{,}000", 6: r"1{,}000{,}000"}[int(round(v))],
                 center=[0, -0.4, 0])
        lb = hist_bars(L.ax, e, lg, color=S.TRUTH, opacity=0.7, stroke_width=0)
        mean_l = vline(L.ax, np.log10(sh["mean"]), MEAN, stroke_width=3)
        med_l = vline(L.ax, np.log10(sh["median"]), MEDIAN, stroke_width=3)
        cap = VGroup(MathTex(rf"\text{{skew of }} \log y = {sh['logincome']['skew']:.2f}", font_size=32, color=S.TRUTH),
                     label(rf"median {money(sh['median'])}", font_size=24, color=MEDIAN),
                     label(rf"mean {money(round(sh['mean']))}", font_size=24, color=MEAN)).arrange(RIGHT, buff=0.5)
        cap.to_edge(UP, buff=0.5)
        with self.voiceover(
            "There's a simple way to tame a tail like this. <bookmark mark='a'/> On an ordinary axis, the incomes are "
            "a cliff and a long, thin beach. Every income from a hundred thousand to millions is squeezed into the "
            "flat part on the right. <bookmark mark='b'/> Now put income on a logarithmic scale, where each step "
            "multiplies by ten. <bookmark mark='c'/> The cliff becomes a hill, and almost a symmetric one: the "
            f"skewness of the logarithm of income is {sh['logincome']['skew']:.2f}. On this scale, the median, "
            f"{money(sh['median'])}, sits in the middle of the hill; the mean, {money(round(sh['mean']))}, sits to "
            "its right, pulled by the tail. <bookmark mark='d'/> A logarithm turns multiplication into addition, and "
            "many quantities grow multiplicatively: incomes, populations, prices, the sizes of towns. Their "
            "logarithms are often close to bell-shaped. That's the log-normal distribution, which the World's "
            "incomes were built from, and which Part 3 derives."
        ) as vo:
            self.play(FadeIn(I), FadeIn(ib))
            vo.wait_until("b")
            self.play(FadeOut(I), FadeIn(L), ReplacementTransform(ib, lb), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(cap[0]), Create(med_l), Create(mean_l), FadeIn(cap[1:]))
        self.clear_scene()

    def pareto(self):
        sh = load("shape")
        xs, ss = np.asarray(sh["tail_x"]), np.asarray(sh["tail_s"])
        ok = ss > 0
        A = axes([4.3, 6.8], [-6.2, 0.2], x_length=7.2, y_length=5.0, xlabel=r"income $y$ (log scale)",
                 ylabel=r"share earning more than $y$ (log scale)",
                 xticks=[5, 6], xfmt=lambda v: {5: r"100{,}000", 6: r"1{,}000{,}000"}[int(round(v))],
                 yticks=[0, -2, -4, -6], yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.4, -0.4, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(np.log10(a), np.log10(b)), radius=0.05, color=S.TRUTH)
                       for a, b in zip(xs[ok], ss[ok])])
        lo, hi = 5.3, 6.6
        fit = Line(ax.c2p(lo, sh["intercept"] + sh["slope"] * lo), ax.c2p(hi, sh["intercept"] + sh["slope"] * hi),
                   color=S.EST, stroke_width=4)
        eq = cmath(r"P(Y > y)", r"\approx", r"C\, y^{-\alpha}", font_size=38).move_to([4.4, 2.0, 0])
        res = VGroup(MathTex(rf"\text{{slope}} = {sh['slope']:.2f}", font_size=32, color=S.EST),
                     MathTex(rf"\text{{Hill estimate}}\ \hat\alpha = {sh['hill']:.2f}", font_size=30, color=S.EST),
                     MathTex(rf"\text{{true}}\ \alpha = {sh['alpha_true']:.1f}", font_size=30, color=S.TRUTH))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.5, 0.4, 0])
        hc = history_card(1896, r"Vilfredo Pareto, \emph{Cours d'\'economie politique}",
                          r"incomes in many countries fall on a straight line on these axes", color=S.MUSEUM,
                          width=4.8, font_size=20).move_to([4.5, -2.0, 0])
        cavs = note(r"Clauset, Shalizi \& Newman (2009): \ a straight line on log--log axes is not proof").to_corner(
            DL, buff=0.3)
        with self.voiceover(
            "The tail itself has a law. <bookmark mark='a'/> Plot, for each income y, the share of adults earning "
            "more than y, with both axes on logarithmic scales. <bookmark mark='b'/> Beyond a hundred thousand or so, "
            "the points fall on a straight line. A straight line on log-log axes means a power law: the share "
            "earning more than y falls like y to the power minus alpha. <bookmark mark='c'/> Vilfredo Pareto found "
            "this in the tax records of several countries in 1896, and it bears his name. <bookmark mark='d'/> The "
            f"slope of this line is {sh['slope']:.2f}. A better estimator, Hill's, uses only the top "
            f"{money(sh['hill_k'])} incomes and gives {sh['hill']:.2f}. And because this is the World, we can check: "
            f"the true exponent is {sh['alpha_true']:.1f}. <bookmark mark='e'/> A caution, from Clauset, Shalizi "
            "and Newman: a straight-looking line on log-log axes is not proof of a power law; log-normal tails can "
            "look straight for a long way. Telling them apart is a problem in testing, and we'll be ready for it in "
            "Part 10."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(p) for p in pts], lag_ratio=0.03), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(fit), Write(eq))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]), FadeIn(res[2]))
            vo.wait_until("e")
            self.play(FadeIn(cavs))
        self.clear_scene()
