from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import BAD, DATA, FIT, GOOD, HL, chapter, hbars, load, plot, sci_tex, side_ladder

OLS, END, TS = FIT, "#B48EF0", "#4FD1C5"


class GaussMarkov(VoiceoverScene):
    def construct(self):
        chapter(self, 2, r"The best linear unbiased line", r"Why squares, and not something else?",
                "Chapter two. Why least squares is the best of its kind.")
        self.theorem()
        self.simulate()
        self.compute_it()

    # ------------------------------------------------------------------
    def theorem(self):
        card = theorem_card(r"Gauss--Markov",
                            r"If the noise has mean $0$, the same variance $\sigma^2$ everywhere, and no correlation, "
                            r"then among all \emph{linear unbiased} estimates of $\boldsymbol\beta$, least squares has "
                            r"the smallest variance.", who=r"Gauss (1821); \ Markov (1900)", width=9.6, font_size=22)
        card.to_edge(UP, buff=0.25)
        colors = {r"\hat{\boldsymbol\beta}": OLS, r"\tilde{\boldsymbol\beta}": END, "D": END}
        rows = [
            cmath(r"\tilde{\boldsymbol\beta}", "=", r"\big((A^{\top}A)^{-1}A^{\top} + D\big)\,\mathbf{y}", colors=colors,
                  font_size=34),
            cmath(r"\mathbb{E}\,\tilde{\boldsymbol\beta}", "=", r"\boldsymbol\beta + DA\boldsymbol\beta", r"\;\Rightarrow\; DA = 0",
                  colors=colors, font_size=34),
            cmath(r"\operatorname{Var}\tilde{\boldsymbol\beta}", "=",
                  r"\sigma^2\big((A^{\top}A)^{-1}A^{\top} + D\big)\big(\cdots\big)^{\top}", colors=colors, font_size=34),
            cmath(r"\operatorname{Var}\tilde{\boldsymbol\beta}", "=", r"\sigma^2(A^{\top}A)^{-1}", "+", r"\sigma^2 DD^{\top}",
                  colors=colors, font_size=34),
            cmath(r"\operatorname{Var}\tilde{\boldsymbol\beta}", r"\succeq", r"\operatorname{Var}\hat{\boldsymbol\beta}",
                  colors=colors, font_size=34),
        ]
        whys = [why(r"any linear estimate: \\ least squares plus $D$"), why(r"unbiased for every $\boldsymbol\beta$"),
                why(r"$\operatorname{Var}\mathbf{y} = \sigma^2 I$"), why(r"cross terms vanish: \\ $DA = 0$"),
                why(r"$DD^{\top}$ is never negative")]
        step = ladder(self, rows, whys, keep=5, top=1.35, x=-1.6, buff=0.3, edge=6.8)
        with self.voiceover(
            "And if the noise isn't a bell? Gauss gave a second answer in 1821, and Markov rediscovered it: least "
            "squares is still the best linear unbiased estimate. <bookmark mark='a'/> Take any "
            "other estimate that's linear in the data: least squares, plus some matrix D. <bookmark mark='b'/> For "
            "it to be right on average, whatever the true line, D times A must vanish. <bookmark mark='c'/> Its "
            "spread is sigma squared times the matrix times its transpose. <bookmark mark='d'/> Multiply out: the "
            "cross terms contain D A, so they vanish, and what's left is least squares' spread plus D D transpose. "
            "<bookmark mark='e'/> That can only add. Every other linear unbiased estimate wobbles more."
        ) as vo:
            self.play(FadeIn(card, shift=DOWN * 0.2))
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=END, scale_factor=1.05))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(Indicate(rows[4], color=HL))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simulate(self):
        gm = load("gaussmarkov")
        x = np.asarray(gm["x"])
        b0, b1 = gm["beta"]
        Y = np.asarray(gm["samples"])
        w_ols, w_end = np.asarray(gm["w_ols"]), np.asarray(gm["w_end"])
        G, T = gm["gauss"], gm["theory"]
        left = plot([0, 11, 1], [-1, 8, 1], x_length=5.2, y_length=3.6, xticks=[0, 5, 10], yticks=[0, 4, 8],
                    center=[-3.9, 0.6, 0], xlabel=r"$x$", ylabel=r"$y$")
        ax = left.ax
        true_l = Line(ax.c2p(0, b0), ax.c2p(11, b0 + 11 * b1), color=GREY_B, stroke_width=2).set_opacity(0.6)

        def fits(k):
            y = Y[k]
            s_o, s_e = float(w_ols @ y), float(w_end @ y)
            i_o = float(y.mean() - s_o * x.mean())
            i_e = float(y[0] - s_e * x[0])
            dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.055, color=DATA) for a, b in zip(x, y)])
            lo = Line(ax.c2p(0, i_o), ax.c2p(11, i_o + 11 * s_o), color=OLS, stroke_width=3.5)
            le = Line(ax.c2p(0, i_e), ax.c2p(11, i_e + 11 * s_e), color=END, stroke_width=3)
            ends = VGroup(Circle(radius=0.11, color=END, stroke_width=2).move_to(dots[0]),
                          Circle(radius=0.11, color=END, stroke_width=2).move_to(dots[-1]))
            return VGroup(dots, lo, le, ends)

        cur = fits(0)
        key = VGroup(label(r"least squares", font_size=22, color=OLS),
                     label(r"the line through the two end points", font_size=22, color=END),
                     label(r"the true line", font_size=22, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        key.next_to(left, DOWN, buff=0.25).align_to(left, LEFT)
        bins = np.asarray(gm["hist_bins"])
        h_o, h_e = np.asarray(gm["hist_ols"]), np.asarray(gm["hist_end"])
        top = float(max(h_o.max(), h_e.max())) * 1.08
        right = plot([bins[0], bins[-1], 0.1], [0, top, top], x_length=5.6, y_length=3.0, xticks=[0.2, 0.5, 0.8],
                     center=[3.4, 0.9, 0], xlabel=rf"the slope, \ from ${gm['R']:,}$ data sets".replace(",", "{,}"))
        rax = right.ax

        def hist(h, col, op):
            g = VGroup()
            for a, b, c_ in zip(bins[:-1], bins[1:], h):
                if c_ <= 0:
                    continue
                p0, p1 = rax.c2p(a, 0), rax.c2p(b, c_)
                g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                fill_opacity=op).move_to((p0 + p1) / 2))
            return g

        ho, he = hist(h_o, OLS, 0.75), hist(h_e, END, 0.45)
        truth = DashedLine(rax.c2p(b1, 0), rax.c2p(b1, top), color=WHITE, stroke_width=2)
        ratio = G["end"]["var"] / G["ols"]["var"]
        reads = VGroup(
            label(rf"least squares: \ variance ${G['ols']['var']:.4f}$ \ (theory ${T['ols']:.4f}$)", font_size=22, color=OLS),
            label(rf"end points: \ ${G['end']['var']:.4f}$ \ (theory ${T['end']:.4f}$)", font_size=22, color=END),
            label(rf"averages: \ ${G['ols']['mean']:.3f}$ and ${G['end']['mean']:.3f}$; \ true slope ${b1:g}$",
                  font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        reads.next_to(right, DOWN, buff=0.25).align_to(right, LEFT)
        H = gm["t3"]
        ts_g, ts_h = G["ts"]["var"], H["ts"]["var"]
        beats = ts_h < H["ols"]["var"]
        vb = hbars([(r"least squares, \ bell-shaped noise", G["ols"]["var"], OLS),
                    (r"Theil--Sen, \ bell-shaped noise", ts_g, TS),
                    (r"least squares, \ heavy tails", H["ols"]["var"], OLS),
                    (r"Theil--Sen, \ heavy tails", ts_h, TS)], width=3.4, lo=0.0, hi=0.0125, font_size=20,
                   fmt=lambda v: f"{v:.4f}", name_width=3.6)
        vbh = label(r"variance of the slope", font_size=24, color=GREY_A)
        vbox = VGroup(vbh, vb).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([-3.4, 0.4, 0])
        tsn = label(r"Theil--Sen (1950, 1968): \ the median of all $66$ pairwise slopes, \ not linear in $\mathbf{y}$",
                    font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        verdict = (f"With heavy-tailed noise of the same variance, though, it wins: {ts_h:.4f} against "
                   f"{H['ols']['var']:.4f}. Gauss-Markov only promises the best of the linear estimates."
                   if beats else
                   f"Even with heavy-tailed noise it doesn't win here: {ts_h:.4f} against {H['ols']['var']:.4f}.")
        with self.voiceover(
            "Let's check. Twelve points on the same twelve x's, with fresh noise each time. <bookmark mark='a'/> "
            "Fit them by least squares, and also by the line through the two end points, which is also linear and "
            f"unbiased. <bookmark mark='b'/> Over {gm['R']:,} data sets, both slopes average out at the truth, but "
            f"least squares' spread is {G['ols']['var']:.4f}, matching the theory, and the end points' is "
            f"{ratio:.1f} times larger."
        ) as vo:
            self.play(FadeIn(left), Create(true_l), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(cur))
            for k in range(1, 6):
                nxt = fits(k)
                self.play(Transform(cur, nxt), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(he), FadeIn(ho), Create(truth))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in reads], lag_ratio=0.3))
        with self.voiceover(
            "Now step outside the rules. Theil and Sen's estimate takes the median of all the pairwise slopes: it "
            f"isn't linear in the data. <bookmark mark='a'/> With bell-shaped noise it loses, {ts_g:.4f} against "
            f"{G['ols']['var']:.4f}. <bookmark mark='b'/> {verdict}"
        ) as vo:
            self.play(FadeOut(VGroup(left, true_l, cur, key)), FadeIn(tsn))
            self.play(FadeIn(vbh))
            vo.wait_until("a")
            self.play(FadeIn(vb[0]), FadeIn(vb[1]))
            vo.wait_until("b")
            self.play(FadeIn(vb[2]), FadeIn(vb[3]))
            self.play(Indicate(vb[3] if beats else vb[2], color=HL))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compute_it(self):
        ls = load("lsq")
        p = load("pages")
        n_te = int(np.asarray(p["test"], bool).sum())
        colors = {r"A^{+}": HL, r"\Sigma^{+}": HL}
        rows = [
            cmath(r"A^{\top}A\,\hat{\boldsymbol\beta}", "=", r"A^{\top}\mathbf{y}", font_size=34, colors=colors),
            cmath(r"\kappa(A^{\top}A)", "=", r"\kappa(A)^2", font_size=34, colors=colors),
            cmath(r"A", "=", r"QR \;\Rightarrow\; R\,\hat{\boldsymbol\beta} = Q^{\top}\mathbf{y}", font_size=34,
                  colors=colors),
            cmath(r"\hat{\boldsymbol\beta}", "=", r"A^{+}\mathbf{y} = V\Sigma^{+}U^{\top}\mathbf{y}", font_size=34,
                  colors=colors),
        ]
        whys = [why(r"the normal equations"), why(r"squaring loses digits \\ (Part 3)"),
                why(r"Householder: \\ no squaring"), why(r"the pseudoinverse: \\ the shortest answer")]
        step = side_ladder(self, rows, whys, -2.7, 4.0, keep=4, top=3.2, buff=0.3)
        kappa = VGroup(label(rf"the pages, $70$ rates and a constant: \ $\kappa(A) = {ls['kappa_A']:.1f}$, \ "
                             rf"$\kappa(A^{{\top}}A) = {ls['kappa_AtA']:.0f}$", font_size=22, color=GREY_A),
                       label(rf"normal equations and QR agree to within ${sci_tex(ls['diff_ne_qr'])}$", font_size=22,
                             color=GREY_A))
        kappa.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.4)
        # the duplicated column
        wn, wa, wb = ls["w_not"], ls["w_not_a"], ls["w_not_b"]
        scale = 1.6 / abs(wn)

        def bar(v, col, x):
            h = abs(v) * scale
            return Rectangle(width=0.6, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [x, 0.6 - h / 2, 0])

        base = Line([2.4, 0.6, 0], [6.6, 0.6, 0], color=GREY_C, stroke_width=1.5)
        b1 = bar(wn, HL, 3.2)
        b2, b3 = bar(wa, HL, 4.9), bar(wb, HL, 5.8)
        l1 = label(r"``not''", font_size=22, color=GREY_A).next_to(b1, DOWN, buff=0.1)
        l23 = VGroup(label(r"``not''", font_size=22, color=GREY_A).next_to(b2, DOWN, buff=0.1),
                     label(r"its copy", font_size=22, color=GREY_A).next_to(b3, DOWN, buff=0.1))
        v1 = MathTex(f"{wn:.3f}", font_size=24, color=HL).next_to(base, UP, buff=0.1).set_x(3.2)
        v23 = VGroup(MathTex(f"{wa:.3f}", font_size=24, color=HL).next_to(base, UP, buff=0.1).set_x(4.9),
                     MathTex(f"{wb:.3f}", font_size=24, color=HL).next_to(base, UP, buff=0.1).set_x(5.8))
        dup_h = label(r"put ``not'' in twice", font_size=26).move_to([4.5, 2.6, 0])
        rank = label(rf"rank ${ls['rank_dup']}$ of ${ls['cols_dup']}$ columns: \ $A^{{\top}}A$ is singular",
                     font_size=22, color=GREY_A).next_to(dup_h, DOWN, buff=0.15)
        if ls["ne_dup"] == "solved":
            big = int(math.floor(math.log10(max(ls["ne_dup_norm"], 1.0))))
            ne_txt = rf"normal equations: \ weights of size $10^{{{big}}}$"
            ne_say = (f"Solving the normal equations anyway gives weights of size ten to the {big}: rounding error, "
                      "magnified.")
        else:
            ne_txt = r"normal equations: \ no solution found"
            ne_say = "The normal equations can't be solved at all."
        ne = label(ne_txt, font_size=22, color=BAD).move_to([4.5, -2.3, 0])
        pi = label(r"pseudoinverse: \ the weight split in half", font_size=22, color=GOOD).next_to(ne, DOWN, buff=0.15)
        cls = label(rf"least squares as a classifier, \ all $70$ rates: \ ${round(ls['acc_test'] * n_te)}$ of ${n_te}$ "
                    r"held-out pages", font_size=24, color=HL).to_edge(UP, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "How should a computer solve it? Part 3 built the tools. <bookmark mark='a'/> The normal equations are "
            "quick, <bookmark mark='b'/> but forming A transpose A squares the condition number, and each factor of ten "
            "costs a digit. On the pages it's mild: "
            f"{ls['kappa_A']:.1f}, squared to {ls['kappa_AtA']:.0f}. <bookmark mark='c'/> QR solves the same problem "
            "without squaring. <bookmark mark='d'/> And when columns repeat, the pseudoinverse picks the shortest of "
            "all the best answers."
        ) as vo:
            self.play(FadeIn(cls))
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=HL, scale_factor=1.05))
            vo.wait_until("b")
            step(1)
            self.play(FadeIn(kappa))
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        with self.voiceover(
            "Put the word 'not' into the table twice. <bookmark mark='a'/> Now two columns are the same, and A transpose "
            f"A can't be inverted. {ne_say} <bookmark mark='b'/> The pseudoinverse instead splits 'not's weight "
            f"exactly in half, {wa:.3f} and {wb:.3f}, and makes the same predictions as before."
        ) as vo:
            self.play(FadeIn(dup_h), Create(base), GrowFromEdge(b1, UP), FadeIn(l1), FadeIn(v1))
            vo.wait_until("a")
            self.play(FadeIn(rank), FadeIn(ne))
            vo.wait_until("b")
            self.play(ReplacementTransform(b1.copy(), b2), ReplacementTransform(b1.copy(), b3), FadeIn(l23), FadeIn(v23),
                      FadeIn(pi))
        self.wait(0.3)
        self.clear_scene()
