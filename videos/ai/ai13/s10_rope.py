from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, K, MONO, PART, POS, Q, V, bars_chart, curve, load


def dial(radius=0.32, color=GREY_C) -> VGroup:
    return VGroup(Circle(radius=radius, stroke_color=color, stroke_width=1.5, fill_color="#121722", fill_opacity=1),
                  Dot(radius=0.025, color=GREY_B))


class Rope(VoiceoverScene):
    def construct(self):
        self.card()
        self.clocks()
        self.proof()
        self.relative()
        self.decay()
        self.use()

    def card(self):
        card = chapter_card(9, r"Positions as rotations", r"Can a position be an angle?", part=PART)
        with self.voiceover("Chapter nine. Positions as rotations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def clocks(self):
        r = load("rope")
        th = np.asarray(r["theta"])
        wl = np.asarray(r["wavelength"])
        n = len(th)
        m = ValueTracker(0.0)
        dials = VGroup(*[dial() for _ in range(n)]).arrange(RIGHT, buff=0.14).move_to(UP * 0.4)
        start = np.random.default_rng(3).uniform(0, 2 * PI, n)  # the query's own angles, before any rotation

        def hands():
            return VGroup(*[Line(d.get_center(), d.get_center() + 0.3 * np.array([math.cos(a0 + m.get_value() * t),
                                                                                   math.sin(a0 + m.get_value() * t), 0]),
                                 color=Q, stroke_width=3)
                            for d, a0, t in zip(dials, start, th)])

        hs = always_redraw(hands)
        wls = VGroup(*[MathTex(f"{v:,.0f}".replace(",", "{,}") if v >= 10 else f"{v:.1f}", font_size=17, color=GREY_B)
                       .next_to(d, DOWN, buff=0.12) for d, v in zip(dials, wl)])
        wlab = label(r"characters per full turn", font_size=22, color=GREY_A).next_to(wls, DOWN, buff=0.15)
        pairs = label(rf"a query's ${2 * n}$ numbers, \ taken in ${n}$ pairs: \ each pair is an arrow", font_size=26,
                      color=GREY_A).to_edge(UP, buff=0.5)
        counter = VGroup(label(r"position", font_size=30, color=POS), Integer(0, font_size=36, color=POS))
        counter.arrange(RIGHT, buff=0.25).next_to(dials, UP, buff=0.6)
        counter[1].add_updater(lambda t: t.set_value(int(round(m.get_value()))))
        colors = {r"m": POS, r"\theta_j": GREY_A}
        f = cmath(r"\begin{pmatrix} \cos m\theta_j & -\sin m\theta_j \\ \sin m\theta_j & \cos m\theta_j \end{pmatrix}",
                  font_size=36).to_edge(DOWN, buff=0.85).shift(LEFT * 2.5)
        fl = cmath(r"\theta_j = 10000^{-2j/32}", font_size=34, colors=colors).next_to(f, RIGHT, buff=0.8)
        cite_ = cite(r"J.~Su et al., \textit{RoFormer: Enhanced Transformer with Rotary Position Embedding} (2021)", corner=DR)
        with self.voiceover(
            "In 2021 Jianlin Su and colleagues proposed the answer nearly every model uses today: instead of adding "
            "a position to the input, rotate the queries and keys. Take a query's thirty-two numbers in sixteen "
            "pairs; each pair is an arrow in a plane. <bookmark mark='a'/> At position m, turn pair j by m times an "
            "angle theta j. <bookmark mark='b'/> The first pair turns fast, a full turn every six characters; each "
            "pair after it turns more slowly, down to one turn in thirty-five thousand. "
            "<bookmark mark='c'/> Keys are turned the same way. Like the hands of a clock, fast hands tell you the "
            "position nearby, slow hands where you are in a long text. This is RoPE, rotary position embedding."
        ) as vo:
            self.play(FadeIn(pairs), LaggedStart(*[FadeIn(d) for d in dials], lag_ratio=0.05), FadeIn(hs))
            vo.wait_until("a")
            self.play(FadeIn(counter), Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(m.animate.set_value(40), FadeIn(wls), FadeIn(wlab), run_time=6.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(cite_), m.animate.set_value(60), run_time=3.0, rate_func=linear)
        self.wait(0.3)
        counter[1].clear_updaters()
        hs.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        r = load("rope")
        colors = {r"q": Q, r"k": K, r"R_m": POS, r"R_n": POS, r"R_{-m}": POS, r"R_{n-m}": POS, r"R_m^\top": POS}
        rows = [
            cmath(r"(R_m q) \cdot (R_n k)", r"=", r"q^\top R_m^\top R_n\, k", font_size=38, colors=colors),
            cmath(r"(R_m q) \cdot (R_n k)", r"=", r"q^\top R_{-m} R_n\, k", font_size=38, colors=colors),
            cmath(r"(R_m q) \cdot (R_n k)", r"=", r"q^\top R_{n-m}\, k", font_size=38, colors=colors),
        ]
        whys = [why(r"$(Ax)\cdot y = x^\top A^\top y$"), why(r"a rotation's transpose turns it back"),
                why(r"turning by $-m$, then by $n$: \\ by $n - m$")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-1.0, buff=0.7, edge=6.9)
        box_t = label(r"the score depends on $n - m$ only: \ relative position, from absolute rotations",
                      font_size=26, color=POS).move_to([0, -1.6, 0])
        dev = float(r["dev"])
        chk = label(rf"checked on random $32$-number vectors, all shifts up to $40$: \ off by at most ${sci(dev)}$",
                    font_size=22, color=C.TRUE_P).next_to(box_t, DOWN, buff=0.35)
        with self.voiceover(
            "Why rotations? Here is the whole proof. Write R m for the rotation at position m. "
            "<bookmark mark='a'/> The score of a rotated query and a rotated key is q transposed, R m transposed, "
            "R n, k. <bookmark mark='b'/> The transpose of a rotation is the rotation backwards. "
            "<bookmark mark='c'/> And turning back by m then forward by n is turning by n minus m. "
            "<bookmark mark='d'/> So the score depends only on how far apart the two characters are, though each "
            "was rotated by its own absolute position. Checked on random vectors, to rounding error."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=POS))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(box_t), FadeIn(chk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def relative(self):
        r = load("rope")
        big = dial(radius=1.8).move_to([-3.4, -0.2, 0])
        qa, ka, th = 0.4, 2.0, 0.35  # illustrative angles for one pair
        mq, nk = ValueTracker(5.0), ValueTracker(2.0)
        c = big.get_center()

        def arrow(a, col, length):
            return Arrow(c, c + length * np.array([math.cos(a), math.sin(a), 0]), buff=0, color=col, stroke_width=6,
                         max_tip_length_to_length_ratio=0.12)

        qarr = always_redraw(lambda: arrow(qa + mq.get_value() * th, Q, 1.6))
        karr = always_redraw(lambda: arrow(ka + nk.get_value() * th, K, 1.3))

        def angle_arc():
            a1, a2 = qa + mq.get_value() * th, ka + nk.get_value() * th
            return Arc(radius=0.55, start_angle=a1, angle=(a2 - a1 + PI) % (2 * PI) - PI, arc_center=c, color=A,
                       stroke_width=4)

        arc = always_redraw(angle_arc)
        readout = VGroup(label(r"query at position", font_size=28, color=Q), Integer(5, font_size=32, color=Q),
                         label(r"key at position", font_size=28, color=K), Integer(2, font_size=32, color=K))
        readout[0].move_to([1.6, 2.6, 0], aligned_edge=LEFT)
        readout[2].move_to([1.6, 2.0, 0], aligned_edge=LEFT)
        readout[1].next_to(readout[0], RIGHT, buff=0.25)
        readout[3].next_to(readout[2], RIGHT, buff=0.25).align_to(readout[1], LEFT)
        readout[1].add_updater(lambda t: t.set_value(int(round(mq.get_value()))))
        readout[3].add_updater(lambda t: t.set_value(int(round(nk.get_value()))))
        score = VGroup(label(r"score", font_size=28, color=A), DecimalNumber(0, num_decimal_places=3, font_size=32, color=A))
        score.arrange(RIGHT, buff=0.2).move_to([1.6, 1.35, 0], aligned_edge=LEFT)
        score[1].add_updater(lambda t: t.set_value(1.6 * 1.3 * math.cos(qa + mq.get_value() * th - ka - nk.get_value() * th) / 2))
        colors = {r"m": Q, r"n": K, r"q": Q, r"k": K}
        f = cmath(r"(R_{", r"m", r"}\,", r"q", r")\cdot(R_{", r"n", r"}\,", r"k", r")", "=", r"q", r"\cdot", r"R_{", r"n",
                  r"-", r"m", r"}\,", r"k", colors=colors, font_size=40).move_to([2.6, 0.6, 0])
        fl = label(r"only the distance between them counts", font_size=26, color=GREY_A).next_to(f, DOWN, buff=0.25)
        chk = label(rf"computed for a real 32-number pair of vectors: \\ shifting both changes the score by under "
                    rf"$10^{{{math.ceil(math.log10(max(float(r['dev']), 1e-16)))}}}$", font_size=22, color=GREY_B)
        chk.next_to(fl, DOWN, buff=0.45)
        tag = note(r"one pair, \ illustrative angles").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Here is the same fact, seen on one pair: a query at position five and a key at position two. "
            "<bookmark mark='a'/> Their score depends on the angle between them. Now move both forward by the same "
            "amount, as if the same words appeared later in the text. <bookmark mark='b'/> Both arrows turn by the "
            "same angle, so the angle between them doesn't change, and neither does the score. "
            "<bookmark mark='c'/> A rotated query and a rotated key score according to how far apart they are, not "
            "where they are."
        ) as vo:
            self.play(FadeIn(big), FadeIn(tag), FadeIn(qarr), FadeIn(karr), FadeIn(readout))
            vo.wait_until("a")
            self.play(Create(arc), FadeIn(score))
            vo.wait_until("b")
            self.play(mq.animate.set_value(25), nk.animate.set_value(22), run_time=5.0, rate_func=smooth)
            vo.wait_until("c")
            self.play(Write(f), FadeIn(fl))
            self.play(FadeIn(chk))
        self.wait(0.3)
        for mob in (qarr, karr, arc, readout[1], readout[3], score[1]):
            mob.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def decay(self):
        r = load("rope")
        rr, dc = np.asarray(r["rs"], float), np.asarray(r["smooth"])
        raw_r, raw = np.asarray(r["r"], float)[1:], np.asarray(r["decay"])[1:]
        lx = np.log10(rr)
        ax = Axes(x_range=[0, 3.4, 1], y_range=[-0.5, 1, 0.5], x_length=7.6, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.9, -0.6, 0])
        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, -0.5), DOWN, buff=0.1)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3))])
        yt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for t, v in (("0", 0), ("1", 1))])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(3.4, 0), color=GREY_D, stroke_width=1.5)
        xn = label(r"distance between query and key, \ in characters", font_size=24, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        yn = label(r"a query's score against itself, \ moved apart \ (relative to distance $0$)", font_size=22, color=GREY_A)
        yn.next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        faint = curve(ax, np.log10(raw_r), raw, POS, 1).set_stroke(opacity=0.25)
        c = curve(ax, lx, dc, POS, 4)
        note_ = label(r"far apart, \\ the hands disagree: \\ distant matches \\ count for less, \\ on average", font_size=26,
                      color=POS).move_to([4.6, 0.6, 0])
        used = label(r"RoPE: \ Llama, Qwen, DeepSeek, \\ Mistral, Gemma, GLM, Kimi \dots", font_size=24, color=GREY_A)
        used.move_to([4.6, -1.6, 0])
        with self.voiceover(
            "And a bonus. Score a query against an identical key, then move them apart. Each pair's arrows drift "
            "out of step at its own speed, so the score shrinks with distance: <bookmark mark='a'/> on average, "
            "nearby matches count more than distant ones, a gentle bias towards the recent past that nobody had to "
            "build in. <bookmark mark='b'/> Since 2021, rotary positions have become the standard: almost every open "
            "model uses them."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), Create(zero), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(FadeIn(faint), Create(c), run_time=2.5)
            self.play(FadeIn(note_))
            vo.wait_until("b")
            self.play(FadeIn(used))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def use(self):
        t, r = load("tf"), load("rope")
        pq, pk = np.asarray(t["pair_q"]), np.asarray(t["pair_k"])  # layer, head, pair: mean squared size
        wl = np.asarray(r["wavelength"])
        ctx = int(t["ctx"])
        e = (pq / pq.sum(-1, keepdims=True) + pk / pk.sum(-1, keepdims=True)).mean((0, 1)) / 2  # share per pair
        n = len(e)
        cols = [interpolate_color(ManimColor(POS), ManimColor(GREY_B), i / (n - 1)) for i in range(n)]
        ch = bars_chart(e, cols, width=7.4, height=2.6, x0=-6.6, base_y=-1.4, vmax=float(e.max()) * 1.15,
                        font_size=14, fmt="{:.2f}")
        for v in ch.vals:
            v.set_opacity(0)
        top = label(r"our transformer: \ each rotation pair's share of the queries' and keys' size \\ "
                    r"(all $16$ heads, \ held-out text)", font_size=20, color=GREY_A).next_to(ch, UP, buff=0.25)
        top.align_to(ch, LEFT)
        xl = VGroup(label(rf"fastest: \ a turn every ${wl[0]:.0f}$", font_size=18, color=POS)
                    .next_to(ch.bars[0], DOWN, buff=0.15).align_to(ch.bars[0], LEFT),
                    label(rf"slowest: \ every ${wl[-1]:,.0f}$".replace(",", "{,}"), font_size=18, color=GREY_B)
                    .next_to(ch.bars[-1], DOWN, buff=0.15).align_to(ch.bars[-1], RIGHT))
        slow = [i for i in range(n) if wl[i] > ctx]  # pairs that never finish a turn inside the context
        s_slow = float(e[slow].sum())
        even = len(slow) / n
        jm = int(np.argmax(e))
        if wl[jm] > ctx and e[jm] > 2.0 / n:
            verdict = (f"Our small model has a favourite: pair {jm + 1}, which turns once every {wl[jm]:,.0f} "
                       f"characters, longer than its whole context, carries {e[jm]:.0%} of the size of its queries and "
                       f"keys, {e[jm] * n:.1f} times an even share. Barely rotating, it works as a plain channel for "
                       "content.")
        elif s_slow > 1.2 * even:
            verdict = (f"Our small model does the same: the {len(slow)} pairs that never finish a turn within its "
                       f"{ctx} characters carry {s_slow:.0%} of the size of its queries and keys, against {even:.0%} "
                       "if it were spread evenly.")
        else:
            verdict = (f"Our small model shows no such preference: the {len(slow)} pairs that never finish a turn "
                       f"within its {ctx} characters carry {s_slow:.0%} of the size of its queries and keys, close to "
                       f"the {even:.0%} of an even spread.")
        hl_ = SurroundingRectangle(ch.bars[jm], color=WHITE, buff=0.05) if e[jm] > 2.0 / n else VGroup()
        facts = VGroup(
            label(r"Barbero et al.\ (2024): \ Gemma uses the fastest pairs \\ for positional patterns, \ the slowest "
                  r"for meaning", font_size=20, color=GREY_A),
            label(r"Qwen3-Next (2025): \ only $64$ of each head's $256$ numbers \\ are rotated at all", font_size=20,
                  color=GREY_A),
            label(r"Gemma 3 (2025): \ base $10{,}000$ in local layers, \\ $1{,}000{,}000$ in global ones",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, 0.2, 0])
        keep_in_frame(facts)
        with self.voiceover(
            "Which hands does a trained model actually use? In 2024 Federico Barbero and colleagues looked inside "
            "Google's Gemma: its fastest pairs build sharp positional patterns, like looking exactly one token back, "
            "while its slowest pairs, which hardly turn, seem to carry meaning. <bookmark mark='a'/> " + verdict
            + " <bookmark mark='b'/> Designers have taken the hint. Qwen3-Next rotates only 64 of each head's 256 "
            "numbers and leaves the rest alone; Gemma 3 slows its global layers' clocks a hundredfold, with a base "
            "of a million instead of ten thousand, so that they turn slowly over long documents."
        ) as vo:
            self.play(FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(ch.base), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in ch.bars], lag_ratio=0.05),
                      FadeIn(xl))
            if len(hl_.submobjects) or isinstance(hl_, SurroundingRectangle):
                self.play(Create(hl_))
            vo.wait_until("b")
            self.play(FadeIn(facts[1:]))
        self.wait(0.3)
        self.clear_scene()
