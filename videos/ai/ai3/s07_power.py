from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, arrow, chapter, dots_on, load, plane

S2 = np.array([[2.0, 0.8], [0.8, 1.2]])
GPTC, LETC = C.TRUE_P, C.MODEL_Q


class Power(VoiceoverScene):
    def construct(self):
        chapter(self, 6, r"Power iteration, run live", r"How does a computer find an eigenvector?",
                "Chapter six. Power iteration: how a computer finds an eigenvector.")
        self.live()
        self.derive()
        self.measured()
        self.uses()

    # ------------------------------------------------------------------
    def live(self):
        lam, Q = np.linalg.eigh(S2)
        q = Q[:, 1] * np.sign(Q[0, 1])
        pl = plane(faded=True)
        eline = Line([*(-7 * q), 0], [*(7 * q), 0], color=C.BITS, stroke_width=2).set_opacity(0.5)
        el = MathTex(r"\text{top eigenvector}", font_size=26, color=C.BITS).move_to([*(3.6 * q), 0] + np.array([0.2, 0.55, 0]))
        el.add_background_rectangle(color=BACKGROUND, opacity=0.8, buff=0.05)
        R = 2.0
        x = np.array([math.cos(2.6), math.sin(2.6)])
        mat = MathTex(r"A = \begin{bmatrix} 2 & 0.8 \\ 0.8 & 1.2 \end{bmatrix}", font_size=34).to_corner(UL, buff=0.4)
        mat.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)
        rec = MathTex(r"\mathbf{x} \leftarrow A\mathbf{x} \,/\, |A\mathbf{x}|", font_size=36, color=C.ADVANTAGE)
        rec.next_to(mat, DOWN, buff=0.3, aligned_edge=LEFT).add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)
        cur = arrow([*(R * x), 0], color=WHITE)
        trail = VGroup()

        def readout(k, ang):
            t = MathTex(rf"\text{{step }} {k}: \ {ang:.1f}^\circ \text{{ from it}}", font_size=32)
            return t.to_corner(UR, buff=0.5).add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)

        def angle(v):
            c = abs(float(v @ q)) / np.linalg.norm(v)
            return math.degrees(math.acos(min(1.0, c)))

        rd = readout(0, angle(x))
        abel = history_card(1824, r"N.~H.~Abel \ (after P.~Ruffini, 1799)",
                            r"no formula, \ built from roots, \ solves every polynomial of degree five or more",
                            color=HIST, width=4.6).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Eigenvalues are roots of a polynomial, of degree 768 for a 768 by 768 matrix, and since Abel there is no "
            "formula beyond degree four. So computers iterate. <bookmark mark='a'/> Start anywhere, multiply by A, "
            "rescale to length one, repeat. <bookmark mark='b'/> Each multiplication favours the direction A stretches "
            "most, and the arrow swings onto the top eigenvector."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(mat), Create(eline), FadeIn(el))
            self.play(FadeIn(abel, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(abel), FadeIn(rec), GrowArrow(cur), FadeIn(rd))
            vo.wait_until("b")
            for k in range(1, 7):
                y = S2 @ x
                big = arrow([*(R * y), 0], color=C.ADVANTAGE)
                self.play(TransformFromCopy(cur, big), run_time=0.6)
                x = y / np.linalg.norm(y)
                new = arrow([*(R * x), 0], color=WHITE)
                ghost = cur.copy().set_opacity(0.25)
                trail.add(ghost)
                nrd = readout(k, angle(x))
                self.add(ghost)
                self.play(ReplacementTransform(big, new), FadeOut(cur), ReplacementTransform(rd, nrd), run_time=0.6)
                cur, rd = new, nrd
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\mathbf{v}_1": C.BITS, r"\lambda_1": C.BITS, r"\lambda_1^k": C.BITS}
        rows = [
            cmath(r"\mathbf{x}_0", "=", r"c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + \dots + c_n\mathbf{v}_n", font_size=36,
                  colors=colors),
            cmath(r"A^k\mathbf{x}_0", "=", r"c_1\lambda_1^k\mathbf{v}_1 + c_2\lambda_2^k\mathbf{v}_2 + \dots", font_size=36,
                  colors=colors),
            cmath(r"A^k\mathbf{x}_0", "=", r"\lambda_1^k\Big(c_1\mathbf{v}_1 + c_2\big(\tfrac{\lambda_2}{\lambda_1}\big)^k"
                  r"\mathbf{v}_2 + \dots\Big)", font_size=36, colors=colors),
            cmath(r"\tan\theta_k", r"\le", r"\big|\tfrac{\lambda_2}{\lambda_1}\big|^k \tan\theta_0", font_size=40,
                  colors=colors),
            cmath(r"|R(\mathbf{x}_k) - \lambda_1|", r"\lesssim", r"\big|\tfrac{\lambda_2}{\lambda_1}\big|^{2k}", font_size=36,
                  colors=colors),
        ]
        whys = [why(r"any start, \ in the eigenvector basis"), why(r"each eigenvector just stretches"),
                why(r"factor out the largest, \ $|\lambda_1| > |\lambda_2| \ge \dots$"),
                why(r"the rest shrinks geometrically"),
                why(r"symmetric $A$: \ an error of angle $\theta$ \\ moves $R$ only by about $\theta^2$")]
        step = ladder(self, rows, whys, keep=5, top=3.2, x=-1.0, buff=0.42, edge=6.9)
        with self.voiceover(
            "Why it works takes four lines. <bookmark mark='a'/> Write the start in the eigenvector basis. "
            "<bookmark mark='b'/> k multiplications stretch each part by its eigenvalue to the k. <bookmark mark='c'/> "
            "Pull out the largest: every other part is multiplied by a ratio below one, to the k. <bookmark mark='d'/> "
            "So the angle shrinks like lambda two over lambda one, to the k: a straight line on a log scale. "
            "<bookmark mark='e'/> The eigenvalue estimate does twice as well, because the Rayleigh quotient sits at a "
            "maximum, where small errors in direction barely move it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0], scale_factor=1.03))
            for k, mk in enumerate("bcde", start=1):
                vo.wait_until(mk)
                step(k)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        p = load("power")
        g = axes([0, 60, 10], [-16, 0.5, 4], x_length=8.0, y_length=4.4, xticks=[0, 10, 20, 30, 40, 50, 60],
                 yticks=[-16, -12, -8, -4, 0], yfmt=lambda v: f"10^{{{int(v)}}}" if v else "1",
                 xlabel=r"step $k$", ylabel=r"$\sin\theta_k$, \ the angle to the top eigenvector",
                 center=[-1.3, -0.2, 0])
        ax = g.ax
        series = []
        for key, col, name in (("gpt2", GPTC, r"GPT-2's token covariance ($768 \times 768$)"),
                               ("letters", LETC, r"the letter table's $M^{\top}M$ ($26 \times 26$)")):
            d = p[key]
            s = np.maximum(np.asarray(d["sin"]), 1e-17)
            ks = np.arange(len(s))
            ok = s > 3e-16
            lines = VGroup(curve(ax, ks[ok], np.log10(s[ok]), col, 3), dots_on(ax, ks[ok], np.log10(s[ok]), col, 0.04))
            pred = np.log10(np.maximum(np.asarray(d["pred_tan"]), 1e-17))
            okp = pred > -16
            pl = DashedLine(ax.c2p(0, pred[0]), ax.c2p(ks[okp][-1], pred[okp][-1]), color=col, stroke_width=2)
            series.append((lines, pl, d, name, col))
        leg = VGroup(*[label(rf"{nm}: \ $\lambda_2/\lambda_1 = {d['ratio']:.3f}$, \ measured rate ${d['rate_measured']:.3f}$",
                             font_size=22, color=col) for _, _, d, nm, col in series]).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.12)
        leg.to_edge(DOWN, buff=0.12)
        key = VGroup(DashedLine(LEFT * 0.3, RIGHT * 0.3, color=GREY_B), label(r"predicted $(\lambda_2/\lambda_1)^k$",
                                                                             font_size=22, color=GREY_B)).arrange(RIGHT)
        key.to_corner(UR, buff=0.5)
        floor = note(r"round-off: $\approx 10^{-16}$").next_to(ax.c2p(60, -15.5), UP, buff=0.05).align_to(ax.c2p(60, 0), RIGHT)
        dg, dl = p["gpt2"], p["letters"]
        s0 = dg["sin"][0]
        verdict = ("both match the prediction to two decimal places"
                   if abs(dg["rate_measured"] - dg["ratio"]) < 0.01 and abs(dl["rate_measured"] - dl["ratio"]) < 0.01
                   else "close to the prediction")
        with self.voiceover(
            "Now real matrices. <bookmark mark='a'/> The covariance of GPT-2's 50,257 token vectors, 768 by 768: its "
            f"top two eigenvalues have a ratio of {dg['ratio']:.3f}, and the error falls by {dg['rate_measured']:.3f} "
            "per step, down to the machine's rounding. The random start was almost perpendicular to the answer, a sine "
            f"of {s0:.4f}; chapter fourteen explains why. <bookmark mark='b'/> Part 1's letter table: a ratio of "
            f"{dl['ratio']:.3f}, and measured, {dl['rate_measured']:.3f}. <bookmark mark='c'/> Dashed, the prediction: "
            f"{verdict}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(key), FadeIn(floor))
            vo.wait_until("a")
            self.play(Create(series[0][0]), Create(series[0][1]), FadeIn(leg[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(series[1][0]), Create(series[1][1]), FadeIn(leg[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(series[0][1], color=WHITE), Indicate(series[1][1], color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        cards = VGroup(
            history_card(1929, r"R.~von Mises \& H.~Pollaczek-Geiringer",
                         r"the power method, \ for the eigenvalues of engineering problems", color=HIST, width=4.3, font_size=30),
            history_card(1998, r"S.~Brin \& L.~Page, \ PageRank",
                         r"a web page's rank is the top eigenvector of the link matrix, \ found by power iteration",
                         color=HIST, width=4.3, font_size=30),
            history_card(2018, r"T.~Miyato et al., \ spectral normalization",
                         r"one power-iteration step per training step estimates each layer's largest stretch",
                         color=HIST, width=4.3, font_size=30),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP)
        cards.move_to(DOWN * 0.1)
        head = label(r"Power iteration at work", font_size=40).to_edge(UP, buff=0.4)
        tail = label(r"today's libraries: \ Krylov methods (Lanczos, 1950), \ power iteration's refinement",
                     font_size=28, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The method is from 1929, by Richard von Mises and Hilda Pollaczek-Geiringer. <bookmark mark='a'/> In 1998 "
            "it ranked the web: PageRank is the top eigenvector of a matrix of links. <bookmark mark='b'/> In 2018, "
            "spectral normalization ran one power step per training step to keep layers from stretching too much. "
            "<bookmark mark='c'/> And today's library routines are its refinement: Krylov methods, after Cornelius "
            "Lanczos in 1950."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()
