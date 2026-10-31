from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, MPC, chapter, dots_on, load

MEAS, EXACT, BOUND = C.TRUE_P, C.BITS, MPC


def worst_plot_data(fine, x_range=(1.9, 3.0), ymax=1.0):
    """Keep only finite observations inside both plotted axes; never invent a bound."""
    bounds, measured = [], []
    for f in fine:
        x = math.log10(f["k"])
        if not x_range[0] <= x <= x_range[1]:
            continue
        epsilon = float(f["bound_eps"])
        if math.isfinite(epsilon) and 0 < epsilon < min(1.0, ymax):
            bounds.append((x, epsilon, int(f["k"])))
        values = np.asarray(f["worst"], float)
        if len(values) and np.isfinite(values).all() and 0 <= values.min() and values.max() <= ymax:
            measured.append((x, float(values.min()), float(values.max()), float(values.mean())))
    return bounds, measured, len(fine) - len(measured)


class JL(VoiceoverScene):
    def construct(self):
        chapter(self, 15, r"Johnson--Lindenstrauss, proved", r"How few numbers can keep the distances?",
                "Chapter fifteen. How few numbers can keep the distances?", lit=(1984,))
        self.squeeze()
        self.statement()
        self.proof()
        self.tails()
        self.worst()

    # ------------------------------------------------------------------
    def squeeze(self):
        j = load("jl")
        ks = [int(k) for k in j["ks"]]
        n = int(j["n"])
        d0 = np.asarray(j["d0"])
        dk = {k: np.asarray(j[f"d{k}"]) for k in ks}
        lo, hi = float(np.percentile(d0, 1)), float(np.percentile(d0, 99.5))
        ax = Axes(x_range=[lo, hi, 1], y_range=[lo * 0.2, hi * 1.6, 1], x_length=6.2, y_length=5.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.6, -0.5, 0])
        diag = Line(ax.c2p(lo, lo), ax.c2p(hi, hi), color=WHITE, stroke_width=2)
        band_up = DashedLine(ax.c2p(lo, lo * 1.1), ax.c2p(hi, hi * 1.1), color=GREY_B, stroke_width=1.5)
        band_dn = DashedLine(ax.c2p(lo, lo * 0.9), ax.c2p(hi, hi * 0.9), color=GREY_B, stroke_width=1.5)
        sel = np.arange(0, len(d0), 4)
        sel = sel[(d0[sel] >= lo) & (d0[sel] <= hi)]
        kt = ValueTracker(0)

        def ys():
            v = kt.get_value()
            i = int(np.floor(min(v, len(ks) - 1 - 1e-9)))
            a = v - i
            return (1 - a) * dk[ks[i]] + a * dk[ks[min(i + 1, len(ks) - 1)]]

        pts = VGroup(*[Dot(radius=0.025, color=C.TRUE_P, fill_opacity=0.7) for _ in sel])

        def place(g):
            y = ys()[sel]
            for dot, m, yy in zip(g, sel, y):
                dot.move_to(ax.c2p(float(d0[m]), float(np.clip(yy, lo * 0.2, hi * 1.6))))

        pts.add_updater(place)
        place(pts)
        xl = label(r"distance in $768$ dimensions", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"after the projection", font_size=24, color=GREY_A).next_to(ax, LEFT, buff=0.15).rotate(PI / 2)
        if zh():
            yl.rotate(-PI / 2)
        kv = Integer(ks[0], font_size=46, color=C.BITS)
        kread = VGroup(MathTex(r"k =", font_size=46), kv).arrange(RIGHT, buff=0.2).move_to([3.6, 2.2, 0])
        w10 = DecimalNumber(100 * j[f"within10_{ks[0]}"], num_decimal_places=1, font_size=40, color=C.BITS, unit=r"\%")
        wcaption = label(r"of distances within $10\%$", font_size=28, color=GREY_A)
        wread = VGroup(w10, wcaption).arrange(RIGHT, buff=0.2)
        wread.move_to([3.8, 1.2, 0])
        # Keep the descriptor clear as the measured percentage changes width.
        wcaption.add_updater(lambda m: m.next_to(w10, RIGHT, buff=0.2))
        w_a, w_b = 100 * j[f"within10_{ks[3]}"], 100 * j[f"within10_{ks[4]}"]
        head = label(rf"${fmt_int(n)}$ of GPT-2's vectors, \ times one random $768 \times k$ matrix", font_size=32)
        head.to_edge(UP, buff=0.35)
        cap = note(rf"ordinary distances; \ ${len(d0):,}$ sampled pairs; \ one map per $k$ \\ "
                   r"every fourth pair drawn in the central range; \ vertical extremes clipped",
                   font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "A consequence that sounds impossible. <bookmark mark='a'/> Multiply a thousand of GPT-2's vectors by one "
            f"random matrix, crushing 768 numbers to a few. These are {len(d0):,} sampled ordinary-distance pairs, "
            f"with one map per target dimension. <bookmark mark='b'/> Down to {ks[0]}, distances are "
            f"scrambled; {ks[1]}, {ks[2]}: better. <bookmark mark='c'/> At {ks[3]}, "
            f"{w_a:.0f} percent of the distances move by less than ten percent; at {ks[4]}, {w_b:.1f} percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), Create(ax), Create(diag), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.add(pts)
            self.play(FadeIn(kread), FadeIn(wread), Create(band_up), Create(band_dn))
            vo.wait_until("b")
            for i, k in enumerate(ks[1:3], start=1):
                self.play(kt.animate.set_value(i), ChangeDecimalToValue(kv, k),
                          ChangeDecimalToValue(w10, 100 * j[f"within10_{k}"]), run_time=1.3)
            vo.wait_until("c")
            for i, k in enumerate(ks[3:], start=3):
                self.play(kt.animate.set_value(i), ChangeDecimalToValue(kv, k),
                          ChangeDecimalToValue(w10, 100 * j[f"within10_{k}"]), run_time=1.3)
        pts.clear_updaters()
        wcaption.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def statement(self):
        j = load("jl")
        thm = theorem_card(r"the Johnson--Lindenstrauss lemma",
                           r"For any $n \ge 2$ points and $0 < \varepsilon < 1$, \ if $k \ge \dfrac{4 \ln n}{\varepsilon^2/2 - "
                           r"\varepsilon^3/3}$, \ a random Gaussian map $f(\mathbf{x}) = R\mathbf{x}/\sqrt{k}$ keeps "
                           r"every squared distance within a factor $1 \pm \varepsilon$, \ with probability at least "
                           r"$1/n$.", who=r"W.~Johnson \& J.~Lindenstrauss (1984); \ this form: S.~Dasgupta \& "
                           r"A.~Gupta (2003)", width=8.6).move_to(UP * 1.0)
        num = label(rf"$n = 1{{,}}000$, \ $\varepsilon = {j['eps']:g}$: \ $k \ge {fmt_int(j['jl_k'])}$", font_size=32,
                    color=C.BITS).next_to(thm, DOWN, buff=0.5)
        note_ = label(r"whatever the starting dimension: \ $768$, or a million", font_size=28, color=GREY_A)
        note_.next_to(num, DOWN, buff=0.25)
        with self.voiceover(
            "The Johnson-Lindenstrauss lemma, from 1984, in Dasgupta and Gupta's form of 2003. <bookmark mark='a'/> To "
            "keep every squared distance among n points within one plus or minus epsilon, a random projection to about "
            "log n over epsilon squared dimensions, up to a constant, suffices. <bookmark mark='b'/> For our thousand points at ten "
            f"percent: {int(j['jl_k']):,}. The starting dimension doesn't appear at all. Let's prove it."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(Indicate(thm.body, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(num), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        rows = [
            cmath(r"(R\mathbf{x})_i = \textstyle\sum_j R_{ij}x_j", r"\sim", r"\mathcal{N}(0, 1)", font_size=32),
            cmath(r"|R\mathbf{x}|^2", r"\sim", r"\chi^2_k, \quad \mathbb{E} = k", font_size=32),
            cmath(r"P\big(|R\mathbf{x}|^2 \ge (1+\varepsilon)k\big)", r"\le",
                  r"e^{-tk(1+\varepsilon)}\, (1-2t)^{-k/2}", font_size=32),
            cmath(r"P\big(|R\mathbf{x}|^2 \ge (1+\varepsilon)k\big)", r"\le",
                  r"\big((1+\varepsilon)e^{-\varepsilon}\big)^{k/2} \le e^{-k(\varepsilon^2/2 - \varepsilon^3/3)/2}",
                  font_size=32),
            cmath(r"P(\text{any pair fails})", r"\le", r"n(n-1)\,e^{-k(\varepsilon^2/2-\varepsilon^3/3)/2}"
                  r" \le 1-1/n",
                  font_size=32),
        ]
        whys = [why(r"$|\mathbf{x}| = 1$: \ a sum of independent normals \\ is normal, variance $\sum x_j^2 = 1$",
                    font_size=22),
                why(r"$k$ independent squares", font_size=22),
                why(r"Markov's inequality on $e^{t|R\mathbf{x}|^2}$ \ (Chernoff)", font_size=22),
                why(r"best $t = \frac{\varepsilon}{2(1+\varepsilon)}$; \ $\ln(1+\varepsilon) \le \varepsilon - "
                    r"\frac{\varepsilon^2}{2} + \frac{\varepsilon^3}{3}$", font_size=22),
                why(r"union bound: \ $\binom{n}{2}$ pairs, two tails; \\ true once $k \ge 4\ln n / "
                    r"(\varepsilon^2/2 - \varepsilon^3/3)$", font_size=22)]
        step = ladder(self, rows, whys, keep=5, top=3.3, x=-2.6, buff=0.42, edge=6.6)
        tag = note(r"a pair $\mathbf{u}, \mathbf{v}$ is the vector $\mathbf{x} = (\mathbf{u} - \mathbf{v})/|\mathbf{u} - "
                   r"\mathbf{v}|$; \ the lower tail obeys the same weaker exponent").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Fix one pair, and let x be their difference, of length one. <bookmark mark='a'/> Each coordinate of R x "
            "is a sum of independent normals: normal, with variance one. <bookmark mark='b'/> The squared length is a "
            "sum of k such squares: chi-squared, mean k. <bookmark mark='c'/> The Chernoff trick: Markov's inequality "
            "on e to the t times it, whose average we know. <bookmark mark='d'/> The best t, and a bound on the "
            "logarithm: the chance of stretching past epsilon falls exponentially in k, and shrinking likewise. "
            "<bookmark mark='e'/> The union bound over all pairs: once k reaches four log n over that small quantity, "
            "the chance of any failure is below one. A good projection exists, and a random one works with probability "
            "at least one over n."
        ) as vo:
            self.play(FadeIn(tag))
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=C.BITS))
            for k, mk in enumerate("bcde", start=1):
                vo.wait_until(mk)
                step(k)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tails(self):
        j = load("jl")
        fine = j["fine"]
        eps = float(j["eps"])
        ks = np.array([f["k"] for f in fine], float)
        lk = np.log10(ks)
        g = axes([0.2, 3.0, 1], [-2.5, 0.15, 1], x_length=7.4, y_length=4.2, xticks=[1, 2],
                 xfmt=lambda v: {1: "10", 2: "100"}[int(v)], yticks=[-2, -1, 0],
                 yfmt=lambda v: {-2: "0.01", -1: "0.1", 0: "1"}[int(v)],
                 xlabel=r"target dimension $k$", ylabel=rf"share of pairs whose squared distance moves by more than "
                 rf"${100 * eps:.0f}\%$", center=[-1.6, -0.5, 0])
        ax = g.ax
        meas = [float(np.mean(f["fail"])) for f in fine]
        ex = [f["exact_fail"] for f in fine]
        ch = [f["chernoff"] for f in fine]
        cl = lambda v: np.log10(np.maximum(v, 10 ** -2.5))  # noqa: E731
        c_ex = curve(ax, lk, cl(ex), EXACT, 3)
        c_ch = DashedVMobject(curve(ax, lk, cl(ch), BOUND, 3), num_dashes=40)
        d_me = dots_on(ax, lk, cl(meas), MEAS, 0.07)
        ranges = VGroup(*[Line(ax.c2p(x, float(cl(min(f["fail"])))), ax.c2p(x, float(cl(max(f["fail"])))),
                              color=MEAS, stroke_width=3) for x, f in zip(lk, fine)])
        cap = note(r"squared-distance error; \ dots: mean of five maps; \ bars: min--max \\ "
                   r"all pairs share a map; \ probabilities below $10^{-2.5}$ shown at the floor",
                   font_size=17).to_edge(DOWN, buff=0.15)
        leg = legend([(MEAS, r"measured: \ five maps, all pairs"), (EXACT, r"exact: \ one pair's $\chi^2_k$ tail"),
                      (BOUND, r"the Chernoff bound")], font_size=22).move_to([4.7, 1.0, 0])
        k768 = fine[-1]
        worst_gap = max(abs(a - b) for a, b in zip(meas, ex))
        with self.voiceover(
            f"Now the data. <bookmark mark='a'/> For one pair, the chance of moving more than {100 * eps:.0f} percent is "
            "exactly a chi-squared tail, in yellow. These are squared-distance errors. <bookmark mark='b'/> "
            f"The mean measured fraction over five maps differs from that probability by at most {worst_gap:.4f}; "
            "the bars show the range. Pairs sharing a map are dependent. <bookmark mark='c'/> The dashed Chernoff "
            f"bound lies above the exact probability: at {int(k768['k'])}, {k768['chernoff']:.2f} "
            f"against {k768['exact_fail']:.3f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cap), FadeIn(leg[1]))
            vo.wait_until("a")
            self.play(Create(c_ex), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(ranges), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in d_me], lag_ratio=0.1), FadeIn(leg[0]))
            vo.wait_until("c")
            self.play(Create(c_ch), FadeIn(leg[2]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worst(self):
        j = load("jl")
        fine = j["fine"]
        n = int(j["n"])
        ks = np.array([f["k"] for f in fine], float)
        lk = np.log10(ks)
        big = [f for f in fine if f["k"] >= 100]
        g = axes([1.9, 3.0, 1], [0, 1.0, 0.25], x_length=7.4, y_length=4.2,
                 xticks=[float(np.log10(f["k"])) for f in big], xfmt=lambda v: f"{10 ** v:.0f}",
                 yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 xlabel=r"target dimension $k$", ylabel=r"the worst distortion over all pairs, \ "
                 r"$\max |\,\text{ratio of squared distances} - 1\,|$", center=[-1.6, -0.5, 0])
        ax = g.ax
        good, measured, omitted = worst_plot_data(fine)
        c_b = (curve(ax, [a for a, _, _ in good], [b for _, b, _ in good], BOUND, 3)
               if len(good) >= 2 else Dot(ax.c2p(*good[0][:2]), radius=0.07, color=BOUND)
               if good else VGroup())
        bars = VGroup(*[Line(ax.c2p(x, lo), ax.c2p(x, hi), color=MEAS, stroke_width=6)
                        for x, lo, hi, mean in measured])
        mids = dots_on(ax, [x for x, _, _, _ in measured], [mean for _, _, _, mean in measured], MEAS, 0.06)
        confidence = 100 * float(j["confidence"])
        delta = float(j["delta"])
        leg = legend([(MEAS, r"measured: \ mean and range of five maps"),
                      (BOUND, rf"union bound: \ ${confidence:g}\%$ confidence")],
                     font_size=20).move_to([4.6, 1.5, 0])
        cap = note(rf"$\delta={delta:g}$: \ probability over the random map \\ "
                   rf"${omitted}$ measured dimensions outside the plotted window omitted; \ no fabricated bounds",
                   font_size=17).to_edge(DOWN, buff=0.12)
        unavailable = label(r"no nontrivial $\varepsilon<1$ bound here", font_size=22, color=BOUND)
        unavailable.move_to([3.8, 0.1, 0])
        last = fine[-1]
        last_bound = float(last["bound_eps"])
        if good and math.isfinite(last_bound) and 0 < last_bound < 1:
            bound_verdict = (f"At {confidence:g} percent confidence over the random map, the first plotted "
                             f"nontrivial bound is at k of {good[0][2]}. At {int(last['k'])}, it certifies "
                             f"squared-distance distortion at most {last_bound:.2f}; the measured worst-pair "
                             f"mean is {np.mean(last['worst']):.2f}.")
        elif good:
            bound_verdict = (f"At {confidence:g} percent confidence, a nontrivial bound is available only at "
                             "the plotted certified dimensions; it is unavailable at the final sampled dimension.")
        else:
            bound_verdict = (f"At {confidence:g} percent confidence, none of these dimensions gives a "
                             "nontrivial epsilon below one from this union bound. That means the bound is "
                             "uninformative here, not that the measured maps failed.")
        hist = history_card(2017, r"K.~Larsen \& J.~Nelson",
                            r"worst-case point sets require \ $k$ to grow like "
                            r"$\log n / \varepsilon^2$", color=HIST, width=5.0).to_corner(DR, buff=0.25)
        with self.voiceover(
            "The lemma promises every pair at once. <bookmark mark='a'/> The worst pair of all, five random matrices "
            f"per k. Bars show the minimum to maximum, with a mean dot. <bookmark mark='b'/> {bound_verdict} "
            "This confidence comparison is separate from the classic existence statement we proved. "
            "<bookmark mark='c'/> In the worst case no map can do much better: in 2017 Kasper Green "
            "Larsen and Jelani Nelson proved log n over epsilon squared optimal, up to a constant."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.1), FadeIn(mids), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(c_b) if good else FadeIn(unavailable), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
