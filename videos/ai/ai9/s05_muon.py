from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import OPT_COLORS, OPT_NAMES, curve, load

MU = OPT_COLORS["muon"]


class Muon(VoiceoverScene):
    def construct(self):
        self.card()
        self.orthogonalize()
        self.steepest()
        self.polynomial()
        self.result()
        self.clip()

    def card(self):
        card = chapter_card(4, r"Muon", r"What if every direction got the same push?", part=9)
        with self.voiceover("Chapter four. Muon."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def orthogonalize(self):
        m = load("muon")
        before, after = np.asarray(m["before"]), np.asarray(m["after"])
        n = len(before)
        ax = Axes(x_range=[0, n, 64], y_range=[0, 1.4, 0.5], x_length=7.6, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-1.8, -0.8, 0])
        xl = label(r"the gradient's $256$ singular values, \ largest first", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        bars_b = VGroup(*[Line(ax.c2p(i + 0.5, 0), ax.c2p(i + 0.5, float(v)), color=GREY_B, stroke_width=2)
                          for i, v in enumerate(before)])
        bars_a = VGroup(*[Line(ax.c2p(i + 0.5, 0), ax.c2p(i + 0.5, float(min(v, 1.4))), color=MU, stroke_width=2)
                          for i, v in enumerate(after)])
        colors = {r"U": GREY_A, r"V^{\top}": GREY_A, r"\Sigma": GREY_B}
        svd = cmath(r"G", "=", r"U", r"\Sigma", r"V^{\top}", colors=colors, font_size=42).move_to([4.2, 2.4, 0])
        orth = cmath(r"\operatorname{orth}(G)", "=", r"U", r"V^{\top}", colors=colors, font_size=42).next_to(svd, DOWN, buff=0.4)
        on = label(r"Part 2's SVD, \ with every \\ singular value set to $1$", font_size=24, color=MU).next_to(orth, DOWN, buff=0.2)
        ns = cmath(r"X \leftarrow aX + b\,(XX^{\top})X + c\,(XX^{\top})^2 X", font_size=30).next_to(on, DOWN, buff=0.5)
        nsl = label(r"Newton--Schulz: \ five matrix products, \ no SVD needed", font_size=22, color=GREY_A)
        nsl.next_to(ns, DOWN, buff=0.15)
        cite_ = cite(r"K.~Jordan et al., \textit{Muon} (2024); \ J.~Liu et al., \textit{Muon is Scalable for LLM Training} (2025)",
                     corner=DR)
        with self.voiceover(
            "Adam treats every weight separately. But the weights of a layer form a matrix, and a matrix has "
            "structure: part two's singular values. <bookmark mark='a'/> Here's a real gradient matrix from the "
            "character model. A few directions dominate; most are tiny. A step along it mostly pushes the few big "
            "directions further. <bookmark mark='b'/> Muon, from 2024, takes the gradient's singular value "
            "decomposition and sets every singular value to one: the same push in every direction. "
            "<bookmark mark='c'/> It doesn't even compute the SVD. Five rounds of a matrix polynomial, Newton–Schulz, "
            "do it approximately and fast."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars_b], lag_ratio=0.004), Write(svd), run_time=2.0)
            vo.wait_until("b")
            self.play(ReplacementTransform(bars_b, bars_a), Write(orth), FadeIn(on), run_time=2.0)
            vo.wait_until("c")
            self.play(Write(ns), FadeIn(nsl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        o = load("optim")
        names = ["sgd", "adamw", "muon"]
        allc = [np.asarray(o[n]) for n in o["names"]]
        top = float(max(c[1, 1] for c in allc)) + 0.2
        bot = float(min(c[-1, 1] for c in allc)) - 0.2
        steps = float(allc[0][-1, 0])
        ax = Axes(x_range=[0, steps, 500], y_range=[bot, top, 0.5], x_length=8.4, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.5, 0])
        xl = label(r"training steps", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"bits per character on held-out text", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        finals = o["finals"]
        rows = VGroup(*[label(rf"{OPT_NAMES[n]}: \ ${finals[n]:.2f}$", font_size=26, color=OPT_COLORS[n]) for n in names])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.7, 1.0, 0])
        lines = [curve(ax, np.asarray(o[n])[1:, 0], np.clip(np.asarray(o[n])[1:, 1], bot, top), OPT_COLORS[n], 3.5)
                 for n in names]
        better = finals["muon"] < finals["adamw"]
        with self.voiceover(
            "On the same character model, with Muon on the hidden matrices and AdamW on the rest: "
            + (f"<bookmark mark='a'/> it reaches {finals['muon']:.2f} bits, ahead of AdamW's {finals['adamw']:.2f}. "
               if better else
               f"<bookmark mark='a'/> it reaches {finals['muon']:.2f} bits, close to AdamW's {finals['adamw']:.2f} on "
               "this small model. ")
            + "Muon has since been scaled up: Moonshot AI reported that it needs about half the compute of AdamW, "
            "and used a version of it to train Kimi K2."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yn), Create(lines[0]), Create(lines[1]), FadeIn(rows[:2]))
            vo.wait_until("a")
            self.play(Create(lines[2]), FadeIn(rows[2]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def steepest(self):
        colors = {r"G": GREY_A, r"\Delta W": MU, r"\eta": C.BITS}
        eqs = VGroup(
            cmath(r"\min_{\|", r"\Delta W", r"\|_2 \,\le\,", r"\eta", r"} \ \langle", r"G", r",", r"\Delta W", r"\rangle", colors=colors, font_size=36),
            cmath(r"\langle", r"G", r",", r"\Delta W", r"\rangle = \sum_i \sigma_i\, u_i^{\top}", r"\Delta W", r"\, v_i \;\ge\; -",
                  r"\eta", r"\sum_i \sigma_i", colors=colors, font_size=36),
            cmath(r"\Delta W", r"= -", r"\eta", r"\, U V^{\top}", colors=colors, font_size=40),
        ).arrange(DOWN, buff=0.55).move_to(UP * 0.4)
        notes = VGroup(label(r"the best step that changes no direction by more than $\eta$", font_size=22, color=GREY_A),
                       label(r"each term is at least $-\eta\,\sigma_i$, \ since $|u^{\top} \Delta W v| \le \|\Delta W\|_2$", font_size=22,
                             color=GREY_A),
                       label(r"equality for every $i$ at once: \ Muon's step", font_size=22, color=MU))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, DOWN, buff=0.12)
        box = SurroundingRectangle(VGroup(eqs[2], notes[2]), color=MU, buff=0.15, corner_radius=0.1)
        cite_ = cite(r"J.~Bernstein \& L.~Newhouse, \textit{Old Optimizer, New Norm} (2024)", corner=DR)
        with self.voiceover(
            "Why set the singular values to one? Because it's the steepest step under the right notion of size. "
            "<bookmark mark='a'/> Ask for the step that lowers the loss fastest, to first order, among all steps "
            "that stretch no direction by more than eta: a bound on the spectral norm, which is what matters for a "
            "matrix that multiplies vectors. <bookmark mark='b'/> Write the gradient in its singular directions. Each "
            "term can be pushed down by at most eta times its singular value. <bookmark mark='c'/> And one step "
            "achieves every bound at once: minus eta times U V transpose. Adam, in the same sense, is the steepest "
            "step when each weight is bounded separately."
        ) as vo:
            self.play(FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(Write(eqs[k]), FadeIn(notes[k]))
            self.play(Create(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def polynomial(self):
        m = load("muon")
        before, after = np.asarray(m["before"], float), np.asarray(m["after"], float)
        a, b, c = 3.4445, -4.7750, 2.0315

        def p(x):
            return a * x + b * x ** 3 + c * x ** 5

        # the iteration on the singular values themselves: start at sigma / ||G||_F, apply p five times
        x = before / np.sqrt((before ** 2).sum())
        its = [x]
        for _ in range(5):
            x = p(x)
            its.append(x)
        match = float(np.abs(np.sort(its[-1])[::-1] - np.sort(after)[::-1]).max())
        ax = CornerAxes(x_range=[0, 1.2, 0.5], y_range=[0, 1.3, 0.5], x_length=4.2, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-4.0, -0.2, 0])
        pc = ax.plot(p, x_range=[0, 1.2, 0.005], color=MU, stroke_width=3.5)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1.2, 1.2), dash_length=0.06, stroke_width=1.5, color=GREY_B)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(1.2, 1), dash_length=0.06, stroke_width=1.5, color=GREY_B)
        f = MathTex(r"p(\sigma) = 3.4445\,\sigma - 4.7750\,\sigma^3 + 2.0315\,\sigma^5", font_size=26, color=MU).next_to(ax, UP, buff=0.2)
        ticks = VGroup(MathTex("1", font_size=20, color=GREY_B).next_to(ax.c2p(1, 0), DOWN, buff=0.08),
                       MathTex("1", font_size=20, color=GREY_B).next_to(ax.c2p(0, 1), LEFT, buff=0.08))
        # a cobweb for one small singular value
        s0 = float(sorted(its[0])[len(its[0]) // 2])
        web, xx = VGroup(), s0
        for _ in range(5):
            y = p(xx)
            web.add(Line(ax.c2p(xx, xx if web else 0), ax.c2p(xx, y), stroke_width=2, color=C.BITS),
                    Line(ax.c2p(xx, y), ax.c2p(min(y, 1.2), y), stroke_width=2, color=C.BITS))
            xx = y
        # right: all 256 singular values, round by round
        bx = CornerAxes(x_range=[0, 5, 1], y_range=[0, 1.3, 0.5], x_length=5.0, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.0, -0.2, 0])
        xt = VGroup(*[MathTex(str(k), font_size=20, color=GREY_B).next_to(bx.c2p(k, 0), DOWN, buff=0.08) for k in range(6)])
        xn = label(r"rounds of $p$", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"the gradient's $256$ singular values, \ scaled", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.2)
        g = np.random.default_rng(1)
        jit = g.uniform(-0.18, 0.18, len(x))
        cols = [interpolate_color(ManimColor(GREY_B), ManimColor(MU), k / 5) for k in range(6)]
        dots = [VGroup(*[Dot(bx.c2p(k + j, float(min(v, 1.3))), radius=0.025, color=cols[k]) for v, j in zip(its[k], jit)])
                for k in range(6)]
        big = before > 0.01  # every singular value above a hundredth of the largest
        lo_b, hi_b, n_b = float(its[-1][big].min()), float(its[-1][big].max()), int(big.sum())
        band = Rectangle(width=bx.c2p(5.3, 0)[0] - bx.c2p(4.7, 0)[0], height=bx.c2p(0, hi_b)[1] - bx.c2p(0, lo_b)[1],
                         stroke_color=MU, stroke_width=1.5).move_to(bx.c2p(5, (hi_b + lo_b) / 2))
        bl = label(rf"the ${n_b}$ above $1\%$ of the largest: \\ all between ${lo_b:.2f}$ and ${hi_b:.2f}$", font_size=18,
                   color=MU).next_to(band, UP, buff=0.1)
        keep_in_frame(bl)
        m_, e_ = f"{match:.0e}".split("e")
        chk = label(rf"the same as the matrix iteration's singular values, \ to ${m_} \times 10^{{{int(e_)}}}$", font_size=18,
                    color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How does Newton–Schulz do it without an SVD? Each round, X becomes a times X, plus b times X X "
            "transpose X, plus c times X X transpose squared X. On the singular values, that's just one polynomial, "
            "applied to each of them separately. <bookmark mark='a'/> Here it is, with Keller Jordan's coefficients. "
            "It rises steeply from zero, so small singular values grow fast, and it hovers around one. "
            "<bookmark mark='b'/> Follow one value: five rounds carry it up to about one. <bookmark mark='c'/> And "
            "here are all two hundred and fifty-six of our gradient's singular values, round by round. Every one "
            f"above a hundredth of the largest, {n_b} of them, ends in a band between {lo_b:.2f} and {hi_b:.2f}: not "
            "exactly one, but close enough, and the coefficients were tuned to get there in five rounds. The tiniest "
            "ones, mostly numerical dust, climb but don't arrive, which costs nothing."
        ) as vo:
            self.play(Create(ax), FadeIn(ticks), Create(diag), Create(one))
            vo.wait_until("a")
            self.play(Write(f), Create(pc), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(web), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(xt), FadeIn(xn), FadeIn(yn), FadeIn(dots[0]))
            for k in range(1, 6):
                self.play(TransformFromCopy(dots[k - 1], dots[k]), run_time=0.8)
            self.play(Create(band), FadeIn(bl), FadeIn(chk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clip(self):
        colors = {r"S^{h}_{\max}": C.SURPRISE, r"\tau": C.BITS, r"\gamma": MU}
        eqs = VGroup(
            cmath(r"S^{h}_{\max}", r"= \max_{i,j}\, \frac{q_i^{h} \cdot k_j^{h}}{\sqrt{d}}", colors=colors, font_size=34),
            cmath(r"\text{if }", r"S^{h}_{\max}", r"> \tau: \quad", r"\gamma", r"=", r"\tau", r"/", r"S^{h}_{\max}", r", \quad "
                  r"W_q^{h} \leftarrow \sqrt{", r"\gamma", r"}\, W_q^{h}, \quad W_k^{h} \leftarrow \sqrt{", r"\gamma", r"}\, W_k^{h}",
                  colors=colors, font_size=34),
        ).arrange(DOWN, buff=0.6).move_to(UP * 0.5)
        notes = VGroup(label(r"each head's largest attention score in the batch", font_size=22, color=GREY_A),
                       label(r"too large: \ shrink that head's query and key weights, \ so the score is exactly $\tau$", font_size=22,
                             color=GREY_A))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, DOWN, buff=0.15)
        res = label(r"Kimi K2: \ $\tau = 100$; \ $15.5$ trillion tokens \ with no loss spike \ (as published)", font_size=24,
                    color=C.BITS).to_edge(DOWN, buff=0.8)
        cite_ = cite(r"Kimi Team, \textit{Kimi K2: Open Agentic Intelligence} (2025): \ MuonClip", corner=DR)
        with self.voiceover(
            "Scaled up, Muon hit one problem: in some heads the attention scores kept growing until training blew up. "
            "Moonshot's fix for Kimi K2 is QK-clip. <bookmark mark='a'/> After each step, look at each head's largest "
            "score. <bookmark mark='b'/> If it's above a threshold tau, shrink that head's query and key weights by "
            "the square root of tau over the score, each, so the score lands exactly on tau. Nothing else changes. "
            "<bookmark mark='c'/> With it, Kimi K2 trained on fifteen and a half trillion tokens without a single "
            "loss spike."
        ) as vo:
            self.play(FadeIn(cite_))
            for k, mk in enumerate("ab"):
                vo.wait_until(mk)
                self.play(Write(eqs[k]), FadeIn(notes[k]))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
