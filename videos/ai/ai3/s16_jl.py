from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, MPC, chapter, dots_on, load

MEAS, EXACT, BOUND = C.TRUE_P, C.BITS, MPC


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
        w10 = DecimalNumber(100 * j[f"within10_{ks[0]}"], num_decimal_places=0, font_size=40, color=C.BITS, unit=r"\%")
        wread = VGroup(w10, label(r"of distances within $10\%$", font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.2)
        wread.move_to([3.8, 1.2, 0])
        head = label(rf"${fmt_int(n)}$ of GPT-2's vectors, \ times one random $768 \times k$ matrix", font_size=32)
        head.to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here's a consequence of that geometry which sounds impossible. <bookmark mark='a'/> Take a thousand of "
            "GPT-2's vectors, and multiply them all by the same random matrix, crushing 768 numbers down to a few. "
            f"<bookmark mark='b'/> Down to {ks[0]}, distances are scrambled. {ks[1]}, {ks[2]}: better. "
            f"<bookmark mark='c'/> At {ks[3]}, {100 * j[f'within10_{ks[3]}']:.0f} percent of the distances move by "
            f"less than ten percent, and at {ks[4]}, {100 * j[f'within10_{ks[4]}']:.1f} percent."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(diag), FadeIn(xl), FadeIn(yl))
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
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def statement(self):
        j = load("jl")
        thm = theorem_card(r"the Johnson--Lindenstrauss lemma",
                           r"For any $n$ points and $0 < \varepsilon < 1$, \ if $k \ge \dfrac{4 \ln n}{\varepsilon^2/2 - "
                           r"\varepsilon^3/3}$, \ a random Gaussian map $f(\mathbf{x}) = R\mathbf{x}/\sqrt{k}$ keeps "
                           r"every squared distance within a factor $1 \pm \varepsilon$, \ with probability at least "
                           r"$1/n$.", who=r"W.~Johnson \& J.~Lindenstrauss (1984); \ this form: S.~Dasgupta \& "
                           r"A.~Gupta (2003)", width=8.6).move_to(UP * 1.0)
        num = label(rf"$n = 1{{,}}000$, \ $\varepsilon = {j['eps']:g}$: \ $k \ge {fmt_int(j['jl_k'])}$", font_size=32,
                    color=C.BITS).next_to(thm, DOWN, buff=0.5)
        note_ = label(r"whatever the starting dimension: \ $768$, or a million", font_size=28, color=GREY_A)
        note_.next_to(num, DOWN, buff=0.25)
        with self.voiceover(
            "This is the Johnson-Lindenstrauss lemma, from 1984, in the form Sanjoy Dasgupta and Anupam Gupta "
            "proved in 2003. <bookmark mark='a'/> To keep every squared distance among n points within one plus or "
            "minus epsilon, a random projection to about four log n over epsilon squared dimensions is enough. "
            "<bookmark mark='b'/> For our thousand points and ten percent, it asks for "
            f"{int(j['jl_k']):,} dimensions. Notice what is missing: the starting dimension. It does not appear at "
            "all. Let's prove it."
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
            cmath(r"P(\text{any pair fails})", r"\le", r"n^2\, e^{-k(\varepsilon^2/2 - \varepsilon^3/3)/2} < 1",
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
        step = ladder(self, rows, whys, keep=5, top=3.3, x=-2.6, buff=0.42, edge=6.9)
        tag = note(r"a pair $\mathbf{u}, \mathbf{v}$ is the vector $\mathbf{x} = (\mathbf{u} - \mathbf{v})/|\mathbf{u} - "
                   r"\mathbf{v}|$; \ the lower tail is the same").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Fix one pair of points, and let x be their difference, scaled to length one. <bookmark mark='a'/> Each "
            "coordinate of R x is a sum of independent normal numbers, so it is normal, with variance one. "
            "<bookmark mark='b'/> The squared length of R x is a sum of k independent squares: a chi-squared "
            "variable with mean k. The projection keeps the length right on average; the question is how far it "
            "strays. <bookmark mark='c'/> The Chernoff trick: apply Markov's inequality to e to the t times the "
            "squared length, whose average we know exactly. <bookmark mark='d'/> Choose the best t and bound the "
            "logarithm: the chance of stretching by more than epsilon falls exponentially in k. The chance of "
            "shrinking is bounded the same way. <bookmark mark='e'/> Finally the union bound: there are fewer than "
            "n squared over two pairs, each with two tails, and once k reaches four log n over that small "
            "quantity, the total chance of any failure is below one. So a good projection exists, and a random one "
            "works with probability at least one over n."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abcde"):
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
        leg = legend([(MEAS, r"measured, \ all $499{,}500$ pairs"), (EXACT, r"exact: \ the $\chi^2_k$ tail"),
                      (BOUND, r"the Chernoff bound")], font_size=22).move_to([4.7, 1.0, 0])
        k768 = fine[-1]
        worst_gap = max(abs(a - b) for a, b in zip(meas, ex))
        with self.voiceover(
            "Now check each step against the data. <bookmark mark='a'/> For one pair, the chance of moving by more "
            f"than {100 * eps:.0f} percent is exactly a chi-squared tail, the yellow curve. <bookmark mark='b'/> "
            f"The measured share of all 499,500 pairs, averaged over five random matrices, sits on it: the largest "
            f"gap is {worst_gap:.4f}. <bookmark mark='c'/> The Chernoff bound, dashed, is above, as a bound must "
            f"be. It is loose for small k, where it can't say anything, and at {int(k768['k'])} it is "
            f"{k768['chernoff']:.2f} against an exact {k768['exact_fail']:.3f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg[1]))
            vo.wait_until("a")
            self.play(Create(c_ex), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in d_me], lag_ratio=0.1), FadeIn(leg[0]))
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
        good = [(np.log10(f["k"]), f["bound_eps"]) for f in fine if f["bound_eps"] == f["bound_eps"]]
        c_b = curve(ax, [a for a, _ in good], [b for _, b in good], BOUND, 3)
        lo = [min(f["worst"]) for f in fine]
        hi = [max(f["worst"]) for f in fine]
        keep = [i for i, f in enumerate(fine) if max(f["worst"]) <= 1.0]
        bars = VGroup(*[Line(ax.c2p(lk[i], lo[i]), ax.c2p(lk[i], hi[i]), color=MEAS, stroke_width=6) for i in keep])
        mids = dots_on(ax, [lk[i] for i in keep], [float(np.mean(fine[i]["worst"])) for i in keep], MEAS, 0.06)
        leg = legend([(MEAS, r"measured: \ five random matrices"), (BOUND, r"proved: \ the union bound's $\varepsilon$")],
                     font_size=22).move_to([4.7, 1.2, 0])
        last = fine[-1]
        first_b = next(f for f in fine if f["bound_eps"] == f["bound_eps"])
        hist = history_card(2017, r"K.~Larsen \& J.~Nelson",
                            r"proved that no map at all, \ random or not, \ can do much better: \ $k$ must grow like "
                            r"$\log n / \varepsilon^2$", color=HIST, width=5.0).to_corner(DR, buff=0.25)
        with self.voiceover(
            "The lemma promises more than an average: every pair at once. <bookmark mark='a'/> Here is the worst "
            f"pair out of all of them, for five random matrices at each k. <bookmark mark='b'/> And here is what "
            f"the union bound guarantees, which only says something from k equals {int(first_b['k'])}. At "
            f"{int(last['k'])} dimensions, it promises {last['bound_eps']:.2f}, and the worst pair measured "
            f"{np.mean(last['worst']):.2f}. The proof is not far from the truth. <bookmark mark='c'/> And it cannot "
            "be much improved: in 2017 Kasper Green Larsen and Jelani Nelson proved that no map whatsoever can beat "
            "log n over epsilon squared by more than a constant. Random projections are as good as it gets."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.1), FadeIn(mids), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(c_b), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
