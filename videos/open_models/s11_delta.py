from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    PLANE_SCALE, Plot, cfg, label, model, model_tag, note, show_chapter_card, toy_tag, vec_arrow,
)
from videos.open_models.toys import overwrite_demo, reassignment_curve


class DeltaRule(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 10, "Kimi: the delta rule, and forgetting")
        self.tag = model_tag("kimi")
        self.add(self.tag)
        self.correct()
        self.chart()
        self.forget()
        self.real_decay()

    # ------------------------------------------------------------------
    def correct(self):
        d = overwrite_demo()
        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-1.6, 1.6, 1], x_length=4 * PLANE_SCALE * 1.4,
                            y_length=3.2 * PLANE_SCALE * 1.4,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.6},
                            axis_config={"stroke_color": GREY_B}).move_to(LEFT * 2.6 + DOWN * 0.3)
        S2 = d["steps"]["delta"][1]
        S3 = d["steps"]["delta"][2]
        k1, v_new = d["k1"], d["v1b"]
        old = S2 @ k1
        new = S3 @ k1
        assert np.allclose(new, v_new)
        k = vec_arrow(plane, k1, C.KEY)
        kl = MathTex(r"\vec k_1", font_size=34, color=C.KEY).next_to(k.get_end(), DOWN, buff=0.1)
        target = vec_arrow(plane, v_new, YELLOW)
        tl = MathTex(r"\vec v_1'", font_size=34, color=YELLOW).next_to(target.get_end(), DOWN, buff=0.1)
        read = vec_arrow(plane, old, C.MEMORY, 6)
        rl = MathTex(r"S\vec k_1", font_size=34, color=C.MEMORY).next_to(read.get_end(), UP, buff=0.1)
        err = Arrow(plane.c2p(*old), plane.c2p(*v_new), buff=0, color=RED, stroke_width=5,
                    max_tip_length_to_length_ratio=0.12)
        el = label(r"error", font_size=26, color=RED).next_to(err.point_from_proportion(0.5), RIGHT, buff=0.15)
        steps = VGroup(
            label(r"\textbf{1.} read: what does memory say now?", font_size=28, color=C.MEMORY),
            label(r"\textbf{2.} compare with the value to store", font_size=28, color=YELLOW),
            label(r"\textbf{3.} write only the difference", font_size=28, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.5 + UP * 1.6)
        eq = MathTex(r"S", r"\;\leftarrow\;", r"S", r"+", r"\beta", r"(", r"\vec v", r"-", r"S\vec k", r")",
                     r"\vec k^{\top}", font_size=44).next_to(steps, DOWN, buff=0.55)
        eq[0].set_color(C.MEMORY)
        eq[2].set_color(C.MEMORY)
        eq[6].set_color(YELLOW)
        eq[8].set_color(C.MEMORY)
        eq[10].set_color(C.KEY)
        gd = label(r"= one step of gradient descent\\on the recall error $\tfrac12\|S\vec k - \vec v\|^2$", font_size=26,
                   color=GREY_A).next_to(eq, DOWN, buff=0.35)
        beta = label(r"$\beta$: how hard to write, chosen by each token", font_size=24, color=GREY_A).next_to(gd, DOWN, 0.25)
        hist = note(r"the delta rule: Widrow \& Hoff, 1960; for linear attention: DeltaNet (Schlag et al., 2021)")
        hist.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The fix is called the delta rule, and it's an old idea, from adaptive filters in 1960. "
            "<bookmark mark='r'/> Before writing, read: ask the memory what it currently returns for this key. "
            "<bookmark mark='e'/> Compare that with the value you want to store. <bookmark mark='w'/> And write only the "
            "difference, the error. <bookmark mark='g'/> This is exactly one step of gradient descent on the memory's "
            "recall error: the memory is learning, as it reads, to map keys to values. <bookmark mark='o'/> And now the "
            "reassignment works. The old value along that key is replaced, not piled on."
        ) as vo:
            self.play(Create(plane), GrowArrow(k), FadeIn(kl), GrowArrow(target), FadeIn(tl), FadeIn(hist))
            vo.wait_until("r")
            self.play(TransformFromCopy(k, read), FadeIn(rl), FadeIn(steps[0]), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(steps[1]), Indicate(target, color=YELLOW))
            vo.wait_until("w")
            self.play(GrowArrow(err), FadeIn(el), FadeIn(steps[2]))
            self.play(Write(eq))
            vo.wait_until("g")
            self.play(FadeIn(gd), FadeIn(beta))
            vo.wait_until("o")
            self.play(Transform(read, vec_arrow(plane, new, C.MEMORY, 6)), rl.animate.next_to(plane.c2p(*new), RIGHT, 0.15),
                      FadeOut(err), FadeOut(el), run_time=1.5)
            self.play(Flash(plane.c2p(*new), color=YELLOW))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def chart(self):
        r = reassignment_curve()
        w = np.array(r["writes"])
        lin, dl = np.array(r["linear"]), np.array(r["delta"])
        assert r["d"] == 64 and r["n_keys"] == 16
        assert lin[-1] < 0.25 and dl[-1] > 0.85 and w[-1] == 320
        pl = Plot((16, 320), (0, 1.0), width=8.0, height=4.2, log_x=True, x_ticks=[16, 32, 64, 128, 256],
                  x_fmt=lambda v: f"{v:g}", y_ticks=[0, 0.5, 1.0]).move_to(DOWN * 0.3 + LEFT * 0.8)
        yl = label(r"how well each key recalls its \emph{latest} value (cosine)", font_size=26, color=GREY_A)
        yl.next_to(pl, UP, buff=0.2).align_to(pl, LEFT)
        xl = label(r"number of writes so far (16 keys, reassigned again and again)", font_size=24, color=GREY_A)
        xl.next_to(pl, DOWN, buff=0.5)
        l1 = pl.line(w, lin, C.MEMORY, 4).set_stroke(opacity=0.5)
        l2 = pl.line(w, dl, YELLOW, 5)
        t1 = label(r"plain sum", font_size=28, color=C.MEMORY).next_to(pl.c2p(w[-1], lin[-1]), RIGHT, buff=0.2)
        t2 = label(r"delta rule", font_size=28, color=YELLOW).next_to(pl.c2p(w[-1], dl[-1]), RIGHT, buff=0.2)
        tag = toy_tag(r"toy: a 64-dimensional memory, random keys and values")
        with self.voiceover(
            "Here's a bigger test: a 64-dimensional memory, and 16 keys that keep getting reassigned new random values. "
            "<bookmark mark='p'/> With the plain sum, recall of the latest values fades as the history piles up. "
            "<bookmark mark='d'/> With the delta rule, it stays high, however long the stream runs."
        ) as vo:
            self.play(Create(pl), FadeIn(yl), FadeIn(xl), FadeIn(tag))
            vo.wait_until("p")
            self.play(Create(l1), FadeIn(t1), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(l2), FadeIn(t2), run_time=1.5)
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def forget(self):
        k = cfg("kimi")
        assert k["kda_head_dim"] == 128 and k["kda_gate_lower_bound"] == -5.0
        n = 10
        rng = np.random.default_rng(2)
        mem = VGroup(*[Square(0.42, stroke_width=0, fill_color=C.MEMORY, fill_opacity=float(o))
                       for o in rng.uniform(0.5, 0.95, n * n)]).arrange_in_grid(n, n, buff=0.05)
        mem.move_to(LEFT * 3.7 + DOWN * 0.6)
        alphas = np.array([0.98, 0.3, 0.9, 0.6, 0.99, 0.45, 0.8, 0.95, 0.2, 0.7])
        a_row = VGroup(*[DecimalNumber(a, num_decimal_places=2, font_size=17, color=C.MEMORY).next_to(mem[j], UP, 0.15)
                         for j, a in enumerate(alphas)])
        a_l = label(r"one retention factor per key channel (column)", font_size=24, color=C.MEMORY)
        a_l.next_to(a_row, UP, buff=0.2)
        eq = MathTex(r"S", r"\;\leftarrow\;", r"S\,\mathrm{Diag}(\vec\alpha_t)", font_size=44)
        eq2 = MathTex(r"S", r"\;\leftarrow\;", r"S", r"+", r"\beta_t", r"(\vec v_t - S\vec k_t)\,\vec k_t^{\top}", font_size=40)
        VGroup(eq, eq2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 2.6 + UP * 1.2)
        for e in (eq, eq2):
            e[0].set_color(C.MEMORY)
        eq_l = VGroup(label(r"forget a little", font_size=24, color=GREY_A).next_to(eq, RIGHT, buff=0.3),
                      label(r"then correct", font_size=24, color=GREY_A).next_to(eq2, DOWN, buff=0.2).align_to(eq2, LEFT))
        kda = label(r"Kimi Delta Attention: the forgetting rate\\is different for each of the 128 key\\channels, "
                    r"and is chosen fresh for\\every token, from the token itself", font_size=26, color=YELLOW)
        kda.next_to(VGroup(eq, eq2), DOWN, buff=0.7).align_to(eq, LEFT)
        lineage = note(r"scalar forgetting: Gated DeltaNet (Yang et al., 2024); per-channel: Kimi Linear (Moonshot, 2025)")
        lineage.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Kimi Delta Attention, KDA, adds one more ingredient: forgetting. <bookmark mark='a'/> Before each write, "
            "every column of the memory is multiplied by a retention factor between zero and one. Old associations fade, "
            "making room for new ones. <bookmark mark='c'/> And here's KDA's refinement: the retention is different for "
            "each of the 128 key channels, and it's chosen fresh for every token, from the token itself. "
            "<bookmark mark='t'/> So some channels can hold on for thousands of tokens, while others turn over almost "
            "immediately."
        ) as vo:
            self.play(FadeIn(mem, lag_ratio=0.005), FadeIn(lineage))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(eq_l[0]))
            self.play(Write(eq2), FadeIn(eq_l[1]))
            vo.wait_until("c")
            self.play(FadeIn(a_row), FadeIn(a_l), FadeIn(kda))
            vo.wait_until("t")
            for _ in range(3):
                self.play(*[mem[i * n + j].animate.set_fill(opacity=mem[i * n + j].get_fill_opacity() * alphas[j])
                            for i in range(n) for j in range(n)], run_time=0.7)
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def real_decay(self):
        kd = model("kimi")["kda_decay"]
        edges = np.array(kd["half_life_edges"])
        hist = np.array(kd["half_life_hist"])
        n_ch = int(hist.sum())
        assert n_ch == 69 * 96 * 128 == 847872
        assert 28 < kd["median_half_life"] < 31 and kd["frac_under_1"] < 0.02 and 0.3 < kd["frac_over_100"] < 0.32
        assert hist[-1] > 0 and edges[-1] == 1e4
        med = kd["per_layer_median"]
        assert 4 < med[0] < 5 and max(med) > 100
        pl = Plot((0.1, 1e4), (0, hist.max() * 1.1), width=7.0, height=3.4, log_x=True,
                  x_ticks=[0.1, 1, 10, 100, 1000, 10000], x_fmt=lambda v: f"{v:g}" if v < 1000 else f"{int(v):,}".replace(",", "{,}"),
                  y_ticks=[]).move_to(LEFT * 2.6 + DOWN * 0.2)
        bars = VGroup()
        for a, b, h in zip(edges[:-1], edges[1:], hist):
            x0, x1 = pl.c2p(a, 0)[0], pl.c2p(b, 0)[0]
            r = Rectangle(width=(x1 - x0) * 0.92, height=max(1e-3, 3.4 * h / (hist.max() * 1.1)), stroke_width=0,
                          fill_color=C.MEMORY, fill_opacity=0.85)
            r.move_to([(x0 + x1) / 2, pl.c2p(a, 0)[1], 0], aligned_edge=DOWN)
            bars.add(r)
        m = kd["median_half_life"]
        mline = DashedLine(pl.c2p(m, 0), pl.c2p(m, hist.max() * 1.1), color=YELLOW, stroke_width=2)
        ml = label(r"median: 29 tokens", font_size=24, color=YELLOW).next_to(mline, UP, buff=0.1)
        xl = label(r"memory half-life at rest (tokens, log scale)", font_size=24, color=GREY_A).next_to(pl, DOWN, buff=0.5)
        yl = label(r"848{,}000 KDA channels", font_size=24, color=C.MEMORY).next_to(pl, UP, buff=0.45).align_to(pl, LEFT)
        pl2 = Plot((0, 69), (1, 200), width=4.2, height=3.4, log_y=True, x_ticks=[1, 23, 46, 69],
                   x_fmt=lambda v: f"{int(v)}", y_ticks=[1, 10, 100], y_fmt=lambda v: f"{int(v)}", font_size=22)
        pl2.move_to(RIGHT * 4.4 + DOWN * 0.2)
        med_line = pl2.line(np.arange(69) + 0.5, med, YELLOW, 3)
        y2 = label(r"median half-life, by layer", font_size=24, color=GREY_A).next_to(pl2, UP, buff=0.45).align_to(pl2, LEFT)
        x2 = label(r"KDA layer (bottom to top)", font_size=22, color=GREY_A).next_to(pl2, DOWN, buff=0.5)
        src = note(r"from K3's learned decay biases: $\alpha = \exp\!\big(-5\,\sigma(e^{A_h} b_{h,c})\big)$, before each "
                   r"token's own input adjusts it").to_edge(DOWN, buff=0.2)
        title = label(r"How long Kimi K3's memories last, read from its weights", font_size=32).to_edge(UP, buff=0.9)
        with self.voiceover(
            "We can see this in Kimi K3's weights. <bookmark mark='h'/> Each channel has a learned bias that sets its "
            "retention when nothing in particular is happening, before each token's own input nudges it. "
            "<bookmark mark='hh'/> Turning those into half-lives, how many tokens it takes for a stored association to "
            "fade to half strength, gives this spread, across all 848 thousand channels: from under one token, to more "
            "than ten thousand. <bookmark mark='md'/> The median is about 29 tokens. <bookmark mark='dp'/> And there's a "
            "trend with depth. In the first KDA layer, the typical channel's memory halves within about four tokens. Deeper in "
            "the network, typical half-lives grow to tens of tokens, and in some layers past a hundred."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("h")
            self.play(FadeIn(src))
            vo.wait_until("hh")
            self.play(Create(pl), FadeIn(xl), FadeIn(yl))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=2)
            vo.wait_until("md")
            self.play(Create(mline), FadeIn(ml))
            vo.wait_until("dp")
            self.play(Create(pl2), FadeIn(y2), FadeIn(x2))
            self.play(Create(med_line), run_time=2)

        cap = label(r"K3 also caps how fast a channel can forget (retention $> e^{-5}$ per token), which keeps the "
                    r"numbers in a range that GPUs' fast matrix units can handle in parallel chunks", font_size=22,
                    color=GREY_A).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "<bookmark mark='c'/> One engineering detail: K3 caps how fast a channel can forget, so that no retention factor "
            "drops below about e to the minus five per token. That keeps the numbers in a range that a GPU's fast matrix "
            "units can handle, when tokens are processed in parallel chunks."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeOut(src), FadeIn(cap, shift=UP * 0.2))
        self.clear_scene()
