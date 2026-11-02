from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, hist_bars, load, predict, show_card, tbar

BH_CODE = [
    "def benjamini_hochberg(p, q=0.05):",
    "    p = np.asarray(p, float)",
    "    m = len(p)",
    "    order = np.argsort(p)",
    "    thresh = q * np.arange(1, m + 1) / m      # the rising line i q / m",
    "    below = p[order] <= thresh",
    "    k = np.max(np.flatnonzero(below)) + 1 if below.any() else 0",
    "    rej = np.zeros(m, bool)",
    "    rej[order[:k]] = True                     # everything up to the last crossing",
    "    return rej",
]


class Many(VoiceoverScene):
    def construct(self):
        m = load("multiple")
        f = load("fdr_sim")
        self.card()
        self.sorted_p(m)
        self.derive()
        self.planted(f)
        self.lab(m, f)

    def card(self):
        c = chapter_card(13, r"Many tests", r"How many of your discoveries are luck?", lit=(2016,), part=PART)
        with self.voiceover("Chapter thirteen. Many tests."):
            show_card(self, c)
        self.play(FadeOut(c))

    def sorted_p(self, m):
        p = np.sort(np.asarray(m["p"]))
        n = len(p)
        k = np.arange(1, n + 1)
        lp = np.log10(np.maximum(p, 1e-4))
        g = axes([0, n + 1], [-4, 0], x_length=7.0, y_length=4.6, xlabel=r"industries, sorted by $p$-value",
                 ylabel=r"$p$-value of the CAPM alpha (log scale)", xticks=[1, 10, 20, 30, 40, 49],
                 yticks=[-4, -3, -2, np.log10(0.05), 0],
                 yfmt=lambda u: {-4: "10^{-4}", -3: "0.001", -2: "0.01", 0: "1"}.get(round(u), "0.05"),
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(i, v), radius=0.06, color=GOOD if pv < 0.05 else DATA_C) for i, v, pv in zip(k, lp, p)])
        five = DashedLine(ax.c2p(0, np.log10(0.05)), ax.c2p(n + 1, np.log10(0.05)), color=GREY_B, stroke_width=2)
        bonf = DashedLine(ax.c2p(0, np.log10(0.05 / n)), ax.c2p(n + 1, np.log10(0.05 / n)), color=BAD, stroke_width=2.5)
        q = ValueTracker(0.0005)
        bh = always_redraw(lambda: curve(ax, k, np.maximum(np.log10(q.get_value() * k / n), -4), ALT, stroke_width=3))
        q_ro = always_redraw(lambda: MathTex(rf"\text{{BH line: }} p_{{(i)}} \le i\,q/m,\ q = {q.get_value():.3f}",
                                             font_size=26, color=ALT).next_to(g, UP, buff=0.05).align_to(g, RIGHT))
        side = VGroup(
            label(r"49 industries, 1926--2020, Newey--West $t$", font_size=21, color=GREY_A),
            MathTex(rf"p < 0.05:\ {m['n_raw']}", font_size=32, color=GOOD),
            MathTex(rf"\text{{expected by luck: }} 49 \times 0.05 \approx {49 * 0.05:.1f}", font_size=28, color=GREY_A),
            MathTex(rf"\text{{Bonferroni, Holm: }} {m['n_bonf']}, {m['n_holm']}", font_size=30, color=BAD),
            MathTex(rf"\text{{Benjamini--Hochberg (5\%): }} {m['n_bh']}", font_size=30, color=ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Test forty-nine industries for an alpha and sort the p-values. <bookmark mark='a'/> "
            f"{m['n_raw']} are below five percent; by luck alone you expect two or three. <bookmark mark='b'/> Bonferroni "
            "divides the threshold by the number of tests, the red line, controlling the chance of even one false "
            "discovery. <bookmark mark='c'/> Benjamini and Hochberg, in 1995, control the share of discoveries that are "
            "false: their line rises from the origin, i times q over m, and everything up to the last p-value under it "
            f"is a discovery. <bookmark mark='d'/> Here, {m['n_bh']}. No industry alpha survives either correction."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03))
            vo.wait_until("a")
            self.play(Create(five), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(bonf), FadeIn(side[3]))
            vo.wait_until("c")
            self.add(bh, q_ro)
            self.play(q.animate.set_value(0.05), run_time=vo.until("d"), rate_func=linear)
            self.play(FadeIn(side[4]))
        bh.clear_updaters()
        q_ro.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        C_ = {r"\alpha/m": BAD, r"q": ALT}
        rows = [cmath(r"P\Big(\textstyle\bigcup_{i \in H_0}\{p_i \le \alpha/m\}\Big)", r"\le",
                      r"\textstyle\sum_{i \in H_0} \alpha/m \le \alpha", font_size=36, colors=C_),
                cmath(r"\text{Holm: first false rejection}", r"\Rightarrow",
                      r"\ge m_0 \text{ remain, threshold} \le \alpha/m_0", font_size=34, colors=C_),
                cmath(r"\mathrm{FDR} = \mathbb{E}\Big[\tfrac{V}{\max(R, 1)}\Big]", r"=", r"\tfrac{m_0}{m}\,q \le q",
                      font_size=36, colors=C_),
                cmath(r"p\text{-histogram}", r"=", r"\pi_0 \cdot \text{Uniform} + (1 - \pi_0)\cdot\text{spike near } 0",
                      font_size=34, colors=C_)]
        whys = [why(r"the union bound: the chance of any false rejection is at most the sum of the chances"),
                why(r"Holm (1979): step down through the sorted $p$-values with thresholds $\alpha/m, \alpha/(m-1), "
                    r"\dots$; at the first true null rejected, at least $m_0$ nulls are left, so FWER $\le \alpha$"),
                why(r"Benjamini and Hochberg (1995), independent $p$-values: $V$ false of $R$ rejected; exact, with "
                    r"$m_0$ true nulls"),
                why(r"what a mixture of nulls and real effects looks like: a flat floor of height $\pi_0$ plus a spike")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.8, edge=6.8)
        with self.voiceover(
            "The proofs are short. Bonferroni is the union bound. <bookmark mark='a'/> Holm's 1979 step-down uses "
            "thresholds alpha over m, then over m minus one, and so on; at its first false rejection at least m-nought "
            "nulls remain, so the union bound still applies, with more power. <bookmark mark='b'/> Benjamini-Hochberg's "
            "false discovery rate, with independent p-values, is the share of true nulls times q: at most q. "
            "<bookmark mark='c'/> And null p-values are uniform, so a histogram of many is a flat floor, the share of "
            "nulls, plus a spike near zero."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def planted(self, f):
        S = f["summary"]
        meths = ["raw", "Bonferroni", "Holm", "BH"]
        mlab = [r"$p < 0.05$", r"Bonferroni", r"Holm", r"BH, $q = 5\%$"]
        g = axes([0, 4], [0, 60], x_length=6.0, y_length=3.6, ylabel=r"discoveries per world (10--90\% whiskers)",
                 xticks=[], yticks=[0, 10, 30, 50], font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        bars = VGroup()
        for i, k in enumerate(meths):
            s = S[k]
            for j, (key, col) in enumerate((("true", GOOD), ("false", BAD))):
                x = i + 0.3 + 0.4 * j
                b = tbar(ax, x, min(s[key], 60), col, width=0.32)
                lo, hi = s[f"{key}_q"]
                wsk = Line(ax.c2p(x, min(lo, 60)), ax.c2p(x, min(hi, 60)), color=WHITE, stroke_width=2)
                bars.add(VGroup(b, wsk))
        labs = VGroup(*[label(t, font_size=17, color=GREY_B).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.12)
                        for i, t in enumerate(mlab)])
        leg = legend([(GOOD, r"true discoveries (of 50)"), (BAD, r"false discoveries")], font_size=18).next_to(
            g, UP, buff=0.1).align_to(g, LEFT)
        pe = np.asarray(f["p_example"])
        h = axes([0, 1], [0, 8], x_length=4.6, y_length=2.6, xlabel=r"$p$-values of one world", xticks=[0, 0.5, 1],
                 yticks=[1, 4, 8], font_size=14).to_edge(RIGHT, buff=0.4).shift(UP * 0.9)
        hb = hist_bars(h.ax, pe, np.linspace(0, 1, 21), DATA_C, density=True, cap=8)
        pi0 = 1 - f["m1"] / f["m"]
        floor = DashedLine(h.ax.c2p(0, pi0), h.ax.c2p(1, pi0), color=YELLOW, stroke_width=2.5)
        fl = MathTex(rf"\pi_0 = {pi0:.2f}", font_size=24, color=YELLOW).next_to(h.ax.c2p(1, pi0), UP, buff=0.08)
        fl.shift(LEFT * 0.4)
        txt = VGroup(
            MathTex(rf"\text{{FDR: raw }} {100 * S['raw']['fdr']:.0f}\%,\ \text{{BH }} {100 * S['BH']['fdr']:.1f}\%",
                    font_size=26, color=ALT),
            MathTex(rf"\text{{FWER: Holm }} {100 * S['Holm']['fwer']:.1f}\%", font_size=26, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(h, DOWN, buff=0.4).align_to(h, LEFT)
        with self.voiceover(
            f"A world with a known truth: a thousand strategies, {f['m1']} real with a Sharpe ratio of {f['sr']} over "
            f"{f['years']} years, the rest noise, two hundred times. <bookmark mark='a'/> At five percent each world finds "
            f"about {S['raw']['true']:.0f} real ones and {S['raw']['false']:.0f} false: {100 * S['raw']['fdr']:.0f} percent "
            f"false. <bookmark mark='b'/> Bonferroni and Holm make almost no false discoveries but find "
            f"{S['Holm']['true']:.0f} real ones; Benjamini-Hochberg finds {S['BH']['true']:.1f} at a false discovery rate "
            f"of {100 * S['BH']['fdr']:.1f} percent, as promised. <bookmark mark='c'/> The p-value histogram shows why it "
            f"is hard: a floor at {pi0:.2f} and a modest spike."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), FadeIn(leg))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]), GrowFromEdge(bars[1][0], DOWN),
                      FadeIn(bars[1][1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1])) for b in bars[2:]],
                                  lag_ratio=0.3, run_time=2.5))
            self.play(FadeIn(txt))
            vo.wait_until("c")
            self.play(FadeIn(h), LaggedStart(*[GrowFromEdge(b, DOWN) for b in hb], lag_ratio=0.05))
            self.play(Create(floor), FadeIn(fl))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, m, f):
        card = lab_card(r"Benjamini--Hochberg in the House", BH_CODE, source="explainer/quant/house/econ.py",
                        width=8.0, font_size=18).to_corner(UL, buff=0.35)
        S = f["summary"]["BH"]
        outs = [f"benjamini_hochberg(p_49_industries).sum()   -> {m['n_bh']}",
                f"planted worlds: {S['true']:.1f} true, {S['false']:.2f} false per world (FDR {100 * S['fdr']:.1f}%)",
                f"1,000 pure-noise strategies: {m['noise_raw']} pass at 5%, {m['noise_bh']} after BH"]
        prev = wrapped_label(r"next: White's reality check and Romano--Wolf (Part 26); $t > 3$ and the factor zoo "
                             r"(Part 25); correcting the winner's estimate (chapter 18)", 5.0, 20, GREY_A)
        prev.to_corner(DR, buff=0.4)
        q = predict(r"Twenty strategies; the best has $p = 0.03$. Significant?", width=6.0).to_corner(UR, buff=0.35)
        with self.voiceover(
            "The House's ten lines: sort, compare with the rising line, reject up to the last crossing. "
            f"<bookmark mark='a'/> Industries: {m['n_bh']}. Planted worlds: about {S['true']:.0f} true discoveries, false "
            f"discovery rate {100 * S['fdr']:.0f} percent. Pure noise: {m['noise_raw']} pass at five percent, "
            f"{m['noise_bh']} after correction. <bookmark mark='b'/> Pause and predict: twenty strategies, the best at p "
            "of three percent. Significant? No: the chance one of twenty useless strategies does that well is forty-six "
            "percent. Part twenty-six builds the machinery."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(q), FadeIn(prev))
        self.wait(0.4)
        self.clear_scene()
