from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import load


class JL(VoiceoverScene):
    def construct(self):
        self.card()
        self.squeeze()
        self.lemma()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"Squeezing dimensions", r"How few numbers can keep the distances?", lit=(1984,), part=2)
        with self.voiceover("Chapter nine. Squeezing dimensions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def squeeze(self):
        j = load("jl")
        ks = list(j["ks"])
        assert ks == [2, 5, 20, 100, 400] and j["n"] == 1000
        d0 = np.asarray(j["d0"])
        dk = {k: np.asarray(j[f"d{k}"]) for k in ks}
        lo, hi = float(np.percentile(d0, 1)), float(np.percentile(d0, 99.5))
        ax = Axes(x_range=[lo, hi, 1], y_range=[lo * 0.2, hi * 1.6, 1], x_length=6.2, y_length=5.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.6, -0.5, 0])
        diag = Line(ax.c2p(lo, lo), ax.c2p(hi, hi), color=WHITE, stroke_width=2)
        band_up = DashedLine(ax.c2p(lo, lo * 1.1), ax.c2p(hi, hi * 1.1), color=GREY_B, stroke_width=1.5)
        band_dn = DashedLine(ax.c2p(lo, lo * 0.9), ax.c2p(hi, hi * 0.9), color=GREY_B, stroke_width=1.5)
        sel = np.arange(0, len(d0), 4)
        kt = ValueTracker(0)  # index into ks, fractional while morphing

        def ys():
            v = kt.get_value()
            i = int(np.floor(min(v, len(ks) - 1 - 1e-9)))
            a = v - i
            return (1 - a) * dk[ks[i]] + a * dk[ks[min(i + 1, len(ks) - 1)]]

        pts = VGroup(*[Dot(radius=0.025, color=C.TRUE_P, fill_opacity=0.7) for _ in sel])

        def place(g):
            y = ys()[sel]
            for dot, n, yy in zip(g, sel, y):
                dot.move_to(ax.c2p(float(d0[n]), float(np.clip(yy, lo * 0.2, hi * 1.6))))

        pts.add_updater(place)
        place(pts)
        xl = label(r"distance in $768$ dimensions", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"after the projection", font_size=24, color=GREY_A).next_to(ax, LEFT, buff=0.15).rotate(PI / 2)
        if zh():
            yl.rotate(-PI / 2)
        kl = MathTex(r"k =", font_size=46)
        kv = Integer(ks[0], font_size=46, color=C.BITS)
        kread = VGroup(kl, kv).arrange(RIGHT, buff=0.2).move_to([3.6, 2.2, 0])
        w10 = DecimalNumber(100 * j["within10_2"], num_decimal_places=0, font_size=40, color=C.BITS, unit=r"\%")
        wl = label(r"of distances within $10\%$", font_size=28, color=GREY_A)
        wread = VGroup(w10, wl).arrange(RIGHT, buff=0.2).move_to([3.8, 1.2, 0])
        head = label(r"$1{,}000$ of GPT-2's vectors, times one random $768 \times k$ matrix", font_size=32).to_edge(UP, buff=0.35)
        assert j["within10_100"] > 0.8 and j["within10_400"] > 0.99
        with self.voiceover(
            "Here's a consequence that sounds impossible. <bookmark mark='a'/> Take a thousand of GPT-2's vectors, "
            "and multiply them all by the same random matrix, crushing 768 numbers down to a few. "
            "<bookmark mark='b'/> Down to two, distances are scrambled. Five, twenty: better. "
            "<bookmark mark='c'/> At a hundred, 84 percent of the distances move by less than ten percent, and at "
            "four hundred, almost all of them."
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
    def lemma(self):
        j = load("jl")
        f = MathTex(r"k \;\ge\; \frac{8 \ln n}{\varepsilon^2}", font_size=60, color=C.BITS).move_to(UP * 1.3)
        what = label(r"keeps every distance among $n$ points within a factor $1 \pm \varepsilon$, \\ with high probability, "
                     r"whatever the starting dimension", font_size=30, color=GREY_A).next_to(f, DOWN, buff=0.4)
        num = label(rf"$n = 1{{,}}000$, \ $\varepsilon = 0.1$: \ $k \ge {j['jl_k']:,}$".replace(",", "{,}"), font_size=30)
        num.next_to(what, DOWN, buff=0.4)
        cons = label(r"a guarantee, and a cautious one: \ in practice $400$ already did", font_size=26, color=GREY_B)
        cons.next_to(num, DOWN, buff=0.25)
        head = label(r"The Johnson--Lindenstrauss lemma (1984)", font_size=36).to_edge(UP, buff=0.4)
        why_ = label(r"why: \ a random projection of a vector has nearly the same length every time", font_size=28,
                     color=C.TRUE_P).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "That's the Johnson–Lindenstrauss lemma, from 1984. <bookmark mark='a'/> To keep the distances among n "
            "points within a factor of one plus or minus epsilon, a random projection to about the log of n over "
            "epsilon squared dimensions is enough, whatever dimension you started from. <bookmark mark='b'/> The "
            "guarantee is cautious: for our thousand points it asks for five and a half thousand, and four hundred "
            "already did the job. <bookmark mark='c'/> The reason it works is the concentration we just saw: a random "
            "projection of a vector has nearly the same length, every time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(what))
            vo.wait_until("b")
            self.play(FadeIn(num), FadeIn(cons))
            vo.wait_until("c")
            self.play(FadeIn(why_))
        self.wait(0.3)
        self.clear_scene()
