from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BOUND, HIST, MEAS, TEST, TRAIN, bars, card_body, chapter, curve, load


class Hoeffding(VoiceoverScene):
    def construct(self):
        chapter(self, 3, r"One rule, then many", r"When can a score on test data be trusted?",
                "Chapter three. One rule, then many.", lit=(1963,))
        self.one_rule()
        self.tails()
        self.many()
        self.curve_k()

    # ------------------------------------------------------------------
    def one_rule(self):
        h = load("hoeffding")
        p, ns = float(h["p"]), [int(n) for n in h["ns"]]
        thm = theorem_card(r"Hoeffding's inequality",
                           card_body(r"$Z_1, \dots, Z_n$ independent, \ each in $[0, 1]$, \ mean $\mu$:",
                                     r"P\big(|\bar Z - \mu| \ge \varepsilon\big) \le 2\, e^{-2n\varepsilon^2}", width=5.4),
                           who=r"W.~Hoeffding (1963); \ derived in Part 5", width=6.2, font_size=22)
        thm.to_corner(UL, buff=0.3)
        app = label(r"$Z_i = 1$ \ if the rule errs on test case $i$: \\ $\bar Z = \hat R$, \ $\mu = R$", font_size=24,
                    color=GREY_A).next_to(thm, DOWN, buff=0.3).align_to(thm, LEFT)
        G = axes([0, 0.7], [0, 14], x_length=6.4, y_length=4.4, xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                 xfmt=lambda v: rf"{100 * v:.0f}\%", xlabel=r"error rate measured on $n$ test cases",
                 center=(3.2, -0.3, 0))
        ax = G.ax
        pline = DashedLine(ax.c2p(p, 0), ax.c2p(p, 14), color=WHITE, stroke_width=2)
        pl = label(rf"true error ${100 * p:.0f}\%$", font_size=22).next_to(ax.c2p(p, 13), RIGHT, buff=0.12)
        eps = 0.05
        zone = Rectangle(width=ax.c2p(p + eps, 0)[0] - ax.c2p(p - eps, 0)[0], height=ax.c2p(0, 14)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=MEAS, fill_opacity=0.10).move_to(ax.c2p(p, 7))

        def hist(n):
            pmf = np.asarray(h[f"pmf{n}"])
            ks = np.arange(len(pmf))
            return bars(ax, ks / n, np.minimum(pmf * n, 14), 0.9 / n if n <= 40 else 1.0 / n, TEST, 0.8)

        hs = {n: hist(n) for n in ns}
        within = {n: 1 - float(np.interp(eps, np.asarray(h["eps"]), np.asarray(h[f"tail{n}"]))) for n in ns}
        tags = {n: label(rf"$n = {n}$: \ ${100 * within[n]:.0f}\%$ of draws within $\pm 5$ points", font_size=24,
                         color=TEST).next_to(G, UP, buff=0.1) for n in ns}
        with self.voiceover(
            "Start with one rule, fixed in advance, and a test set. Each test case is a coin flip: the rule errs "
            "or it doesn't, and the measured error rate is the average of those flips. Part five proved Hoeffding's "
            "inequality: an average of n independent numbers between zero and one strays from its mean by epsilon "
            "with probability at most two e to the minus two n epsilon squared. <bookmark mark='a'/> Watch it "
            f"happen. A rule whose true error is {100 * p:.0f} percent, measured on ten test cases, a hundred thousand "
            f"times: only {100 * within[ns[0]]:.0f} percent of the measurements land within five points. "
            f"<bookmark mark='b'/> On forty, {100 * within[ns[1]]:.0f} percent. <bookmark mark='c'/> On "
            f"{ns[2]}, {100 * within[ns[2]]:.0f}. <bookmark mark='d'/> On {ns[3]}, {100 * within[ns[3]]:.0f} "
            "percent: the histogram narrows like one over the square root of n."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2), FadeIn(app))
            self.play(FadeIn(G), FadeIn(zone), Create(pline), FadeIn(pl))
            vo.wait_until("a")
            self.play(FadeIn(hs[ns[0]]), FadeIn(tags[ns[0]]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(ReplacementTransform(hs[ns[k]], hs[ns[k + 1]]),
                          ReplacementTransform(tags[ns[k]], tags[ns[k + 1]]), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tails(self):
        h = load("hoeffding")
        n = 160
        e = np.asarray(h["eps"])
        tail, hoef, cheb = (np.asarray(h[k + str(n)]) for k in ("tail", "hoef", "cheb"))
        ok = tail > 0
        G = axes([0, 0.3], [-5, 0], x_length=6.6, y_length=4.4, xticks=[0, 0.1, 0.2, 0.3], yticks=[-4, -3, -2, -1, 0],
                 xfmt=lambda v: rf"{100 * v:.0f}", yfmt=lambda v: "1" if v == 0 else f"10^{{{int(v)}}}",
                 xlabel=r"$\varepsilon$: \ points off the true error", ylabel=r"chance of being that far off, \ $n = 160$",
                 center=(-2.8, -0.3, 0))
        ax = G.ax
        cm = curve(ax, e[ok], np.log10(tail[ok]), MEAS, 4)
        ch = curve(ax, e, np.log10(np.maximum(hoef, 1e-5)), BOUND, 3.5)
        okc = cheb < 1.0
        cc = curve(ax, e[okc], np.log10(cheb[okc]), GREY_B, 3)
        key = legend([(MEAS, r"measured, $100{,}000$ draws"), (BOUND, r"Hoeffding: \ $2e^{-2n\varepsilon^2}$"),
                      (GREY_B, r"Chebyshev: \ $\frac{p(1-p)}{n\varepsilon^2}$")], font_size=20)
        key.next_to(G, UP, buff=0.05).align_to(G, RIGHT)
        nh, ne, nc = int(h["n_hoef"]), int(h["n_exact"]), int(h["n_cheb"])
        q = label(r"How many test cases \\ to be within $5$ points, \\ $95\%$ of the time?", font_size=26)
        tab = VGroup(*[VGroup(label(a, font_size=24, color=c), MathTex(fmt_int(v), font_size=30, color=c)).arrange(RIGHT, buff=0.3)
                       for a, v, c in ((r"exact, \ knowing $p$:", ne, MEAS), (r"Hoeffding:", nh, BOUND),
                                       (r"Chebyshev:", nc, GREY_B))]).arrange(DOWN, aligned_edge=RIGHT, buff=0.22)
        side = VGroup(q, tab).arrange(DOWN, buff=0.4).move_to([4.3, -0.2, 0])
        ratio = nh / ne
        with self.voiceover(
            "On a log scale, the measured tail at a hundred and sixty test cases falls off like a parabola, and so "
            "does Hoeffding's bound, always above it. <bookmark mark='a'/> Chebyshev's bound, which uses only the "
            "variance, falls far more slowly. <bookmark mark='b'/> So how many test cases do you need to be within "
            f"five points of the truth, ninety-five percent of the time? Knowing the true error, exactly {ne}. "
            f"Hoeffding asks for {nh:,}, about {ratio:.1f} times as many, but it needs to know nothing about the "
            f"rule. Chebyshev asks for {nc:,}. That's why a held-out test set of a few thousand examples is a "
            "trustworthy score."
        ) as vo:
            self.play(FadeIn(G), Create(cm), Create(ch), FadeIn(key[:2]), run_time=1.6)
            vo.wait_until("a")
            self.play(Create(cc), FadeIn(key[2]))
            vo.wait_until("b")
            self.play(FadeIn(q))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def many(self):
        u = load("union")
        errs = np.asarray(u["sample_errs"])
        K, n = int(u["sample_K"]), int(u["sample_n"])
        best, fresh = float(u["sample_best"]), float(u["fresh_best"])
        G = axes([0.25, 0.75], [0, 0.09], x_length=6.0, y_length=3.4, xticks=[0.3, 0.4, 0.5, 0.6, 0.7],
                 xfmt=lambda v: rf"{100 * v:.0f}\%", xlabel=rf"training error, \ on ${n}$ coin-flip labels",
                 center=(-3.2, 0.2, 0))
        ax = G.ax
        vals, cnt = np.unique(np.round(errs, 2), return_counts=True)
        hb = bars(ax, vals, cnt / K, 0.009, TRAIN, 0.85)
        bd = Dot(ax.c2p(best, 0), radius=0.09, color=TEST)
        bl = label(rf"best: \ ${100 * best:.0f}\%$", font_size=24, color=TEST).next_to(bd, UP, buff=0.5)
        ar = Arrow(bl.get_bottom(), bd.get_top(), buff=0.08, color=TEST, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        cap = label(rf"${fmt_int(K)}$ rules that know nothing", font_size=26).next_to(G, UP, buff=0.15)
        fr = label(rf"the best one, \ on $10{{,}}000$ fresh cases: \ ${100 * fresh:.1f}\%$", font_size=24, color=TEST)
        fr.next_to(G, DOWN, buff=0.3)
        rows = [
            cmath(r"P\big(\exists h \in \mathcal H: |\hat R(h) - R(h)| \ge \varepsilon\big)", r"\le",
                  r"\textstyle\sum_{h \in \mathcal H} P\big(|\hat R(h) - R(h)| \ge \varepsilon\big)", font_size=28),
            cmath(r"P\big(\exists h \in \mathcal H: |\hat R(h) - R(h)| \ge \varepsilon\big)", r"\le",
                  r"2|\mathcal H|\, e^{-2n\varepsilon^2}", font_size=28),
            cmath(r"|\hat R(h) - R(h)|", r"\le", r"\sqrt{\dfrac{\ln(2|\mathcal H|/\delta)}{2n}}", font_size=30,
                  colors={r"\sqrt{\dfrac{\ln(2|\mathcal H|/\delta)}{2n}}": BOUND}),
        ]
        whys = [why(r"union bound: \ the chance of any is at most the sum"),
                why(r"Hoeffding, \ for each fixed $h$"),
                why(r"set the right side to $\delta$: \ for every $h$ at once, \ with probability $1 - \delta$")]
        for r_, w_ in zip(rows, whys):
            w_.scale(0.85)
        step = ladder(self, rows, whys, keep=3, top=0.9, x=0.8, buff=0.35, edge=6.9)
        with self.voiceover(
            "But a learner doesn't test one rule; it picks the best of many, on the same data. Here are "
            f"{K:,} rules that know nothing at all, scored on {n} examples whose labels are coin flips. "
            f"<bookmark mark='a'/> Each one's training error scatters around fifty percent, and the best of them "
            f"scores {100 * best:.0f}. <bookmark mark='b'/> On ten thousand fresh cases, that winner's error is "
            f"{100 * fresh:.1f} percent. Choosing among many rules is what made the score lie. "
            "<bookmark mark='c'/> The fix is the union bound: the chance that any rule strays is at most the sum of "
            "the chances. <bookmark mark='d'/> Each is a Hoeffding tail. <bookmark mark='e'/> Set the total to delta "
            "and solve: with probability one minus delta, every rule in a finite family is within the square root of "
            "log of the family's size over n. The price of choosing grows only with the logarithm."
        ) as vo:
            self.play(FadeIn(G), FadeIn(cap))
            self.play(FadeIn(hb, lag_ratio=0.05), run_time=1.4)
            vo.wait_until("a")
            self.play(FadeIn(bd), FadeIn(bl), GrowArrow(ar))
            vo.wait_until("b")
            self.play(FadeIn(fr))
            vo.wait_until("c")
            self.play(VGroup(G, cap, hb, bd, bl, ar, fr).animate.scale(0.55).to_corner(UL, buff=0.3))
            step(0)
            vo.wait_until("d")
            step(1)
            vo.wait_until("e")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve_k(self):
        u = load("union")
        Ks = np.log10(np.asarray(u["Ks"], float))
        b100, g100, bd100 = (np.asarray(u[k]) for k in ("best100", "gap100", "bound100"))
        G = axes([0, 6], [0, 0.55], x_length=6.4, y_length=4.4, xticks=[0, 2, 4, 6],
                 xfmt=lambda v: "1" if v == 0 else f"10^{{{int(v)}}}", yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                 yfmt=lambda v: rf"{100 * v:.0f}\%", xlabel=r"$|\mathcal H|$: \ rules to choose from \ ($n = 100$)",
                 center=(-3.0, -0.4, 0))
        ax = G.ax
        cb = curve(ax, Ks, b100, TRAIN, 3.5)
        cg = curve(ax, Ks, g100, MEAS, 4)
        cu = curve(ax, Ks, bd100, BOUND, 3.5)
        key = legend([(TRAIN, r"the best rule's training error"), (MEAS, r"largest gap, $95\%$ of the time"),
                      (BOUND, r"union bound")], font_size=20).next_to(G, UP, buff=0.1).align_to(G, LEFT)
        dfn = definition_card(r"PAC learning",
                              r"a family is \textit{probably approximately correct} learnable if, \ for every "
                              r"$\varepsilon, \delta$, \ some $n(\varepsilon, \delta)$ examples give, \ with probability "
                              r"$1 - \delta$, \ a rule within $\varepsilon$ of the best. \ Finite families: \ "
                              r"$n \approx \ln(|\mathcal H|/\delta)\,/\,\varepsilon^2$.", width=6.0, font_size=21)
        dfn.move_to([3.6, 1.0, 0])
        hist = history_card(1984, r"L.~G.~Valiant, \ \textit{A Theory of the Learnable}",
                            r"learning as a computation with a guarantee; \ Turing Award (2010)", width=6.0,
                            font_size=19, color=HIST).next_to(dfn, DOWN, buff=0.25)
        i6 = len(Ks) - 1
        tight = ": for independent rules it's nearly tight. " if g100[i6] > 0.8 * bd100[i6] else ". "
        with self.voiceover(
            f"As the family grows from one rule to a million, scored on a hundred examples, the best training "
            f"error drops from {100 * b100[0]:.0f} to {100 * b100[i6]:.0f} percent, on labels that are pure noise. "
            f"<bookmark mark='a'/> The largest gap between training and true error, ninety-five percent of the time, "
            f"grows from {100 * g100[0]:.0f} to {100 * g100[i6]:.0f} points, <bookmark mark='b'/> and the union bound, "
            f"from {100 * bd100[0]:.0f} to {100 * bd100[i6]:.0f}, stays above it"
            + tight
            + "<bookmark mark='c'/> Leslie Valiant made this the definition of learning in 1984: "
            "probably approximately correct. A family can be learned if enough examples make every rule's score "
            "trustworthy, with high probability, to within epsilon. For a finite family, the log of its size divided "
            "by epsilon squared is enough. But a line has infinitely many positions. The next chapter counts them "
            "properly."
        ) as vo:
            self.play(FadeIn(G), Create(cb), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(cg), FadeIn(key[1]))
            vo.wait_until("b")
            self.play(Create(cu), FadeIn(key[2]))
            vo.wait_until("c")
            self.play(FadeIn(dfn, shift=LEFT * 0.2))
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
