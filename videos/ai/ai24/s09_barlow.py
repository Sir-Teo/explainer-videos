from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (BARLOW, HIST, NAIVE, PART, SIMCLR, VICREG_C, axes, bars_chart, curve, heat, load,
                                   pct, take_away)

INV = "#5BD17A"
RED = "#FF9F45"


class Barlow(VoiceoverScene):
    def construct(self):
        self.card()
        self.barlow()
        self.replay()
        self.vicreg()
        self.duality()

    def card(self):
        card = chapter_card(8, r"Decorrelate: \ Barlow Twins and VICReg", r"Can we forbid collapse directly?",
                            lit=(1961,), part=PART)
        with self.voiceover("Chapter eight. Decorrelate: Barlow Twins and VICReg."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def barlow(self):
        hc = history_card(1961, r"Horace Barlow", r"proposed that sensory neurons recode their input to reduce its "
                          r"redundancy: \ each should carry something the others don't", color=HIST, width=5.4)
        hc.move_to([-3.8, 1.6, 0])
        f = MathTex(r"\mathcal L_{\rm BT}", r"=", r"\sum_i \big(1 - \mathcal C_{ii}\big)^2", r"+",
                    r"\lambda \sum_i \sum_{j \ne i} \mathcal C_{ij}^{\,2}", font_size=40).move_to([0.8, -0.6, 0])
        f[2].set_color(INV)
        f[4].set_color(RED)
        cdef = MathTex(r"\mathcal C_{ij}", r"=", r"\frac{\sum_b z^A_{b,i}\, z^B_{b,j}}{\sqrt{\sum_b (z^A_{b,i})^2}"
                       r"\sqrt{\sum_b (z^B_{b,j})^2}}", font_size=32).move_to([3.6, 1.7, 0])
        cl = label(r"the correlation of dimension $i$ of one view \\ with dimension $j$ of the other, \ over the batch",
                   font_size=20, color=GREY_A).next_to(cdef, DOWN, buff=0.2)
        b1 = brace_note(f[2], r"each dimension: \ the same for both views", color=INV, font_size=22)
        b2 = brace_note(f[4], r"different dimensions: \ uncorrelated", color=RED, font_size=22)
        src = cite(r"Barlow (1961); \ Zbontar, Jing, Misra, LeCun \& Deny (2021)")
        with self.voiceover(
            "In 1961 the neuroscientist Horace Barlow argued that the senses should recode their input so that each "
            "neuron carries something the others do not. <bookmark mark='a'/> Sixty years later, Jure Zbontar, Li "
            "Jing, Ishan Misra, Yann LeCun and Stéphane Deny named a method after him. Run both views of a batch "
            "through the network, and correlate every output dimension of one view with every dimension of the "
            "other. <bookmark mark='b'/> The loss wants this matrix to be the identity. On the diagonal, each "
            "dimension must agree between the views: invariance. <bookmark mark='c'/> Off the diagonal, different "
            "dimensions must be uncorrelated: no redundancy. A constant output cannot satisfy the diagonal, because "
            "a correlation needs variation. Collapse is ruled out by the loss itself."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(src))
            vo.wait_until("a")
            self.play(Write(cdef), FadeIn(cl))
            vo.wait_until("b")
            self.play(Write(f[:3]), FadeIn(b1))
            vo.wait_until("c")
            self.play(Write(f[3:]), FadeIn(b2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        r = load("redundancy")
        Cs = np.asarray(r["rec_C"])
        dg, off = np.asarray(r["rec_diag"]), np.asarray(r["rec_off"])
        steps = np.asarray(r["rec_steps"])
        n = len(steps)
        tr = ValueTracker(0)
        S = 4.6

        def mat():
            i = int(np.clip(round(tr.get_value()), 0, n - 1))
            return heat(Cs[i], S, S, vmax=1.0, signed=True, pos=INV, neg=RED).move_to([-3.0, -0.3, 0])

        hm = always_redraw(mat)
        frame = Square(S, color=GREY_D, stroke_width=1.5).move_to([-3.0, -0.3, 0])
        cap = label(r"$\mathcal C$, \ the first $24$ of $512$ dimensions", font_size=22, color=GREY_A).next_to(
            frame, UP, buff=0.15)
        st = always_redraw(lambda: label(rf"step ${steps[int(np.clip(round(tr.get_value()), 0, n - 1))]}$",
                                         font_size=22, color=GREY_A).next_to(frame, DOWN, buff=0.15))
        ax = axes([0, n - 1], [0, 1.0], x_length=4.4, y_length=3.0, xlabel=r"snapshot", yticks=[0, 0.5, 1],
                  center=[3.6, -0.3, 0])
        cd = curve(ax.ax, np.arange(n), dg, INV, 3)
        co = curve(ax.ax, np.arange(n), np.sqrt(off) * 10, RED, 3)
        leg = VGroup(label(r"mean of the diagonal", font_size=20, color=INV),
                     label(r"off the diagonal: \ rms $\times 10$", font_size=20, color=RED)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, UP, buff=0.15)
        tg = tag(r"computed: \ Barlow Twins, \ $512$ output dimensions, \ $\lambda = 0.005$")
        with self.voiceover(
            "Here is the matrix in our Barlow Twins, for the first twenty-four of its five hundred and twelve "
            "dimensions, measured on test digits as it trains. <bookmark mark='a'/> At first it is noise. "
            "<bookmark mark='b'/> The diagonal brightens as each dimension learns to ignore the changes between "
            f"views, reaching an average correlation of {dg[-1]:.2f}, <bookmark mark='c'/> and the rest goes dark, "
            f"with typical off-diagonal correlations of {np.sqrt(off[-1]):.3f}. Five hundred and twelve "
            "dimensions, each saying something different, each stable under the views."
        ) as vo:
            self.play(FadeIn(hm), Create(frame), FadeIn(cap), FadeIn(st), FadeIn(tg))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(leg))
            vo.wait_until("b")
            self.play(tr.animate.set_value(n - 1), Create(cd), Create(co), run_time=max(3.0, vo.until("c")),
                      rate_func=linear)
        for m in (hm, st):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vicreg(self):
        r = load("redundancy")
        runs, K = r["runs"], r["keys"]
        f = MathTex(r"\lambda\, \|z - z'\|^2", r"+", r"\mu \sum_j \max\big(0,\, 1 - \mathrm{std}(z_j)\big)", r"+",
                    r"\nu \sum_{i \ne j} \mathrm{Cov}(z)_{ij}^{\,2}", font_size=34).to_edge(UP, buff=0.6)
        f[0].set_color(INV)
        f[2].set_color(VICREG_C)
        f[4].set_color(RED)
        names = VGroup(label(r"invariance", font_size=22, color=INV).next_to(f[0], DOWN, buff=0.15),
                       label(r"variance: \ every dimension keeps a spread of at least 1", font_size=22,
                             color=VICREG_C).next_to(f[2], DOWN, buff=0.15),
                       label(r"covariance", font_size=22, color=RED).next_to(f[4], DOWN, buff=0.15))
        S_ = runs[K["vicreg"][0]]["steps"][-1]

        def std_curve(k):
            r_ = runs[k]
            xs = [s for s, lg in zip(r_["steps"], r_["logs"]) if lg]
            ys = [max(0.0, 1 - lg["var"]) for lg in r_["logs"] if lg]
            return xs, ys

        ax = axes([0, S_], [0, 1.1], x_length=5.6, y_length=3.0, xlabel=r"training step",
                  ylabel=r"typical std of a dimension (up to 1)", xticks=[0, S_], yticks=[0, 0.5, 1],
                  center=[-2.6, -1.3, 0])
        cv = VGroup(*[curve(ax.ax, *std_curve(k), VICREG_C, 3 if i == 0 else 1.8) for i, k in enumerate(K["vicreg"])])
        cn = VGroup(*[curve(ax.ax, *std_curve(k), NAIVE, 3 if i == 0 else 1.8) for i, k in enumerate(K["vicreg_novar"])])
        leg = VGroup(label(r"VICReg", font_size=20, color=VICREG_C),
                     label(r"without the variance term", font_size=20, color=NAIVE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.2, -0.4, 0])
        s_v = float(np.mean([std_curve(k)[1][-1] for k in K["vicreg"]]))
        s_n = float(np.mean([std_curve(k)[1][-1] for k in K["vicreg_novar"]]))
        kn = float(np.mean([runs[k]["final"]["knn"] for k in K["vicreg_novar"]]))
        kv = float(np.mean([runs[k]["final"]["knn"] for k in K["vicreg"]]))
        collapsed = s_n < 0.2 * max(s_v, 1e-6)
        v = (f"Without it, the spread of each dimension falls to {s_n:.3f}: the other two terms are happiest with "
             f"everything at zero, and the network obliges. Its nearest-neighbour accuracy ends at {pct(kn)} percent, "
             f"against {pct(kv)} for VICReg." if collapsed else
             f"Without it, the spread ends at {s_n:.2f}, against {s_v:.2f}.")
        src = cite(r"Bardes, Ponce \& LeCun (2022): \ VICReg; \ $\lambda = \mu = 25$, \ $\nu = 1$", corner=DR)
        with self.voiceover(
            "VICReg, from Adrien Bardes, Jean Ponce and Yann LeCun, splits the same idea into three named terms. "
            "<bookmark mark='a'/> Invariance: the two views' vectors should be close. <bookmark mark='b'/> "
            "Variance: every dimension must keep a standard deviation of at least one across the batch, a hinge "
            "that only bites when a dimension starts to collapse. <bookmark mark='c'/> Covariance: different "
            "dimensions should not be correlated. <bookmark mark='d'/> Each term can be removed to see what it "
            f"does, so we removed the variance term. {v}"
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(Write(f[0]), FadeIn(names[0]))
            vo.wait_until("b")
            self.play(Write(f[1:3]), FadeIn(names[1]))
            vo.wait_until("c")
            self.play(Write(f[3:]), FadeIn(names[2]))
            vo.wait_until("d")
            self.play(FadeIn(ax), FadeIn(leg), Create(cv), Create(cn), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def duality(self):
        r = load("redundancy")
        s = load("simclr")
        rng = np.random.default_rng(1)
        # schematic: a batch's similarity matrix (samples x samples) and a correlation matrix (dimensions x dims)
        Ms = np.eye(16) * 0.9 + rng.normal(0, 0.08, (16, 16))
        Md = np.asarray(r["rec_C"])[-1][:16, :16]
        m1 = heat(Ms, 2.6, 2.6, vmax=1.0, pos=SIMCLR, neg=RED).move_to([-4.6, 0.9, 0])
        m2 = heat(Md, 2.6, 2.6, vmax=1.0, pos=BARLOW, neg=RED).move_to([-1.4, 0.9, 0])
        l1 = label(r"contrastive: \\ images $\times$ images", font_size=20, color=SIMCLR).next_to(m1, DOWN, buff=0.15)
        l2 = label(r"Barlow, VICReg: \\ dimensions $\times$ dimensions", font_size=20, color=BARLOW).next_to(
            m2, DOWN, buff=0.15)
        sch = note(r"left: schematic; \ right: our Barlow Twins", font_size=18).next_to(VGroup(l1, l2), DOWN, buff=0.2)
        src = cite(r"Garrido et al.\ (2023); \ Balestriero \& LeCun (2025): \ LeJEPA")
        names = [r"SimCLR", r"Barlow Twins", r"VICReg"]
        lin = [s["summary"]["0.2"]["linear"], r["summary"]["barlow"]["linear"], r["summary"]["vicreg"]["linear"]]
        lo = float(np.floor((min(x[1] for x in lin) - 0.01) * 100) / 100)
        ch = bars_chart([x[0] for x in lin], [SIMCLR, BARLOW, VICREG_C], names, height=2.6, bar_w=0.8, gap=0.5,
                        vmin=lo, vmax=1.0, spread=[(x[1], x[2]) for x in lin], value_fmt=lambda v: pct(v),
                        font_size=20).move_to([3.9, 0.4, 0])
        cl = label(rf"linear probe, \% \ (from ${pct(lo, 0)}$)", font_size=20, color=GREY_A).next_to(ch, UP, buff=0.25)
        sig = label(r"LeJEPA (2025): \ push the vectors toward an isotropic Gaussian; \ no stop-gradient, \ no teacher; "
                    r"\\ ViT-H/14 on ImageNet: \ $79\%$ linear probe", font_size=21, color=GREY_A).to_edge(DOWN,
                                                                                                        buff=0.6)
        bt, vr, sc = lin[1][0], lin[2][0], lin[0][0]
        line = ("On our digits, Barlow Twins and VICReg match SimCLR to within a point."
                if max(abs(bt - sc), abs(vr - sc)) < 0.01 else
                f"On our digits: SimCLR {pct(sc)}, Barlow Twins {pct(bt)}, VICReg {pct(vr)} percent.")
        with self.voiceover(
            "The two families are closer than they look. A contrastive loss makes the images in a batch "
            "dissimilar from each other; Barlow Twins and VICReg make the dimensions dissimilar from each other. "
            "<bookmark mark='a'/> Quentin Garrido and colleagues showed that, written out, the two are nearly the "
            f"same objective, one acting on the rows of the data and the other on the columns. <bookmark "
            f"mark='b'/> {line} <bookmark mark='c'/> The latest of this line is LeJEPA, from Randall Balestriero and "
            "Yann LeCun in 2025: push the vectors toward an isotropic Gaussian and nothing else, no stop-gradient, no "
            "teacher."
        ) as vo:
            self.play(FadeIn(m1), FadeIn(m2), FadeIn(l1), FadeIn(l2), FadeIn(sch), FadeIn(src))
            vo.wait_until("a")
            self.play(Indicate(VGroup(m1, m2), scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(cl), FadeIn(ch))
            vo.wait_until("c")
            self.play(FadeIn(sig, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
